#!/usr/bin/env python3
"""
Example Usage of PCI DSS Control Extractor - Modular Architecture

This file demonstrates how to use the individual components of the
refactored PCI DSS control extractor system.

Updated for the new modular architecture with separate components for:
- Text processing
- Content building  
- Metadata generation
- CSV generation
"""

import sys
from pathlib import Path

# Add the rag_service root to Python path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

def example_basic_extraction():
    """Example 1: Basic control extraction using the main orchestrator."""
    print("🚀 Example 1: Basic Control Extraction")
    print("=" * 50)
    
    from core.extractor import ControlExtractor
    
    # Initialize extractor
    extractor = ControlExtractor("PCI-DSS-v4_0_1-FULL.md")
    
    # Load and extract
    extractor.load_markdown()
    controls = extractor.extract_all_controls()
    
    print(f"✅ Extracted {len(controls)} controls")
    
    # Show a sample control
    sample_id = "1.2.8" if "1.2.8" in controls else list(controls.keys())[0]
    sample_control = controls[sample_id]
    
    print(f"\n📋 Sample Control {sample_id}:")
    print(f"   Tables: {len(sample_control['tables'])}")
    print(f"   Rows: {len(sample_control['rows'])}")
    print(f"   Content length: {len(sample_control['content'])} chars")
    print(f"   First 200 chars: {sample_control['content'][:200]}...")
    
    return controls

def example_component_usage():
    """Example 2: Using individual components separately."""
    print("\n🧩 Example 2: Individual Component Usage")
    print("=" * 50)
    
    from core.text_processors import TextProcessor, ControlIDDetector
    from core.content_builders import ControlContentBuilder
    from core.metadata_generators import ValidationMetadataGenerator
    
    # Sample table row data (would normally come from extraction)
    sample_row = {
        'col1': '**1.2.8** All system components must be protected from malware.',
        'col2': '**1.2.8.a** Examine documentation and observe processes.',
        'col3': '**Purpose** This requirement ensures malware protection.'
    }
    
    print("🔍 Text Processing:")
    
    # Clean text
    clean_col1 = TextProcessor.clean_text(sample_row['col1'])
    print(f"   Cleaned: {clean_col1}")
    
    # Extract control ID
    control_id = ControlIDDetector.extract_control_id(sample_row['col1'])
    print(f"   Control ID: {control_id}")
    
    # Check if valid context
    is_valid = ControlIDDetector.is_control_context_row(sample_row)
    print(f"   Valid context: {is_valid}")
    
    print("\n📝 Content Building:")
    
    # Sample control data structure
    sample_control_data = {
        'control_id': '1.2.8',
        'rows': [sample_row],
        'tables': [{'header': 'Sample Table', 'rows': [sample_row]}],
        'sections': {
            'requirements': True,
            'testing_procedures': True,
            'purpose': True,
            'examples': False,
            'good_practice': False
        }
    }
    
    # Build content
    builder = ControlContentBuilder()
    content = builder.build_control_content(sample_control_data)
    print(f"   Built content ({len(content)} chars):")
    print(f"   {content[:150]}...")
    
    print("\n📊 Metadata Generation:")
    
    # Generate validation metadata
    validator = ValidationMetadataGenerator()
    metadata = validator.generate_validation_metadata('1.2.8', sample_control_data, content)
    print(f"   Token count: {metadata['token_count']}")
    print(f"   Has requirements: {metadata['has_requirements']}")
    print(f"   Has procedures: {metadata['has_testing_procedures']}")
    
    # Analyze quality
    quality = validator.analyze_extraction_quality(metadata)
    print(f"   Quality score: {quality['quality_score']}/100")

def example_csv_generation():
    """Example 3: CSV generation for Bedrock."""
    print("\n📊 Example 3: CSV Generation")
    print("=" * 50)
    
    from core.bedrock_csv_generator import BedrockCSVGenerator
    
    # Create sample extracted controls directory structure
    sample_dir = Path("temp_sample_controls")
    sample_dir.mkdir(exist_ok=True)
    
    # Create sample control files
    sample_control = """Control 1.2.8

Defined Approach Requirements:
All system components must be protected from malware through the use of anti-malware solutions.

Testing Procedures:
Testing Procedure 1.2.8.a: Examine anti-malware solution configurations to verify they are configured to detect malware.

Guidance:
Purpose: This requirement ensures that malware protection is implemented across all system components."""
    
    sample_metadata = {
        "req_id": "1.2.8",
        "standard": "PCI-DSS-v4.0",
        "title": "All system components must be protected from malware.",
        "chunk_type": "requirement",
        "status": "required",
        "testing_procedures": ["Examine anti-malware solution configurations"],
        "source": "PCI_DSS_PDF_v4.0",
        "text": sample_control
    }
    
    # Write sample files
    with open(sample_dir / "control_1.2.8.md", 'w') as f:
        f.write(sample_control)
    
    import json
    with open(sample_dir / "control_1.2.8_production.json", 'w') as f:
        json.dump(sample_metadata, f, indent=2)
    
    try:
        # Generate CSV
        generator = BedrockCSVGenerator()
        generator.load_extracted_controls(str(sample_dir))
        
        output_dir = Path("temp_csv_output")
        generator.generate_csv(str(output_dir), target_chunk_size=300)
        
        print(f"✅ Generated CSV in {output_dir}/")
        
        # Show CSV content
        csv_file = output_dir / "pci_dss_controls.csv"
        if csv_file.exists():
            with open(csv_file, 'r') as f:
                lines = f.readlines()
            print(f"   CSV has {len(lines)} lines")
            print(f"   Header: {lines[0].strip()}")
            if len(lines) > 1:
                print(f"   Sample row: {lines[1][:100]}...")
        
        # Cleanup
        import shutil
        shutil.rmtree(sample_dir, ignore_errors=True)
        shutil.rmtree(output_dir, ignore_errors=True)
        
    except Exception as e:
        print(f"❌ CSV generation failed: {e}")
        # Cleanup on error
        import shutil
        shutil.rmtree(sample_dir, ignore_errors=True)

def example_quality_analysis():
    """Example 4: Quality analysis and validation."""
    print("\n📈 Example 4: Quality Analysis")
    print("=" * 50)
    
    from core.metadata_generators import ValidationMetadataGenerator, MetadataFileManager
    
    # Sample validation metadata
    sample_metadata = {
        'control_id': '1.2.8',
        'sections': {
            'requirements': True,
            'testing_procedures': True,
            'purpose': True,
            'examples': False,
            'good_practice': False
        },
        'row_count': 5,
        'table_count': 1,
        'content_length_chars': 850,
        'token_count': 212,
        'has_requirements': True,
        'has_testing_procedures': True,
        'has_guidance': True
    }
    
    # Analyze quality
    validator = ValidationMetadataGenerator()
    quality = validator.analyze_extraction_quality(sample_metadata)
    
    print(f"📊 Quality Analysis for Control {sample_metadata['control_id']}:")
    print(f"   Quality Score: {quality['quality_score']}/100 ({quality['quality_percentage']:.1f}%)")
    print(f"   Issues Found: {len(quality['issues'])}")
    
    for issue in quality['issues']:
        print(f"     ⚠️  {issue}")
    
    print(f"   Recommendations: {len(quality['recommendations'])}")
    for rec in quality['recommendations']:
        print(f"     💡 {rec}")

def example_advanced_workflow():
    """Example 5: Advanced workflow with custom processing."""
    print("\n🔬 Example 5: Advanced Custom Workflow")
    print("=" * 50)
    
    from core.extractor import ControlExtractor
    from core.text_processors import SectionExtractor
    from core.content_builders import MarkdownFormatter
    
    # Custom extraction with filtering
    extractor = ControlExtractor("PCI-DSS-v4_0_1-FULL.md")
    
    try:
        extractor.load_markdown()
        
        # Extract only tables (without full processing)
        tables = extractor.extract_tables()
        print(f"📊 Found {len(tables)} tables")
        
        # Custom filtering - only extract requirement 1 controls
        print(f"🎯 Filtering for Requirement 1 controls...")
        
        all_controls = extractor.extract_controls_from_tables(tables)
        req1_controls = {k: v for k, v in all_controls.items() if k.startswith('1.')}
        
        print(f"📋 Found {len(req1_controls)} Requirement 1 controls")
        
        # Process a specific control in detail
        if '1.2.8' in req1_controls:
            control_data = req1_controls['1.2.8']
            
            # Analyze sections
            sections = SectionExtractor.analyze_control_sections(control_data)
            print(f"\n🔍 Analysis of Control 1.2.8:")
            print(f"   Rows extracted: {len(control_data['rows'])}")
            print(f"   Tables spanned: {len(control_data['tables'])}")
            print(f"   Sections found:")
            
            for section, present in sections.items():
                status = "✅" if present else "❌"
                print(f"     {status} {section.replace('_', ' ').title()}")
            
            # Build and format content
            from core.content_builders import ControlContentBuilder
            builder = ControlContentBuilder()
            content = builder.build_control_content(control_data)
            
            # Format for markdown
            formatted = MarkdownFormatter.format_for_markdown(content, '1.2.8')
            
            print(f"\n📝 Content preview ({len(content)} chars):")
            print(formatted[:300] + "..." if len(formatted) > 300 else formatted)
        
    except FileNotFoundError:
        print("❌ PCI-DSS-v4_0_1-FULL.md not found")
        print("   This example requires the full markdown file")
    except Exception as e:
        print(f"❌ Error in advanced workflow: {e}")

def main():
    """Run all examples."""
    print("🎯 PCI DSS Control Extractor - Example Usage")
    print("=" * 60)
    print("Demonstrating the modular architecture components")
    
    try:
        # Run examples that don't require the full file
        example_component_usage()
        example_csv_generation()
        example_quality_analysis()
        
        # Run examples that require the full markdown file
        try:
            controls = example_basic_extraction()
            example_advanced_workflow()
        except FileNotFoundError:
            print("\n⚠️  Full markdown file not found - skipping file-dependent examples")
            print("   To run all examples, ensure PCI-DSS-v4_0_1-FULL.md is available")
        
        print("\n✅ All examples completed!")
        print("\n💡 Next steps:")
        print("   1. Try running: python main.py extract --help")
        print("   2. Check the README.md for detailed documentation")
        print("   3. Explore the core/ modules for implementation details")
        
    except Exception as e:
        print(f"\n❌ Error running examples: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 