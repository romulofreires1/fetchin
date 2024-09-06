from http_utils.metrics.metrics_interface import MetricsInterface
from prometheus_client import Summary, Counter


class PrometheusMetrics(MetricsInterface):
    def __init__(self):
        self.request_time = Summary(
            "http_request_duration_seconds",
            "Time spent processing request",
            ["method", "status_code"],
        )

        self.request_counter = Counter(
            "http_requests_total", "Total number of requests", ["method", "status_code"]
        )

        self.retry_counter = Counter(
            "http_request_retries_total", "Total number of retries", ["method"]
        )

    def track_request(self, method: str, status_code: int, response_time: float):
        self.request_time.labels(method=method, status_code=status_code).observe(
            response_time
        )
        self.request_counter.labels(method=method, status_code=status_code).inc()

    def track_retry(self, method: str):
        self.retry_counter.labels(method=method).inc()
