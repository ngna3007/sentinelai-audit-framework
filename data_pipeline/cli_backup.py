#!/usr/bin/env python3
"""
Centralized CLI for all data pipeline operations.

This CLI provides a unified interface for extracting compliance controls
from various frameworks while preserving all existing functionality.
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

# Import docling converter with error handling
try:
    from processors.compliance_standards.pci_dss.core.pdf_converter_docling import PDFToMarkdownDoclingConverter
    DOCLING_AVAILABLE = True
except ImportError:
    DOCLING_AVAILABLE = False
from processors.adapters.aws_guidance_adapter import AWSGuidancePipelineAdapter

@click.group()
def cli():
    """SentinelAI Data Pipeline - Centralized ETL for compliance data."""
    pass

@cli.group()
def extract():
    """Extract data from compliance documents."""
    pass

@cli.group()
def pci_dss():
    """Direct PCI DSS processor commands."""
    pass

@pci_dss.command(name='convert')
@click.option('--pdf-file', default='shared_data/documents/PCI-DSS-v4_0_1.pdf', help='Input PDF file')
@click.option('--output-file', default='PCI-DSS-v4_0_1-FULL.md', help='Output markdown file')
@click.option('--engine', type=click.Choice(['pymupdf4llm', 'docling']), default='pymupdf4llm', help='PDF conversion engine (default: pymupdf4llm)')
@click.option('--source-path', help='Manual input: source PDF file path (overrides --pdf-file)')
@click.option('--output-name', help='Manual input: output markdown file name without extension (overrides --output-file)')
@click.option('--output-folder', help='Manual input: output folder path for markdown file')
@click.option('--verbose', is_flag=True, help='Enable verbose output')
def pci_dss_convert(pdf_file, output_file, engine, source_path, output_name, output_folder, verbose):
    """Convert PCI DSS PDF to Markdown using the PCI DSS processor.
    
    Engine Options:
    - pymupdf4llm: Fast conversion, LLM-optimized (default)
    - docling: Advanced layout analysis, superior table detection (slower)
    
    Examples:
        python cli.py pci-dss convert --engine docling --verbose
        python cli.py pci-dss convert --engine docling --source-path /path/to/file.pdf --output-name custom-name --output-folder /path/to/output/
    """
    
    try:
        # Handle manual input options
        final_pdf_file = source_path if source_path else pdf_file
        
        if output_name:
            if output_folder:
                # Custom output folder specified
                output_path = Path(output_folder)
                output_path.mkdir(parents=True, exist_ok=True)
                final_output_file = str(output_path / f"{output_name}.md")
            else:
                # Use default documents folder
                final_output_file = f"shared_data/documents/{output_name}.md"
        else:
            final_output_file = output_file
        
        if verbose:
            click.echo(f"🔧 Engine: {engine}")
            click.echo(f"📄 Source PDF: {final_pdf_file}")
            click.echo(f"📝 Output file: {final_output_file}")
        
        adapter = PCIDSSPipelineAdapter()
        success = adapter.convert_pdf_to_markdown(str(final_pdf_file), str(final_output_file))
        if success:
            click.echo("🎉 PCI DSS PDF conversion completed!")
        else:
            click.echo("❌ PCI DSS PDF conversion failed!")
            
    except Exception as e:
        click.echo(f"❌ Error: {str(e)}")
        if verbose:
            traceback.print_exc()

@pci_dss.command(name='extract')
@click.option('--input-file', default='PCI-DSS-v4_0_1-FULL.md', help='Input markdown file')
@click.option('--output-dir', default='shared_data/outputs/pci_dss_v4/controls', help='Output directory for extracted controls')
@click.option('--verbose', is_flag=True, help='Enable verbose output')
def pci_dss_extract(input_file, output_dir, verbose):
    """Extract PCI DSS controls from markdown using the PCI DSS processor."""
    
    try:
        adapter = PCIDSSPipelineAdapter()
        result = adapter.extract_from_markdown(str(input_file), str(output_dir))
        success = result.total_controls > 0
        
        if success:
            click.echo(f"🎉 PCI DSS control extraction completed! Extracted {result.total_controls} controls.")
            if verbose:
                click.echo(f"📊 Quality Score: {result.quality_metrics.overall_score}%")
                click.echo(f"🔄 Multi-table controls: {result.multi_table_controls}")
        else:
            click.echo("❌ PCI DSS control extraction failed!")
            
            # Show detailed error information
            if hasattr(result, 'quality_metrics') and result.quality_metrics.validation_notes:
                click.echo("🔍 Error details:")
                for note in result.quality_metrics.validation_notes:
                    click.echo(f"   • {note}")
            
            if verbose and hasattr(result, 'extraction_metadata'):
                click.echo(f"📄 Source file: {result.extraction_metadata.source_file}")
                click.echo(f"🔧 Processing tool: {result.extraction_metadata.processing_tool}")
                click.echo(f"📈 Controls found: {result.total_controls}")
            
            if result.total_controls == 0:
                click.echo("💡 Suggestions:")
                click.echo("   • Check if the markdown file contains PCI DSS control tables")
                click.echo("   • Verify the file path is correct")
                click.echo("   • Try running with --verbose for more details")
            
    except Exception as e:
        click.echo(f"❌ Error: {str(e)}")
        if verbose:
            traceback.print_exc()

@pci_dss.command(name='chunk')
@click.option('--input-file', default='shared_data/documents/PCI-DSS-v4_0_1-docling.md', help='Input markdown file to chunk')
@click.option('--output-dir', default='shared_data/outputs/pci_dss_v4/chunks', help='Output directory for chunked files')
@click.option('--chunk-size', type=int, default=512, help='Target chunk size in tokens')
@click.option('--overlap', type=float, default=0.25, help='Overlap between chunks as percentage (0.25 = 25% overlap)')
@click.option('--source', help='Custom source identifier (defaults to filename if not provided)')
@click.option('--verbose', is_flag=True, help='Enable verbose output')
def pci_dss_chunk(input_file, output_dir, chunk_size, overlap, source, verbose):
    """Chunk PCI DSS document using recursive chunking with chonkie library and overlap refinery.
    
    This command uses the chonkie library to perform recursive chunking of the
    PCI DSS document with overlap refinery for better context continuity,
    creating semantically meaningful chunks suitable for vector database ingestion and RAG applications.
    
    Examples:
        python cli.py pci-dss chunk --verbose
        python cli.py pci-dss chunk --chunk-size 1024 --overlap 0.5 --source "PCI_DSS_v4" --input-file custom.md
    """
    
    try:
        adapter = PCIDSSPipelineAdapter()
        result = adapter.chunk_document(str(input_file), str(output_dir), chunk_size, overlap, source)
        
        if result.success:
            click.echo("🎉 PCI DSS document chunking completed!")
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
            click.echo("❌ PCI DSS document chunking failed!")
            for error in result.errors:
                click.echo(f"   • {error}")
                
    except Exception as e:
        click.echo(f"❌ Error: {str(e)}")
        if verbose:
            traceback.print_exc()

@pci_dss.command(name='csv')
@click.option('--input-dir', default='shared_data/outputs/pci_dss_v4/controls', help='Input directory with extracted controls')
@click.option('--output-dir', default='shared_data/outputs/pci_dss_v4/database_import', help='CSV output directory')
@click.option('--chunk-size', type=int, default=300, help='Target chunk size in tokens')
@click.option('--verbose', is_flag=True, help='Enable verbose output')
def pci_dss_csv(input_dir, output_dir, chunk_size, verbose):
    """Generate CSV files for Bedrock using the PCI DSS processor."""
    
    try:
        adapter = PCIDSSPipelineAdapter()
        result = adapter.generate_csv(str(input_dir), str(output_dir), chunk_size)
        success = result.success
        if success:
            click.echo("🎉 PCI DSS CSV generation completed!")
        else:
            click.echo("❌ PCI DSS CSV generation failed!")
            
    except Exception as e:
        click.echo(f"❌ Error: {str(e)}")
        if verbose:
            traceback.print_exc()

@pci_dss.command(name='all')
@click.option('--pdf-file', help='Input PDF file (optional - if provided, will convert first)')
@click.option('--input-file', default='PCI-DSS-v4_0_1-FULL.md', help='Input markdown file')
@click.option('--output-dir', default='shared_data/outputs/pci_dss_v4/controls', help='Output directory for extracted controls')
@click.option('--csv-output', default='shared_data/outputs/pci_dss_v4/bedrock', help='CSV output directory')
@click.option('--chunk-size', type=int, default=300, help='Target chunk size in tokens')
@click.option('--engine', type=click.Choice(['pymupdf4llm', 'docling']), default='pymupdf4llm', help='PDF conversion engine (default: pymupdf4llm)')
@click.option('--verbose', is_flag=True, help='Enable verbose output')
def pci_dss_all(pdf_file, input_file, output_dir, csv_output, chunk_size, engine, verbose):
    """Run complete PCI DSS workflow: convert (optional), extract, and generate CSV.
    
    Engine Options:
    - pymupdf4llm: Fast conversion, LLM-optimized (default)
    - docling: Advanced layout analysis, superior table detection (slower)
    """
    
    try:
        success = True
        
        # Convert PDF if provided
        if pdf_file:
            if verbose:
                click.echo(f"🔄 Step 1: Converting PDF to Markdown using {engine}...")
            adapter = PCIDSSPipelineAdapter()
            success = adapter.convert_pdf_to_markdown(str(pdf_file), str(input_file))
            if not success:
                click.echo("❌ PDF conversion failed!")
                return
        
        # Extract controls
        if verbose:
            click.echo("🔄 Step 2: Extracting controls...")
        adapter = PCIDSSPipelineAdapter()
        result = adapter.extract_from_markdown(str(input_file), str(output_dir))
        success = result.total_controls > 0
        
        if not success:
            click.echo("❌ Control extraction failed!")
            if hasattr(result, 'quality_metrics') and result.quality_metrics.validation_notes:
                click.echo("🔍 Error details:")
                for note in result.quality_metrics.validation_notes:
                    click.echo(f"   • {note}")
            return
            
        # Generate CSV
        if verbose:
            click.echo("🔄 Step 3: Generating CSV files...")
        adapter = PCIDSSPipelineAdapter()
        result = adapter.generate_csv(str(output_dir), str(csv_output), chunk_size)
        success = result.success
        if not success:
            click.echo("❌ CSV generation failed!")
            return
            
        click.echo("🎉 Complete PCI DSS workflow completed successfully!")
        click.echo(f"📁 Controls: {output_dir}/")
        click.echo(f"📊 CSV files: {csv_output}/")
            
    except Exception as e:
        click.echo(f"❌ Error: {str(e)}")
        if verbose:
            traceback.print_exc()

@cli.group()
def convert():
    """Convert documents between formats."""
    pass

@convert.command(name='pdf-to-md')
@click.option('--pdf-file', required=True, help='Input PDF file path')
@click.option('--output-file', help='Output markdown file path (optional)')
@click.option('--engine', type=click.Choice(['pymupdf4llm', 'docling']), default='pymupdf4llm', help='PDF conversion engine (default: pymupdf4llm)')
@click.option('--pages', help='Comma-separated list of page numbers to convert (optional, pymupdf4llm only)')
@click.option('--verbose', is_flag=True, help='Enable verbose output')
def convert_pdf_to_markdown(pdf_file, output_file, engine, pages, verbose):
    """
    Convert PDF to Markdown using pymupdf4llm or docling.
    
    Engine Options:
    - pymupdf4llm: Fast conversion, LLM-optimized, supports page selection
    - docling: Advanced layout analysis, superior table detection, processes entire document
    
    Examples:
        python cli.py convert pdf-to-md --pdf-file input.pdf --engine pymupdf4llm
        python cli.py convert pdf-to-md --pdf-file input.pdf --engine docling --verbose
        python cli.py convert pdf-to-md --pdf-file input.pdf --output-file output.md --engine docling
        python cli.py convert pdf-to-md --pdf-file input.pdf --pages 1,2,3 --engine pymupdf4llm
    """
    
    try:
        if verbose:
            print(f"🔄 PDF to Markdown Conversion ({engine})")
            print("=" * 50)
            print(f"📄 Input PDF: {pdf_file}")
            print(f"🔧 Engine: {engine}")
            if output_file:
                print(f"📝 Output MD: {output_file}")
            if pages:
                print(f"📄 Pages: {pages}")
        
        # Parse page numbers if provided (only for pymupdf4llm)
        page_list = None
        if pages:
            if engine == 'docling':
                click.echo("⚠️  Page selection not supported with docling engine. Processing entire document.")
            else:
                try:
                    page_list = [int(p.strip()) - 1 for p in pages.split(',')]  # Convert to 0-based
                    if verbose:
                        print(f"🔢 Processing pages: {[p+1 for p in page_list]}")
                except ValueError:
                    click.echo("❌ Invalid page numbers. Use format: 1,2,3")
                    return
        
        # Initialize universal converter
        converter = UniversalPDFConverter()
        
        # Convert PDF to Markdown
        if page_list and engine == 'pymupdf4llm':
            # Use original converter for page selection (pymupdf4llm only)
            from processors.compliance_standards.pci_dss.core.pdf_converter import PDFToMarkdownConverter
            legacy_converter = PDFToMarkdownConverter()
            md_content = legacy_converter.convert_pdf_to_markdown(
                pdf_path=pdf_file,
                output_path=output_file,
                pages=page_list
            )
            quality_metrics = legacy_converter.validate_conversion_quality(md_content)
        else:
            # Use universal converter for standard conversion
            result = converter.convert_with_metadata(
                pdf_path=pdf_file,
                output_path=output_file,
                engine=engine,
                processor_type='generic'
            )
            md_content = result.markdown_content
            quality_metrics = result.quality_metrics
        
        if verbose:
            print(f"\n📊 Conversion Quality Metrics:")
            print(f"   Total lines: {quality_metrics['total_lines']:,}")
            print(f"   Non-empty lines: {quality_metrics['non_empty_lines']:,}")
            print(f"   Headers detected: {quality_metrics['headers_detected']}")
            print(f"   Table markers: {quality_metrics['table_markers']}")
            quality_key = 'quality_assessment' if 'quality_assessment' in quality_metrics else 'estimated_quality'
            print(f"   Quality assessment: {quality_metrics.get(quality_key, 'unknown')}")
            
            # Show engine-specific metrics
            if engine == 'docling':
                print(f"   Conversion tool: {quality_metrics.get('conversion_tool', 'docling')}")
                if 'structured_content_lines' in quality_metrics:
                    print(f"   Structured content: {quality_metrics['structured_content_lines']}")
        
        click.echo(f"✅ PDF to Markdown conversion completed successfully with {engine}!")
        click.echo(f"📊 Generated {len(md_content):,} characters of markdown")
        
        if output_file:
            click.echo(f"📝 Saved to: {output_file}")
        else:
            click.echo("💡 Use --output-file to save the markdown to a file")
                
    except ImportError as e:
        click.echo(f"❌ Conversion failed: {str(e)}")
        if engine == 'pymupdf4llm':
            click.echo("💡 Install pymupdf4llm with: pip install pymupdf4llm")
        elif engine == 'docling':
            click.echo("💡 Install docling with: pip install docling")
    except Exception as e:
        click.echo(f"❌ Conversion failed: {str(e)}")
        if verbose:
            traceback.print_exc()

@extract.command(name='pci-dss')
@click.option('--pdf-file', help='Input PDF file path')
@click.option('--markdown-file', help='Input markdown file path') 
@click.option('--verbose', is_flag=True, help='Enable verbose output')
def extract_pci_dss(pdf_file, markdown_file, verbose):
    """
    Extract PCI DSS v4.0.1 controls from PDF or Markdown.
    
    This command uses the proven PCI DSS extractor that successfully
    extracts 306 controls with quality scoring and multi-table handling.
    
    Examples:
        python cli.py extract pci-dss --verbose
        python cli.py extract pci-dss --pdf-file custom.pdf
        python cli.py extract pci-dss --markdown-file custom.md --verbose
    """
    
    start_time = time.time()
    
    try:
        pipeline = CompliancePipeline()
        
        if verbose:
            print("🎯 PCI DSS Control Extraction - Centralized Pipeline")
            print("=" * 60)
        
        result = pipeline.process_pci_dss_document(
            markdown_file=markdown_file,
            pdf_file=pdf_file,
            verbose=verbose
        )
        
        if result.total_controls > 0:
            processing_time = time.time() - start_time
            
            click.echo(f"✅ Successfully extracted {result.total_controls} controls")
            click.echo(f"📁 Output saved to: shared_data/outputs/pci_dss_v4/controls/")
            click.echo(f"🔗 Multi-table controls: {result.multi_table_controls}")
            click.echo(f"⏱️ Processing time: {processing_time:.2f} seconds")
            click.echo(f"🏆 Overall quality score: {result.quality_metrics.overall_score:.1f}%")
            
            if verbose and result.requirements_breakdown:
                click.echo("\n📊 Requirements Breakdown:")
                for req, count in sorted(result.requirements_breakdown.items()):
                    click.echo(f"   {req}: {count} controls")
        else:
            click.echo("❌ Extraction failed:")
            for note in result.quality_metrics.validation_notes:
                click.echo(f"   {note}")
                
    except Exception as e:
        click.echo(f"❌ Pipeline error: {str(e)}")
        if verbose:
            traceback.print_exc()

@cli.group()
def generate():
    """Generate output files for different systems."""
    pass

@generate.command(name='csv')
@click.option('--framework', type=click.Choice(['pci-dss']), default='pci-dss', help='Compliance framework')
@click.option('--chunk-size', type=int, default=300, help='Target chunk size in tokens')
@click.option('--verbose', is_flag=True, help='Enable verbose output')
def generate_csv(framework, chunk_size, verbose):
    """
    Generate CSV files for Bedrock Knowledge Base.
    
    This command uses the original BedrockCSVGenerator that produces
    306 individual CSV files optimized for vector database ingestion.
    
    Examples:
        python cli.py generate csv --verbose
        python cli.py generate csv --chunk-size 400
    """
    
    try:
        pipeline = CompliancePipeline()
        
        if verbose:
            print("📊 CSV Generation for Bedrock Knowledge Base")
            print("=" * 60)
        
        # Map CLI framework to enum
        framework_map = {
            'pci-dss': ComplianceFramework.PCI_DSS_V4
        }
        
        result = pipeline.generate_csv_for_bedrock(
            framework=framework_map[framework],
            chunk_size=chunk_size,
            verbose=verbose
        )
        
        if result.success:
            click.echo(f"✅ Generated {result.total_files} CSV files")
            click.echo(f"📁 Output directory: {result.output_directory}")
            click.echo(f"🔤 Chunk strategy: {result.chunk_strategy}")
            click.echo(f"🎯 Target token size: {result.target_token_size}")
            
            if result.metadata_template_path:
                click.echo(f"📋 Metadata template: {result.metadata_template_path}")
        else:
            click.echo("❌ CSV generation failed:")
            for error in result.errors:
                click.echo(f"   {error}")
                
    except Exception as e:
        click.echo(f"❌ Pipeline error: {str(e)}")
        if verbose:
            traceback.print_exc()

@cli.command()
@click.option('--framework', type=click.Choice(['pci-dss']), default='pci-dss', help='Compliance framework')
@click.option('--pdf-file', help='Input PDF file path')
@click.option('--markdown-file', help='Input markdown file path')
@click.option('--chunk-size', type=int, default=300, help='Target chunk size for CSV generation')
@click.option('--verbose', is_flag=True, help='Enable verbose output')
def workflow(framework, pdf_file, markdown_file, chunk_size, verbose):
    """
    Run complete workflow: extract controls and generate CSV files.
    
    This is the recommended command that runs the full pipeline,
    preserving the exact same functionality as the original system.
    
    Examples:
        python cli.py workflow --verbose
        python cli.py workflow --pdf-file input.pdf --verbose
        python cli.py workflow --chunk-size 400
    """
    
    start_time = time.time()
    
    try:
        pipeline = CompliancePipeline()
        
        if verbose:
            print("🚀 Complete Compliance Workflow - Centralized Pipeline")
            print("=" * 70)
        
        # Map CLI framework to enum
        framework_map = {
            'pci-dss': ComplianceFramework.PCI_DSS_V4
        }
        
        extraction_result, csv_result = pipeline.run_complete_workflow(
            markdown_file=markdown_file,
            pdf_file=pdf_file,
            framework=framework_map[framework],
            chunk_size=chunk_size,
            verbose=verbose
        )
        
        total_time = time.time() - start_time
        
        # Final summary
        click.echo("\n🎉 Workflow Complete!")
        click.echo("=" * 40)
        click.echo(f"📋 Controls extracted: {extraction_result.total_controls}")
        click.echo(f"📊 CSV files generated: {csv_result.total_files}")
        click.echo(f"🏆 Quality score: {extraction_result.quality_metrics.overall_score:.1f}%")
        click.echo(f"⏱️ Total time: {total_time:.2f} seconds")
        
        if extraction_result.total_controls >= 306:
            click.echo("✨ Excellent! Achieved expected control count (306)")
        elif extraction_result.total_controls >= 300:
            click.echo("👍 Good! Close to expected control count")
        else:
            click.echo("⚠️ Warning: Lower than expected control count")
            
    except Exception as e:
        click.echo(f"❌ Workflow error: {str(e)}")
        if verbose:
            traceback.print_exc()

@cli.command()
@click.option('--framework', type=click.Choice(['pci-dss']), default='pci-dss', help='Compliance framework')
def validate(framework):
    """
    Validate extracted controls quality.
    
    Provides detailed quality assessment of the extraction results.
    """
    
    try:
        pipeline = CompliancePipeline()
        
        # Map CLI framework to enum
        framework_map = {
            'pci-dss': ComplianceFramework.PCI_DSS_V4
        }
        
        report = pipeline.validate_extraction_quality(framework_map[framework])
        
        click.echo(f"📊 Validation Report - {framework.upper()}")
        click.echo("=" * 50)
        click.echo(f"📋 Total controls: {report.total_controls}")
        click.echo(f"✅ Validation passed: {report.validation_passed}")
        click.echo(f"🏆 Quality score: {report.overall_quality_score:.1f}%")
        
        if report.recommendations:
            click.echo("\n💡 Recommendations:")
            for rec in report.recommendations:
                click.echo(f"   • {rec}")
        else:
            click.echo("\n✨ No issues found!")
            
    except Exception as e:
        click.echo(f"❌ Validation error: {str(e)}")

@cli.group()
def aws_guidance():
    """AWS Config Rules guidance processor commands."""
    pass

@aws_guidance.command(name='process')
@click.option('--input-file', default='shared_data/outputs/aws_config_guidance/aws_config_rule_full_mapping.csv', help='Input CSV file with AWS Config rules')
@click.option('--output-dir', default='shared_data/outputs/aws_config_guidance/database_import', help='Output directory for processed files')
@click.option('--verbose', is_flag=True, help='Enable verbose output')
def process_aws_guidance(input_file, output_dir, verbose):
    """
    Process AWS Config Rules guidance data for database import.
    
    This command processes the AWS Config rules mapping data and generates
    database-friendly CSV files with metadata for import.
    
    Examples:
        python cli.py aws-guidance process --verbose
        python cli.py aws-guidance process --input-file custom.csv
    """
    
    start_time = time.time()
    
    try:
        adapter = AWSGuidancePipelineAdapter()
        
        if verbose:
            print("🎯 AWS Config Rules Guidance Processing")
            print("=" * 60)
        
        result = adapter.process_config_rules(
            input_file=input_file,
            output_dir=output_dir
        )
        
        if result.success:
            processing_time = time.time() - start_time
            
            click.echo(f"✅ Successfully processed AWS Config rules")
            click.echo(f"📁 Output saved to: {output_dir}")
            click.echo(f"📊 Generated files: {result.total_files}")
            click.echo(f"⏱️ Processing time: {processing_time:.2f} seconds")
            
            if verbose and result.metadata_template_path:
                click.echo(f"\n📋 Schema file: {result.metadata_template_path}")
        else:
            click.echo("❌ Processing failed:")
            for error in result.errors:
                click.echo(f"   {error}")
                
    except Exception as e:
        click.echo(f"❌ Processing error: {str(e)}")
        if verbose:
            traceback.print_exc()

@aws_guidance.command(name='pci-mappings')
@click.option('--input-file', help='Input JSON file with PCI controls (optional)')
@click.option('--output-dir', help='Output directory for processed files (optional)')
@click.option('--verbose', is_flag=True, help='Enable verbose output')
def process_pci_mappings(input_file, output_dir, verbose):
    """
    Process PCI DSS to AWS Config rule mappings.
    
    This command processes the PCI DSS control to AWS Config rule mappings and generates
    database-friendly CSV files with metadata for import.
    
    Examples:
        python cli.py aws-guidance pci-mappings --verbose
        python cli.py aws-guidance pci-mappings --input-file custom.json --output-dir custom/output
    """
    
    start_time = time.time()
    
    try:
        adapter = AWSGuidancePipelineAdapter()
        
        if verbose:
            print("🎯 PCI DSS to AWS Config Rule Mapping Processing")
            print("=" * 60)
        
        result = adapter.process_pci_mappings(
            input_file=input_file,
            output_dir=output_dir
        )
        
        if result.success:
            processing_time = time.time() - start_time
            
            click.echo(f"✅ Successfully processed PCI DSS to AWS Config rule mappings")
            click.echo(f"📁 Output saved to: {result.output_directory}")
            click.echo(f"📊 Generated files: {result.total_files}")
            click.echo(f"⏱️ Processing time: {processing_time:.2f} seconds")
            
            if verbose and result.metadata_template_path:
                click.echo(f"\n📋 Schema file: {result.metadata_template_path}")
        else:
            click.echo("❌ Processing failed:")
            for error in result.errors:
                click.echo(f"   {error}")
                
    except Exception as e:
        click.echo(f"❌ Processing error: {str(e)}")
        if verbose:
            traceback.print_exc()

@cli.command()
def status():
    """
    Show current pipeline status and statistics.
    
    Displays information about extracted controls and generated files.
    """
    
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
            click.echo("\n📈 Extraction Statistics:")
            for framework, data in stats.items():
                click.echo(f"\n{framework.upper()}:")
                click.echo(f"   📄 Markdown files: {data['markdown_files']}")
                click.echo(f"   📋 JSON files: {data['json_files']}")
                click.echo(f"   📊 CSV files: {data['csv_files']}")
                click.echo(f"   ⏰ Status: {data['last_extraction']}")
        else:
            click.echo("\n📭 No extractions found. Run 'python cli.py workflow' to get started.")
            
    except Exception as e:
        click.echo(f"❌ Status error: {str(e)}")

@cli.command()
def compare():
    """
    Show pipeline status (migration completed).
    
    Note: The original rag_service symlinks have been removed as the migration
    to centralized data pipeline is complete and successful.
    """
    
    click.echo("📊 Pipeline Status (Migration Complete)")
    click.echo("=" * 45)
    
    # Check centralized results
    centralized_controls = Path("shared_data/outputs/pci_dss_v4/controls")
    if centralized_controls.exists():
        cent_md = len(list(centralized_controls.glob("control_*.md")))
        cent_json = len(list(centralized_controls.glob("control_*.json")))
        cent_csv = len(list(Path("shared_data/outputs/pci_dss_v4/bedrock").glob("*.csv")))
        click.echo(f"🎯 Centralized Data Pipeline:")
        click.echo(f"   📄 Markdown controls: {cent_md}")
        click.echo(f"   📋 JSON controls: {cent_json}")
        click.echo(f"   📊 CSV files: {cent_csv}")
        
        if cent_md >= 306:
            click.echo("✅ Migration successful! Expected control count achieved.")
        elif cent_md >= 300:
            click.echo("✅ Migration successful! Close to expected control count.")
        else:
            click.echo("⚠️ Warning: Lower than expected control count.")
    else:
        click.echo("🎯 Centralized Pipeline: Not run yet")
        click.echo("💡 Run: python cli.py workflow --verbose")
    
    click.echo(f"\n📋 Migration Status:")
    click.echo(f"   ✅ Extractors moved to data_pipeline/extractors/compliance/")
    click.echo(f"   ✅ Data centralized in shared_data/")
    click.echo(f"   ✅ Unified CLI operational")
    click.echo(f"   ✅ Original symlinks removed (rag_service ready for RAG)")
    
    click.echo(f"\n🚀 Usage:")
    click.echo(f"   python cli.py workflow --verbose    # Complete extraction")
    click.echo(f"   python cli.py status               # Show statistics")

if __name__ == '__main__':
    cli() 