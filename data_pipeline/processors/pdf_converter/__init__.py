"""Universal PDF converter with multiple engines and document-specific processing.

This module provides a unified interface for PDF to markdown conversion with:
- Multiple conversion engines (PyMuPDF4LLM, Docling)
- Automatic engine fallback
- Document-specific processors (AWS, PCI DSS, Generic)
- Comprehensive quality metrics and metadata

Usage:
    from processors.pdf_converter import UniversalPDFConverter, convert_pdf_to_markdown
    
    # Simple conversion
    content = convert_pdf_to_markdown('document.pdf')
    
    # Advanced conversion with metadata
    converter = UniversalPDFConverter(processor_type='pci')
    result = converter.convert_with_metadata('pci_dss.pdf')
"""

from typing import List

from .universal_converter import UniversalPDFConverter, convert_pdf_to_markdown
from .engines import PyMuPDF4LLMEngine, DoclingEngine, BaseEngine
from .processors import AWSProcessor, PCIProcessor, GenericProcessor, BaseProcessor

# Main exports for external use
__all__ = [
    'UniversalPDFConverter',
    'convert_pdf_to_markdown',
    'PyMuPDF4LLMEngine',
    'DoclingEngine', 
    'BaseEngine',
    'AWSProcessor',
    'PCIProcessor',
    'GenericProcessor',
    'BaseProcessor'
]

# Version and availability info
__version__ = '1.0.0'

def is_available() -> bool:
    """Check if any PDF conversion engines are available."""
    return UniversalPDFConverter.is_available()

def list_available_engines() -> List[str]:
    """List available conversion engines."""
    converter = UniversalPDFConverter()
    return converter.list_available_engines()

def list_available_processors() -> List[str]:
    """List available document processors."""
    converter = UniversalPDFConverter()
    return converter.list_available_processors()