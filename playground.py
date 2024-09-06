from http_utils.fetcher.fetcher import Fetcher
from http_utils.logging.logger import CustomLogger
from http_utils.metrics.metrics import CustomMetrics


logger = CustomLogger()
metrics = CustomMetrics()

fetcher1 = Fetcher(label="api-service", logger=logger, metrics=metrics)
fetcher2 = Fetcher(label="api-service", logger=logger, metrics=metrics)

try:
    response = fetcher1.get("http://localhost:8080/api/example")
    print(response.json())
except Exception as e:
    logger.error(f"Error during fetch: {e}")