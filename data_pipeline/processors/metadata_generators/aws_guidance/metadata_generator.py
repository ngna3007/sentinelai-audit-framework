"""
Metadata Generators for AWS Config Guidance Processing

Minimal metadata generation for PDF conversion.
"""

from pathlib import Path
from typing import Dict, Any
from json import dump
from time import strftime
from logging import getLogger


class MetadataGenerator:
    """
    Generates basic metadata for AWS Config guidance processing.
    """
    
    def __init__(self):
        self.logger = getLogger(__name__)
    
    def generate_conversion_metadata(self, source_file: str, result: Dict[str, Any]) -> Dict[str, Any]:
        """Generate metadata for PDF conversion."""
        return {
            'source_file': source_file,
            'conversion_tool': 'pymupdf4llm',
            'timestamp': strftime('%Y-%m-%d %H:%M:%S'),
            'content_length': len(result.get('content', '')),
            'processing_time': result.get('processing_time', 0)
        }