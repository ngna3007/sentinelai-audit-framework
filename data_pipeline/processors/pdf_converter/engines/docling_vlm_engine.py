"""Enhanced Docling engine with Vision Language Model (VLM) for picture annotation."""

from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from logging import getLogger
from time import time
import json

from .base_engine import BaseEngine

logger = getLogger(__name__)

# Check if docling with VLM is available
try:
    from docling.document_converter import DocumentConverter, FormatOption
    from docling.datamodel.base_models import InputFormat
    from docling.datamodel.pipeline_options import PdfPipelineOptions, AcceleratorOptions, AcceleratorDevice
    from docling.pipeline.standard_pdf_pipeline import StandardPdfPipeline
    from docling.backend.docling_parse_v4_backend import DoclingParseV4DocumentBackend
    from docling_core.types.doc.base import ImageRefMode
    
    # VLM-specific imports
    try:
        from docling.datamodel.pipeline_options import (
            PictureDescriptionVlmOptions, 
            VlmPipelineOptions,
            granite_picture_description,
            smolvlm_picture_description
        )
        VLM_AVAILABLE = True
    except ImportError:
        VLM_AVAILABLE = False
        logger.warning("🤖 VLM features not available. Install with: pip install 'docling[vlm]'")
        
    DOCLING_AVAILABLE = True
except ImportError:
    DOCLING_AVAILABLE = False
    VLM_AVAILABLE = False
    logger.warning("📚 Docling not available. Install with: pip install 'docling[vlm]'")


class DoclingVLMEngine(BaseEngine):
    """Enhanced Docling engine with Vision Language Model for picture annotation and description."""
    
    def __init__(self, 
                 enable_ocr: bool = True,
                 enable_table_structure: bool = True,
                 enable_picture_description: bool = True,
                 vision_model: str = "smolvlm",
                 picture_description_prompt: str = None,
                 ocr_languages: List[str] = None,
                 num_threads: int = 8,
                 device: str = "auto"):
        """Initialize Enhanced Docling converter with VLM picture annotation.
        
        Args:
            enable_ocr: Enable OCR processing for better text extraction
            enable_table_structure: Enable advanced table structure recognition
            enable_picture_description: Enable VLM-based picture description
            vision_model: Vision model to use ("granite_vision", "smolvlm", "custom")
            picture_description_prompt: Custom prompt for picture description
            ocr_languages: List of OCR language codes (default: ["en"])
            num_threads: Number of threads for parallel processing  
            device: Processing device ("auto", "cpu", "cuda")
        """
        if not self.is_available():
            raise ImportError("Docling is not available. Install with: pip install 'docling[vlm]'")
        
        if enable_picture_description and not VLM_AVAILABLE:
            logger.warning("🤖 VLM features not available. Picture description will be disabled.")
            enable_picture_description = False
        
        # Set default OCR languages to English if not specified
        if ocr_languages is None:
            ocr_languages = ["en"]
            
        # Set default picture description prompt if not provided
        if picture_description_prompt is None:
            picture_description_prompt = (
                "Describe this image in detail, focusing on key visual elements, "
                "text content, diagrams, charts, and any relevant information that "
                "would be useful for document understanding and search. Be concise but comprehensive."
            )
        
        # Configure pipeline options
        pipeline_options = PdfPipelineOptions()
        pipeline_options.do_ocr = enable_ocr
        pipeline_options.do_table_structure = enable_table_structure
        
        # Configure image generation for embedding and VLM processing
        pipeline_options.generate_page_images = True
        pipeline_options.generate_picture_images = True
        pipeline_options.images_scale = 2.0  # Higher resolution for better VLM analysis
        
        # Configure VLM picture description
        if enable_picture_description and VLM_AVAILABLE:
            try:
                pipeline_options.do_picture_description = True
                
                # Configure vision model based on selection
                if vision_model.lower() == "granite_vision":
                    # Use IBM Granite Vision model
                    vlm_config = granite_picture_description
                elif vision_model.lower() == "smolvlm":
                    # Use SmolVLM model
                    vlm_config = smolvlm_picture_description
                else:
                    logger.warning(f"🤖 Unknown vision model: {vision_model}. Using granite_vision as default.")
                    vlm_config = granite_picture_description
                
                # Set VLM configuration
                pipeline_options.picture_description_options = vlm_config
                
                # Override prompt if custom prompt is provided
                if picture_description_prompt != vlm_config.prompt:
                    # Create a copy of the configuration with custom prompt
                    from copy import deepcopy
                    custom_config = deepcopy(vlm_config)
                    custom_config.prompt = picture_description_prompt
                    pipeline_options.picture_description_options = custom_config
                    
                logger.info(f"🤖 VLM picture description enabled with {vision_model}")
                
            except Exception as e:
                logger.error(f"❌ Failed to configure VLM picture description: {e}")
                enable_picture_description = False
                pipeline_options.do_picture_description = False
        
        # Configure table structure options
        if enable_table_structure:
            pipeline_options.table_structure_options.do_cell_matching = True
        
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
        
        # Initialize DocumentConverter with VLM configuration
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
            'picture_description_enabled': enable_picture_description,
            'vision_model': vision_model,
            'picture_description_prompt': picture_description_prompt,
            'ocr_languages': ocr_languages,
            'num_threads': num_threads,
            'device': device,
            'embedded_images': True,
            'images_scale': 2.0,
            'vlm_available': VLM_AVAILABLE
        }
        
        logger.info(f"🔧 Enhanced Docling configured with OCR: {enable_ocr}, "
                   f"Table Structure: {enable_table_structure}, "
                   f"Picture Description: {enable_picture_description}, "
                   f"Vision Model: {vision_model}, "
                   f"Languages: {ocr_languages}, "
                   f"Threads: {num_threads}, "
                   f"Device: {device}")
    
    def convert(
        self, 
        pdf_path: Union[str, Path], 
        pages: Optional[List[int]] = None,
        export_images: bool = True,
        **kwargs
    ) -> str:
        """Convert PDF to markdown using Enhanced Docling with VLM picture annotation.
        
        Args:
            pdf_path: Path to PDF file
            pages: Optional list of page numbers (not supported by Docling)
            export_images: Whether to export images with descriptions
            **kwargs: Docling-specific options
            
        Returns:
            Markdown content as string with picture descriptions
        """
        if not self.is_available():
            raise ImportError("Docling is not available. Install with: pip install 'docling[vlm]'")
        
        if pages is not None:
            logger.warning("⚠️ Page selection not supported by Docling. Converting entire document.")
        
        pdf_path = Path(pdf_path)
        if not pdf_path.exists():
            raise FileNotFoundError(f"📄 PDF file not found: {pdf_path}")
        
        logger.info(f"🔄 Converting PDF using Enhanced Docling with VLM: {pdf_path.name}")
        
        try:
            start_time = time()
            
            # Convert PDF using Enhanced Docling with VLM
            result = self.converter.convert(str(pdf_path))
            
            # Export markdown with picture descriptions
            md_content = result.document.export_to_markdown(
                strict_text=False,
                include_annotations=True,
                image_placeholder="[IMAGE_PLACEHOLDER]"
            )
            
            # Process and enhance image descriptions if VLM is enabled
            if self.config['picture_description_enabled'] and VLM_AVAILABLE:
                md_content = self._enhance_image_descriptions(md_content, result)
            
            conversion_time = time() - start_time
            
            # Log enhanced processing details
            ocr_status = "with OCR" if self.config['ocr_enabled'] else "without OCR"
            table_status = "with table structure" if self.config['table_structure_enabled'] else "without table structure"
            vlm_status = "with VLM picture description" if self.config['picture_description_enabled'] else "without VLM"
            
            logger.info(f"✅ Successfully converted {pdf_path.name} to markdown in {conversion_time:.2f}s "
                       f"({ocr_status}, {table_status}, {vlm_status})")
            
            return md_content
            
        except Exception as e:
            logger.error(f"❌ Failed to convert {pdf_path.name}: {e}")
            raise
    
    def _enhance_image_descriptions(self, md_content: str, result) -> str:
        """Enhance markdown content with VLM-generated image descriptions.
        
        Args:
            md_content: Original markdown content
            result: Docling conversion result with image data
            
        Returns:
            Enhanced markdown with detailed image descriptions
        """
        try:
            # Extract image descriptions from the result
            enhanced_content = md_content
            
            # Process document images if available
            if hasattr(result, 'document') and hasattr(result.document, 'pictures'):
                for i, picture in enumerate(result.document.pictures):
                    if hasattr(picture, 'annotations') and picture.annotations:
                        # Get VLM-generated description
                        description = self._extract_picture_description(picture)
                        if description:
                            # Replace or enhance image placeholders with descriptions
                            placeholder = f"[IMAGE_PLACEHOLDER_{i}]"
                            enhanced_description = f"**Image {i+1}:** {description}"
                            enhanced_content = enhanced_content.replace(
                                placeholder, 
                                enhanced_description
                            )
            
            return enhanced_content
            
        except Exception as e:
            logger.warning(f"⚠️ Failed to enhance image descriptions: {e}")
            return md_content
    
    def _extract_picture_description(self, picture) -> str:
        """Extract VLM-generated description from picture annotations.
        
        Args:
            picture: Picture object with annotations
            
        Returns:
            VLM-generated description string
        """
        try:
            # Extract description from picture annotations
            if hasattr(picture, 'annotations'):
                for annotation in picture.annotations:
                    if hasattr(annotation, 'description'):
                        return annotation.description
                    elif hasattr(annotation, 'text'):
                        return annotation.text
                        
            return ""
            
        except Exception as e:
            logger.warning(f"⚠️ Failed to extract picture description: {e}")
            return ""
    
    def validate_quality(self, content: str) -> Dict[str, Any]:
        """Validate conversion quality for Enhanced Docling with VLM output.
        
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
        
        # Count VLM-generated image descriptions
        image_descriptions = content.count('**Image')
        image_placeholders = content.count('[IMAGE_PLACEHOLDER]')
        
        # Calculate average line length
        total_chars = sum(len(line) for line in non_empty_lines)
        avg_line_length = total_chars / len(non_empty_lines) if non_empty_lines else 0
        
        # Enhanced quality assessment for VLM-enabled Docling
        base_score = 'excellent' if (len(headers) >= 8 and len(non_empty_lines) >= 150 and avg_line_length > 30) else \
                    'good' if (len(headers) >= 4 and len(non_empty_lines) >= 80 and avg_line_length > 20) else \
                    'fair' if (len(headers) >= 2 and len(non_empty_lines) >= 40) else \
                    'needs_review'
        
        # Boost quality score if VLM descriptions are present
        if image_descriptions > 0 and self.config['picture_description_enabled']:
            quality_scores = ['needs_review', 'fair', 'good', 'excellent']
            current_index = quality_scores.index(base_score)
            if current_index < len(quality_scores) - 1:
                base_score = quality_scores[current_index + 1]
        
        return {
            'total_lines': len(lines),
            'non_empty_lines': len(non_empty_lines),
            'headers_detected': len(headers),
            'table_markers': tables,
            'code_blocks': code_blocks // 2,
            'image_descriptions': image_descriptions,
            'image_placeholders': image_placeholders,
            'total_characters': len(content),
            'avg_line_length': round(avg_line_length, 2),
            'has_structure': len(headers) > 0 and len(non_empty_lines) > 50,
            'has_vlm_descriptions': image_descriptions > 0,
            'quality_assessment': base_score,
            'engine': self.name
        }
    
    def generate_metadata(
        self, 
        pdf_path: Union[str, Path], 
        content: str,
        pages: Optional[List[int]] = None
    ) -> Dict[str, Any]:
        """Generate metadata for Enhanced Docling with VLM conversion.
        
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
            
        if self.config['picture_description_enabled']:
            features.extend(['vlm_picture_description', 'vision_language_model', 'automated_image_annotation'])
            capabilities.extend(['vision_language_processing', 'image_understanding', 'content_description'])
        
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
                'picture_description_enabled': self.config['picture_description_enabled'],
                'vision_model': self.config['vision_model'],
                'ocr_languages': self.config['ocr_languages'],
                'num_threads': self.config['num_threads'],
                'processing_device': self.config['device'],
                'embedded_images': self.config['embedded_images'],
                'images_scale': self.config['images_scale'],
                'vlm_available': self.config['vlm_available']
            },
            'vlm_enhancements': {
                'vision_language_model': self.config['vision_model'],
                'picture_description_prompt': self.config['picture_description_prompt'],
                'automated_image_annotation': self.config['picture_description_enabled'],
                'image_understanding': self.config['vlm_available'],
                'description_count': quality_metrics.get('image_descriptions', 0)
            },
            'processing_enhancements': {
                'easyocr_integration': self.config['ocr_enabled'],
                'cell_matching': self.config['table_structure_enabled'],
                'parallel_processing': self.config['num_threads'] > 1,
                'hardware_acceleration': self.config['device'] != 'cpu',
                'embedded_images': self.config['embedded_images'],
                'high_resolution_images': self.config['images_scale'] > 1.0,
                'vlm_picture_description': self.config['picture_description_enabled']
            }
        }
    
    def convert_image_only(self, image_path: Union[str, Path], **kwargs) -> str:
        """Convert a single image file using VLM for description.
        
        Args:
            image_path: Path to image file
            **kwargs: Additional options
            
        Returns:
            Image description as markdown
        """
        if not self.config['picture_description_enabled']:
            raise ValueError("Picture description is not enabled. Initialize with enable_picture_description=True")
        
        image_path = Path(image_path)
        if not image_path.exists():
            raise FileNotFoundError(f"📷 Image file not found: {image_path}")
        
        logger.info(f"🔄 Processing image with VLM: {image_path.name}")
        
        try:
            # Convert image using VLM
            result = self.converter.convert(str(image_path))
            
            # Extract description
            description = result.document.export_to_markdown(
                strict_text=False,
                include_annotations=True
            )
            
            logger.info(f"✅ Successfully processed image: {image_path.name}")
            return description
            
        except Exception as e:
            logger.error(f"❌ Failed to process image {image_path.name}: {e}")
            raise
    
    @classmethod
    def is_available(cls) -> bool:
        """Check if Enhanced Docling with VLM is available."""
        return DOCLING_AVAILABLE
    
    @classmethod
    def is_vlm_available(cls) -> bool:
        """Check if VLM features are available."""
        return VLM_AVAILABLE
    
    @property
    def name(self) -> str:
        """Engine name."""
        return 'docling_vlm'
    
    @property
    def supports_page_selection(self) -> bool:
        """Docling does not support page selection."""
        return False
    
    @property
    def supports_image_description(self) -> bool:
        """Check if image description is supported."""
        return self.config['picture_description_enabled'] and VLM_AVAILABLE