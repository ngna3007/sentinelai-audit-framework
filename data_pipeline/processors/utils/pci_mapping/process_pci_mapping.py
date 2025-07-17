#!/usr/bin/env python3
"""
Process PCI DSS to AWS Config Rule Mappings

This script processes the PCI DSS control to AWS Config rule mappings,
extracting relevant data and generating database-friendly formats.
"""

from json import load, dump
from uuid import uuid4
from pathlib import Path
from typing import Dict, List, Any
import csv

class PCIMappingProcessor:
    def __init__(self, input_file: str = None, output_dir: str = None):
        # Default input file location
        if input_file is None:
            base_dir = Path(__file__).parent.parent.parent.parent.parent
            input_file = base_dir / "shared_data" / "outputs" / "aws_config_guidance" / "processed_data" / "unique_pci_controls.json"
        self.input_file = Path(input_file)
        
        # Default output directory
        if output_dir is None:
            base_dir = Path(__file__).parent.parent.parent.parent.parent
            output_dir = base_dir / "shared_data" / "outputs" / "pci_aws_config_rule_mapping"
        self.output_dir = Path(output_dir)
        
    def process_mapping_data(self) -> tuple[List[Dict], Dict]:
        """Process the mapping data and extract relevant information."""
        with open(self.input_file, 'r', encoding='utf-8') as f:
            data = load(f)
            
        # Extract stats
        stats = data['extraction_info']
        
        # Process control mappings
        mappings = []
        for control in data['unique_pci_controls']:
            # Create a single mapping per control with array of rules
            mapping = {
                'id': str(uuid4()),
                'control_id': control['control_id'],
                'config_rules': [
                    {
                        'rule_name': rule['aws_config_rule'],
                        'guidance': rule['guidance']
                    }
                    for rule in control['aws_config_rules']
                ]
            }
            mappings.append(mapping)
                
        return mappings, stats
    
    def save_stats(self, stats: Dict):
        """Save extraction statistics to a JSON file."""
        self.output_dir.mkdir(parents=True, exist_ok=True)
        stats_file = self.output_dir / "pci_aws_config_rule_mapping_stats.json"
        
        with open(stats_file, 'w', encoding='utf-8') as f:
            dump(stats, f, indent=2)
            
    def generate_database_schema(self) -> Dict:
        """Generate database schema information for PostgreSQL."""
        schema = {
            "table_name": "pci_aws_config_rule_mappings",
            "description": "Mapping between PCI DSS controls and AWS Config rules",
            "columns": [
                {
                    "name": "id",
                    "type": "UUID",
                    "description": "Unique mapping identifier",
                    "constraints": ["PRIMARY KEY", "NOT NULL"]
                },
                {
                    "name": "control_id",
                    "type": "VARCHAR(20)",
                    "description": "PCI DSS control identifier (e.g., '1.1.1', 'A1.1.1')",
                    "constraints": ["NOT NULL", "UNIQUE"]
                },
                {
                    "name": "config_rules",
                    "type": "JSONB",
                    "description": "Array of AWS Config rules with guidance",
                    "constraints": ["NOT NULL"]
                }
            ],
            "indexes": [
                {
                    "name": "idx_pci_mapping_id",
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
                    "name": "idx_config_rules",
                    "type": "GIN",
                    "columns": ["config_rules"],
                    "description": "GIN index for searching within config rules array"
                }
            ],
            "sample_queries": [
                "-- Get all AWS Config rules for a PCI control",
                "SELECT control_id, config_rules FROM pci_aws_config_rule_mappings WHERE control_id = '1.1.1';",
                "",
                "-- Get all PCI controls that use a specific AWS Config rule",
                "SELECT control_id FROM pci_aws_config_rule_mappings WHERE config_rules @> '[{\"rule_name\": \"cloudtrail-enabled\"}]';",
                "",
                "-- Get controls with rules containing specific guidance text",
                "SELECT control_id, config_rules FROM pci_aws_config_rule_mappings WHERE config_rules @> '[{\"guidance\": \"%encryption%\"}]';",
                "",
                "-- Get all unique AWS Config rules",
                "SELECT DISTINCT jsonb_array_elements(config_rules)->>'rule_name' as rule_name FROM pci_aws_config_rule_mappings;"
            ]
        }
        
        # Save schema
        self.output_dir.mkdir(parents=True, exist_ok=True)
        schema_file = self.output_dir / "database_schema.json"
        
        with open(schema_file, 'w', encoding='utf-8') as f:
            dump(schema, f, indent=2)
            
        return schema
    
    def generate_csv(self, mappings: List[Dict]) -> Path:
        """Generate CSV file for database import."""
        self.output_dir.mkdir(parents=True, exist_ok=True)
        csv_file = self.output_dir / "pci_aws_config_rule_mapping.csv"
        
        # Define columns
        columns = ['id', 'control_id', 'config_rules']
        
        # Convert mappings for CSV (JSON encode config_rules)
        csv_mappings = [
            {
                'id': m['id'],
                'control_id': m['control_id'],
                'config_rules': dump(m['config_rules'])
            }
            for m in mappings
        ]
        
        # Write CSV
        with open(csv_file, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=columns)
            writer.writeheader()
            writer.writerows(csv_mappings)
            
        return csv_file
    
    def process_all(self):
        """Process all data and generate output files."""
        print("🔄 Processing PCI DSS to AWS Config Rule Mappings")
        print("=" * 60)
        
        # Process data
        mappings, stats = self.process_mapping_data()
        
        # Save stats
        self.save_stats(stats)
        print(f"✅ Saved statistics to: {self.output_dir}/pci_aws_config_rule_mapping_stats.json")
        
        # Generate schema
        schema = self.generate_database_schema()
        print(f"✅ Generated database schema: {self.output_dir}/database_schema.json")
        
        # Generate CSV
        csv_file = self.generate_csv(mappings)
        print(f"✅ Generated CSV file: {csv_file}")
        print(f"📊 Processed {len(mappings)} mappings")
        
        # Print summary
        print("\n📋 Output Summary")
        print("-" * 30)
        print(f"📁 Output directory: {self.output_dir}")
        print(f"📄 Files generated:")
        print("  • pci_aws_config_rule_mapping.csv")
        print("  • pci_aws_config_rule_mapping_stats.json")
        print("  • database_schema.json")
        
        # Print sample mapping
        if mappings:
            print("\n📝 Sample Mapping:")
            sample = mappings[0]
            print(f"Control ID: {sample['control_id']}")
            print(f"Config Rules: {sample['config_rules']}")

def main():
    """Main execution function."""
    processor = PCIMappingProcessor()
    processor.process_all()

if __name__ == "__main__":
    main()