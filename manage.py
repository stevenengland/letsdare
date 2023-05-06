#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main() -> None:
    """
    Main function.

    It does several things:
    1. Sets default settings module, if it is not set
    2. Warns if Django is not installed
    3. Executes any given command
    """
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

    try:
        from django.core import management  # noqa: WPS433
    except ImportError:
        raise ImportError(
            "Couldn't import Django.",
        )

    management.execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
