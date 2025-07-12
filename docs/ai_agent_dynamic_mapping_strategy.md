# AI Agent Dynamic Mapping Strategy

## The Concept: AI-Driven Evidence Discovery

Instead of pre-extracting every possible control mapping, let the **AI Agent reason** about what evidence to collect based on the Knowledge Base content.

## Two-Tier Approach

### Tier 1: Known Exact Mappings (Fast Path)
```python
# For well-defined, frequently-used controls
exact_mappings = {
    "1.2.5": {
        "evidence_service": "cloudfront",
        "evidence_type": "distributions", 
        "evaluation": "any(protocol == 'SSLv3' for dist in evidence for origin in dist['origins'] for protocol in origin['ssl_protocols'])"
    }
}
```

### Tier 2: AI Agent Dynamic Resolution (Smart Path)
```python
async def resolve_control_mapping(control_id: str) -> ControlMapping:
    """Let AI Agent figure out what evidence to check"""
    
    # 1. Query Knowledge Base for control details
    control_context = await vector_search_control_details(control_id)
    
    # 2. AI Agent reasons about evidence needed
    evidence_plan = await ai_agent_analyze(f"""
    Control: {control_id}
    Requirement: {control_context.requirement_text}
    AWS Config Rule: {control_context.aws_config_rule}
    
    Based on this PCI DSS control, determine:
    1. Which AWS service evidence is needed?
    2. What specific resource types to check?
    3. What fields/attributes are relevant?
    4. How to evaluate compliance?
    
    Available evidence services: {get_available_evidence_services()}
    """)
    
    # 3. Return dynamic mapping
    return ControlMapping(
        control_id=control_id,
        evidence_service=evidence_plan.service,
        evidence_type=evidence_plan.resource_type,
        evidence_fields=evidence_plan.fields,
        evaluation_logic=evidence_plan.evaluation,
        confidence_score=evidence_plan.confidence
    )
```

## Example: Control 8.2.1 (User Authentication)

**Knowledge Base Content:**
```
Control 8.2.1: Multi-factor authentication (MFA) is implemented for all non-console 
access into the CDE. AWS Config Rule: iam-mfa-enabled-for-iam-console-access
Guidance: NON_COMPLIANT if any IAM user has console access without MFA enabled.
```

**AI Agent Dynamic Resolution:**
```python
# AI Agent reasoning process:
agent_analysis = {
    "control_understanding": "Need to check IAM users for MFA on console access",
    "aws_service": "iam",
    "evidence_needed": ["iam_users", "mfa_devices", "login_profiles"],
    "evaluation_logic": "Check each IAM user with console access has MFA device attached",
    "evidence_queries": [
        {
            "service": "iam",
            "resource_type": "users",
            "fields": ["username", "mfa_devices", "console_access_enabled"]
        }
    ],
    "compliance_check": "all(user.mfa_devices for user in evidence if user.console_access_enabled)"
}
```

## Benefits of AI Agent Mapping

### 1. Handles Complex Requirements
```python
# Complex control with multiple AWS services
control_context = """
Control 11.4: Implement network segmentation between CDE and other networks.
Multiple AWS services involved: VPC, Security Groups, NACLs, Transit Gateway
"""

# AI Agent can reason about multi-service evidence collection
ai_resolution = {
    "evidence_services": ["ec2", "vpc", "transitgateway"],
    "resource_types": ["security_groups", "network_acls", "route_tables", "subnets"],
    "evaluation": "Check isolation between CDE and non-CDE subnets"
}
```

### 2. Adapts to Ambiguous Guidance
```python
# When PDF guidance is unclear
unclear_guidance = """
Control X.Y.Z: Ensure proper encryption in transit.
AWS Config Rule: [Multiple rules mentioned]
"""

# AI Agent can interpret and prioritize
ai_interpretation = {
    "primary_checks": ["elb-tls-https-listeners-only", "cloudfront-https-required"],
    "secondary_checks": ["s3-bucket-ssl-requests-only"],
    "reasoning": "Focus on public-facing services first for encryption in transit"
}
```

### 3. Cross-Control Reasoning
```python
async def evaluate_with_context(control_id: str) -> ComplianceResult:
    """AI Agent considers related controls"""
    
    # Get related controls
    related = await find_related_controls(control_id)
    
    # Reason about combined evidence
    evidence_plan = await ai_agent_analyze(f"""
    Primary Control: {control_id}
    Related Controls: {related}
    
    Consider evidence overlap and dependencies.
    Optimize evidence collection across related controls.
    """)
    
    return evidence_plan
```

## Implementation Architecture

```python
class IntelligentComplianceAgent:
    def __init__(self):
        self.exact_mappings = load_exact_mappings()
        self.knowledge_base = VectorKnowledgeBase()
        self.evidence_db = EvidenceDatabase()
        
    async def evaluate_control(self, control_id: str, account_id: str) -> ComplianceResult:
        # Try exact mapping first (fast path)
        if control_id in self.exact_mappings:
            mapping = self.exact_mappings[control_id]
        else:
            # AI Agent dynamic resolution (smart path)
            mapping = await self.resolve_mapping_with_ai(control_id)
            
        # Query evidence using resolved mapping
        evidence = await self.evidence_db.query(
            account_id=account_id,
            service=mapping.evidence_service,
            resource_type=mapping.evidence_type
        )
        
        # Apply evaluation logic
        result = self.evaluate_compliance(mapping, evidence)
        
        return result
        
    async def resolve_mapping_with_ai(self, control_id: str) -> ControlMapping:
        """AI Agent figures out evidence requirements"""
        
        # Get control context from Knowledge Base
        context = await self.knowledge_base.get_control_details(control_id)
        
        # AI reasoning prompt
        prompt = f"""
        Analyze this PCI DSS control and determine evidence collection strategy:
        
        Control ID: {control_id}
        Control Text: {context.requirement_text}
        AWS Config Rule: {context.aws_config_rule}
        Technical Guidance: {context.technical_details}
        
        Available AWS services in evidence database:
        {self.evidence_db.get_available_services()}
        
        Determine:
        1. Primary AWS service to check
        2. Resource type (e.g., 'instances', 'security_groups')  
        3. Specific fields to examine
        4. Evaluation logic (Python expression)
        5. Confidence level (0-1)
        
        Format as JSON with clear reasoning.
        """
        
        ai_response = await self.ai_model.analyze(prompt)
        
        return ControlMapping.from_ai_response(ai_response)
```

## Hybrid Strategy: Best of Both Worlds

```python
# Combine exact mappings with AI reasoning
class HybridMappingStrategy:
    async def get_control_mapping(self, control_id: str) -> ControlMapping:
        # 1. Check exact mappings first
        if control_id in self.exact_mappings:
            return self.exact_mappings[control_id]
            
        # 2. AI Agent dynamic resolution
        ai_mapping = await self.ai_resolve_mapping(control_id)
        
        # 3. Validate and cache successful AI mappings
        if ai_mapping.confidence_score > 0.8:
            self.cache_mapping(control_id, ai_mapping)
            
        return ai_mapping
```

## Advantages

1. **Flexibility**: Handles complex, multi-service controls
2. **Adaptability**: Can interpret ambiguous or incomplete guidance  
3. **Coverage**: Works even when exact mappings aren't pre-extracted
4. **Intelligence**: Considers control relationships and context
5. **Learning**: Improves over time as it sees more controls

## Potential Concerns

1. **Consistency**: Same control might be interpreted differently over time
2. **Auditability**: Harder to trace AI reasoning for compliance validation
3. **Performance**: AI analysis adds latency vs direct lookup

## Mitigation Strategy

1. **Cache successful AI mappings** as exact mappings for future use
2. **Human validation** for critical controls before production use
3. **Confidence scoring** to identify when human review is needed
4. **Audit logging** of AI reasoning process for compliance traceability

This approach gives us the **precision of exact mappings** where possible, with the **intelligence of AI reasoning** for complex cases! 