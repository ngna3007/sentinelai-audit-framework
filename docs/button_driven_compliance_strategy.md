# Button-Driven Compliance Strategy - UI → AI Agent → Evidence Database

## 🎯 **Actual User Workflow**

```
UI Dashboard:
┌─────────────────────────────────┐
│ Control 1.2.5                   │
│ Network Security Controls       │
│ [Check Compliant]  ←── User clicks this
└─────────────────────────────────┘

AI Agent Process:
1. Lookup Control 1.2.5 in Knowledge Base
2. Find: "Check CloudFront distributions for SSLv3 in OriginSslProtocols"  
3. Query Evidence Database for CloudFront SSL evidence
4. Evaluate: Found SSLv3 → NON_COMPLIANT
5. Return to UI: "❌ NON_COMPLIANT: 3 distributions using deprecated SSLv3"
```

## 🏗️ **Three-Component Architecture**

### **Component 1: Knowledge Base (KB) - Guidance Intelligence**
Maps Control ID → What to check for

```json
{
  "control_mappings": {
    "1.2.5": {
      "description": "Network security controls are configured and maintained",
      "aws_config_rule": "cloudfront-no-deprecated-ssl-protocols",
      "check_logic": {
        "service": "cloudfront",
        "resource_type": "distributions", 
        "evidence_field": "ssl_protocols",
        "evaluation": {
          "type": "not_contains",
          "fail_values": ["SSLv3"],
          "pass_message": "All distributions use secure SSL protocols",
          "fail_message": "Distributions found using deprecated SSLv3"
        }
      }
    }
  }
}
```

### **Component 2: Evidence Database - Structured Evidence Storage**
Pre-collected evidence from AWS accounts

```sql
-- Evidence table structure
CREATE TABLE evidence (
    id SERIAL PRIMARY KEY,
    account_id VARCHAR(12),
    service VARCHAR(50),
    resource_type VARCHAR(50),
    resource_id VARCHAR(255),
    evidence_data JSONB,
    collection_timestamp TIMESTAMP,
    related_controls TEXT[],
    INDEX (account_id, service, resource_type),
    INDEX (related_controls USING GIN)
);

-- Example evidence record
{
  "account_id": "123456789",
  "service": "cloudfront", 
  "resource_type": "distributions",
  "resource_id": "distribution-xyz",
  "evidence_data": {
    "ssl_protocols": {
      "origins": [
        {
          "origin_id": "origin1",
          "ssl_protocols": ["TLSv1.2", "SSLv3"]  ← This triggers NON_COMPLIANT
        }
      ]
    }
  },
  "collection_timestamp": "2024-01-15T10:30:00Z",
  "related_controls": ["1.2.5", "1.2.8"]
}
```

### **Component 3: AI Agent - Intelligent Bridge**
Connects KB guidance with Evidence Database

```python
class ComplianceAgent:
    def check_control_compliance(self, control_id: str, account_id: str = None) -> ComplianceResult:
        """
        Handle the "Check Compliant" button click for a specific control.
        """
        
        # 1. Lookup control in Knowledge Base
        control_info = self.knowledge_base.get_control(control_id)
        if not control_info:
            return ComplianceResult(status="UNKNOWN", message="Control not found in KB")
        
        # 2. Extract what to check for
        check_logic = control_info["check_logic"]
        service = check_logic["service"]
        resource_type = check_logic["resource_type"]
        evidence_field = check_logic["evidence_field"]
        evaluation = check_logic["evaluation"]
        
        # 3. Query Evidence Database
        evidence_records = self.evidence_db.query(
            service=service,
            resource_type=resource_type,
            account_id=account_id,
            related_controls=control_id
        )
        
        # 4. Apply compliance evaluation
        compliance_results = []
        for record in evidence_records:
            result = self.evaluate_evidence(record, evaluation)
            compliance_results.append(result)
        
        # 5. Determine overall status
        overall_status = self.determine_overall_status(compliance_results)
        
        return ComplianceResult(
            control_id=control_id,
            status=overall_status,
            details=compliance_results,
            summary=self.generate_summary(compliance_results, evaluation)
        )
```

## 🔄 **Complete Workflow**

### **1. UI Button Click Handler**
```javascript
// Frontend button handler
async function checkCompliance(controlId) {
    showLoading(controlId);
    
    try {
        const response = await fetch('/api/check-compliance', {
            method: 'POST',
            body: JSON.stringify({ 
                control_id: controlId,
                account_id: selectedAccount 
            })
        });
        
        const result = await response.json();
        displayComplianceResult(controlId, result);
        
    } catch (error) {
        displayError(controlId, error);
    }
}
```

### **2. Backend API Endpoint**
```python
@app.post("/api/check-compliance")
async def check_compliance(request: ComplianceCheckRequest):
    """API endpoint for "Check Compliant" button clicks."""
    
    agent = ComplianceAgent(
        knowledge_base=load_knowledge_base(),
        evidence_db=get_evidence_database()
    )
    
    result = agent.check_control_compliance(
        control_id=request.control_id,
        account_id=request.account_id
    )
    
    return ComplianceResponse(
        control_id=request.control_id,
        status=result.status,
        message=result.summary,
        details=result.details,
        timestamp=datetime.utcnow()
    )
```

### **3. AI Agent Intelligence**
```python
def evaluate_evidence(self, evidence_record: dict, evaluation: dict) -> EvaluationResult:
    """Apply evaluation logic to evidence data."""
    
    evaluation_type = evaluation["type"]
    evidence_data = evidence_record["evidence_data"]
    
    if evaluation_type == "not_contains":
        # Extract the relevant field from evidence
        field_path = evaluation.get("evidence_field", "")
        field_value = self.extract_field_value(evidence_data, field_path)
        
        # Check if any fail values are present
        fail_values = evaluation["fail_values"]
        has_fail_value = any(fail_val in str(field_value) for fail_val in fail_values)
        
        if has_fail_value:
            return EvaluationResult(
                resource_id=evidence_record["resource_id"],
                status="NON_COMPLIANT",
                details=f"Found prohibited values: {fail_values} in {field_value}",
                evidence=field_value
            )
        else:
            return EvaluationResult(
                resource_id=evidence_record["resource_id"],
                status="COMPLIANT", 
                details=evaluation["pass_message"],
                evidence=field_value
            )
```

## 📊 **Evidence Database Schema Design**

### **Core Evidence Table**
```sql
CREATE TABLE compliance_evidence (
    -- Primary identification
    id SERIAL PRIMARY KEY,
    account_id VARCHAR(12) NOT NULL,
    region VARCHAR(20),
    
    -- AWS resource identification  
    service VARCHAR(50) NOT NULL,
    resource_type VARCHAR(50) NOT NULL,
    resource_id VARCHAR(255) NOT NULL,
    resource_arn TEXT,
    
    -- Evidence data
    evidence_data JSONB NOT NULL,
    evidence_hash VARCHAR(64), -- For change detection
    
    -- Compliance mapping
    related_controls TEXT[] NOT NULL,
    config_rules TEXT[],
    
    -- Collection metadata
    collection_timestamp TIMESTAMP NOT NULL,
    collection_method VARCHAR(50),
    
    -- Indexes for fast queries
    UNIQUE(account_id, service, resource_type, resource_id),
    INDEX idx_controls (related_controls USING GIN),
    INDEX idx_service_resource (service, resource_type),
    INDEX idx_collection_time (collection_timestamp)
);
```

### **Evidence Query Examples**
```sql
-- Query for Control 1.2.5 (CloudFront SSL protocols)
SELECT * FROM compliance_evidence 
WHERE '1.2.5' = ANY(related_controls)
  AND service = 'cloudfront'
  AND resource_type = 'distributions'
  AND account_id = '123456789';

-- Query for all evidence for an account
SELECT service, resource_type, COUNT(*) as resource_count
FROM compliance_evidence 
WHERE account_id = '123456789'
GROUP BY service, resource_type;
```

## 🎯 **Knowledge Base Structure**

### **Control Mapping Format**
```yaml
controls:
  "1.2.5":
    description: "Network security controls are configured and maintained"
    aws_config_rule: "cloudfront-no-deprecated-ssl-protocols"
    
    check_logic:
      service: "cloudfront"
      resource_type: "distributions"
      evidence_field: "ssl_protocols.origins[*].ssl_protocols"
      
      evaluation:
        type: "not_contains"
        fail_values: ["SSLv3"]
        pass_message: "All CloudFront distributions use secure SSL protocols"
        fail_message: "Found distributions using deprecated SSLv3 protocol"
        
    remediation:
      description: "Update CloudFront distributions to use TLS 1.2 or higher"
      aws_docs: "https://docs.aws.amazon.com/cloudfront/latest/DeveloperGuide/..."

  "1.2.8":
    description: "Network security controls associated with WAF"  
    aws_config_rule: "cloudfront-associated-with-waf"
    
    check_logic:
      service: "cloudfront"
      resource_type: "distributions"
      evidence_field: "web_acl_id"
      
      evaluation:
        type: "exists"
        pass_message: "All distributions are associated with WAF"
        fail_message: "Found distributions not associated with WAF"
```

## 🚀 **Implementation Priority**

### **Phase 1: Core Infrastructure**
1. Design evidence database schema
2. Create Knowledge Base structure
3. Build basic AI Agent framework

### **Phase 2: Evidence Collection**
1. CloudFront evidence collection (SSL protocols, WAF)
2. EC2 evidence collection (security groups)
3. IAM evidence collection (password policies)

### **Phase 3: UI Integration**
1. API endpoints for compliance checks
2. Frontend button handlers
3. Results display components

### **Phase 4: Intelligence Enhancement**
1. Advanced evaluation logic
2. Compliance trend analysis
3. Automated remediation suggestions

This architecture gives you a **clean, button-driven compliance system** where the AI agent intelligently bridges your Knowledge Base with the Evidence Database! 🎯 