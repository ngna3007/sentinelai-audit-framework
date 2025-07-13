#!/usr/bin/env python3
"""
CSV import functionality
"""

import csv
import json
import uuid
from pathlib import Path
from typing import Dict, List, Any, Optional
from ..auth.connection import db_connection

class CsvImporter:
    """Handles CSV file imports"""
    
    def __init__(self, batch_size: int = 1000, show_progress: bool = True):
        self.batch_size = batch_size
        self.show_progress = show_progress
        self.client = db_connection.get_client()
    
    def import_file(self, file_path: str, table_name: str) -> Dict[str, Any]:
        """Import CSV file into table"""
        try:
            imported_count = 0
            total_rows = self._count_csv_rows(file_path)
            
            if self.show_progress and total_rows > 0:
                print(f"   📊 Total rows to import: {total_rows}")
            
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                batch = []
                
                for row_num, row in enumerate(reader, 1):
                    try:
                        # Clean and validate row data
                        cleaned_row = self._clean_row_data(row, table_name)
                        if cleaned_row:
                            batch.append(cleaned_row)
                        
                        if len(batch) >= self.batch_size:
                            self._import_batch(table_name, batch)
                            imported_count += len(batch)
                            
                            if self.show_progress:
                                progress = (row_num / total_rows) * 100 if total_rows > 0 else 0
                                print(f"   📈 Progress: {row_num}/{total_rows} ({progress:.1f}%) - Imported: {imported_count}")
                            
                            batch = []
                            
                    except Exception as e:
                        if self.show_progress:
                            print(f"   ⚠️  Skipped row {row_num}: {str(e)}")
                        continue
                
                # Import remaining records
                if batch:
                    self._import_batch(table_name, batch)
                    imported_count += len(batch)
            
            return {
                'success': True,
                'imported_count': imported_count,
                'file': file_path,
                'total_rows': total_rows
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'file': file_path,
                'imported_count': imported_count
            }
    
    def _import_batch(self, table_name: str, batch: List[Dict[str, Any]]):
        """Import batch of records with error handling"""
        try:
            result = self.client.table(table_name).insert(batch).execute()
            return result
        except Exception as e:
            # Try importing records one by one to identify problematic records
            successful_imports = 0
            for i, record in enumerate(batch):
                try:
                    self.client.table(table_name).insert(record).execute()
                    successful_imports += 1
                except Exception as record_error:
                    if self.show_progress:
                        print(f"   ❌ Failed to import record {i+1} in batch: {str(record_error)}")
            
            if successful_imports < len(batch):
                raise Exception(f"Batch import partially failed. {successful_imports}/{len(batch)} records imported. Error: {str(e)}")
    
    def _clean_row_data(self, row: Dict[str, Any], table_name: str) -> Optional[Dict[str, Any]]:
        """Clean and validate row data based on table schema"""
        cleaned_row = {}
        
        # Add UUID if not present
        if 'id' not in row or not row['id']:
            cleaned_row['id'] = str(uuid.uuid4())
        else:
            cleaned_row['id'] = row['id']
        
        # Table-specific cleaning
        if table_name == 'pci_dss_controls':
            cleaned_row.update(self._clean_pci_control_row(row))
        elif table_name == 'aws_config_rules_guidance':
            cleaned_row.update(self._clean_aws_config_row(row))
        elif table_name == 'pci_aws_config_rule_mappings':
            cleaned_row.update(self._clean_mapping_row(row))
        else:
            # Generic cleaning for unknown tables
            for key, value in row.items():
                if key != 'id':
                    cleaned_row[key] = value.strip() if isinstance(value, str) else value
        
        return cleaned_row
    
    def _clean_pci_control_row(self, row: Dict[str, Any]) -> Dict[str, Any]:
        """Clean PCI control specific data"""
        cleaned = {}
        
        # Required fields
        if 'control_id' in row:
            cleaned['control_id'] = row['control_id'].strip()
        if 'chunk' in row:
            cleaned['chunk'] = row['chunk'].strip()
        
        # Optional fields
        if 'requirement' in row and row['requirement']:
            cleaned['requirement'] = row['requirement'].strip()
        
        # Handle metadata
        if 'metadata' in row and row['metadata']:
            try:
                if isinstance(row['metadata'], str):
                    cleaned['metadata'] = json.loads(row['metadata'])
                else:
                    cleaned['metadata'] = row['metadata']
            except json.JSONDecodeError:
                cleaned['metadata'] = {'raw': row['metadata']}
        else:
            cleaned['metadata'] = {}
        
        return cleaned
    
    def _clean_aws_config_row(self, row: Dict[str, Any]) -> Dict[str, Any]:
        """Clean AWS Config rule specific data"""
        cleaned = {}
        
        if 'config_rule' in row:
            cleaned['config_rule'] = row['config_rule'].strip()
        if 'chunk' in row:
            cleaned['chunk'] = row['chunk'].strip()
        
        # Handle metadata
        if 'metadata' in row and row['metadata']:
            try:
                if isinstance(row['metadata'], str):
                    cleaned['metadata'] = json.loads(row['metadata'])
                else:
                    cleaned['metadata'] = row['metadata']
            except json.JSONDecodeError:
                cleaned['metadata'] = {'raw': row['metadata']}
        else:
            cleaned['metadata'] = {}
        
        return cleaned
    
    def _clean_mapping_row(self, row: Dict[str, Any]) -> Dict[str, Any]:
        """Clean mapping specific data"""
        cleaned = {}
        
        if 'control_id' in row:
            cleaned['control_id'] = row['control_id'].strip()
        
        # Handle config_rules JSON array
        if 'config_rules' in row and row['config_rules']:
            try:
                if isinstance(row['config_rules'], str):
                    cleaned['config_rules'] = json.loads(row['config_rules'])
                else:
                    cleaned['config_rules'] = row['config_rules']
            except json.JSONDecodeError:
                cleaned['config_rules'] = []
        else:
            cleaned['config_rules'] = []
        
        return cleaned
    
    def _count_csv_rows(self, file_path: str) -> int:
        """Count total rows in CSV file for progress tracking"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                next(reader)  # Skip header
                return sum(1 for _ in reader)
        except Exception:
            return 0
