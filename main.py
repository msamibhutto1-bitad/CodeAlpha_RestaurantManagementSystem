"""Entry point.

    python main.py                      migrate + start the dev server
    python main.py createsuperuser      any Django management command works
"""
import os
import sys

from config import Config


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.settings")
    from django.core.management import execute_from_command_line

    if len(sys.argv) > 1:
        execute_from_command_line(sys.argv)
        return

    execute_from_command_line([sys.argv[0], "migrate", "--noinput"])
    execute_from_command_line([sys.argv[0], "runserver", f"{Config.HOST}:{Config.PORT}"])


if __name__ == "__main__":
    main()
