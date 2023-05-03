import abc


class LoggingServiceInterface(abc.ABC):
    @abc.abstractmethod
    def log_info(self, message: str) -> None:
        pass

    @abc.abstractmethod
    def log_warning(self, message: str) -> None:
        pass

    @abc.abstractmethod
    def log_error(self, message: str) -> None:
        pass
