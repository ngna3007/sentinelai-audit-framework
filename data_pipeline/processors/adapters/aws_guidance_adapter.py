"""
Adapter to integrate AWS Config Rules guidance with centralized pipeline.

This adapter integrates the AWS Config Rules guidance processor with the main pipeline,
providing standardized interfaces for database generation and metadata handling.
"""

from pathlib import Path
from typing import Dict, Any, List
from time import time

# Import with fallback for direct execution
try:
    from data_pipeline.output_generators.aws_guidance.csv_generator import AWSConfigCSVGenerator
    from data_pipeline.schemas.compliance import (
        ControlExtractionResult, 
        ComplianceFramework, 
        QualityMetrics,
        ProcessingMetadata,
        CSVGenerationResult
    )
except ImportError:
    import sys
    from pathlib import Path
    sys.path.append(str(Path(__file__).parent.parent.parent))
    from output_generators.aws_guidance.csv_generator import AWSConfigCSVGenerator
    from schemas.compliance import (
        ControlExtractionResult, 
        ComplianceFramework, 
        QualityMetrics,
        ProcessingMetadata,
        CSVGenerationResult
    )

from ..utils.pci_mapping.process_pci_mapping import PCIMappingProcessor


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
        start_time = time()
        
        try:
            # Use the database generator
            generator = AWSConfigDataGenerator(input_file=input_file, output_dir=output_dir)
            generator.generate_files()
            
            # Calculate processing time
            processing_time = time() - start_time
            
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
        start_time = time()
        
        try:
            # Use the PCI mapping processor
            processor = PCIMappingProcessor(input_file=input_file, output_dir=output_dir)
            processor.process_all()
            
            # Calculate processing time
            processing_time = time() - start_time
            
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
    
    def get_supported_operations(self) -> List[str]:
        """Get list of supported operations."""
        return ["process_config_rules", "process_pci_mappings"]