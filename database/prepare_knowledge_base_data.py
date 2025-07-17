#!/usr/bin/env python3
"""
Data preparation script for knowledge base insertion
Processes parquet files and metadata JSON files to prepare data for Supabase insertion
"""

from pathlib import Path
from typing import Dict, List, Any
from uuid import uuid4
from json import load, dump
from logging import getLogger, basicConfig, INFO

import pandas as pd
import numpy as np

basicConfig(level=INFO)
logger = getLogger(__name__)

class KnowledgeBaseDataPreparator:
    """Prepares knowledge base data for insertion into Supabase"""
    
    def __init__(self, data_dir: str = "shared_data/outputs/knowledgebase/embeddings"):
        # Handle both relative and absolute paths
        if Path(data_dir).is_absolute():
            self.data_dir = Path(data_dir)
        else:
            # For relative paths, resolve from the project root
            script_dir = Path(__file__).parent
            project_root = script_dir.parent
            self.data_dir = project_root / data_dir
        
        self.output_dir = self.data_dir / "prepared_data"
        
        # Verify source directory exists
        if not self.data_dir.exists():
            logger.error(f"Source data directory does not exist: {self.data_dir}")
            raise FileNotFoundError(f"Source data directory not found: {self.data_dir}")
        
        # Create output directory with parents if it doesn't exist
        try:
            self.output_dir.mkdir(parents=True, exist_ok=True)
            logger.info(f"Using output directory: {self.output_dir}")
        except Exception as e:
            logger.error(f"Failed to create output directory {self.output_dir}: {e}")
            raise
        
    def load_document_metadata(self, metadata_file: Path) -> Dict[str, Any]:
        """Load and parse document metadata from JSON file, preserving all keys"""
        try:
            with open(metadata_file, 'r') as f:
                metadata = load(f)
            
            # Keep the complete metadata structure but also extract flattened attributes
            attrs = metadata.get('metadataAttributes', {})
            parsed_metadata = {
                'original_metadata': metadata,  # Preserve complete original structure
                'metadata_attributes': attrs    # Keep structured attributes
            }
            
            # Flatten common attributes for easier querying
            for key, value_obj in attrs.items():
                value = value_obj.get('value', {})
                if value.get('type') == 'STRING':
                    parsed_metadata[key] = value.get('stringValue', '')
                elif value.get('type') == 'STRING_LIST':
                    parsed_metadata[key] = value.get('stringListValue', [])
                    
            return parsed_metadata
            
        except Exception as e:
            logger.error(f"Failed to load metadata from {metadata_file}: {e}")
            return {}
    
    def process_parquet_file(self, parquet_file: Path, metadata: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Process a single parquet file and prepare records for insertion (simplified to text + embedding only)"""
        try:
            # Load parquet file
            df = pd.read_parquet(parquet_file)
            logger.info(f"Loaded {len(df)} rows from {parquet_file.name}")
            
            # Verify required columns exist
            required_columns = ['text', 'embedding']
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                logger.error(f"Missing required columns in {parquet_file.name}: {missing_columns}")
                return []
            
            # Prepare records for insertion
            records = []
            
            for _, row in df.iterrows():
                # Convert numpy array to list for JSON serialization
                embedding = row['embedding'].tolist() if isinstance(row['embedding'], np.ndarray) else row['embedding']
                
                # Extract source document name from parquet filename
                source_document = parquet_file.stem.replace('_chunks_embeddings', '')
                
                # Combine all metadata (document-level + processing metadata)
                combined_metadata = {
                    # Document-level metadata (all keys preserved)
                    **metadata,
                    # Processing metadata
                    'source_document': source_document,
                    'source_file': parquet_file.name,
                    'embedding_dimension': len(embedding),
                    'model_name': 'BAAI/bge-m3',
                    'embedding_implementation': 'sentence_transformers'
                }
                
                record = {
                    'uuid': str(uuid4()),
                    'content': row['text'],  # text column becomes content
                    'embedding': embedding,
                    'metadata': combined_metadata
                }
                
                records.append(record)
            
            return records
            
        except Exception as e:
            logger.error(f"Failed to process {parquet_file}: {e}")
            return []
    
    def prepare_all_data(self) -> Dict[str, Any]:
        """Process all parquet files and prepare complete dataset"""
        all_records = []
        processing_stats = {
            'total_files': 0,
            'processed_files': 0,
            'total_records': 0,
            'failed_files': [],
            'file_stats': []
        }
        
        # Find all parquet files
        parquet_files = list(self.data_dir.glob("*_chunks_embeddings.parquet"))
        processing_stats['total_files'] = len(parquet_files)
        
        logger.info(f"Found {len(parquet_files)} parquet files to process")
        
        for parquet_file in parquet_files:
            try:
                # Find corresponding metadata file
                base_name = parquet_file.stem.replace('_chunks_embeddings', '')
                # Remove additional suffixes that might be present
                base_name = base_name.replace('-pic-annot', '').replace('-docling', '')
                metadata_file = self.data_dir / f"{base_name}.extension.metadata.json"
                
                if not metadata_file.exists():
                    logger.warning(f"Metadata file not found for {parquet_file.name}")
                    metadata = {}
                else:
                    metadata = self.load_document_metadata(metadata_file)
                
                # Process the parquet file
                records = self.process_parquet_file(parquet_file, metadata)
                
                if records:
                    all_records.extend(records)
                    processing_stats['processed_files'] += 1
                    processing_stats['file_stats'].append({
                        'file': parquet_file.name,
                        'records': len(records),
                        'metadata_found': metadata_file.exists()
                    })
                    logger.info(f"Processed {parquet_file.name}: {len(records)} records")
                else:
                    processing_stats['failed_files'].append(parquet_file.name)
                    
            except Exception as e:
                logger.error(f"Failed to process {parquet_file}: {e}")
                processing_stats['failed_files'].append(parquet_file.name)
        
        processing_stats['total_records'] = len(all_records)
        
        return {
            'records': all_records,
            'stats': processing_stats
        }
    
    def save_prepared_data(self, data: Dict[str, Any], batch_size: int = 1000) -> List[Path]:
        """Save prepared data to JSON files in batches"""
        records = data['records']
        stats = data['stats']
        
        # Save processing statistics
        stats_file = self.output_dir / "processing_stats.json"
        with open(stats_file, 'w') as f:
            dump(stats, f, indent=2)
        
        # Save records in batches
        batch_files = []
        total_batches = (len(records) + batch_size - 1) // batch_size
        
        for i in range(0, len(records), batch_size):
            batch_num = i // batch_size + 1
            batch_records = records[i:i + batch_size]
            
            batch_file = self.output_dir / f"knowledge_base_batch_{batch_num:03d}.json"
            with open(batch_file, 'w') as f:
                dump(batch_records, f, indent=2)
            
            batch_files.append(batch_file)
            logger.info(f"Saved batch {batch_num}/{total_batches}: {len(batch_records)} records")
        
        # Save complete dataset (for smaller datasets)
        if len(records) <= 5000:  # Only save complete file for smaller datasets
            complete_file = self.output_dir / "knowledge_base_complete.json"
            with open(complete_file, 'w') as f:
                dump(records, f, indent=2)
            logger.info(f"Saved complete dataset: {len(records)} records")
        
        return batch_files
    
    def generate_sql_insert_script(self, batch_files: List[Path]) -> Path:
        """Generate SQL script for batch insertion"""
        sql_file = self.output_dir / "insert_knowledge_base.sql"
        
        with open(sql_file, 'w') as f:
            f.write("-- Generated SQL script for knowledge base insertion\n")
            f.write("-- Run this script in your Supabase SQL editor\n\n")
            
            f.write("-- Ensure required extensions are enabled\n")
            f.write("CREATE EXTENSION IF NOT EXISTS vector;\n")
            f.write("CREATE EXTENSION IF NOT EXISTS pg_trgm;\n\n")
            
            f.write("-- Clear existing knowledge base data (uncomment if needed)\n")
            f.write("-- DELETE FROM knowledge_base;\n\n")
            
            f.write("-- Insert data in batches\n")
            f.write("-- Note: You'll need to use the JSON files with a PostgreSQL client\n")
            f.write("-- that supports JSON import, or use the CLI tool provided\n\n")
            
            for i, batch_file in enumerate(batch_files, 1):
                f.write(f"-- Batch {i}: {batch_file.name}\n")
                f.write(f"-- Use: python -m database.cli data import-kb --batch-file {batch_file.name}\n\n")
        
        return sql_file
    
    def run(self, batch_size: int = 1000) -> Dict[str, Any]:
        """Main execution method"""
        logger.info("Starting knowledge base data preparation...")
        
        # Prepare all data
        data = self.prepare_all_data()
        
        # Save prepared data
        batch_files = self.save_prepared_data(data, batch_size)
        
        # Generate SQL script
        sql_file = self.generate_sql_insert_script(batch_files)
        
        # Summary
        stats = data['stats']
        logger.info(f"Data preparation completed!")
        logger.info(f"  Total files processed: {stats['processed_files']}/{stats['total_files']}")
        logger.info(f"  Total records prepared: {stats['total_records']}")
        logger.info(f"  Batch files created: {len(batch_files)}")
        logger.info(f"  Output directory: {self.output_dir}")
        
        return {
            'batch_files': batch_files,
            'sql_file': sql_file,
            'stats': stats,
            'output_dir': self.output_dir
        }

def main():
    """Main function for standalone execution"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Prepare knowledge base data for Supabase insertion")
    parser.add_argument("--data-dir", default="shared_data/outputs/knowledgebase/embeddings", 
                       help="Directory containing parquet and metadata files")
    parser.add_argument("--batch-size", type=int, default=1000, 
                       help="Number of records per batch file")
    
    args = parser.parse_args()
    
    preparator = KnowledgeBaseDataPreparator(args.data_dir)
    result = preparator.run(args.batch_size)
    
    print(f"\n✅ Data preparation completed successfully!")
    print(f"📁 Output directory: {result['output_dir']}")
    print(f"📊 Total records: {result['stats']['total_records']}")
    print(f"📦 Batch files: {len(result['batch_files'])}")
    print(f"💾 SQL script: {result['sql_file']}")
    print(f"\n🚀 Next steps:")
    print(f"   1. Run the SQL table creation script in Supabase")
    print(f"   2. Use the CLI tool to import data: python -m database.cli data import-kb")

if __name__ == "__main__":
    main()