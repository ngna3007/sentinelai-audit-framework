"""PyMuPDF4LLM engine for fast PDF conversion."""

from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from logging import getLogger

from .base_engine import BaseEngine

logger = getLogger(__name__)

# Check if pymupdf4llm is available
try:
    from pymupdf4llm import to_markdown
    PYMUPDF4LLM_AVAILABLE = True
except ImportError:
    PYMUPDF4LLM_AVAILABLE = False
    logger.warning("📚 PyMuPDF4LLM not available. Install with: pip install pymupdf4llm")


class PyMuPDF4LLMEngine(BaseEngine):
    """Fast PDF conversion engine using PyMuPDF4LLM."""
    
    def convert(
        self, 
        pdf_path: Union[str, Path], 
        pages: Optional[List[int]] = None,
        **kwargs
    ) -> str:
        """Convert PDF to markdown using PyMuPDF4LLM.
        
        Args:
            pdf_path: Path to PDF file
            pages: Optional list of page numbers to convert
            **kwargs: PyMuPDF4LLM-specific options
            
        Returns:
            Markdown content as string
        """
        if not self.is_available():
            raise ImportError("PyMuPDF4LLM is not available. Install with: pip install pymupdf4llm")
        
        pdf_path = Path(pdf_path)
        if not pdf_path.exists():
            raise FileNotFoundError(f"📄 PDF file not found: {pdf_path}")
        
        logger.info(f"🔄 Converting PDF using PyMuPDF4LLM: {pdf_path.name}")
        
        try:
            # Convert with optional page selection
            md_content = to_markdown(str(pdf_path), pages=pages, **kwargs)
            logger.info(f"✅ Successfully converted {pdf_path.name} to markdown")
            return md_content
            
        except Exception as e:
            logger.error(f"❌ Failed to convert {pdf_path.name}: {e}")
            raise
    
    def validate_quality(self, content: str) -> Dict[str, Any]:
        """Validate conversion quality for PyMuPDF4LLM output.
        
        Args:
            content: Converted markdown content
            
        Returns:
            Quality metrics dictionary
        """
        lines = content.split('\n')
        non_empty_lines = [line for line in lines if line.strip()]
        headers = [line for line in lines if line.strip().startswith('#')]
        tables = content.count('|')  # Rough table indicator
        
        # Basic quality assessment
        quality_score = 'excellent' if (len(headers) >= 10 and len(non_empty_lines) >= 200) else \
                       'good' if (len(headers) >= 5 and len(non_empty_lines) >= 100) else \
                       'acceptable' if (len(headers) >= 2 and len(non_empty_lines) >= 50) else \
                       'needs_review'
        
        return {
            'total_lines': len(lines),
            'non_empty_lines': len(non_empty_lines),
            'headers_detected': len(headers),
            'table_markers': tables,
            'total_characters': len(content),
            'quality_assessment': quality_score,
            'engine': self.name
        }
    
    def generate_metadata(
        self, 
        pdf_path: Union[str, Path], 
        content: str,
        pages: Optional[List[int]] = None
    ) -> Dict[str, Any]:
        """Generate metadata for PyMuPDF4LLM conversion.
        
        Args:
            pdf_path: Source PDF path
            content: Converted content
            pages: Pages that were converted
            
        Returns:
            Metadata dictionary
        """
        quality_metrics = self.validate_quality(content)
        
        return {
            'source_file': str(pdf_path),
            'source_format': 'PDF',
            'conversion_engine': self.name,
            'pages_processed': pages if pages else 'all',
            'total_characters': len(content),
            'total_lines': len(content.split('\n')),
            'features': [
                'fast_conversion',
                'llm_optimized',
                'page_selection'
            ],
            'quality_metrics': quality_metrics
        }
    
    @classmethod
    def is_available(cls) -> bool:
        """Check if PyMuPDF4LLM is available."""
        return PYMUPDF4LLM_AVAILABLE
    
    @property
    def name(self) -> str:
        """Engine name."""
        return 'pymupdf4llm'
    
    @property
    def supports_page_selection(self) -> bool:
        """PyMuPDF4LLM supports page selection."""
        return True