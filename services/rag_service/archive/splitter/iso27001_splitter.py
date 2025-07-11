"""
ISO/IEC 27001:2022 document splitter implementation.

This is a template implementation for ISO 27001 document splitting.
Customize based on specific document structure and requirements.
"""

import re
from typing import List, Optional
from .base import BaseSplitter, Chunk


class ISO27001Splitter(BaseSplitter):
    """Splitter for ISO/IEC 27001:2022 documents."""
    
    def __init__(self, max_tokens: int = 350, overlap_tokens: int = 50):
        super().__init__(max_tokens, overlap_tokens)
        # ISO 27001 typically uses A.x.x.x control numbering
        self.control_pattern = re.compile(r'(A\.\d+\.\d+(?:\.\d+)*)')
        
    def get_standard_name(self) -> str:
        return "iso27001"
    
    def split_document(
        self, 
        content: str, 
        source_document: str, 
        preserve_structure: bool = False,
        **kwargs
    ) -> List[Chunk]:
        """
        Split ISO 27001 document into chunks.
        
        Args:
            content: Document text content
            source_document: Source document filename
            preserve_structure: Whether to preserve control hierarchy
            
        Returns:
            List of Chunk objects
        """
        # For ISO 27001, we typically use semantic splitting
        # rather than strict control-based splitting
        if preserve_structure:
            chunks = self._split_by_sections(content, source_document)
        else:
            chunks = self._split_semantically(content, source_document)
            
        return chunks
    
    def _split_by_sections(self, content: str, source_document: str) -> List[Chunk]:
        """Split document by ISO 27001 sections."""
        chunks = []
        
        # Extract sections based on headings and control patterns
        sections = self._extract_sections(content)
        
        chunk_index = 0
        for section in sections:
            control_id = self._extract_control_id(section['content'])
            
            if self._count_tokens(section['content']) > self.max_tokens:
                # Split large sections
                sub_chunks = self._split_large_section(
                    section['content'],
                    control_id,
                    source_document,
                    chunk_index
                )
                chunks.extend(sub_chunks)
                chunk_index += len(sub_chunks)
            else:
                chunk = Chunk(
                    id=f"{source_document}_{chunk_index}",
                    content=self._clean_text(section['content']),
                    token_count=self._count_tokens(section['content']),
                    source_document=source_document,
                    section=section.get('heading'),
                    control_id=control_id,
                    standard=self.get_standard_name(),
                    chunk_index=chunk_index,
                    metadata=self._extract_metadata(section['content'])
                )
                chunks.append(chunk)
                chunk_index += 1
                
        return chunks
    
    def _split_semantically(self, content: str, source_document: str) -> List[Chunk]:
        """Split document semantically by paragraphs and sentences."""
        chunks = []
        
        # Split by paragraphs first
        paragraphs = content.split('\n\n')
        
        current_chunk = []
        current_tokens = 0
        chunk_index = 0
        
        for paragraph in paragraphs:
            paragraph = paragraph.strip()
            if not paragraph:
                continue
                
            para_tokens = self._count_tokens(paragraph)
            
            if current_tokens + para_tokens > self.max_tokens and current_chunk:
                # Create chunk from current content
                chunk_content = '\n\n'.join(current_chunk)
                control_id = self._extract_control_id(chunk_content)
                
                chunk = Chunk(
                    id=f"{source_document}_{chunk_index}",
                    content=self._clean_text(chunk_content),
                    token_count=current_tokens,
                    source_document=source_document,
                    control_id=control_id,
                    standard=self.get_standard_name(),
                    chunk_index=chunk_index,
                    metadata=self._extract_metadata(chunk_content)
                )
                chunks.append(chunk)
                chunk_index += 1
                
                # Start new chunk
                current_chunk = [paragraph]
                current_tokens = para_tokens
            else:
                current_chunk.append(paragraph)
                current_tokens += para_tokens
        
        # Add final chunk
        if current_chunk:
            chunk_content = '\n\n'.join(current_chunk)
            control_id = self._extract_control_id(chunk_content)
            
            chunk = Chunk(
                id=f"{source_document}_{chunk_index}",
                content=self._clean_text(chunk_content),
                token_count=current_tokens,
                source_document=source_document,
                control_id=control_id,
                standard=self.get_standard_name(),
                chunk_index=chunk_index,
                metadata=self._extract_metadata(chunk_content)
            )
            chunks.append(chunk)
            
        return chunks
    
    def _extract_sections(self, content: str) -> List[dict]:
        """Extract sections from ISO 27001 document."""
        sections = []
        lines = content.split('\n')
        current_section = []
        current_heading = None
        
        for line in lines:
            # Check if line is a heading (customize based on document format)
            if self._is_heading(line):
                if current_section:
                    sections.append({
                        'content': '\n'.join(current_section),
                        'heading': current_heading
                    })
                current_section = [line]
                current_heading = line.strip()
            else:
                current_section.append(line)
        
        # Add final section
        if current_section:
            sections.append({
                'content': '\n'.join(current_section),
                'heading': current_heading
            })
            
        return sections
    
    def _is_heading(self, line: str) -> bool:
        """Determine if a line is a heading."""
        # Customize based on document format
        line = line.strip()
        
        # Check for control IDs
        if self.control_pattern.search(line):
            return True
            
        # Check for numbered headings
        if re.match(r'^\d+(\.\d+)*\s+', line):
            return True
            
        # Check for capitalized short lines
        if len(line) < 100 and line.isupper():
            return True
            
        return False
    
    def _extract_control_id(self, content: str) -> Optional[str]:
        """Extract ISO 27001 control ID from content."""
        match = self.control_pattern.search(content)
        return match.group(1) if match else None
    
    def _split_large_section(
        self,
        content: str,
        control_id: Optional[str],
        source_document: str,
        start_index: int
    ) -> List[Chunk]:
        """Split a large section into smaller chunks."""
        chunks = []
        sentences = re.split(r'(?<=[.!?])\s+', content)
        
        current_chunk = []
        current_tokens = 0
        chunk_index = start_index
        
        for sentence in sentences:
            sentence_tokens = self._count_tokens(sentence)
            
            if current_tokens + sentence_tokens > self.max_tokens and current_chunk:
                chunk_content = ' '.join(current_chunk)
                chunk = Chunk(
                    id=f"{source_document}_{chunk_index}",
                    content=self._clean_text(chunk_content),
                    token_count=current_tokens,
                    source_document=source_document,
                    control_id=control_id,
                    standard=self.get_standard_name(),
                    chunk_index=chunk_index,
                    metadata=self._extract_metadata(chunk_content)
                )
                chunks.append(chunk)
                chunk_index += 1
                current_chunk = [sentence]
                current_tokens = sentence_tokens
            else:
                current_chunk.append(sentence)
                current_tokens += sentence_tokens
        
        # Add final chunk
        if current_chunk:
            chunk_content = ' '.join(current_chunk)
            chunk = Chunk(
                id=f"{source_document}_{chunk_index}",
                content=self._clean_text(chunk_content),
                token_count=current_tokens,
                source_document=source_document,
                control_id=control_id,
                standard=self.get_standard_name(),
                chunk_index=chunk_index,
                metadata=self._extract_metadata(chunk_content)
            )
            chunks.append(chunk)
            
        return chunks
    
    def _extract_metadata(self, content: str) -> dict:
        """Extract ISO 27001 specific metadata."""
        metadata = {}
        
        # Extract information security domains
        domains = []
        iso_domains = [
            'information security policy', 'organization of information security',
            'human resource security', 'asset management', 'access control',
            'cryptography', 'physical and environmental security',
            'operations security', 'communications security',
            'system acquisition', 'supplier relationships',
            'information security incident management',
            'business continuity', 'compliance'
        ]
        
        content_lower = content.lower()
        for domain in iso_domains:
            if domain in content_lower:
                domains.append(domain)
                
        if domains:
            metadata['security_domains'] = domains
            
        # Extract requirement type
        if 'shall' in content_lower:
            metadata['type'] = 'requirement'
        elif 'should' in content_lower:
            metadata['type'] = 'recommendation'
        elif 'may' in content_lower:
            metadata['type'] = 'guidance'
            
        return metadata 