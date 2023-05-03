import structlog

from app.common.services.logging_service_interface import (
    LoggingServiceInterface,
)


class LoggingService(LoggingServiceInterface):
    def __init__(
        self,
    ) -> None:
        self.logger = structlog.get_logger("django")

    def log_info(self, message: str) -> None:
        self.logger.info(message)

    def log_warning(self, message: str) -> None:
        self.logger.warning(message)

    def log_error(self, message: str) -> None:
        self.logger.error(message)
