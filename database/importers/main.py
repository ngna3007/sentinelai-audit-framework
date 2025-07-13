#!/usr/bin/env python3
"""
Standalone CLI for database import operations

Usage:
    python -m database.importers --help
    python database/importers/main.py csv /path/to/file.csv table_name
    python database/importers/main.py bulk /path/to/source/dir
"""

import click
import sys
import os
from pathlib import Path

# Handle imports for both standalone and module execution
try:
    # When run as module (python -m database.importers)
    from .bulk_import import BulkImporter
    from .csv_importer import CsvImporter
except ImportError:
    # When run as standalone script
    project_root = Path(__file__).parent.parent.parent
    sys.path.insert(0, str(project_root))
    from database.importers.bulk_import import BulkImporter
    from database.importers.csv_importer import CsvImporter


@click.group()
def cli():
    """Database import utilities"""
    pass


@cli.command()
@click.argument('file_path', type=click.Path(exists=True))
@click.argument('table_name')
@click.option('--batch-size', default=1000, help='Batch size for imports')
@click.option('--progress/--no-progress', default=True, help='Show progress')
def csv(file_path, table_name, batch_size, progress):
    """Import single CSV file into specified table"""
    click.echo(f"📥 Importing {file_path} into {table_name}...")
    
    try:
        importer = CsvImporter(batch_size=batch_size, show_progress=progress)
        result = importer.import_file(file_path, table_name)
        
        if result['success']:
            click.echo(f"✅ Successfully imported {result['imported_count']} records")
        else:
            click.echo(f"❌ Import failed: {result['error']}")
            sys.exit(1)
            
    except Exception as e:
        click.echo(f"❌ Unexpected error: {str(e)}")
        sys.exit(1)


@cli.command()  
@click.argument('source_dir', type=click.Path(exists=True))
@click.option('--batch-size', default=1000, help='Batch size for imports')
@click.option('--validate/--no-validate', default=True, help='Validate before import')
@click.option('--progress/--no-progress', default=True, help='Show progress')
def bulk(source_dir, batch_size, validate, progress):
    """Import multiple CSV files from directory"""
    click.echo(f"📦 Running bulk import from {source_dir}...")
    
    try:
        importer = BulkImporter(
            batch_size=batch_size, 
            show_progress=progress, 
            validate_data=validate
        )
        result = importer.import_all(source_dir)
        
        if result['success']:
            click.echo(f"✅ Bulk import completed successfully!")
            for table, count in result['imported_counts'].items():
                click.echo(f"   • {table}: {count} records")
        else:
            click.echo(f"❌ Bulk import failed!")
            for error in result['errors']:
                click.echo(f"   • {error}")
            sys.exit(1)
            
        if result['validation_warnings']:
            click.echo(f"⚠️  Validation warnings:")
            for warning in result['validation_warnings']:
                click.echo(f"   • {warning}")
                
    except Exception as e:
        click.echo(f"❌ Unexpected error: {str(e)}")
        sys.exit(1)


@cli.command()
def info():
    """Show importer package information"""
    try:
        from . import __version__, __author__
    except ImportError:
        from database.importers import __version__, __author__
    
    click.echo(f"Database Importers v{__version__}")
    click.echo(f"Author: {__author__}")
    click.echo(f"Available importers: BulkImporter, CsvImporter")


if __name__ == '__main__':
    cli()