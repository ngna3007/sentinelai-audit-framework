"""
Metadata Generators for AWS Config Guidance Processing

Minimal metadata generation for PDF conversion.
"""

from pathlib import Path
from typing import Dict, Any
import json
import time
import logging


class MetadataGenerator:
    """
    Generates basic metadata for AWS Config guidance processing.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def generate_conversion_metadata(self, source_file: str, result: Dict[str, Any]) -> Dict[str, Any]:
        """Generate metadata for PDF conversion."""
        return {
            'source_file': source_file,
            'conversion_tool': 'pymupdf4llm',
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'content_length': len(result.get('content', '')),
            'processing_time': result.get('processing_time', 0)
        } 