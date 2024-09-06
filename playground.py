from http_utils.logging.logger import CustomLogger
from http_utils.fetcher.fetcher import Fetcher
from prometheus_client import start_http_server
import time

logger = CustomLogger()

def linear_backoff(attempt: int):
    return attempt * 2

circuit_config = {
    "fail_max": 3,
    "reset_timeout": 60,
    "backoff_strategy": linear_backoff
}

def start_metrics_server(port=8000):
    start_http_server(port)
    print(f"Metrics server started at http://localhost:{port}/metrics")

if __name__ == "__main__":
    start_metrics_server()

    fetcher = Fetcher(label="api-service", logger=logger, metrics=None, circuit_config=circuit_config)

    while True:
        try:
            response = fetcher.get("http://localhost:8080/api/example")
            print(response.json())
        except Exception as e:
            logger.error(f"Error during fetch: {e}")
        
        time.sleep(10)
