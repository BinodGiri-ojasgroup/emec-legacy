#!/usr/bin/env python
"""EMEC — Django management entrypoint."""
import os
import sys


def main():
    # Defaults to dev locally; deployment environments must export
    # DJANGO_SETTINGS_MODULE=config.settings.prod explicitly.
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.dev")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
