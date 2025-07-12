#!/usr/bin/env python3
"""
Example usage of AWS Config Rules Database Generator

This script demonstrates how to use the AWSConfigDataGenerator
to process AWS Config rules into a database-friendly format.
"""

import sys
from pathlib import Path

# Add the project root to Python path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent))

from data_pipeline.processors.aws_guidance.core.database_data_generator import AWSConfigDataGenerator

def main():
    """Example usage of the database data generator."""
    
    # Basic usage with default paths
    generator = AWSConfigDataGenerator()
    generator.generate_files()
    
    # Custom input/output paths
    custom_generator = AWSConfigDataGenerator(
        input_file="path/to/custom/aws_config_rule_mapping.csv",
        output_dir="path/to/custom/output"
    )
    custom_generator.generate_files()

if __name__ == "__main__":
    main() 