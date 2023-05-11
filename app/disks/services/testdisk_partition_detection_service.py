import re

from dependency_injector.wiring import Provide, inject
from django.conf import settings

from app.common.services.file_system_service_interface import (
    FileSystemServiceInterface,
)
from app.common.services.shell_service_interface import ShellServiceInterface
from app.disks.services.partition_detection_service_interface import (
    PartitionDetectionServiceInterface,
)


@inject
class TestDiskPartitionDetectionService(PartitionDetectionServiceInterface):
    def __init__(  # noqa: WPS211
        self,
        file_system_service: FileSystemServiceInterface = Provide[  # noqa: WPS404
            "file_system_service"
        ],
        shell_service: ShellServiceInterface = Provide["shell_service"],  # noqa: WPS404
    ) -> None:
        self.file_system_service = file_system_service
        self.shell_service = shell_service

    def get_partition_table_type(self, device: str) -> str:
        cmd_cwd = self.file_system_service.create_tmp_dir()

        self.shell_service.run_command(
            [
                settings.TOOLS_TESTDISK_BINARY,  # type: ignore[misc]
                "/log",
                "/list",
                "/direct",
                device,
            ],
            cmd_cwd=cmd_cwd,
        )

        testdisk_log_text = self.file_system_service.get_file_content(
            f"{cmd_cwd}/testdisk.log",
        )

        self.file_system_service.delete_dir(cmd_cwd)

        regex = r"Partition table type \(auto\): (.*)$"
        match = re.search(regex, testdisk_log_text, re.MULTILINE)

        print(self.shell_service.stdout)  # noqa: WPS421
        print(testdisk_log_text)  # noqa: WPS421

        if match:
            return match.group(1)

        return ""
