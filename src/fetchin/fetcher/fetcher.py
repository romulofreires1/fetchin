import requests
import pybreaker
import time
from ..metrics import MetricsInterface


class Fetcher:
    circuit_breakers = {}

    def __init__(
        self,
        label: str,
        logger=None,
        metrics: MetricsInterface = None,
        circuit_config: dict = None,
        max_retries: int = 3,
    ):
        self.label = label
        self.logger = logger
        self.metrics = metrics
        self.max_retries = max_retries

        self.circuit_breaker = self._initialize_circuit_breaker(label, circuit_config)

    def _initialize_circuit_breaker(self, label: str, circuit_config: dict):
        default_config = {
            "fail_max": 3,
            "reset_timeout": 60,
        }

        if circuit_config:
            default_config.update(circuit_config)

        if label not in Fetcher.circuit_breakers:
            Fetcher.circuit_breakers[label] = pybreaker.CircuitBreaker(
                fail_max=default_config["fail_max"],
                reset_timeout=default_config["reset_timeout"],
                state_storage=pybreaker.CircuitMemoryStorage(
                    state=pybreaker.STATE_CLOSED
                ),
            )

        return Fetcher.circuit_breakers[label]

    def _log(self, level: str, message: str, extra=None):
        if self.logger:
            log_method = getattr(self.logger, level, None)
            if log_method:
                log_method(message, extra=extra)

    def _track(
        self,
        method: str,
        status_code: int = None,
        response_time: float = None,
        is_retry: bool = False,
    ):
        if self.metrics:
            if is_retry:
                self.metrics.track_retry(method)
            else:
                self.metrics.track_request(method, status_code, response_time)

    def _perform_request_with_retries(self, method: str, url: str, **kwargs):
        attempt, start_time = 0, time.time()

        while attempt < self.max_retries:
            attempt += 1
            try:
                response = self.circuit_breaker.call(
                    requests.request, method, url, **kwargs
                )
                response_time = time.time() - start_time

                self._log(
                    "info",
                    f"Response received: {response.status_code}",
                    extra={
                        "url": url,
                        "status_code": response.status_code,
                        "fetcher_label": self.label,
                    },
                )
                self._track(method, response.status_code, response_time)

                if self.circuit_breaker.current_state == pybreaker.STATE_HALF_OPEN:
                    self.circuit_breaker.close()

                return response
            except pybreaker.CircuitBreakerError as e:
                self._log(
                    "error",
                    f"Circuit breaker open: {e}",
                    extra={"url": url, "error_message": str(e)},
                )
                self._track(method, status_code=500, response_time=0)
                raise e
            except Exception as e:
                self._log(
                    "error",
                    f"Attempt {attempt} failed: {e}",
                    extra={"url": url, "error_message": str(e)},
                )

                if self.circuit_breaker.current_state == pybreaker.STATE_HALF_OPEN:
                    self.circuit_breaker.open()

                if attempt < self.max_retries:
                    # Track retry attempt
                    self._track(method, is_retry=True)
                    time.sleep(self.default_backoff_strategy(attempt))
                else:
                    raise e

    def _handle_request(self, method: str, url: str, **kwargs):
        self._log(
            "info",
            f"{method} request to {url}",
            extra={"url": url, "fetcher_label": self.label},
        )
        return self._perform_request_with_retries(method, url, **kwargs)

    def default_backoff_strategy(self, attempt: int):
        return 2**attempt

    def get(self, url: str, **kwargs):
        return self._handle_request("GET", url, **kwargs)

    def post(self, url: str, data: dict = None, **kwargs):
        return self._handle_request("POST", url, json=data, **kwargs)

    def delete(self, url: str, **kwargs):
        return self._handle_request("DELETE", url, **kwargs)

    def put(self, url: str, data: dict = None, **kwargs):
        return self._handle_request("PUT", url, json=data, **kwargs)

    def patch(self, url: str, data: dict = None, **kwargs):
        return self._handle_request("PATCH", url, json=data, **kwargs)
