"""
General Text Processing Utilities

This module contains general-purpose utilities for:
- Text cleaning and normalization
- Markdown preprocessing for chunking
- Whitespace and artifact removal
- Content structure preservation

These utilities can be used across different document types and frameworks.
"""

import re
from typing import Optional


class GeneralTextProcessor:
    """General-purpose utilities for cleaning and processing text content."""
    
    @staticmethod
    def clean_text(text: str) -> str:
        """Clean text by removing HTML and excessive markup while preserving structure."""
        if not text:
            return ""
        
        # Replace HTML breaks with spaces
        text = text.replace('<br>', ' ').replace('<br/>', ' ')
        
        # Clean up excessive whitespace
        text = ' '.join(text.split())
        
        # Remove bullet point markup but keep the structure
        text = text.replace('• ', '')
        
        return text.strip()
    
    @staticmethod
    def preprocess_markdown_for_chunking(text: str) -> str:
        """
        Preprocess markdown content before chunking to improve token counting accuracy.
        
        This method:
        - Removes excessive whitespace and newlines
        - Cleans up conversion artifacts (e.g., from docling, pandoc)
        - Normalizes spacing around headers and sections
        - Removes empty lines
        - Preserves document structure for semantic chunking
        
        Args:
            text: Raw markdown content
            
        Returns:
            Cleaned markdown content ready for chunking
        """
        if not text:
            return ""
        
        # Split into lines for processing
        lines = text.split('\n')
        processed_lines = []
        
        for line in lines:
            # Remove leading/trailing whitespace
            line = line.strip()
            
            # Skip empty lines
            if not line:
                continue
                
            # Remove common conversion artifacts
            if '<!-- image -->' in line:
                continue
            if line.startswith('<!--') and line.endswith('-->'):
                continue
            if line.startswith('<!-- '):
                continue
                
            # Remove docling/pandoc specific artifacts
            if line.startswith('!['):  # Image references
                continue
            if line.strip() == '---':  # Horizontal rules (unless truly needed)
                continue
                
            # Clean up excessive spacing within lines
            line = ' '.join(line.split())
            
            # Normalize markdown headers (ensure single space after #)
            if line.startswith('#'):
                # Count leading hashes
                hash_count = 0
                for char in line:
                    if char == '#':
                        hash_count += 1
                    else:
                        break
                # Rebuild header with proper spacing
                header_text = line[hash_count:].strip()
                if header_text:
                    line = '#' * hash_count + ' ' + header_text
            
            # Clean up table formatting (normalize spacing)
            if line.startswith('|') and line.endswith('|'):
                # Split by pipe, clean each cell, rejoin
                cells = [cell.strip() for cell in line.split('|')]
                if len(cells) > 2:  # Valid table row
                    line = '| ' + ' | '.join(cells[1:-1]) + ' |'
            
            # Add cleaned line
            processed_lines.append(line)
        
        # Join lines with single newlines
        cleaned_text = '\n'.join(processed_lines)
        
        # Final cleanup: remove multiple consecutive newlines
        cleaned_text = re.sub(r'\n{3,}', '\n\n', cleaned_text)
        
        # Remove any remaining excessive whitespace
        cleaned_text = re.sub(r'[ \t]+', ' ', cleaned_text)
        
        return cleaned_text.strip()
    
    @staticmethod
    def normalize_whitespace(text: str) -> str:
        """Normalize whitespace in text while preserving line breaks."""
        if not text:
            return ""
        
        # Replace multiple spaces with single space
        text = re.sub(r'[ \t]+', ' ', text)
        
        # Replace multiple newlines with double newline (paragraph break)
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        return text.strip()
    
    @staticmethod
    def remove_conversion_artifacts(text: str, converter_type: str = "auto") -> str:
        """
        Remove specific artifacts from document conversion tools.
        
        Args:
            text: Input text with artifacts
            converter_type: Type of converter ("docling", "pandoc", "auto")
            
        Returns:
            Text with conversion artifacts removed
        """
        if not text:
            return ""
        
        lines = text.split('\n')
        cleaned_lines = []
        
        for line in lines:
            line = line.strip()
            
            # Common artifacts from various converters
            if not line:
                continue
                
            # Docling artifacts
            if converter_type in ["docling", "auto"]:
                if '<!-- image -->' in line:
                    continue
                if line.startswith('<!-- ') and line.endswith(' -->'):
                    continue
            
            # Pandoc artifacts  
            if converter_type in ["pandoc", "auto"]:
                if line.startswith(':::'):  # Pandoc divs
                    continue
                if line == '{.unnumbered}':
                    continue
            
            cleaned_lines.append(line)
        
        return '\n'.join(cleaned_lines)