import unittest
from http_utils.logging.logger import CustomLogger
from io import StringIO
import logging

class TestCustomLogger(unittest.TestCase):
    def setUp(self):
        self.log_output = StringIO()
        handler = logging.StreamHandler(self.log_output)
        handler.setFormatter(logging.Formatter('%(message)s'))

        self.logger = CustomLogger(extra_params={"app_name": "MyApp", "environment": "production"})
        self.logger.logger.handlers = [handler]

    def test_info_log(self):
        self.logger.info("Fetching data", extra={"endpoint": "/api/data", "method": "GET"})
        output = self.log_output.getvalue().strip()
        expected_output = '{"app_name": "MyApp", "environment": "production", "endpoint": "/api/data", "method": "GET", "message": "Fetching data"}'
        self.assertEqual(output, expected_output)

    def test_error_log(self):
        self.logger.error("Failed to fetch data", extra={"endpoint": "/api/data", "error_code": 500})
        output = self.log_output.getvalue().strip()
        expected_output = '{"app_name": "MyApp", "environment": "production", "endpoint": "/api/data", "error_code": 500, "message": "Failed to fetch data"}'
        self.assertEqual(output, expected_output)

if __name__ == '__main__':
    unittest.main()
