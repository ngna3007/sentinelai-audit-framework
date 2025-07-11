"""
Document Extractors for Compliance Frameworks

This package contains modular extractors for various compliance and regulatory frameworks.
Each framework has its own specialized extractor with a modular architecture for easy maintenance.

Available Extractors:
- pci_dss_v4_0_1: PCI DSS v4.0.1 Requirements Document extractor (modular architecture)

Usage:
    # Use the main CLI interface
    python -m extractors.pci_dss_v4_0_1.main extract
    
    # Or import specific components
    from extractors.pci_dss_v4_0_1.core import ControlExtractor

Future extractors may include:
- iso_27001: ISO 27001:2013/2022 controls
- sox: Sarbanes-Oxley requirements  
- hipaa: HIPAA security requirements
- gdpr: GDPR compliance requirements
"""

# Import framework-specific extractors
from . import pci_dss_v4_0_1

__all__ = [
    'pci_dss_v4_0_1',
]
