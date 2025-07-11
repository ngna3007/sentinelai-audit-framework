"""
PCI DSS Control Extractor - Core Components

This module contains the refactored core components for extracting PCI DSS controls.
The original 853-line extractor has been broken down into focused modules for better
maintainability and testing.

Modules:
    extractor: Main control extraction logic and table parsing
    text_processors: Text cleaning, parsing, and processing utilities  
    content_builders: Content assembly and formatting for different output types
    metadata_generators: Validation and production metadata generation
    bedrock_csv_generator: CSV generation for Bedrock Knowledge Base
"""

from .extractor import ControlExtractor
from .text_processors import TextProcessor, ControlIDDetector, SectionExtractor
from .content_builders import ControlContentBuilder, MarkdownFormatter
from .metadata_generators import ValidationMetadataGenerator, ProductionMetadataGenerator
from .bedrock_csv_generator import BedrockCSVGenerator

__all__ = [
    'ControlExtractor',
    'TextProcessor', 
    'ControlIDDetector',
    'SectionExtractor',
    'ControlContentBuilder',
    'MarkdownFormatter',
    'ValidationMetadataGenerator',
    'ProductionMetadataGenerator',
    'BedrockCSVGenerator'
] 