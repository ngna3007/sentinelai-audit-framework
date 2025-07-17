#!/usr/bin/env python3
"""
Module entry point for database.importers package

Enables running: python -m database.importers
"""

from .main import cli

if __name__ == '__main__':
    cli()