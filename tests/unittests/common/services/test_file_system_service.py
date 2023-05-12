import os
import shutil
import tempfile

import pytest
from pytest_mock import MockerFixture

from app.common import hashers
from app.common.services import file_system_service


@pytest.fixture(scope="function", name="fss")
def photo_consumer_service() -> file_system_service.FileSystemService:
    fss = file_system_service.FileSystemService()
    return fss  # noqa: WPS331


def test_copying_file_succeeds_if_path_does_not_exist(
    when,
    mocker: MockerFixture,
) -> None:
    when(hashers).get_md5(...)
    mocker.patch(
        "app.common.services.file_system_service.os.path.exists",
        return_value=False,
    )
    mocker.patch(
        "app.common.services.file_system_service.os.path.abspath",
        return_value="/testdir",
    )
    mocker.patch("app.common.services.file_system_service.os.makedirs")
    mocker.patch("app.common.services.file_system_service.shutil.copy2")
    fss = file_system_service.FileSystemService()

    fss.copy_file("testsrc", "testdst")

    file_system_service.os.makedirs.assert_called_once_with("/", exist_ok=True)  # type: ignore[attr-defined]
    file_system_service.shutil.copy2.assert_called_once_with(  # type: ignore[attr-defined]
        src="testsrc",
        dst="testdst",
    )


def test_copying_file_succeeds_if_path_exists(
    when,
    mocker: MockerFixture,
) -> None:
    when(hashers).get_md5(...)
    mocker.patch(
        "app.common.services.file_system_service.os.path.exists",
        return_value=True,
    )
    mocked_copy = mocker.patch("app.common.services.file_system_service.shutil.copy2")
    fss = file_system_service.FileSystemService()

    fss.copy_file("testsrc", "testdst")

    mocked_copy.assert_called_once_with(src="testsrc", dst="testdst")


def test_copy_throws_if_file_already_exists(when):
    when(shutil).copy2(..., ...).thenRaise(shutil.SameFileError)
    with pytest.raises(expected_exception=Exception, match="already exists"):
        fss = file_system_service.FileSystemService()
        fss.copy_file("testsrc", "testdst")


def test_copy_throws_if_file_copied_has_wrong_hash(
    when,
    expect,
    fss: file_system_service.FileSystemService,
):
    expect(os, times=1).remove(...)
    when(shutil).copy2(..., ...)
    when(hashers).get_md5(...).thenReturn("first_hash").thenReturn("secondHash")
    with pytest.raises(expected_exception=Exception, match="hash"):
        fss.copy_file("testsrc", "testdst")


def test_delete_removes_file(
    expect,
    fss: file_system_service.FileSystemService,
):
    expect(os, times=1).remove(...)
    fss.delete_file("testdst")


def test_get_files_in_dir_should_return_array_of_2_elements_when_2_files_are_in_dir(
    fss: file_system_service.FileSystemService,
    when,
):
    when(os.path).isdir(...).thenReturn(True)
    when(os.path).isfile(...).thenReturn(True)
    when(os).scandir(...).thenReturn(
        [DirEntry("/test/test1.txt"), DirEntry("/test/test2.txt")],
    )
    files = fss.get_files_in_dir("/testdir")

    assert len(files) == 2
    assert any("test1.txt" in file_full_path for file_full_path in files)
    assert any("test2.txt" in file_full_path for file_full_path in files)


def test_get_files_in_dir_should_throw_when_directory_is_invalid(
    fss: file_system_service.FileSystemService,
):
    with pytest.raises(expected_exception=Exception, match="is not a directory"):
        fss.get_files_in_dir("/testdirthatdoesnotexist")


def test_create_temp_dir_should_return_tmp_dir_path(
    fss: file_system_service.FileSystemService,
    when,
):
    when(tempfile).mkdtemp(...).thenReturn("tempdir")
    assert fss.create_tmp_dir("/tmpdir") == "tempdir"  # noqa: S108


class DirEntry:  # noqa: WPS306
    def __init__(self, path: str) -> None:
        self._path = path

    @property
    def path(self) -> str:
        return self._path
