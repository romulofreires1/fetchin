import requests
from http_utils.metrics.metrics_interface import MetricsInterface
from http_utils.metrics.prometheus_metrics import PrometheusMetrics
import pybreaker
import time
from http_utils.logging.logger import CustomLogger


class CircuitBreakerRegistry:
    _registry = {}

    @classmethod
    def get_circuit_breaker(
        cls,
        label: str,
        fail_max: int = 3,
        reset_timeout: int = 60,
        backoff_strategy=None,
    ):
        if label not in cls._registry:
            breaker = pybreaker.CircuitBreaker(
                fail_max=fail_max, reset_timeout=reset_timeout
            )
            if backoff_strategy:
                breaker.backoff = backoff_strategy
            cls._registry[label] = breaker
        return cls._registry[label]


class Fetcher:
    def __init__(
        self,
        label: str,
        logger: CustomLogger,
        metrics: MetricsInterface = None,
        circuit_config: dict = None,
    ):
        self.logger = logger

        self.metrics = metrics if metrics else PrometheusMetrics()

        default_circuit_config = {
            "fail_max": 3,
            "reset_timeout": 60,
            "backoff_strategy": self.default_backoff_strategy,
        }

        if circuit_config:
            default_circuit_config.update(circuit_config)

        self.circuit_breaker = CircuitBreakerRegistry.get_circuit_breaker(
            label,
            fail_max=default_circuit_config["fail_max"],
            reset_timeout=default_circuit_config["reset_timeout"],
            backoff_strategy=default_circuit_config["backoff_strategy"],
        )

    def default_backoff_strategy(self, attempt: int):
        return 2**attempt

    def get(self, url: str):
        self.logger.info(f"Fetching URL: {url}")
        start_time = time.time()
        attempt = 0

        while True:
            attempt += 1
            try:
                if attempt > 1:
                    self.metrics.track_retry("GET")
                response = self.circuit_breaker.call(requests.get, url)
                response_time = time.time() - start_time
                self.logger.info(f"Response status: {response.status_code}")
                self.metrics.track_request("GET", response.status_code, response_time)
                return response
            except pybreaker.CircuitBreakerError as e:
                self.logger.error(f"Circuit breaker open: {e}")
                self.metrics.track_request("GET", 500, 0)
                break

    def post(self, url: str, data: dict):
        self.logger.info(f"Posting to URL: {url}")
        start_time = time.time()
        attempt = 0

        while True:
            attempt += 1
            try:
                if attempt > 1:
                    self.metrics.track_retry("POST")
                response = self.circuit_breaker.call(requests.post, url, json=data)
                response_time = time.time() - start_time
                self.logger.info(f"Response status: {response.status_code}")
                self.metrics.track_request("POST", response.status_code, response_time)
                return response
            except pybreaker.CircuitBreakerError as e:
                self.logger.error(f"Circuit breaker open: {e}")
                self.metrics.track_request("POST", 500, 0)
                break
