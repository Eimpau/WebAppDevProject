#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings') # Set the default settings module for the 'django' program
    try:
        from django.core.management import execute_from_command_line # Import the command-line utility to interact with Django
    except ImportError as exc:
        raise ImportError( # Raise a helpful error if Django isn't installed or the environment isn't set up properly
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv) # Run the command-line utility with the arguments provide


if __name__ == '__main__':
    main()
