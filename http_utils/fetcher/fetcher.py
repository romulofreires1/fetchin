import requests
import pybreaker
from http_utils.logging.logger import CustomLogger
from http_utils.metrics.metrics import CustomMetrics


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
        metrics: CustomMetrics,
        circuit_config: dict = None,
    ):
        self.logger = logger
        self.metrics = metrics

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
        """
        Exponential backoff strategy (2^attempt) to control retry intervals
        """
        return 2**attempt

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
