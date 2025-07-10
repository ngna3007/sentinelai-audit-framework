"""
Base classes for document splitting and chunk representation.
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime


class Chunk(BaseModel):
    """Represents a document chunk with metadata."""
    
    id: str = Field(description="Unique identifier for the chunk")
    content: str = Field(description="The actual text content")
    token_count: int = Field(description="Number of tokens in the content")
    
    # Source metadata
    source_document: str = Field(description="Original document filename")
    page_number: Optional[int] = Field(None, description="Page number if applicable")
    section: Optional[str] = Field(None, description="Document section or heading")
    
    # Compliance-specific metadata
    control_id: Optional[str] = Field(None, description="Control ID (e.g., PCI-DSS 1.1.1)")
    standard: str = Field(description="Compliance standard (e.g., pci-dss)")
    
    # Processing metadata
    chunk_index: int = Field(description="Sequential index within document")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Additional metadata
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class BaseSplitter(ABC):
    """Abstract base class for document splitters."""
    
    def __init__(self, max_tokens: int = 350, overlap_tokens: int = 50):
        self.max_tokens = max_tokens
        self.overlap_tokens = overlap_tokens
    
    @abstractmethod
    def split_document(
        self, 
        content: str, 
        source_document: str, 
        **kwargs
    ) -> List[Chunk]:
        """
        Split a document into chunks.
        
        Args:
            content: The document text content
            source_document: The source document filename
            **kwargs: Additional arguments specific to the splitter
            
        Returns:
            List of Chunk objects
        """
        pass
    
    @abstractmethod
    def get_standard_name(self) -> str:
        """Return the name of the compliance standard this splitter handles."""
        pass
    
    def _count_tokens(self, text: str) -> int:
        """Count tokens in text. Override for specific tokenizer."""
        # Simple approximation: ~4 characters per token
        return len(text) // 4
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text content."""
        import re
        
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove common PDF artifacts
        text = re.sub(r'[^\x00-\x7F]+', ' ', text)  # Remove non-ASCII
        text = re.sub(r'\f', ' ', text)  # Remove form feeds
        
        return text.strip()
    
    def _extract_metadata(self, content: str, **kwargs) -> Dict[str, Any]:
        """Extract additional metadata from content. Override in subclasses."""
        return {} 