#!/usr/bin/env python3
"""
SentinelAI Data Pipeline CLI - Restructured

This CLI provides a unified interface organized into two main categories:

1. DATABASE - For structured document processing that goes into databases
   - Regex and logic-heavy processing
   - Framework-specific extractors
   - Database-ready outputs

2. KNOWLEDGEBASE - For general document processing for RAG/vector databases
   - General-purpose chunking
   - Vector database preparation
   - Future RAG pipeline operations
"""

import click
from pathlib import Path
import sys
import time
import json
import shutil
import traceback
from typing import Dict, List, Optional

# Add current directory to path for imports
sys.path.append(str(Path(__file__).parent))

from pipelines.compliance_pipeline import CompliancePipeline
from schemas.compliance import ComplianceFramework
from processors.pdf_converter import UniversalPDFConverter, convert_pdf_to_markdown
from processors.adapters.pci_dss_adapter import PCIDSSPipelineAdapter
from processors.adapters.aws_guidance_adapter import AWSGuidancePipelineAdapter

# Import general chunking processors
from processors.chunking.general.recursive_chunking_processor import GeneralRecursiveChunkingProcessor, ChunkingResult
from processors.chunking.general.semantic_chunking_processor import GeneralSemanticChunkingProcessor
from processors.chunking.general.hierarchical_chunking_processor import GeneralHierarchicalChunkingProcessor

# Import docling converter with error handling
try:
    from processors.compliance_standards.pci_dss.core.pdf_converter_docling import PDFToMarkdownDoclingConverter
    DOCLING_AVAILABLE = True
except ImportError:
    DOCLING_AVAILABLE = False


@click.group()
def cli():
    """SentinelAI Data Pipeline - Structured and RAG-Ready Processing."""
    pass


# =============================================================================
# DATABASE COMMANDS - For structured document processing
# =============================================================================

@cli.group()
def database():
    """Process documents for structured database storage.
    
    This command group handles structured document processing with regex/logic
    for extracting specific data elements that will be stored in databases.
    
    Examples:
        python cli.py database pci-dss extract    # Extract PCI DSS controls
        python cli.py database aws-guidance       # Process AWS guidance
    """
    pass


@database.group(name='pci-dss')
def database_pci_dss():
    """PCI DSS document processing for database storage."""
    pass


@database_pci_dss.command(name='convert')
@click.option('--pdf-file', default='shared_data/documents/PCI-DSS-v4_0_1.pdf', help='Input PDF file')
@click.option('--output-file', default='PCI-DSS-v4_0_1-FULL.md', help='Output markdown file')
@click.option('--engine', type=click.Choice(['pymupdf4llm', 'docling', 'docling_vlm']), default='pymupdf4llm', help='PDF conversion engine')
@click.option('--verbose', is_flag=True, help='Enable verbose output')
def database_pci_dss_convert(pdf_file, output_file, engine, verbose):
    """Convert PCI DSS PDF to Markdown for structured processing."""
    try:
        adapter = PCIDSSPipelineAdapter()
        success = adapter.convert_pdf_to_markdown(str(pdf_file), str(output_file))
        if success:
            click.echo("🎉 PCI DSS PDF conversion completed!")
        else:
            click.echo("❌ PCI DSS PDF conversion failed!")
    except Exception as e:
        click.echo(f"❌ Error: {str(e)}")
        if verbose:
            traceback.print_exc()


@database_pci_dss.command(name='extract')
@click.option('--input-file', default='PCI-DSS-v4_0_1-FULL.md', help='Input markdown file')
@click.option('--output-dir', default='shared_data/outputs/pci_dss_v4/controls', help='Output directory for extracted controls')
@click.option('--verbose', is_flag=True, help='Enable verbose output')
def database_pci_dss_extract(input_file, output_dir, verbose):
    """Extract PCI DSS controls for database storage."""
    try:
        adapter = PCIDSSPipelineAdapter()
        result = adapter.extract_from_markdown(str(input_file), str(output_dir))
        success = result.total_controls > 0
        
        if success:
            click.echo(f"🎉 PCI DSS control extraction completed! Extracted {result.total_controls} controls.")
            if verbose:
                click.echo(f"📊 Quality Score: {result.quality_metrics.overall_score}%")
        else:
            click.echo("❌ PCI DSS control extraction failed!")
    except Exception as e:
        click.echo(f"❌ Error: {str(e)}")
        if verbose:
            traceback.print_exc()


@database_pci_dss.command(name='csv')
@click.option('--input-dir', default='shared_data/outputs/pci_dss_v4/controls', help='Input directory with extracted controls')
@click.option('--output-dir', default='shared_data/outputs/pci_dss_v4/database_import', help='CSV output directory')
@click.option('--chunk-size', type=int, default=300, help='Target chunk size in tokens')
@click.option('--verbose', is_flag=True, help='Enable verbose output')
def database_pci_dss_csv(input_dir, output_dir, chunk_size, verbose):
    """Generate database-ready CSV files from extracted controls."""
    try:
        adapter = PCIDSSPipelineAdapter()
        result = adapter.generate_csv(str(input_dir), str(output_dir), chunk_size)
        if result.success:
            click.echo("🎉 PCI DSS CSV generation completed!")
        else:
            click.echo("❌ PCI DSS CSV generation failed!")
    except Exception as e:
        click.echo(f"❌ Error: {str(e)}")
        if verbose:
            traceback.print_exc()


@database.group(name='aws-guidance')
def database_aws_guidance():
    """AWS Config guidance processing for database storage."""
    pass


@database_aws_guidance.command(name='process')
@click.option('--input-file', default='shared_data/outputs/aws_config_guidance/aws_config_rule_full_mapping.csv', help='Input CSV file')
@click.option('--output-dir', default='shared_data/outputs/aws_config_guidance/database_import', help='Output directory')
@click.option('--verbose', is_flag=True, help='Enable verbose output')
def database_aws_guidance_process(input_file, output_dir, verbose):
    """Process AWS Config Rules guidance for database import."""
    try:
        adapter = AWSGuidancePipelineAdapter()
        result = adapter.process_config_rules(input_file=input_file, output_dir=output_dir)
        
        if result.success:
            click.echo(f"✅ Successfully processed AWS Config rules")
            click.echo(f"📁 Output saved to: {output_dir}")
        else:
            click.echo("❌ Processing failed:")
            for error in result.errors:
                click.echo(f"   {error}")
    except Exception as e:
        click.echo(f"❌ Error: {str(e)}")
        if verbose:
            traceback.print_exc()


# =============================================================================
# KNOWLEDGEBASE COMMANDS - For RAG and vector database processing
# =============================================================================

@cli.group()
def knowledgebase():
    """Process documents for RAG and vector database storage.
    
    This command group handles general document processing for vector databases,
    RAG applications, and knowledge base systems.
    
    Examples:
        python cli.py knowledgebase chunk recursive document.md    # Recursive chunking
        python cli.py knowledgebase chunk semantic document.md     # Semantic chunking
        python cli.py knowledgebase embedding --input-file data.csv # Generate embeddings
    """
    pass


@knowledgebase.group(name='chunk')
def knowledgebase_chunk():
    """Chunk documents for vector database ingestion.
    
    This command group provides different chunking strategies for processing
    markdown documents for RAG applications and vector databases.
    
    Available chunking methods:
    - recursive: Traditional recursive chunking with overlap
    - semantic: Semantic chunking based on content similarity
    - hybrid: Hierarchical chunking using docling for document structure
    
    Examples:
        python cli.py knowledgebase chunk recursive --input-file document.md
        python cli.py knowledgebase chunk semantic --input-file document.md
        python cli.py knowledgebase chunk hybrid --input-file document.pdf
    """
    pass


@knowledgebase_chunk.command(name='recursive')
@click.option('--input-file', required=True, help='Input markdown file to chunk')
@click.option('--output-dir', default='shared_data/outputs/knowledgebase/chunks', help='Output directory for chunked files')
@click.option('--chunk-size', type=int, default=512, help='Target chunk size in tokens')
@click.option('--overlap', type=float, default=0.25, help='Overlap between chunks as percentage (0.25 = 25% overlap)')
@click.option('--source', help='Custom source identifier (defaults to filename if not provided)')
@click.option('--verbose', is_flag=True, help='Enable verbose output')
def knowledgebase_chunk_recursive(input_file, output_dir, chunk_size, overlap, source, verbose):
    """Chunk any document for vector database ingestion using recursive chunking.
    
    This command uses the chonkie library to perform recursive chunking of any
    markdown document with overlap refinery for better context continuity.
    Perfect for RAG applications and vector databases.
    
    Examples:
        python cli.py knowledgebase chunk recursive --input-file document.md --verbose
        python cli.py knowledgebase chunk recursive --input-file report.md --chunk-size 1024 --overlap 0.5 --source "Technical_Report"
    """
    
    try:
        processor = GeneralRecursiveChunkingProcessor(chunk_size=chunk_size, overlap=overlap)
        result = processor.process_document(str(input_file), str(output_dir), source)
        
        if result.success:
            click.echo("🎉 Document chunking completed!")
            click.echo(f"📊 Total chunks created: {result.total_chunks}")
            if verbose and result.metadata:
                click.echo(f"📁 Output directory: {output_dir}")
                click.echo(f"🔤 Average chunk size: {result.metadata.get('avg_chunk_size', 0):.1f} tokens")
                click.echo(f"📄 Total tokens: {result.metadata.get('total_tokens', 0):,}")
                if 'output_files' in result.metadata:
                    files = result.metadata['output_files']
                    if files.get('json_file'):
                        click.echo(f"📋 JSON output: {files['json_file']}")
                    if files.get('csv_file'):
                        click.echo(f"📊 CSV output: {files['csv_file']}")
        else:
            click.echo("❌ Document chunking failed!")
            for error in result.errors:
                click.echo(f"   • {error}")
                
    except Exception as e:
        click.echo(f"❌ Error: {str(e)}")
        if verbose:
            traceback.print_exc()


@knowledgebase_chunk.command(name='semantic')
@click.option('--input-file', required=True, help='Input markdown file to chunk')
@click.option('--output-dir', default='shared_data/outputs/knowledgebase/chunks', help='Output directory for chunked files')
@click.option('--chunk-size', type=int, default=1024, help='Target chunk size in tokens')
@click.option('--threshold', type=float, default=0.5, help='Similarity threshold for semantic chunking (0.0-1.0)')
@click.option('--embedding-model', default='minishlab/potion-base-8M', help='Embedding model for semantic analysis')
@click.option('--source', help='Custom source identifier (defaults to filename if not provided)')
@click.option('--verbose', is_flag=True, help='Enable verbose output')
def knowledgebase_chunk_semantic(input_file, output_dir, chunk_size, threshold, embedding_model, source, verbose):
    """Chunk any document for vector database ingestion using semantic chunking.
    
    This command uses the chonkie library to perform semantic chunking based on
    content similarity, ensuring that related content stays together. Uses
    embedding models to understand semantic relationships.
    
    Examples:
        python cli.py knowledgebase chunk semantic --input-file document.md --verbose
        python cli.py knowledgebase chunk semantic --input-file report.md --chunk-size 1024 --threshold 0.7 --source "Technical_Report"
    """
    
    try:
        processor = GeneralSemanticChunkingProcessor(
            chunk_size=chunk_size, 
            threshold=threshold,
            embedding_model=embedding_model
        )
        result = processor.process_document(str(input_file), str(output_dir), source)
        
        if result.success:
            click.echo("🎉 Semantic document chunking completed!")
            click.echo(f"📊 Total chunks created: {result.total_chunks}")
            if verbose and result.metadata:
                click.echo(f"📁 Output directory: {output_dir}")
                click.echo(f"🔤 Average chunk size: {result.metadata.get('avg_chunk_size', 0):.1f} tokens")
                click.echo(f"📄 Total tokens: {result.metadata.get('total_tokens', 0):,}")
                click.echo(f"🧠 Embedding model: {result.metadata.get('embedding_model', 'unknown')}")
                click.echo(f"🎯 Similarity threshold: {result.metadata.get('similarity_threshold', 0.5)}")
                if 'output_files' in result.metadata:
                    files = result.metadata['output_files']
                    if files.get('json_file'):
                        click.echo(f"📋 JSON output: {files['json_file']}")
                    if files.get('csv_file'):
                        click.echo(f"📊 CSV output: {files['csv_file']}")
        else:
            click.echo("❌ Semantic document chunking failed!")
            for error in result.errors:
                click.echo(f"   • {error}")
                
    except Exception as e:
        click.echo(f"❌ Error: {str(e)}")
        if verbose:
            traceback.print_exc()


@knowledgebase_chunk.command(name='hybrid')
@click.option('--input-file', required=True, help='Input PDF or markdown file to chunk')
@click.option('--output-dir', default='shared_data/outputs/knowledgebase/chunks', help='Output directory for chunked files')
@click.option('--chunk-size', type=int, default=1024, help='Target chunk size in characters')
@click.option('--enable-ocr', is_flag=True, default=True, help='Enable OCR processing for PDFs')
@click.option('--enable-table-structure', is_flag=True, default=True, help='Enable table structure recognition')
@click.option('--source', help='Custom source identifier (defaults to filename if not provided)')
@click.option('--verbose', is_flag=True, help='Enable verbose output')
def knowledgebase_chunk_hybrid(input_file, output_dir, chunk_size, enable_ocr, enable_table_structure, source, verbose):
    """Chunk documents using hierarchical/hybrid chunking with docling.
    
    This command uses docling's hierarchical chunking to create chunks that
    preserve document structure and context. It works best with PDF documents
    where document structure can be analyzed, but also supports markdown files.
    
    Features:
    - Preserves document hierarchy and heading context
    - Maintains structural relationships between sections
    - Uses docling's advanced PDF analysis for structure detection
    - Includes parent section context in each chunk
    - Supports both PDF and markdown input files
    
    Examples:
        python cli.py knowledgebase chunk hybrid --input-file document.pdf --verbose
        python cli.py knowledgebase chunk hybrid --input-file report.pdf --chunk-size 2048 --source "Technical_Report"
        python cli.py knowledgebase chunk hybrid --input-file document.md --enable-ocr=false --verbose
    """
    
    try:
        processor = GeneralHierarchicalChunkingProcessor(
            chunk_size=chunk_size,
            enable_ocr=enable_ocr,
            enable_table_structure=enable_table_structure
        )
        result = processor.process_document(str(input_file), str(output_dir), source)
        
        if result.success:
            click.echo("🎉 Hierarchical document chunking completed!")
            click.echo(f"📊 Total chunks created: {result.total_chunks}")
            if verbose and result.metadata:
                click.echo(f"📁 Output directory: {output_dir}")
                click.echo(f"🔤 Average chunk size: {result.metadata.get('avg_chunk_size', 0):.1f} tokens")
                click.echo(f"📄 Total tokens: {result.metadata.get('total_tokens', 0):,}")
                click.echo(f"🏗️ Chunking method: {result.metadata.get('chunking_method', 'unknown')}")
                click.echo(f"📚 Document type: {result.metadata.get('document_type', 'unknown')}")
                
                # Show structural features
                structural_features = result.metadata.get('structural_features', {})
                click.echo(f"🔍 OCR enabled: {structural_features.get('ocr_enabled', False)}")
                click.echo(f"📋 Table structure: {structural_features.get('table_structure_enabled', False)}")
                click.echo(f"🧭 Hierarchical context: {structural_features.get('hierarchical_context', False)}")
                
                if 'output_files' in result.metadata:
                    files = result.metadata['output_files']
                    if files.get('json_file'):
                        click.echo(f"📋 JSON output: {files['json_file']}")
                    if files.get('csv_file'):
                        click.echo(f"📊 CSV output: {files['csv_file']}")
        else:
            click.echo("❌ Hierarchical document chunking failed!")
            for error in result.errors:
                click.echo(f"   • {error}")
                
    except Exception as e:
        click.echo(f"❌ Error: {str(e)}")
        if verbose:
            traceback.print_exc()


# =============================================================================
# EMBEDDING COMMANDS - For generating embeddings from text data
# =============================================================================

@knowledgebase.command(name='embedding')
@click.option('--input-file', required=True, help='Input CSV file with text data')
@click.option('--output-dir', default='shared_data/outputs/knowledgebase/embeddings', help='Output directory for embedding files')
@click.option('--model-name', default='BAAI/bge-m3', help='Embedding model name')
@click.option('--batch-size', type=int, default=32, help='Batch size for processing')
@click.option('--use-chonkie', is_flag=True, default=True, help='Use Chonkie embedding implementation')
@click.option('--verbose', is_flag=True, help='Enable verbose output')
def knowledgebase_embedding(input_file, output_dir, model_name, batch_size, use_chonkie, verbose):
    """Generate embeddings from CSV text data using baai/bge-m3 or custom models.
    
    This command processes CSV files with a 'text' column and generates embeddings
    using the specified model. Supports both Chonkie and SentenceTransformers implementations.
    
    Examples:
        python cli.py knowledgebase embedding --input-file chunks.csv --verbose
        python cli.py knowledgebase embedding --input-file data.csv --model-name "sentence-transformers/all-MiniLM-L6-v2" --batch-size 16
        python cli.py knowledgebase embedding --input-file data.csv --use-chonkie --verbose
    """
    try:
        from processors.embedding.embedding_processor import EmbeddingProcessor
        
        if verbose:
            click.echo(f"🚀 Starting embedding generation...")
            click.echo(f"📄 Input file: {input_file}")
            click.echo(f"📁 Output directory: {output_dir}")
            click.echo(f"🤖 Model: {model_name}")
            click.echo(f"📦 Batch size: {batch_size}")
            click.echo(f"🔧 Implementation: {'Chonkie' if use_chonkie else 'SentenceTransformers'}")
        
        processor = EmbeddingProcessor(model_name=model_name, use_chonkie=use_chonkie)
        
        if verbose:
            model_info = processor.get_model_info()
            click.echo(f"📊 Model info: {model_info}")
        
        result = processor.process_csv(str(input_file), str(output_dir), batch_size)
        
        if result.success:
            click.echo("🎉 Embedding generation completed!")
            click.echo(f"📊 Total embeddings created: {result.total_embeddings}")
            if verbose and result.metadata:
                click.echo(f"📁 Output file: {result.output_file}")
                click.echo(f"📏 Embedding dimension: {result.metadata.get('embedding_dimension', 'unknown')}")
                click.echo(f"🔤 Processed rows: {result.metadata.get('processed_row_count', 0)}")
                click.echo(f"⚠️  Filtered out: {result.metadata.get('filtered_out_count', 0)}")
                click.echo(f"📊 Processing time: {result.metadata.get('processed_at', 'unknown')}")
        else:
            click.echo("❌ Embedding generation failed!")
            for error in result.errors:
                click.echo(f"   • {error}")
                
    except ImportError as e:
        click.echo(f"❌ Import error: {str(e)}")
        click.echo("💡 Try: pip install 'chonkie[semantic,st]' or pip install sentence-transformers")
    except Exception as e:
        click.echo(f"❌ Error: {str(e)}")
        if verbose:
            traceback.print_exc()


# =============================================================================
# LEGACY COMMANDS - For backward compatibility
# =============================================================================

@cli.group()
def convert():
    """Convert documents between formats."""
    pass


@convert.command(name='pdf-to-md')
@click.option('--pdf-file', required=True, help='Input PDF file path')
@click.option('--output-file', help='Output markdown file path (optional)')
@click.option('--engine', type=click.Choice(['pymupdf4llm', 'docling', 'docling_vlm']), default='pymupdf4llm', help='PDF conversion engine')
@click.option('--verbose', is_flag=True, help='Enable verbose output')
def convert_pdf_to_markdown_cmd(pdf_file, output_file, engine, verbose):
    """Convert PDF to Markdown using pymupdf4llm, docling, or docling_vlm."""
    try:
        converter = UniversalPDFConverter()
        result = converter.convert_with_metadata(
            pdf_path=pdf_file,
            output_path=output_file,
            engine=engine,
            processor_type='generic'
        )
        
        click.echo(f"✅ PDF to Markdown conversion completed successfully with {engine}!")
        click.echo(f"📊 Generated {len(result['content']):,} characters of markdown")
        if output_file:
            click.echo(f"📝 Saved to: {output_file}")
                
    except Exception as e:
        click.echo(f"❌ Conversion failed: {str(e)}")
        if verbose:
            traceback.print_exc()


@convert.command(name='image-describe')
@click.option('--image-file', required=True, help='Input image file path')
@click.option('--output-file', help='Output markdown file path (optional)')
@click.option('--vision-model', type=click.Choice(['granite_vision', 'smolvlm']), default='granite_vision', help='Vision Language Model to use')
@click.option('--custom-prompt', help='Custom prompt for image description')
@click.option('--verbose', is_flag=True, help='Enable verbose output')
def convert_image_describe_cmd(image_file, output_file, vision_model, custom_prompt, verbose):
    """Describe image content using Vision Language Model (VLM)."""
    try:
        # Import VLM engine
        from processors.pdf_converter.engines.docling_vlm_engine import DoclingVLMEngine
        
        # Configure VLM engine
        engine_config = {
            'enable_picture_description': True,
            'vision_model': vision_model,
            'enable_ocr': False,  # Focus on image description
            'enable_table_structure': False
        }
        
        if custom_prompt:
            engine_config['picture_description_prompt'] = custom_prompt
        
        # Initialize VLM engine
        if not DoclingVLMEngine.is_available():
            click.echo("❌ Docling VLM not available. Install with: pip install 'docling[vlm]'")
            return
        
        if not DoclingVLMEngine.is_vlm_available():
            click.echo("❌ VLM features not available. Install with: pip install 'docling[vlm]'")
            return
        
        engine = DoclingVLMEngine(**engine_config)
        
        # Process image
        click.echo(f"🔄 Describing image with {vision_model}: {image_file}")
        result = engine.convert_image_only(image_file)
        
        # Save result if output file specified
        if output_file:
            from pathlib import Path
            Path(output_file).write_text(result, encoding='utf-8')
            click.echo(f"📝 Description saved to: {output_file}")
        else:
            click.echo("📝 Image Description:")
            click.echo("-" * 40)
            click.echo(result)
        
        click.echo("✅ Image description completed!")
        
    except Exception as e:
        click.echo(f"❌ Image description failed: {str(e)}")
        if verbose:
            traceback.print_exc()


@cli.command()
def status():
    """Show current pipeline status and statistics."""
    try:
        pipeline = CompliancePipeline()
        
        click.echo("📊 Pipeline Status")
        click.echo("=" * 30)
        
        # Show supported frameworks
        frameworks = pipeline.get_supported_frameworks()
        click.echo(f"🎯 Supported frameworks: {len(frameworks)}")
        for fw in frameworks:
            click.echo(f"   • {fw}")
        
        # Show extraction statistics
        stats = pipeline.get_extraction_statistics()
        
        if stats:
            click.echo("\n📈 Database Processing Statistics:")
            for framework, data in stats.items():
                click.echo(f"\n{framework.upper()}:")
                click.echo(f"   📄 Markdown files: {data['markdown_files']}")
                click.echo(f"   📋 JSON files: {data['json_files']}")
                click.echo(f"   📊 CSV files: {data['csv_files']}")
                click.echo(f"   ⏰ Status: {data['last_extraction']}")
        else:
            click.echo("\n📭 No database extractions found.")
            
        # Show knowledgebase processing
        kb_chunks_dir = Path("shared_data/outputs/knowledgebase/chunks")
        if kb_chunks_dir.exists():
            csv_files = list(kb_chunks_dir.glob("*.csv"))
            json_files = list(kb_chunks_dir.glob("*.json"))
            click.echo(f"\n🧠 Knowledgebase Processing:")
            click.echo(f"   📊 Chunk CSV files: {len(csv_files)}")
            click.echo(f"   📋 Chunk JSON files: {len(json_files)}")
        else:
            click.echo("\n🧠 No knowledgebase processing found.")
            
    except Exception as e:
        click.echo(f"❌ Status error: {str(e)}")


if __name__ == '__main__':
    cli()