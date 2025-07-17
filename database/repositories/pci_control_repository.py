#!/usr/bin/env python3
"""
PCI Control repository for database operations
"""

from typing import List, Optional, Dict, Any
from uuid import UUID
from .base import BaseRepository
from ..models.pci_controls import PciControl

class PciControlRepository(BaseRepository[PciControl]):
    """Repository for PCI DSS Control operations"""
    
    def __init__(self):
        super().__init__('pci_dss_controls', PciControl)
    
    def find_by_control_id(self, control_id: str) -> List[PciControl]:
        """Find records by control ID"""
        return self.find_by_field('control_id', control_id)
    
    def find_by_requirement(self, requirement: str) -> List[PciControl]:
        """Find records by requirement text"""
        return self.find_by_field('requirement', requirement)
    
    def search_by_content(self, search_term: str) -> List[PciControl]:
        """Search records by content in chunk field"""
        result = self.client.table(self.table_name)\
            .select('*')\
            .ilike('chunk', f'%{search_term}%')\
            .execute()
        return [self.model_class.from_dict(item) for item in result.data]
    
    def search_by_requirement_text(self, search_term: str) -> List[PciControl]:
        """Search records by content in requirement field"""
        result = self.client.table(self.table_name)\
            .select('*')\
            .ilike('requirement', f'%{search_term}%')\
            .execute()
        return [self.model_class.from_dict(item) for item in result.data]
    
    def find_by_metadata_key(self, key: str, value: Any) -> List[PciControl]:
        """Find records by metadata key-value pair"""
        # Using JSONB query for metadata
        result = self.client.table(self.table_name)\
            .select('*')\
            .eq(f'metadata->{key}', str(value))\
            .execute()
        return [self.model_class.from_dict(item) for item in result.data]
    
    def get_all_control_ids(self) -> List[str]:
        """Get list of all unique control IDs"""
        result = self.client.table(self.table_name)\
            .select('control_id')\
            .execute()
        
        # Extract unique control IDs
        control_ids = set()
        for item in result.data:
            if item['control_id']:
                control_ids.add(item['control_id'])
        
        return sorted(list(control_ids))
    
    def get_all_requirements(self) -> List[str]:
        """Get list of all unique requirements"""
        result = self.client.table(self.table_name)\
            .select('requirement')\
            .execute()
        
        # Extract unique requirements
        requirements = set()
        for item in result.data:
            if item['requirement']:
                requirements.add(item['requirement'])
        
        return sorted(list(requirements))
    
    def get_controls_by_pattern(self, pattern: str) -> List[PciControl]:
        """Get controls where control_id matches a pattern (e.g., '1.%' for all 1.x controls)"""
        result = self.client.table(self.table_name)\
            .select('*')\
            .like('control_id', pattern)\
            .execute()
        return [self.model_class.from_dict(item) for item in result.data]
    
    def get_stats(self) -> Dict[str, Any]:
        """Get repository statistics"""
        total_count = self.count()
        control_ids = self.get_all_control_ids()
        requirements = self.get_all_requirements()
        
        # Count records with requirements vs without
        with_requirements = len([c for c in self.find_all() if c.requirement])
        without_requirements = total_count - with_requirements
        
        return {
            'total_records': total_count,
            'unique_control_ids': len(control_ids),
            'unique_requirements': len(requirements),
            'records_with_requirements': with_requirements,
            'records_without_requirements': without_requirements,
            'control_ids': control_ids
        }