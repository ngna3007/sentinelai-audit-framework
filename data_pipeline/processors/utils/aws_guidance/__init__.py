"""
AWS Guidance Utilities Module

This module contains utility functions for processing AWS guidance data,
including canonicalization, extraction, and duplicate removal operations.
"""

from .canonicalize_mappings import main as canonicalize_mappings
from .extract_unique_config_rules import extract_unique_config_rules
from .extract_unique_pci_controls import extract_unique_pci_controls
from .remove_duplicates_mappings import main as remove_duplicates_mappings
from .replace_guidance_with_canonical import main as replace_guidance_with_canonical

__all__ = [
    'canonicalize_mappings',
    'extract_unique_config_rules',
    'extract_unique_pci_controls',
    'remove_duplicates_mappings',
    'replace_guidance_with_canonical'
]