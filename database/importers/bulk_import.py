#!/usr/bin/env python3
"""
Bulk import orchestration
"""

import os
import csv
from pathlib import Path
from typing import Dict, Any, List
from .csv_importer import CsvImporter

class BulkImporter:
    """Orchestrates bulk imports from multiple sources"""
    
    def __init__(self, batch_size: int = 1000, show_progress: bool = True, validate_data: bool = True):
        self.csv_importer = CsvImporter(batch_size=batch_size, show_progress=show_progress)
        self.show_progress = show_progress
        self.validate_data = validate_data
    
    def import_all(self, source_dir: str = None) -> Dict[str, Any]:
        """Import all data from source directory"""
        if source_dir is None:
            base_path = Path(__file__).parent.parent.parent
            source_dir = base_path / "shared_data" / "outputs"
        
        results = {
            'success': True,
            'imported_counts': {},
            'errors': [],
            'validation_warnings': []
        }
        
        # Define table mappings with expected schemas
        table_mappings = {
            'pci_dss_controls.csv': {
                'table': 'pci_dss_controls',
                'required_columns': ['control_id', 'chunk'],
                'optional_columns': ['requirement', 'metadata', 'id']
            },
            'aws_config_rules_guidance.csv': {
                'table': 'aws_config_rules_guidance',
                'required_columns': ['config_rule', 'chunk'],
                'optional_columns': ['metadata', 'id']
            },
            'pci_aws_config_rule_mapping.csv': {
                'table': 'pci_aws_config_rule_mappings',
                'required_columns': ['control_id', 'config_rules'],
                'optional_columns': ['id']
            }
        }
        
        if self.show_progress:
            print(f"🔍 Scanning directory: {source_dir}")
        
        # First, validate all files if validation is enabled
        if self.validate_data:
            validation_results = self._validate_csv_files(source_dir, table_mappings)
            if validation_results['errors']:
                results['errors'].extend(validation_results['errors'])
                results['success'] = False
                return results
            if validation_results['warnings']:
                results['validation_warnings'].extend(validation_results['warnings'])
        
        # Process each CSV file
        files_processed = 0
        total_files = len([f for f in os.listdir(source_dir) if f in table_mappings])
        
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                if file in table_mappings:
                    files_processed += 1
                    file_path = os.path.join(root, file)
                    mapping = table_mappings[file]
                    table_name = mapping['table']
                    
                    if self.show_progress:
                        print(f"📥 [{files_processed}/{total_files}] Importing {file} into {table_name}...")
                    
                    try:
                        result = self.csv_importer.import_file(file_path, table_name)
                        
                        if result['success']:
                            results['imported_counts'][table_name] = result['imported_count']
                            if self.show_progress:
                                print(f"✅ Imported {result['imported_count']} records into {table_name}")
                        else:
                            results['success'] = False
                            error_msg = f"Failed to import {file}: {result['error']}"
                            results['errors'].append(error_msg)
                            if self.show_progress:
                                print(f"❌ {error_msg}")
                    except Exception as e:
                        results['success'] = False
                        error_msg = f"Unexpected error importing {file}: {str(e)}"
                        results['errors'].append(error_msg)
                        if self.show_progress:
                            print(f"❌ {error_msg}")
        
        if files_processed == 0:
            results['errors'].append(f"No recognized CSV files found in {source_dir}")
            results['success'] = False
        
        return results
    
    def _validate_csv_files(self, source_dir: str, table_mappings: Dict[str, Dict]) -> Dict[str, List[str]]:
        """Validate CSV files before import"""
        validation_results = {
            'errors': [],
            'warnings': []
        }
        
        if self.show_progress:
            print("🔍 Validating CSV files...")
        
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                if file in table_mappings:
                    file_path = os.path.join(root, file)
                    mapping = table_mappings[file]
                    
                    # Validate file structure
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            reader = csv.DictReader(f)
                            headers = reader.fieldnames
                            
                            if not headers:
                                validation_results['errors'].append(f"{file}: No headers found")
                                continue
                            
                            # Check required columns
                            missing_required = set(mapping['required_columns']) - set(headers)
                            if missing_required:
                                validation_results['errors'].append(
                                    f"{file}: Missing required columns: {', '.join(missing_required)}"
                                )
                            
                            # Check for unexpected columns
                            expected_columns = set(mapping['required_columns'] + mapping['optional_columns'])
                            unexpected_columns = set(headers) - expected_columns
                            if unexpected_columns:
                                validation_results['warnings'].append(
                                    f"{file}: Unexpected columns (will be ignored): {', '.join(unexpected_columns)}"
                                )
                            
                            # Validate first few rows for data integrity
                            row_count = 0
                            for row in reader:
                                row_count += 1
                                if row_count > 5:  # Only check first 5 rows
                                    break
                                
                                # Check for empty required fields
                                for req_col in mapping['required_columns']:
                                    if req_col in row and not row[req_col].strip():
                                        validation_results['warnings'].append(
                                            f"{file}: Row {row_count} has empty required field '{req_col}'"
                                        )
                            
                            if self.show_progress:
                                print(f"✅ {file}: Validation passed ({row_count}+ rows)")
                                
                    except Exception as e:
                        validation_results['errors'].append(f"{file}: Validation error - {str(e)}")
        
        return validation_results
