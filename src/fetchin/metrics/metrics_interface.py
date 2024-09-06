from abc import ABC, abstractmethod


class MetricsInterface(ABC):
    @abstractmethod
    def track_request(self, method: str, status_code: int, response_time: float):
        pass

    @abstractmethod
    def track_retry(self, method: str):
        pass
