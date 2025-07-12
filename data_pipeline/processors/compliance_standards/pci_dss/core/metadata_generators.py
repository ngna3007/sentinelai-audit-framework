"""
Metadata Generators for PCI DSS Control Extraction

This module handles:
- Validation metadata generation for debugging and analysis
- Production metadata generation for database/vector search
- Metadata formatting and standardization
- Quality metrics and validation checks
"""

import json
import uuid
from typing import Dict, Any, List
from pathlib import Path
from .content_builders import ProductionContentFormatter
from .text_processors import SectionExtractor


class ValidationMetadataGenerator:
    """Generates metadata for validation, debugging, and analysis purposes."""
    
    @staticmethod
    def generate_validation_metadata(control_id: str, control_data: Dict, content: str) -> Dict[str, Any]:
        """Generate comprehensive validation metadata for debugging and analysis."""
        return {
            'control_id': control_id,
            'sections': control_data.get('sections', {}),
            'row_count': len(control_data['rows']),
            'table_count': len(control_data['tables']),
            'spans_multiple_tables': len(control_data['tables']) > 1,
            'token_count': ProductionContentFormatter.count_tokens(content),
            'content_length_chars': len(content),
            'content_lines': len(content.split('\n')),
            'has_testing_procedures': 'Testing Procedures:' in content,
            'has_guidance': 'Guidance:' in content,
            'has_requirements': 'Defined Approach Requirements:' in content,
            'table_sources': [
                {
                    'table_index': i,
                    'start_line': table.get('start_line', -1),
                    'end_line': table.get('end_line', -1),
                    'header': table.get('header', ''),
                    'row_count': len(table.get('rows', []))
                }
                for i, table in enumerate(control_data['tables'])
            ]
        }
    
    @staticmethod
    def analyze_extraction_quality(validation_metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze the quality of the extraction based on validation metadata."""
        quality_score = 0
        max_score = 100
        issues = []
        
        # Content length analysis (30 points)
        content_length = validation_metadata['content_length_chars']
        if content_length < 100:
            issues.append("Content too short (< 100 chars)")
        elif content_length < 500:
            quality_score += 10
            issues.append("Content somewhat short (< 500 chars)")
        elif content_length <= 3000:
            quality_score += 30  # Optimal range
        elif content_length <= 5000:
            quality_score += 20
            issues.append("Content somewhat long (> 3000 chars)")
        else:
            quality_score += 10
            issues.append("Content very long (> 5000 chars)")
        
        # Section completeness (40 points)
        sections = validation_metadata['sections']
        required_sections = ['requirements', 'testing_procedures']
        optional_sections = ['purpose', 'examples', 'good_practice']
        
        for section in required_sections:
            if sections.get(section, False):
                quality_score += 15
            else:
                issues.append(f"Missing required section: {section}")
        
        optional_count = sum(1 for section in optional_sections if sections.get(section, False))
        quality_score += min(optional_count * 3, 10)  # Up to 10 points for optional sections
        
        # Table structure (20 points)
        if validation_metadata['table_count'] == 0:
            issues.append("No tables found")
        elif validation_metadata['table_count'] == 1:
            quality_score += 20  # Single table is ideal
        else:
            quality_score += 15  # Multi-table is acceptable but slightly lower score
            
        # Row count assessment (10 points)
        row_count = validation_metadata['row_count']
        if row_count == 0:
            issues.append("No rows extracted")
        elif row_count < 3:
            quality_score += 5
            issues.append("Very few rows extracted")
        elif row_count <= 10:
            quality_score += 10  # Optimal range
        else:
            quality_score += 8
            issues.append("Many rows extracted - might include noise")
        
        return {
            'quality_score': quality_score,
            'max_score': max_score,
            'quality_percentage': (quality_score / max_score) * 100,
            'issues': issues,
            'recommendations': ValidationMetadataGenerator._generate_recommendations(issues, validation_metadata)
        }
    
    @staticmethod
    def _generate_recommendations(issues: List[str], validation_metadata: Dict[str, Any]) -> List[str]:
        """Generate improvement recommendations based on identified issues."""
        recommendations = []
        
        for issue in issues:
            if "Content too short" in issue:
                recommendations.append("Check if control content is being fully extracted from tables")
            elif "Missing required section" in issue and "requirements" in issue:
                recommendations.append("Verify that Defined Approach Requirements are being properly extracted")
            elif "Missing required section" in issue and "testing_procedures" in issue:
                recommendations.append("Check testing procedures extraction logic for this control")
            elif "No tables found" in issue:
                recommendations.append("Verify that table parsing is working for this control's source")
            elif "Many rows extracted" in issue:
                recommendations.append("Review row filtering logic to reduce noise")
        
        return recommendations


class ProductionMetadataGenerator:
    """Generates metadata for production use in databases and vector search."""
    
    @staticmethod
    def generate_production_metadata(control_id: str, content: str, requirement: str = "") -> Dict[str, Any]:
        """Generate production metadata for database/vector search storage with UUID primary key."""
        has_testing_procedures = 'Testing Procedures:' in content
        
        # Generate UUID for primary key
        record_id = str(uuid.uuid4())
        
        return {
            'id': record_id,  # UUID primary key
            'control_id': control_id,
            'chunk': content,
            'requirement': requirement,  # New field for extracted requirement text
            'metadata': {
                'control_id': control_id,
                'standard': 'PCI-DSS-v4.0',
                'source': 'PCI_DSS_PDF_v4.0',
                'control_category': ProductionMetadataGenerator._categorize_control(control_id),
                'has_testing_procedures': has_testing_procedures,
                'requirements_id': ProductionMetadataGenerator._extract_requirements_id(control_id)
            }
        }
    
    @staticmethod
    def _extract_requirements_id(control_id: str) -> str:
        """Extract the requirements ID from control ID."""
        if control_id.startswith('A'):
            # Handle appendix controls like A1.1.1 -> A1, A2.1.1 -> A2
            return control_id[:2]  # A1, A2, A3, etc.
        else:
            # Handle regular controls like 1.1.1 -> 1, 11.1.1 -> 11
            major = control_id.split('.')[0]
            return major
    
    @staticmethod
    def _categorize_control(control_id: str) -> str:
        """Categorize the control based on its ID."""
        if control_id.startswith('A'):
            return 'appendix'
        
        # Extract the major requirement number
        major = control_id.split('.')[0]
        try:
            major_num = int(major)
            categories = {
                1: 'network_security',
                2: 'system_configuration',
                3: 'data_protection',
                4: 'encryption_transit',
                5: 'malware_protection',
                6: 'secure_development',
                7: 'access_control_general',
                8: 'user_identification',
                9: 'physical_access',
                10: 'logging_monitoring',
                11: 'security_testing',
                12: 'information_security_policy'
            }
            return categories.get(major_num, 'unknown')
        except ValueError:
            return 'unknown'
    
    @staticmethod
    def _determine_requirement_level(control_id: str) -> str:
        """Determine the level of the requirement (main, sub, sub-sub, etc.)."""
        if control_id.startswith('A'):
            # Appendix requirements
            parts = control_id[1:].split('.')  # Remove 'A' prefix
        else:
            parts = control_id.split('.')
        
        if len(parts) == 2:
            return 'main'
        elif len(parts) == 3:
            return 'sub'
        elif len(parts) == 4:
            return 'sub_sub'
        else:
            return 'detailed'


class MetadataFileManager:
    """Manages saving and loading metadata files."""
    
    @staticmethod
    def save_validation_metadata(control_id: str, metadata: Dict[str, Any], output_dir: Path):
        """Save validation metadata to file."""
        output_dir.mkdir(exist_ok=True)
        validate_file = output_dir / f"control_{control_id}_validate.json"
        
        with open(validate_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2)
    
    @staticmethod
    def save_production_metadata(control_id: str, metadata: Dict[str, Any], output_dir: Path):
        """Save production metadata to file."""
        output_dir.mkdir(exist_ok=True)
        production_file = output_dir / f"control_{control_id}_production.json"
        
        with open(production_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2)
    
    @staticmethod
    def load_validation_metadata(control_id: str, input_dir: Path) -> Dict[str, Any]:
        """Load validation metadata from file."""
        validate_file = input_dir / f"control_{control_id}_validate.json"
        
        if not validate_file.exists():
            raise FileNotFoundError(f"Validation metadata not found: {validate_file}")
        
        with open(validate_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    @staticmethod
    def load_production_metadata(control_id: str, input_dir: Path) -> Dict[str, Any]:
        """Load production metadata from file."""
        production_file = input_dir / f"control_{control_id}_production.json"
        
        if not production_file.exists():
            raise FileNotFoundError(f"Production metadata not found: {production_file}")
        
        with open(production_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    @staticmethod
    def generate_extraction_summary(output_dir: Path) -> Dict[str, Any]:
        """Generate a summary of all extracted controls."""
        output_dir = Path(output_dir)
        
        # Find all validation metadata files
        validate_files = list(output_dir.glob("*_validate.json"))
        
        if not validate_files:
            return {'error': 'No validation metadata files found'}
        
        summary = {
            'total_controls': len(validate_files),
            'controls_by_category': {},
            'quality_distribution': {'high': 0, 'medium': 0, 'low': 0},
            'common_issues': {},
            'extraction_stats': {
                'avg_content_length': 0,
                'avg_token_count': 0,
                'avg_table_count': 0,
                'multi_table_controls': 0
            }
        }
        
        total_content_length = 0
        total_token_count = 0
        total_table_count = 0
        
        for validate_file in validate_files:
            with open(validate_file, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
            
            # Categorize control
            control_id = metadata['control_id']
            category = ProductionMetadataGenerator._categorize_control(control_id)
            summary['controls_by_category'][category] = summary['controls_by_category'].get(category, 0) + 1
            
            # Analyze quality if available
            if 'quality_analysis' in metadata:
                quality_pct = metadata['quality_analysis']['quality_percentage']
                if quality_pct >= 80:
                    summary['quality_distribution']['high'] += 1
                elif quality_pct >= 60:
                    summary['quality_distribution']['medium'] += 1
                else:
                    summary['quality_distribution']['low'] += 1
                
                # Track common issues
                for issue in metadata['quality_analysis'].get('issues', []):
                    summary['common_issues'][issue] = summary['common_issues'].get(issue, 0) + 1
            
            # Accumulate stats
            total_content_length += metadata.get('content_length_chars', 0)
            total_token_count += metadata.get('token_count', 0)
            total_table_count += metadata.get('table_count', 0)
            
            if metadata.get('spans_multiple_tables', False):
                summary['extraction_stats']['multi_table_controls'] += 1
        
        # Calculate averages
        count = len(validate_files)
        summary['extraction_stats']['avg_content_length'] = total_content_length // count
        summary['extraction_stats']['avg_token_count'] = total_token_count // count
        summary['extraction_stats']['avg_table_count'] = total_table_count / count
        
        return summary 