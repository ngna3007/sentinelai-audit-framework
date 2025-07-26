"""Generic processor for standard PDF conversion."""

from typing import Any, Dict

from .base_processor import BaseProcessor


class GenericProcessor(BaseProcessor):
    """Generic processor for standard PDF documents."""
    
    def preprocess(self, content: str) -> str:
        """Apply basic preprocessing to markdown content.
        
        Args:
            content: Raw markdown content from PDF conversion
            
        Returns:
            Processed markdown content with basic cleanup
        """
        lines = content.split('\n')
        processed_lines = []
        
        for line in lines:
            # Clean up common PDF conversion artifacts
            line = line.strip()
            
            # Skip empty lines and standalone page numbers
            if not line or (line.isdigit() and len(line) <= 3):
                continue
            
            # Basic cleanup for generic documents
            processed_lines.append(line)
        
        return '\n'.join(processed_lines)
    
    def enhance_quality_metrics(self, base_metrics: Dict[str, Any], content: str) -> Dict[str, Any]:
        """Enhance quality metrics with generic assessments.
        
        Args:
            base_metrics: Base quality metrics from engine
            content: Processed content
            
        Returns:
            Enhanced quality metrics with generic indicators
        """
        # For generic documents, just add processor info
        enhanced_metrics = {
            **base_metrics,
            'document_focus': 'generic',
            'processor': self.processor_name
        }
        
        return enhanced_metrics
    
    def enhance_metadata(self, base_metadata: Dict[str, Any], content: str) -> Dict[str, Any]:
        """Enhance metadata with generic information.
        
        Args:
            base_metadata: Base metadata from engine
            content: Processed content
            
        Returns:
            Enhanced metadata with generic details
        """
        enhanced_metadata = {
            **base_metadata,
            'document_type': self.document_type,
            'processor': self.processor_name,
            'optimized_for': 'General document processing and text extraction',
            'processing_features': [
                'basic_cleanup',
                'page_number_removal',
                'whitespace_normalization'
            ]
        }
        
        return enhanced_metadata
    
    @property
    def document_type(self) -> str:
        """Document type identifier."""
        return 'Generic Document'
    
    @property
    def processor_name(self) -> str:
        """Processor name."""
        return 'generic'