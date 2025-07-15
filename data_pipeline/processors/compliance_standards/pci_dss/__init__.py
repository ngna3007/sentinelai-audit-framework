"""
PCI DSS v4.0.1 Modular Control Extractor

This module provides a modern, modular architecture for extracting PCI DSS v4.0.1 
compliance controls from markdown documents. The architecture is designed for 
maintainability, testability, and ease of extension.

Key Components:
- main: CLI entry point for all extraction operations
- core.extractor: Central orchestration and control extraction logic
- text_processors.compliance_standards.pci_dss: Text cleaning and parsing utilities
- core.content_builders: Content assembly and formatting
- core.metadata_generators: Quality scoring and metadata generation
- core.csv_generator: CSV generation for database import (PostgreSQL bulk import)

Usage:
    # Use the CLI interface (recommended)
    python -m extractors.pci_dss_v4_0_1.main extract
    
    # Or import specific components
    from extractors.pci_dss_v4_0_1.core import ControlExtractor

Architecture Benefits:
- Single responsibility principle per module
- Comprehensive quality scoring and token analysis
- Multiple output formats (Markdown, JSON, CSV)
- Ready for production and team collaboration
"""

# Import components from new modular structure
from ...chunking.compliance_standards.pci_dss.extractor import ControlExtractor
from data_pipeline.output_generators.compliance_standards.pci_dss.csv_generator import PCIDSSCSVGenerator as CSVGenerator
from ...text_processors.compliance_standards.pci_dss.text_processor import TextProcessor, ControlIDDetector
from ...chunking.compliance_standards.pci_dss.content_builder import ControlContentBuilder
from ...metadata_generators.compliance_standards.pci_dss.metadata_generator import ValidationMetadataGenerator, ProductionMetadataGenerator

__all__ = [
    'ControlExtractor',
    'CSVGenerator', 
    'TextProcessor',
    'ControlIDDetector',
    'ControlContentBuilder',
    'ValidationMetadataGenerator',
    'ProductionMetadataGenerator',
] 