"""
This file contains all the settings that defines the development server.

SECURITY WARNING: don't run with debug turned on in production!
"""

import logging
import socket

import structlog

from config.settings.components import BASE_DIR
from config.settings.components.common import INSTALLED_APPS, MIDDLEWARE
from config.settings.components.csp import (
    CSP_CONNECT_SRC,
    CSP_IMG_SRC,
    CSP_SCRIPT_SRC,
)
from config.settings.components.letsdare import HOSTING_DOMAIN_NAME

# Setting the development status:

DEBUG = True

ALLOWED_HOSTS = [
    HOSTING_DOMAIN_NAME,
    "localhost",
    "0.0.0.0",  # noqa: S104
    "127.0.0.1",
    "[::1]",
]

# Setting the DB

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "testdatabase",  # This is where you put the name of the db file.
    },
}

# Installed apps for development only:

INSTALLED_APPS += (
    # Better debug:
    "debug_toolbar",
    "nplusone.ext.django",
    # Linting migrations:
    "django_migration_linter",
    # django-test-migrations:
    "django_test_migrations.contrib.django_checks.AutoNames",
    # This check might be useful in production as well,
    # so it might be a good idea to move `django-test-migrations`
    # to prod dependencies and use this check in the main `settings.py`.
    # This will check that your database is configured properly,
    # when you run `python manage.py check` before deploy.
    "django_test_migrations.contrib.django_checks.DatabaseConfiguration",
    # django-extra-checks:
    "extra_checks",
)


# Django debug toolbar:
# https://django-debug-toolbar.readthedocs.io

MIDDLEWARE += (
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    # https://github.com/bradmontgomery/django-querycount
    # Prints how many queries were executed, useful for the APIs.
    "querycount.middleware.QueryCountMiddleware",
)

# https://django-debug-toolbar.readthedocs.io/en/stable/installation.html#configure-internal-ips
try:  # This might fail on some OS
    INTERNAL_IPS = [
        "{0}.1".format(ip[: ip.rfind(".")])
        for ip in socket.gethostbyname_ex(socket.gethostname())[2]
    ]
except socket.error:  # pragma: no cover
    INTERNAL_IPS = []
INTERNAL_IPS += ["127.0.0.1", "10.0.2.2"]


def _custom_show_toolbar(request) -> bool:
    """Only show the debug toolbar to users with the superuser flag."""
    return DEBUG and request.user.is_superuser


DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": "config.settings.environments.development._custom_show_toolbar",
}

# This will make debug toolbar to work with django-csp,
# since `ddt` loads some scripts from `ajax.googleapis.com`:
CSP_SCRIPT_SRC += ("ajax.googleapis.com",)
CSP_IMG_SRC += ("data:",)
CSP_CONNECT_SRC += ("'self'",)


# nplusone
# https://github.com/jmcarp/nplusone

# Should be the first in line:
MIDDLEWARE = ("nplusone.ext.django.NPlusOneMiddleware",) + MIDDLEWARE  # noqa: WPS440

# Logging N+1 requests:
NPLUSONE_RAISE = True  # comment out if you want to allow N+1 requests
NPLUSONE_LOGGER = logging.getLogger("django")
NPLUSONE_LOG_LEVEL = logging.WARN
NPLUSONE_WHITELIST = [
    {"model": "admin.*"},
]


# django-test-migrations
# https://github.com/wemake-services/django-test-migrations

# Set of badly named migrations to ignore:
DTM_IGNORED_MIGRATIONS = frozenset((("axes", "*"),))


# django-extra-checks
# https://github.com/kalekseev/django-extra-checks

EXTRA_CHECKS = {
    "checks": [
        # Forbid `unique_together`:
        "no-unique-together",
        # Use the indexes option instead:
        "no-index-together",
        # Each model must be registered in admin:
        "model-admin",
        # FileField/ImageField must have non empty `upload_to` argument:
        "field-file-upload-to",
        # Text fields shouldn't use `null=True`:
        "field-text-null",
        # Prefer using BooleanField(null=True) instead of NullBooleanField:
        "field-boolean-null",
        # Don't pass `null=False` to model fields (this is django default)
        "field-null",
        # ForeignKey fields must specify db_index explicitly if used in
        # other indexes:
        {"id": "field-foreign-key-db-index", "when": "indexes"},
        # If field nullable `(null=True)`,
        # then default=None argument is redundant and should be removed:
        "field-default-null",
        # Fields with choices must have companion CheckConstraint
        # to enforce choices on database level
        "field-choices-constraint",
    ],
}

TEST_ASSETS_DIR = BASE_DIR.joinpath("tests", "test_assets")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    # We use these formatters in our `'handlers'` configuration.
    # Probably, you won't need to modify these lines.
    # Unless, you know what you are doing.
    "formatters": {
        "json_formatter": {
            "()": structlog.stdlib.ProcessorFormatter,
            "processor": structlog.processors.JSONRenderer(),
        },
        "console": {
            "()": structlog.stdlib.ProcessorFormatter,
            "processor": structlog.processors.KeyValueRenderer(
                key_order=["timestamp", "level", "event", "logger"],
            ),
        },
    },
    # You can easily swap `key/value` (default) output and `json` ones.
    # Use `'json_console'` if you need `json` logs.
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "console",
        },
        "json_console": {
            "class": "logging.StreamHandler",
            "formatter": "json_formatter",
        },
    },
    # These loggers are required by our app:
    # - django is required when using `logger.getLogger('django')`
    # - security is required by `axes`
    "loggers": {
        "django": {
            "handlers": ["console"],
            "propagate": True,
            "level": "INFO",
        },
        "security": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
    },
}

TOOLS_PARTED_BINARY = "/opt/letsdare/parted/parted/parted"
TOOLS_TESTDISK_BINARY = "/opt/letsdare/testdisk/testdisk_static"
