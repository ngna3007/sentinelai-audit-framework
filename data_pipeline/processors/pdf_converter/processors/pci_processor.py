"""PCI DSS processor for PDF conversion."""

from typing import Any, Dict

from .base_processor import BaseProcessor


class PCIProcessor(BaseProcessor):
    """Processor for PCI DSS compliance documents."""
    
    def preprocess(self, content: str) -> str:
        """Apply PCI DSS specific preprocessing to markdown content.
        
        Args:
            content: Raw markdown content from PDF conversion
            
        Returns:
            Processed markdown content optimized for PCI DSS
        """
        lines = content.split('\n')
        processed_lines = []
        
        for line in lines:
            # Clean up common PDF conversion artifacts
            line = line.strip()
            
            # Skip empty lines and page numbers
            if not line or line.isdigit():
                continue
            
            # Keep line for PCI DSS processing
            # PCI DSS uses minimal preprocessing to preserve compliance text integrity
            processed_lines.append(line)
        
        return '\n'.join(processed_lines)
    
    def enhance_quality_metrics(self, base_metrics: Dict[str, Any], content: str) -> Dict[str, Any]:
        """Enhance quality metrics with PCI DSS-specific assessments.
        
        Args:
            base_metrics: Base quality metrics from engine
            content: Processed content
            
        Returns:
            Enhanced quality metrics with PCI DSS-specific indicators
        """
        lines = content.split('\n')
        
        # Count PCI DSS specific elements
        pci_references = len([line for line in lines if 'pci' in line.lower()])
        requirement_references = len([line for line in lines if 'requirement' in line.lower()])
        control_references = len([line for line in lines if 'control' in line.lower()])
        testing_references = len([line for line in lines if 'test' in line.lower() or 'testing' in line.lower()])
        
        # PCI DSS-specific quality assessment
        pci_quality = 'excellent' if (pci_references >= 5 and requirement_references >= 10 and base_metrics.get('headers_detected', 0) >= 8) else \
                     'good' if (pci_references >= 2 and requirement_references >= 5 and base_metrics.get('headers_detected', 0) >= 4) else \
                     'acceptable' if (pci_references >= 1 and requirement_references >= 2) else \
                     'needs_review'
        
        # Enhance base metrics
        enhanced_metrics = {
            **base_metrics,
            'pci_references': pci_references,
            'requirement_references': requirement_references,
            'control_references': control_references,
            'testing_references': testing_references,
            'pci_quality_assessment': pci_quality,
            'document_focus': 'pci_dss_compliance',
            'processor': self.processor_name
        }
        
        return enhanced_metrics
    
    def enhance_metadata(self, base_metadata: Dict[str, Any], content: str) -> Dict[str, Any]:
        """Enhance metadata with PCI DSS-specific information.
        
        Args:
            base_metadata: Base metadata from engine
            content: Processed content
            
        Returns:
            Enhanced metadata with PCI DSS-specific details
        """
        enhanced_metadata = {
            **base_metadata,
            'document_type': self.document_type,
            'processor': self.processor_name,
            'optimized_for': 'PCI DSS compliance control extraction and RAG applications',
            'processing_features': [
                'compliance_text_preservation',
                'requirement_detection',
                'control_extraction',
                'testing_procedure_identification'
            ],
            'pci_enhancements': {
                'minimal_preprocessing': True,
                'text_integrity_preservation': True,
                'llm_optimization': True,
                'vector_search_ready': True
            }
        }
        
        return enhanced_metadata
    
    @property
    def document_type(self) -> str:
        """Document type identifier."""
        return 'PCI DSS Compliance'
    
    @property
    def processor_name(self) -> str:
        """Processor name."""
        return 'pci_dss'