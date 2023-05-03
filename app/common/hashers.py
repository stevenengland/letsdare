import hashlib


def get_md5(file_path: str) -> str:
    hash_md5 = hashlib.md5(usedforsecurity=False)
    with open(file_path, "rb") as file2hash:
        for chunk in iter(lambda: file2hash.read(4096), b""):  # noqa: WPS426, WPS432
            hash_md5.update(chunk)
    return hash_md5.hexdigest()
