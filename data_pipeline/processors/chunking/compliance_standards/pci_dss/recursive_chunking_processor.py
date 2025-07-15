"""
Recursive Chunking Processor for PCI DSS Documents using Chonkie

This processor implements recursive chunking of PCI DSS documents using the chonkie library.
It processes markdown documents and creates semantically meaningful chunks that can be
converted to CSV format for vector database ingestion.

Following the existing data pipeline patterns and architecture.
"""

from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
from uuid import uuid4
import json
import csv

try:
    from chonkie import RecursiveChunker, RecursiveRules, OverlapRefinery
    CHONKIE_AVAILABLE = True
except ImportError:
    CHONKIE_AVAILABLE = False

from ....text_processors.compliance_standards.pci_dss.text_processor import TextProcessor


class ChunkingResult:
    """Result object for chunking operations."""
    
    def __init__(self, success: bool, total_chunks: int = 0, chunks: List[Dict] = None, 
                 metadata: Dict = None, errors: List[str] = None):
        self.success = success
        self.total_chunks = total_chunks
        self.chunks = chunks or []
        self.metadata = metadata or {}
        self.errors = errors or []


class RecursiveChunkingProcessor:
    """
    Processes PCI DSS documents using recursive chunking via chonkie library.
    
    This processor:
    1. Loads markdown documents
    2. Applies recursive chunking using chonkie
    3. Generates metadata for each chunk
    4. Outputs both JSON and CSV formats
    """
    
    def __init__(self, chunk_size: int = 512, overlap: float = 0.25):
        """
        Initialize the chunking processor.
        
        Args:
            chunk_size: Target size for chunks in tokens
            overlap: Overlap between chunks as percentage (0.25 = 25% overlap)
        """
        if not CHONKIE_AVAILABLE:
            raise ImportError("chonkie library not available. Install with: pip install chonkie")
        
        self.chunk_size = chunk_size
        self.overlap = overlap
        self.chunker = RecursiveChunker(
            tokenizer_or_token_counter="character",  # Using character-based counting as baseline
            chunk_size=chunk_size,
            rules=RecursiveRules(),
            min_characters_per_chunk=50  # Minimum characters to avoid tiny chunks
        )
        
        # Initialize OverlapRefinery with default values from documentation
        self.overlap_refinery = OverlapRefinery(
            tokenizer_or_token_counter="character",
            context_size=overlap,  # Percentage of chunk size for overlap
            method="suffix",       # Add context from next chunk (default)
            merge=True,           # Directly modify chunk text (default)
            inplace=True          # Modify chunks in place (default)
        )
        
        self.text_processor = TextProcessor()
        
    def load_markdown(self, markdown_path: str) -> str:
        """Load markdown content from file."""
        path = Path(markdown_path)
        if not path.exists():
            raise FileNotFoundError(f"Markdown file not found: {markdown_path}")
        
        return path.read_text(encoding='utf-8')
    
    def chunk_document(self, markdown_path: str, source: str = None) -> ChunkingResult:
        """
        Chunk the entire document using recursive chunking.
        
        Args:
            markdown_path: Path to the markdown document
            source: Custom source identifier (defaults to filename if not provided)
            
        Returns:
            ChunkingResult with chunks and metadata
        """
        try:
            # Load markdown content
            content = self.load_markdown(markdown_path)
            
            # Preprocess markdown to clean up whitespace and artifacts for better chunking
            content = self.text_processor.preprocess_markdown_for_chunking(content)
            
            # Apply recursive chunking
            chunks = self.chunker(content)
            
            # Apply overlap refinery for context overlap
            if self.overlap > 0:
                chunks = self.overlap_refinery(chunks)
            
            # Convert chonkie chunks to our simplified format
            processed_chunks = []
            # Use provided source or default to filename
            chunk_source = source if source else Path(markdown_path).stem
            
            for i, chunk in enumerate(chunks):
                chunk_data = {
                    'chunk_id': str(uuid4()),
                    'chunk_index': i,
                    'text': chunk.text,
                    'token_count': chunk.token_count,
                    'source': chunk_source
                }
                processed_chunks.append(chunk_data)
            
            # Generate overall metadata
            metadata = {
                'source_file': markdown_path,
                'total_chunks': len(processed_chunks),
                'chunking_method': 'recursive',
                'chunking_library': 'chonkie',
                'processed_at': datetime.now().isoformat(),
                'total_tokens': sum(chunk['token_count'] for chunk in processed_chunks),
                'avg_chunk_size': sum(chunk['token_count'] for chunk in processed_chunks) / len(processed_chunks) if processed_chunks else 0,
                'framework': 'PCI_DSS_v4_0_1'
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
                errors=[f"Chunking failed: {str(e)}"]
            )
    
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
        
        CSV format follows the existing pattern from the data pipeline.
        """
        try:
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            fieldnames = [
                'chunk_id',
                'chunk_index', 
                'text',
                'token_count',
                'source'
            ]
            
            with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                
                for chunk in chunks:
                    # Direct row creation - no metadata to flatten
                    writer.writerow(chunk)
            
            return True
        except Exception:
            return False
    
    def process_document(self, markdown_path: str, output_dir: str, source: str = None) -> ChunkingResult:
        """
        Complete processing: chunk document and save in both JSON and CSV formats.
        
        Args:
            markdown_path: Path to input markdown document
            output_dir: Directory to save output files
            source: Custom source identifier (defaults to filename if not provided)
            
        Returns:
            ChunkingResult with processing status
        """
        # Chunk the document
        result = self.chunk_document(markdown_path, source)
        
        if not result.success:
            return result
        
        # Create output directory
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Generate output filenames
        source_name = Path(markdown_path).stem
        json_output = output_path / f"{source_name}_chunks.json"
        csv_output = output_path / f"{source_name}_chunks.csv"
        metadata_output = output_path / f"{source_name}_metadata.json"
        
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


def chunk_pci_dss_document(markdown_path: str, output_dir: str, 
                          chunk_size: int = 512, overlap: float = 0.25, source: str = None) -> ChunkingResult:
    """
    Convenience function to chunk a PCI DSS document.
    
    Args:
        markdown_path: Path to the PCI DSS markdown document
        output_dir: Output directory for chunked files
        chunk_size: Target chunk size in tokens
        overlap: Overlap between chunks as percentage (0.25 = 25% overlap)
        source: Custom source identifier (defaults to filename if not provided)
        
    Returns:
        ChunkingResult with processing status and metadata
    """
    processor = RecursiveChunkingProcessor(chunk_size=chunk_size, overlap=overlap)
    return processor.process_document(markdown_path, output_dir, source)