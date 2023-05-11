from appdirs import AppDirs

from config.settings.components import config

special_dirs = AppDirs("letsdare", "stevenengland")

DATA_ROOTDIR: str = config(
    "LETSDARE_DATA_ROOTDIR",
    default=f"{special_dirs.user_data_dir}/data",
)

HOSTING_DOMAIN_NAME: str = config("LETSDARE_HOSTING_DOMAIN_NAME", default="local.lan")

LOGGING_FILE: str = config(
    "LETSDARE_LOGGING_FILE",
    default=f"{DATA_ROOTDIR}/logs/letsdare.log",
)
LOGGING_LEVEL: str = config("LETSDARE_LOGGING_LEVEL", default="info")

# When dir is None then a os dependent temp directory will be used.
TMP_ROOTDIR: str = config(
    "LETSDARE_TMP_ROOTDIR",
    default=None,
)

TOOLS_DDRESCUE_BINARY: str = config(
    "LETSDARE_TOOLS_DDRESCUE_BINARY",
    default="ddrescue",
)

TOOLS_PARTED_BINARY: str = config(
    "LETSDARE_TOOLS_PARTED_BINARY",
    default="parted",
)

TOOLS_TESTDISK_BINARY: str = config(
    "LETSDARE_TOOLS_TESTDISK_BINARY",
    default="testdisk",
)
