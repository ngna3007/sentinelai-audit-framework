"""
PDF to Markdown Converter

This module provides PDF to Markdown conversion capabilities using pymupdf4llm,
which is specifically designed for LLM and RAG applications. This functionality
was accidentally removed during the modular refactoring and is now restored.

The converter produces high-quality Markdown optimized for:
- Vector search and embeddings
- Table structure preservation  
- Multi-column page handling
- Header detection and formatting
- Token-efficient output for LLM ingestion
"""

from pathlib import Path
from typing import Optional, List, Dict, Any
import logging

try:
    import pymupdf4llm
    PYMUPDF4LLM_AVAILABLE = True
except ImportError:
    PYMUPDF4LLM_AVAILABLE = False
    logging.warning("pymupdf4llm not available. Install with: pip install pymupdf4llm")


class PDFToMarkdownConverter:
    """
    Converts PDF files to Markdown format using pymupdf4llm.
    
    This converter is specifically optimized for LLM and RAG applications,
    producing structured Markdown that preserves document layout and
    content relationships.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        if not PYMUPDF4LLM_AVAILABLE:
            raise ImportError(
                "pymupdf4llm is required for PDF to Markdown conversion. "
                "Install with: pip install pymupdf4llm"
            )
    
    def convert_pdf_to_markdown(
        self, 
        pdf_path: str | Path, 
        output_path: Optional[str | Path] = None,
        pages: Optional[List[int]] = None,
        **kwargs
    ) -> str:
        """
        Convert PDF to Markdown format optimized for LLM applications.
        
        Args:
            pdf_path: Path to input PDF file
            output_path: Optional path to save markdown file
            pages: Optional list of 0-based page numbers to process
            **kwargs: Additional arguments for pymupdf4llm.to_markdown()
            
        Returns:
            Markdown content as string
            
        Raises:
            FileNotFoundError: If PDF file doesn't exist
            Exception: If conversion fails
        """
        pdf_path = Path(pdf_path)
        
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        self.logger.info(f"Converting PDF to Markdown: {pdf_path}")
        
        try:
            # Convert PDF to Markdown using pymupdf4llm
            md_content = pymupdf4llm.to_markdown(
                str(pdf_path),
                pages=pages,
                **kwargs
            )
            
            self.logger.info(f"✅ Conversion completed: {len(md_content):,} characters")
            
            # Save to file if output path specified
            if output_path:
                output_path = Path(output_path)
                output_path.parent.mkdir(parents=True, exist_ok=True)
                
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(md_content)
                
                self.logger.info(f"💾 Saved markdown to: {output_path}")
            
            return md_content
            
        except Exception as e:
            self.logger.error(f"❌ PDF conversion failed: {str(e)}")
            raise
    
    def convert_with_metadata(
        self, 
        pdf_path: str | Path,
        output_path: Optional[str | Path] = None,
        pages: Optional[List[int]] = None
    ) -> Dict[str, Any]:
        """
        Convert PDF to Markdown with additional metadata extraction.
        
        Args:
            pdf_path: Path to input PDF file  
            output_path: Optional path to save markdown file
            pages: Optional list of 0-based page numbers to process
            
        Returns:
            Dictionary containing markdown content and metadata
        """
        pdf_path = Path(pdf_path)
        
        self.logger.info(f"Converting PDF with metadata extraction: {pdf_path}")
        
        try:
            # Get basic markdown content
            md_content = self.convert_pdf_to_markdown(pdf_path, pages=pages)
            
            # Extract additional metadata
            metadata = {
                'source_file': str(pdf_path),
                'source_format': 'PDF',
                'conversion_tool': 'pymupdf4llm',
                'total_characters': len(md_content),
                'total_lines': len(md_content.split('\n')),
                'pages_processed': pages if pages else 'all',
                'optimized_for': 'LLM/RAG applications'
            }
            
            result = {
                'content': md_content,
                'metadata': metadata
            }
            
            # Save with metadata if output path specified
            if output_path:
                output_path = Path(output_path)
                
                # Save markdown content
                md_file = output_path.with_suffix('.md')
                with open(md_file, 'w', encoding='utf-8') as f:
                    f.write(md_content)
                
                # Save metadata  
                import json
                metadata_file = output_path.with_suffix('.json')
                with open(metadata_file, 'w', encoding='utf-8') as f:
                    json.dump(metadata, f, indent=2)
                
                self.logger.info(f"💾 Saved markdown to: {md_file}")
                self.logger.info(f"💾 Saved metadata to: {metadata_file}")
            
            return result
            
        except Exception as e:
            self.logger.error(f"❌ PDF conversion with metadata failed: {str(e)}")
            raise
    
    def validate_conversion_quality(self, md_content: str) -> Dict[str, Any]:
        """
        Validate the quality of the markdown conversion.
        
        Args:
            md_content: Markdown content to validate
            
        Returns:
            Quality metrics dictionary
        """
        lines = md_content.split('\n')
        
        # Count different markdown elements
        headers = len([line for line in lines if line.strip().startswith('#')])
        tables = md_content.count('|')  # Rough table indicator
        bold_text = md_content.count('**')
        italic_text = md_content.count('*') - bold_text  # Subtract bold markers
        code_blocks = md_content.count('```')
        
        quality_metrics = {
            'total_lines': len(lines),
            'non_empty_lines': len([line for line in lines if line.strip()]),
            'headers_detected': headers,
            'table_markers': tables,
            'bold_formatting': bold_text // 2,  # Pairs of **
            'italic_formatting': italic_text // 2,  # Pairs of *
            'code_blocks': code_blocks // 2,  # Pairs of ```
            'estimated_quality': 'good' if headers > 0 and len(lines) > 100 else 'needs_review'
        }
        
        return quality_metrics
    
    @staticmethod
    def is_available() -> bool:
        """Check if pymupdf4llm is available."""
        return PYMUPDF4LLM_AVAILABLE


def convert_pdf_to_markdown(
    pdf_path: str | Path, 
    output_path: Optional[str | Path] = None,
    pages: Optional[List[int]] = None,
    **kwargs
) -> str:
    """
    Convenience function for PDF to Markdown conversion.
    
    Args:
        pdf_path: Path to input PDF file
        output_path: Optional path to save markdown file
        pages: Optional list of 0-based page numbers to process
        **kwargs: Additional arguments for pymupdf4llm.to_markdown()
        
    Returns:
        Markdown content as string
    """
    converter = PDFToMarkdownConverter()
    return converter.convert_pdf_to_markdown(pdf_path, output_path, pages, **kwargs) 