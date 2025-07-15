"""
Core PCI DSS Control Extractor

This is the main extractor class that orchestrates the extraction process.
It has been refactored from the original 853-line monolithic file into
a focused orchestration class that delegates to specialized modules.

Responsibilities:
- Load and parse markdown files
- Extract tables and detect control structure
- Orchestrate content building and metadata generation
- Save outputs in multiple formats
"""

from pathlib import Path
from typing import Dict, List, Tuple, Optional
import json
import sys

from ....text_processors.compliance_standards.pci_dss.text_processor import TextProcessor, ControlIDDetector, SectionExtractor
from .content_builder import ControlContentBuilder, MarkdownFormatter

# Import from new metadata generators location
from ....metadata_generators.compliance_standards.pci_dss.metadata_generator import (
    ValidationMetadataGenerator, 
    ProductionMetadataGenerator, 
    MetadataFileManager
)


class ControlExtractor:
    """Main control extractor class - orchestrates the extraction process."""
    
    def __init__(self, markdown_path: str):
        self.markdown_path = Path(markdown_path)
        self.content = ""
        self.lines = []
        self.controls = {}
        
        # Initialize components
        self.text_processor = TextProcessor()
        self.control_id_detector = ControlIDDetector()
        self.section_extractor = SectionExtractor()
        self.content_builder = ControlContentBuilder()
        self.markdown_formatter = MarkdownFormatter()
        
    def load_markdown(self):
        """Load the markdown content."""
        if not self.markdown_path.exists():
            raise FileNotFoundError(f"Markdown file not found: {self.markdown_path}")
        
        with open(self.markdown_path, 'r', encoding='utf-8') as f:
            self.content = f.read()
        
        self.lines = self.content.split('\n')
        print(f"📄 Loaded {len(self.lines):,} lines from {self.markdown_path}")
    
    def extract_tables(self) -> List[Dict]:
        """Extract all tables from the markdown."""
        tables = []
        current_table = None
        
        for i, line in enumerate(self.lines):
            # Skip header/footer lines
            if self.text_processor.is_header_footer(line):
                continue
            
            # Start of a new table
            if self.text_processor.is_table_header(line):
                if current_table:
                    tables.append(current_table)
                
                current_table = {
                    'start_line': i,
                    'header': line,
                    'rows': []
                }
            
            # Table separator (skip)
            elif self.text_processor.is_table_separator(line):
                continue
            
            # Table row
            elif self.text_processor.is_table_row(line) and current_table:
                col1, col2, col3 = self.text_processor.parse_table_row(line)
                current_table['rows'].append({
                    'line_num': i,
                    'raw': line,
                    'col1': col1,
                    'col2': col2,
                    'col3': col3
                })
            
            # End of table (empty line or non-table content)
            elif current_table and line.strip() == "":
                current_table['end_line'] = i
                tables.append(current_table)
                current_table = None
        
        # Add the last table if exists
        if current_table:
            current_table['end_line'] = len(self.lines) - 1
            tables.append(current_table)
        
        return tables
    
    def extract_controls_from_tables(self, tables: List[Dict]) -> Dict[str, Dict]:
        """Extract controls from parsed tables using the complex continuation logic."""
        controls = {}
        last_control_with_continuation = None
        
        for table_idx, table in enumerate(tables):
            current_control = None
            control_rows = []
            pending_context_rows = []  # Store rows before control ID
            table_has_continuation_content = False
            
            for i, row in enumerate(table['rows']):
                # Check for control ID in any column, but only in valid control context
                control_id = None
                continuation_id = None
                
                # First check if this row is in a valid control context
                is_valid_context = self.control_id_detector.is_control_context_row(row)
                
                if is_valid_context:
                    # Check all columns for control IDs
                    for col in [row['col1'], row['col2'], row['col3']]:
                        if not control_id:
                            control_id = self.control_id_detector.extract_control_id(col)
                        if not continuation_id:
                            continuation_id = self.control_id_detector.is_control_continuation(col)
                
                # Check if any column contains "continued on next page"
                has_continuation_marker = any("continued on next page" in col.lower() 
                                            for col in [row['col1'], row['col2'], row['col3']])
                
                # Stop any previous continuation when we find a new control ID
                if control_id and last_control_with_continuation and last_control_with_continuation != control_id:
                    last_control_with_continuation = None
                
                # Handle explicit continuation
                if continuation_id:
                    if continuation_id in controls:
                        controls[continuation_id]['rows'].append(row)
                        if table not in controls[continuation_id]['tables']:
                            controls[continuation_id]['tables'].append(table)
                        current_control = continuation_id
                        control_rows = []
                        pending_context_rows = []
                    continue
                
                # New control found
                if control_id:
                    # Save previous control if exists
                    if current_control and control_rows:
                        if current_control not in controls:
                            controls[current_control] = {
                                'control_id': current_control,
                                'rows': control_rows.copy(),
                                'tables': [table]
                            }
                        else:
                            controls[current_control]['rows'].extend(control_rows)
                            if table not in controls[current_control]['tables']:
                                controls[current_control]['tables'].append(table)
                    
                    # Start new control - include pending context rows
                    current_control = control_id
                    control_rows = pending_context_rows.copy() + [row]
                    pending_context_rows = []
                    
                    # Check if this control has a continuation marker
                    if has_continuation_marker:
                        last_control_with_continuation = control_id
                
                # Add row to current control or handle as potential continuation
                elif current_control:
                    control_rows.append(row)
                    if has_continuation_marker:
                        last_control_with_continuation = current_control
                else:
                    # Handle potential continuation content
                    self._handle_potential_continuation(
                        row, last_control_with_continuation, controls, table, table_has_continuation_content
                    )
                    
                    # Check for context rows
                    has_context = any(marker in f"{row['col1']} {row['col2']} {row['col3']}".lower() 
                                    for marker in ['purpose', 'examples', 'good practice', 'defined approach'])
                    
                    if has_context:
                        pending_context_rows.append(row)
                    else:
                        pending_context_rows = []
            
            # Handle table-level continuation logic
            self._handle_table_continuation(
                table, table_idx, tables, last_control_with_continuation, 
                controls, current_control, table_has_continuation_content
            )
            
            # Save final control in this table
            if current_control and control_rows and not table_has_continuation_content:
                if current_control not in controls:
                    controls[current_control] = {
                        'control_id': current_control,
                        'rows': control_rows.copy(),
                        'tables': [table]
                    }
                else:
                    controls[current_control]['rows'].extend(control_rows)
                    if table not in controls[current_control]['tables']:
                        controls[current_control]['tables'].append(table)
            
            # Set continuation for the current control
            if current_control:
                last_control_with_continuation = current_control
        
        return controls
    
    def _handle_potential_continuation(self, row: Dict, last_control_with_continuation: Optional[str], 
                                     controls: Dict, table: Dict, table_has_continuation_content: bool):
        """Handle rows that might be continuation content."""
        row_text = f"{row['col1']} {row['col2']} {row['col3']}".lower()
        
        continuation_sections = ['customized approach objective', 'applicability notes', 'definitions', 'further information']
        guidance_sections = ['purpose', 'good practice', 'examples']
        
        found_continuation = [s for s in continuation_sections if s in row_text]
        found_guidance = [s for s in guidance_sections if s in row_text]
        
        # Treat as continuation if has continuation sections and limited guidance
        total_sections = len(found_continuation) + len(found_guidance)
        has_continuation_sections = bool(found_continuation) and (not found_guidance or total_sections <= 2)
        
        if has_continuation_sections and last_control_with_continuation:
            if last_control_with_continuation in controls:
                controls[last_control_with_continuation]['rows'].append(row)
                if table not in controls[last_control_with_continuation]['tables']:
                    controls[last_control_with_continuation]['tables'].append(table)
                table_has_continuation_content = True
    
    def _handle_table_continuation(self, table: Dict, table_idx: int, tables: List[Dict], 
                                 last_control_with_continuation: Optional[str], controls: Dict,
                                 current_control: Optional[str], table_has_continuation_content: bool):
        """Handle table-level continuation logic."""
        if (not current_control and not table_has_continuation_content and 
            last_control_with_continuation and table_idx > 0):
            
            # Check if this table contains continuation sections
            table_text = ""
            for row in table['rows']:
                table_text += f" {row['col1']} {row['col2']} {row['col3']}"
            
            has_continuation_sections = any(section in table_text.lower() 
                                          for section in ['customized approach objective', 'applicability notes', 
                                                        'definitions', 'further information'])
            
            has_new_control = any(self.control_id_detector.extract_control_id(f"{row['col1']} {row['col2']} {row['col3']}") 
                                for row in table['rows'])
            
            has_new_section = 'defined approach requirements' in table_text.lower()
            
            if has_continuation_sections and not has_new_control and not has_new_section:
                if last_control_with_continuation in controls:
                    for row in table['rows']:
                        controls[last_control_with_continuation]['rows'].append(row)
                    if table not in controls[last_control_with_continuation]['tables']:
                        controls[last_control_with_continuation]['tables'].append(table)
                    table_has_continuation_content = True
                last_control_with_continuation = None
            elif has_new_control or has_new_section:
                last_control_with_continuation = None
    
    def extract_all_controls(self) -> Dict[str, Dict]:
        """Extract all controls from the markdown."""
        print("🔍 Extracting tables from markdown...")
        tables = self.extract_tables()
        print(f"📊 Found {len(tables)} tables")
        
        print("🎯 Extracting controls from tables...")
        self.controls = self.extract_controls_from_tables(tables)
        print(f"📋 Found {len(self.controls)} controls")
        
        # Analyze and build content for each control
        for control_id, control_data in self.controls.items():
            sections = self.section_extractor.analyze_control_sections(control_data)
            control_data['sections'] = sections
            control_data['content'], control_data['requirement'] = self.content_builder.build_control_content(control_data)
        
        return self.controls
    
    def save_controls(self, output_dir: str = "extracted_controls"):
        """Save individual control files with both validation and production metadata."""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        print(f"💾 Saving controls to {output_path}/")
        
        validation_generator = ValidationMetadataGenerator()
        production_generator = ProductionMetadataGenerator()
        file_manager = MetadataFileManager()
        
        for control_id, control_data in self.controls.items():
            content = control_data['content']
            
            # Save markdown file
            md_file = output_path / f"control_{control_id}.md"
            with open(md_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # Generate and save validation metadata
            validation_metadata = validation_generator.generate_validation_metadata(
                control_id, control_data, content
            )
            
            # Add quality analysis
            quality_analysis = validation_generator.analyze_extraction_quality(validation_metadata)
            validation_metadata['quality_analysis'] = quality_analysis
            
            file_manager.save_validation_metadata(control_id, validation_metadata, output_path)
            
            # Generate and save production metadata
            requirement = control_data.get('requirement', '')
            production_metadata = production_generator.generate_production_metadata(control_id, content, requirement)
            file_manager.save_production_metadata(control_id, production_metadata, output_path)
        
        print(f"✅ Saved {len(self.controls)} controls with validation and production metadata")
    
    def print_summary(self):
        """Print a summary of extracted controls."""
        print("\n📊 CONTROL EXTRACTION SUMMARY")
        print("=" * 60)
        
        # Group by major requirement
        by_major = {}
        for control_id in self.controls:
            major = control_id.split('.')[0]
            if major not in by_major:
                by_major[major] = []
            by_major[major].append(control_id)
        
        # Custom sorting for both numeric and appendix requirements
        def sort_major(major):
            if major.startswith('A'):
                appendix_num = int(major[1:])
                return (100, appendix_num)
            else:
                return (int(major), 0)
        
        def sort_control_id(control_id):
            parts = control_id.split('.')
            if control_id.startswith('A'):
                return [int(parts[0][1:])] + [int(p) for p in parts[1:]]
            else:
                return [int(p) for p in parts]
        
        for major in sorted(by_major.keys(), key=sort_major):
            controls = sorted(by_major[major], key=sort_control_id)
            print(f"Requirement {major}: {len(controls)} controls")
            
            # Show details for first few and multi-table controls
            for i, control_id in enumerate(controls):
                control_data = self.controls[control_id]
                sections = control_data['sections']
                section_count = sum(sections.values())
                
                multi_table = len(control_data['tables']) > 1
                marker = " [MULTI-TABLE]" if multi_table else ""
                
                if i < 3 or multi_table:
                    print(f"  {control_id}: {len(control_data['rows'])} rows, {section_count} sections{marker}")
                elif i == 3:
                    print(f"  ... and {len(controls) - 3} more")
                    break
        
        # Show multi-table controls
        multi_table_controls = [
            control_id for control_id, data in self.controls.items() 
            if len(data['tables']) > 1
        ]
        
        if multi_table_controls:
            print(f"\n🔗 MULTI-TABLE CONTROLS ({len(multi_table_controls)}):")
            for control_id in sorted(multi_table_controls, key=sort_control_id):
                control_data = self.controls[control_id]
                print(f"  {control_id}: {len(control_data['tables'])} tables, {len(control_data['rows'])} rows")


def main():
    """Main extraction function."""
    print("🚀 PCI DSS CONTROL EXTRACTOR (Modular)")
    print("=" * 60)
    
    # Initialize extractor
    extractor = ControlExtractor("PCI-DSS-v4_0_1-FULL.md")
    
    # Load and extract
    extractor.load_markdown()
    extractor.extract_all_controls()
    
    # Print summary
    extractor.print_summary()
    
    # Save controls
    extractor.save_controls()
    
    print(f"\n✅ EXTRACTION COMPLETE!")
    print(f"📁 Check the 'extracted_controls' directory for individual control files.")

if __name__ == "__main__":
    main()