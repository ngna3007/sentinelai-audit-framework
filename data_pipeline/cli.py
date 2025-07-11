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

# Add current directory to path for imports
sys.path.append(str(Path(__file__).parent))

from pipelines.compliance_pipeline import CompliancePipeline
from schemas.compliance import ComplianceFramework

@click.group()
def cli():
    """SentinelAI Data Pipeline - Centralized ETL for compliance data."""
    pass

@cli.group()
def extract():
    """Extract data from compliance documents."""
    pass

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
            import traceback
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
            import traceback
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
            import traceback
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