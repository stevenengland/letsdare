"""Put all the logical tests concerning the settings right here."""

from django.conf import settings


def test_all_app_settings_are_set() -> None:
    assert settings.PHOTOS_REPO_ROOTDIR  # type: ignore[misc]
