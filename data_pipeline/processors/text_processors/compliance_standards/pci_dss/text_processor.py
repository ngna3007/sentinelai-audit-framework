"""
Text Processing Utilities for PCI DSS Control Extraction

This module contains utilities for:
- Text cleaning and normalization
- Control ID detection and validation
- Section extraction from markdown content
- Pattern matching for control elements
"""

from typing import Optional, List, Set, Dict
import re


class TextProcessor:
    """Utilities for cleaning and processing text content."""
    
    @staticmethod
    def clean_text(text: str) -> str:
        """Clean text by removing HTML and excessive markup while preserving structure."""
        if not text:
            return ""
        
        # Replace HTML breaks with spaces
        text = text.replace('<br>', ' ').replace('<br/>', ' ')
        
        # Clean up excessive whitespace
        text = ' '.join(text.split())
        
        # Remove bullet point markup but keep the structure
        text = text.replace('• ', '')
        
        return text.strip()
    
    @staticmethod
    def clean_final_text(text: str) -> str:
        """Clean final text for output by removing continuation markers and other artifacts."""
        if not text:
            return ""
        
        # First apply basic cleaning
        text = TextProcessor.clean_text(text)
        
        # Remove continuation markers (only in final output)
        text = text.replace('_(continued)_', '')
        text = text.replace('_(continued on next page)_', '')
        text = text.replace('(continued)_', '')
        # Clean up any resulting double spaces
        text = ' '.join(text.split())
        
        return text.strip()
    
    @staticmethod
    def is_header_footer(line: str) -> bool:
        """Check if a line is a header/footer."""
        return ("_Payment Card Industry Data Security Standard" in line or
                "_©2006 - 2024 PCI Security Standards Council" in line or
                "_Page " in line)
    
    @staticmethod
    def is_table_header(line: str) -> bool:
        """Check if a line is a table header."""
        return (line.startswith("|Requirements and Testing Procedures|") or 
                line.startswith("|Requirements and Testing Procedures Guidance|") or
                line.startswith("|Defined Approach Requirements|"))
    
    @staticmethod
    def is_table_separator(line: str) -> bool:
        """Check if a line is a table separator."""
        return line.startswith("|---")
    
    @staticmethod
    def is_table_row(line: str) -> bool:
        """Check if a line is a table row."""
        return (line.startswith("|") and 
                line.endswith("|") and 
                not TextProcessor.is_table_separator(line) and
                not TextProcessor.is_table_header(line))
    
    @staticmethod
    def parse_table_row(line: str) -> tuple[str, str, str]:
        """Parse a table row into its three columns."""
        # Remove leading/trailing | and split by |
        parts = line.strip('|').split('|')
        
        if len(parts) >= 3:
            col1 = parts[0].strip()
            col2 = parts[1].strip()
            col3 = parts[2].strip()
            return col1, col2, col3
        else:
            return "", "", ""
    
    @staticmethod
    def preprocess_markdown_for_chunking(text: str) -> str:
        """
        Preprocess markdown content before chunking to improve token counting accuracy.
        
        This method:
        - Removes excessive whitespace and newlines
        - Cleans up docling artifacts
        - Normalizes spacing around headers and sections
        - Removes empty lines
        - Preserves document structure for semantic chunking
        
        Args:
            text: Raw markdown content
            
        Returns:
            Cleaned markdown content ready for chunking
        """
        if not text:
            return ""
        
        # Split into lines for processing
        lines = text.split('\n')
        processed_lines = []
        
        for line in lines:
            # Remove leading/trailing whitespace
            line = line.strip()
            
            # Skip empty lines
            if not line:
                continue
                
            # Remove docling artifacts and HTML comments
            if '<!-- image -->' in line:
                continue
            if line.startswith('<!--') and line.endswith('-->'):
                continue
            if line.startswith('<!-- '):
                continue
                
            # Clean up excessive spacing within lines
            line = ' '.join(line.split())
            
            # Normalize markdown headers (ensure single space after #)
            if line.startswith('#'):
                # Count leading hashes
                hash_count = 0
                for char in line:
                    if char == '#':
                        hash_count += 1
                    else:
                        break
                # Rebuild header with proper spacing
                header_text = line[hash_count:].strip()
                if header_text:
                    line = '#' * hash_count + ' ' + header_text
            
            # Add cleaned line
            processed_lines.append(line)
        
        # Join lines with single newlines
        cleaned_text = '\n'.join(processed_lines)
        
        # Final cleanup: remove multiple consecutive newlines
        cleaned_text = re.sub(r'\n{3,}', '\n\n', cleaned_text)
        
        # Remove any remaining excessive whitespace
        cleaned_text = re.sub(r'[ \t]+', ' ', cleaned_text)
        
        return cleaned_text.strip()


class ControlIDDetector:
    """Utilities for detecting and validating control IDs."""
    
    @staticmethod
    def extract_control_id(text: str) -> Optional[str]:
        """Extract control ID from text (e.g., **1.2.8**, **3.3.1.1**, **8.3.10.1**, **A1.1.1**, **A3.2.1**)."""
        # Skip header rows
        if "defined approach requirements" in text.lower():
            return None
            
        # Look for control IDs in bold format - require minimum 3 segments to avoid section headers
        pattern = r'\*\*([A]?\d+\.\d+\.\d+(?:\.\d+)*)\*\*'
        matches = re.findall(pattern, text)
        return matches[0] if matches else None
    
    @staticmethod
    def is_control_continuation(text: str) -> Optional[str]:
        """Check if text contains a control continuation marker."""
        # Look for patterns like **2.2.3**_(continued)_, **9.5.1.2**_(continued)_, or **A1.1.1**_(continued)_
        pattern = r'\*\*([A]?\d+\.\d+\.\d+(?:\.\d+)*)\*\*_\(continued\)_'
        matches = re.findall(pattern, text)
        return matches[0] if matches else None
    
    @staticmethod
    def is_control_context_row(row: Dict) -> bool:
        """Check if a table row is in the right context for containing control IDs."""
        # Combine all columns to check for context indicators
        all_text = f"{row['col1']} {row['col2']} {row['col3']}".lower()
        
        # This should be a content row, not a header row
        if "defined approach requirements" in all_text:
            return False  # This is a header row
        
        # Look for indicators that this row contains actual requirements/procedures
        control_indicators = [
            # Common requirement language
            "shall", "must", "are:", "is:", "includes:", "ensure", "establish", 
            "define", "identify", "configure", "install", "protect", "secure",
            # Testing procedure language  
            "examine", "verify", "inspect", "interview", "observe", "confirm",
            "validate", "test", "check", "review", "assess",
            # Control structure indicators
            "documented", "implemented", "maintained", "reviewed", "updated",
            "assigned", "approved", "authorized", "restricted", "controlled",
            # Bullet points indicating requirements
            "•", "<br>•",
            # Common control patterns
            "requirement", "procedure", "policy", "process", "mechanism",
            "standard", "method", "practice", "approach", "control"
        ]
        
        # Also accept rows that contain control ID patterns even without specific indicators
        # This handles cases where control rows might not have typical language
        has_control_pattern = bool(ControlIDDetector.extract_control_id(all_text))
        
        return any(indicator in all_text for indicator in control_indicators) or has_control_pattern


class SectionExtractor:
    """Utilities for extracting different sections from control content."""
    
    @staticmethod
    def extract_testing_procedures(col1: str, col2: str, control_id: str, procedures: Set[str]):
        """Extract testing procedures from columns."""
        # Look for testing procedures in both col1 and col2
        for col in [col1, col2]:
            if not col:
                continue
                
            # Look for numbered testing procedures (e.g., 1.2.8.a, 1.2.8.b)
            pattern = rf'\*\*{re.escape(control_id)}\.([a-z])\*\*\s*(.*?)(?=\*\*{re.escape(control_id)}\.([a-z])\*\*|\*\*[A-Z]|$)'
            matches = re.findall(pattern, col, re.DOTALL)
            
            for match in matches:
                letter = match[0]
                proc_text = TextProcessor.clean_text(match[1])
                if proc_text and len(proc_text) > 10:
                    procedures.add(f"Testing Procedure {control_id}.{letter}: {proc_text}")
            
            # Also look for simpler patterns without letter designation
            if f"**{control_id}**" in col and any(word in col.lower() for word in ['examine', 'verify', 'inspect', 'interview', 'observe']):
                # Split by ** and look for testing procedure content
                parts = col.split('**')
                for i, part in enumerate(parts):
                    if part.strip() == control_id and i + 1 < len(parts):
                        proc_text = TextProcessor.clean_text(parts[i + 1])
                        if proc_text and len(proc_text) > 10 and any(word in proc_text.lower() for word in ['examine', 'verify', 'inspect', 'interview', 'observe']):
                            procedures.add(f"Testing Procedure {control_id}: {proc_text}")
                            break
    
    @staticmethod
    def extract_guidance_sections(col1: str, col2: str, col3: str, guidance: Dict[str, str]):
        """Extract embedded guidance sections like Purpose, Examples, Good Practice, etc. from the guidance column."""
        # Focus on the guidance column (usually col3) but also check other columns
        all_content = f" {col1} {col2} {col3}"
        
        # Define embedded section markers (sections that appear inline with content)
        embedded_sections = {
            'Purpose': ['**Purpose**', 'Purpose<br>'],
            'Examples': ['**Examples**', 'Examples<br>'],
            'Good Practice': ['**Good Practice**', 'Good Practice<br>'],
            'Definitions': ['**Definitions**', 'Definitions<br>'],
            'Further Information': ['**Further Information**', 'Further Information<br>']
        }
        
        for section_name, markers in embedded_sections.items():
            for marker in markers:
                if marker.lower() in all_content.lower():
                    # Extract content after the marker
                    parts = all_content.lower().split(marker.lower())
                    if len(parts) > 1:
                        # Take content until next section marker or end
                        section_content = parts[1]
                        
                        # Find end of this section (next marker or end)
                        for other_section, other_markers in embedded_sections.items():
                            if other_section != section_name:
                                for other_marker in other_markers:
                                    if other_marker.lower() in section_content:
                                        section_content = section_content.split(other_marker.lower())[0]
                                        break
                        
                        # Clean and store
                        clean_content = TextProcessor.clean_text(section_content)
                        if clean_content and len(clean_content) > 10:  # Avoid tiny fragments
                            guidance[section_name] = clean_content
                            break
    
    @staticmethod
    def extract_defined_approach_requirements(row: Dict, control_id: str) -> List[str]:
        """Extract Defined Approach Requirements content from a table row."""
        requirements = []
        
        if f"**{control_id}**" in row['col1']:
            # Extract the requirement text after the control ID from Col1 (Defined Approach Requirements column)
            req_text = row['col1'].split(f"**{control_id}**", 1)
            if len(req_text) > 1:
                req_clean = TextProcessor.clean_text(req_text[1])
                # Remove any leading markup or formatting and continuation markers
                req_clean = req_clean.lstrip('*_: ').strip()
                # Remove continuation markers
                if "(continued on next page)" in req_clean:
                    req_clean = req_clean.replace("(continued on next page)", "").strip()
                # Clean up embedded markdown
                req_clean = req_clean.replace('**', '')
                if req_clean and not req_clean.startswith('Defined Approach') and len(req_clean) > 10:
                    requirements.append(req_clean)
        
        return requirements
    
    @staticmethod
    def analyze_control_sections(control_data: Dict) -> Dict[str, bool]:
        """Analyze what sections are present in a control."""
        sections = {
            'purpose': False,
            'examples': False, 
            'good_practice': False,
            'requirements': False,
            'testing_procedures': False,
            'customized_approach': False,
            'applicability_notes': False,
            'definitions': False,
            'further_information': False
        }
        
        # Check all content for section markers
        all_text = ""
        for row in control_data['rows']:
            all_text += f" {row['col1']} {row['col2']} {row['col3']}"
        
        all_text = all_text.lower()
        
        # More comprehensive section detection
        if "**purpose**" in all_text or "purpose<br>" in all_text:
            sections['purpose'] = True
        if "**examples**" in all_text or "examples<br>" in all_text:
            sections['examples'] = True
        if "**good practice**" in all_text or "good practice<br>" in all_text:
            sections['good_practice'] = True
        if "defined approach requirements" in all_text or "requirements" in all_text:
            sections['requirements'] = True
        if "testing procedures" in all_text:
            sections['testing_procedures'] = True
        if "customized approach" in all_text:
            sections['customized_approach'] = True
        if "applicability notes" in all_text:
            sections['applicability_notes'] = True
        if "**definitions**" in all_text or "definitions<br>" in all_text:
            sections['definitions'] = True
        if "further information" in all_text:
            sections['further_information'] = True
        
        return sections