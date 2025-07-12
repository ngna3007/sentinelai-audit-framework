#!/usr/bin/env python3
"""
Example Usage of PCI DSS to AWS Config Rule Mapping Processor

This script demonstrates how to use the PCIMappingProcessor to:
1. Process PCI DSS control to AWS Config rule mappings
2. Generate database-friendly CSV format
3. Create database schema and statistics
"""

import sys
from pathlib import Path

# Add project root to Python path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent))

from data_pipeline.processors.aws_guidance.pci_mapping.process_pci_mapping import PCIMappingProcessor

def example_with_default_paths():
    """Example using default input/output paths."""
    print("Example 1: Using Default Paths")
    print("=" * 50)
    
    processor = PCIMappingProcessor()
    processor.process_all()

def example_with_custom_paths():
    """Example using custom input/output paths."""
    print("\nExample 2: Using Custom Paths")
    print("=" * 50)
    
    # Define custom paths
    input_file = "path/to/custom/unique_pci_controls.json"
    output_dir = "path/to/custom/output"
    
    processor = PCIMappingProcessor(
        input_file=input_file,
        output_dir=output_dir
    )
    processor.process_all()

def main():
    """Run examples."""
    # Example with default paths
    example_with_default_paths()
    
    # Example with custom paths (commented out as paths don't exist)
    # example_with_custom_paths()

if __name__ == "__main__":
    main() 