"""
PCI Mapping Utilities Module

This module contains utilities for processing PCI DSS control to AWS Config rule mappings,
including data processing, schema generation, and database-friendly format creation.
"""

from .process_pci_mapping import PCIMappingProcessor

__all__ = [
    'PCIMappingProcessor'
]