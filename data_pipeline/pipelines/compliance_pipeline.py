"""
Centralized pipeline for compliance document processing.

This pipeline orchestrates the end-to-end process of extracting compliance
controls from documents. It uses existing extractors without modifying their
logic, providing a standardized interface for the centralized architecture.
"""

import sys
from pathlib import Path
from typing import Dict, Any, Optional
import time

# Add extractors to path
sys.path.append(str(Path(__file__).parent.parent))

from processors.compliance_standards.pci_dss.adapter import PCIDSSPipelineAdapter
from schemas.compliance import (
    ControlExtractionResult, 
    ComplianceFramework, 
    CSVGenerationResult,
    ValidationReport
)

class CompliancePipeline:
    """
    Orchestrates compliance document processing across all frameworks.
    
    This pipeline provides a centralized interface for extracting compliance
    controls while preserving all existing functionality of the original extractors.
    """
    
    def __init__(self, shared_data_path: str = "shared_data"):
        self.shared_data_path = Path(shared_data_path)
        self.adapters = {
            ComplianceFramework.PCI_DSS_V4: PCIDSSPipelineAdapter()
        }
    
    def process_pci_dss_document(
        self, 
        markdown_file: Optional[str] = None,
        pdf_file: Optional[str] = None,
        verbose: bool = False
    ) -> ControlExtractionResult:
        """
        Process PCI DSS document end-to-end using original extractor logic.
        
        This method orchestrates the full pipeline while preserving the exact
        functionality that successfully extracts 306 controls.
        """
        
        if verbose:
            print("🔄 Starting PCI DSS document processing...")
        
        # Resolve file paths
        if not markdown_file:
            markdown_file = str(self.shared_data_path / "documents" / "PCI-DSS-v4_0_1-FULL.md")
        
        # Convert PDF if provided and markdown doesn't exist
        if pdf_file and not Path(markdown_file).exists():
            adapter = self.adapters[ComplianceFramework.PCI_DSS_V4]
            if adapter.convert_pdf_to_markdown(pdf_file, markdown_file):
                if verbose:
                    print(f"✅ Converted PDF to Markdown: {markdown_file}")
            else:
                if verbose:
                    print(f"❌ Failed to convert PDF: {pdf_file}")
                # Create a failed result
                from schemas.compliance import QualityMetrics, ProcessingMetadata
                return ControlExtractionResult(
                    framework=ComplianceFramework.PCI_DSS_V4,
                    total_controls=0,
                    controls={},
                    quality_metrics=QualityMetrics(
                        completeness_score=0.0,
                        accuracy_score=0.0,
                        structure_score=0.0,
                        overall_score=0.0,
                        validation_notes=["PDF conversion failed"]
                    ),
                    extraction_metadata=ProcessingMetadata(
                        source_file=pdf_file,
                        processing_tool="centralized_pipeline",
                        processing_version="1.0.0",
                        framework_version="PCI_DSS_v4_0_1",
                        extraction_method="pdf_conversion"
                    ),
                    multi_table_controls=0,
                    requirements_breakdown={}
                )
        
        # Extract using adapter (preserves original logic)
        output_dir = str(self.shared_data_path / "outputs" / "pci_dss_v4" / "controls")
        adapter = self.adapters[ComplianceFramework.PCI_DSS_V4]
        result = adapter.extract_from_markdown(markdown_file, output_dir)
        
        if result.total_controls > 0 and verbose:
            print(f"✅ Extracted {result.total_controls} controls")
            print(f"📁 Saved to: {output_dir}")
            print(f"🔗 Multi-table controls: {result.multi_table_controls}")
            
            # Print requirements breakdown
            if result.requirements_breakdown:
                print("📊 Requirements breakdown:")
                for req, count in sorted(result.requirements_breakdown.items()):
                    print(f"   {req}: {count} controls")
        
        return result
    
    def generate_csv_for_bedrock(
        self,
        framework: ComplianceFramework = ComplianceFramework.PCI_DSS_V4,
        chunk_size: int = 300,
        verbose: bool = False
    ) -> CSVGenerationResult:
        """
        Generate CSV files for Bedrock Knowledge Base using original CSV generator.
        
        Uses the exact same BedrockCSVGenerator logic that produces 306 individual
        CSV files optimized for vector database ingestion.
        """
        
        if verbose:
            print("📊 Starting CSV generation for Bedrock...")
        
        if framework != ComplianceFramework.PCI_DSS_V4:
            # For future frameworks
            return CSVGenerationResult(
                success=False,
                total_files=0,
                output_directory="",
                chunk_strategy="unknown",
                target_token_size=chunk_size,
                errors=[f"Framework {framework} not supported yet"]
            )
        
        # Use PCI DSS adapter with original CSV generator
        controls_dir = str(self.shared_data_path / "outputs" / "pci_dss_v4" / "controls")
        output_dir = str(self.shared_data_path / "outputs" / "pci_dss_v4" / "bedrock")
        
        adapter = self.adapters[framework]
        result = adapter.generate_csv(controls_dir, output_dir, chunk_size)
        
        if result.success and verbose:
            print(f"✅ Generated {result.total_files} CSV files")
            print(f"📁 Output directory: {result.output_directory}")
            print(f"🔤 Chunk strategy: {result.chunk_strategy}")
            if result.metadata_template_path:
                print(f"📋 Metadata template: {result.metadata_template_path}")
        
        return result
    
    def run_complete_workflow(
        self,
        markdown_file: Optional[str] = None,
        pdf_file: Optional[str] = None,
        framework: ComplianceFramework = ComplianceFramework.PCI_DSS_V4,
        chunk_size: int = 300,
        verbose: bool = False
    ) -> tuple[ControlExtractionResult, CSVGenerationResult]:
        """
        Run the complete workflow: extract controls and generate CSV.
        
        This preserves the exact same workflow as the original system but
        through the centralized pipeline interface.
        """
        
        if verbose:
            print("🚀 Starting complete compliance workflow...")
            print("=" * 60)
        
        # Step 1: Extract controls
        extraction_result = self.process_pci_dss_document(
            markdown_file=markdown_file,
            pdf_file=pdf_file,
            verbose=verbose
        )
        
        # Step 2: Generate CSV (only if extraction succeeded)
        if extraction_result.total_controls > 0:
            if verbose:
                print("\n📊 Proceeding to CSV generation...")
            
            csv_result = self.generate_csv_for_bedrock(
                framework=framework,
                chunk_size=chunk_size,
                verbose=verbose
            )
        else:
            # Create failed CSV result
            csv_result = CSVGenerationResult(
                success=False,
                total_files=0,
                output_directory="",
                chunk_strategy="none",
                target_token_size=chunk_size,
                errors=["No controls extracted - skipping CSV generation"]
            )
        
        if verbose:
            print("\n🎉 Complete workflow finished!")
            print(f"📋 Controls extracted: {extraction_result.total_controls}")
            print(f"📊 CSV files generated: {csv_result.total_files}")
        
        return extraction_result, csv_result
    
    def validate_extraction_quality(
        self,
        framework: ComplianceFramework = ComplianceFramework.PCI_DSS_V4
    ) -> ValidationReport:
        """
        Validate the quality of extracted controls.
        
        Provides detailed quality assessment based on the standardized
        criteria for each compliance framework.
        """
        
        # Load controls from output directory
        controls_dir = self.shared_data_path / "outputs" / "pci_dss_v4" / "controls"
        
        if not controls_dir.exists():
            return ValidationReport(
                framework=framework,
                total_controls=0,
                validation_passed=False,
                overall_quality_score=0.0,
                recommendations=["Run extraction first - no controls found"]
            )
        
        # Count markdown files (actual controls)
        md_files = list(controls_dir.glob("control_*.md"))
        
        # Basic validation for PCI DSS
        expected_min_controls = 300  # We know PCI DSS should have 306
        validation_passed = len(md_files) >= expected_min_controls
        
        # Quality score based on control count
        if len(md_files) >= 306:
            quality_score = 100.0
        elif len(md_files) >= 300:
            quality_score = 95.0
        elif len(md_files) >= 250:
            quality_score = 80.0
        else:
            quality_score = 60.0
        
        recommendations = []
        if len(md_files) < expected_min_controls:
            recommendations.append(f"Expected at least {expected_min_controls} controls, found {len(md_files)}")
        if quality_score < 90:
            recommendations.append("Consider re-running extraction with verbose mode to check for issues")
        
        return ValidationReport(
            framework=framework,
            total_controls=len(md_files),
            validation_passed=validation_passed,
            overall_quality_score=quality_score,
            recommendations=recommendations
        )
    
    def get_supported_frameworks(self) -> list:
        """Get list of supported compliance frameworks."""
        return list(self.adapters.keys())
    
    def get_extraction_statistics(self) -> Dict[str, Any]:
        """Get statistics about the current extraction state."""
        
        stats = {}
        
        # PCI DSS statistics
        pci_controls_dir = self.shared_data_path / "outputs" / "pci_dss_v4" / "controls"
        pci_csv_dir = self.shared_data_path / "outputs" / "pci_dss_v4" / "bedrock"
        
        if pci_controls_dir.exists():
            md_files = list(pci_controls_dir.glob("control_*.md"))
            json_files = list(pci_controls_dir.glob("control_*_production.json"))
            
            stats["pci_dss_v4"] = {
                "markdown_files": len(md_files),
                "json_files": len(json_files),
                "csv_files": len(list(pci_csv_dir.glob("*.csv"))) if pci_csv_dir.exists() else 0,
                "last_extraction": "Available" if md_files else "Not run"
            }
        
        return stats 