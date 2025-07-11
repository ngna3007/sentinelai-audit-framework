#!/usr/bin/env python3
"""
Simple raw PDF content viewer using PyMuPDF (fitz).
This script extracts and displays the raw content so we can examine what we're working with.
"""

import fitz
from pathlib import Path

def show_raw_pdf_content():
    """Extract and display raw PDF content using PyMuPDF."""
    
    print("📄 RAW PDF CONTENT VIEWER")
    print("=" * 80)
    
    # Open the PDF
    pdf_path = Path("ingest/data/PCI-DSS-v4_0_1.pdf")
    print(f"Opening: {pdf_path}")
    
    if not pdf_path.exists():
        print(f"❌ PDF file not found at {pdf_path}")
        return
    
    # Open with PyMuPDF
    doc = fitz.open(pdf_path)
    print(f"📊 Document info:")
    print(f"  Total pages: {len(doc)}")
    print(f"  Title: {doc.metadata.get('title', 'N/A')}")
    print(f"  Author: {doc.metadata.get('author', 'N/A')}")
    
    # Let's look at a few specific pages around Control 1.2.8 (should be around page 54-55)
    pages_to_examine = [53, 54, 55]  # 0-indexed, so this is pages 54-56
    
    for page_num in pages_to_examine:
        if page_num >= len(doc):
            continue
            
        print(f"\n" + "=" * 80)
        print(f"📄 PAGE {page_num + 1} CONTENT")
        print("=" * 80)
        
        page = doc[page_num]
        
        # Basic text extraction
        print(f"\n🔤 BASIC TEXT EXTRACTION:")
        print("-" * 60)
        basic_text = page.get_text()
        print(basic_text[:1500])  # First 1500 characters
        if len(basic_text) > 1500:
            print("\n... (truncated)")
        
        # Dict extraction (structured)
        print(f"\n📋 STRUCTURED EXTRACTION (dict):")
        print("-" * 60)
        try:
            text_dict = page.get_text("dict")
            print(f"Blocks found: {len(text_dict.get('blocks', []))}")
            
            # Show first few blocks
            for i, block in enumerate(text_dict.get('blocks', [])[:3]):
                if 'lines' in block:
                    print(f"\nBlock {i+1}:")
                    block_text = ""
                    for line in block['lines']:
                        for span in line.get('spans', []):
                            block_text += span.get('text', '') + " "
                    print(f"  Text: {block_text[:200]}...")
                    print(f"  BBox: {block.get('bbox')}")
        except Exception as e:
            print(f"Error in structured extraction: {e}")
        
        print(f"\n🔍 LOOKING FOR CONTROL 1.2.8 ON THIS PAGE:")
        print("-" * 60)
        if "1.2.8" in basic_text:
            print("✅ Found '1.2.8' on this page!")
            
            # Find the lines containing 1.2.8
            lines = basic_text.split('\n')
            for i, line in enumerate(lines):
                if "1.2.8" in line:
                    print(f"  Line {i}: {line.strip()}")
        else:
            print("❌ '1.2.8' not found on this page")
        
        # Look for control boundaries
        print(f"\n🔍 CONTROL BOUNDARY DETECTION:")
        print("-" * 60)
        lines = basic_text.split('\n')
        control_lines = []
        for i, line in enumerate(lines):
            line_stripped = line.strip()
            # Look for control patterns
            if any(pattern in line_stripped for pattern in ['1.2.8', '1.3 Network', '1.2.7', '1.2.9']):
                control_lines.append(f"  Line {i}: {line_stripped}")
        
        if control_lines:
            print("Control-related lines found:")
            for cl in control_lines:
                print(cl)
        else:
            print("No obvious control boundaries found")
    
    doc.close()
    print(f"\n" + "=" * 80)
    print("✅ Raw content examination complete!")

if __name__ == "__main__":
    show_raw_pdf_content() 