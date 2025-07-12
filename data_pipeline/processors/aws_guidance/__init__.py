"""
AWS Config Guidance Processor

This module provides a specialized processor for handling PCI-DSS v4.0.1 AWS Config 
Guidance documents. It focuses on PDF to Markdown conversion and content extraction
optimized for AWS Config rule mapping and compliance guidance.

Key Components:
- main: CLI entry point for conversion and processing operations
- core.pdf_converter: PDF to Markdown conversion using pymupdf4llm
- core.content_processor: AWS Config specific content processing
- core.text_processors: Text cleaning and parsing utilities
- core.metadata_generators: Quality scoring and metadata generation

Usage:
    # Use the CLI interface (recommended)
    python -m data_pipeline.processors.compliance_standards.aws_config_guidance.main convert
    
    # Or import specific components
    from data_pipeline.processors.compliance_standards.aws_config_guidance.core import PDFConverter

Architecture Benefits:
- Specialized for AWS Config guidance documents
- PDF to Markdown conversion optimized for LLM/RAG
- Modular design for maintainability
- Ready for integration with compliance pipeline
"""

# Import core components for programmatic access
from .core.pdf_converter import PDFConverter
from .core.content_processor import ContentProcessor
from .core.text_processors import TextProcessor
from .core.metadata_generators import MetadataGenerator

__all__ = [
    'PDFConverter',
    'ContentProcessor', 
    'TextProcessor',
    'MetadataGenerator',
]