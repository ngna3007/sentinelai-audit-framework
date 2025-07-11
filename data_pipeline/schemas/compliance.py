"""
Compliance-specific schemas for requirements and controls.

This module defines standardized data structures for compliance
frameworks like PCI DSS, ISO27001, NIST CSF, etc.
"""

from .base import ExtractionResult, QualityMetrics, ProcessingMetadata
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from enum import Enum

class ComplianceFramework(str, Enum):
    """Supported compliance frameworks."""
    PCI_DSS_V4 = "PCI_DSS_v4_0_1"
    ISO27001 = "ISO27001"
    NIST_CSF = "NIST_CSF"
    SOC2 = "SOC2"

class RequirementStatus(str, Enum):
    """Status of compliance requirements."""
    ACTIVE = "active"
    DEPRECATED = "deprecated"
    DRAFT = "draft"
    SUPERSEDED = "superseded"

class RequirementSchema(BaseModel):
    """Standard schema for compliance requirements across all frameworks."""
    req_id: str
    framework: ComplianceFramework
    title: str
    content: str
    testing_procedures: List[str] = []
    guidance: Optional[str] = None
    applicability_notes: Optional[str] = None
    status: RequirementStatus = RequirementStatus.ACTIVE
    
    # Quality and metadata
    quality_score: float = 0.0
    token_count: int = 0
    section_count: int = 0
    
    # Source tracking
    source_tables: List[int] = []
    source_pages: List[int] = []
    is_multi_table: bool = False

class ControlExtractionResult(BaseModel):
    """Result from control extraction process."""
    framework: ComplianceFramework
    total_controls: int
    controls: Dict[str, Any]  # Keep flexible to preserve original extractor format
    quality_metrics: QualityMetrics
    extraction_metadata: ProcessingMetadata
    
    # Processing statistics
    multi_table_controls: int = 0
    requirements_breakdown: Dict[str, int] = {}  # e.g., {"Requirement 1": 19, ...}

class CSVGenerationResult(BaseModel):
    """Result from CSV generation for vector databases."""
    success: bool
    total_files: int
    output_directory: str
    chunk_strategy: str
    target_token_size: int
    metadata_template_path: Optional[str] = None
    errors: List[str] = []

class ValidationReport(BaseModel):
    """Comprehensive validation report for extracted controls."""
    framework: ComplianceFramework
    total_controls: int
    validation_passed: bool
    overall_quality_score: float
    
    # Detailed breakdown
    controls_with_issues: List[str] = []
    missing_sections: Dict[str, List[str]] = {}  # control_id: [missing_sections]
    quality_distribution: Dict[str, int] = {}  # score_range: count
    
    # Recommendations
    recommendations: List[str] = [] 