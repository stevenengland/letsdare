import abc
from typing import Optional


class FileSystemServiceInterface(abc.ABC):
    @abc.abstractmethod
    def copy_file(self, src_file_path: str, dst_file_path: str) -> None:
        pass

    @abc.abstractmethod
    def delete_file(self, file_path: str) -> None:
        pass

    @abc.abstractmethod
    def get_files_in_dir(self, dir_path: str, recursive: bool = False) -> list[str]:
        pass

    @abc.abstractmethod
    def create_tmp_dir(self, dest_dir: Optional[str] = None) -> str:
        pass

    @abc.abstractmethod
    def delete_dir(self, dir_path) -> None:
        pass
