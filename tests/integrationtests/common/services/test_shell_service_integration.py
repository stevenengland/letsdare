import pytest

from app.common.services.shell_service import ShellService


@pytest.fixture(scope="function", name="uut")
def shell_service() -> ShellService:
    uut = ShellService()
    return uut  # noqa: WPS331


def test_run_command_returns_stdout(uut: ShellService):
    uut.run_command(["echo", "teststdout"])
    assert uut.stdout == "teststdout\n"
