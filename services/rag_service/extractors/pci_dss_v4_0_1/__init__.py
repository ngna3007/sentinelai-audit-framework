"""
PCI DSS v4.0.1 Modular Control Extractor

This module provides a modern, modular architecture for extracting PCI DSS v4.0.1 
compliance controls from markdown documents. The architecture is designed for 
maintainability, testability, and ease of extension.

Key Components:
- main: CLI entry point for all extraction operations
- core.extractor: Central orchestration and control extraction logic
- core.text_processors: Text cleaning and parsing utilities
- core.content_builders: Content assembly and formatting
- core.metadata_generators: Quality scoring and metadata generation
- core.bedrock_csv_generator: CSV generation for Bedrock Knowledge Base

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

# Import core components for programmatic access
from .core.extractor import ControlExtractor
from .core.bedrock_csv_generator import BedrockCSVGenerator
from .core.text_processors import TextProcessor, ControlIDDetector
from .core.content_builders import ControlContentBuilder
from .core.metadata_generators import ValidationMetadataGenerator, ProductionMetadataGenerator

__all__ = [
    'ControlExtractor',
    'BedrockCSVGenerator', 
    'TextProcessor',
    'ControlIDDetector',
    'ControlContentBuilder',
    'ValidationMetadataGenerator',
    'ProductionMetadataGenerator',
] 