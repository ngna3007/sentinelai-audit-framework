"""
Document splitter implementations for different compliance standards.

This module provides a strategy pattern for document-specific chunking
with a registry system for dynamic splitter selection.
"""

from .base import BaseSplitter, Chunk
from .registry import SplitterRegistry, register_splitter, get_splitter, get_enhanced_splitter
from .pci_splitter import PCISplitter
from .iso27001_splitter import ISO27001Splitter

__all__ = [
    "BaseSplitter",
    "Chunk", 
    "SplitterRegistry",
    "register_splitter",
    "get_splitter",
    "get_enhanced_splitter",
    "PCISplitter",
    "ISO27001Splitter",
] 