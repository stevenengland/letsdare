from typing import Final, Tuple

app_version: Final[Tuple[int, int, int]] = (0, 0, 0)
# Version string like X.Y.Z
app_full_version_str: Final[str] = ".".join(map(str, app_version))
# Version string like X.Y
app_major_minor_version_str: Final[str] = ".".join(map(str, app_version[:-1]))
