# Hybrid Compliance Knowledge Base Strategy

## The Accuracy Problem with Pure Vector Search

For compliance auditing, **precision is critical**. Vector search introduces uncertainty that could lead to:
- False positive/negative compliance results
- Missed technical criteria details
- Non-defensible audit findings
- Regulatory compliance failures

## Hybrid Architecture: Exact + Context

### Primary Layer: Structured Exact Mappings
```python
# PostgreSQL schema for exact mappings
class ControlMapping(BaseModel):
    control_id: str              # "1.2.5"
    control_title: str           # "Ensure CloudFront distributions..."
    aws_config_rule: str         # "cloudfront-no-deprecated-ssl-protocols"
    compliance_criteria: str     # "NON_COMPLIANT if any 'OriginSslProtocols' includes 'SSLv3'"
    evidence_service: str        # "cloudfront" (maps to Evidence DB service field)
    evidence_type: str           # "distributions" (maps to Evidence DB resource_type field)
    evidence_fields: List[str]   # ["ssl_protocols", "origins"] (what fields to extract from evidence_data)
    evaluation_logic: str        # "any(protocol == 'SSLv3' for origin in evidence for protocol in origin.ssl_protocols)"
    remediation_guidance: str    # "Configure minimum TLS 1.2 on CloudFront origins"
```

### Secondary Layer: Vector Search for Context
```python
# Vector embeddings for supplementary guidance
class ControlContext(BaseModel):
    control_id: str
    guidance_text: str          # Full PDF section text
    related_controls: List[str] # Cross-references
    implementation_notes: str   # Additional context
    # Embedded as vectors for similarity search
```

## Implementation Strategy

### 1. Extract Exact Mappings First
```python
# From AWSOperationalBestPracticesPCIDSS4.pdf
control_mappings = {
    "1.2.5": {
        "config_rule": "cloudfront-no-deprecated-ssl-protocols",
        "criteria": "NON_COMPLIANT if any 'OriginSslProtocols' includes 'SSLv3'",
        "evidence_mapping": {
            "service": "cloudfront",
            "resource_type": "distributions", 
            "fields": ["ssl_protocols", "origins"],
            "evaluation": "any(protocol == 'SSLv3' for dist in evidence for origin in dist['origins'] for protocol in origin['ssl_protocols'])"
        }
    }
}
```

### 2. Evidence Collection (Scheduled, Pre-fetch)
```python
# Evidence Collector (runs scheduled, not real-time)
class EvidenceCollector:
    async def collect_cloudfront_evidence(self, account_id: str):
        """Pre-fetch CloudFront evidence via boto3"""
        cloudfront = boto3.client('cloudfront')
        
        # Get all distributions
        distributions = cloudfront.list_distributions()
        
        evidence_items = []
        for dist in distributions['DistributionList']['Items']:
            dist_config = cloudfront.get_distribution_config(Id=dist['Id'])
            
            # Extract SSL protocols for each origin
            ssl_evidence = {
                "distribution_id": dist['Id'],
                "domain_name": dist['DomainName'],
                "origins": []
            }
            
            for origin in dist_config['DistributionConfig']['Origins']['Items']:
                if 'CustomOriginConfig' in origin:
                    ssl_protocols = origin['CustomOriginConfig'].get('OriginSslProtocols', {}).get('Items', [])
                    ssl_evidence["origins"].append({
                        "origin_id": origin['Id'],
                        "domain_name": origin['DomainName'],
                        "ssl_protocols": ssl_protocols
                    })
            
            evidence_items.append(ssl_evidence)
        
        # Store in Evidence Database
        await store_evidence(
            account_id=account_id,
            service="cloudfront",
            resource_type="distributions",
            evidence=evidence_items,
            collected_at=datetime.utcnow()
        )

# Evidence Database Schema
class EvidenceItem(BaseModel):
    account_id: str
    service: str                 # "cloudfront"
    resource_type: str          # "distributions"
    resource_id: str            # "E12345"
    evidence_data: Dict         # JSONB field with actual evidence
    collected_at: datetime
    expires_at: datetime
```

### 3. AI Agent Compliance Evaluation (Real-time, Database Query)
```python
# AI Agent Process (queries pre-collected evidence)
async def check_compliance(control_id: str, account_id: str) -> ComplianceResult:
    # 1. EXACT lookup (guaranteed accuracy)
    mapping = get_exact_control_mapping(control_id)
    
    # 2. Query pre-collected evidence from database (NO boto3 calls)
    evidence = await query_evidence_database(
        account_id=account_id,
        service=mapping.evidence_service,        # "cloudfront"
        resource_type=mapping.evidence_type,     # "distributions"
        fields_needed=mapping.evidence_fields    # ["ssl_protocols", "origins"]
    )
    
    # 3. Apply exact evaluation logic to database evidence
    is_compliant = evaluate_compliance_criteria(mapping.evaluation_logic, evidence)
    
    # 4. Optional: Vector search for remediation guidance
    remediation = None
    if not is_compliant:
        remediation = vector_search_remediation(control_id)
    
    return ComplianceResult(
        control_id=control_id,
        account_id=account_id,
        status="COMPLIANT" if is_compliant else "NON_COMPLIANT",
        evidence_summary=evidence,
        criteria_applied=mapping.compliance_criteria,
        remediation_guidance=remediation
    )

# Example evidence query function
async def query_evidence_database(account_id: str, service: str, resource_type: str, fields_needed: List[str]):
    """Query pre-collected evidence from PostgreSQL"""
    query = """
    SELECT evidence_data 
    FROM evidence_items 
    WHERE account_id = %s 
      AND service = %s 
      AND resource_type = %s
      AND collected_at > NOW() - INTERVAL '24 hours'
    """
    
    evidence_rows = await db.fetch_all(query, account_id, service, resource_type)
    return [row['evidence_data'] for row in evidence_rows]
```

## Benefits of Hybrid Approach

### Exact Mapping Benefits:
- **100% precision** for known control mappings
- **Deterministic results** - same input always gives same output
- **Audit defensible** - can trace back to exact PDF guidance
- **Fast lookups** - O(1) database queries vs vector similarity calculations

### Vector Search Benefits:
- **Additional context** for complex controls
- **Remediation guidance** from broader knowledge base
- **Cross-control relationships** discovery
- **Natural language queries** for exploratory analysis

## Example: Control 1.2.5 Evaluation

```python
# EXACT MAPPING (Primary)
control_1_2_5 = {
    "criteria": "NON_COMPLIANT if any 'OriginSslProtocols' includes 'SSLv3'",
    "evidence_service": "cloudfront",
    "evidence_type": "distributions",
    "evaluation": "any(protocol == 'SSLv3' for dist in evidence for origin in dist['origins'] for protocol in origin['ssl_protocols'])"
}

# PRE-COLLECTED EVIDENCE (from Evidence Database)
evidence_from_db = [
    {
        "distribution_id": "E12345",
        "domain_name": "example.cloudfront.net",
        "origins": [
            {
                "origin_id": "origin1",
                "domain_name": "backend.example.com",
                "ssl_protocols": ["SSLv3", "TLSv1.2"]  # ❌ Contains SSLv3
            }
        ]
    },
    {
        "distribution_id": "E67890", 
        "domain_name": "secure.cloudfront.net",
        "origins": [
            {
                "origin_id": "origin1",
                "domain_name": "api.example.com", 
                "ssl_protocols": ["TLSv1.2", "TLSv1.3"]  # ✅ No SSLv3
            }
        ]
    }
]

# EVALUATION RESULT
is_compliant = not any(protocol == 'SSLv3' 
                      for dist in evidence_from_db 
                      for origin in dist['origins'] 
                      for protocol in origin['ssl_protocols'])
# Result: False (non-compliant due to E12345 using SSLv3)

# VECTOR SEARCH (Secondary Context)
vector_context = """
CloudFront SSL/TLS Best Practices:
- Use TLS 1.2 or higher
- Disable SSLv3 due to POODLE vulnerability
- Configure minimum protocol version
- Regularly audit SSL configurations
"""

# FINAL RESULT
result = ComplianceResult(
    control_id="1.2.5",
    account_id="123456789",
    status="NON_COMPLIANT",
    evidence_summary={"distributions_with_sslv3": ["E12345"]},
    criteria_applied="NON_COMPLIANT if any 'OriginSslProtocols' includes 'SSLv3'",
    remediation_guidance=vector_context
)
```

## Implementation Priority

1. **Phase 1**: Build exact mapping extractor from AWS Config Rules PDF
2. **Phase 2**: Create PostgreSQL schemas for control mappings and evidence storage
3. **Phase 3**: Build Evidence Collector with scheduled boto3 data collection
4. **Phase 4**: Implement AI Agent with exact evaluation logic (queries evidence DB)
5. **Phase 5**: Add vector search layer for additional context and remediation guidance
6. **Phase 6**: Build hybrid compliance evaluation interface

## Architecture Flow

```
PDF → Config Rule Mappings (Phase 1) → Knowledge Base (Phase 2)
                                           ↓
AWS APIs → Evidence Collector (Phase 3) → Evidence Database (Phase 2)
                                           ↓
User Request → AI Agent (Phase 4) → Query Evidence DB → Apply Exact Criteria → Result
                ↓
          Vector Search (Phase 5) → Enhanced Remediation Guidance
```

This ensures **accuracy first, enhancement second** - exactly what compliance auditing requires. 