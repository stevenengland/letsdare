import abc
from typing import Optional

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
    def run_command(self, command: Command) -> int:
        pass

    @abc.abstractmethod
    def is_admin(self) -> bool:
        pass
