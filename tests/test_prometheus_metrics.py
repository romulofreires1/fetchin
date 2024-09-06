import unittest
from src.fetchin.metrics.prometheus_metrics import PrometheusMetrics
from prometheus_client import CollectorRegistry, generate_latest

class TestPrometheusMetrics(unittest.TestCase):
    def setUp(self):
        self.registry = CollectorRegistry()
        self.metrics = PrometheusMetrics(registry=self.registry)

    def test_track_request(self):
        self.metrics.track_request("GET", 200, 1.5)
        
        output = generate_latest(self.registry).decode('utf-8')
        self.assertIn('http_request_duration_seconds_sum', output)
        self.assertIn('1.5', output)

    def test_track_retry(self):
        self.metrics.track_retry("GET")
        
        output = generate_latest(self.registry).decode('utf-8')
        self.assertIn('http_request_retries_total', output)
        self.assertIn('1', output)

if __name__ == '__main__':
    unittest.main()
