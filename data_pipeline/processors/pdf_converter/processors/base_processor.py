"""Base class for document-specific processors."""

from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseProcessor(ABC):
    """Abstract base class for document-specific processors."""
    
    @abstractmethod
    def preprocess(self, content: str) -> str:
        """Apply document-specific preprocessing to content.
        
        Args:
            content: Raw markdown content from PDF conversion
            
        Returns:
            Processed markdown content
        """
        pass
    
    @abstractmethod
    def enhance_quality_metrics(self, base_metrics: Dict[str, Any], content: str) -> Dict[str, Any]:
        """Enhance quality metrics with document-specific assessments.
        
        Args:
            base_metrics: Base quality metrics from engine
            content: Processed content
            
        Returns:
            Enhanced quality metrics
        """
        pass
    
    @abstractmethod
    def enhance_metadata(self, base_metadata: Dict[str, Any], content: str) -> Dict[str, Any]:
        """Enhance metadata with document-specific information.
        
        Args:
            base_metadata: Base metadata from engine
            content: Processed content
            
        Returns:
            Enhanced metadata
        """
        pass
    
    @property
    @abstractmethod
    def document_type(self) -> str:
        """Document type identifier."""
        pass
    
    @property
    @abstractmethod
    def processor_name(self) -> str:
        """Processor name."""
        pass