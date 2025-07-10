"""
Content Builders for PCI DSS Control Extraction

This module handles:
- Assembling complete control content from extracted data
- Formatting content for different output types (markdown, JSON, CSV)
- Building structured content optimized for vector embeddings
- Handling guidance sections and testing procedures
"""

from typing import Dict, List, Set
from .text_processors import TextProcessor, SectionExtractor


class ControlContentBuilder:
    """Builds complete control content from extracted table data."""
    
    def __init__(self):
        self.text_processor = TextProcessor()
        self.section_extractor = SectionExtractor()
    
    def build_control_content(self, control_data: Dict) -> str:
        """Build the complete content for a control in paragraph format optimized for vector embeddings."""
        control_id = control_data['control_id']
        rows = control_data['rows']
        
        # Extract and organize content by type
        testing_procedures = set()  # Use set to avoid duplicates
        guidance_sections = {}
        defined_approach_requirements = []  # Main requirement text under "Defined Approach Requirements"
        
        # Process rows and handle separate header/content rows for guidance sections
        guidance_headers = {}  # Track section headers
        
        for i, row in enumerate(rows):
            # Clean up the content - remove HTML breaks and excessive markup
            col1 = self.text_processor.clean_text(row['col1'])
            col2 = self.text_processor.clean_text(row['col2'])
            col3 = self.text_processor.clean_text(row['col3'])
            
            # Extract Defined Approach Requirements content
            requirements = self.section_extractor.extract_defined_approach_requirements(row, control_id)
            defined_approach_requirements.extend(requirements)
            
            # Extract testing procedures
            self.section_extractor.extract_testing_procedures(col1, col2, control_id, testing_procedures)
            
            # Check if this row is a standalone section header
            self._extract_standalone_headers(col1, col2, col3, guidance_headers, i)
            
            # Extract embedded guidance sections from Guidance column
            self.section_extractor.extract_guidance_sections(col1, col2, col3, guidance_sections)
        
        # Handle standalone section headers with content in the next row
        self._process_standalone_sections(rows, guidance_headers, guidance_sections)
        
        # Build the structured content
        return self._assemble_final_content(
            control_id, 
            defined_approach_requirements, 
            guidance_sections, 
            testing_procedures
        )
    
    def _extract_standalone_headers(self, col1: str, col2: str, col3: str, guidance_headers: Dict, row_index: int):
        """Extract standalone section headers that span all columns."""
        row_text_lower = f"{col1} {col2} {col3}".lower()
        
        standalone_headers = {
            'Customized Approach Objective': 'customized approach objective',
            'Applicability Notes': 'applicability notes'
        }
        
        for section_name, marker in standalone_headers.items():
            # Check if this marker appears in all three columns (indicating a section header row)
            if (marker in col1.lower() and marker in col2.lower() and marker in col3.lower()):
                guidance_headers[section_name] = row_index
    
    def _process_standalone_sections(self, rows: List[Dict], guidance_headers: Dict, guidance_sections: Dict):
        """Process standalone section headers and extract their content."""
        for section_name, header_row_idx in guidance_headers.items():
            if header_row_idx + 1 < len(rows):  # Check if there's a next row with content
                next_row = rows[header_row_idx + 1]
                
                # For standalone sections, content is usually the same across all columns
                # Pick the column with the most substantial content
                content_candidates = [
                    self.text_processor.clean_text(next_row['col1']),
                    self.text_processor.clean_text(next_row['col2']), 
                    self.text_processor.clean_text(next_row['col3'])
                ]
                
                # Choose the longest non-empty content
                best_content = max(content_candidates, key=len) if content_candidates else ""
                
                if best_content and len(best_content.split()) > 3:  # Ensure substantial content
                    guidance_sections[section_name] = best_content
    
    def _assemble_final_content(self, control_id: str, defined_approach_requirements: List[str], 
                              guidance_sections: Dict, testing_procedures: Set[str]) -> str:
        """Assemble the final structured content."""
        content_parts = []
        
        # Control ID and basic info
        content_parts.append(f"Control {control_id}")
        content_parts.append("")
        
        # Defined Approach Requirements
        if defined_approach_requirements:
            content_parts.append("Defined Approach Requirements:")
            for req in defined_approach_requirements:
                content_parts.append(req)
            content_parts.append("")
        
        # Customized Approach Objective
        if 'Customized Approach Objective' in guidance_sections:
            content_parts.append("Customized Approach Objective:")
            content_parts.append(guidance_sections['Customized Approach Objective'])
            content_parts.append("")
        
        # Applicability Notes
        if 'Applicability Notes' in guidance_sections:
            content_parts.append("Applicability Notes:")
            content_parts.append(guidance_sections['Applicability Notes'])
            content_parts.append("")
        
        # Testing Procedures
        if testing_procedures:
            content_parts.append("Testing Procedures:")
            sorted_procedures = sorted(list(testing_procedures))
            for proc in sorted_procedures:
                content_parts.append(proc)
            content_parts.append("")
        
        # Guidance (embedded sections)
        embedded_guidance = {k: v for k, v in guidance_sections.items() 
                           if k not in ['Customized Approach Objective', 'Applicability Notes']}
        if embedded_guidance:
            content_parts.append("Guidance:")
            guidance_text = self._format_guidance_sections(embedded_guidance)
            content_parts.append(guidance_text)
        
        return "\n".join(content_parts).strip()
    
    def _format_guidance_sections(self, guidance: Dict[str, str]) -> str:
        """Format guidance sections into readable text."""
        formatted_parts = []
        
        # Order sections logically
        section_order = ['Purpose', 'Examples', 'Good Practice', 'Customized Approach Objective', 
                        'Definitions', 'Further Information', 'Applicability Notes']
        
        for section in section_order:
            if section in guidance and guidance[section]:
                content = guidance[section].strip()
                
                # Capitalize first letter and ensure proper sentence ending
                if content:
                    content = content[0].upper() + content[1:] if len(content) > 1 else content.upper()
                    if not content.endswith('.'):
                        content += '.'
                    
                    formatted_parts.append(f"{section}: {content}")
        
        return " ".join(formatted_parts)


class MarkdownFormatter:
    """Formats control content specifically for markdown output."""
    
    @staticmethod
    def format_for_markdown(content: str, control_id: str) -> str:
        """Format content specifically for markdown files."""
        lines = content.split('\n')
        formatted_lines = []
        
        for line in lines:
            line = line.strip()
            if not line:
                formatted_lines.append("")
                continue
            
            # Format section headers
            if line.endswith(':') and line in ['Defined Approach Requirements:', 'Testing Procedures:', 
                                             'Guidance:', 'Customized Approach Objective:', 'Applicability Notes:']:
                formatted_lines.append(f"## {line}")
            # Format testing procedures with bullet points
            elif line.startswith('Testing Procedure'):
                formatted_lines.append(f"- {line}")
            else:
                formatted_lines.append(line)
        
        return "\n".join(formatted_lines)
    
    @staticmethod
    def create_control_summary(control_data: Dict) -> str:
        """Create a summary of the control for overview purposes."""
        control_id = control_data['control_id']
        sections = control_data.get('sections', {})
        
        summary_parts = [
            f"# Control {control_id} Summary",
            "",
            f"**Tables:** {len(control_data['tables'])}",
            f"**Rows:** {len(control_data['rows'])}",
            f"**Multi-table:** {'Yes' if len(control_data['tables']) > 1 else 'No'}",
            "",
            "**Sections Present:**"
        ]
        
        for section, present in sections.items():
            status = "✅" if present else "❌"
            summary_parts.append(f"- {status} {section.replace('_', ' ').title()}")
        
        return "\n".join(summary_parts)


class ProductionContentFormatter:
    """Formats content for production use (JSON, CSV, database)."""
    
    @staticmethod
    def extract_title_from_requirements(content: str) -> str:
        """Extract title from Defined Approach Requirements section."""
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if 'Defined Approach Requirements:' in line and i + 1 < len(lines):
                title = lines[i + 1].strip()
                # Take first sentence or up to 100 characters for title
                if '. ' in title:
                    title = title.split('. ')[0] + '.'
                elif len(title) > 100:
                    title = title[:97] + '...'
                return title
        return ""
    
    @staticmethod
    def extract_status_from_content(content: str) -> str:
        """Extract implementation status from content."""
        content_lower = content.lower()
        
        # Look for best practice language (handle underscores and formatting)
        if 'best practice until' in content_lower:
            # Extract the date, handling underscores and formatting
            import re
            # Remove underscores and extra spaces for pattern matching
            cleaned_content = re.sub(r'_+', ' ', content_lower)
            cleaned_content = re.sub(r'\s+', ' ', cleaned_content)
            
            date_match = re.search(r'best practice until.*?(\d{1,2}\s+(march|april|may|june|july|august|september|october|november|december)\s+\d{4})', cleaned_content)
            if date_match:
                return f"best_practice_until_{date_match.group(1).replace(' ', '-')}"
        
        # Look for other status indicators
        if 'not applicable' in content_lower:
            return "not_applicable"
        elif 'customized approach' in content_lower and 'not eligible' in content_lower:
            return "required_defined_approach_only"
        
        # Default to required
        return "required"
    
    @staticmethod
    def extract_testing_procedures_list(content: str) -> List[str]:
        """Extract testing procedures as a list."""
        procedures = []
        lines = content.split('\n')
        in_testing_section = False
        
        for line in lines:
            line = line.strip()
            if 'Testing Procedures:' in line:
                in_testing_section = True
                continue
            elif in_testing_section and line.startswith('Testing Procedure'):
                # Extract the procedure text after the ID
                if ':' in line:
                    proc_text = line.split(':', 1)[1].strip()
                    procedures.append(proc_text)
            elif in_testing_section and line and not line.startswith('Testing Procedure'):
                # We've moved to next section
                break
                
        return procedures
    
    @staticmethod
    def count_tokens(text: str) -> int:
        """Estimate token count for text (rough approximation)."""
        # Simple token estimation: ~4 characters per token for English text
        return len(text) // 4 