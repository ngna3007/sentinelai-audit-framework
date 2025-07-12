"""
Content Processor for AWS Config Guidance Documents

This module provides specialized content processing for AWS Config guidance documents,
focusing on extracting the PCI DSS to AWS Config rule mapping table.
"""

from pathlib import Path
from typing import Dict, List, Any, Optional
import re
import logging
from .text_processors import TextProcessor


class ContentProcessor:
    """
    Processes AWS Config guidance content to extract PCI DSS to AWS Config rule mappings.
    
    The processor focuses on the main table structure:
    |Control ID|Control Description|AWS Config Rule|Guidance|
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.text_processor = TextProcessor()
    
    def process_markdown(self, md_content: str) -> Dict[str, Any]:
        """
        Process AWS Config guidance markdown content to extract the mapping table.
        
        Args:
            md_content: Markdown content to process
            
        Returns:
            Dictionary containing structured AWS Config guidance data
        """
        self.logger.info("Processing AWS Config guidance markdown content")
        
        # Clean the content first
        cleaned_content = self._clean_content(md_content)
        
        # Extract the main mapping table
        mappings = self._extract_mapping_table(cleaned_content)
        
        # Generate summary statistics
        pci_controls = list(set([mapping['control_id'] for mapping in mappings]))
        config_rules = list(set([mapping['aws_config_rule'] for mapping in mappings]))
        
        # Generate compliance statistics
        compliance_stats = self._generate_compliance_statistics(mappings)
        
        # Create main mappings result
        mappings_result = {
            'document_type': 'aws_config_guidance',
            'total_mappings': len(mappings),
            'unique_pci_controls': len(pci_controls),
            'unique_config_rules': len(config_rules),
            'mappings': mappings
        }
        
        # Create separate metadata result
        metadata_result = {
            'document_type': 'aws_config_guidance',
            'summary': {
                'total_mappings': len(mappings),
                'unique_pci_controls': len(pci_controls),
                'unique_config_rules': len(config_rules)
            },
            'compliance_statistics': compliance_stats,
            'pci_controls': sorted(pci_controls),
            'config_rules': sorted(config_rules),
            'processing_metadata': {
                'total_characters': len(md_content),
                'total_lines': len(md_content.split('\n')),
                'cleaned_lines': len(cleaned_content.split('\n'))
            }
        }
        
        result = {
            'mappings': mappings_result,
            'metadata': metadata_result
        }
        
        self.logger.info(f"✅ Processed content: {len(mappings)} mappings, {len(pci_controls)} PCI controls, {len(config_rules)} Config rules")
        
        return result
    
    def _clean_content(self, md_content: str) -> str:
        """Clean the markdown content by removing headers, footers, and page artifacts."""
        lines = md_content.split('\n')
        cleaned_lines = []
        
        for line in lines:
            line = line.strip()
            
            # Skip empty lines
            if not line:
                continue
                
            # Skip headers and footers
            if self._is_header_footer(line):
                continue
                
            # Skip page numbers
            if line.isdigit():
                continue
                
            cleaned_lines.append(line)
        
        return '\n'.join(cleaned_lines)
    
    def _is_header_footer(self, line: str) -> bool:
        """Check if a line is a header or footer that should be removed."""
        line_lower = line.lower()
        
        # Headers
        if 'aws config developer guide' in line_lower:
            return True
            
        # Footers
        if 'operational best practices for pci dss' in line_lower:
            return True
            
        # Table headers (only remove if they appear multiple times)
        if line.startswith('**|Control ID|Control Description|AWS Config Rule|Guidance|**'):
            return True
            
        return False
    
    def _extract_mapping_table(self, content: str) -> List[Dict[str, Any]]:
        """Extract the PCI DSS to AWS Config rule mapping table."""
        mappings = []
        lines = content.split('\n')
        
        # Find table rows (lines that start with |)
        table_rows = []
        for line in lines:
            if line.startswith('|') and not line.startswith('|---|'):
                table_rows.append(line)
        
        # Process each table row
        for i, row in enumerate(table_rows):
            # Skip the header row
            if 'Control ID' in row and 'Control Description' in row:
                continue
                
            mapping = self._parse_table_row(row, i + 1)
            if mapping:
                mappings.append(mapping)
        
        return mappings
    
    def _parse_table_row(self, row: str, row_number: int) -> Optional[Dict[str, Any]]:
        """Parse a single table row into a mapping dictionary."""
        try:
            # Split by pipe and clean each cell
            cells = [cell.strip() for cell in row.split('|')]
            
            # Remove empty cells at start/end
            while cells and not cells[0]:
                cells.pop(0)
            while cells and not cells[-1]:
                cells.pop()
                
            # Should have exactly 4 cells
            if len(cells) != 4:
                self.logger.debug(f"Row {row_number}: Expected 4 cells, got {len(cells)}")
                return None
                
            # Clean each column with appropriate method
            control_id = self._clean_cell_content(cells[0])
            control_description = self._clean_cell_content(cells[1])
            aws_config_rule = self._clean_config_rule_content(cells[2])  # Special handling for config rules
            guidance = self._clean_cell_content(cells[3])
            
            # Validate that we have essential data
            if not control_id or not aws_config_rule:
                self.logger.debug(f"Row {row_number}: Missing essential data")
                return None
            
            # Extract compliance conditions from guidance
            compliance_info = self._extract_compliance_info(guidance)
            
            return {
                'control_id': control_id,
                'control_description': control_description,
                'aws_config_rule': aws_config_rule,
                'guidance': guidance,
                'row_number': row_number,
                'compliance_conditions': compliance_info
            }
            
        except Exception as e:
            self.logger.warning(f"Error parsing row {row_number}: {str(e)}")
            return None
    
    def _clean_cell_content(self, content: str) -> str:
        """Clean content from a table cell with intelligent br tag handling."""
        
        # First, handle <br> tags intelligently using text processor (without additional patterns)
        content = self.text_processor.clean_br_tags(content, remove_all=False)
        
        # Remove extra whitespace (normalize first, then apply specific patterns)
        content = re.sub(r'\s+', ' ', content)
        
        # Remove markdown formatting
        content = re.sub(r'\*\*(.*?)\*\*', r'\1', content)  # Remove bold
        content = re.sub(r'\*(.*?)\*', r'\1', content)      # Remove italic
        
        # Apply our specific whitespace cleaning patterns AFTER general normalization
        content = self.text_processor._clean_whitespace_patterns(content)
        
        # Fix common PDF conversion artifacts
        content = self._fix_common_word_breaks(content)
        
        return content.strip()
    
    def _clean_config_rule_content(self, content: str) -> str:
        """Clean AWS Config rule names - remove ALL br tags and ALL whitespace."""
        # For config rules, remove all <br> tags completely using text processor
        content = self.text_processor.clean_br_tags(content, remove_all=True)
        
        # Remove markdown formatting
        content = re.sub(r'\*\*(.*?)\*\*', r'\1', content)  # Remove bold
        content = re.sub(r'\*(.*?)\*', r'\1', content)      # Remove italic
        
        # Remove ALL whitespace (spaces, tabs, newlines) for config rule names
        content = re.sub(r'\s+', '', content)
        
        return content.strip()
    

    
    def _fix_common_word_breaks(self, content: str) -> str:
        """Fix common word break patterns that might remain."""
        
        # Common broken words to fix
        fixes = {
            r'\bcloudfront\b': 'CloudFront',
            r'\baws config\b': 'AWS Config',
            r'\bamazon\s+web\s+services\b': 'Amazon Web Services',
            r'\bnon_compliant\b': 'NON_COMPLIANT',
            r'\bnon compliant\b': 'NON_COMPLIANT',
            r'\bcompliant\s+if\b': 'COMPLIANT if',
            r'\bnon_compl\s+iant\b': 'NON_COMPLIANT',
            r'\bcloud\s*fron\s*t\b': 'CloudFront',
            r'\bapi\s+gateway\b': 'API Gateway',
            r'\bvpc\s*flow\s*logs\b': 'VPC Flow Logs',
            r'\bssl\s+certificate\b': 'SSL certificate',
            r'\bhttps\s+requests\b': 'HTTPS requests',
            
            # Specific word break fix requested by user
            r'\blogConﬁg\s+uration\b': 'logConﬁguration',
            r'\bINSUFFICI\s+ENT_DATA\b': 'INSUFFICIENT_DATA',
            
            # Fix spacing around technical terms
            r'\s+SSL\s+': ' SSL ',
            r'\s+HTTPS\s+': ' HTTPS ',
            r'\s+VPC\s+': ' VPC ',
            r'\s+IAM\s+': ' IAM ',
            r'\s+S3\s+': ' S3 ',
            r'\s+EC2\s+': ' EC2 ',
        }
        
        for pattern, replacement in fixes.items():
            content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
        
        return content
    
    def _extract_compliance_info(self, guidance: str) -> Dict[str, Any]:
        """Extract compliance conditions from guidance text."""
        # First remove <br> tags that might split the compliance keywords using text processor
        cleaned_guidance = self.text_processor.clean_br_tags(guidance, remove_all=True)
        
        # Simple detection - just check if NON_COMPLIANT or COMPLIANT appears in the cleaned text
        has_non_compliant = 'NON_COMPLIANT' in cleaned_guidance
        has_compliant = 'COMPLIANT' in cleaned_guidance and 'NON_COMPLIANT' not in cleaned_guidance
        
        return {
            'has_non_compliance_info': has_non_compliant,
            'has_compliance_info': has_compliant
        }
    
    def _generate_compliance_statistics(self, mappings: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate detailed compliance statistics for the mappings."""
        
        # Categorize mappings by compliance information
        has_non_compliance = []
        has_compliance = []
        has_both = []
        has_neither = []
        
        for mapping in mappings:
            compliance = mapping.get('compliance_conditions', {})
            has_non = compliance.get('has_non_compliance_info', False)
            has_comp = compliance.get('has_compliance_info', False)
            
            entry_info = {
                'control_id': mapping['control_id'],
                'aws_config_rule': mapping['aws_config_rule']
            }
            
            if has_non and has_comp:
                has_both.append(entry_info)
            elif has_non:
                has_non_compliance.append(entry_info)
            elif has_comp:
                has_compliance.append(entry_info)
            else:
                has_neither.append(entry_info)
        
        return {
            'has_non_compliance_only': {
                'count': len(has_non_compliance),
                'entries': has_non_compliance
            },
            'has_compliance_only': {
                'count': len(has_compliance),
                'entries': has_compliance
            },
            'has_both_compliance_types': {
                'count': len(has_both),
                'entries': has_both
            },
            'has_no_compliance_info': {
                'count': len(has_neither),
                'entries': has_neither
            },
            'summary': {
                'total_with_non_compliance': len(has_non_compliance) + len(has_both),
                'total_with_compliance': len(has_compliance) + len(has_both),
                'total_with_any_compliance_info': len(has_non_compliance) + len(has_compliance) + len(has_both),
                'total_without_compliance_info': len(has_neither)
            }
        }

    
    def extract_unique_pci_controls(self, mappings: List[Dict[str, Any]]) -> List[str]:
        """Extract unique PCI DSS control IDs from mappings."""
        return sorted(list(set([mapping['control_id'] for mapping in mappings])))
    
    def extract_unique_config_rules(self, mappings: List[Dict[str, Any]]) -> List[str]:
        """Extract unique AWS Config rule names from mappings."""
        return sorted(list(set([mapping['aws_config_rule'] for mapping in mappings])))
    
    def group_by_pci_control(self, mappings: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """Group mappings by PCI DSS control ID."""
        grouped = {}
        for mapping in mappings:
            control_id = mapping['control_id']
            if control_id not in grouped:
                grouped[control_id] = []
            grouped[control_id].append(mapping)
        return grouped
    
    def group_by_config_rule(self, mappings: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """Group mappings by AWS Config rule name."""
        grouped = {}
        for mapping in mappings:
            rule_name = mapping['aws_config_rule']
            if rule_name not in grouped:
                grouped[rule_name] = []
            grouped[rule_name].append(mapping)
        return grouped 