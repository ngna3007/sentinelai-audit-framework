"""
Base schemas for all data pipeline operations.

This module defines the foundational data structures used across
all extractors, transformers, and loaders in the data pipeline.
"""

from pydantic import BaseModel
from typing import Dict, List, Any, Optional
from enum import Enum
from datetime import datetime

class ProcessingStatus(str, Enum):
    """Status of processing operations."""
    PENDING = "pending"
    PROCESSING = "processing" 
    COMPLETED = "completed"
    FAILED = "failed"

class ExtractionResult(BaseModel):
    """Standard result format for all extraction operations."""
    success: bool
    total_items: int
    data: Dict[str, Any]
    metadata: Dict[str, Any]
    errors: List[str] = []
    processing_time: Optional[float] = None
    timestamp: datetime = datetime.now()

class QualityMetrics(BaseModel):
    """Quality assessment metrics for extracted data."""
    completeness_score: float  # 0-100
    accuracy_score: float      # 0-100  
    structure_score: float     # 0-100
    overall_score: float       # 0-100
    validation_notes: List[str] = []

class ProcessingMetadata(BaseModel):
    """Metadata about processing operations."""
    source_file: str
    processing_tool: str
    processing_version: str
    framework_version: str
    extraction_method: str
    quality_metrics: Optional[QualityMetrics] = None 