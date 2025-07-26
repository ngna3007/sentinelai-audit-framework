"""
Text Processing Utilities for AWS Config Guidance

This module provides specialized text processing utilities for AWS Config guidance
documents, including cleaning, normalization, and AWS-specific text processing.
"""

from logging import getLogger
from typing import List, Dict, Any, Set
import re


class TextProcessor:
    """
    Provides text processing utilities for AWS Config guidance documents.
    """
    
    def __init__(self):
        self.logger = getLogger(__name__)
        
        # Common AWS service abbreviations and full names
        self.aws_services = {
            'EC2': 'Amazon Elastic Compute Cloud',
            'S3': 'Amazon Simple Storage Service',
            'IAM': 'AWS Identity and Access Management',
            'VPC': 'Amazon Virtual Private Cloud',
            'RDS': 'Amazon Relational Database Service',
            'EBS': 'Amazon Elastic Block Store',
            'ELB': 'Elastic Load Balancing',
            'CloudTrail': 'AWS CloudTrail',
            'CloudWatch': 'Amazon CloudWatch',
            'Config': 'AWS Config',
            'KMS': 'AWS Key Management Service',
            'SNS': 'Amazon Simple Notification Service',
            'SQS': 'Amazon Simple Queue Service',
            'Lambda': 'AWS Lambda'
        }
    
    def clean_markdown_content(self, content: str) -> str:
        """
        Clean and normalize markdown content for AWS Config guidance.
        
        Args:
            content: Raw markdown content
            
        Returns:
            Cleaned markdown content
        """
        # Remove extra whitespace and normalize line breaks
        content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
        
        # Fix common PDF conversion issues
        content = self._fix_hyphenated_words(content)
        content = self._normalize_whitespace(content)
        content = self._standardize_aws_terms(content)
        content = self._clean_table_formatting(content)
        
        return content.strip()
    
    def _fix_hyphenated_words(self, content: str) -> str:
        """Fix words that were hyphenated across line breaks."""
        # Pattern: word- followed by newline and word continuation
        pattern = r'(\w)-\s*\n\s*(\w)'
        return re.sub(pattern, r'\1\2', content)
    
    def _normalize_whitespace(self, content: str) -> str:
        """Normalize whitespace while preserving markdown structure."""
        lines = content.split('\n')
        cleaned_lines = []
        
        for line in lines:
            # Don't normalize whitespace in code blocks or tables
            if line.strip().startswith('```') or '|' in line:
                cleaned_lines.append(line)
            else:
                # Normalize internal whitespace but preserve leading/trailing for lists
                if line.strip().startswith(('-', '*', '+')):
                    # Preserve list formatting
                    cleaned_lines.append(re.sub(r'  +', ' ', line))
                else:
                    # Normal line - collapse multiple spaces
                    cleaned_lines.append(re.sub(r'\s+', ' ', line).strip())
        
        return '\n'.join(cleaned_lines)
    
    def _standardize_aws_terms(self, content: str) -> str:
        """Standardize AWS service names and terms."""
        # Fix common spacing issues
        content = re.sub(r'AWS\s+Config', 'AWS Config', content, flags=re.IGNORECASE)
        content = re.sub(r'PCI\s+DSS', 'PCI DSS', content, flags=re.IGNORECASE)
        content = re.sub(r'Amazon\s+Web\s+Services', 'Amazon Web Services', content, flags=re.IGNORECASE)
        
        # Standardize AWS service references
        for abbrev, full_name in self.aws_services.items():
            # Don't replace if it's already in the full form
            if full_name.lower() not in content.lower():
                # Replace standalone abbreviations with full names in parentheses
                pattern = r'\b' + re.escape(abbrev) + r'\b(?!\s*\()'
                replacement = f"{abbrev} ({full_name})"
                content = re.sub(pattern, replacement, content)
        
        return content
    
    def _clean_table_formatting(self, content: str) -> str:
        """Clean up table formatting issues from PDF conversion."""
        lines = content.split('\n')
        cleaned_lines = []
        
        for line in lines:
            if '|' in line:
                # Clean up table rows
                line = re.sub(r'\|\s*\|\s*\|', '| |', line)  # Fix empty cells
                line = re.sub(r'\s*\|\s*', ' | ', line)     # Normalize spacing around pipes
                line = line.strip()
            
            cleaned_lines.append(line)
        
        return '\n'.join(cleaned_lines)
    
    def extract_aws_terms(self, content: str) -> List[str]:
        """Extract AWS-specific terms and services."""
        aws_terms = set()
        
        # Pattern for AWS services (case-insensitive)
        aws_patterns = [
            r'\bAWS\s+[A-Z][a-zA-Z\s]+\b',
            r'\bAmazon\s+[A-Z][a-zA-Z\s]+\b',
            r'\b(?:EC2|S3|IAM|VPC|RDS|EBS|ELB|CloudTrail|CloudWatch|Config|KMS|SNS|SQS|Lambda)\b'
        ]
        
        for pattern in aws_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                cleaned_match = match.strip()
                if self._is_valid_aws_term(cleaned_match):
                    aws_terms.add(cleaned_match)
        
        return sorted(list(aws_terms))
    
    def _is_valid_aws_term(self, term: str) -> bool:
        """Validate if a term is a legitimate AWS service or term."""
        term_lower = term.lower()
        
        # Must contain AWS, Amazon, or be a known service
        if not any(keyword in term_lower for keyword in ['aws', 'amazon'] + [s.lower() for s in self.aws_services.keys()]):
            return False
        
        # Should not be too long or contain invalid characters
        if len(term) > 60 or any(char in term for char in ['(', ')', '[', ']', '{', '}']):
            return False
        
        # Should not end with common non-service words
        exclude_endings = ['and', 'or', 'the', 'for', 'with', 'in', 'on', 'at']
        words = term.lower().split()
        if words and words[-1] in exclude_endings:
            return False
        
        return True
    
    def extract_config_rule_references(self, content: str) -> List[Dict[str, Any]]:
        """Extract AWS Config rule references with context."""
        rule_references = []
        
        # Patterns for different types of Config rule references
        patterns = [
            {
                'pattern': r'\b([a-z-]+(?:-compliance|-compliant|-enabled|-required))\b',
                'type': 'compliance_rule',
                'description': 'Compliance-related Config rules'
            },
            {
                'pattern': r'\b(config[-_][a-z0-9-]+)\b',
                'type': 'config_prefixed',
                'description': 'Config-prefixed rules'
            },
            {
                'pattern': r'\b([A-Z_]+[-_][A-Z_0-9-]+)\b',
                'type': 'uppercase_rule',
                'description': 'Uppercase Config rule format'
            },
            {
                'pattern': r'\b([a-z0-9]+[-_][a-z0-9-]+[-_][a-z0-9-]+)\b',
                'type': 'multi_part',
                'description': 'Multi-part rule names'
            }
        ]
        
        lines = content.split('\n')
        
        for i, line in enumerate(lines):
            for pattern_info in patterns:
                matches = re.findall(pattern_info['pattern'], line, re.IGNORECASE)
                for match in matches:
                    if self._is_likely_config_rule_name(match):
                        rule_references.append({
                            'rule_name': match,
                            'line_number': i + 1,
                            'context': line.strip(),
                            'rule_type': pattern_info['type'],
                            'description': pattern_info['description']
                        })
        
        # Remove duplicates
        seen_rules = set()
        unique_references = []
        for ref in rule_references:
            rule_key = ref['rule_name'].lower()
            if rule_key not in seen_rules:
                seen_rules.add(rule_key)
                unique_references.append(ref)
        
        return unique_references
    
    def _is_likely_config_rule_name(self, name: str) -> bool:
        """Determine if a name is likely a Config rule."""
        name_lower = name.lower()
        
        # Length check
        if len(name) < 5 or len(name) > 100:
            return False
        
        # Must have separators (hyphens or underscores)
        if not any(sep in name for sep in ['-', '_']):
            return False
        
        # Should contain Config-related keywords
        config_keywords = [
            'compliance', 'compliant', 'enabled', 'required', 'config',
            'security', 'encryption', 'access', 'logging', 'monitoring',
            'backup', 'snapshot', 'public', 'private', 'policy'
        ]
        
        has_config_keyword = any(keyword in name_lower for keyword in config_keywords)
        
        # Should not be common non-rule words
        exclude_words = [
            'this', 'that', 'with', 'from', 'into', 'section',
            'table', 'figure', 'page', 'document', 'example'
        ]
        
        is_excluded = name_lower in exclude_words
        
        return has_config_keyword and not is_excluded
    
    def extract_pci_requirements(self, content: str) -> List[Dict[str, Any]]:
        """Extract PCI DSS requirement references."""
        requirements = []
        
        # Patterns for PCI DSS requirements
        pci_patterns = [
            {
                'pattern': r'\b(?:PCI\s*DSS\s*)?(?:Requirement\s*)?(\d+\.\d+(?:\.\d+)?)\b',
                'type': 'numbered_requirement'
            },
            {
                'pattern': r'\b(Req\s*\d+\.\d+(?:\.\d+)?)\b',
                'type': 'abbreviated_requirement'
            },
            {
                'pattern': r'\b(\d+\.\d+(?:\.\d+)?)\s*(?:requirement|req)\b',
                'type': 'suffixed_requirement'
            }
        ]
        
        lines = content.split('\n')
        
        for i, line in enumerate(lines):
            line_lower = line.lower()
            
            # Only look in lines that mention PCI or requirements
            if any(keyword in line_lower for keyword in ['pci', 'requirement', 'req', 'compliance']):
                for pattern_info in pci_patterns:
                    matches = re.findall(pattern_info['pattern'], line, re.IGNORECASE)
                    for match in matches:
                        requirements.append({
                            'requirement_id': match.strip(),
                            'line_number': i + 1,
                            'context': line.strip(),
                            'pattern_type': pattern_info['type'],
                            'full_context': self._get_surrounding_context(lines, i, 2)
                        })
        
        # Remove duplicates
        seen_reqs = set()
        unique_requirements = []
        for req in requirements:
            req_key = req['requirement_id'].lower()
            if req_key not in seen_reqs:
                seen_reqs.add(req_key)
                unique_requirements.append(req)
        
        return unique_requirements
    
    def _get_surrounding_context(self, lines: List[str], current_line: int, context_size: int) -> str:
        """Get surrounding context for a line."""
        start = max(0, current_line - context_size)
        end = min(len(lines), current_line + context_size + 1)
        return '\n'.join(lines[start:end]).strip()
    
    def normalize_whitespace(self, text: str) -> str:
        """Simple whitespace normalization."""
        return re.sub(r'\s+', ' ', text).strip()
    
    def clean_special_characters(self, text: str) -> str:
        """Clean special characters that might interfere with processing."""
        # Replace common problematic characters
        replacements = {
            '\u2013': '-',  # en dash
            '\u2014': '--', # em dash
            '\u2018': "'",  # left single quotation mark
            '\u2019': "'",  # right single quotation mark
            '\u201c': '"',  # left double quotation mark
            '\u201d': '"',  # right double quotation mark
            '\u2022': '*',  # bullet
            '\u00a0': ' ',  # non-breaking space
        }
        
        for old, new in replacements.items():
            text = text.replace(old, new)
        
        return text
    
    def extract_implementation_steps(self, content: str) -> List[Dict[str, Any]]:
        """Extract numbered implementation steps or procedures."""
        steps = []
        lines = content.split('\n')
        
        # Patterns for numbered steps
        step_patterns = [
            r'^(\d+)\.\s+(.+)$',           # 1. Step description
            r'^Step\s+(\d+):\s*(.+)$',     # Step 1: Description
            r'^(\d+)\)\s+(.+)$',           # 1) Step description
        ]
        
        for i, line in enumerate(lines):
            line = line.strip()
            
            for pattern in step_patterns:
                match = re.match(pattern, line, re.IGNORECASE)
                if match:
                    step_number = match.group(1)
                    step_description = match.group(2).strip()
                    
                    steps.append({
                        'step_number': int(step_number),
                        'description': step_description,
                        'line_number': i + 1,
                        'context': self._get_surrounding_context(lines, i, 1)
                    })
                    break
        
        return steps
    
    def clean_br_tags(self, content: str, remove_all: bool = False) -> str:
        """
        Clean <br> tags from content with intelligent handling.
        
        Args:
            content: Text content containing <br> tags
            remove_all: If True, remove all <br> tags. If False, intelligently handle them.
            
        Returns:
            Cleaned content
        """
        if remove_all:
            # For config rules and other cases where we want no br tags at all
            return re.sub(r'<br\s*/?>', '', content)
        else:
            # Intelligent handling - rejoin broken words or add spaces
            content = self._fix_br_tags_intelligent(content)
            # Note: Whitespace patterns are now applied separately in content processor
            return content

    def _clean_whitespace_patterns(self, content: str) -> str:
        """
        Clean specific whitespace patterns in the content.
        
        Handles:
        1. Remove whitespace inside single quotes: 'accessLo gSettings' → 'accessLogSettings'
        2. Add whitespace before and after single quotes: "is'http-only'" → "is 'http-only'" (DISABLED)
        3. Fix broken CamelCase words: "ClusterEn dpointEncryptionType" → "ClusterEndpointEncryptionType"
        4. Remove whitespace inside parentheses with underscores: "(some_func tion_name)" → "(some_function_name)"
        
        Args:
            content: Text content to clean
            
        Returns:
            Content with cleaned whitespace patterns
        """
        # Pattern 1: Remove whitespace inside single quotes
        # Match 'text with spaces inside' and remove internal spaces
        def clean_quoted_text(match):
            quote_content = match.group(1)
            # Remove all whitespace inside the quotes
            cleaned_content = re.sub(r'\s+', '', quote_content)
            return f"'{cleaned_content}'"
        
        content = re.sub(r"'([^']*?)'", clean_quoted_text, content)
        
        # Pattern 2: Add whitespace before and after single quotes (but not inside)
        # TEMPORARILY DISABLED - this pattern is interfering with Pattern 1
        # Only match quotes that are directly attached to words (no spaces)
        # Handle word'quoted'word -> word 'quoted' word (only when directly attached)
        # content = re.sub(r"(\w)'([^']*?)'(\w)", r"\1 '\2' \3", content)
        # Handle word'quoted' at end -> word 'quoted' (only when directly attached)
        # content = re.sub(r"(\w)'([^']*?)'(?=\s|$|[.,;:])", r"\1 '\2'", content)
        # Handle start'quoted'word -> 'quoted' word (only when directly attached)
        # content = re.sub(r"(^|[\s.,;:])'([^']*?)'(\w)", r"\1'\2' \3", content)
        
        # Pattern 3: Fix broken CamelCase words
        content = self._fix_broken_camelcase(content)
        
        # Pattern 4: Remove whitespace inside parentheses that contain underscores
        # Match (content_with_underscores and spaces) and remove internal spaces
        def clean_parentheses_with_underscores(match):
            paren_content = match.group(1)
            # Only clean if content contains underscores
            if '_' in paren_content:
                # Remove all whitespace inside the parentheses
                cleaned_content = re.sub(r'\s+', '', paren_content)
                return f"({cleaned_content})"
            else:
                # Keep original if no underscores
                return match.group(0)
        
        content = re.sub(r'\(([^)]*?)\)', clean_parentheses_with_underscores, content)
        
        return content

    def _fix_broken_camelcase(self, content: str) -> str:
        """
        Fix broken CamelCase words like 'ClusterEn dpointEncryptionType' → 'ClusterEndpointEncryptionType'
        
        Pattern: CapitalLetter + lowercase letters + space + lowercase letters (continuing the word)
        """
        # Pattern to match broken CamelCase: Word with capital letter, followed by space and lowercase continuation
        # Examples: "ClusterEn dpointEncryptionType", "DefaultCa cheBehavior"
        camelcase_pattern = r'\b([A-Z][a-z]+(?:[A-Z][a-z]*)*)\s+([a-z]+(?:[A-Z][a-z]*)*)\b'
        
        def fix_camelcase_match(match):
            part1 = match.group(1)  # e.g., "ClusterEn" or "DefaultCa"
            part2 = match.group(2)  # e.g., "dpointEncryptionType" or "cheBehavior"
            
            # Check if this looks like a broken CamelCase word
            if self._is_broken_camelcase(part1, part2):
                return part1 + part2
            else:
                # Keep the space if it doesn't look like a broken CamelCase word
                return match.group(0)
        
        return re.sub(camelcase_pattern, fix_camelcase_match, content)

    def _is_broken_camelcase(self, part1: str, part2: str) -> bool:
        """
        Determine if two parts represent a broken CamelCase word that should be rejoined.
        
        Args:
            part1: First part (e.g., "ClusterEn")
            part2: Second part (e.g., "dpointEncryptionType")
            
        Returns:
            True if they should be rejoined, False otherwise
        """
        # Known AWS/tech term patterns that commonly get broken
        known_broken_patterns = [
            # AWS service/feature names
            ('Cluster', 'EndpointEncryptionType'),
            ('ClusterEn', 'dpointEncryptionType'),
            ('Default', 'CacheBehavior'),
            ('DefaultCa', 'cheBehavior'),
            ('Access', 'LogSettings'),
            ('AccessLo', 'gSettings'),
            ('Security', 'Group'),
            ('SecurityGro', 'up'),
            ('Elastic', 'LoadBalancer'),
            ('ElasticLo', 'adBalancer'),
            ('Cloud', 'FormationTemplate'),
            ('CloudFor', 'mationTemplate'),
            ('Cloud', 'TrailEvents'),
            ('CloudTr', 'ailEvents'),
            ('Auto', 'ScalingGroup'),
            ('AutoSca', 'lingGroup'),
            ('Target', 'HealthCheck'),
            ('TargetHe', 'althCheck'),
            ('Network', 'AccessControl'),
            ('NetworkAc', 'cessControl'),
            ('Public', 'AccessBlock'),
            ('PublicAc', 'cessBlock'),
            ('Multi', 'FactorAuthentication'),
            ('MultiFac', 'torAuthentication'),
            ('Certificate', 'Authority'),
            ('CertificateAu', 'thority'),
            ('Encryption', 'Configuration'),
            ('EncryptionCon', 'figuration'),
            ('Instance', 'MetadataOptions'),
            ('InstanceMeta', 'dataOptions'),
            ('Resource', 'Policy'),
            ('ResourcePo', 'licy'),
        ]
        
        # Check exact matches first
        combined = part1 + part2
        for known_part1, known_part2 in known_broken_patterns:
            if (part1 == known_part1 and part2 == known_part2) or combined == known_part1 + known_part2:
                return True
        
        # Pattern-based detection
        # 1. If part1 ends with incomplete common prefixes and part2 starts with the completion
        common_break_patterns = [
            (r'.*En$', r'^dpoin.*'),           # ClusterEn + dpointEncryptionType
            (r'.*Ca$', r'^che.*'),             # DefaultCa + cheBehavior  
            (r'.*Lo$', r'^[gd].*'),            # AccessLo + gSettings, ElasticLo + adBalancer
            (r'.*Ac$', r'^cess.*'),            # PublicAc + cessBlock
            (r'.*For$', r'^mation.*'),         # CloudFor + mationTemplate
            (r'.*Tr$', r'^ail.*'),             # CloudTr + ailEvents
            (r'.*Sca$', r'^ling.*'),           # AutoSca + lingGroup
            (r'.*He$', r'^alth.*'),            # TargetHe + althCheck
            (r'.*Meta$', r'^data.*'),          # InstanceMeta + dataOptions
            (r'.*Con$', r'^fig.*'),            # EncryptionCon + figuration
            (r'.*Po$', r'^licy.*'),            # ResourcePo + licy
            (r'.*Fac$', r'^tor.*'),            # MultiFac + torAuthentication
            (r'.*Au$', r'^th.*'),              # CertificateAu + thority
            (r'.*Gro$', r'^up.*'),             # SecurityGro + up
        ]
        
        for part1_pattern, part2_pattern in common_break_patterns:
            if re.match(part1_pattern, part1) and re.match(part2_pattern, part2):
                return True
        
        # 2. General heuristics
        # If the combined length suggests a reasonable compound word
        total_length = len(part1) + len(part2)
        if 8 <= total_length <= 40:  # Reasonable compound word length
            # Check if part1 ends abruptly (likely broken)
            if len(part1) >= 3 and part1[-2:].lower() in ['en', 'ca', 'lo', 'ac', 'tr', 'he', 'au', 'po', 'gr']:
                return True
            
            # Check if part2 starts with lowercase (continuation of CamelCase)
            if part2[0].islower() and len(part2) > 3:
                # And contains more CamelCase after
                if re.search(r'[A-Z]', part2[1:]):
                    return True
        
        return False 
    
    def _fix_br_tags_intelligent(self, content: str) -> str:
        """Intelligently handle br tags - rejoin broken words or add spaces between words."""
        
        # Pattern to find text<br>text sequences
        br_pattern = r'(\S+)<br\s*/?>\s*(\S+)'
        
        def fix_br_match(match):
            before = match.group(1)
            after = match.group(2)
            
            # Check if this looks like a broken word that should be rejoined
            if self._is_broken_word(before, after):
                return before + after
            else:
                # This looks like separate words that need a space
                return before + ' ' + after
        
        # Apply the fix repeatedly until no more matches
        while re.search(br_pattern, content):
            content = re.sub(br_pattern, fix_br_match, content)
        
        # Handle any remaining <br> tags
        content = re.sub(r'<br\s*/?>', ' ', content)
        
        return content

    def _is_broken_word(self, before: str, after: str) -> bool:
        """Determine if before<br>after represents a broken word that should be rejoined."""
        
        # If either part is a complete common word, don't join
        common_complete_words = {
            'amazon', 'aws', 'cloud', 'config', 'service', 'policy', 'security', 
            'network', 'the', 'and', 'or', 'for', 'with', 'from', 'to', 'in', 'on', 'at', 'by',
            'is', 'are', 'was', 'were', 'have', 'has', 'had', 'will', 'would', 'could',
            'between', 'through', 'during', 'before', 'after', 'above', 'below', 'ensure',
            'that', 'this', 'rule', 'if', 'not', 'use', 'using', 'does', 'do'
        }
        
        if before.lower() in common_complete_words or after.lower() in common_complete_words:
            return False
        
        # Specific patterns for obviously broken words that should be rejoined
        obvious_broken_patterns = [
            # AWS service names that got broken
            (r'cloudfront$', r'^$'),           # CloudFront -> CloudFront 
            (r'cloud$', r'^front$'),       # Cloud Front -> CloudFront
            
            # Common word breaks
            (r'distribut$', r'^ions?$'),          # distribut-ions
            (r'configur$', r'^ation$'),           # configur-ation  
            (r'applica$', r'^tions?$'),           # applica-tions
            (r'certifica$', r'^tes?$'),           # certifica-tes
            (r'communica$', r'^tion$'),           # communica-tion
            (r'implementa$', r'^tion$'),          # implementa-tion
            (r'non_compl$', r'^iant$'),           # NON_COMPL-IANT
            (r'fragmente$', r'^d$'),              # fragmente-d
            (r'associate$', r'^d$'),              # associate-d
            (r'relationa$', r'^l$'),              # relationa-l
            (r'accessibl$', r'^e$'),              # accessibl-e
            (r'identifi$', r'^[eé]r?$'),          # identifie-r
            
            # Short broken parts (likely hyphenated words)
            (r'.{1,3}$', r'^.{1,3}$'),                   # Very short parts usually broken
        ]
        
        # Check specific patterns
        for before_pattern, after_pattern in obvious_broken_patterns:
            if re.search(before_pattern, before, re.IGNORECASE) and re.search(after_pattern, after, re.IGNORECASE):
                return True
        
        # Only join if it looks like a hyphenated compound word ending
        compound_suffixes = r'^(ing|ed|tion|ation|able|ible|ent|ant|ial|ous|ive|er|est|ly|ness|less|ful)$'
        if re.search(r'[a-z]$', before) and re.search(compound_suffixes, after, re.IGNORECASE):
            return True
            
        # Don't join anything else - err on the side of adding spaces
        return False