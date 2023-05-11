import re

from dependency_injector.wiring import Provide, inject
from django.conf import settings

from app.common.services.shell_service_interface import ShellServiceInterface
from app.disks.services.partition_detection_service_interface import (
    PartitionDetectionServiceInterface,
)


@inject
class PartedPartitionDetectionService(PartitionDetectionServiceInterface):
    def __init__(  # noqa: WPS211
        self,
        shell_service: ShellServiceInterface = Provide["shell_service"],  # noqa: WPS404
    ) -> None:
        self.shell_service = shell_service

    def get_partition_table_type(self, device: str) -> str:
        self.shell_service.run_command(
            [
                settings.TOOLS_PARTED_BINARY,  # type: ignore[misc]
                "--script",
                device,
                "print",
            ],
        )

        parted_result = (
            self.shell_service.stdout if self.shell_service.stdout is not None else ""
        )

        regex = "Partition Table: (.*)$"
        match = re.search(regex, parted_result, re.MULTILINE)

        if match:
            return match.group(1)

        return ""
