"""
PDF to Markdown Converter for AWS Config Guidance Documents

This module provides specialized PDF to Markdown conversion for AWS Config guidance 
documents using pymupdf4llm, optimized for LLM and RAG applications.

The converter produces high-quality Markdown optimized for:
- AWS Config rule mapping
- Compliance guidance extraction
- Vector search and embeddings
- Table structure preservation
- Multi-column page handling
"""

from pathlib import Path
from typing import Optional, List, Dict, Any
import logging
import time

try:
    import pymupdf4llm
    PYMUPDF4LLM_AVAILABLE = True
except ImportError:
    PYMUPDF4LLM_AVAILABLE = False
    logging.warning("pymupdf4llm not available. Install with: pip install pymupdf4llm")


class PDFConverter:
    """
    Converts AWS Config Guidance PDF files to Markdown format.
    
    This converter is specifically optimized for AWS Config guidance documents,
    producing structured Markdown that preserves AWS Config rule references,
    compliance mappings, and implementation guidance.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        if not PYMUPDF4LLM_AVAILABLE:
            raise ImportError(
                "pymupdf4llm is required for PDF to Markdown conversion. "
                "Install with: pip install pymupdf4llm"
            )
    
    def convert_to_markdown(
        self, 
        pdf_path: str | Path, 
        output_path: Optional[str | Path] = None,
        pages: Optional[List[int]] = None,
        **kwargs
    ) -> str:
        """
        Convert AWS Config Guidance PDF to Markdown format.
        
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
        
        self.logger.info(f"Converting AWS Config Guidance PDF to Markdown: {pdf_path}")
        start_time = time.time()
        
        try:
            # Convert PDF to Markdown using pymupdf4llm with AWS Config optimizations
            md_content = pymupdf4llm.to_markdown(
                str(pdf_path),
                pages=pages,
                # Optimize for AWS Config guidance content
                write_images=False,  # Focus on text content
                image_path=None,     # No image extraction needed
                **kwargs
            )
            
            processing_time = time.time() - start_time
            self.logger.info(f"✅ Conversion completed: {len(md_content):,} characters in {processing_time:.2f}s")
            
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
    
    def convert_with_preprocessing(
        self, 
        pdf_path: str | Path,
        output_path: Optional[str | Path] = None,
        pages: Optional[List[int]] = None
    ) -> Dict[str, Any]:
        """
        Convert PDF to Markdown with AWS Config specific preprocessing.
        
        Args:
            pdf_path: Path to input PDF file  
            output_path: Optional path to save markdown file
            pages: Optional list of 0-based page numbers to process
            
        Returns:
            Dictionary containing markdown content and metadata
        """
        pdf_path = Path(pdf_path)
        
        self.logger.info(f"Converting AWS Config Guidance PDF with preprocessing: {pdf_path}")
        
        try:
            # Get basic markdown content
            md_content = self.convert_to_markdown(pdf_path, pages=pages)
            
            # Apply AWS Config specific preprocessing
            processed_content = self._preprocess_aws_config_content(md_content)
            
            # Extract metadata
            metadata = {
                'source_file': str(pdf_path),
                'source_format': 'PDF',
                'document_type': 'AWS Config Guidance',
                'conversion_tool': 'pymupdf4llm',
                'processor': 'aws_guidance',
                'total_characters': len(processed_content),
                'total_lines': len(processed_content.split('\n')),
                'pages_processed': pages if pages else 'all',
                'optimized_for': 'AWS Config rule mapping and compliance guidance',
                'processing_features': [
                    'config_rule_detection',
                    'compliance_mapping',
                    'implementation_guidance'
                ]
            }
            
            result = {
                'content': processed_content,
                'original_content': md_content,
                'metadata': metadata
            }
            
            # Save processed content if output path specified
            if output_path:
                output_path = Path(output_path)
                
                # Save processed markdown content
                md_file = output_path.with_suffix('.md')
                with open(md_file, 'w', encoding='utf-8') as f:
                    f.write(processed_content)
                
                # Save metadata  
                import json
                metadata_file = output_path.with_suffix('.json')
                with open(metadata_file, 'w', encoding='utf-8') as f:
                    json.dump(metadata, f, indent=2)
                
                self.logger.info(f"💾 Saved processed markdown to: {md_file}")
                self.logger.info(f"💾 Saved metadata to: {metadata_file}")
            
            return result
            
        except Exception as e:
            self.logger.error(f"❌ AWS Config PDF conversion with preprocessing failed: {str(e)}")
            raise
    
    def _preprocess_aws_config_content(self, md_content: str) -> str:
        """
        Apply AWS Config specific preprocessing to markdown content.
        
        Args:
            md_content: Raw markdown content from PDF conversion
            
        Returns:
            Preprocessed markdown content optimized for AWS Config guidance
        """
        import re
        
        # Basic preprocessing for AWS Config guidance
        lines = md_content.split('\n')
        processed_lines = []
        
        for line in lines:
            # Clean up common PDF conversion artifacts
            line = line.strip()
            
            # Skip empty lines and page numbers
            if not line or line.isdigit():
                continue
                
            # Fix hyphenated words split across lines
            if line.endswith('-'):
                line = line[:-1]  # Remove trailing hyphen
                
            # Enhance AWS Config rule references
            if 'config rule' in line.lower() or 'aws config' in line.lower():
                line = f"**{line}**"  # Emphasize Config rule references
                
            # Standardize AWS service names
            line = re.sub(r'AWS\s+Config', 'AWS Config', line, flags=re.IGNORECASE)
            line = re.sub(r'PCI\s+DSS', 'PCI DSS', line, flags=re.IGNORECASE)
            
            processed_lines.append(line)
        
        return '\n'.join(processed_lines)
    
    def validate_conversion_quality(self, md_content: str) -> Dict[str, Any]:
        """
        Validate the quality of the AWS Config guidance markdown conversion.
        
        Args:
            md_content: Markdown content to validate
            
        Returns:
            Quality metrics dictionary specific to AWS Config guidance
        """
        lines = md_content.split('\n')
        
        # Count AWS Config specific elements
        config_references = len([line for line in lines if 'config' in line.lower()])
        aws_references = len([line for line in lines if 'aws' in line.lower()])
        compliance_references = len([line for line in lines if 'compliance' in line.lower() or 'compliant' in line.lower()])
        rule_references = len([line for line in lines if 'rule' in line.lower()])
        
        # Count general markdown elements
        headers = len([line for line in lines if line.strip().startswith('#')])
        tables = md_content.count('|')  # Rough table indicator
        bold_text = md_content.count('**')
        
        quality_metrics = {
            'total_lines': len(lines),
            'non_empty_lines': len([line for line in lines if line.strip()]),
            'headers_detected': headers,
            'table_markers': tables,
            'bold_formatting': bold_text // 2,
            'config_references': config_references,
            'aws_references': aws_references,
            'compliance_references': compliance_references,
            'rule_references': rule_references,
            'estimated_quality': self._assess_quality(headers, config_references, aws_references),
            'document_focus': 'aws_config_guidance'
        }
        
        return quality_metrics
    
    def _assess_quality(self, headers: int, config_refs: int, aws_refs: int) -> str:
        """Assess the quality of the conversion based on AWS Config guidance criteria."""
        if headers > 10 and config_refs > 5 and aws_refs > 10:
            return 'excellent'
        elif headers > 5 and config_refs > 2 and aws_refs > 5:
            return 'good'
        elif headers > 0 and (config_refs > 0 or aws_refs > 0):
            return 'acceptable'
        else:
            return 'needs_review'
    
    @staticmethod
    def is_available() -> bool:
        """Check if the PDF converter is available."""
        return PYMUPDF4LLM_AVAILABLE


def convert_pdf_to_markdown(
    pdf_path: str | Path, 
    output_path: Optional[str | Path] = None,
    pages: Optional[List[int]] = None,
    **kwargs
) -> str:
    """
    Convenience function for AWS Config Guidance PDF to Markdown conversion.
    
    Args:
        pdf_path: Path to input PDF file
        output_path: Optional path to save markdown file
        pages: Optional list of 0-based page numbers to process
        **kwargs: Additional arguments for pymupdf4llm.to_markdown()
        
    Returns:
        Markdown content as string
    """
    converter = PDFConverter()
    return converter.convert_to_markdown(pdf_path, output_path, pages, **kwargs) 