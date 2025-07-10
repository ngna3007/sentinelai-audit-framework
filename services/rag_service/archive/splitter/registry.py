"""
Registry system for document splitter implementations.

Provides dynamic registration and retrieval of splitters based on compliance standards.
"""

from typing import Dict, Type, Optional
from .base import BaseSplitter


class SplitterRegistry:
    """Registry for document splitter implementations."""
    
    def __init__(self):
        self._splitters: Dict[str, Type[BaseSplitter]] = {}
    
    def register(self, standard: str, splitter_class: Type[BaseSplitter]) -> None:
        """
        Register a splitter for a compliance standard.
        
        Args:
            standard: The compliance standard name (e.g., 'pci-dss')
            splitter_class: The splitter class to register
        """
        self._splitters[standard.lower()] = splitter_class
    
    def get(self, standard: str) -> Optional[Type[BaseSplitter]]:
        """
        Get a splitter class for a compliance standard.
        
        Args:
            standard: The compliance standard name
            
        Returns:
            The splitter class or None if not found
        """
        return self._splitters.get(standard.lower())
    
    def list_standards(self) -> list[str]:
        """Get list of registered compliance standards."""
        return list(self._splitters.keys())
    
    def create_splitter(
        self, 
        standard: str, 
        max_tokens: int = 350, 
        overlap_tokens: int = 50,
        **kwargs
    ) -> Optional[BaseSplitter]:
        """
        Create a splitter instance for a compliance standard.
        
        Args:
            standard: The compliance standard name
            max_tokens: Maximum tokens per chunk
            overlap_tokens: Overlap tokens between chunks
            **kwargs: Additional arguments passed to splitter constructor
            
        Returns:
            Splitter instance or None if standard not found
        """
        splitter_class = self.get(standard)
        if splitter_class:
            try:
                return splitter_class(max_tokens=max_tokens, overlap_tokens=overlap_tokens, **kwargs)
            except TypeError:
                # Fallback for splitters that don't support additional kwargs
                return splitter_class(max_tokens=max_tokens, overlap_tokens=overlap_tokens)
        return None
    
    def create_enhanced_splitter(
        self, 
        standard: str, 
        max_tokens: int = 350, 
        overlap_tokens: int = 50,
        use_enhanced_extraction: bool = True,
        **kwargs
    ) -> Optional[BaseSplitter]:
        """
        Create a splitter instance with enhanced extraction capabilities.
        
        Args:
            standard: The compliance standard name
            max_tokens: Maximum tokens per chunk
            overlap_tokens: Overlap tokens between chunks
            use_enhanced_extraction: Whether to enable enhanced PDF extraction
            **kwargs: Additional arguments passed to splitter constructor
            
        Returns:
            Enhanced splitter instance or None if standard not found
        """
        return self.create_splitter(
            standard=standard,
            max_tokens=max_tokens,
            overlap_tokens=overlap_tokens,
            use_enhanced_extraction=use_enhanced_extraction,
            **kwargs
        )


# Global registry instance
_registry = SplitterRegistry()


def register_splitter(standard: str, splitter_class: Type[BaseSplitter]) -> None:
    """
    Register a splitter for a compliance standard.
    
    Args:
        standard: The compliance standard name
        splitter_class: The splitter class to register
    """
    _registry.register(standard, splitter_class)


def get_splitter(
    standard: str, 
    max_tokens: int = 350, 
    overlap_tokens: int = 50,
    **kwargs
) -> Optional[BaseSplitter]:
    """
    Get a splitter instance for a compliance standard.
    
    Args:
        standard: The compliance standard name
        max_tokens: Maximum tokens per chunk
        overlap_tokens: Overlap tokens between chunks
        **kwargs: Additional arguments passed to splitter constructor
        
    Returns:
        Splitter instance or None if standard not found
    """
    return _registry.create_splitter(standard, max_tokens, overlap_tokens, **kwargs)


def get_enhanced_splitter(
    standard: str, 
    max_tokens: int = 350, 
    overlap_tokens: int = 50,
    use_enhanced_extraction: bool = True,
    **kwargs
) -> Optional[BaseSplitter]:
    """
    Get an enhanced splitter instance for a compliance standard.
    
    Args:
        standard: The compliance standard name
        max_tokens: Maximum tokens per chunk
        overlap_tokens: Overlap tokens between chunks
        use_enhanced_extraction: Whether to enable enhanced PDF extraction
        **kwargs: Additional arguments passed to splitter constructor
        
    Returns:
        Enhanced splitter instance or None if standard not found
    """
    return _registry.create_enhanced_splitter(
        standard=standard,
        max_tokens=max_tokens,
        overlap_tokens=overlap_tokens,
        use_enhanced_extraction=use_enhanced_extraction,
        **kwargs
    )


def get_splitter_class(standard: str) -> Optional[Type[BaseSplitter]]:
    """
    Get a splitter class for a compliance standard.
    
    Args:
        standard: The compliance standard name
        
    Returns:
        The splitter class or None if not found
    """
    return _registry.get(standard)


def list_supported_standards() -> list[str]:
    """Get list of supported compliance standards."""
    return _registry.list_standards()


# Register default splitters
def _register_default_splitters():
    """Register the default splitter implementations."""
    from .pci_splitter import PCISplitter
    from .iso27001_splitter import ISO27001Splitter
    
    register_splitter('pci-dss', PCISplitter)
    register_splitter('iso27001', ISO27001Splitter)


# Auto-register default splitters when module is imported
_register_default_splitters() 