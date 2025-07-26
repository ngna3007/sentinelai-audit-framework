"""
General Hierarchical Chunking Processor using Docling

This processor implements hierarchical chunking of documents using docling's
HierarchicalChunker. It processes PDF documents directly and creates chunks that
preserve document structure and context, including heading hierarchy.

This is a hybrid approach that uses docling's built-in document structure
analysis to create more semantically meaningful chunks.
"""

from pathlib import Path
from typing import Dict, List, Optional, Any, Union
from datetime import datetime
from uuid import uuid4
import json
import csv

# Import docling components
try:
    from docling.document_converter import DocumentConverter, FormatOption
    from docling.datamodel.base_models import InputFormat
    from docling.datamodel.pipeline_options import PdfPipelineOptions
    from docling.pipeline.standard_pdf_pipeline import StandardPdfPipeline
    from docling.backend.docling_parse_v4_backend import DoclingParseV4DocumentBackend
    from docling_core.transforms.chunker import HierarchicalChunker
    DOCLING_AVAILABLE = True
except ImportError:
    DOCLING_AVAILABLE = False

from ...text_processors.general_text_processor import GeneralTextProcessor


class ChunkingResult:
    """Result object for chunking operations."""
    
    def __init__(self, success: bool, total_chunks: int = 0, chunks: List[Dict] = None, 
                 metadata: Dict = None, errors: List[str] = None):
        self.success = success
        self.total_chunks = total_chunks
        self.chunks = chunks or []
        self.metadata = metadata or {}
        self.errors = errors or []


class GeneralHierarchicalChunkingProcessor:
    """
    General-purpose processor for documents using hierarchical chunking via docling.
    
    This processor:
    1. Loads PDF documents directly (no markdown conversion needed)
    2. Uses docling's document structure analysis
    3. Applies hierarchical chunking using docling's HierarchicalChunker
    4. Preserves document structure and heading context
    5. Generates metadata for each chunk including hierarchical context
    6. Outputs both JSON and CSV formats
    
    This is a hybrid approach combining docling's structure analysis with chunking.
    """
    
    def __init__(self, 
                 chunk_size: int = 1024,
                 enable_ocr: bool = True,
                 enable_table_structure: bool = True,
                 num_threads: int = 4):
        """
        Initialize the hierarchical chunking processor.
        
        Args:
            chunk_size: Target size for chunks in characters (not tokens for docling)
            enable_ocr: Enable OCR processing for better text extraction
            enable_table_structure: Enable table structure recognition
            num_threads: Number of threads for parallel processing
        """
        if not DOCLING_AVAILABLE:
            raise ImportError("docling library not available. Install with: pip install docling")
        
        self.chunk_size = chunk_size
        self.enable_ocr = enable_ocr
        self.enable_table_structure = enable_table_structure
        self.num_threads = num_threads
        
        # Configure docling pipeline options
        pipeline_options = PdfPipelineOptions()
        pipeline_options.do_ocr = enable_ocr
        pipeline_options.do_table_structure = enable_table_structure
        
        # Initialize DocumentConverter
        self.converter = DocumentConverter(
            format_options={
                InputFormat.PDF: FormatOption(
                    pipeline_cls=StandardPdfPipeline,
                    pipeline_options=pipeline_options,
                    backend=DoclingParseV4DocumentBackend
                )
            }
        )
        
        # Initialize hierarchical chunker
        self.chunker = HierarchicalChunker(
            chunk_size=chunk_size,
            overlap=0.1  # Small overlap for context preservation
        )
        
        self.text_processor = GeneralTextProcessor()
        
    def load_pdf(self, pdf_path: str) -> Any:
        """Load PDF and convert to docling document."""
        path = Path(pdf_path)
        if not path.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        # Convert PDF to docling document
        result = self.converter.convert(str(path))
        return result.document
    
    def load_markdown(self, markdown_path: str) -> str:
        """Load markdown content from file (fallback method)."""
        path = Path(markdown_path)
        if not path.exists():
            raise FileNotFoundError(f"Markdown file not found: {markdown_path}")
        
        return path.read_text(encoding='utf-8')
    
    def chunk_document(self, document_path: str, source: str = None) -> ChunkingResult:
        """
        Chunk the document using hierarchical chunking.
        
        Args:
            document_path: Path to the PDF or markdown document
            source: Custom source identifier (defaults to filename if not provided)
            
        Returns:
            ChunkingResult with chunks and metadata
        """
        try:
            path = Path(document_path)
            
            # Determine if we have a PDF or markdown file
            if path.suffix.lower() == '.pdf':
                # Use docling's hierarchical chunking for PDF
                docling_doc = self.load_pdf(document_path)
                
                # Apply hierarchical chunking
                chunks = list(self.chunker.chunk(docling_doc))
                
                # Convert docling chunks to our format
                processed_chunks = []
                chunk_source = source if source else path.stem
                
                for i, chunk in enumerate(chunks):
                    # Extract hierarchical context
                    headings = []
                    if hasattr(chunk, 'meta') and hasattr(chunk.meta, 'headings'):
                        headings = [
                            {
                                'level': heading.level if hasattr(heading, 'level') else 1,
                                'text': heading.text if hasattr(heading, 'text') else str(heading)
                            }
                            for heading in chunk.meta.headings
                        ]
                    
                    # Create chunk data with hierarchical context
                    chunk_data = {
                        'chunk_id': str(uuid4()),
                        'chunk_index': i,
                        'text': chunk.text,
                        'token_count': len(chunk.text.split()),  # Approximate token count
                        'source': chunk_source,
                        'hierarchical_context': {
                            'headings': headings,
                            'level': len(headings),  # Current nesting level
                            'parent_sections': [h['text'] for h in headings]
                        }
                    }
                    processed_chunks.append(chunk_data)
                
                # Generate metadata
                metadata = {
                    'source_file': document_path,
                    'total_chunks': len(processed_chunks),
                    'chunking_method': 'hierarchical',
                    'chunking_library': 'docling',
                    'document_type': 'pdf',
                    'processed_at': datetime.now().isoformat(),
                    'total_tokens': sum(chunk['token_count'] for chunk in processed_chunks),
                    'avg_chunk_size': sum(chunk['token_count'] for chunk in processed_chunks) / len(processed_chunks) if processed_chunks else 0,
                    'chunk_size_target': self.chunk_size,
                    'structural_features': {
                        'hierarchical_context': True,
                        'heading_preservation': True,
                        'document_structure': True,
                        'ocr_enabled': self.enable_ocr,
                        'table_structure_enabled': self.enable_table_structure
                    }
                }
                
            else:
                # Fallback to markdown processing with simulated hierarchy
                content = self.load_markdown(document_path)
                
                # Preprocess markdown
                content = self.text_processor.preprocess_markdown_for_chunking(content)
                
                # Simple hierarchical chunking for markdown
                processed_chunks = self._chunk_markdown_hierarchically(content, source or path.stem)
                
                # Generate metadata for markdown
                metadata = {
                    'source_file': document_path,
                    'total_chunks': len(processed_chunks),
                    'chunking_method': 'hierarchical_markdown',
                    'chunking_library': 'custom',
                    'document_type': 'markdown',
                    'processed_at': datetime.now().isoformat(),
                    'total_tokens': sum(chunk['token_count'] for chunk in processed_chunks),
                    'avg_chunk_size': sum(chunk['token_count'] for chunk in processed_chunks) / len(processed_chunks) if processed_chunks else 0,
                    'chunk_size_target': self.chunk_size,
                    'structural_features': {
                        'hierarchical_context': True,
                        'heading_preservation': True,
                        'document_structure': True,
                        'ocr_enabled': False,
                        'table_structure_enabled': False
                    }
                }
            
            return ChunkingResult(
                success=True,
                total_chunks=len(processed_chunks),
                chunks=processed_chunks,
                metadata=metadata
            )
            
        except Exception as e:
            return ChunkingResult(
                success=False,
                errors=[f"Hierarchical chunking failed: {str(e)}"]
            )
    
    def _chunk_markdown_hierarchically(self, content: str, source: str) -> List[Dict]:
        """
        Fallback hierarchical chunking for markdown content.
        
        Args:
            content: Markdown content
            source: Source identifier
            
        Returns:
            List of chunk dictionaries
        """
        lines = content.split('\n')
        chunks = []
        current_chunk = []
        current_headings = []
        chunk_index = 0
        
        for line in lines:
            # Detect heading
            if line.strip().startswith('#'):
                # Save current chunk if it has content
                if current_chunk:
                    chunk_text = '\n'.join(current_chunk).strip()
                    if chunk_text:
                        chunks.append({
                            'chunk_id': str(uuid4()),
                            'chunk_index': chunk_index,
                            'text': chunk_text,
                            'token_count': len(chunk_text.split()),
                            'source': source,
                            'hierarchical_context': {
                                'headings': current_headings.copy(),
                                'level': len(current_headings),
                                'parent_sections': [h['text'] for h in current_headings]
                            }
                        })
                        chunk_index += 1
                        current_chunk = []
                
                # Update heading context
                level = len(line) - len(line.lstrip('#'))
                heading_text = line.strip('# ').strip()
                
                # Update headings based on level
                current_headings = [h for h in current_headings if h['level'] < level]
                current_headings.append({
                    'level': level,
                    'text': heading_text
                })
            
            current_chunk.append(line)
            
            # Check if chunk is getting too large
            if len('\n'.join(current_chunk)) > self.chunk_size:
                chunk_text = '\n'.join(current_chunk).strip()
                if chunk_text:
                    chunks.append({
                        'chunk_id': str(uuid4()),
                        'chunk_index': chunk_index,
                        'text': chunk_text,
                        'token_count': len(chunk_text.split()),
                        'source': source,
                        'hierarchical_context': {
                            'headings': current_headings.copy(),
                            'level': len(current_headings),
                            'parent_sections': [h['text'] for h in current_headings]
                        }
                    })
                    chunk_index += 1
                    current_chunk = []
        
        # Save final chunk
        if current_chunk:
            chunk_text = '\n'.join(current_chunk).strip()
            if chunk_text:
                chunks.append({
                    'chunk_id': str(uuid4()),
                    'chunk_index': chunk_index,
                    'text': chunk_text,
                    'token_count': len(chunk_text.split()),
                    'source': source,
                    'hierarchical_context': {
                        'headings': current_headings.copy(),
                        'level': len(current_headings),
                        'parent_sections': [h['text'] for h in current_headings]
                    }
                })
        
        return chunks
    
    def save_chunks_json(self, chunks: List[Dict], output_path: str) -> bool:
        """Save chunks to JSON format."""
        try:
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(chunks, f, indent=2, ensure_ascii=False)
            
            return True
        except Exception:
            return False
    
    def save_chunks_csv(self, chunks: List[Dict], output_path: str) -> bool:
        """
        Save chunks to CSV format compatible with vector databases.
        
        CSV format: chunk_id, chunk_index, text, token_count, source, hierarchical_level, parent_sections
        """
        try:
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            fieldnames = [
                'chunk_id',
                'chunk_index',
                'text',
                'token_count',
                'source',
                'hierarchical_level',
                'parent_sections'
            ]
            
            with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                
                for chunk in chunks:
                    # Flatten hierarchical context for CSV
                    hierarchical_context = chunk.get('hierarchical_context', {})
                    parent_sections = ' > '.join(hierarchical_context.get('parent_sections', []))
                    
                    row = {
                        'chunk_id': chunk['chunk_id'],
                        'chunk_index': chunk['chunk_index'],
                        'text': chunk['text'],
                        'token_count': chunk['token_count'],
                        'source': chunk['source'],
                        'hierarchical_level': hierarchical_context.get('level', 0),
                        'parent_sections': parent_sections
                    }
                    writer.writerow(row)
            
            return True
        except Exception:
            return False
    
    def process_document(self, document_path: str, output_dir: str, source: str = None) -> ChunkingResult:
        """
        Complete processing: chunk document and save in both JSON and CSV formats.
        
        Args:
            document_path: Path to input document (PDF or markdown)
            output_dir: Directory to save output files
            source: Custom source identifier (defaults to filename if not provided)
            
        Returns:
            ChunkingResult with processing status
        """
        # Chunk the document
        result = self.chunk_document(document_path, source)
        
        if not result.success:
            return result
        
        # Create output directory
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Generate output filenames
        source_name = Path(document_path).stem
        json_output = output_path / f"{source_name}-hierarchical_chunks.json"
        csv_output = output_path / f"{source_name}-hierarchical_chunks.csv"
        metadata_output = output_path / f"{source_name}-hierarchical_metadata.json"
        
        # Save outputs
        json_saved = self.save_chunks_json(result.chunks, str(json_output))
        csv_saved = self.save_chunks_csv(result.chunks, str(csv_output))
        
        # Save metadata
        metadata_saved = self.save_chunks_json([result.metadata], str(metadata_output))
        
        # Update result with file paths
        result.metadata['output_files'] = {
            'json_file': str(json_output) if json_saved else None,
            'csv_file': str(csv_output) if csv_saved else None,
            'metadata_file': str(metadata_output) if metadata_saved else None
        }
        
        # Add any errors
        if not json_saved:
            result.errors.append("Failed to save JSON output")
        if not csv_saved:
            result.errors.append("Failed to save CSV output")
        if not metadata_saved:
            result.errors.append("Failed to save metadata")
        
        # Update success status
        result.success = json_saved and csv_saved and metadata_saved
        
        return result


def chunk_document(document_path: str, output_dir: str, 
                  chunk_size: int = 1024, source: str = None,
                  enable_ocr: bool = True, enable_table_structure: bool = True) -> ChunkingResult:
    """
    Convenience function to chunk any document using hierarchical chunking.
    
    Args:
        document_path: Path to the document (PDF or markdown)
        output_dir: Output directory for chunked files
        chunk_size: Target chunk size in characters
        source: Custom source identifier (defaults to filename if not provided)
        enable_ocr: Enable OCR processing for PDFs
        enable_table_structure: Enable table structure recognition
        
    Returns:
        ChunkingResult with processing status and metadata
    """
    processor = GeneralHierarchicalChunkingProcessor(
        chunk_size=chunk_size,
        enable_ocr=enable_ocr,
        enable_table_structure=enable_table_structure
    )
    return processor.process_document(document_path, output_dir, source)