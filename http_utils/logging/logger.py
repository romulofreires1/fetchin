import logging
import json


class CustomLogger:
    def __init__(self, name: str = "http-utils", extra_params: dict = None):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        handler = logging.StreamHandler()
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(message)s")
        handler.setFormatter(formatter)

        if not self.logger.handlers:
            self.logger.addHandler(handler)

        self.extra_params = extra_params or {}

    def _merge_params(self, message: str, extra: dict):
        merged = self.extra_params.copy()
        merged.update(extra or {})
        merged["message"] = message
        return json.dumps(merged, ensure_ascii=False)

    def info(self, message: str, extra: dict = None):
        log_message = self._merge_params(message, extra)
        self.logger.info(log_message)

    def error(self, message: str, extra: dict = None):
        log_message = self._merge_params(message, extra)
        self.logger.error(log_message)

    def debug(self, message: str, extra: dict = None):
        log_message = self._merge_params(message, extra)
        self.logger.debug(log_message)
