
# fetchin

**fetchin** is an efficient library for handling HTTP requests in Python. It provides a custom logger to monitor HTTP traffic, a metrics model to track request performance, and a fetcher to simplify HTTP requests. This library is ideal for developers who want greater control and visibility over their HTTP requests and performance metrics.

## Features

- **Custom Logger**: Logs HTTP request details and their responses in a structured way.
- **Metrics Model**: Collect metrics such as response time, request count, and HTTP status.
- **Fetcher**: Simplifies sending HTTP requests (GET, POST, etc.) with integrated logging and metrics system.

## Fetcher Parameters

The `Fetcher` accepts the following parameters during instantiation:

- **label (str)**: A label to identify the fetcher. Fetchers with the same label share the same Circuit Breaker.
- **logger (CustomLogger)**: Custom logger to record requests.
- **metrics (MetricsInterface)**: Metrics system (optional). If not passed, Prometheus will be used by default.
- **circuit_config (dict)**: Circuit Breaker settings, including:
  - `fail_max`: Maximum number of failures before opening the Circuit Breaker.
  - `reset_timeout`: Time in seconds to wait before closing the Circuit Breaker after a failure.
  - `backoff_strategy`: Backoff strategy to determine the wait time between retries.
- **max_retries (int)**: Maximum number of retry attempts for a request in case of failure.

## Installation

Install via pip:

```bash
pip install fetchin
```

## Example Usage

### Basic Example with Prometheus (default implementation)

```python
from src.fetchin.logging.logger import CustomLogger
from src.fetchin.fetcher.fetcher import Fetcher
from src.fetchin.metrics.prometheus_metrics import PrometheusMetrics


logger = CustomLogger()

# Circuit Breaker configuration with linear backoff strategy
def linear_backoff(attempt: int):
    return attempt * 2

circuit_config = {
    "fail_max": 3,
    "reset_timeout": 60,
    "backoff_strategy": linear_backoff
}

# Create a fetcher using the logger and Prometheus as the default metrics system
fetcher = Fetcher(label="api-service", logger=logger, metrics=PrometheusMetrics(), circuit_config=circuit_config, max_retries=5)

try:
    response = fetcher.get("http://localhost:8080/api/example")
    print(response.json())
except Exception as e:
    logger.error(f"Error during fetch: {e}")
```

### Example with Custom Metrics Implementation

You can also provide your own metrics implementation. Simply implement the `MetricsInterface`.

```python
from src.fetchin.logging.logger import CustomLogger
from src.fetchin.metrics.metrics_interface import MetricsInterface
from src.fetchin.fetcher.fetcher import Fetcher

class CustomMetrics(MetricsInterface):
    def track_request(self, method: str, status_code: int, response_time: float):
        print(f"Custom Metrics -> Method: {method}, Status: {status_code}, Time: {response_time:.2f}s")
    
    def track_retry(self, method: str):
        print(f"Custom Retry -> Method: {method}")

logger = CustomLogger()
metrics = CustomMetrics()

# Create a fetcher with a custom metrics implementation
fetcher = Fetcher(label="api-service", logger=logger, metrics=metrics, max_retries=3)

try:
    response = fetcher.get("http://localhost:8080/api/example")
    print(response.json())
except Exception as e:
    logger.error(f"Error during fetch: {e}")
```

## Setting up the Virtual Environment

To set up a Python virtual environment and install dependencies:

1. Create the virtual environment:

   ```bash
   python3 -m venv venv
   ```

2. Activate the virtual environment:

   - **Linux/macOS**:
     ```bash
     source venv/bin/activate
     ```
   - **Windows**:
     ```bash
     .\venv\Scripts\activate
     ```

3. Install project dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. To deactivate the virtual environment, run:

   ```bash
   deactivate
   ```

## Running a Mock API for Testing

You can use **WireMock** to run a mock API for testing. With **Docker Compose**, you can easily start and stop the mock API. Follow these steps:

### Start the Mock API:

1. Run the following command to start the mock API in the background:

   ```bash
   make docker-up
   ```

2. The mock API will now be available at `http://localhost:8080`. You can test an example endpoint with:

   ```bash
   curl http://localhost:8080/api/example
   ```

   This should return a mocked response like:

   ```json
   {
     "message": "This is a mocked response from WireMock!"
   }
   ```

### Stop the Mock API:

To stop the mock API and stop the container, run:

```bash
make docker-down
```

## Additional Makefile Commands

### Install Dependencies

To install the project dependencies, run:

```bash
make install
```

### Lint the Code

To check code style with **flake8**, run:

```bash
make lint
```

### Format the Code

To format the code according to style conventions using **black**, run:

```bash
make format
```

### Run Tests

To run project tests using **pytest**, run:

```bash
make test
```

### Build Docker Compose

If there are changes in the configuration files and you want to rebuild the WireMock container, run:

```bash
make docker-build
```

### WireMock Logs

To see the logs of the WireMock container in real-time, run:

```bash
make docker-logs
```

### Playground

To test the project execution and see usage examples in the **playground**, run:

```bash
make play
```

### Generate Distribution Files

Use the following command to generate the library distribution files:

```bash
make build
```



## Contributing

Contributions are welcome! Please open an issue or submit a pull request.