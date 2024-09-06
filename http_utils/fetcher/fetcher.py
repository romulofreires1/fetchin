import requests
import pybreaker
import time
from http_utils.logging.logger import CustomLogger
from http_utils.metrics.metrics_interface import MetricsInterface
from http_utils.metrics.prometheus_metrics import PrometheusMetrics


class Fetcher:
    def __init__(
        self,
        label: str,
        logger: CustomLogger,
        metrics: MetricsInterface = None,
        circuit_config: dict = None,
        max_retries: int = 3,
    ):
        self.logger = logger
        self.label = label
        self.max_retries = max_retries

        self.metrics = metrics if metrics else PrometheusMetrics()

        default_circuit_config = {
            "fail_max": 3,
            "reset_timeout": 60,
        }

        if circuit_config:
            default_circuit_config.update(circuit_config)

        self.circuit_breaker = pybreaker.CircuitBreaker(
            fail_max=default_circuit_config["fail_max"],
            reset_timeout=default_circuit_config["reset_timeout"],
            state_storage=pybreaker.CircuitMemoryStorage(state=pybreaker.STATE_CLOSED),
        )

    def default_backoff_strategy(self, attempt: int):
        return 2**attempt

    def _handle_request(self, method: str, url: str, **kwargs):
        self.logger.info(
            f"{method} to URL: {url}", extra={"url": url, "fetcher_label": self.label}
        )
        start_time = time.time()
        attempt = 0

        while attempt < self.max_retries:
            attempt += 1
            try:
                if attempt > 1:
                    self.metrics.track_retry(method)

                response = self.circuit_breaker.call(
                    requests.request, method, url, **kwargs
                )
                response_time = time.time() - start_time
                self.logger.info(
                    f"Response status: {response.status_code}",
                    extra={
                        "url": url,
                        "fetcher_label": self.label,
                        "status_code": response.status_code,
                    },
                )
                self.metrics.track_request(method, response.status_code, response_time)

                if self.circuit_breaker.current_state == pybreaker.STATE_HALF_OPEN:
                    self.circuit_breaker.close()

                return response
            except pybreaker.CircuitBreakerError as e:
                self.logger.error(
                    f"Circuit breaker open: {e}",
                    extra={
                        "url": url,
                        "fetcher_label": self.label,
                        "error_message": str(e),
                    },
                )
                self.metrics.track_request(method, 500, 0)
                raise e
            except Exception as e:
                self.logger.error(
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
