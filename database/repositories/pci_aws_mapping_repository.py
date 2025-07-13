#!/usr/bin/env python3
"""
PCI to AWS Config mapping repository for database operations
"""

from typing import List, Optional, Dict, Any
from uuid import UUID
from .base import BaseRepository
from ..models.aws_config import PciAwsConfigMapping

class PciAwsConfigMappingRepository(BaseRepository[PciAwsConfigMapping]):
    """Repository for PCI DSS to AWS Config Rule mapping operations"""
    
    def __init__(self):
        super().__init__('pci_aws_config_rule_mappings', PciAwsConfigMapping)
    
    def find_by_control_id(self, control_id: str) -> Optional[PciAwsConfigMapping]:
        """Find mapping by PCI control ID"""
        mappings = self.find_by_field('control_id', control_id)
        return mappings[0] if mappings else None
    
    def find_by_config_rule(self, config_rule_name: str) -> List[PciAwsConfigMapping]:
        """Find mappings that contain a specific AWS Config rule"""
        # This requires a more complex query to search within the JSONB array
        result = self.client.table(self.table_name)\
            .select('*')\
            .contains('config_rules', [{'rule_name': config_rule_name}])\
            .execute()
        return [self.model_class.from_dict(item) for item in result.data]
    
    def search_config_rules_by_service(self, aws_service: str) -> List[PciAwsConfigMapping]:
        """Find mappings that contain config rules for a specific AWS service"""
        # Search for service name in the config_rules JSONB field
        result = self.client.table(self.table_name)\
            .select('*')\
            .ilike('config_rules', f'%{aws_service}%')\
            .execute()
        return [self.model_class.from_dict(item) for item in result.data]
    
    def get_all_control_ids(self) -> List[str]:
        """Get list of all PCI control IDs that have mappings"""
        result = self.client.table(self.table_name)\
            .select('control_id')\
            .execute()
        
        control_ids = set()
        for item in result.data:
            control_ids.add(item['control_id'])
        
        return sorted(list(control_ids))
    
    def get_all_config_rules(self) -> List[str]:
        """Get list of all unique AWS Config rule names across all mappings"""
        mappings = self.find_all()
        config_rules = set()
        
        for mapping in mappings:
            for rule in mapping.config_rules:
                if isinstance(rule, dict) and 'rule_name' in rule:
                    config_rules.add(rule['rule_name'])
        
        return sorted(list(config_rules))
    
    def get_mappings_without_config_rules(self) -> List[PciAwsConfigMapping]:
        """Get mappings that have empty or null config_rules"""
        result = self.client.table(self.table_name)\
            .select('*')\
            .or_('config_rules.is.null,config_rules.eq.[]')\
            .execute()
        return [self.model_class.from_dict(item) for item in result.data]
    
    def get_config_rule_coverage(self) -> Dict[str, Any]:
        """Get statistics about config rule coverage"""
        all_mappings = self.find_all()
        total_controls = len(all_mappings)
        
        controls_with_rules = 0
        controls_without_rules = 0
        total_rules = 0
        
        for mapping in all_mappings:
            if mapping.config_rules and len(mapping.config_rules) > 0:
                # Filter out empty rules
                valid_rules = [r for r in mapping.config_rules if r and (isinstance(r, dict) and r.get('rule_name'))]
                if valid_rules:
                    controls_with_rules += 1
                    total_rules += len(valid_rules)
                else:
                    controls_without_rules += 1
            else:
                controls_without_rules += 1
        
        coverage_percentage = (controls_with_rules / total_controls * 100) if total_controls > 0 else 0
        
        return {
            'total_controls': total_controls,
            'controls_with_rules': controls_with_rules,
            'controls_without_rules': controls_without_rules,
            'total_config_rules': total_rules,
            'coverage_percentage': round(coverage_percentage, 2),
            'average_rules_per_control': round(total_rules / controls_with_rules, 2) if controls_with_rules > 0 else 0
        }
    
    def get_stats(self) -> Dict[str, Any]:
        """Get repository statistics"""
        total_count = self.count()
        control_ids = self.get_all_control_ids()
        config_rules = self.get_all_config_rules()
        coverage = self.get_config_rule_coverage()
        
        return {
            'total_mappings': total_count,
            'unique_control_ids': len(control_ids),
            'unique_config_rules': len(config_rules),
            'coverage_stats': coverage
        }
