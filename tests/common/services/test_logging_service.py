import pytest
import structlog
from structlog.testing import LogCapture

from app.common.services.logging_service import LoggingService


@pytest.fixture(scope="function", name="ls")
def logging_service() -> LoggingService:
    ls = LoggingService()
    return ls  # noqa: WPS331


@pytest.fixture(name="log_output")
def fixture_log_output():
    return LogCapture()


@pytest.fixture(scope="function", autouse=True)
def fixture_configure_structlog(log_output):
    structlog.configure(processors=[log_output])


def test_logging_should_log_info(ls: LoggingService, log_output):
    ls.log_info("test")
    assert log_output.entries[0]["event"] == "test"
    assert log_output.entries[0]["log_level"] == "info"


def test_logging_should_log_warning(ls: LoggingService, log_output):
    ls.log_warning("test")
    assert log_output.entries[0]["event"] == "test"
    assert log_output.entries[0]["log_level"] == "warning"


def test_logging_should_log_error(ls: LoggingService, log_output):
    ls.log_error("test")
    assert log_output.entries[0]["event"] == "test"
    assert log_output.entries[0]["log_level"] == "error"
