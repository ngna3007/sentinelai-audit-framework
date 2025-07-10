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
    1. Ensure PCI-DSS-v4_0_1-FULL.md is in the rag_service/data/ directory
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
  python main.py extract                    # Extract controls only
  python main.py csv                        # Generate CSV only (requires extracted controls)
  python main.py all                        # Complete workflow
  python main.py extract --output-dir /tmp # Custom output directory
  python main.py csv --chunk-size 400      # Custom token chunk size

Workflow:
  1. extract: Parses data/PCI-DSS-v4_0_1-FULL.md and extracts individual controls
  2. csv:     Processes extracted controls and generates CSV for Bedrock
  3. all:     Runs both extract and csv steps
        """
    )
    
    parser.add_argument(
        'command',
        choices=['extract', 'csv', 'all'],
        help='Command to execute'
    )
    
    parser.add_argument(
        '--input-file',
        type=str,
        default='PCI-DSS-v4_0_1-FULL.md',
        help='Input markdown file (default: PCI-DSS-v4_0_1-FULL.md)'
    )
    
    parser.add_argument(
        '--output-dir',
        type=str,
        default='extracted_controls',
        help='Output directory for extracted controls (default: extracted_controls)'
    )
    
    parser.add_argument(
        '--csv-output',
        type=str,
        default='ingest/bedrock/pci_dss_4.0',
        help='CSV output directory for Bedrock (default: ingest/bedrock/pci_dss_4.0)'
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
    rag_service_root = Path(__file__).parent.parent.parent
    
    # Check if input file exists (look in rag_service data folder)
    input_file = rag_service_root / "data" / "PCI-DSS-v4_0_1-FULL.md"
    if not input_file.exists():
        errors.append(f"❌ PCI-DSS-v4_0_1-FULL.md not found at {input_file}")
    
    if errors:
        print("🚨 Environment validation failed:")
        for error in errors:
            print(f"   {error}")
        print("\n💡 Setup instructions:")
        print("   1. Navigate to the rag_service directory")
        print("   2. Ensure PCI-DSS-v4_0_1-FULL.md is in the data/ folder")
        print("   3. Run: python -m extractors.pci_dss_v4_0_1.main extract")
        return False
    
    return True

def run_extraction(input_file: str, output_dir: str, verbose: bool = False) -> bool:
    """Run the control extraction process."""
    try:
        from .core.extractor import ControlExtractor
        
        print("🚀 Starting PCI DSS Control Extraction")
        print("=" * 60)
        
        if verbose:
            print(f"📄 Input file: {input_file}")
            print(f"📁 Output directory: {output_dir}")
        
        # Resolve input file path relative to rag_service root
        rag_service_root = Path(__file__).parent.parent.parent
        if not Path(input_file).is_absolute():
            input_file = str(rag_service_root / "data" / input_file)
        
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
        from .core.bedrock_csv_generator import BedrockCSVGenerator
        
        print("\n📊 Starting CSV Generation for Bedrock")
        print("=" * 60)
        
        if verbose:
            print(f"📁 Input directory: {input_dir}")
            print(f"📁 Output directory: {output_dir}")
            print(f"🔤 Target chunk size: {chunk_size} tokens")
        
        # Initialize and run CSV generator with correct input directory
        generator = BedrockCSVGenerator(controls_dir=input_dir)
        generator.generate_bedrock_files()
        
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
    if args.command in ['extract', 'all']:
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