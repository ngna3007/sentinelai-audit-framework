"""
Adapter to integrate AWS Config Rules guidance with centralized pipeline.

This adapter integrates the AWS Config Rules guidance processor with the main pipeline,
providing standardized interfaces for database generation and metadata handling.
"""

import sys
from pathlib import Path
from typing import Dict, Any
import time

# Fix path for imports
current_dir = Path(__file__).parent
sys.path.append(str(current_dir))

# Import core processors
from data_pipeline.processors.aws_guidance.core.database_data_generator import AWSConfigDataGenerator
from data_pipeline.processors.aws_guidance.pci_mapping.process_pci_mapping import PCIMappingProcessor

# Import shared schemas
from data_pipeline.schemas.compliance import (
    ControlExtractionResult, 
    ComplianceFramework, 
    QualityMetrics,
    ProcessingMetadata,
    CSVGenerationResult
)

class AWSGuidancePipelineAdapter:
    """
    Adapter to integrate AWS Config Rules guidance with centralized pipeline.
    
    This class provides a standardized interface for processing AWS Config Rules
    guidance data and generating database-friendly formats.
    """
    
    def __init__(self):
        self.framework = ComplianceFramework.AWS_CONFIG
        
    def process_config_rules(self, input_file: str, output_dir: str) -> CSVGenerationResult:
        """
        Process AWS Config Rules and generate database-friendly CSV.
        
        Args:
            input_file: Path to AWS Config rules mapping CSV
            output_dir: Output directory for processed files
        """
        start_time = time.time()
        
        try:
            # Use the database generator
            generator = AWSConfigDataGenerator(input_file=input_file, output_dir=output_dir)
            generator.generate_files()
            
            # Calculate processing time
            processing_time = time.time() - start_time
            
            # Get output files
            output_path = Path(output_dir)
            csv_files = list(output_path.glob("*.csv"))
            schema_file = output_path / "database_schema.json"
            
            return CSVGenerationResult(
                success=True,
                total_files=len(csv_files),
                output_directory=output_dir,
                chunk_strategy="rule_based",
                target_token_size=None,
                metadata_template_path=str(schema_file) if schema_file.exists() else None,
                processing_time=processing_time
            )
            
        except Exception as e:
            return CSVGenerationResult(
                success=False,
                total_files=0,
                output_directory=output_dir,
                chunk_strategy="rule_based",
                target_token_size=None,
                errors=[str(e)]
            )
    
    def process_pci_mappings(self, input_file: str = None, output_dir: str = None) -> CSVGenerationResult:
        """
        Process PCI DSS to AWS Config rule mappings.
        
        Args:
            input_file: Optional path to input JSON file
            output_dir: Optional path to output directory
        """
        start_time = time.time()
        
        try:
            # Use the PCI mapping processor
            processor = PCIMappingProcessor(input_file=input_file, output_dir=output_dir)
            processor.process_all()
            
            # Calculate processing time
            processing_time = time.time() - start_time
            
            # Get output files
            output_path = processor.output_dir
            csv_file = output_path / "pci_aws_config_rule_mapping.csv"
            schema_file = output_path / "database_schema.json"
            stats_file = output_path / "pci_aws_config_rule_mapping_stats.json"
            
            return CSVGenerationResult(
                success=True,
                total_files=3,  # CSV, schema, and stats files
                output_directory=str(output_path),
                chunk_strategy="control_based",
                target_token_size=None,
                metadata_template_path=str(schema_file) if schema_file.exists() else None,
                processing_time=processing_time
            )
            
        except Exception as e:
            return CSVGenerationResult(
                success=False,
                total_files=0,
                output_directory=str(output_dir) if output_dir else None,
                chunk_strategy="control_based",
                target_token_size=None,
                errors=[str(e)]
            )
    
    def get_supported_operations(self) -> list:
        """Get list of supported operations."""
        return ["process_config_rules", "process_pci_mappings"] 