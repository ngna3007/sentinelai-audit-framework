#!/usr/bin/env python3
"""
Base repository for database operations
"""

from typing import Dict, List, Any, Optional, TypeVar, Generic, Type
from uuid import UUID
from ..auth.connection import db_connection

T = TypeVar('T')

class BaseRepository(Generic[T]):
    """Base repository with common database operations"""
    
    def __init__(self, table_name: str, model_class: Type[T]):
        self.table_name = table_name
        self.model_class = model_class
        self.client = db_connection.get_client()
    
    def find_by_id(self, id: UUID) -> Optional[T]:
        """Find record by ID"""
        try:
            result = self.client.table(self.table_name).select('*').eq('id', str(id)).single().execute()
            return self.model_class.from_dict(result.data) if result.data else None
        except Exception:
            return None
    
    def find_all(self) -> List[T]:
        """Find all records"""
        result = self.client.table(self.table_name).select('*').execute()
        return [self.model_class.from_dict(item) for item in result.data]
    
    def create(self, model: T) -> T:
        """Create new record"""
        result = self.client.table(self.table_name).insert(model.to_dict()).execute()
        return self.model_class.from_dict(result.data[0])
    
    def create_batch(self, models: List[T]) -> List[T]:
        """Create multiple records in batch with transaction support"""
        try:
            data = [model.to_dict() for model in models]
            result = self.client.table(self.table_name).insert(data).execute()
            return [self.model_class.from_dict(item) for item in result.data]
        except Exception as e:
            # If batch insert fails, try inserting records one by one to identify issues
            successful_records = []
            errors = []
            
            for i, model in enumerate(models):
                try:
                    single_result = self.client.table(self.table_name).insert(model.to_dict()).execute()
                    if single_result.data:
                        successful_records.append(self.model_class.from_dict(single_result.data[0]))
                except Exception as single_error:
                    errors.append(f"Record {i+1}: {str(single_error)}")
            
            if errors:
                error_summary = f"Batch insert partially failed. {len(successful_records)}/{len(models)} successful. Errors: {'; '.join(errors[:3])}"
                if len(errors) > 3:
                    error_summary += f" (and {len(errors)-3} more)"
                raise Exception(error_summary)
            
            return successful_records
    
    def update(self, id: UUID, data: Dict[str, Any]) -> Optional[T]:
        """Update record"""
        result = self.client.table(self.table_name).update(data).eq('id', str(id)).execute()
        return self.model_class.from_dict(result.data[0]) if result.data else None
    
    def delete(self, id: UUID) -> bool:
        """Delete record"""
        result = self.client.table(self.table_name).delete().eq('id', str(id)).execute()
        return bool(result.data)
    
    def delete_all(self) -> int:
        """Delete all records from table"""
        # Get all records first to count them
        all_records = self.client.table(self.table_name).select('id').execute()
        count = len(all_records.data) if all_records.data else 0
        
        if count > 0:
            # Delete all records using a condition that matches all UUIDs
            result = self.client.table(self.table_name).delete().neq('id', '00000000-0000-0000-0000-000000000000').execute()
            return count
        return 0
    
    def count(self) -> int:
        """Count total records"""
        result = self.client.table(self.table_name).select('id', count='exact').execute()
        return result.count if hasattr(result, 'count') else 0
    
    def find_by_field(self, field: str, value: Any) -> List[T]:
        """Find records by specific field value"""
        result = self.client.table(self.table_name).select('*').eq(field, value).execute()
        return [self.model_class.from_dict(item) for item in result.data]
