"""
PCI DSS v4.0 document splitter implementation with improved control extraction.

This splitter handles the hierarchical structure of PCI DSS documents,
preserving complete control IDs, testing procedures, and guidance sections.
Enhanced with proper header/footer removal and page metadata tracking.
"""

import re
from typing import List, Optional, Dict, Tuple, Any
from pathlib import Path
from .base import BaseSplitter, Chunk
from datetime import datetime, timezone

# Import enhanced PDF processor for improved extraction
try:
    from ..processors.enhanced_pdf_processor import EnhancedPDFProcessor, ExtractionStrategy
    ENHANCED_EXTRACTION_AVAILABLE = True
except ImportError:
    ENHANCED_EXTRACTION_AVAILABLE = False


class PCISplitter(BaseSplitter):
    """Enhanced splitter for PCI DSS v4.0 documents with improved control extraction."""
    
    def __init__(self, max_tokens: int = 350, overlap_tokens: int = 50, use_enhanced_extraction: bool = True):
        super().__init__(max_tokens, overlap_tokens)
        
        # Initialize logger
        import logging
        self.logger = logging.getLogger(__name__)
        
        # Enhanced patterns for PCI DSS structure
        self.main_control_pattern = re.compile(r'(?<!v)(\d+\.\d+\.\d+)\s+(?![a-z])', re.MULTILINE)
        self.sub_control_pattern = re.compile(r'(?<!v)(\d+\.\d+\.\d+[a-z])\s+', re.MULTILINE)
        
        # Improved page boundary detection
        self.page_marker_pattern = re.compile(r'\[PAGE\s+(\d+)\]', re.IGNORECASE)
        self.control_marker_pattern = re.compile(r'===\s*CONTROL\s+(\d+\.\d+\.\d+).*?===', re.IGNORECASE)
        
        # Section patterns for complete control extraction
        self.section_patterns = {
            'requirements': re.compile(r'(?i)(requirements?\s+and\s+testing\s+procedures?|defined\s+approach\s+requirements?)', re.MULTILINE),
            'testing': re.compile(r'(?i)(defined\s+approach\s+testing\s+procedures?|testing\s+procedures?)', re.MULTILINE),
            'customized': re.compile(r'(?i)(customized\s+approach\s+objective)', re.MULTILINE),
            'applicability': re.compile(r'(?i)(applicability\s+notes)', re.MULTILINE),
            'purpose': re.compile(r'(?i)(purpose)', re.MULTILINE),
            'guidance': re.compile(r'(?i)(good\s+practice)', re.MULTILINE),
            'examples': re.compile(r'(?i)(examples?)', re.MULTILINE)
        }
        
        # Initialize enhanced PDF processor
        self.use_enhanced_extraction = use_enhanced_extraction and ENHANCED_EXTRACTION_AVAILABLE
        self.enhanced_processor = None
        self._extraction_strategy = ExtractionStrategy.HYBRID
        
        if self.use_enhanced_extraction:
            try:
                self.enhanced_processor = EnhancedPDFProcessor()
            except Exception as e:
                self.logger.warning(f"Failed to initialize enhanced PDF processor: {e}")
                self.use_enhanced_extraction = False
        
    def get_standard_name(self) -> str:
        return "pci-dss"
    
    def split_document(
        self, 
        content: str, 
        source_document: str, 
        preserve_structure: bool = True,
        pdf_path: Optional[Path] = None,
        semantic_splitting: bool = False,
        **kwargs
    ) -> List[Chunk]:
        """
        Split PCI DSS document using improved control-first approach.
        
        Args:
            content: Document content to split
            source_document: Source document identifier
            preserve_structure: Whether to preserve document structure
            pdf_path: Path to PDF file (for enhanced extraction)
            semantic_splitting: Whether to split controls into semantic sections
            
        Returns:
            List of chunks with complete controls and page metadata
        """
        self.logger.info(f"Starting improved PCI DSS splitting for {source_document}")
        self.logger.info(f"Enhanced extraction: {self.is_enhanced_extraction_available()}")
        
        # Use enhanced extraction if available and PDF provided
        if self.is_enhanced_extraction_available() and pdf_path:
            self.logger.info("Using enhanced PDF extraction with cleanup")
            content = self._extract_with_enhanced_processor(pdf_path)
        
        # Extract complete controls with page metadata
        self.logger.info("Phase 1: Extracting complete controls with page tracking")
        complete_controls = self._extract_complete_controls_with_pages(content)
        
        # Validate extraction quality
        self.logger.info(f"Phase 2: Validation - Found {len(complete_controls)} controls")
        self._validate_control_extraction(complete_controls)
        
        # Create chunks with page metadata
        self.logger.info(f"Phase 3: Creating chunks with page metadata")
        chunks = self._create_enhanced_control_chunks(
            complete_controls, 
            source_document, 
            semantic_splitting=semantic_splitting
        )
        
        self.logger.info(f"Enhanced splitting complete: {len(chunks)} chunks created")
        return chunks
    
    def _extract_complete_controls_with_pages(self, content: str) -> Dict[str, Dict]:
        """
        Extract complete controls with page metadata tracking.
        Uses a two-phase approach to handle complex table structures.
        
        Returns:
            Dict mapping control_id -> {'content': str, 'sections': dict, 'metadata': dict}
        """
        lines = content.split('\n')
        
        # Phase 1: Find all valid control starts and their positions
        self.logger.debug("Phase 1: Identifying all valid control positions")
        control_positions = self._find_all_control_positions(lines)
        
        # Phase 2: Extract content ranges for each control
        self.logger.debug("Phase 2: Extracting content for each control")
        controls = self._extract_control_content_ranges(lines, control_positions)
        
        # Clean up and validate controls
        cleaned_controls = {}
        for control_id, control_data in controls.items():
            if self._is_complete_valid_control(control_id, control_data):
                cleaned_controls[control_id] = control_data
            else:
                self.logger.debug(f"Removing incomplete control {control_id}: {control_data.get('metadata', {}).get('rejection_reason', 'unknown')}")
        
        self.logger.info(f"Extracted {len(cleaned_controls)} complete controls with page metadata")
        return cleaned_controls

    def _find_all_control_positions(self, lines: List[str]) -> List[Dict]:
        """Find all valid control start positions in the document."""
        control_positions = []
        current_page = 1
        
        for i, line in enumerate(lines):
            line_stripped = line.strip()
            
            # Track page changes
            page_match = self.page_marker_pattern.search(line)
            if page_match:
                current_page = int(page_match.group(1))
                continue
            
            # Check for enhanced control markers
            control_match = self.control_marker_pattern.search(line)
            if control_match:
                control_id = control_match.group(1)
                control_positions.append({
                    'control_id': control_id,
                    'line_index': i,
                    'page_number': current_page,
                    'line_content': line_stripped,
                    'marker_type': 'enhanced'
                })
                continue
            
            # Check for natural control boundaries
            main_match = self.main_control_pattern.match(line_stripped)
            if main_match and self._is_valid_control_start(line_stripped, lines, i):
                control_id = main_match.group(1)
                control_positions.append({
                    'control_id': control_id,
                    'line_index': i,
                    'page_number': current_page,
                    'line_content': line_stripped,
                    'marker_type': 'natural'
                })
        
        self.logger.debug(f"Found {len(control_positions)} valid control positions")
        return control_positions

    def _extract_control_content_ranges(self, lines: List[str], control_positions: List[Dict]) -> Dict[str, Dict]:
        """Extract content for each control using intelligent range detection."""
        controls = {}
        
        for i, position in enumerate(control_positions):
            control_id = position['control_id']
            start_line = position['line_index']
            page_number = position['page_number']
            
            # Determine end line for this control
            end_line = self._determine_control_end_line(lines, position, control_positions, i)
            
            # Extract content for this control
            control_content = self._extract_single_control_content(
                lines, start_line, end_line, control_id, page_number
            )
            
            # Merge with existing control if it already exists (handle duplicates)
            if control_id in controls:
                controls[control_id] = self._merge_control_content(
                    controls[control_id], control_content
                )
            else:
                controls[control_id] = control_content
        
        return controls

    def _determine_control_end_line(self, lines: List[str], current_position: Dict, 
                                   all_positions: List[Dict], position_index: int) -> int:
        """Determine where the current control's content ends with improved boundary detection."""
        start_line = current_position['line_index']
        control_id = current_position['control_id']
        
        # Get the control family (e.g., "1.1" from "1.1.1")
        control_parts = control_id.split('.')
        control_family = '.'.join(control_parts[:2]) if len(control_parts) >= 2 else control_id
        
        # Look for a logical stopping point
        max_look_ahead = 80  # Reduced for tighter boundaries
        
        for offset in range(1, max_look_ahead):
            line_index = start_line + offset
            if line_index >= len(lines):
                return len(lines)
            
            line = lines[line_index].strip()
            if not line:
                continue
            
            # Enhanced control boundary detection
            other_control_match = self.main_control_pattern.search(line)
            if other_control_match:
                other_control_id = other_control_match.group(1)
                other_parts = other_control_id.split('.')
                other_family = '.'.join(other_parts[:2]) if len(other_parts) >= 2 else other_control_id
                
                # Always stop at different control families
                if other_family != control_family:
                    self.logger.debug(f"Control {control_id}: Stopping at different family {other_family} (line {line_index})")
                    return line_index
                
                # For same family, stop if it's a different specific control AND has substantial content
                if other_control_id != control_id:
                    # Look ahead a few lines to see if this is a substantial control start
                    look_ahead_content = ""
                    for la_offset in range(3):
                        if line_index + la_offset < len(lines):
                            look_ahead_content += lines[line_index + la_offset] + " "
                    
                    # If substantial content follows, this is likely a new control
                    if len(look_ahead_content.strip()) > 100:
                        self.logger.debug(f"Control {control_id}: Stopping at substantial control {other_control_id} (line {line_index})")
                        return line_index
            
            # Stop at definitive section boundaries
            section_boundaries = [
                'requirement and testing procedures',
                'requirements and testing procedures', 
                'defined approach requirements',
                'requirement 2',  # Next major requirement
                'requirement 3',
                'requirement 4',
                'requirement 5',
                'requirement 6',
                'requirement 7',
                'requirement 8',
                'requirement 9',
                'requirement 10',
                'requirement 11',
                'requirement 12'
            ]
            
            line_lower = line.lower()
            for boundary in section_boundaries:
                if boundary in line_lower and offset > 15:  # Only after some content
                    self.logger.debug(f"Control {control_id}: Stopping at section boundary '{boundary}' (line {line_index})")
                    return line_index
            
            # Special case: Stop at numbered requirement sections
            if re.match(r'^\d+\.\d+\s+[A-Z]', line) and offset >= 8:  # e.g., "1.3 Network access"
                self.logger.debug(f"Control {control_id}: Stopping at numbered section (line {line_index})")
                return line_index
            
            # Specific pattern for major control transitions
            major_control_patterns = [
                r'^1\.3\s+Network\s+access',
                r'^2\.1\s+',
                r'^3\.1\s+',
                r'^4\.1\s+',
                r'^5\.1\s+',
                r'^6\.1\s+',
                r'^7\.1\s+',
                r'^8\.1\s+',
                r'^9\.1\s+',
                r'^10\.1\s+',
                r'^11\.1\s+',
                r'^12\.1\s+'
            ]
            
            for pattern in major_control_patterns:
                if re.match(pattern, line, re.IGNORECASE) and offset >= 8:
                    self.logger.debug(f"Control {control_id}: Stopping at major control pattern '{pattern}' (line {line_index})")
                    return line_index
        
        # Use next control position if available and it's a different family
        if position_index + 1 < len(all_positions):
            next_position = all_positions[position_index + 1]
            next_control_family = '.'.join(next_position['control_id'].split('.')[:2])
            
            # If next control is different family, use its position
            if next_control_family != control_family:
                self.logger.debug(f"Control {control_id}: Using next control position for different family {next_control_family}")
                return next_position['line_index']
        
        return start_line + max_look_ahead

    def _extract_single_control_content(self, lines: List[str], start_line: int, 
                                       end_line: int, control_id: str, page_number: int) -> Dict:
        """Extract and process content for a single control."""
        
        # Collect all lines for this control
        control_lines = []
        for i in range(start_line, min(end_line, len(lines))):
            line = lines[i].strip()
            if line and not self.page_marker_pattern.search(line):  # Skip page markers
                control_lines.append(line)
        
        content = '\n'.join(control_lines)
        
        # Create the control dictionary
        return self._create_enhanced_control_dict(control_id, content, page_number)

    def _merge_control_content(self, existing_control: Dict, new_control: Dict) -> Dict:
        """Merge content from duplicate control instances."""
        
        # Combine content, avoiding duplication
        existing_content = existing_control['content']
        new_content = new_control['content']
        
        # Only merge if new content adds substantial value
        if len(new_content) > len(existing_content):
            # New content is longer, use it as primary
            merged_content = new_content
        elif len(new_content) > 100 and new_content not in existing_content:
            # New content is substantial and different, append it
            merged_content = existing_content + '\n\n' + new_content
        else:
            # Keep existing content
            merged_content = existing_content
        
        # Update the control with merged content
        existing_control['content'] = merged_content
        existing_control['character_count'] = len(merged_content)
        existing_control['line_count'] = len([line for line in merged_content.split('\n') if line.strip()])
        
        # Re-analyze sections with merged content
        existing_control['sections'] = self._analyze_complete_control_sections(merged_content)
        
        # Update metadata
        existing_control['metadata'] = self._extract_complete_control_metadata(
            existing_control['control_id'], 
            merged_content, 
            existing_control['sections'], 
            existing_control['page_number']
        )
        
        return existing_control
    
    def _is_valid_control_start(self, line: str, lines: List[str], line_index: int) -> bool:
        """Enhanced validation for control start detection."""
        
        # Extract control ID and following text
        match = self.main_control_pattern.match(line)
        if not match:
            return False
        
        control_id = match.group(1)
        remaining_text = line[match.end():].strip()
        
        # More lenient content length requirement
        if len(remaining_text) < 5:
            return False
        
        # Check for obvious invalid patterns first
        invalid_patterns = [
            r'^\(continued\)$',  # Just "(continued)"
            r'^page\s+\d+$',     # Just "page X"  
            r'^\.{3,}$',         # Just dots
            r'^-+$'              # Just dashes
        ]
        
        for pattern in invalid_patterns:
            if re.match(pattern, remaining_text.lower()):
                return False
        
        # Look ahead for control-related content
        look_ahead = min(15, len(lines) - line_index - 1)
        following_lines = lines[line_index + 1:line_index + 1 + look_ahead]
        following_text = ' '.join(line.strip() for line in following_lines).lower()
        
        # Comprehensive indicators of a real control
        strong_indicators = [
            'configuration', 'files', 'nsc', 'network security', 
            'firewall', 'router', 'must', 'shall', 'ensure',
            'examine', 'verify', 'testing', 'procedure', 'interview',
            'observe', 'review', 'documented', 'implemented'
        ]
        
        medium_indicators = [
            'requirement', 'implement', 'establish', 'maintain',
            'protect', 'secure', 'document', 'policy', 'process',
            'system', 'access', 'control', 'data', 'security'
        ]
        
        weak_indicators = [
            'are', 'is', 'all', 'any', 'that', 'this', 'with',
            'accordance', 'specified', 'elements', 'standards'
        ]
        
        # Count indicators in both current line and following content
        full_context = (remaining_text + ' ' + following_text).lower()
        
        strong_count = sum(1 for indicator in strong_indicators if indicator in full_context)
        medium_count = sum(1 for indicator in medium_indicators if indicator in full_context)
        weak_count = sum(1 for indicator in weak_indicators if indicator in full_context)
        
        # More lenient validation logic
        if strong_count >= 1:
            return True  # Any strong indicator is good
        elif medium_count >= 2:
            return True  # Multiple medium indicators
        elif medium_count >= 1 and weak_count >= 2:
            return True  # One medium + multiple weak
        elif len(remaining_text) >= 20 and medium_count >= 1:
            return True  # Substantial content + one medium indicator
        
        # Special case: If line contains specific control patterns
        control_specific_patterns = [
            f'{control_id}\\s+(examine|verify|interview|observe)',
            r'(policies|procedures|standards|requirements).*are',
            r'(documented|implemented|maintained|established)',
            r'accordance\s+with.*elements'
        ]
        
        for pattern in control_specific_patterns:
            if re.search(pattern, full_context, re.IGNORECASE):
                return True
        
        return False
    
    def _create_enhanced_control_dict(self, control_id: str, content: str, page_number: int) -> Dict:
        """Create enhanced control dictionary with complete metadata."""
        
        # Analyze control sections
        sections = self._analyze_complete_control_sections(content)
        
        # Extract comprehensive metadata
        metadata = self._extract_complete_control_metadata(control_id, content, sections, page_number)
        
        return {
            'control_id': control_id,
            'content': content.strip(),
            'sections': sections,
            'metadata': metadata,
            'page_number': page_number,
            'character_count': len(content.strip()),
            'line_count': len([line for line in content.split('\n') if line.strip()])
        }
    
    def _analyze_complete_control_sections(self, content: str) -> Dict[str, Dict]:
        """Analyze complete control content to identify all sections."""
        
        sections = {
            'main_requirement': {'content': '', 'start_pos': -1, 'end_pos': -1, 'found': False},
            'testing_procedures': {'content': '', 'start_pos': -1, 'end_pos': -1, 'found': False},
            'customized_approach': {'content': '', 'start_pos': -1, 'end_pos': -1, 'found': False},
            'applicability_notes': {'content': '', 'start_pos': -1, 'end_pos': -1, 'found': False},
            'purpose': {'content': '', 'start_pos': -1, 'end_pos': -1, 'found': False},
            'good_practice': {'content': '', 'start_pos': -1, 'end_pos': -1, 'found': False},
            'examples': {'content': '', 'start_pos': -1, 'end_pos': -1, 'found': False}
        }
        
        content_lower = content.lower()
        
        # Enhanced section detection patterns
        section_patterns = {
            'main_requirement': [
                r'(\d+\.\d+\.\d+)\s+[A-Z]',  # Control ID followed by requirement text
                r'configuration\s+files\s+for\s+nscs',  # Specific to 1.2.8
            ],
            'testing_procedures': [
                r'(\d+\.\d+\.\d+)\s+examine',
                r'examine\s+configuration\s+files',
                r'verify.*accordance.*requirement'
            ],
            'customized_approach': [
                r'customized\s+approach\s+objective',
                r'nscs\s+cannot\s+be\s+defined'
            ],
            'applicability_notes': [
                r'applicability\s+notes',
                r'any\s+file\s+or\s+setting\s+used'
            ],
            'purpose': [
                r'purpose\s*:',
                r'to\s+prevent\s+unauthorized'
            ],
            'good_practice': [
                r'good\s+practice',
                r'keeping\s+configuration\s+information'
            ],
            'examples': [
                r'examples?\s*:',
                r'if\s+the\s+secure\s+configuration'
            ]
        }
        
        for section_name, patterns in section_patterns.items():
            for pattern in patterns:
                matches = list(re.finditer(pattern, content_lower))
                if matches:
                    first_match = matches[0]
                    sections[section_name]['start_pos'] = first_match.start()
                    sections[section_name]['found'] = True
                    
                    # Extract substantial content around the match
                    start = max(0, first_match.start() - 20)
                    # Look for next section or end of content
                    end = min(len(content), first_match.end() + 300)
                    
                    # Try to find natural end point
                    extract = content[start:end]
                    sentences = extract.split('.')
                    if len(sentences) > 3:
                        # Take first few complete sentences
                        extract = '.'.join(sentences[:3]) + '.'
                    
                    sections[section_name]['content'] = extract.strip()
                    break
        
        return sections
    
    def _extract_complete_control_metadata(self, control_id: str, content: str, sections: Dict, page_number: int) -> Dict:
        """Extract comprehensive metadata for complete control."""
        
        # Base metadata
        metadata = {
            'control_id': control_id,
            'page_number': page_number,
            'control_family': control_id.split('.')[0],
            'control_section': '.'.join(control_id.split('.')[:2]),
            'has_sub_controls': len(control_id.split('.')) > 2,
            'extraction_method': 'complete_control_with_pages',
            'enhanced_extraction': self.is_enhanced_extraction_available()
        }
        
        # Section completeness analysis
        found_sections = [name for name, data in sections.items() if data['found']]
        metadata['sections_found'] = found_sections
        metadata['completeness_score'] = len(found_sections) / len(sections)
        
        # Content quality indicators
        metadata['has_complete_requirement'] = 'main_requirement' in found_sections
        metadata['has_testing_procedure'] = 'testing_procedures' in found_sections
        metadata['has_guidance'] = any(section in found_sections for section in ['purpose', 'good_practice', 'examples'])
        
        # Compliance-specific metadata
        metadata.update(self._extract_compliance_metadata(content))
        
        return metadata
    
    def _extract_compliance_metadata(self, content: str) -> Dict:
        """Extract compliance-specific metadata from content."""
        content_lower = content.lower()
        
        metadata = {}
        
        # Risk assessment
        if any(term in content_lower for term in ['unauthorized', 'security', 'protection']):
            metadata['risk_level'] = 'high'
        elif any(term in content_lower for term in ['configuration', 'management', 'control']):
            metadata['risk_level'] = 'medium'
        else:
            metadata['risk_level'] = 'standard'
        
        # Implementation complexity
        if any(term in content_lower for term in ['network', 'system', 'infrastructure']):
            metadata['complexity'] = 'high'
        elif any(term in content_lower for term in ['file', 'document', 'procedure']):
            metadata['complexity'] = 'medium'
        else:
            metadata['complexity'] = 'low'
        
        # Validation methods
        validation_methods = []
        if 'examine' in content_lower:
            validation_methods.append('documentation_review')
        if 'verify' in content_lower:
            validation_methods.append('technical_validation')
        if 'interview' in content_lower:
            validation_methods.append('personnel_interview')
        
        metadata['validation_methods'] = validation_methods
        
        return metadata
    
    def _is_complete_valid_control(self, control_id: str, control_data: Dict) -> bool:
        """Validate that a control is complete and substantial."""
        
        content = control_data['content']
        sections = control_data['sections']
        
        # Must have minimum substantial content (more lenient)
        if len(content.strip()) < 50:
            control_data['metadata']['rejection_reason'] = 'insufficient_content_length'
            return False
        
        # Must mention the control ID (allow partial matches)
        if control_id not in content and not any(part in content for part in control_id.split('.')):
            control_data['metadata']['rejection_reason'] = 'missing_control_id'
            return False
        
        # Content quality check - must have some meaningful words
        meaningful_words = [
            'requirement', 'examine', 'verify', 'implement', 'maintain',
            'document', 'policy', 'procedure', 'system', 'security',
            'configuration', 'access', 'control', 'data', 'network'
        ]
        
        content_lower = content.lower()
        meaningful_count = sum(1 for word in meaningful_words if word in content_lower)
        
        if meaningful_count < 2:
            control_data['metadata']['rejection_reason'] = 'insufficient_meaningful_content'
            return False
        
        # For specific known controls, check for expected content (more lenient)
        if control_id == "1.2.8":
            required_terms = ['configuration', 'files', 'nsc']
            if not any(term in content.lower() for term in required_terms):
                control_data['metadata']['rejection_reason'] = 'missing_control_specific_terms'
                return False
        
        # Length-based quality check
        if len(content.strip()) < 200:
            # For shorter content, require higher quality indicators
            high_quality_terms = ['examine', 'verify', 'interview', 'observe', 'testing', 'procedure']
            if not any(term in content_lower for term in high_quality_terms):
                control_data['metadata']['rejection_reason'] = 'insufficient_quality_for_length'
                return False
        
        return True
    
    def _validate_control_extraction(self, controls: Dict[str, Dict]) -> None:
        """Enhanced validation of control extraction results."""
        
        total_controls = len(controls)
        self.logger.info(f"Enhanced control extraction validation:")
        self.logger.info(f"  Total controls found: {total_controls}")
        
        # Expected ranges for PCI DSS v4.0.1
        expected_min = 200
        expected_max = 250
        
        if total_controls < expected_min:
            self.logger.warning(f"Low control count: {total_controls} < {expected_min}")
        elif total_controls > expected_max:
            self.logger.warning(f"High control count: {total_controls} > {expected_max}")
        else:
            self.logger.info(f"✅ Control count in expected range: {expected_min}-{expected_max}")
        
        # Analyze completeness
        complete_controls = sum(1 for control_data in controls.values() 
                              if control_data['metadata']['completeness_score'] > 0.5)
        
        self.logger.info(f"  Complete controls (>50% sections): {complete_controls}")
        self.logger.info(f"  Completeness rate: {complete_controls/total_controls:.1%}")
        
        # Check for critical controls
        critical_controls = ['1.1.1', '1.2.8', '2.1.1', '3.1.1', '4.1.1']
        missing_critical = [c for c in critical_controls if c not in controls]
        if missing_critical:
            self.logger.warning(f"Missing critical controls: {missing_critical}")
        else:
            self.logger.info("✅ All critical controls found")
        
        # Page distribution analysis
        page_numbers = [control_data['page_number'] for control_data in controls.values()]
        self.logger.info(f"  Page range: {min(page_numbers)}-{max(page_numbers)}")
    
    def _create_enhanced_control_chunks(
        self, 
        controls: Dict[str, Dict], 
        source_document: str, 
        semantic_splitting: bool = False
    ) -> List[Chunk]:
        """Create enhanced chunks with complete metadata."""
        
        chunks = []
        
        for control_id, control_data in controls.items():
            if semantic_splitting:
                control_chunks = self._create_semantic_chunks_with_metadata(control_data, source_document)
            else:
                control_chunks = [self._create_complete_control_chunk(control_data, source_document)]
            
            chunks.extend(control_chunks)
        
        return chunks
    
    def _create_complete_control_chunk(self, control_data: Dict, source_document: str) -> Chunk:
        """Create a complete chunk for entire control with enhanced metadata."""
        
        content = control_data['content']
        control_id = control_data['control_id']
        page_number = control_data['page_number']
        
        # Calculate token count
        token_count = self._count_tokens(content)
        
        # Create enhanced chunk
        return Chunk(
            id=f"{source_document}_{control_id}",
            content=content,
            control_id=control_id,
            source_document=source_document,
            page_number=page_number,
            standard=self.get_standard_name(),
            chunk_index=0,
            token_count=token_count,
            metadata=control_data['metadata'],
            created_at=datetime.now(timezone.utc)
        )
    
    def _create_semantic_chunks_with_metadata(self, control_data: Dict, source_document: str) -> List[Chunk]:
        """Create semantic section chunks with complete metadata."""
        
        chunks = []
        control_id = control_data['control_id']
        sections = control_data['sections']
        page_number = control_data['page_number']
        
        chunk_index = 0
        
        for section_name, section_data in sections.items():
            if section_data['found'] and section_data['content'] and len(section_data['content'].strip()) > 50:
                
                token_count = self._count_tokens(section_data['content'])
                
                # Create section-specific metadata
                section_metadata = control_data['metadata'].copy()
                section_metadata.update({
                    'section_type': section_name,
                    'is_semantic_split': True,
                    'section_completeness': 1.0 if section_data['found'] else 0.0
                })
                
                chunk = Chunk(
                    id=f"{source_document}_{control_id}_{section_name}_{chunk_index}",
                    content=section_data['content'],
                    control_id=control_id,
                    source_document=source_document,
                    page_number=page_number,
                    standard=self.get_standard_name(),
                    chunk_index=chunk_index,
                    token_count=token_count,
                    metadata=section_metadata,
                    created_at=datetime.now(timezone.utc)
                )
                
                chunks.append(chunk)
                chunk_index += 1
        
        # If no semantic sections, create single chunk
        if not chunks:
            chunks = [self._create_complete_control_chunk(control_data, source_document)]
        
        return chunks
    
    def split_pdf_document(
        self, 
        pdf_path: Path, 
        preserve_structure: bool = True,
        semantic_splitting: bool = False,
        **kwargs
    ) -> List[Chunk]:
        """
        Enhanced PDF splitting with improved header/footer handling.
        
        Args:
            pdf_path: Path to PDF file
            preserve_structure: Whether to preserve control hierarchy
            semantic_splitting: Whether to split controls into semantic sections
            
        Returns:
            List of Chunk objects with complete controls and page metadata
        """
        self.logger.info(f"Processing PDF with enhanced approach: {pdf_path}")
        
        # Extract content using enhanced processor
        if self.is_enhanced_extraction_available():
            content = self._extract_with_enhanced_processor(pdf_path)
        else:
            # Fallback to basic extraction
            self.logger.warning("Enhanced extraction not available, using basic extraction")
            try:
                import fitz
                doc = fitz.open(pdf_path)
                content = ""
                for page_num, page in enumerate(doc, 1):
                    page_text = page.get_text()
                    content += f"[PAGE {page_num}]\n{page_text}\n\n"
                doc.close()
            except Exception as e:
                self.logger.error(f"Failed to extract PDF content: {e}")
                raise
        
        # Process using enhanced document splitting
        return self.split_document(
            content=content,
            source_document=pdf_path.name,
            preserve_structure=preserve_structure,
            pdf_path=pdf_path,
            semantic_splitting=semantic_splitting,
            **kwargs
        )
    
    def _extract_with_enhanced_processor(self, pdf_path: Path) -> str:
        """Extract content using the enhanced PDF processor."""
        try:
            content = self.enhanced_processor.extract_content(pdf_path, self._extraction_strategy)
            self.logger.info(f"Enhanced PDF extraction completed: {len(content)} characters")
            return content
        except Exception as e:
            self.logger.error(f"Enhanced PDF extraction failed: {e}")
            raise
    
    def is_enhanced_extraction_available(self) -> bool:
        """Check if enhanced extraction is available and enabled."""
        return self.use_enhanced_extraction and self.enhanced_processor is not None
    
    def get_extraction_info(self) -> Dict[str, Any]:
        """Get information about the extraction capabilities."""
        return {
            'enhanced_extraction_available': ENHANCED_EXTRACTION_AVAILABLE,
            'enhanced_extraction_enabled': self.use_enhanced_extraction,
            'enhanced_processor_ready': self.enhanced_processor is not None,
            'supports_pdf_direct': self.is_enhanced_extraction_available(),
            'extraction_strategies': ['basic', 'pdfplumber', 'tabula', 'camelot', 'hybrid'] if self.is_enhanced_extraction_available() else ['basic']
        }
    
    def set_extraction_strategy(self, strategy: str = 'hybrid') -> bool:
        """Set the extraction strategy for enhanced processing."""
        if not self.is_enhanced_extraction_available():
            self.logger.warning("Enhanced extraction not available")
            return False
        
        try:
            # Validate strategy
            if hasattr(ExtractionStrategy, strategy.upper()):
                self._extraction_strategy = getattr(ExtractionStrategy, strategy.upper())
                self.logger.info(f"Extraction strategy set to: {strategy}")
                return True
            else:
                self.logger.warning(f"Invalid extraction strategy: {strategy}")
                return False
        except Exception as e:
            self.logger.error(f"Failed to set extraction strategy: {e}")
            return False