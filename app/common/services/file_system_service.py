import os
import shutil
import tempfile
from typing import Optional

from app.common import hashers
from app.common.exceptions import ApplicationError
from app.common.services.file_system_service_interface import (
    FileSystemServiceInterface,
)


class FileSystemService(FileSystemServiceInterface):  # noqa: WPS214
    def copy_file(self, src_file_path: str, dst_file_path: str) -> None:
        if not os.path.exists(dst_file_path):
            os.makedirs(
                os.path.dirname(os.path.abspath(dst_file_path)),
                exist_ok=True,
            )
        try:
            shutil.copy2(src=src_file_path, dst=dst_file_path)

        except shutil.SameFileError:
            raise ApplicationError("The same file already exists.")

        except PermissionError:
            raise ApplicationError("Permission denied.")

        except Exception:
            raise ApplicationError("Error occurred while copying file.")

        self._compare_hashes(src_file_path, dst_file_path)

    def delete_file(self, file_path: str) -> None:
        os.remove(file_path)

    def get_files_in_dir(  # noqa: WPS210
        self,
        dir_path: str,
        recursive: bool = False,
    ) -> list[str]:
        dir_path = os.path.abspath(dir_path)

        if not os.path.isdir(dir_path):
            raise ApplicationError(f"{dir_path} is not a directory.")

        if recursive:
            return self._get_files_in_dir_recursive(dir_path)

        return self._get_files_in_dir(dir_path)

    def create_tmp_dir(self, dest_dir: Optional[str] = None) -> str:
        return tempfile.mkdtemp(
            prefix="letsdare_",
            dir=dest_dir,
        )

    def delete_dir(self, dir_path) -> None:
        shutil.rmtree(dir_path)

    def _get_files_in_dir_recursive(
        self,
        dir_path: str,
    ):
        files = []
        for dirpath, _, filenames in os.walk(dir_path):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                files.append(filepath)
        return files

    def _get_files_in_dir(
        self,
        dir_path: str,
    ):
        files = []
        for entry in os.scandir(dir_path):
            if os.path.isfile(entry.path):
                files.append(entry.path)
        return files

    def _compare_hashes(self, src_file_path: str, dst_file_path: str):
        pre_hash = hashers.get_md5(file_path=src_file_path)
        post_hash = hashers.get_md5(file_path=dst_file_path)
        if pre_hash != post_hash:
            os.remove(path=src_file_path)
            raise ApplicationError(
                "The hashes of the source file differs from the file copied to the target.",
            )
