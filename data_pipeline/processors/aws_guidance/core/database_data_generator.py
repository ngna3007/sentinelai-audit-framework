#!/usr/bin/env python3
"""
Database Data Generator for AWS Config Rules

Processes AWS Config rule mapping data into database-friendly format
with metadata and content chunks for PostgreSQL import.
"""

import csv
import json
import uuid
import pandas as pd
from pathlib import Path
from typing import Dict, List, Any

class AWSConfigDataGenerator:
    def __init__(self, input_file: str = None, output_dir: str = None):
        # Default to standard input location if not provided
        if input_file is None:
            base_dir = Path(__file__).parent.parent.parent.parent.parent
            input_file = base_dir / "shared_data" / "outputs" / "aws_config_guidance" / "aws_config_rule_full_mapping.csv"
        self.input_file = Path(input_file)
        
        # Use provided output directory or default to centralized directory
        if output_dir is not None:
            self.output_dir = Path(output_dir)
        else:
            base_dir = Path(__file__).parent.parent.parent.parent.parent
            self.output_dir = base_dir / "shared_data" / "outputs" / "aws_config_guidance" / "database_import"
            
    def load_config_data(self) -> List[Dict]:
        """Load and process AWS Config rule data."""
        # Read CSV file
        df = pd.read_csv(self.input_file)
        
        # Drop unnecessary columns
        df = df.drop(['client', 'function', 'keys_to_get', 'doc_link'], axis=1)
        
        # Create chunk column by combining config_rule and guidance
        df['chunk'] = df.apply(lambda row: f"Config Rule: {row['config_rule']}\n\nGuidance: {row['guidance']}", axis=1)
        
        # Generate records with UUID and metadata
        records = []
        for _, row in df.iterrows():
            record = {
                'id': str(uuid.uuid4()),
                'config_rule': row['config_rule'],
                'chunk': row['chunk'],
                'metadata': json.dumps({
                    'guidance': row['guidance'],
                    'service': row['service']
                })
            }
            records.append(record)
            
        return records

    def generate_single_csv(self, records: List[Dict]) -> Path:
        """Generate a single CSV file for PostgreSQL bulk import."""
        if not records:
            print("❌ No records to generate CSV")
            return None
        
        # Ensure output directory exists
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Define column order
        columns = [
            'id',           # UUID primary key
            'config_rule',  # Rule name
            'chunk',        # Combined content
            'metadata'      # JSON metadata
        ]
        
        # Create filename for single CSV
        csv_filename = "aws_config_rules_guidance.csv"
        csv_path = self.output_dir / csv_filename
        
        print(f"📝 Writing single CSV file for database import...")
        
        # Create DataFrame with all records
        df = pd.DataFrame(records, columns=columns)
        
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
        
        print(f"✅ Generated single CSV file with {len(records)} rules: {csv_path}")
        return csv_path

    def generate_database_schema_info(self):
        """Generate database schema information for PostgreSQL table creation."""
        schema_info = {
            "table_name": "aws_config_rules",
            "description": "AWS Config Rules with guidance for compliance management",
            "columns": [
                {
                    "name": "id",
                    "type": "UUID",
                    "description": "Unique rule identifier (generated UUID)",
                    "constraints": ["PRIMARY KEY", "NOT NULL"]
                },
                {
                    "name": "config_rule",
                    "type": "VARCHAR(100)",
                    "description": "AWS Config rule name",
                    "constraints": ["NOT NULL"]
                },
                {
                    "name": "chunk",
                    "type": "TEXT",
                    "description": "Combined rule description and guidance",
                    "constraints": ["NOT NULL"]
                },
                {
                    "name": "metadata",
                    "type": "JSONB",
                    "description": "Structured metadata including guidance and service",
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
                    "name": "idx_config_rule",
                    "type": "UNIQUE",
                    "columns": ["config_rule"],
                    "description": "Unique index for config rule lookups"
                },
                {
                    "name": "idx_metadata_gin",
                    "type": "GIN",
                    "columns": ["metadata"],
                    "description": "GIN index for efficient JSON queries"
                }
            ],
            "sample_queries": [
                "-- Get all rules for a specific service",
                "SELECT config_rule, metadata->>'guidance' FROM aws_config_rules WHERE metadata->>'service' = 'ec2';",
                "",
                "-- Full text search in rule content",
                "SELECT config_rule FROM aws_config_rules WHERE chunk ILIKE '%encryption%';",
                "",
                "-- Get rules with specific guidance patterns",
                "SELECT config_rule FROM aws_config_rules WHERE metadata->>'guidance' ILIKE '%backup%';"
            ]
        }
        
        schema_path = self.output_dir / "database_schema.json"
        
        print(f"🔧 Writing database schema info to {schema_path}")
        
        with open(schema_path, 'w', encoding='utf-8') as f:
            json.dump(schema_info, f, indent=2, ensure_ascii=False)
        
        print("✅ Generated database schema information for PostgreSQL")
        return schema_path

    def generate_files(self):
        """Generate all necessary files for database import."""
        print("🚀 AWS CONFIG RULES DATABASE GENERATOR")
        print("=" * 50)
        
        # Load and process data
        records = self.load_config_data()
        
        if not records:
            print("❌ No data found. Check input CSV file.")
            return
        
        # Generate CSV file
        csv_file = self.generate_single_csv(records)
        
        # Generate database schema
        schema_path = self.generate_database_schema_info()
        
        print(f"\n📊 DATABASE IMPORT FILES READY")
        print("=" * 50)
        print(f"📁 Output directory: {self.output_dir}")
        print(f"📄 CSV file: {csv_file.name}")
        print(f"⚙️  Schema file: {schema_path.name}")
        print(f"📋 Total rules: {len(records)}")
        
        # Show sample of CSV structure
        if records:
            print(f"\n📋 CSV STRUCTURE:")
            print("-" * 30)
            sample = records[0]
            print(f"id: {sample['id']}")
            print(f"config_rule: {sample['config_rule']}")
            print(f"chunk: {sample['chunk'][:100]}...")
            print(f"metadata: {sample['metadata'][:80]}...")
        
        print(f"\n💾 DATABASE IMPORT USAGE:")
        print("1. Create PostgreSQL table using the schema in database_schema.json")
        print("2. Use PostgreSQL COPY command for bulk import:")
        print(f"   COPY aws_config_rules FROM '{csv_file}' CSV HEADER;")
        print("3. Create indexes for efficient querying")
        print("4. Query using JSONB operators for metadata filtering")

def main():
    """Main execution function."""
    generator = AWSConfigDataGenerator()
    generator.generate_files()

if __name__ == "__main__":
    main() 