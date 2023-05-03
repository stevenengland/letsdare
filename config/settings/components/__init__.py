import os
from collections import OrderedDict
from pathlib import PurePath

from decouple import AutoConfig, RepositoryEnv

AutoConfig.SUPPORTED = OrderedDict(
    [
        ("letsdare.conf", RepositoryEnv),
    ],
)

# Build paths inside the project like this: BASE_DIR.joinpath('some')
# `pathlib` is better than writing: dirname(dirname(dirname(__file__)))
BASE_DIR = PurePath(__file__).parent.parent.parent.parent

# Tap paperless.conf if it's available
configuration_path = os.getenv("LETSDARE_CONFIGURATION_PATH")
if configuration_path and os.path.exists(configuration_path):
    configuration_path = os.getenv("LETSDARE_CONFIGURATION_PATH")
elif os.path.exists("../../../../letsdare.conf"):
    configuration_path = "../../../../"
elif os.path.exists("/etc/letsdare.conf"):
    configuration_path = "/etc/"
elif os.path.exists("/usr/local/etc/letsdare.conf"):
    configuration_path = "/usr/local/etc/"

# Loading `.env` style files
# See docs: https://gitlab.com/mkleehammer/autoconfig
config = AutoConfig(search_path=configuration_path)
