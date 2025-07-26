"""Docling engine for advanced PDF layout analysis."""

from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from logging import getLogger
from time import time

from .base_engine import BaseEngine

logger = getLogger(__name__)

# Check if docling is available
try:
    from docling.document_converter import DocumentConverter, FormatOption
    from docling.datamodel.base_models import InputFormat
    from docling.datamodel.pipeline_options import PdfPipelineOptions, AcceleratorOptions, AcceleratorDevice
    from docling.pipeline.standard_pdf_pipeline import StandardPdfPipeline
    from docling.backend.docling_parse_v4_backend import DoclingParseV4DocumentBackend
    from docling_core.types.doc.base import ImageRefMode
    DOCLING_AVAILABLE = True
except ImportError:
    DOCLING_AVAILABLE = False
    logger.warning("📚 Docling not available. Install with: pip install docling")


class DoclingEngine(BaseEngine):
    """Advanced PDF conversion engine using Docling with OCR, table structure recognition, and embedded images."""
    
    def __init__(self, 
                 enable_ocr: bool = True,
                 enable_table_structure: bool = True,
                 ocr_languages: List[str] = None,
                 num_threads: int = 8,
                 device: str = "auto"):
        """Initialize Docling converter with advanced options.
        
        Args:
            enable_ocr: Enable OCR processing for better text extraction
            enable_table_structure: Enable advanced table structure recognition
            ocr_languages: List of OCR language codes (default: ["en"])
            num_threads: Number of threads for parallel processing  
            device: Processing device ("auto", "cpu", "cuda")
        """
        if not self.is_available():
            raise ImportError("Docling is not available. Install with: pip install docling")
        
        # Set default OCR languages to English if not specified
        if ocr_languages is None:
            ocr_languages = ["en"]
        
        # Configure pipeline options
        pipeline_options = PdfPipelineOptions()
        pipeline_options.do_ocr = enable_ocr
        pipeline_options.do_table_structure = enable_table_structure
        
        # Configure image generation for embedding
        pipeline_options.generate_page_images = True
        pipeline_options.generate_picture_images = True
        pipeline_options.images_scale = 2.0  # Higher resolution for better quality
        
        # Configure table structure options
        if enable_table_structure:
            pipeline_options.table_structure_options.do_cell_matching = False
        
        # Configure OCR options
        if enable_ocr:
            pipeline_options.ocr_options.lang = ocr_languages
        
        # Configure accelerator options for performance
        device_mapping = {
            "auto": AcceleratorDevice.AUTO,
            "cpu": AcceleratorDevice.CPU,
            "cuda": AcceleratorDevice.CUDA if hasattr(AcceleratorDevice, 'CUDA') else AcceleratorDevice.AUTO
        }
        
        pipeline_options.accelerator_options = AcceleratorOptions(
            num_threads=num_threads, 
            device=device_mapping.get(device.lower(), AcceleratorDevice.AUTO)
        )
        # Describe image references for embedded images
    #     pipeline_options.do_picture_description = True
    #     pipeline_options.picture_description_options = (
    #         granite_picture_description  # <-- the model choice
    # )
    #     pipeline_options.picture_description_options.prompt = (
    #         "Describe the image in three sentences. Be consise and accurate."
    #     )
        # Initialize DocumentConverter with advanced configuration
        self.converter = DocumentConverter(
            format_options={
                InputFormat.PDF: FormatOption(
                    pipeline_cls=StandardPdfPipeline,
                    pipeline_options=pipeline_options,
                    backend=DoclingParseV4DocumentBackend
                )
            }
        )
        
        # Store configuration for metadata
        self.config = {
            'ocr_enabled': enable_ocr,
            'table_structure_enabled': enable_table_structure,
            'ocr_languages': ocr_languages,
            'num_threads': num_threads,
            'device': device,
            'embedded_images': True,
            'images_scale': 2.0
        }
        
        logger.info(f"🔧 Docling configured with OCR: {enable_ocr}, Table Structure: {enable_table_structure}, Embedded Images: True, Languages: {ocr_languages}, Threads: {num_threads}, Device: {device}")
    
    def convert(
        self, 
        pdf_path: Union[str, Path], 
        pages: Optional[List[int]] = None,
        **kwargs
    ) -> str:
        """Convert PDF to markdown using Docling.
        
        Args:
            pdf_path: Path to PDF file
            pages: Optional list of page numbers (not supported by Docling)
            **kwargs: Docling-specific options
            
        Returns:
            Markdown content as string
        """
        if not self.is_available():
            raise ImportError("Docling is not available. Install with: pip install docling")
        
        if pages is not None:
            logger.warning("⚠️ Page selection not supported by Docling. Converting entire document.")
        
        pdf_path = Path(pdf_path)
        if not pdf_path.exists():
            raise FileNotFoundError(f"📄 PDF file not found: {pdf_path}")
        
        logger.info(f"🔄 Converting PDF using Docling with advanced features: {pdf_path.name}")
        
        try:
            start_time = time()
            
            # Convert PDF using Docling with OCR and table structure recognition
            result = self.converter.convert(str(pdf_path))
            
            # Export markdown 
            md_content = result.document.export_to_markdown(
                strict_text=False,
                include_annotations=True
            )
            
            conversion_time = time() - start_time
            
            # Log enhanced processing details
            ocr_status = "with OCR" if self.config['ocr_enabled'] else "without OCR"
            table_status = "with table structure" if self.config['table_structure_enabled'] else "without table structure"
            logger.info(f"✅ Successfully converted {pdf_path.name} to markdown in {conversion_time:.2f}s ({ocr_status}, {table_status})")
            
            return md_content
            
        except Exception as e:
            logger.error(f"❌ Failed to convert {pdf_path.name}: {e}")
            raise
    
    def validate_quality(self, content: str) -> Dict[str, Any]:
        """Validate conversion quality for Docling output.
        
        Args:
            content: Converted markdown content
            
        Returns:
            Quality metrics dictionary
        """
        lines = content.split('\n')
        non_empty_lines = [line for line in lines if line.strip()]
        headers = [line for line in lines if line.strip().startswith('#')]
        tables = content.count('|')  # Table indicators
        code_blocks = content.count('```')  # Code block indicators
        
        # Calculate average line length
        total_chars = sum(len(line) for line in non_empty_lines)
        avg_line_length = total_chars / len(non_empty_lines) if non_empty_lines else 0
        
        # Enhanced quality assessment for Docling
        quality_score = 'excellent' if (len(headers) >= 8 and len(non_empty_lines) >= 150 and avg_line_length > 30) else \
                       'good' if (len(headers) >= 4 and len(non_empty_lines) >= 80 and avg_line_length > 20) else \
                       'fair' if (len(headers) >= 2 and len(non_empty_lines) >= 40) else \
                       'needs_review'
        
        return {
            'total_lines': len(lines),
            'non_empty_lines': len(non_empty_lines),
            'headers_detected': len(headers),
            'table_markers': tables,
            'code_blocks': code_blocks // 2,
            'total_characters': len(content),
            'avg_line_length': round(avg_line_length, 2),
            'has_structure': len(headers) > 0 and len(non_empty_lines) > 50,
            'quality_assessment': quality_score,
            'engine': self.name
        }
    
    def generate_metadata(
        self, 
        pdf_path: Union[str, Path], 
        content: str,
        pages: Optional[List[int]] = None
    ) -> Dict[str, Any]:
        """Generate metadata for Docling conversion.
        
        Args:
            pdf_path: Source PDF path
            content: Converted content
            pages: Pages that were converted (not applicable for Docling)
            
        Returns:
            Metadata dictionary
        """
        quality_metrics = self.validate_quality(content)
        
        # Build feature list based on configuration
        features = [
            'advanced_layout_analysis',
            'reading_order_detection',
            'unified_document_representation',
            'embedded_images',
            'high_resolution_images'
        ]
        
        capabilities = [
            'layout_analysis',
            'reading_order',
            'document_structure',
            'image_embedding',
            'image_generation'
        ]
        
        if self.config['ocr_enabled']:
            features.extend(['ocr_text_extraction', 'multi_language_ocr'])
            capabilities.extend(['ocr_processing', 'language_detection'])
            
        if self.config['table_structure_enabled']:
            features.extend(['table_structure_preservation', 'cell_matching'])
            capabilities.extend(['table_detection', 'table_structure_analysis'])
        
        return {
            'source_file': str(pdf_path),
            'source_format': 'PDF',
            'conversion_engine': self.name,
            'pages_processed': 'all',  # Docling always processes all pages
            'total_characters': len(content),
            'total_lines': len(content.split('\n')),
            'features': features,
            'quality_metrics': quality_metrics,
            'docling_capabilities': capabilities,
            'configuration': {
                'ocr_enabled': self.config['ocr_enabled'],
                'table_structure_enabled': self.config['table_structure_enabled'],
                'ocr_languages': self.config['ocr_languages'],
                'num_threads': self.config['num_threads'],
                'processing_device': self.config['device'],
                'embedded_images': self.config['embedded_images'],
                'images_scale': self.config['images_scale']
            },
            'processing_enhancements': {
                'easyocr_integration': self.config['ocr_enabled'],
                'cell_matching': self.config['table_structure_enabled'],
                'parallel_processing': self.config['num_threads'] > 1,
                'hardware_acceleration': self.config['device'] != 'cpu',
                'embedded_images': self.config['embedded_images'],
                'high_resolution_images': self.config['images_scale'] > 1.0
            }
        }
    
    @classmethod
    def is_available(cls) -> bool:
        """Check if Docling is available."""
        return DOCLING_AVAILABLE
    
    @property
    def name(self) -> str:
        """Engine name."""
        return 'docling'
    
    @property
    def supports_page_selection(self) -> bool:
        """Docling does not support page selection."""
        return False