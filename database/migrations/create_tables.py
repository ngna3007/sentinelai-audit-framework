#!/usr/bin/env python3
"""
Database Migration Script for Supabase
Creates tables from JSON schema files
"""

import json
import os
import uuid
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class SupabaseTableCreator:
    """Creates and manages database tables from JSON schema files"""
    
    def __init__(self):
        self.supabase_url = os.getenv('SUPABASE_URL')
        self.supabase_key = os.getenv('SUPABASE_SERVICE_ROLE_KEY')
        
        if not self.supabase_url or not self.supabase_key:
            raise ValueError("SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be set in .env")
        
        self.supabase: Client = create_client(self.supabase_url, self.supabase_key)
    
    def read_schema_file(self, schema_path: str) -> Dict[str, Any]:
        """Read JSON schema file and return schema definition."""
        try:
            with open(schema_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Schema file not found: {schema_path}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in schema file {schema_path}: {e}")
    
    def generate_create_table_sql(self, schema: Dict[str, Any]) -> str:
        """Generate PostgreSQL CREATE TABLE statement from schema."""
        table_name = schema['table_name']
        columns = schema['columns']
        
        # Build column definitions
        column_definitions = []
        for column in columns:
            col_name = column['name']
            col_type = column['type']
            constraints = column.get('constraints', [])
            
            # Build constraint string
            constraint_str = ' '.join(constraints)
            column_definitions.append(f"{col_name} {col_type} {constraint_str}".strip())
        
        # Create table SQL
        columns_str = ',\n            '.join(column_definitions)
        create_table_sql = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            {columns_str}
        );
        """
        
        return create_table_sql
    
    def generate_index_sql(self, schema: Dict[str, Any]) -> List[str]:
        """Generate CREATE INDEX statements from schema."""
        indexes = schema.get('indexes', [])
        table_name = schema['table_name']
        index_statements = []
        
        for index in indexes:
            index_name = index['name']
            index_type = index['type']
            columns = index['columns']
            
            if index_type == 'PRIMARY':
                # Primary key is already defined in table creation
                continue
            elif index_type == 'UNIQUE':
                index_statements.append(
                    f"CREATE UNIQUE INDEX IF NOT EXISTS {index_name} ON {table_name} ({', '.join(columns)});"
                )
            elif index_type == 'GIN':
                index_statements.append(
                    f"CREATE INDEX IF NOT EXISTS {index_name} ON {table_name} USING GIN ({', '.join(columns)});"
                )
            else:
                index_statements.append(
                    f"CREATE INDEX IF NOT EXISTS {index_name} ON {table_name} ({', '.join(columns)});"
                )
        
        return index_statements
    
    def execute_sql(self, sql: str) -> Dict[str, Any]:
        """Execute SQL statement against Supabase."""
        try:
            # Try to use Supabase's SQL execution via RPC if available
            result = self.supabase.rpc('exec_sql', {'sql': sql}).execute()
            return {"success": True, "result": result}
        except Exception as e:
            # Fallback: Create tables using Supabase REST API instead of raw SQL
            print(f"SQL execution failed: {str(e)}")
            print("Note: Direct SQL execution not available. Tables should be created manually in Supabase dashboard.")
            return {"success": False, "error": f"SQL execution not supported: {str(e)}"}
    
    def create_table_from_schema(self, schema_path: str) -> Dict[str, Any]:
        """Create table from JSON schema file."""
        print(f"Processing schema: {schema_path}")
        
        # Read schema
        schema = self.read_schema_file(schema_path)
        table_name = schema['table_name']
        
        # Generate SQL statements
        create_table_sql = self.generate_create_table_sql(schema)
        index_statements = self.generate_index_sql(schema)
        
        print(f"Creating table: {table_name}")
        print(f"SQL: {create_table_sql}")
        
        # Execute table creation
        table_result = self.execute_sql(create_table_sql)
        if not table_result['success']:
            return table_result
        
        # Execute index creation
        for index_sql in index_statements:
            print(f"Creating index: {index_sql}")
            index_result = self.execute_sql(index_sql)
            if not index_result['success']:
                print(f"Warning: Index creation failed: {index_result['error']}")
        
        return {"success": True, "table": table_name, "schema": schema}
    
    def create_all_tables(self, schema_directory: str = None) -> Dict[str, Any]:
        """Create all tables from schema files in directory."""
        if schema_directory is None:
            # Default to your shared_data outputs directory
            base_path = Path(__file__).parent.parent.parent
            schema_directory = base_path / "shared_data" / "outputs"
        
        schema_files = []
        for root, dirs, files in os.walk(schema_directory):
            for file in files:
                if file == "database_schema.json":
                    schema_files.append(os.path.join(root, file))
        
        results = {}
        for schema_file in schema_files:
            try:
                result = self.create_table_from_schema(schema_file)
                results[schema_file] = result
            except Exception as e:
                results[schema_file] = {"success": False, "error": str(e)}
        
        return results
    
    def drop_table(self, table_name: str) -> Dict[str, Any]:
        """Drop a table from the database."""
        sql = f"DROP TABLE IF EXISTS {table_name} CASCADE;"
        return self.execute_sql(sql)
    
    def list_tables(self) -> Dict[str, Any]:
        """List all tables in the database."""
        sql = """
        SELECT table_name, table_type 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
        ORDER BY table_name;
        """
        return self.execute_sql(sql)
    
    def get_table_info(self, table_name: str) -> Dict[str, Any]:
        """Get detailed information about a table."""
        sql = f"""
        SELECT column_name, data_type, is_nullable, column_default
        FROM information_schema.columns 
        WHERE table_name = '{table_name}'
        ORDER BY ordinal_position;
        """
        return self.execute_sql(sql)

def main():
    """Main function to create all tables."""
    try:
        creator = SupabaseTableCreator()
        
        # Create all tables from schema files
        results = creator.create_all_tables()
        
        # Print results
        print("\n" + "="*50)
        print("TABLE CREATION RESULTS")
        print("="*50)
        
        success_count = 0
        error_count = 0
        
        for schema_file, result in results.items():
            if result['success']:
                print(f"✅ {schema_file}: {result['table']} created successfully")
                success_count += 1
            else:
                print(f"❌ {schema_file}: {result['error']}")
                error_count += 1
        
        print(f"\nSummary: {success_count} successful, {error_count} failed")
        
        return results
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    main()
