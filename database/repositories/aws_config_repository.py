#!/usr/bin/env python3
"""
AWS Config Rule repository for database operations
"""

from typing import List, Optional, Dict, Any
from uuid import UUID
from .base import BaseRepository
from ..models.aws_config import AwsConfigRule

class AwsConfigRuleRepository(BaseRepository[AwsConfigRule]):
    """Repository for AWS Config Rule operations"""
    
    def __init__(self):
        super().__init__('aws_config_rules_guidance', AwsConfigRule)
    
    def find_by_config_rule(self, config_rule: str) -> List[AwsConfigRule]:
        """Find records by config rule name"""
        return self.find_by_field('config_rule', config_rule)
    
    def search_by_content(self, search_term: str) -> List[AwsConfigRule]:
        """Search records by content in chunk field"""
        result = self.client.table(self.table_name)\
            .select('*')\
            .ilike('chunk', f'%{search_term}%')\
            .execute()
        return [self.model_class.from_dict(item) for item in result.data]
    
    def find_by_metadata_key(self, key: str, value: Any) -> List[AwsConfigRule]:
        """Find records by metadata key-value pair"""
        # Using JSONB query for metadata
        result = self.client.table(self.table_name)\
            .select('*')\
            .eq(f'metadata->{key}', str(value))\
            .execute()
        return [self.model_class.from_dict(item) for item in result.data]
    
    def get_all_config_rules(self) -> List[str]:
        """Get list of all unique config rule names"""
        result = self.client.table(self.table_name)\
            .select('config_rule')\
            .execute()
        
        # Extract unique config rule names
        config_rules = set()
        for item in result.data:
            config_rules.add(item['config_rule'])
        
        return sorted(list(config_rules))
    
    def get_stats(self) -> Dict[str, Any]:
        """Get repository statistics"""
        total_count = self.count()
        config_rules = self.get_all_config_rules()
        
        return {
            'total_records': total_count,
            'unique_config_rules': len(config_rules),
            'config_rule_names': config_rules
        }
