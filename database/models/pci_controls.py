#!/usr/bin/env python3
"""PCI DSS Control models"""

from typing import Optional, Dict, Any
from dataclasses import dataclass
from uuid import UUID

@dataclass
class PciControl:
    """PCI DSS Control model"""
    id: UUID
    control_id: str
    requirement: Optional[str]
    chunk: str
    metadata: Dict[str, Any]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PciControl':
        return cls(
            id=data['id'],
            control_id=data['control_id'],
            requirement=data.get('requirement'),
            chunk=data['chunk'],
            metadata=data['metadata']
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': str(self.id),
            'control_id': self.control_id,
            'requirement': self.requirement,
            'chunk': self.chunk,
            'metadata': self.metadata
        }