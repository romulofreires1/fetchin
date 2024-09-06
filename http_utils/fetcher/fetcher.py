import requests
import pybreaker
from http_utils.logging.logger import CustomLogger
from http_utils.metrics.metrics import CustomMetrics


class CircuitBreakerRegistry:
    _registry = {}

    @classmethod
    def get_circuit_breaker(
        cls, label: str, failures_threshold: int = 3, recovery_timeout: int = 60
    ):
        if label not in cls._registry:
            cls._registry[label] = pybreaker.CircuitBreaker(
                fail_max=failures_threshold, reset_timeout=recovery_timeout
            )
        return cls._registry[label]


class Fetcher:
    def __init__(
        self,
        label: str,
        logger: CustomLogger,
        metrics: CustomMetrics,
        failures_threshold: int = 3,
        recovery_timeout: int = 60,
    ):
        self.logger = logger
        self.metrics = metrics
        self.circuit_breaker = CircuitBreakerRegistry.get_circuit_breaker(
            label, failures_threshold, recovery_timeout
        )

    def get(self, url: str):
        self.logger.info(f"Fetching URL: {url}")
        self.metrics.start_timer("GET Request")
        try:
            response = self.circuit_breaker.call(requests.get, url)
            self.logger.info(f"Response status: {response.status_code}")
            return response
        except pybreaker.CircuitBreakerError as e:
            self.logger.error(f"Circuit breaker open: {e}")
        finally:
            self.metrics.stop_timer("GET Request")

    def post(self, url: str, data: dict):
        self.logger.info(f"Posting to URL: {url}")
        self.metrics.start_timer("POST Request")
        try:
            response = self.circuit_breaker.call(requests.post, url, json=data)
            self.logger.info(f"Response status: {response.status_code}")
            return response
        except pybreaker.CircuitBreakerError as e:
            self.logger.error(f"Circuit breaker open: {e}")
        finally:
            self.metrics.stop_timer("POST Request")
