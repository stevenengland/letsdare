import pytest

from app.disks.services.parted_partition_detection_service import (
    PartedPartitionDetectionService,
)
from config.settings.environments.test import TEST_ASSETS_DIR


@pytest.fixture(scope="function", name="uut")
def parted_partition_detection_service() -> PartedPartitionDetectionService:
    uut = PartedPartitionDetectionService()
    return uut  # noqa: WPS331


def test_partion_table_is_returned_if_partition_table_type_is_detectable(
    uut: PartedPartitionDetectionService,
):
    partition_table_type = uut.get_partition_table_type(
        str(TEST_ASSETS_DIR.joinpath("disk_images", "uc0001.img")),
    )

    assert partition_table_type == "gpt"


def test_partion_table_is_unknown_if_partition_table_type_is_partly_destroyed(
    uut: PartedPartitionDetectionService,
):
    partition_table_type = uut.get_partition_table_type(
        str(TEST_ASSETS_DIR.joinpath("disk_images", "uc0003.img")),
    )

    assert partition_table_type == "unknown"


def test_partion_table_is_unknown_if_partition_table_type_is_not_detectable(
    uut: PartedPartitionDetectionService,
):
    partition_table_type = uut.get_partition_table_type(
        str(TEST_ASSETS_DIR.joinpath("disk_images", "uc0004.img")),
    )

    assert partition_table_type == "unknown"
