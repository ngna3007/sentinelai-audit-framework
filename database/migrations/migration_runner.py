#!/usr/bin/env python3
"""
Migration runner for orchestrating database migrations
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
from .create_tables import SupabaseTableCreator
from .schema_validator import SchemaValidator

class MigrationRunner:
    """Orchestrates the complete migration process"""
    
    def __init__(self):
        self.table_creator = SupabaseTableCreator()
        self.schema_validator = SchemaValidator()
    
    def run_migration(self, 
                     validate_schemas: bool = True,
                     create_tables: bool = True,
                     dry_run: bool = False) -> Dict[str, Any]:
        """Run the complete migration process."""
        results = {
            'validation': {},
            'creation': {},
            'success': False,
            'errors': []
        }
        
        try:
            # Step 1: Validate schemas
            if validate_schemas:
                print("�� Validating schemas...")
                validation_results = self.schema_validator.validate_all_schemas()
                results['validation'] = validation_results
                
                # Check for validation errors
                invalid_schemas = [
                    path for path, (is_valid, _) in validation_results.items() 
                    if not is_valid
                ]
                
                if invalid_schemas:
                    error_msg = f"Found {len(invalid_schemas)} invalid schemas"
                    results['errors'].append(error_msg)
                    print(f"❌ {error_msg}")
                    for schema in invalid_schemas:
                        print(f"   - {schema}")
                    
                    if not dry_run:
                        return results
            
            # Step 2: Create tables
            if create_tables:
                print("🏗️  Creating tables...")
                if dry_run:
                    print("DRY RUN: Would create tables")
                    results['creation'] = {'dry_run': True}
                else:
                    creation_results = self.table_creator.create_all_tables()
                    results['creation'] = creation_results
                    
                    # Check for creation errors
                    failed_creations = [
                        path for path, result in creation_results.items() 
                        if not result['success']
                    ]
                    
                    if failed_creations:
                        error_msg = f"Failed to create {len(failed_creations)} tables"
                        results['errors'].append(error_msg)
                        print(f"❌ {error_msg}")
            
            results['success'] = len(results['errors']) == 0
            
            if results['success']:
                print("✅ Migration completed successfully!")
            else:
                print("❌ Migration completed with errors")
            
            return results
            
        except Exception as e:
            error_msg = f"Migration failed: {str(e)}"
            results['errors'].append(error_msg)
            print(f"❌ {error_msg}")
            return results
    
    def rollback_tables(self, table_names: List[str]) -> Dict[str, Any]:
        """Rollback specific tables."""
        results = {}
        
        for table_name in table_names:
            print(f"🗑️  Dropping table: {table_name}")
            result = self.table_creator.drop_table(table_name)
            results[table_name] = result
            
            if result['success']:
                print(f"✅ Dropped table: {table_name}")
            else:
                print(f"❌ Failed to drop table {table_name}: {result['error']}")
        
        return results
    
    def list_existing_tables(self) -> Dict[str, Any]:
        """List all existing tables."""
        return self.table_creator.list_tables()
    
    def get_table_details(self, table_name: str) -> Dict[str, Any]:
        """Get detailed information about a table."""
        return self.table_creator.get_table_info(table_name)

def main():
    """Main function to run migrations."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Run database migrations')
    parser.add_argument('--validate-only', action='store_true', 
                       help='Only validate schemas, do not create tables')
    parser.add_argument('--create-only', action='store_true',
                       help='Skip validation, only create tables')
    parser.add_argument('--dry-run', action='store_true',
                       help='Show what would be done without making changes')
    parser.add_argument('--rollback', nargs='+',
                       help='Rollback specific tables')
    parser.add_argument('--list-tables', action='store_true',
                       help='List existing tables')
    parser.add_argument('--table-info', type=str,
                       help='Get detailed info about a specific table')
    
    args = parser.parse_args()
    
    runner = MigrationRunner()
    
    if args.rollback:
        results = runner.rollback_tables(args.rollback)
        return results
    
    if args.list_tables:
        results = runner.list_existing_tables()
        print("EXISTING TABLES:")
        print(json.dumps(results, indent=2))
        return results
    
    if args.table_info:
        results = runner.get_table_details(args.table_info)
        print(f"TABLE INFO FOR {args.table_info}:")
        print(json.dumps(results, indent=2))
        return results
    
    # Run migration
    validate_schemas = not args.create_only
    create_tables = not args.validate_only
    
    results = runner.run_migration(
        validate_schemas=validate_schemas,
        create_tables=create_tables,
        dry_run=args.dry_run
    )
    
    return results

if __name__ == "__main__":
    main()