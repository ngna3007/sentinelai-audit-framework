#!/usr/bin/env python3
"""
AWS Config Guidance Processor - PDF to Markdown Converter

Simple converter to turn the AWS Config Guidance PDF into markdown and extract the mapping table.
"""

import argparse
import sys
import time
from pathlib import Path

# Add the project root to Python path for imports
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

def setup_cli() -> argparse.ArgumentParser:
    """Setup command line interface."""
    parser = argparse.ArgumentParser(
        description="AWS Config Guidance PDF to Markdown Converter and Processor"
    )
    
    parser.add_argument(
        'command',
        choices=['convert', 'process', 'all'],
        help='Command to execute: convert PDF to MD, process MD to extract table, or all'
    )
    
    parser.add_argument(
        '--pdf-file',
        type=str,
        default='shared_data/documents/PCI-DSS-v4_0_1-AWSConfig-Guidance.pdf',
        help='Input PDF file'
    )
    
    parser.add_argument(
        '--output-file',
        type=str,
        default='shared_data/documents/PCI-DSS-v4_0_1-AWSConfig-Guidance.md',
        help='Output markdown file'
    )
    
    parser.add_argument(
        '--input-file',
        type=str,
        default='shared_data/documents/PCI-DSS-v4_0_1-AWSConfig-Guidance.md',
        help='Input markdown file for processing'
    )
    
    parser.add_argument(
        '--output-dir',
        type=str,
        default='shared_data/outputs/aws_config_guidance',
        help='Output directory for processed results'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose output'
    )
    
    return parser

def run_conversion(pdf_file: str, output_file: str, verbose: bool = False) -> bool:
    """Run PDF to Markdown conversion."""
    try:
        from data_pipeline.processors.aws_guidance.core.pdf_converter import PDFConverter
        
        print("🔄 Converting AWS Config Guidance PDF to Markdown")
        print("=" * 60)
        
        if verbose:
            print(f"📄 PDF file: {pdf_file}")
            print(f"📝 Output file: {output_file}")
        
        # Initialize converter
        converter = PDFConverter()
        
        # Resolve paths relative to project root
        if not Path(pdf_file).is_absolute():
            pdf_file = str(project_root / pdf_file)
        if not Path(output_file).is_absolute():
            output_file = str(project_root / output_file)
        
        # Convert PDF to Markdown
        start_time = time.time()
        result = converter.convert_with_preprocessing(pdf_file, output_file)
        processing_time = time.time() - start_time
        
        # Validate conversion quality
        quality_metrics = converter.validate_conversion_quality(result['content'])
        
        print("✅ Conversion completed successfully!")
        print(f"📝 Markdown saved to: {output_file}")
        
        if verbose:
            print(f"\n📊 Quality Metrics:")
            print(f"   Total lines: {quality_metrics['total_lines']:,}")
            print(f"   Headers: {quality_metrics['headers_detected']}")
            print(f"   AWS references: {quality_metrics['aws_references']}")
            print(f"   Config references: {quality_metrics['config_references']}")
            print(f"   Quality: {quality_metrics['estimated_quality']}")
            print(f"   Processing time: {processing_time:.2f}s")
        
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

def run_processing(input_file: str, output_dir: str, verbose: bool = False) -> bool:
    """Run table extraction processing on markdown file."""
    try:
        from data_pipeline.processors.aws_guidance.core.content_processor import ContentProcessor
        
        print("🔄 Processing AWS Config Guidance Table")
        print("=" * 50)
        
        if verbose:
            print(f"📄 Input file: {input_file}")
            print(f"📁 Output directory: {output_dir}")
        
        # Resolve paths relative to project root
        if not Path(input_file).is_absolute():
            input_file = str(project_root / input_file)
        if not Path(output_dir).is_absolute():
            output_dir = str(project_root / output_dir)
        
        # Check if input file exists
        if not Path(input_file).exists():
            print(f"❌ Input file not found: {input_file}")
            return False
        
        # Read markdown content
        with open(input_file, 'r', encoding='utf-8') as f:
            md_content = f.read()
        
        # Process content
        start_time = time.time()
        processor = ContentProcessor()
        processing_results = processor.process_markdown(md_content)
        processing_time = time.time() - start_time
        
        # Create output directory
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Save processing results as separate files
        import json
        
        # Save main mappings file
        mappings_file = output_path / "aws_config_mappings.json"
        with open(mappings_file, 'w', encoding='utf-8') as f:
            json.dump(processing_results['mappings'], f, indent=2, ensure_ascii=False)
        
        # Save metadata file
        metadata_file = output_path / "aws_config_metadata.json"
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(processing_results['metadata'], f, indent=2, ensure_ascii=False)
        
        print("✅ Processing completed successfully!")
        print(f"📝 Mappings saved to: {mappings_file}")
        print(f"📊 Metadata saved to: {metadata_file}")
        
        if verbose:
            mappings_data = processing_results['mappings']
            metadata_data = processing_results['metadata']
            
            print(f"\n📊 Processing Results:")
            print(f"   Total mappings: {mappings_data['total_mappings']}")
            print(f"   Unique PCI controls: {mappings_data['unique_pci_controls']}")
            print(f"   Unique Config rules: {mappings_data['unique_config_rules']}")
            print(f"   Processing time: {processing_time:.2f}s")
            
            # Show compliance statistics summary
            compliance_stats = metadata_data['compliance_statistics']['summary']
            print(f"\n📋 Compliance Statistics:")
            print(f"   With NON_COMPLIANT info: {compliance_stats['total_with_non_compliance']}")
            print(f"   With COMPLIANT info: {compliance_stats['total_with_compliance']}")
            print(f"   Without compliance info: {compliance_stats['total_without_compliance_info']}")
            
            # Show first few mappings as examples
            if mappings_data['mappings']:
                print(f"\n📋 Sample Mappings:")
                for i, mapping in enumerate(mappings_data['mappings'][:3]):
                    print(f"   {i+1}. {mapping['control_id']} → {mapping['aws_config_rule']}")
                    compliance_info = mapping.get('compliance_conditions', {})
                    has_compliance = compliance_info.get('has_compliance_info', False)
                    has_non_compliance = compliance_info.get('has_non_compliance_info', False)
                    if has_compliance or has_non_compliance:
                        flags = []
                        if has_compliance:
                            flags.append("COMPLIANT")
                        if has_non_compliance:
                            flags.append("NON_COMPLIANT")
                        print(f"      Has compliance info: {', '.join(flags)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Processing failed: {str(e)}")
        if verbose:
            import traceback
            traceback.print_exc()
        return False

def main():
    """Main entry point."""
    parser = setup_cli()
    args = parser.parse_args()
    
    success = True
    
    try:
        if args.command in ['convert', 'all']:
            success = run_conversion(args.pdf_file, args.output_file, args.verbose)
            if not success:
                sys.exit(1)
        
        if args.command in ['process', 'all']:
            success = run_processing(args.input_file, args.output_dir, args.verbose)
            if not success:
                sys.exit(1)
        
        if args.command == 'convert':
            print("\n🎉 PDF to Markdown conversion completed!")
            print("📖 You can now review the markdown file to check for patterns.")
            print("💡 Next step: python main.py process --verbose")
        elif args.command == 'process':
            print("\n🎉 Table processing completed!")
            print("📊 Check the output JSON for extracted mappings.")
        else:  # all
            print("\n🎉 Complete processing workflow completed!")
            print("📊 Both conversion and table extraction are done.")
        
    except KeyboardInterrupt:
        print("\n⚠️  Processing interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main() 