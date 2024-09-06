import logging
import unittest
from unittest.mock import patch, MagicMock
from http_utils.fetcher.fetcher import Fetcher
from http_utils.logging.logger import CustomLogger
from http_utils.metrics.prometheus_metrics import PrometheusMetrics
from pybreaker import CircuitBreakerError
import requests

class TestFetcher(unittest.TestCase):
    def setUp(self):
        self.logger = CustomLogger()
        self.metrics = PrometheusMetrics()

        logging.disable(logging.CRITICAL)

        self.circuit_config = {
            "fail_max": 1,
            "reset_timeout": 60,
        }
        
    def tearDown(self):
        logging.disable(logging.NOTSET)

    @patch('requests.request')
    def test_get_success(self, mock_request):
        fetcher = Fetcher(label="test_get_success", logger=self.logger, metrics=self.metrics, circuit_config=self.circuit_config)
        
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": "test"}
        mock_request.return_value = mock_response

        response = fetcher.get("http://localhost:8080/api/example")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"data": "test"})

    @patch('requests.request')
    def test_post_success(self, mock_request):
        fetcher = Fetcher(label="test_post_success", logger=self.logger, metrics=self.metrics, circuit_config=self.circuit_config)
        
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_response.json.return_value = {"success": True}
        mock_request.return_value = mock_response

        response = fetcher.post("http://localhost:8080/api/example", data={"key": "value"})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"success": True})

    @patch('requests.request')
    def test_delete_success(self, mock_request):
        fetcher = Fetcher(label="test_delete_success", logger=self.logger, metrics=self.metrics, circuit_config=self.circuit_config)
        
        mock_response = MagicMock()
        mock_response.status_code = 204
        mock_request.return_value = mock_response

        response = fetcher.delete("http://localhost:8080/api/example")
        self.assertEqual(response.status_code, 204)

    @patch('requests.request')
    def test_put_success(self, mock_request):
        fetcher = Fetcher(label="test_put_success", logger=self.logger, metrics=self.metrics, circuit_config=self.circuit_config)
        
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"updated": True}
        mock_request.return_value = mock_response

        response = fetcher.put("http://localhost:8080/api/example", data={"key": "value"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"updated": True})

    @patch('requests.request')
    def test_patch_success(self, mock_request):
        fetcher = Fetcher(label="test_patch_success", logger=self.logger, metrics=self.metrics, circuit_config=self.circuit_config)
        
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"patched": True}
        mock_request.return_value = mock_response

        response = fetcher.patch("http://localhost:8080/api/example", data={"key": "value"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"patched": True})

    @patch('requests.request')
    def test_get_circuit_breaker_error(self, mock_request):
        fetcher = Fetcher(label="test_get_circuit_breaker_error", logger=self.logger, metrics=self.metrics, circuit_config=self.circuit_config)

        mock_request.side_effect = requests.exceptions.ConnectionError()

        with self.assertRaises(CircuitBreakerError):
            fetcher.get("http://localhost:8080/api/example")
            fetcher.get("http://localhost:8080/api/example")

    @patch('requests.request')
    def test_get_retry(self, mock_request):
        circuit_config = {
            "fail_max": 2,
            "reset_timeout": 60,
        }
                
        fetcher = Fetcher(label="test_get_retry", logger=self.logger, metrics=self.metrics, circuit_config=circuit_config)

        mock_request.side_effect = [
            requests.exceptions.ConnectionError(),
            MagicMock(status_code=200, json=lambda: {"data": "test"})
        ]

        response = fetcher.get("http://localhost:8080/api/example")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"data": "test"})

if __name__ == '__main__':
    unittest.main()
