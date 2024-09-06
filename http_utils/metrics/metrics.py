import time


class CustomMetrics:
    def __init__(self):
        self.metrics = {}

    def start_timer(self, name: str):
        self.metrics[name] = time.time()

    def stop_timer(self, name: str):
        if name in self.metrics:
            elapsed_time = time.time() - self.metrics[name]
            print(f"Timer [{name}] took {elapsed_time:.2f} seconds")
            del self.metrics[name]

    def log_metric(self, name: str, value):
        print(f"Metric [{name}] = {value}")
