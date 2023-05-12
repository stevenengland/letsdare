import pytest

from app.disks.services.testdisk_partition_detection_service import (
    TestDiskPartitionDetectionService,
)
from config.settings.environments.test import TEST_ASSETS_DIR


@pytest.fixture(scope="function", name="uut")
def testdisk_partition_detection_service() -> TestDiskPartitionDetectionService:
    uut = TestDiskPartitionDetectionService()
    return uut  # noqa: WPS331


def test_partition_type_is_returned_when_partition_type_is_readable(
    uut: TestDiskPartitionDetectionService,
):
    ptt = uut.get_partition_table_type(
        str(TEST_ASSETS_DIR.joinpath("disk_images", "uc0001.img")),
    )
    assert ptt == "EFI GPT"


def test_partition_type_is_returned_when_partition_type_is_partly_destroyed(
    uut: TestDiskPartitionDetectionService,
):
    ptt = uut.get_partition_table_type(
        str(TEST_ASSETS_DIR.joinpath("disk_images", "uc0003.img")),
    )
    assert ptt == "EFI GPT"


def test_partition_type_returns_empty_when_partition_type_is_not_readable(
    uut: TestDiskPartitionDetectionService,
):
    ptt = uut.get_partition_table_type(
        str(TEST_ASSETS_DIR.joinpath("disk_images", "uc0004.img")),
    )
    assert ptt == "EFI GPT"
