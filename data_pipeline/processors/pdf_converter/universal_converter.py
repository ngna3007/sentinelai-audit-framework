"""Universal PDF converter with multiple engines and document processors."""

from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from logging import getLogger

from .engines import PyMuPDF4LLMEngine, DoclingEngine, DoclingVLMEngine, BaseEngine
from .processors import AWSProcessor, PCIProcessor, GenericProcessor, BaseProcessor

logger = getLogger(__name__)


class UniversalPDFConverter:
    """Universal PDF converter with engine fallback and document-specific processing."""
    
    def __init__(
        self, 
        primary_engine: str = 'pymupdf4llm',
        fallback_engine: str = 'docling',
        processor_type: str = 'auto'
    ):
        """Initialize universal converter.
        
        Args:
            primary_engine: Primary engine to use ('pymupdf4llm', 'docling', or 'docling_vlm')
            fallback_engine: Fallback engine if primary fails
            processor_type: Document processor ('auto', 'aws', 'pci', 'generic')
        """
        self.primary_engine_name = primary_engine
        self.fallback_engine_name = fallback_engine
        self.processor_type = processor_type
        
        # Initialize engines
        self.engines = self._initialize_engines()
        
        # Initialize processors
        self.processors = {
            'aws': AWSProcessor(),
            'pci': PCIProcessor(),
            'generic': GenericProcessor()
        }
    
    def _initialize_engines(self) -> Dict[str, BaseEngine]:
        """Initialize available engines."""
        engines = {}
        
        # Initialize PyMuPDF4LLM engine
        if PyMuPDF4LLMEngine.is_available():
            engines['pymupdf4llm'] = PyMuPDF4LLMEngine()
            logger.info("✅ PyMuPDF4LLM engine available")
        else:
            logger.warning("⚠️ PyMuPDF4LLM engine not available")
        
        # Initialize Docling engine
        if DoclingEngine.is_available():
            try:
                engines['docling'] = DoclingEngine()
                logger.info("✅ Docling engine available")
            except Exception as e:
                logger.warning(f"⚠️ Failed to initialize Docling engine: {e}")
        else:
            logger.warning("⚠️ Docling engine not available")
        
        # Initialize Docling VLM engine
        if DoclingVLMEngine.is_available():
            try:
                engines['docling_vlm'] = DoclingVLMEngine()
                logger.info("✅ Docling VLM engine available")
            except Exception as e:
                logger.warning(f"⚠️ Failed to initialize Docling VLM engine: {e}")
        else:
            logger.warning("⚠️ Docling VLM engine not available")
        
        if not engines:
            raise RuntimeError("No PDF conversion engines available. Install pymupdf4llm or docling.")
        
        return engines
    
    def _detect_document_type(self, pdf_path: Union[str, Path]) -> str:
        """Auto-detect document type from filename.
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            Detected processor type ('aws', 'pci', 'generic')
        """
        filename = Path(pdf_path).name.lower()
        
        if 'aws' in filename or 'config' in filename:
            return 'aws'
        elif 'pci' in filename or 'dss' in filename:
            return 'pci'
        else:
            return 'generic'
    
    def _get_processor(self, processor_type: str = None) -> BaseProcessor:
        """Get appropriate processor.
        
        Args:
            processor_type: Specific processor type or None for auto-detection
            
        Returns:
            Document processor instance
        """
        if processor_type is None:
            processor_type = self.processor_type
        
        if processor_type == 'auto':
            # Auto-detection would need the PDF path, default to generic
            processor_type = 'generic'
        
        return self.processors.get(processor_type, self.processors['generic'])
    
    def _get_engine(self, engine_name: str) -> Optional[BaseEngine]:
        """Get engine by name.
        
        Args:
            engine_name: Engine name
            
        Returns:
            Engine instance or None if not available
        """
        return self.engines.get(engine_name)
    
    def convert_pdf_to_markdown(
        self,
        pdf_path: Union[str, Path],
        output_path: Optional[Union[str, Path]] = None,
        pages: Optional[List[int]] = None,
        processor_type: Optional[str] = None,
        engine: Optional[str] = None,
        **kwargs
    ) -> str:
        """Convert PDF to markdown with processing.
        
        Args:
            pdf_path: Path to PDF file
            output_path: Optional output file path
            pages: Optional list of page numbers
            processor_type: Document processor type ('auto', 'aws', 'pci', 'generic')
            engine: Specific engine to use
            **kwargs: Engine-specific options
            
        Returns:
            Processed markdown content
        """
        pdf_path = Path(pdf_path)
        
        # Auto-detect processor if needed
        if processor_type == 'auto' or (processor_type is None and self.processor_type == 'auto'):
            processor_type = self._detect_document_type(pdf_path)
        
        processor = self._get_processor(processor_type)
        logger.info(f"📋 Using processor: {processor.processor_name}")
        
        # Determine engine to use
        engine_name = engine or self.primary_engine_name
        selected_engine = self._get_engine(engine_name)
        
        if not selected_engine:
            # Try fallback engine
            logger.warning(f"⚠️ Primary engine '{engine_name}' not available, trying fallback")
            engine_name = self.fallback_engine_name
            selected_engine = self._get_engine(engine_name)
            
            if not selected_engine:
                raise RuntimeError(f"No engines available. Tried: {self.primary_engine_name}, {self.fallback_engine_name}")
        
        logger.info(f"🔧 Using engine: {selected_engine.name}")
        
        try:
            # Convert using selected engine
            raw_content = selected_engine.convert(pdf_path, pages=pages, **kwargs)
            
            # Apply document-specific processing
            processed_content = processor.preprocess(raw_content)
            
            # Save to file if output path provided
            if output_path:
                output_path = Path(output_path)
                output_path.parent.mkdir(parents=True, exist_ok=True)
                output_path.write_text(processed_content, encoding='utf-8')
                logger.info(f"💾 Saved processed markdown to: {output_path}")
            
            return processed_content
            
        except Exception as e:
            # Try fallback engine if primary failed and we haven't already
            if engine is None and engine_name == self.primary_engine_name:
                logger.warning(f"⚠️ Primary engine failed: {e}. Trying fallback engine.")
                return self.convert_pdf_to_markdown(
                    pdf_path, output_path, pages, processor_type, 
                    self.fallback_engine_name, **kwargs
                )
            else:
                raise
    
    def convert_with_metadata(
        self,
        pdf_path: Union[str, Path],
        output_path: Optional[Union[str, Path]] = None,
        pages: Optional[List[int]] = None,
        processor_type: Optional[str] = None,
        engine: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Convert PDF with comprehensive metadata.
        
        Args:
            pdf_path: Path to PDF file
            output_path: Optional output file path
            pages: Optional list of page numbers
            processor_type: Document processor type
            engine: Specific engine to use
            **kwargs: Engine-specific options
            
        Returns:
            Dictionary with converted content and metadata
        """
        pdf_path = Path(pdf_path)
        
        # Auto-detect processor if needed
        if processor_type == 'auto' or (processor_type is None and self.processor_type == 'auto'):
            processor_type = self._detect_document_type(pdf_path)
        
        processor = self._get_processor(processor_type)
        
        # Convert content
        processed_content = self.convert_pdf_to_markdown(
            pdf_path, None, pages, processor_type, engine, **kwargs
        )
        
        # Get engine that was actually used (after fallback logic)
        engine_name = engine or self.primary_engine_name
        used_engine = self._get_engine(engine_name)
        
        if not used_engine and self._get_engine(self.fallback_engine_name):
            used_engine = self._get_engine(self.fallback_engine_name)
        
        # Generate metadata
        base_metadata = used_engine.generate_metadata(pdf_path, processed_content, pages)
        enhanced_metadata = processor.enhance_metadata(base_metadata, processed_content)
        
        # Generate quality metrics
        base_quality = used_engine.validate_quality(processed_content)
        enhanced_quality = processor.enhance_quality_metrics(base_quality, processed_content)
        
        result = {
            'content': processed_content,
            'metadata': enhanced_metadata,
            'quality_metrics': enhanced_quality,
            'processing_info': {
                'engine_used': used_engine.name,
                'processor_used': processor.processor_name,
                'pages_converted': pages if pages else 'all'
            }
        }
        
        # Save files if output path provided
        if output_path:
            output_path = Path(output_path)
            
            # Save markdown content
            md_path = output_path.with_suffix('.md')
            md_path.parent.mkdir(parents=True, exist_ok=True)
            md_path.write_text(processed_content, encoding='utf-8')
            
            # Save metadata as JSON
            import json
            metadata_path = output_path.with_suffix('.metadata.json')
            metadata_path.write_text(json.dumps(result, indent=2, default=str), encoding='utf-8')
            
            logger.info(f"💾 Saved content to: {md_path}")
            logger.info(f"💾 Saved metadata to: {metadata_path}")
        
        return result
    
    @classmethod
    def is_available(cls) -> bool:
        """Check if any conversion engines are available."""
        return PyMuPDF4LLMEngine.is_available() or DoclingEngine.is_available() or DoclingVLMEngine.is_available()
    
    def list_available_engines(self) -> List[str]:
        """List available engines."""
        return list(self.engines.keys())
    
    def list_available_processors(self) -> List[str]:
        """List available processors."""
        return list(self.processors.keys())


# Convenience functions for backward compatibility
def convert_pdf_to_markdown(
    pdf_path: Union[str, Path],
    output_path: Optional[Union[str, Path]] = None,
    pages: Optional[List[int]] = None,
    processor_type: str = 'auto',
    **kwargs
) -> str:
    """Convenience function for PDF to markdown conversion.
    
    Args:
        pdf_path: Path to PDF file
        output_path: Optional output file path
        pages: Optional list of page numbers
        processor_type: Document processor type
        **kwargs: Additional options
        
    Returns:
        Converted markdown content
    """
    converter = UniversalPDFConverter(processor_type=processor_type)
    return converter.convert_pdf_to_markdown(pdf_path, output_path, pages, **kwargs)