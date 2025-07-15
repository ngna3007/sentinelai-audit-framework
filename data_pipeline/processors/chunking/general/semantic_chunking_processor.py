"""
General Semantic Chunking Processor using Chonkie

This processor implements semantic chunking of documents using the chonkie library.
It processes markdown documents and creates semantically meaningful chunks based on
content similarity, ensuring that related content stays together in the same chunk.

This is a general-purpose processor that can be used for any document type.
"""

from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
from uuid import uuid4
import json
import csv

try:
    from chonkie import SemanticChunker
    CHONKIE_AVAILABLE = True
except ImportError:
    CHONKIE_AVAILABLE = False

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


class GeneralSemanticChunkingProcessor:
    """
    General-purpose processor for documents using semantic chunking via chonkie library.
    
    This processor:
    1. Loads markdown documents
    2. Applies text preprocessing to clean artifacts
    3. Applies semantic chunking using chonkie with embedding similarity
    4. Generates metadata for each chunk
    5. Outputs both JSON and CSV formats
    
    Can be used for any document type and framework.
    """
    
    def __init__(self, chunk_size: int = 1024, threshold: float = 0.5, 
                 embedding_model: str = "minishlab/potion-base-8M"):
        """
        Initialize the semantic chunking processor.
        
        Args:
            chunk_size: Target size for chunks in tokens
            threshold: Similarity threshold for semantic chunking (0.0-1.0)
            embedding_model: Model to use for semantic embeddings
        """
        if not CHONKIE_AVAILABLE:
            raise ImportError("chonkie library not available. Install with: pip install 'chonkie[semantic]'")
        
        self.chunk_size = chunk_size
        self.threshold = threshold
        self.embedding_model = embedding_model
        
        try:
            self.chunker = SemanticChunker(
                embedding_model=embedding_model,
                chunk_size=chunk_size,
                threshold=threshold
            )
        except Exception as e:
            raise ImportError(f"Failed to initialize semantic chunker. Please ensure you have installed 'chonkie[semantic]': {e}")
        
        self.text_processor = GeneralTextProcessor()
        
    def load_markdown(self, markdown_path: str) -> str:
        """Load markdown content from file."""
        path = Path(markdown_path)
        if not path.exists():
            raise FileNotFoundError(f"Markdown file not found: {markdown_path}")
        
        return path.read_text(encoding='utf-8')
    
    def chunk_document(self, markdown_path: str, source: str = None) -> ChunkingResult:
        """
        Chunk the entire document using semantic chunking.
        
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
            
            # Apply semantic chunking
            chunks = self.chunker.chunk(content)
            
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
                'chunking_method': 'semantic',
                'chunking_library': 'chonkie',
                'embedding_model': self.embedding_model,
                'processed_at': datetime.now().isoformat(),
                'total_tokens': sum(chunk['token_count'] for chunk in processed_chunks),
                'avg_chunk_size': sum(chunk['token_count'] for chunk in processed_chunks) / len(processed_chunks) if processed_chunks else 0,
                'chunk_size_target': self.chunk_size,
                'similarity_threshold': self.threshold
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
                errors=[f"Semantic chunking failed: {str(e)}"]
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
        
        CSV format: chunk_id, chunk_index, text, token_count, source
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
        
        # Generate output filenames (add -semantic suffix for semantic chunking)
        source_name = Path(markdown_path).stem
        json_output = output_path / f"{source_name}-semantic_chunks.json"
        csv_output = output_path / f"{source_name}-semantic_chunks.csv"
        metadata_output = output_path / f"{source_name}-semantic_metadata.json"
        
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


def chunk_document(markdown_path: str, output_dir: str, 
                  chunk_size: int = 1024, threshold: float = 0.5, 
                  embedding_model: str = "minishlab/potion-base-8M", source: str = None) -> ChunkingResult:
    """
    Convenience function to chunk any document using semantic chunking.
    
    Args:
        markdown_path: Path to the markdown document
        output_dir: Output directory for chunked files
        chunk_size: Target chunk size in tokens
        threshold: Similarity threshold for semantic chunking (0.0-1.0)
        embedding_model: Model to use for semantic embeddings
        source: Custom source identifier (defaults to filename if not provided)
        
    Returns:
        ChunkingResult with processing status and metadata
    """
    processor = GeneralSemanticChunkingProcessor(
        chunk_size=chunk_size, 
        threshold=threshold,
        embedding_model=embedding_model
    )
    return processor.process_document(markdown_path, output_dir, source)