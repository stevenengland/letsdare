from dependency_injector import containers, providers

from app.common.services.logging_service import LoggingService


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    logging_service = providers.Factory(LoggingService)


container = Container()
