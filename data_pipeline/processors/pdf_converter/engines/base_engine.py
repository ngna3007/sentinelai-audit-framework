"""Base class for PDF conversion engines."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, List, Optional, Union


class BaseEngine(ABC):
    """Abstract base class for PDF conversion engines."""
    
    @abstractmethod
    def convert(
        self, 
        pdf_path: Union[str, Path], 
        pages: Optional[List[int]] = None,
        **kwargs
    ) -> str:
        """Convert PDF to markdown.
        
        Args:
            pdf_path: Path to PDF file
            pages: Optional list of page numbers to convert
            **kwargs: Engine-specific options
            
        Returns:
            Markdown content as string
        """
        pass
    
    @abstractmethod
    def validate_quality(self, content: str) -> Dict[str, Any]:
        """Validate conversion quality.
        
        Args:
            content: Converted markdown content
            
        Returns:
            Quality metrics dictionary
        """
        pass
    
    @abstractmethod
    def generate_metadata(
        self, 
        pdf_path: Union[str, Path], 
        content: str,
        pages: Optional[List[int]] = None
    ) -> Dict[str, Any]:
        """Generate conversion metadata.
        
        Args:
            pdf_path: Source PDF path
            content: Converted content
            pages: Pages that were converted
            
        Returns:
            Metadata dictionary
        """
        pass
    
    @classmethod
    @abstractmethod
    def is_available(cls) -> bool:
        """Check if engine is available."""
        pass
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Engine name."""
        pass
    
    @property
    @abstractmethod
    def supports_page_selection(self) -> bool:
        """Whether engine supports page selection."""
        pass