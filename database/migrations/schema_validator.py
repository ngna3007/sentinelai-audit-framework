#!/usr/bin/env python3
"""
Schema validation utilities for database migrations
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Any, Tuple

class SchemaValidator:
    """Validates JSON schema files before table creation"""
    
    def __init__(self):
        self.required_fields = ['table_name', 'columns']
        self.valid_column_types = [
            'UUID', 'VARCHAR', 'TEXT', 'INTEGER', 'BIGINT', 'SMALLINT',
            'DECIMAL', 'NUMERIC', 'REAL', 'DOUBLE PRECISION', 'BOOLEAN',
            'DATE', 'TIME', 'TIMESTAMP', 'JSONB', 'JSON', 'ARRAY'
        ]
        self.valid_constraints = [
            'PRIMARY KEY', 'NOT NULL', 'UNIQUE', 'DEFAULT', 'CHECK',
            'FOREIGN KEY', 'REFERENCES'
        ]
        self.valid_index_types = ['PRIMARY', 'UNIQUE', 'GIN', 'BTREE', 'HASH']
    
    def validate_schema_file(self, schema_path: str) -> Tuple[bool, List[str]]:
        """Validate a single schema file."""
        errors = []
        
        try:
            # Read and parse JSON
            with open(schema_path, 'r') as f:
                schema = json.load(f)
        except FileNotFoundError:
            return False, [f"Schema file not found: {schema_path}"]
        except json.JSONDecodeError as e:
            return False, [f"Invalid JSON in {schema_path}: {e}"]
        
        # Validate required fields
        for field in self.required_fields:
            if field not in schema:
                errors.append(f"Missing required field: {field}")
        
        if errors:
            return False, errors
        
        # Validate table name
        if not isinstance(schema['table_name'], str):
            errors.append("table_name must be a string")
        elif not schema['table_name'].replace('_', '').isalnum():
            errors.append("table_name must contain only alphanumeric characters and underscores")
        
        # Validate columns
        if not isinstance(schema['columns'], list):
            errors.append("columns must be a list")
        else:
            column_errors = self._validate_columns(schema['columns'])
            errors.extend(column_errors)
        
        # Validate indexes (optional)
        if 'indexes' in schema:
            index_errors = self._validate_indexes(schema['indexes'], schema['table_name'])
            errors.extend(index_errors)
        
        return len(errors) == 0, errors
    
    def _validate_columns(self, columns: List[Dict[str, Any]]) -> List[str]:
        """Validate column definitions."""
        errors = []
        column_names = set()
        
        for i, column in enumerate(columns):
            # Check required column fields
            if 'name' not in column:
                errors.append(f"Column {i}: missing 'name' field")
                continue
            
            if 'type' not in column:
                errors.append(f"Column {column['name']}: missing 'type' field")
                continue
            
            # Check for duplicate column names
            if column['name'] in column_names:
                errors.append(f"Duplicate column name: {column['name']}")
            else:
                column_names.add(column['name'])
            
            # Validate column type
            col_type = column['type']
            if not any(valid_type in col_type.upper() for valid_type in self.valid_column_types):
                errors.append(f"Column {column['name']}: invalid type '{col_type}'")
            
            # Validate constraints
            if 'constraints' in column:
                constraint_errors = self._validate_constraints(column['constraints'], column['name'])
                errors.extend(constraint_errors)
        
        return errors
    
    def _validate_constraints(self, constraints: List[str], column_name: str) -> List[str]:
        """Validate column constraints."""
        errors = []
        
        for constraint in constraints:
            # Basic constraint validation
            if not any(valid_constraint in constraint.upper() for valid_constraint in self.valid_constraints):
                errors.append(f"Column {column_name}: potentially invalid constraint '{constraint}'")
        
        return errors
    
    def _validate_indexes(self, indexes: List[Dict[str, Any]], table_name: str) -> List[str]:
        """Validate index definitions."""
        errors = []
        index_names = set()
        
        for i, index in enumerate(indexes):
            # Check required index fields
            if 'name' not in index:
                errors.append(f"Index {i}: missing 'name' field")
                continue
            
            if 'type' not in index:
                errors.append(f"Index {index['name']}: missing 'type' field")
                continue
            
            if 'columns' not in index:
                errors.append(f"Index {index['name']}: missing 'columns' field")
                continue
            
            # Check for duplicate index names
            if index['name'] in index_names:
                errors.append(f"Duplicate index name: {index['name']}")
            else:
                index_names.add(index['name'])
            
            # Validate index type
            if index['type'] not in self.valid_index_types:
                errors.append(f"Index {index['name']}: invalid type '{index['type']}'")
            
            # Validate columns is a list
            if not isinstance(index['columns'], list):
                errors.append(f"Index {index['name']}: columns must be a list")
        
        return errors
    
    def validate_all_schemas(self, schema_directory: str = None) -> Dict[str, Tuple[bool, List[str]]]:
        """Validate all schema files in a directory."""
        if schema_directory is None:
            base_path = Path(__file__).parent.parent.parent
            schema_directory = base_path / "shared_data" / "outputs"
        
        results = {}
        
        for root, dirs, files in os.walk(schema_directory):
            for file in files:
                if file == "database_schema.json":
                    schema_path = os.path.join(root, file)
                    is_valid, errors = self.validate_schema_file(schema_path)
                    results[schema_path] = (is_valid, errors)
        
        return results

def main():
    """Main function to validate all schemas."""
    validator = SchemaValidator()
    results = validator.validate_all_schemas()
    
    print("SCHEMA VALIDATION RESULTS")
    print("="*50)
    
    valid_count = 0
    invalid_count = 0
    
    for schema_path, (is_valid, errors) in results.items():
        if is_valid:
            print(f"✅ {schema_path}: Valid")
            valid_count += 1
        else:
            print(f"❌ {schema_path}: Invalid")
            for error in errors:
                print(f"   - {error}")
            invalid_count += 1
    
    print(f"\nSummary: {valid_count} valid, {invalid_count} invalid")
    
    return results

if __name__ == "__main__":
    main()