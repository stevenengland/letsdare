import abc
from typing import Optional, Union

from app.common.entities.command import Command


class ShellServiceInterface(abc.ABC):
    @property
    @abc.abstractmethod
    def stdout(self) -> Optional[str]:
        pass

    @property
    @abc.abstractmethod
    def stderr(self) -> Optional[str]:
        pass

    @abc.abstractmethod
    def run_command(  # noqa: WPS211
        self,
        command: Command,
        cmd_input: Union[str, bytes, None] = None,
        cmd_timeout: Optional[float] = None,
        cmd_cwd: Optional[str] = None,
        encoding: Optional[str] = None,
    ) -> int:
        pass

    @abc.abstractmethod
    def is_admin(self) -> bool:
        pass
