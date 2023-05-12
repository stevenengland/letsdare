import ctypes
import os
import subprocess  # noqa: S404
from typing import Optional, Union

from django.conf import settings

from app.common.entities.command import Command
from app.common.exceptions import ApplicationError
from app.common.services.shell_service_interface import ShellServiceInterface


class ShellService(ShellServiceInterface):
    def __init__(
        self,
    ) -> None:
        self._stdout: Optional[str] = None
        self._stderr: Optional[str] = None
        self._returncode: Optional[int] = None

    @property
    def stdout(self) -> Optional[str]:
        return self._stdout

    @property
    def stderr(self) -> Optional[str]:
        return self._stderr

    @property
    def returncode(self) -> Optional[int]:
        return self._returncode

    def run_command(  # noqa: WPS211
        self,
        command: Command,
        cmd_input: Union[str, bytes, None] = None,
        cmd_timeout: Optional[float] = None,
        cmd_cwd: Optional[str] = None,
        encoding: Optional[str] = None,
    ) -> int:
        if cmd_input and not isinstance(cmd_input, bytes) and encoding:
            cmd_input = cmd_input.encode(encoding)

        if cmd_cwd is None:
            cmd_cwd = settings.TOOLS_WORKING_DIR  # type: ignore[misc]

        process = subprocess.Popen(  # noqa: S603
            command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=cmd_cwd,
        )
        stdout, stderr = process.communicate(
            timeout=cmd_timeout,
            input=cmd_input,  # type: ignore[arg-type]
        )

        self._stderr = stderr.decode("utf-8")
        self._stdout = stdout.decode("utf-8")

        return process.returncode

    def is_admin(self) -> bool:
        try:
            return os.getuid() == 0
        except AttributeError:
            pass  # noqa: WPS420
        try:
            return ctypes.windll.shell32.IsUserAnAdmin() == 1  # type: ignore[attr-defined]
        except AttributeError:
            raise ApplicationError(
                "Could not determine if the user has root privilges.",
            )
