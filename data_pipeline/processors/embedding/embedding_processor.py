"""
Embedding Processor for Document Text Vectorization

This processor takes CSV files with text data and generates embeddings using various models.
It supports both SentenceTransformers and Chonkie's embedding capabilities with the baai/bge-m3 model.

The processor:
1. Loads CSV files using pandas
2. Extracts text from the 'text' column
3. Generates embeddings using the specified model
4. Adds embeddings to the dataframe
5. Saves the result as a parquet file to preserve vector data
"""

from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime
import pandas as pd
import numpy as np
import json

try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False

try:
    from chonkie import SentenceTransformerEmbeddings
    CHONKIE_AVAILABLE = True
except ImportError:
    CHONKIE_AVAILABLE = False


class EmbeddingResult:
    """Result object for embedding operations."""
    
    def __init__(self, success: bool, total_embeddings: int = 0, 
                 output_file: str = None, metadata: Dict = None, 
                 errors: List[str] = None):
        self.success = success
        self.total_embeddings = total_embeddings
        self.output_file = output_file
        self.metadata = metadata or {}
        self.errors = errors or []


class EmbeddingProcessor:
    """
    Processor for generating embeddings from CSV text data.
    
    This processor loads CSV files, extracts text from the 'text' column,
    generates embeddings using the specified model, and saves the results
    as parquet files with the embeddings added as a new column.
    """
    
    def __init__(self, model_name: str = "BAAI/bge-m3", use_chonkie: bool = True):
        """
        Initialize the embedding processor.
        
        Args:
            model_name: Name of the embedding model to use
            use_chonkie: Whether to use Chonkie's embedding implementation
        """
        self.model_name = model_name
        self.use_chonkie = use_chonkie
        self.model = None
        
        # Initialize the appropriate embedding model
        if use_chonkie and CHONKIE_AVAILABLE:
            try:
                self.model = SentenceTransformerEmbeddings(model_name=model_name)
            except Exception as e:
                if SENTENCE_TRANSFORMERS_AVAILABLE:
                    print(f"Warning: Chonkie initialization failed ({e}), falling back to SentenceTransformers")
                    self.use_chonkie = False
                    self.model = SentenceTransformer(model_name)
                else:
                    raise ImportError(f"Neither Chonkie nor SentenceTransformers available: {e}")
        elif SENTENCE_TRANSFORMERS_AVAILABLE:
            self.use_chonkie = False
            self.model = SentenceTransformer(model_name)
        else:
            raise ImportError(
                "Neither Chonkie nor SentenceTransformers available. "
                "Install with: pip install 'chonkie[semantic,st]' or pip install sentence-transformers"
            )
    
    def load_csv(self, csv_path: str) -> pd.DataFrame:
        """
        Load CSV file into a pandas DataFrame.
        
        Args:
            csv_path: Path to the CSV file
            
        Returns:
            DataFrame with the CSV data
        """
        path = Path(csv_path)
        if not path.exists():
            raise FileNotFoundError(f"CSV file not found: {csv_path}")
        
        try:
            df = pd.read_csv(csv_path)
            return df
        except Exception as e:
            raise ValueError(f"Failed to load CSV file: {e}")
    
    def validate_csv_structure(self, df: pd.DataFrame) -> bool:
        """
        Validate that the DataFrame has the required 'text' column.
        
        Args:
            df: DataFrame to validate
            
        Returns:
            True if valid, raises ValueError if not
        """
        if 'text' not in df.columns:
            raise ValueError("CSV file must contain a 'text' column")
        
        # Check for empty or null text values
        empty_count = df['text'].isna().sum() + (df['text'] == '').sum()
        if empty_count > 0:
            print(f"Warning: Found {empty_count} empty text entries")
        
        return True
    
    def generate_embeddings(self, texts: List[str]) -> np.ndarray:
        """
        Generate embeddings for the provided texts.
        
        Args:
            texts: List of texts to embed
            
        Returns:
            NumPy array of embeddings
        """
        if not texts:
            return np.array([])
        
        try:
            if self.use_chonkie:
                # Use Chonkie's embedding method
                embeddings = self.model.embed(texts)
            else:
                # Use SentenceTransformers directly
                embeddings = self.model.encode(texts)
            
            return embeddings
        except Exception as e:
            raise RuntimeError(f"Failed to generate embeddings: {e}")
    
    def process_csv(self, csv_path: str, output_dir: str, 
                   batch_size: int = 32) -> EmbeddingResult:
        """
        Process a CSV file to generate embeddings.
        
        Args:
            csv_path: Path to the input CSV file
            output_dir: Directory to save the output parquet file
            batch_size: Number of texts to process in each batch
            
        Returns:
            EmbeddingResult with processing status and metadata
        """
        try:
            # Load and validate CSV
            df = self.load_csv(csv_path)
            self.validate_csv_structure(df)
            
            # Filter out empty/null text entries
            original_count = len(df)
            df = df.dropna(subset=['text'])
            df = df[df['text'].str.strip() != '']
            filtered_count = len(df)
            
            if filtered_count == 0:
                return EmbeddingResult(
                    success=False,
                    errors=["No valid text entries found in CSV"]
                )
            
            # Extract texts for embedding
            texts = df['text'].tolist()
            
            # Generate embeddings in batches
            all_embeddings = []
            for i in range(0, len(texts), batch_size):
                batch_texts = texts[i:i + batch_size]
                batch_embeddings = self.generate_embeddings(batch_texts)
                all_embeddings.append(batch_embeddings)
            
            # Concatenate all embeddings
            if all_embeddings:
                embeddings_array = np.vstack(all_embeddings)
            else:
                embeddings_array = np.array([])
            
            # Add embeddings to dataframe
            df['embedding'] = embeddings_array.tolist()
            
            # Create output directory and file path
            output_path = Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)
            
            # Generate output filename
            input_stem = Path(csv_path).stem
            output_file = output_path / f"{input_stem}_embeddings.parquet"
            
            # Save as parquet to preserve vector data
            df.to_parquet(output_file, index=False)
            
            # Generate metadata
            metadata = {
                'source_file': csv_path,
                'output_file': str(output_file),
                'model_name': self.model_name,
                'embedding_implementation': 'chonkie' if self.use_chonkie else 'sentence_transformers',
                'processed_at': datetime.now().isoformat(),
                'original_row_count': original_count,
                'processed_row_count': filtered_count,
                'filtered_out_count': original_count - filtered_count,
                'embedding_dimension': embeddings_array.shape[1] if embeddings_array.size > 0 else 0,
                'batch_size': batch_size,
                'total_embeddings': filtered_count
            }
            
            # Save metadata
            metadata_file = output_path / f"{input_stem}_embedding_metadata.json"
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
            
            return EmbeddingResult(
                success=True,
                total_embeddings=filtered_count,
                output_file=str(output_file),
                metadata=metadata
            )
            
        except Exception as e:
            return EmbeddingResult(
                success=False,
                errors=[f"Embedding processing failed: {str(e)}"]
            )
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Get information about the loaded model.
        
        Returns:
            Dictionary with model information
        """
        info = {
            'model_name': self.model_name,
            'implementation': 'chonkie' if self.use_chonkie else 'sentence_transformers',
            'model_loaded': self.model is not None
        }
        
        if self.model is not None:
            try:
                # Try to get embedding dimension by encoding a test string
                test_embedding = self.generate_embeddings(['test'])
                info['embedding_dimension'] = test_embedding.shape[1] if test_embedding.size > 0 else 0
            except Exception:
                info['embedding_dimension'] = 'unknown'
        
        return info


def process_csv_embeddings(csv_path: str, output_dir: str, 
                          model_name: str = "BAAI/bge-m3",
                          use_chonkie: bool = True,
                          batch_size: int = 32) -> EmbeddingResult:
    """
    Convenience function to process CSV files for embeddings.
    
    Args:
        csv_path: Path to the input CSV file
        output_dir: Directory to save output files
        model_name: Name of the embedding model to use
        use_chonkie: Whether to use Chonkie's embedding implementation
        batch_size: Number of texts to process in each batch
        
    Returns:
        EmbeddingResult with processing status and metadata
    """
    processor = EmbeddingProcessor(model_name=model_name, use_chonkie=use_chonkie)
    return processor.process_csv(csv_path, output_dir, batch_size)