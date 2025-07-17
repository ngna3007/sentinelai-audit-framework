"""AWS Config guidance processor for PDF conversion."""

import re
from typing import Any, Dict

from .base_processor import BaseProcessor


class AWSProcessor(BaseProcessor):
    """Processor for AWS Config guidance documents."""
    
    def preprocess(self, content: str) -> str:
        """Apply AWS Config specific preprocessing to markdown content.
        
        Args:
            content: Raw markdown content from PDF conversion
            
        Returns:
            Processed markdown content optimized for AWS Config guidance
        """
        lines = content.split('\n')
        processed_lines = []
        
        for line in lines:
            # Clean up common PDF conversion artifacts
            line = line.strip()
            
            # Skip empty lines and page numbers
            if not line or line.isdigit():
                continue
                
            # Fix hyphenated words split across lines
            if line.endswith('-'):
                line = line[:-1]  # Remove trailing hyphen
                
            # Enhance AWS Config rule references
            if 'config rule' in line.lower() or 'aws config' in line.lower():
                line = f"**{line}**"  # Emphasize Config rule references
                
            # Standardize AWS service names
            line = re.sub(r'AWS\s+Config', 'AWS Config', line, flags=re.IGNORECASE)
            line = re.sub(r'PCI\s+DSS', 'PCI DSS', line, flags=re.IGNORECASE)
            
            processed_lines.append(line)
        
        return '\n'.join(processed_lines)
    
    def enhance_quality_metrics(self, base_metrics: Dict[str, Any], content: str) -> Dict[str, Any]:
        """Enhance quality metrics with AWS-specific assessments.
        
        Args:
            base_metrics: Base quality metrics from engine
            content: Processed content
            
        Returns:
            Enhanced quality metrics with AWS-specific indicators
        """
        lines = content.split('\n')
        
        # Count AWS Config specific elements
        config_references = len([line for line in lines if 'config' in line.lower()])
        aws_references = len([line for line in lines if 'aws' in line.lower()])
        compliance_references = len([line for line in lines if 'compliance' in line.lower() or 'compliant' in line.lower()])
        rule_references = len([line for line in lines if 'rule' in line.lower()])
        
        # AWS-specific quality assessment
        aws_quality = 'excellent' if (config_references >= 5 and aws_references >= 10 and base_metrics.get('headers_detected', 0) >= 10) else \
                     'good' if (config_references >= 2 and aws_references >= 5 and base_metrics.get('headers_detected', 0) >= 5) else \
                     'acceptable' if (config_references >= 1 and aws_references >= 2) else \
                     'needs_review'
        
        # Enhance base metrics
        enhanced_metrics = {
            **base_metrics,
            'config_references': config_references,
            'aws_references': aws_references,
            'compliance_references': compliance_references,
            'rule_references': rule_references,
            'aws_quality_assessment': aws_quality,
            'document_focus': 'aws_config_guidance',
            'processor': self.processor_name
        }
        
        return enhanced_metrics
    
    def enhance_metadata(self, base_metadata: Dict[str, Any], content: str) -> Dict[str, Any]:
        """Enhance metadata with AWS-specific information.
        
        Args:
            base_metadata: Base metadata from engine
            content: Processed content
            
        Returns:
            Enhanced metadata with AWS-specific details
        """
        enhanced_metadata = {
            **base_metadata,
            'document_type': self.document_type,
            'processor': self.processor_name,
            'optimized_for': 'AWS Config rule mapping and compliance guidance',
            'processing_features': [
                'config_rule_detection',
                'compliance_mapping',
                'implementation_guidance',
                'aws_service_standardization'
            ],
            'aws_enhancements': {
                'config_rule_emphasis': True,
                'service_name_standardization': True,
                'hyphen_cleanup': True,
                'compliance_focus': True
            }
        }
        
        return enhanced_metadata
    
    @property
    def document_type(self) -> str:
        """Document type identifier."""
        return 'AWS Config Guidance'
    
    @property
    def processor_name(self) -> str:
        """Processor name."""
        return 'aws_guidance'