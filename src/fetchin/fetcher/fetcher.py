import requests
import pybreaker
import time
from src.fetchin.metrics.metrics_interface import MetricsInterface


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
        self.max_retries = max_retries

        self.metrics = metrics if metrics else None

        default_circuit_config = {
            "fail_max": 3,
            "reset_timeout": 60,
        }

        if circuit_config:
            default_circuit_config.update(circuit_config)

        if label not in Fetcher.circuit_breakers:
            Fetcher.circuit_breakers[label] = pybreaker.CircuitBreaker(
                fail_max=default_circuit_config["fail_max"],
                reset_timeout=default_circuit_config["reset_timeout"],
                state_storage=pybreaker.CircuitMemoryStorage(
                    state=pybreaker.STATE_CLOSED
                ),
            )

        self.circuit_breaker = Fetcher.circuit_breakers[label]

    def default_backoff_strategy(self, attempt: int):
        return 2**attempt

    def _log_info(self, message: str, extra=None):
        if self.logger:
            self.logger.info(message, extra=extra)

    def _log_error(self, message: str, extra=None):
        if self.logger:
            self.logger.error(message, extra=extra)

    def _track_request(self, method: str, status_code: int, response_time: float):
        if self.metrics:
            self.metrics.track_request(method, status_code, response_time)

    def _track_retry(self, method: str):
        if self.metrics:
            self.metrics.track_retry(method)

    def _handle_request(self, method: str, url: str, **kwargs):
        self._log_info(
            f"{method} to URL: {url}", extra={"url": url, "fetcher_label": self.label}
        )
        start_time = time.time()
        attempt = 0

        while attempt < self.max_retries:
            attempt += 1
            try:
                if attempt > 1:
                    self._track_retry(method)

                response = self.circuit_breaker.call(
                    requests.request, method, url, **kwargs
                )
                response_time = time.time() - start_time
                self._log_info(
                    f"Response status: {response.status_code}",
                    extra={
                        "url": url,
                        "fetcher_label": self.label,
                        "status_code": response.status_code,
                    },
                )
                self._track_request(method, response.status_code, response_time)

                if self.circuit_breaker.current_state == pybreaker.STATE_HALF_OPEN:
                    self.circuit_breaker.close()

                return response
            except pybreaker.CircuitBreakerError as e:
                self._log_error(
                    f"Circuit breaker open: {e}",
                    extra={
                        "url": url,
                        "fetcher_label": self.label,
                        "error_message": str(e),
                    },
                )
                self._track_request(method, 500, 0)
                raise e
            except Exception as e:
                self._log_error(
                    f"Attempt {attempt} failed: {e}",
                    extra={
                        "url": url,
                        "fetcher_label": self.label,
                        "error_message": str(e),
                    },
                )

                if self.circuit_breaker.current_state == pybreaker.STATE_HALF_OPEN:
                    self.circuit_breaker.open()

                if attempt == self.max_retries:
                    raise e
                time.sleep(self.default_backoff_strategy(attempt))

    def get(self, url: str):
        return self._handle_request("GET", url)

    def post(self, url: str, data: dict):
        return self._handle_request("POST", url, json=data)

    def delete(self, url: str):
        return self._handle_request("DELETE", url)

    def put(self, url: str, data: dict):
        return self._handle_request("PUT", url, json=data)

    def patch(self, url: str, data: dict):
        return self._handle_request("PATCH", url, json=data)
