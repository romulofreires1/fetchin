from http_utils.logging.logger import CustomLogger
from http_utils.metrics.metrics import CustomMetrics
from http_utils.fetcher.fetcher import Fetcher

logger = CustomLogger()
metrics = CustomMetrics()

def linear_backoff(attempt: int):
    return attempt * 2  

circuit_config = {
    "fail_max": 3,
    "reset_timeout": 60,
    "backoff_strategy": linear_backoff
}

fetcher = Fetcher(label="api-service", logger=logger, metrics=metrics, circuit_config=circuit_config)

try:
    response = fetcher.get("http://localhost:8080/api/example")
    print(response.json())
except Exception as e:
    logger.error(f"Error during fetch: {e}")