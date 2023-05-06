from django.apps import AppConfig


class CommonConfig(AppConfig):
    """The config."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "app.common"

    def ready(self) -> None:
        from app.common.ioc_containers import container  # noqa: WPS433

        container.wire(
            packages=[
                "app.disks",
                "app.common",
            ],
        )
