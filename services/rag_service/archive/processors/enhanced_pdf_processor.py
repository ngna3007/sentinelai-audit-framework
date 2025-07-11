"""
Enhanced PDF processor for compliance documents with improved header/footer removal.

This module fixes the PDF table extraction limitations by implementing:
1. Page-by-page processing with proper header/footer removal
2. Page number extraction for metadata
3. Complete control boundary detection
"""

import re
import logging
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path
from dataclasses import dataclass
from enum import Enum

# Standard PDF processing
import fitz  # PyMuPDF

# Enhanced table extraction libraries
import pdfplumber
try:
    import tabula
    TABULA_AVAILABLE = True
except ImportError:
    TABULA_AVAILABLE = False
    logging.warning("tabula-py not available. Install with: pip install tabula-py")

try:
    import camelot
    CAMELOT_AVAILABLE = True
except ImportError:
    CAMELOT_AVAILABLE = False
    logging.warning("camelot-py not available. Install with: pip install camelot-py[cv]")


class ExtractionStrategy(Enum):
    """PDF extraction strategies."""
    BASIC = "basic"  # PyMuPDF basic text extraction
    PDFPLUMBER = "pdfplumber"  # pdfplumber table-aware extraction
    TABULA = "tabula"  # tabula-py table extraction
    CAMELOT = "camelot"  # camelot-py advanced table extraction
    HYBRID = "hybrid"  # Combined approach


@dataclass
class PageContent:
    """Represents content from a single page with metadata."""
    content: str
    page_number: int
    has_tables: bool
    control_ids: List[str]
    sections: List[str]


@dataclass
class TableCell:
    """Represents a table cell with position and content."""
    text: str
    bbox: Tuple[float, float, float, float]  # x0, y0, x1, y1
    row: int
    col: int


@dataclass
class ExtractedTable:
    """Represents an extracted table with metadata."""
    cells: List[TableCell]
    bbox: Tuple[float, float, float, float]
    page_number: int
    confidence: float
    extraction_method: str


@dataclass
class PCIControlBlock:
    """Represents a complete PCI control block with all sections."""
    control_id: str
    main_requirement: str
    testing_procedure: str
    customized_approach: str
    applicability_notes: str
    purpose: str
    good_practice: str
    examples: str
    page_number: int
    bbox: Optional[Tuple[float, float, float, float]] = None


class EnhancedPDFProcessor:
    """Enhanced PDF processor with improved header/footer removal and page processing."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # PCI DSS specific patterns
        self.pci_control_pattern = re.compile(r'(?<!v)(\d+\.\d+\.\d+)\s+(?![a-z])', re.MULTILINE)
        self.pci_table_headers = [
            "defined approach requirements",
            "defined approach testing procedures", 
            "customized approach objective",
            "applicability notes",
            "purpose",
            "good practice",
            "examples"
        ]
        
        # Enhanced header/footer patterns
        self.header_patterns = [
            re.compile(r'^Payment Card Industry.*?Standard.*?$', re.IGNORECASE),
            re.compile(r'^Requirements and Testing Procedures.*?$', re.IGNORECASE),
            re.compile(r'^Guidance.*?$', re.IGNORECASE),
        ]
        
        self.footer_patterns = [
            re.compile(r'^.*?Payment Card Industry.*?v\d+\.\d+\.\d+.*?$', re.IGNORECASE),
            re.compile(r'^.*?\w+\s+\d{4}.*?Page\s+(\d+).*?$', re.IGNORECASE),  # Captures page number
            re.compile(r'^.*?Page\s+(\d+).*?$', re.IGNORECASE),  # Simple page number pattern
        ]
        
        # Table detection patterns
        self.table_indicators = [
            r"requirements?\s+and\s+testing\s+procedures?",
            r"defined\s+approach\s+requirements?",
            r"testing\s+procedures?",
            r"customized\s+approach",
            r"applicability\s+notes",
            r"purpose",
            r"good\s+practice",
            r"examples?"
        ]
    
    def extract_content(
        self, 
        pdf_path: Path, 
        strategy: ExtractionStrategy = ExtractionStrategy.HYBRID
    ) -> str:
        """
        Extract content from PDF using specified strategy with improved header/footer removal.
        
        Args:
            pdf_path: Path to PDF file
            strategy: Extraction strategy to use
            
        Returns:
            Extracted text content with preserved table structure and page metadata
        """
        self.logger.info(f"Extracting content from {pdf_path} using {strategy.value} strategy")
        
        if strategy == ExtractionStrategy.BASIC:
            return self._extract_basic_with_cleanup(pdf_path)
        elif strategy == ExtractionStrategy.PDFPLUMBER:
            return self._extract_pdfplumber_with_cleanup(pdf_path)
        elif strategy == ExtractionStrategy.TABULA and TABULA_AVAILABLE:
            return self._extract_tabula(pdf_path)
        elif strategy == ExtractionStrategy.CAMELOT and CAMELOT_AVAILABLE:
            return self._extract_camelot(pdf_path)
        elif strategy == ExtractionStrategy.HYBRID:
            return self._extract_hybrid_with_cleanup(pdf_path)
        else:
            self.logger.warning(f"Strategy {strategy.value} not available, falling back to basic")
            return self._extract_basic_with_cleanup(pdf_path)
    
    def _extract_basic_with_cleanup(self, pdf_path: Path) -> str:
        """Enhanced PyMuPDF extraction with layout preservation."""
        doc = fitz.open(pdf_path)
        pages_content = []
        
        for page_num, page in enumerate(doc, 1):
            # Use layout-preserving extraction
            page_content = self._extract_page_with_layout_preservation(page, page_num)
            cleaned_content = self._clean_page_content(page_content, page_num)
            if cleaned_content.strip():  # Only add non-empty pages
                pages_content.append(f"[PAGE {page_num}]\n{cleaned_content}")
        
        doc.close()
        return "\n\n".join(pages_content)
    
    def _extract_page_with_layout_preservation(self, page, page_num: int) -> str:
        """Extract page content with better layout preservation using PyMuPDF."""
        
        # Method 1: Try text blocks first (preserves layout better)
        try:
            text_blocks = page.get_text("dict")
            reconstructed_text = self._reconstruct_from_text_blocks(text_blocks, page_num)
            if reconstructed_text.strip():
                return reconstructed_text
        except Exception as e:
            self.logger.debug(f"Text blocks extraction failed for page {page_num}: {e}")
        
        # Method 2: Try text with layout flags
        try:
            layout_text = page.get_text("text", flags=fitz.TEXT_PRESERVE_WHITESPACE | fitz.TEXT_PRESERVE_LIGATURES)
            if layout_text.strip():
                return layout_text
        except Exception as e:
            self.logger.debug(f"Layout text extraction failed for page {page_num}: {e}")
        
        # Method 3: Fall back to basic text extraction
        return page.get_text()
    
    def _reconstruct_from_text_blocks(self, text_dict: Dict, page_num: int) -> str:
        """Reconstruct text from PyMuPDF text blocks with proper table handling."""
        
        if not text_dict.get("blocks"):
            return ""
        
        # Group text blocks by approximate y-coordinate (rows)
        text_rows = []
        current_row_y = None
        current_row_blocks = []
        
        for block in text_dict["blocks"]:
            if "lines" not in block:
                continue
                
            block_y = block["bbox"][1]  # y0 coordinate
            
            # Start new row if y-coordinate differs significantly
            if current_row_y is None or abs(block_y - current_row_y) > 5:
                if current_row_blocks:
                    text_rows.append(self._process_text_row(current_row_blocks))
                current_row_blocks = [block]
                current_row_y = block_y
            else:
                current_row_blocks.append(block)
        
        # Process the last row
        if current_row_blocks:
            text_rows.append(self._process_text_row(current_row_blocks))
        
        return "\n".join(text_rows)
    
    def _process_text_row(self, blocks: List[Dict]) -> str:
        """Process a row of text blocks, handling table-like layouts."""
        
        # Sort blocks by x-coordinate (left to right)
        sorted_blocks = sorted(blocks, key=lambda b: b["bbox"][0])
        
        row_parts = []
        for block in sorted_blocks:
            block_text = ""
            
            for line in block.get("lines", []):
                line_text = ""
                for span in line.get("spans", []):
                    span_text = span.get("text", "").strip()
                    if span_text:
                        line_text += span_text + " "
                
                if line_text.strip():
                    block_text += line_text.strip() + " "
            
            if block_text.strip():
                row_parts.append(block_text.strip())
        
        # Join row parts with appropriate spacing
        if len(row_parts) == 1:
            return row_parts[0]
        elif len(row_parts) > 1:
            # Check if this looks like a table row
            if self._looks_like_table_row(row_parts):
                return " | ".join(row_parts)  # Table format
            else:
                return " ".join(row_parts)  # Regular text
        
        return ""
    
    def _looks_like_table_row(self, parts: List[str]) -> bool:
        """Determine if text parts represent a table row."""
        
        if len(parts) < 2:
            return False
        
        # Check for table indicators
        combined_text = " ".join(parts).lower()
        
        # PCI-specific table patterns
        table_indicators = [
            "defined approach requirements",
            "testing procedures", 
            "customized approach",
            "applicability notes",
            "purpose",
            "good practice",
            "examples"
        ]
        
        has_table_indicator = any(indicator in combined_text for indicator in table_indicators)
        
        # Check for control ID patterns in multiple parts
        control_pattern = re.compile(r'\d+\.\d+\.\d+')
        parts_with_controls = sum(1 for part in parts if control_pattern.search(part))
        
        return has_table_indicator or parts_with_controls >= 2
    
    def _extract_pdfplumber_with_cleanup(self, pdf_path: Path) -> str:
        """Table-aware extraction with header/footer removal."""
        content_parts = []
        
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages, 1):
                page_content = self._extract_page_with_cleanup(page, page_num)
                if page_content.content.strip():
                    # Add page marker with number for control tracking
                    content_parts.append(f"[PAGE {page_content.page_number}]")
                    content_parts.append(page_content.content)
        
        return "\n\n".join(content_parts)
    
    def _extract_page_with_cleanup(self, page, page_num: int) -> PageContent:
        """Extract content from a single page with proper cleanup."""
        # Extract raw text first
        raw_text = page.extract_text() or ""
        
        # Clean headers and footers
        cleaned_text = self._clean_page_content(raw_text, page_num)
        
        # Extract tables if present
        tables = page.extract_tables()
        has_tables = bool(tables)
        
        if has_tables:
            # Process tables and merge with cleaned text
            table_content = []
            for table in tables:
                if self._is_pci_table(table):
                    reconstructed = self._reconstruct_pci_table(table, page_num)
                    table_content.append(reconstructed)
                else:
                    table_text = self._table_to_text(table)
                    table_content.append(table_text)
            
            # Combine cleaned text with table content
            if table_content:
                all_content = cleaned_text + "\n\n" + "\n\n".join(table_content)
            else:
                all_content = cleaned_text
        else:
            all_content = cleaned_text
        
        # Extract control IDs and sections for metadata
        control_ids = self.pci_control_pattern.findall(all_content)
        sections = self._identify_sections(all_content)
        
        return PageContent(
            content=all_content,
            page_number=page_num,
            has_tables=has_tables,
            control_ids=control_ids,
            sections=sections
        )
    
    def _clean_page_content(self, content: str, page_num: int) -> str:
        """
        Enhanced page content cleaning with duplicate removal and better formatting.
        
        Args:
            content: Raw page content
            page_num: Page number for validation
            
        Returns:
            Cleaned content with headers/footers removed and duplicates reduced
        """
        if not content.strip():
            return ""
        
        lines = content.split('\n')
        cleaned_lines = []
        extracted_page_num = None
        seen_lines = set()  # Track duplicates
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Check if this line is a header
            is_header = any(pattern.match(line) for pattern in self.header_patterns)
            if is_header:
                continue
            
            # Check if this line is a footer and extract page number
            is_footer = False
            for pattern in self.footer_patterns:
                match = pattern.match(line)
                if match:
                    is_footer = True
                    # Try to extract page number from the match
                    if match.groups():
                        try:
                            extracted_page_num = int(match.group(1))
                        except (ValueError, IndexError):
                            pass
                    break
            
            if is_footer:
                continue
            
            # Skip very short lines that might be artifacts
            if len(line) <= 5:
                continue
            
            # Advanced duplicate detection for table content
            line_normalized = self._normalize_line_for_dedup(line)
            if line_normalized in seen_lines:
                # Check if this is a control marker - these can legitimately repeat
                if not self.pci_control_pattern.search(line):
                    continue  # Skip non-control duplicates
            
            seen_lines.add(line_normalized)
            cleaned_lines.append(line)
        
        # Post-process to improve formatting
        final_content = self._post_process_content_formatting(cleaned_lines)
        
        # Log page number discrepancies for debugging
        if extracted_page_num and extracted_page_num != page_num:
            self.logger.debug(f"Page number mismatch: expected {page_num}, extracted {extracted_page_num}")
        
        return final_content
    
    def _normalize_line_for_dedup(self, line: str) -> str:
        """Normalize line for duplicate detection."""
        # Remove extra whitespace and control characters
        normalized = ' '.join(line.split())
        
        # For table content, normalize common variations
        normalized = re.sub(r'\s*\|\s*', ' | ', normalized)  # Standardize table separators
        normalized = re.sub(r'\s*•\s*', ' • ', normalized)   # Standardize bullet points
        
        return normalized.lower()
    
    def _post_process_content_formatting(self, lines: List[str]) -> str:
        """Post-process content to improve formatting and reduce artifacts."""
        if not lines:
            return ""
        
        processed_lines = []
        i = 0
        
        while i < len(lines):
            current_line = lines[i]
            
            # Check for fragmented control definitions that should be joined
            if i + 1 < len(lines):
                next_line = lines[i + 1]
                
                # Join lines if current ends abruptly and next continues logically
                if (self._should_join_lines(current_line, next_line)):
                    # Join the lines with appropriate spacing
                    joined_line = current_line + " " + next_line
                    processed_lines.append(joined_line)
                    i += 2  # Skip the next line since we joined it
                    continue
            
            processed_lines.append(current_line)
            i += 1
        
        return '\n'.join(processed_lines)
    
    def _should_join_lines(self, current: str, next_line: str) -> bool:
        """Determine if two lines should be joined for better formatting."""
        
        # Don't join if either is a control marker
        if (self.pci_control_pattern.search(current) or 
            self.pci_control_pattern.search(next_line)):
            return False
        
        # Join if current line ends with a connector and next continues
        current_ends_with_connector = current.rstrip().endswith(('and', 'or', 'to', 'for', 'with', 'are:', 'is:'))
        next_starts_lowercase = next_line and next_line[0].islower()
        
        # Join if current is very short and next continues the thought
        current_very_short = len(current.strip()) < 30
        next_continues = next_starts_lowercase and not next_line.startswith('•')
        
        return (current_ends_with_connector and next_starts_lowercase) or (current_very_short and next_continues)
    
    def _extract_hybrid_with_cleanup(self, pdf_path: Path) -> str:
        """Hybrid extraction prioritizing PyMuPDF with enhanced layout preservation."""
        self.logger.info("Starting hybrid extraction (PyMuPDF-focused with enhanced cleanup)")
        
        # Step 1: Get content using enhanced PyMuPDF extraction (now primary)
        pymupdf_content = self._extract_basic_with_cleanup(pdf_path)
        self.logger.info(f"Enhanced PyMuPDF extraction: {len(pymupdf_content)} characters")
        
        # Step 2: Try pdfplumber as backup for table-heavy content
        pdfplumber_content = None
        
        try:
            pdfplumber_backup = self._extract_pdfplumber_with_cleanup(pdf_path)
            if pdfplumber_backup and len(pdfplumber_backup) > 1000:
                pdfplumber_content = pdfplumber_backup
                self.logger.info(f"PDFPlumber backup extraction: {len(pdfplumber_backup)} characters")
        except Exception as e:
            self.logger.warning(f"PDFPlumber backup extraction failed: {e}")
        
        # Step 3: Choose best extraction based on quality metrics
        if pdfplumber_content:
            combined_content = self._combine_clean_extractions(pymupdf_content, pdfplumber_content)
            self.logger.info(f"Final combined extraction: {len(combined_content)} characters")
            return combined_content
        else:
            self.logger.info("Using enhanced PyMuPDF extraction")
            return pymupdf_content
    
    def _combine_clean_extractions(self, pymupdf_content: str, pdfplumber_content: str) -> str:
        """Combine extractions prioritizing PyMuPDF while preserving complete controls."""
        # Now prioritize PyMuPDF content (better layout preservation)
        # but validate completeness against pdfplumber content
        
        pymupdf_controls = set(self.pci_control_pattern.findall(pymupdf_content))
        pdfplumber_controls = set(self.pci_control_pattern.findall(pdfplumber_content))
        
        self.logger.info(f"PyMuPDF extraction controls: {len(pymupdf_controls)}")
        self.logger.info(f"PDFPlumber extraction controls: {len(pdfplumber_controls)}")
        
        # Calculate quality metrics
        pymupdf_quality = self._calculate_content_quality(pymupdf_content)
        pdfplumber_quality = self._calculate_content_quality(pdfplumber_content)
        
        self.logger.info(f"PyMuPDF quality score: {pymupdf_quality:.3f}")
        self.logger.info(f"PDFPlumber quality score: {pdfplumber_quality:.3f}")
        
        # Choose based on control completeness and quality
        if len(pymupdf_controls) >= len(pdfplumber_controls) * 0.9 and pymupdf_quality >= pdfplumber_quality * 0.8:
            self.logger.info("Using PyMuPDF extraction (better layout preservation)")
            return pymupdf_content
        elif len(pdfplumber_controls) > len(pymupdf_controls) * 1.2:
            self.logger.info("Using PDFPlumber extraction (more complete controls)")
            return pdfplumber_content
        else:
            # Close call - prefer PyMuPDF for better formatting
            self.logger.info("Using PyMuPDF extraction (formatting preference)")
            return pymupdf_content
    
    def _calculate_content_quality(self, content: str) -> float:
        """Calculate content quality score based on structure and formatting."""
        if not content.strip():
            return 0.0
        
        quality_score = 0.0
        
        # Factor 1: Control completeness (40% weight)
        control_count = len(self.pci_control_pattern.findall(content))
        control_score = min(control_count / 200, 1.0)  # Normalize to expected ~200 controls
        quality_score += control_score * 0.4
        
        # Factor 2: Structure preservation (30% weight)
        lines = content.split('\n')
        non_empty_lines = [line for line in lines if line.strip()]
        
        # Good structure has reasonable line length distribution
        if non_empty_lines:
            avg_line_length = sum(len(line) for line in non_empty_lines) / len(non_empty_lines)
            # Prefer moderate line lengths (not too short/fragmented, not too long/run-together)
            line_length_score = 1.0 - abs(avg_line_length - 80) / 200  # Optimal around 80 chars
            line_length_score = max(0.0, min(1.0, line_length_score))
        else:
            line_length_score = 0.0
        
        quality_score += line_length_score * 0.3
        
        # Factor 3: Content density (20% weight)
        content_density = len(content.strip()) / max(len(lines), 1)
        density_score = min(content_density / 100, 1.0)  # Normalize
        quality_score += density_score * 0.2
        
        # Factor 4: Duplicate reduction (10% weight)
        unique_lines = set(line.strip() for line in lines if line.strip())
        if non_empty_lines:
            duplicate_ratio = 1.0 - (len(unique_lines) / len(non_empty_lines))
            dedup_score = 1.0 - duplicate_ratio  # Lower duplicates = higher score
        else:
            dedup_score = 0.0
        
        quality_score += dedup_score * 0.1
        
        return quality_score
    
    def _identify_sections(self, content: str) -> List[str]:
        """Identify document sections present in content."""
        sections = []
        content_lower = content.lower()
        
        section_keywords = {
            'requirements': ['defined approach requirements', 'requirements and testing'],
            'testing': ['testing procedures', 'examine', 'verify'],
            'customized': ['customized approach', 'objective'],
            'applicability': ['applicability notes'],
            'purpose': ['purpose'],
            'good_practice': ['good practice'],
            'examples': ['examples', 'for example']
        }
        
        for section_name, keywords in section_keywords.items():
            if any(keyword in content_lower for keyword in keywords):
                sections.append(section_name)
        
        return sections
    
    def _is_pci_table(self, table: List[List[str]]) -> bool:
        """Detect if a table contains PCI DSS control structure."""
        if not table or len(table) < 2:
            return False
        
        # Check for PCI table headers - handle None values
        flat_text = " ".join([" ".join(cell or "" for cell in row) for row in table if row]).lower()
        
        header_matches = sum(1 for header in self.pci_table_headers 
                           if header.lower() in flat_text)
        
        # Check for control IDs
        control_matches = len(self.pci_control_pattern.findall(flat_text))
        
        return header_matches >= 2 or control_matches >= 1
    
    def _reconstruct_pci_table(self, table: List[List[str]], page_num: int) -> str:
        """Reconstruct PCI DSS table into complete control blocks."""
        control_blocks = {}
        
        for row_idx, row in enumerate(table):
            for cell_idx, cell in enumerate(row):
                if not cell or cell is None:
                    continue
                
                # Look for control IDs
                matches = self.pci_control_pattern.findall(str(cell))
                for control_id in matches:
                    if control_id not in control_blocks:
                        control_blocks[control_id] = {
                            'main_requirement': '',
                            'testing_procedure': '',
                            'customized_approach': '',
                            'applicability_notes': '',
                            'purpose': '',
                            'good_practice': '',
                            'examples': '',
                            'page_number': page_num
                        }
                    
                    # Determine which section this cell belongs to
                    section = self._classify_table_section(cell, row, table)
                    
                    # Add content to appropriate section
                    if section in control_blocks[control_id]:
                        cell_text = str(cell or "").strip()
                        if cell_text and cell_text != control_id:  # Don't duplicate control ID
                            if control_blocks[control_id][section]:
                                control_blocks[control_id][section] += " " + cell_text
                            else:
                                control_blocks[control_id][section] = cell_text
        
        # Reconstruct complete control text with page metadata
        reconstructed_parts = []
        for control_id, sections in control_blocks.items():
            control_text = self._format_complete_control_with_page(control_id, sections, page_num)
            reconstructed_parts.append(control_text)
        
        return "\n\n".join(reconstructed_parts)
    
    def _classify_table_section(self, cell: str, row: List[str], table: List[List[str]]) -> str:
        """Classify which section of PCI DSS control a table cell belongs to."""
        cell_lower = str(cell or "").lower()
        row_text = " ".join(str(c or "") for c in row).lower()
        
        # Classification patterns with improved detection
        if any(pattern in cell_lower for pattern in ["examine", "verify", "test", "review", "interview", "observe"]):
            return "testing_procedure"
        elif "customized approach" in row_text or "objective" in row_text:
            return "customized_approach"
        elif "applicability" in row_text or "this requirement applies" in row_text:
            return "applicability_notes"
        elif "purpose" in row_text or "this requirement aims" in row_text:
            return "purpose"
        elif "good practice" in row_text or "guidance" in row_text:
            return "good_practice"
        elif "example" in row_text or "for example" in row_text:
            return "examples"
        else:
            return "main_requirement"
    
    def _format_complete_control_with_page(self, control_id: str, sections: Dict[str, str], page_num: int) -> str:
        """Format a complete PCI control block with page metadata."""
        parts = []
        
        # Add control header with page metadata
        parts.append(f"=== CONTROL {control_id} (Page {page_num}) ===")
        
        # Main requirement
        if sections['main_requirement']:
            parts.append(f"{control_id} {sections['main_requirement']}")
        
        # Testing procedure
        if sections['testing_procedure']:
            parts.append(f"{control_id} {sections['testing_procedure']}")
        
        # Additional sections with clear labels
        section_labels = {
            'customized_approach': 'Customized Approach Objective',
            'applicability_notes': 'Applicability Notes', 
            'purpose': 'Purpose',
            'good_practice': 'Good Practice',
            'examples': 'Examples'
        }
        
        for section_key, label in section_labels.items():
            if sections[section_key]:
                parts.append(f"{label}: {sections[section_key]}")
        
        parts.append(f"=== END CONTROL {control_id} ===")
        
        return "\n".join(parts)
    
    def _table_to_text(self, table: List[List[str]]) -> str:
        """Convert table to structured text format."""
        if not table:
            return ""
        
        text_rows = []
        for row in table:
            if row and any(cell for cell in row if cell):  # Skip empty rows
                row_text = " | ".join(str(cell or "") for cell in row)
                text_rows.append(row_text)
        
        return "\n".join(text_rows)
    
    def _dataframe_to_text(self, df, table_name: str) -> str:
        """Convert pandas DataFrame to text format."""
        try:
            return f"[{table_name}]\n" + df.to_string(index=False, header=False)
        except Exception:
            return f"[{table_name}]\n(Table conversion failed)"
    
    # Keep tabula and camelot methods unchanged
    def _extract_tabula(self, pdf_path: Path) -> str:
        """Extract tables using tabula-py."""
        if not TABULA_AVAILABLE:
            return self._extract_basic_with_cleanup(pdf_path)
        
        try:
            tables = tabula.read_pdf(
                str(pdf_path), 
                pages='all', 
                multiple_tables=True,
                pandas_options={'header': None}
            )
            
            content_parts = []
            for i, table in enumerate(tables):
                table_text = self._dataframe_to_text(table, f"Table_{i}")
                content_parts.append(table_text)
            
            return "\n".join(content_parts)
            
        except Exception as e:
            self.logger.error(f"Tabula extraction failed: {e}")
            return self._extract_basic_with_cleanup(pdf_path)
    
    def _extract_camelot(self, pdf_path: Path) -> str:
        """Extract tables using camelot-py."""
        if not CAMELOT_AVAILABLE:
            return self._extract_basic_with_cleanup(pdf_path)
        
        try:
            tables = camelot.read_pdf(str(pdf_path), pages='all', flavor='lattice')
            
            content_parts = []
            for table in tables:
                table_text = self._dataframe_to_text(table.df, f"Camelot_Table")
                content_parts.append(table_text)
            
            return "\n".join(content_parts)
            
        except Exception as e:
            self.logger.error(f"Camelot extraction failed: {e}")
            return self._extract_basic_with_cleanup(pdf_path)
    
    def extract_pci_controls(self, pdf_path: Path) -> List[PCIControlBlock]:
        """Extract complete PCI control blocks from PDF."""
        content = self.extract_content(pdf_path, ExtractionStrategy.HYBRID)
        
        # This would implement the complete control block extraction
        # For now, return empty list - this can be expanded
        return []


def create_enhanced_processor() -> EnhancedPDFProcessor:
    """Factory function to create enhanced PDF processor."""
    return EnhancedPDFProcessor() 