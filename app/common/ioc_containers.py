from dependency_injector import containers, providers

from app.common.services.file_system_service import FileSystemService
from app.common.services.logging_service import LoggingService
from app.common.services.shell_service import ShellService


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    logging_service = providers.Factory(LoggingService)
    shell_service = providers.Factory(ShellService)
    file_system_service = providers.Factory(FileSystemService)


container = Container()
