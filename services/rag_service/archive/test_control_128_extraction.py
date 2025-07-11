#!/usr/bin/env python3
"""
Test script for Control 1.2.8 PDF extraction validation.

This script tests the enhanced PDF processor against the issues identified 
in the Control 1.2.8 diagnosis, comparing basic vs enhanced extraction.
"""

import sys
import logging
from pathlib import Path
from typing import Dict, Any, List
import re

# Add the ingest module to the path
sys.path.append(str(Path(__file__).parent / "ingest"))

from ingest.processors.enhanced_pdf_processor import EnhancedPDFProcessor, ExtractionStrategy
from ingest.splitter import get_splitter


class Control128Validator:
    """Validator for Control 1.2.8 extraction quality."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.control_pattern = re.compile(r'1\.2\.8')
        
        # Expected sections from diagnosis
        self.expected_sections = {
            'main_requirement': r'1\.2\.8.*Configuration files for NSCs are',
            'testing_procedure': r'1\.2\.8.*Examine configuration files for NSCs',
            'customized_approach': r'NSCs cannot be defined or modified using untrusted',
            'applicability_notes': r'Any file or setting used to configure',
            'purpose': r'prevent.*unauthorized configurations',  # Missing in diagnosis
            'examples': r'secure configuration.*router.*stored'
        }
    
    def analyze_extraction(self, content: str, extraction_method: str) -> Dict[str, Any]:
        """Analyze extraction quality for Control 1.2.8."""
        results = {
            'method': extraction_method,
            'content_length': len(content),
            'control_128_mentions': len(self.control_pattern.findall(content)),
            'sections_found': {},
            'completeness_score': 0,
            'quality_score': 0
        }
        
        # Check for expected sections
        sections_found = 0
        for section, pattern in self.expected_sections.items():
            match = re.search(pattern, content, re.IGNORECASE | re.DOTALL)
            results['sections_found'][section] = bool(match)
            if match:
                sections_found += 1
        
        # Calculate scores
        results['completeness_score'] = sections_found / len(self.expected_sections)
        results['quality_score'] = self._calculate_quality_score(content)
        
        return results
    
    def _calculate_quality_score(self, content: str) -> float:
        """Calculate overall quality score based on content characteristics."""
        score = 0.0
        
        # Check for table structure preservation
        if 'Defined Approach Requirements' in content:
            score += 0.2
        if 'Testing Procedures' in content:
            score += 0.2
        if 'Customized Approach' in content:
            score += 0.2
        
        # Check for control ID associations
        control_matches = len(self.control_pattern.findall(content))
        if control_matches >= 2:  # Should find main requirement + testing procedure
            score += 0.2
        
        # Check for content coherence (not fragmented)
        if 'Configuration files for NSCs are:' in content:
            if 'Secured from unauthorized access' in content:
                score += 0.1
            if 'Kept consistent with active network configurations' in content:
                score += 0.1
        
        return min(score, 1.0)
    
    def extract_control_128_content(self, content: str) -> List[str]:
        """Extract all content related to Control 1.2.8."""
        chunks = []
        
        # Find all lines mentioning 1.2.8
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if self.control_pattern.search(line):
                # Extract context around the match
                start = max(0, i - 5)
                end = min(len(lines), i + 10)
                context = '\n'.join(lines[start:end])
                chunks.append(context)
        
        return chunks
    
    def create_diagnosis_report(self, basic_results: Dict, enhanced_results: Dict) -> str:
        """Create a diagnosis report comparing extraction methods."""
        report = []
        report.append("=" * 80)
        report.append("CONTROL 1.2.8 ENHANCED EXTRACTION VALIDATION REPORT")
        report.append("=" * 80)
        
        # Comparison summary
        report.append("\n📊 EXTRACTION COMPARISON:")
        report.append("-" * 50)
        report.append(f"{'Metric':<30} {'Basic':<15} {'Enhanced':<15} {'Improvement'}")
        report.append("-" * 50)
        
        metrics = [
            ('Content Length', 'content_length', 'characters'),
            ('Control 1.2.8 Mentions', 'control_128_mentions', 'count'),
            ('Completeness Score', 'completeness_score', '%'),
            ('Quality Score', 'quality_score', '%')
        ]
        
        for metric_name, key, unit in metrics:
            basic_val = basic_results[key]
            enhanced_val = enhanced_results[key]
            
            if key in ['completeness_score', 'quality_score']:
                basic_display = f"{basic_val:.1%}"
                enhanced_display = f"{enhanced_val:.1%}"
                improvement = f"{((enhanced_val - basic_val) / basic_val * 100) if basic_val > 0 else 0:+.1f}%"
            else:
                basic_display = str(basic_val)
                enhanced_display = str(enhanced_val)
                improvement = f"{((enhanced_val - basic_val) / basic_val * 100) if basic_val > 0 else 0:+.1f}%"
            
            report.append(f"{metric_name:<30} {basic_display:<15} {enhanced_display:<15} {improvement}")
        
        # Section detection details
        report.append("\n🔍 SECTION DETECTION ANALYSIS:")
        report.append("-" * 50)
        
        for section in self.expected_sections.keys():
            basic_found = "✅" if basic_results['sections_found'][section] else "❌"
            enhanced_found = "✅" if enhanced_results['sections_found'][section] else "❌"
            status = "FIXED" if not basic_results['sections_found'][section] and enhanced_results['sections_found'][section] else "SAME"
            
            report.append(f"{section:<25} {basic_found} → {enhanced_found} ({status})")
        
        # Recommendations
        report.append("\n💡 RECOMMENDATIONS:")
        report.append("-" * 50)
        
        if enhanced_results['completeness_score'] > basic_results['completeness_score']:
            report.append("✅ Enhanced extraction IMPROVED completeness")
        else:
            report.append("⚠️  Enhanced extraction did not improve completeness")
        
        if enhanced_results['quality_score'] > basic_results['quality_score']:
            report.append("✅ Enhanced extraction IMPROVED quality")
        else:
            report.append("⚠️  Enhanced extraction did not improve quality")
        
        if enhanced_results['completeness_score'] < 0.8:
            report.append("🔧 Further PDF processing improvements needed")
        
        report.append("=" * 80)
        
        return '\n'.join(report)


def test_control_128_extraction(pdf_path: Path) -> None:
    """Test Control 1.2.8 extraction with basic vs enhanced methods."""
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    
    if not pdf_path.exists():
        print(f"❌ PDF file not found: {pdf_path}")
        print("Please place a PCI DSS v4.0 PDF in the ingest/data directory")
        return
    
    validator = Control128Validator()
    processor = EnhancedPDFProcessor()
    
    print("🔍 Testing Control 1.2.8 PDF Extraction...")
    print("=" * 60)
    
    # Test basic extraction
    print("\n1️⃣ Testing BASIC extraction...")
    basic_content = processor.extract_content(pdf_path, ExtractionStrategy.BASIC)
    basic_results = validator.analyze_extraction(basic_content, "BASIC")
    
    # Test enhanced extraction
    print("\n2️⃣ Testing ENHANCED extraction...")
    enhanced_content = processor.extract_content(pdf_path, ExtractionStrategy.HYBRID)
    enhanced_results = validator.analyze_extraction(enhanced_content, "ENHANCED")
    
    # Extract specific Control 1.2.8 content for detailed analysis
    print("\n3️⃣ Extracting Control 1.2.8 specific content...")
    basic_128_chunks = validator.extract_control_128_content(basic_content)
    enhanced_128_chunks = validator.extract_control_128_content(enhanced_content)
    
    print(f"Basic extraction found {len(basic_128_chunks)} chunks with 1.2.8")
    print(f"Enhanced extraction found {len(enhanced_128_chunks)} chunks with 1.2.8")
    
    # Generate diagnosis report
    report = validator.create_diagnosis_report(basic_results, enhanced_results)
    print("\n" + report)
    
    # Show specific Control 1.2.8 content
    print("\n📄 CONTROL 1.2.8 EXTRACTED CONTENT:")
    print("=" * 60)
    
    print("\n🔹 BASIC EXTRACTION:")
    for i, chunk in enumerate(basic_128_chunks[:2]):  # Show first 2 chunks
        print(f"Chunk {i+1}:")
        print("-" * 40)
        print(chunk)
        print()
    
    print("\n🔹 ENHANCED EXTRACTION:")
    for i, chunk in enumerate(enhanced_128_chunks[:2]):  # Show first 2 chunks
        print(f"Chunk {i+1}:")
        print("-" * 40)
        print(chunk)
        print()
    
    # Test with PCI splitter
    print("\n4️⃣ Testing with PCI Splitter...")
    try:
        splitter = get_splitter("pci-dss", max_tokens=350, overlap_tokens=50)
        
        basic_chunks = splitter.split_document(
            content=basic_content,
            source_document=pdf_path.name,
            preserve_structure=True
        )
        
        enhanced_chunks = splitter.split_document(
            content=enhanced_content,
            source_document=pdf_path.name,
            preserve_structure=True
        )
        
        # Find Control 1.2.8 chunks
        basic_128_chunks = [c for c in basic_chunks if c.control_id == "1.2.8"]
        enhanced_128_chunks = [c for c in enhanced_chunks if c.control_id == "1.2.8"]
        
        print(f"PCI Splitter - Basic: {len(basic_128_chunks)} chunks for Control 1.2.8")
        print(f"PCI Splitter - Enhanced: {len(enhanced_128_chunks)} chunks for Control 1.2.8")
        
        if enhanced_128_chunks:
            print("\n📋 Enhanced PCI Splitter Control 1.2.8 Content:")
            for chunk in enhanced_128_chunks:
                print(f"Chunk ID: {chunk.id}")
                print(f"Tokens: {chunk.token_count}")
                print(f"Content: {chunk.content[:200]}...")
                print("-" * 40)
        
    except Exception as e:
        print(f"❌ PCI Splitter test failed: {e}")


if __name__ == "__main__":
    # Look for PCI DSS PDF in data directory
    data_dir = Path(__file__).parent / "ingest" / "data"
    pdf_files = list(data_dir.glob("*.pdf"))
    
    if not pdf_files:
        print("❌ No PDF files found in ingest/data directory")
        print("Please place a PCI DSS v4.0 PDF file in services/rag_service/ingest/data/")
        sys.exit(1)
    
    # Use the first PDF file found
    pdf_path = pdf_files[0]
    print(f"📖 Using PDF: {pdf_path}")
    
    test_control_128_extraction(pdf_path) 