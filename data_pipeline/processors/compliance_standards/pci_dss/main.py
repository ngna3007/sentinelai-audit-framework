#!/usr/bin/env python3
"""
PCI DSS Control Extractor - Main Entry Point

This is the primary interface for extracting PCI DSS controls from markdown.
Run this script to execute the complete extraction workflow.

Usage:
    python main.py extract    # Extract controls to markdown and JSON
    python main.py csv        # Generate CSV for Bedrock Knowledge Base
    python main.py all        # Run complete workflow (extract + csv)
    python main.py --help     # Show detailed help

For teammates:
    1. Ensure PCI-DSS-v4_0_1-FULL.md is in the shared_data/documents directory
    2. Run: python -m extractors.pci_dss_v4_0_1.main extract
    3. Check output in extracted_controls/ and ingest/bedrock/
"""

import argparse
import sys
from pathlib import Path
from typing import Optional

# Add the rag_service root to Python path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

def setup_cli() -> argparse.ArgumentParser:
    """Setup command line interface."""
    parser = argparse.ArgumentParser(
        description="PCI DSS Control Extractor - Extract and process PCI DSS controls",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py convert                    # Convert PDF to Markdown
  python main.py extract                    # Extract controls from Markdown
  python main.py csv                        # Generate CSV only (requires extracted controls)
  python main.py all                        # Complete workflow (extract + csv)
  python main.py convert --pdf-file custom.pdf --input-file custom.md
  python main.py extract --output-dir /tmp # Custom output directory
  python main.py csv --chunk-size 400      # Custom token chunk size

Workflow:
  1. convert: Converts PDF to Markdown using pymupdf4llm (LLM-optimized)
  2. extract: Parses Markdown and extracts individual controls
  3. csv:     Processes extracted controls and generates CSV for Bedrock
  4. all:     Runs both extract and csv steps (requires existing Markdown)
        """
    )
    
    parser.add_argument(
        'command',
        choices=['convert', 'extract', 'csv', 'all'],
        help='Command to execute'
    )
    
    parser.add_argument(
        '--input-file',
        type=str,
        default='PCI-DSS-v4_0_1-FULL.md',
        help='Input markdown file for extract/csv commands (default: PCI-DSS-v4_0_1-FULL.md)'
    )
    
    parser.add_argument(
        '--pdf-file',
        type=str,
        default='shared_data/documents/PCI-DSS-v4_0_1.pdf',
        help='Input PDF file for convert command (default: shared_data/documents/PCI-DSS-v4_0_1.pdf)'
    )
    
    parser.add_argument(
        '--output-dir',
        type=str,
        default='shared_data/outputs/pci_dss_v4/controls',
        help='Output directory for extracted controls (default: shared_data/outputs/pci_dss_v4/controls)'
    )
    
    parser.add_argument(
        '--csv-output',
        type=str,
        default='shared_data/outputs/pci_dss_v4/database_import',
        help='CSV output directory for database import (default: shared_data/outputs/pci_dss_v4/database_import)'
    )
    
    parser.add_argument(
        '--chunk-size',
        type=int,
        default=300,
        help='Target chunk size in tokens for CSV generation (default: 300)'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose output'
    )
    
    return parser

def validate_environment() -> bool:
    """Validate that the environment is set up correctly."""
    errors = []
    
    # Check if we're in the right directory structure
    current_dir = Path.cwd()
    # Navigate to project root from data_pipeline/processors/compliance_standards/pci_dss/
    project_root = Path(__file__).parent.parent.parent.parent.parent
    
    # Check if input file exists (look in shared_data/documents folder)
    input_file = project_root / "shared_data" / "documents" / "PCI-DSS-v4_0_1-FULL.md"
    if not input_file.exists():
        errors.append(f"❌ PCI-DSS-v4_0_1-FULL.md not found at {input_file}")
    
    if errors:
        print("🚨 Environment validation failed:")
        for error in errors:
            print(f"   {error}")
        print("\n💡 Setup instructions:")
        print("   1. Ensure PCI-DSS-v4_0_1-FULL.md is in shared_data/documents/")
        print("   2. Run from project root: python -m data_pipeline.processors.compliance_standards.pci_dss.main extract")
        return False
    
    return True

def run_pdf_conversion(pdf_file: str, output_file: str, verbose: bool = False) -> bool:
    """Run PDF to Markdown conversion using pymupdf4llm."""
    try:
        from .core.pdf_converter import PDFToMarkdownConverter
        
        print("🔄 Starting PDF to Markdown Conversion")
        print("=" * 60)
        
        if verbose:
            print(f"📄 PDF file: {pdf_file}")
            print(f"📝 Output file: {output_file}")
        
        # Check if pymupdf4llm is available
        converter = PDFToMarkdownConverter()
        
        # Resolve paths relative to project root
        project_root = Path(__file__).parent.parent.parent.parent.parent
        if not Path(pdf_file).is_absolute():
            pdf_file = str(project_root / pdf_file)
        if not Path(output_file).is_absolute():
            output_file = str(project_root / "shared_data" / "documents" / output_file)
        
        # Convert PDF to Markdown
        md_content = converter.convert_pdf_to_markdown(pdf_file, output_file)
        
        # Validate conversion quality
        quality_metrics = converter.validate_conversion_quality(md_content)
        
        if verbose:
            print(f"\n📊 Conversion Quality Metrics:")
            print(f"   Total lines: {quality_metrics['total_lines']:,}")
            print(f"   Non-empty lines: {quality_metrics['non_empty_lines']:,}")
            print(f"   Headers detected: {quality_metrics['headers_detected']}")
            print(f"   Table markers: {quality_metrics['table_markers']}")
            print(f"   Quality assessment: {quality_metrics['estimated_quality']}")
        
        print("✅ PDF to Markdown conversion completed successfully!")
        print(f"📝 Markdown saved to: {output_file}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Conversion failed: {str(e)}")
        print("💡 Install pymupdf4llm with: pip install pymupdf4llm")
        return False
    except Exception as e:
        print(f"❌ Conversion failed: {str(e)}")
        if verbose:
            import traceback
            traceback.print_exc()
        return False


def run_extraction(input_file: str, output_dir: str, verbose: bool = False) -> bool:
    """Run the control extraction process."""
    try:
        from .core.extractor import ControlExtractor
        
        print("🚀 Starting PCI DSS Control Extraction")
        print("=" * 60)
        
        if verbose:
            print(f"📄 Input file: {input_file}")
            print(f"📁 Output directory: {output_dir}")
        
        # Resolve paths relative to project root
        project_root = Path(__file__).parent.parent.parent.parent.parent
        if not Path(input_file).is_absolute():
            input_file = str(project_root / "shared_data" / "documents" / input_file)
        
        # Also resolve output directory relative to project root
        if not Path(output_dir).is_absolute():
            output_dir = str(project_root / output_dir)
        
        # Initialize and run extractor
        extractor = ControlExtractor(input_file)
        extractor.load_markdown()
        extractor.extract_all_controls()
        
        if verbose:
            extractor.print_summary()
        
        extractor.save_controls(output_dir)
        
        print("✅ Control extraction completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Extraction failed: {str(e)}")
        if verbose:
            import traceback
            traceback.print_exc()
        return False

def run_csv_generation(input_dir: str, output_dir: str, chunk_size: int, verbose: bool = False) -> bool:
    """Run the CSV generation process for Bedrock."""
    try:
        from .core.csv_generator import CSVGenerator
        
        print("\n📊 Starting CSV Generation for Bedrock")
        print("=" * 60)
        
        if verbose:
            print(f"📁 Input directory: {input_dir}")
            print(f"📁 Output directory: {output_dir}")
            print(f"🔤 Target chunk size: {chunk_size} tokens")
        
        # Resolve paths relative to project root
        project_root = Path(__file__).parent.parent.parent.parent.parent
        if not Path(input_dir).is_absolute():
            input_dir = str(project_root / input_dir)
        if not Path(output_dir).is_absolute():
            output_dir = str(project_root / output_dir)
        
        # Initialize and run CSV generator with correct input and output directories
        generator = CSVGenerator(controls_dir=input_dir, output_dir=output_dir)
        generator.generate_csv_files()
        
        print("✅ CSV generation completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ CSV generation failed: {str(e)}")
        if verbose:
            import traceback
            traceback.print_exc()
        return False

def main():
    """Main entry point."""
    parser = setup_cli()
    args = parser.parse_args()
    
    print("🎯 PCI DSS Control Extractor")
    print("=" * 60)
    
    # Validate environment
    if not validate_environment():
        sys.exit(1)
    
    success = True
    
    # Execute requested command
    if args.command == 'convert':
        success = run_pdf_conversion(
            pdf_file=args.pdf_file,
            output_file=args.input_file,
            verbose=args.verbose
        )
    elif args.command in ['extract', 'all']:
        success = run_extraction(
            input_file=args.input_file,
            output_dir=args.output_dir,
            verbose=args.verbose
        )
    
    if success and args.command in ['csv', 'all']:
        success = run_csv_generation(
            input_dir=args.output_dir,
            output_dir=args.csv_output,
            chunk_size=args.chunk_size,
            verbose=args.verbose
        )
    
    if success:
        print("\n🎉 All operations completed successfully!")
        print("\n📁 Output locations:")
        print(f"   📄 Extracted controls: {args.output_dir}/")
        if args.command in ['csv', 'all']:
            print(f"   📊 Bedrock CSV: {args.csv_output}/")
    else:
        print("\n💥 Operations failed. Check error messages above.")
        sys.exit(1)

if __name__ == "__main__":
    main() 