from app.common import hashers
from config.settings.components import BASE_DIR


def test_get_md5_returns_valid_hash():
    assert (
        hashers.get_md5(
            str(BASE_DIR.joinpath("tests", "test_assets", "hashing", "md5hashtest.txt")),
        )
        == "d09dba7d332adb585d176cf807f00f34"  # noqa: W503
    )
