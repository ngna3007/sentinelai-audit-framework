#!/usr/bin/env python3
"""
AWS Bedrock Knowledge Base CSV Generator

Combines PCI DSS control production metadata and content into CSV format
for AWS Bedrock Knowledge Base ingestion, with proper metadata.json configuration.
"""

import csv
import json
import os
import pandas as pd
from pathlib import Path
from typing import Dict, List

class BedrockCSVGenerator:
    def __init__(self, controls_dir: str = None):
        # Default to organized extracted controls if no path provided
        if controls_dir is None:
            # Go up from core/ to pci_dss_v4_0_1/ to extractors/ to rag_service/
            base_dir = Path(__file__).parent.parent.parent.parent
            controls_dir = base_dir / "ingest" / "extracted" / "pci_dss_4.0"
        self.controls_dir = Path(controls_dir)
        # Output to organized directory: ingest/bedrock/pci_dss_4.0/
        # Go up from core/ to pci_dss_v4_0_1/ to extractors/ to rag_service/
        base_dir = Path(__file__).parent.parent.parent.parent
        self.output_dir = base_dir / "ingest" / "bedrock" / "pci_dss_4.0"
        
    def load_control_data(self) -> List[Dict]:
        """Load all production metadata and content for controls."""
        controls_data = []
        
        # Find all production JSON files
        production_files = list(self.controls_dir.glob("*_production.json"))
        
        print(f"🔍 Found {len(production_files)} production metadata files")
        
        for prod_file in sorted(production_files):
            # Extract control ID from filename (e.g., control_12.3.3_production.json -> 12.3.3)
            control_id = prod_file.stem.replace("control_", "").replace("_production", "")
            
            # Load production metadata
            with open(prod_file, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
            
            # Load markdown content
            md_file = self.controls_dir / f"control_{control_id}.md"
            if md_file.exists():
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                
                # Combine metadata and content (pandas will handle CSV formatting)
                control_data = {
                    'req_id': metadata['req_id'],
                    'standard': metadata['standard'],
                    'title': metadata['title'],
                    'chunk_type': metadata['chunk_type'],
                    'status': metadata['status'],
                    'testing_procedures': self.format_testing_procedures(metadata['testing_procedures']),
                    'source': metadata['source'],
                    'content': content.strip()  # Main content field for Bedrock
                }
                
                controls_data.append(control_data)
            else:
                print(f"⚠️  Warning: Missing markdown file for {control_id}")
        
        return controls_data
    
    def format_testing_procedures(self, procedures: List[str]) -> str:
        """Convert testing procedures list to string format."""
        if not procedures:
            return ""
        
        # Join multiple procedures with semicolon separator
        return "; ".join(procedures)
    

    
    def generate_individual_csvs(self, controls_data: List[Dict]) -> List[Path]:
        """Generate individual CSV files for each control using pandas (better for Bedrock chunking)."""
        if not controls_data:
            print("❌ No controls data to generate CSVs")
            return []
        
        # Ensure output directory exists
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Define column order (content field last for clarity)
        columns = [
            'req_id',
            'standard', 
            'title',
            'chunk_type',
            'status',
            'testing_procedures',
            'source',
            'content'  # Main content field for Bedrock
        ]
        
        csv_files = []
        print(f"📝 Writing individual CSV files using pandas...")
        
        for control in controls_data:
            # Create filename: control_1.1.1.csv
            csv_filename = f"control_{control['req_id']}.csv"
            csv_path = self.output_dir / csv_filename
            
            # Create single-row DataFrame for this control
            df = pd.DataFrame([control], columns=columns)
            
            # Write to CSV with proper handling of multiline content
            df.to_csv(
                csv_path,
                index=False,              # Don't include row index
                encoding='utf-8',         # UTF-8 encoding  
                quoting=csv.QUOTE_ALL,    # Quote all fields for safety
                lineterminator='\n',      # Consistent line endings
                doublequote=True,         # Handle quotes properly
                quotechar='"',            # Use double quotes
                escapechar=None           # Let pandas handle escaping
            )
            
            csv_files.append(csv_path)
        
        print(f"✅ Generated {len(csv_files)} individual CSV files")
        return csv_files
    
    def generate_metadata_json_template(self):
        """Generate a template metadata.json file for Bedrock Knowledge Base."""
        metadata_config = {
            "metadataAttributes": {
                "source_document": "PCI_DSS_v4.0_Requirements",
                "document_type": "compliance_requirements", 
                "standard": "PCI-DSS-v4.0",
                "document_version": "4.0.1",
                "extraction_date": "2024-07-10",
                "extractor_version": "pci_dss_v4_0_1"
            },
            "documentStructureConfiguration": {
                "type": "RECORD_BASED_STRUCTURE_METADATA",
                "recordBasedStructureMetadata": {
                    "contentFields": [
                        {
                            "fieldName": "content"  # Main content field
                        }
                    ],
                    "metadataFieldsSpecification": {
                        "fieldsToInclude": [
                            {"fieldName": "req_id"},
                            {"fieldName": "standard"},
                            {"fieldName": "title"},
                            {"fieldName": "chunk_type"},
                            {"fieldName": "status"},
                            {"fieldName": "testing_procedures"},
                            {"fieldName": "source"}
                        ]
                        # Note: fieldsToExclude not needed since we're explicitly including
                    }
                }
            }
        }
        
        metadata_path = self.output_dir / "csv_metadata_template.json"
        
        print(f"🔧 Writing metadata template to {metadata_path}")
        
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata_config, f, indent=2, ensure_ascii=False)
        
        print("✅ Generated Bedrock metadata template (apply this to all CSV files)")
        return metadata_path
    
    def generate_bedrock_files(self):
        """Generate individual CSV files for each control using pandas (better Bedrock chunking)."""
        print("🚀 AWS BEDROCK CSV GENERATOR (Organized by Standard)")
        print("=" * 65)
        
        # Load all control data
        controls_data = self.load_control_data()
        
        if not controls_data:
            print("❌ No control data found. Make sure production JSON files exist.")
            return
        
        # Generate individual CSV files
        csv_files = self.generate_individual_csvs(controls_data)
        
        # Generate metadata template
        metadata_path = self.generate_metadata_json_template()
        
        print(f"\n📊 BEDROCK INGESTION FILES READY")
        print("=" * 65)
        print(f"📁 Output directory: {self.output_dir}")
        print(f"📄 Individual CSV files: {len(csv_files)} files")
        print(f"⚙️  Metadata template: {metadata_path}")
        print(f"📋 Total controls: {len(controls_data)}")
        
        # Show sample files
        if csv_files:
            print(f"\n📝 SAMPLE CSV FILES:")
            print("-" * 30)
            for i, csv_file in enumerate(csv_files[:3]):  # Show first 3
                print(f"  {csv_file.name}")
            if len(csv_files) > 3:
                print(f"  ... and {len(csv_files) - 3} more")
        
        # Show sample of CSV structure
        if controls_data:
            print(f"\n📋 SAMPLE CSV STRUCTURE (each file contains 1 control):")
            print("-" * 30)
            sample = controls_data[0]
            for key, value in sample.items():
                if key == 'content':
                    print(f"{key}: {value[:100]}...")
                elif key == 'testing_procedures':
                    print(f"{key}: {value[:80]}...")
                else:
                    print(f"{key}: {value}")
        
        print(f"\n🔗 USAGE:")
        print("1. Upload the entire pci_dss_4.0/ folder to your S3 bucket")
        print("   📁 s3://your-bucket/knowledge-base/pci_dss_4.0/")
        print("2. Each CSV file will be treated as a separate chunk by Bedrock")
        print("3. Apply the metadata template configuration to all CSV files")
        print("4. Configure Bedrock Knowledge Base to use this S3 location")
        print("5. Each control will be embedded as an individual chunk")
        print("\n📁 ORGANIZED STRUCTURE:")
        print("   ingest/bedrock/")
        print("   ├── pci_dss_4.0/           # PCI DSS v4.0 controls")
        print("   ├── iso27001/              # Future: ISO 27001 controls") 
        print("   ├── pci_aws_guidance/      # Future: PCI DSS AWS Guidance")
        print("   └── nist_csf/              # Future: NIST Cybersecurity Framework")
        print("\n💡 Benefits of organized structure:")
        print("   - Document-specific chunking and retrieval")
        print("   - Easy to add new compliance standards")
        print("   - Clear separation of different document types")
        print("   - Better metadata filtering in Bedrock queries")

def main():
    """Main execution function."""
    generator = BedrockCSVGenerator()
    generator.generate_bedrock_files()

if __name__ == "__main__":
    main() 