#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projectsite.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Activate the project venv and install deps:\n"
            "  cd ..\\n"
            "  .\\venv\\Scripts\\Activate.ps1\n"
            "  pip install -r requirements.txt\n"
            "  cd projectsite\n"
            "  python manage.py runserver"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
