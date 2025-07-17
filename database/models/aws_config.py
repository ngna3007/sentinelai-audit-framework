#!/usr/bin/env python3
"""AWS Config Rules models"""

from typing import Dict, Any, List
from dataclasses import dataclass
from uuid import UUID

@dataclass
class AwsConfigRule:
    """AWS Config Rule model"""
    id: UUID
    config_rule: str
    chunk: str
    metadata: Dict[str, Any]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AwsConfigRule':
        return cls(
            id=data['id'],
            config_rule=data['config_rule'],
            chunk=data['chunk'],
            metadata=data['metadata']
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': str(self.id),
            'config_rule': self.config_rule,
            'chunk': self.chunk,
            'metadata': self.metadata
        }

@dataclass
class PciAwsConfigMapping:
    """PCI DSS to AWS Config Rule mapping model"""
    id: UUID
    control_id: str
    config_rules: List[Dict[str, Any]]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PciAwsConfigMapping':
        return cls(
            id=data['id'],
            control_id=data['control_id'],
            config_rules=data['config_rules']
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': str(self.id),
            'control_id': self.control_id,
            'config_rules': self.config_rules
        }