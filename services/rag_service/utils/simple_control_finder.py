#!/usr/bin/env python3
"""
Simple control boundary finder using backwards scanning.
Finds control IDs and works backwards to find true control start points.
"""

import fitz
import re
from pathlib import Path

def find_control_boundaries():
    """Find true control boundaries by working backwards from control IDs."""
    
    print("🔍 SIMPLE CONTROL BOUNDARY FINDER")
    print("=" * 80)
    
    # Open PDF
    pdf_path = Path("ingest/data/PCI-DSS-v4_0_1.pdf")
    doc = fitz.open(pdf_path)
    
    # Extract all content first
    all_lines = []
    page_markers = {}  # Track which page each line comes from
    
    print("📄 Extracting all content...")
    for page_num in range(len(doc)):
        page = doc[page_num]
        page_text = page.get_text()
        lines = page_text.split('\n')
        
        for line in lines:
            line_stripped = line.strip()
            if line_stripped:  # Only keep non-empty lines
                all_lines.append(line_stripped)
                page_markers[len(all_lines) - 1] = page_num + 1  # 1-indexed page
    
    doc.close()
    
    print(f"Total non-empty lines: {len(all_lines)}")
    
    # Find all control IDs using regex
    control_pattern = re.compile(r'^\d+\.\d+\.\d+\s+')
    control_positions = []
    
    for i, line in enumerate(all_lines):
        if control_pattern.match(line):
            # Extract control ID
            match = control_pattern.match(line)
            control_id = match.group().strip()
            control_positions.append({
                'control_id': control_id,
                'line_index': i,
                'line_content': line,
                'page': page_markers.get(i, '?')
            })
    
    print(f"Found {len(control_positions)} potential controls")
    
    # Focus on controls around 1.2.8 for testing
    target_controls = []
    for pos in control_positions:
        control_id = pos['control_id']
        if control_id in ['1.2.7', '1.2.8', '1.3']:
            target_controls.append(pos)
    
    print(f"\n🎯 FOCUSING ON TARGET CONTROLS:")
    for ctrl in target_controls:
        print(f"  {ctrl['control_id']} at line {ctrl['line_index']} (page {ctrl['page']})")
    
    # For each target control, find the true start by working backwards
    for i, control in enumerate(target_controls):
        print(f"\n" + "=" * 80)
        print(f"🔍 ANALYZING CONTROL {control['control_id']}")
        print("=" * 80)
        
        control_line = control['line_index']
        
        # Work backwards to find true start
        true_start = find_control_start_backwards(all_lines, control_line, control['control_id'])
        
        # Work forwards to find end (using next control or reasonable limit)
        if i + 1 < len(target_controls):
            next_control_line = target_controls[i + 1]['line_index']
            # Find backwards start of next control too
            next_true_start = find_control_start_backwards(all_lines, next_control_line, target_controls[i + 1]['control_id'])
            true_end = next_true_start
        else:
            true_end = min(control_line + 30, len(all_lines))  # Reasonable limit
        
        print(f"📍 Control {control['control_id']} boundaries:")
        print(f"   Control ID line: {control_line}")
        print(f"   True start: {true_start}")
        print(f"   True end: {true_end}")
        print(f"   Total lines: {true_end - true_start}")
        
        # Show the complete content
        print(f"\n📄 COMPLETE CONTROL CONTENT:")
        print("-" * 60)
        for line_idx in range(true_start, true_end):
            if line_idx < len(all_lines):
                line = all_lines[line_idx]
                marker = " <<<< CONTROL ID" if line_idx == control_line else ""
                print(f"{line_idx:3d}: {line}{marker}")
        
        print("-" * 60)
        
        # Analyze sections found
        content_lines = all_lines[true_start:true_end]
        sections_found = analyze_sections(content_lines)
        print(f"\n📋 SECTIONS FOUND: {sections_found}")

def find_control_start_backwards(all_lines, control_line_index, control_id):
    """Work backwards from control ID to find true start of control content."""
    
    # Section markers that indicate control content
    section_markers = [
        'purpose', 'examples', 'good practice', 'guidance',
        'defined approach requirements', 'defined approach testing procedures'
    ]
    
    # Look backwards for content boundaries
    start_line = control_line_index
    
    # Go backwards line by line
    for i in range(control_line_index - 1, max(0, control_line_index - 50), -1):
        line = all_lines[i].lower().strip()
        
        # Stop if we hit another control ID
        if re.match(r'^\d+\.\d+\.\d+\s+', all_lines[i]):
            start_line = i + 1
            break
        
        # Stop if we hit headers/footers
        if any(header in line for header in [
            'payment card industry', 'page ', '©2006', 'june 2024',
            'requirements and testing procedures', 'guidance'
        ]):
            if 'purpose' not in line and 'examples' not in line:  # These are section headers, not page headers
                start_line = i + 1
                break
        
        # Look for section content that belongs to this control
        if any(marker in line for marker in section_markers):
            start_line = i  # Include this line
            continue
        
        # If we find substantial content, include it
        if len(line) > 20 and not line.startswith('•'):
            start_line = i  # Include this line
            continue
        
        # If we hit empty areas or bullets without context, this might be our boundary
        if not line or (line.startswith('•') and len(line) < 50):
            # Check if next few lines are also empty/bullets
            empty_count = 0
            for j in range(i, max(0, i - 5), -1):
                if not all_lines[j].strip() or all_lines[j].strip().startswith('•'):
                    empty_count += 1
            
            if empty_count >= 2:  # Found a boundary
                start_line = i + 1
                break
    
    return max(0, start_line)

def analyze_sections(content_lines):
    """Analyze what sections are present in the content."""
    content_text = ' '.join(content_lines).lower()
    
    sections = []
    if 'purpose' in content_text:
        sections.append('Purpose')
    if 'examples' in content_text or 'example' in content_text:
        sections.append('Examples')
    if 'good practice' in content_text:
        sections.append('Good Practice')
    if 'customized approach' in content_text:
        sections.append('Customized Approach')
    if 'applicability notes' in content_text:
        sections.append('Applicability Notes')
    if 'examine' in content_text:
        sections.append('Testing Procedures')
    
    return sections

if __name__ == "__main__":
    find_control_boundaries() 