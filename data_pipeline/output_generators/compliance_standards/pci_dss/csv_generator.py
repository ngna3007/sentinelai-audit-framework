#!/usr/bin/env python3
"""
CSV Generator for PCI DSS Database Import

Combines PCI DSS control production metadata and content into CSV format
for PostgreSQL database bulk import. Supports both single CSV and individual 
file generation for different use cases.
"""

from csv import QUOTE_ALL
from json import dumps, dump, load
from pathlib import Path
from typing import Dict, List

import pandas as pd


class PCIDSSCSVGenerator:
    def __init__(self, controls_dir: str = None, output_dir: str = None):
        # Default to organized extracted controls if no path provided
        if controls_dir is None:
            # Go up from pci_dss/ to compliance_standards/ to output_generators/ to data_pipeline/ to project root/
            base_dir = Path(__file__).parent.parent.parent.parent.parent
            controls_dir = base_dir / "shared_data" / "outputs" / "pci_dss_v4" / "controls"
        self.controls_dir = Path(controls_dir)
        
        # Use provided output directory or default to centralized directory
        if output_dir is not None:
            self.output_dir = Path(output_dir)
        else:
            # Go up from pci_dss/ to compliance_standards/ to output_generators/ to data_pipeline/ to project root/
            base_dir = Path(__file__).parent.parent.parent.parent.parent
            self.output_dir = base_dir / "shared_data" / "outputs" / "pci_dss_v4" / "database_import"
        
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
                metadata = load(f)
            
            # Use the new UUID structure with 'id' as primary key
            control_data = {
                'id': metadata['id'],  # UUID primary key
                'control_id': metadata['control_id'],
                'chunk': metadata['chunk'],
                'requirement': metadata.get('requirement', ''),  # New requirement field
                'metadata': dumps(metadata['metadata'])  # Convert metadata dict to JSON string for CSV
            }
            
            controls_data.append(control_data)
        
        return controls_data
    
    def generate_single_csv(self, controls_data: List[Dict]) -> Path:
        """Generate a single CSV file containing all controls for PostgreSQL bulk import."""
        if not controls_data:
            print("❌ No controls data to generate CSV")
            return None
        
        # Ensure output directory exists
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Define column order (chunk field last for clarity)
        columns = [
            'id',        # UUID primary key
            'control_id',
            'requirement',  # New requirement field
            'chunk',     # Main content field
            'metadata'   # JSON string containing all metadata
        ]
        
        # Create filename for single CSV
        csv_filename = "pci_dss_controls.csv"
        csv_path = self.output_dir / csv_filename
        
        print(f"📝 Writing single CSV file for database import...")
        
        # Create DataFrame with all controls
        df = pd.DataFrame(controls_data, columns=columns)
        
        # Write to CSV with proper handling of multiline content
        df.to_csv(
            csv_path,
            index=False,              # Don't include row index
            encoding='utf-8',         # UTF-8 encoding  
            quoting=QUOTE_ALL,        # Quote all fields for safety
            lineterminator='\n',      # Consistent line endings
            doublequote=True,         # Handle quotes properly
            quotechar='"',            # Use double quotes
            escapechar=None           # Let pandas handle escaping
        )
        
        print(f"✅ Generated single CSV file with {len(controls_data)} controls: {csv_path}")
        return csv_path

    def generate_individual_csvs(self, controls_data: List[Dict]) -> List[Path]:
        """Generate individual CSV files for each control (optional for specific use cases)."""
        if not controls_data:
            print("❌ No controls data to generate CSVs")
            return []
        
        # Ensure output directory exists
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Define column order (chunk field last for clarity)
        columns = [
            'id',        # UUID primary key
            'control_id',
            'requirement',  # New requirement field
            'chunk',     # Main content field
            'metadata'   # JSON string containing all metadata
        ]
        
        csv_files = []
        print(f"📝 Writing individual CSV files...")
        
        for control in controls_data:
            # Create filename: control_1.1.1.csv
            csv_filename = f"control_{control['control_id']}.csv"
            csv_path = self.output_dir / csv_filename
            
            # Create single-row DataFrame for this control
            df = pd.DataFrame([control], columns=columns)
            
            # Write to CSV with proper handling of multiline content
            df.to_csv(
                csv_path,
                index=False,              # Don't include row index
                encoding='utf-8',         # UTF-8 encoding  
                quoting=QUOTE_ALL,        # Quote all fields for safety
                lineterminator='\n',      # Consistent line endings
                doublequote=True,         # Handle quotes properly
                quotechar='"',            # Use double quotes
                escapechar=None           # Let pandas handle escaping
            )
            
            csv_files.append(csv_path)
        
        print(f"✅ Generated {len(csv_files)} individual CSV files")
        return csv_files
    
    def generate_database_schema_info(self):
        """Generate database schema information for PostgreSQL table creation."""
        schema_info = {
            "table_name": "pci_dss_controls",
            "description": "PCI DSS v4.0.1 controls extracted for compliance management",
            "columns": [
                {
                    "name": "id",
                    "type": "UUID",
                    "description": "Unique control identifier (generated UUID)",
                    "constraints": ["PRIMARY KEY", "NOT NULL"]
                },
                {
                    "name": "control_id",
                    "type": "VARCHAR(20)",
                    "description": "Unique control identifier (e.g., '1.1.1', 'A1.1.1')",
                    "constraints": ["NOT NULL"]
                },
                {
                    "name": "requirement",
                    "type": "TEXT",
                    "description": "Extracted requirement text from Defined Approach Requirements section",
                    "constraints": []
                },
                {
                    "name": "chunk",
                    "type": "TEXT",
                    "description": "Full control content including requirements, procedures, and guidance",
                    "constraints": ["NOT NULL"]
                },
                {
                    "name": "metadata",
                    "type": "JSONB",
                    "description": "Structured metadata including standard, source, category, etc.",
                    "constraints": ["NOT NULL"]
                }
            ],
            "indexes": [
                {
                    "name": "idx_id",
                    "type": "PRIMARY",
                    "columns": ["id"]
                },
                {
                    "name": "idx_control_id",
                    "type": "UNIQUE",
                    "columns": ["control_id"],
                    "description": "Unique index for control_id lookups"
                },
                {
                    "name": "idx_metadata_gin",
                    "type": "GIN",
                    "columns": ["metadata"],
                    "description": "GIN index for efficient JSON queries"
                }
            ],
            "sample_queries": [
                "-- Get all controls for requirement 1",
                "SELECT * FROM pci_dss_controls WHERE (metadata->>'requirements_id') = '1';",
                "",
                "-- Search for controls with testing procedures",
                "SELECT control_id, metadata->>'control_category' FROM pci_dss_controls WHERE (metadata->>'has_testing_procedures')::boolean = true;",
                "",
                "-- Full text search in control content",
                "SELECT control_id FROM pci_dss_controls WHERE chunk ILIKE '%network security%';"
            ]
        }
        
        schema_path = self.output_dir / "database_schema.json"
        
        print(f"🔧 Writing database schema info to {schema_path}")
        
        with open(schema_path, 'w', encoding='utf-8') as f:
            dump(schema_info, f, indent=2, ensure_ascii=False)
        
        print("✅ Generated database schema information for PostgreSQL")
        return schema_path
    
    def generate_csv_files(self, individual_files: bool = False):
        """Generate CSV files for database import (single CSV by default, individual files optional)."""
        print("🚀 CSV GENERATOR FOR DATABASE IMPORT")
        print("=" * 50)
        
        # Load all control data
        controls_data = self.load_control_data()
        
        if not controls_data:
            print("❌ No control data found. Make sure production JSON files exist.")
            return
        
        # Generate CSV files based on preference
        if individual_files:
            print("📝 Generating individual CSV files...")
            csv_files = self.generate_individual_csvs(controls_data)
            result_info = {
                'type': 'individual',
                'files': csv_files,
                'count': len(csv_files)
            }
        else:
            print("📝 Generating single CSV file for bulk import...")
            csv_file = self.generate_single_csv(controls_data)
            result_info = {
                'type': 'single',
                'file': csv_file,
                'count': 1
            }
        
        # Generate database schema information
        schema_path = self.generate_database_schema_info()
        
        print(f"\n📊 DATABASE IMPORT FILES READY")
        print("=" * 50)
        print(f"📁 Output directory: {self.output_dir}")
        
        if individual_files:
            print(f"📄 Individual CSV files: {result_info['count']} files")
            print(f"📝 Main file: pci_dss_controls_individual/")
        else:
            print(f"📄 Single CSV file: {result_info['file'].name}")
            print(f"📝 Ready for: COPY pci_dss_controls FROM '{result_info['file']}'")
        
        print(f"⚙️  Database schema: {schema_path}")
        print(f"📋 Total controls: {len(controls_data)}")
        
        # Show sample of CSV structure
        if controls_data:
            print(f"\n📋 CSV STRUCTURE:")
            print("-" * 30)
            sample = controls_data[0]
            print(f"id: {sample['id']}")
            print(f"control_id: {sample['control_id']}")
            print(f"chunk: {sample['chunk'][:100]}...")
            print(f"metadata: {sample['metadata'][:80]}...")
        
        print(f"\n💾 DATABASE IMPORT USAGE:")
        print("1. Create PostgreSQL table using the schema in database_schema.json")
        if individual_files:
            print("2. Use individual CSV files for targeted imports or testing")
            print("3. Combine files if needed: cat control_*.csv > combined.csv")
        else:
            print("2. Use PostgreSQL COPY command for bulk import:")
            print(f"   COPY pci_dss_controls FROM '{result_info['file'] if not individual_files else 'pci_dss_controls.csv'}' CSV HEADER;")
        print("3. Create indexes for efficient querying (see schema file)")
        print("4. Query using JSONB operators for metadata filtering")
        
        print(f"\n🗃️  DATABASE STRUCTURE:")
        print("   database_import/")
        print("   ├── pci_dss_controls.csv        # Main import file")
        print("   ├── database_schema.json        # Table creation info")
        print("   └── individual/                 # Optional individual files")
        
        print(f"\n💡 Benefits for database import:")
        print("   - Single CSV file for efficient bulk import")
        print("   - JSONB metadata for flexible querying")
        print("   - Proper PostgreSQL data types")
        print("   - Sample queries included in schema")

    # Backward compatibility method
    def generate_bedrock_files(self):
        """Legacy method for backward compatibility - redirects to generate_csv_files with individual files."""
        print("⚠️  generate_bedrock_files() is deprecated. Use generate_csv_files() instead.")
        self.generate_csv_files(individual_files=True)


def main():
    """Main execution function."""
    generator = PCIDSSCSVGenerator()
    generator.generate_csv_files()


if __name__ == "__main__":
    main()