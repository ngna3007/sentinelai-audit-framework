# Evidence Collection Strategy - From Guidance to Practical Implementation

## 🎯 **The Core Challenge**

Transform this guidance: 
```
Control: 1.2.5
AWS Config Rule: cloudfront-no-deprecated-ssl-protocols  
Guidance: NON_COMPLIANT if any 'OriginSslProtocols' includes 'SSLv3'
```

Into this practical system:
```
User Query: "Check Control 1.2.5"
AI Agent: 
  1. Lookup → s3://evidence-bucket/account123/cloudfront/distributions/evidence.json
  2. Evaluate → Found SSLv3 in distribution xyz
  3. Result → "NON_COMPLIANT: Distribution xyz uses deprecated SSLv3"
```

## 🏗️ **Two-Phase Architecture**

### **Phase 1: Evidence Collection (Scheduled/Periodic)**
- Run daily/weekly to collect fresh evidence
- Store in S3 with structured organization
- No real-time boto3 calls during audits

### **Phase 2: Audit Queries (Real-time)**
- AI agent retrieves pre-collected evidence from S3
- Fast compliance evaluation
- No AWS API costs during audit queries

## 📋 **Strategic Mapping Plan**

### **Step 1: Guidance → Implementation Mapping**

Create a systematic way to transform guidance into actionable boto3 calls:

```yaml
control_mappings:
  "1.2.5":
    pci_description: "Network security controls are configured and maintained"
    aws_config_rule: "cloudfront-no-deprecated-ssl-protocols"
    guidance: "NON_COMPLIANT if any 'OriginSslProtocols' includes 'SSLv3'"
    
    # YOUR EXPERTISE: Convert guidance to practical implementation
    implementation:
      service: "cloudfront" 
      discovery_method: "list_distributions"
      evidence_collection:
        method: "get_distribution_config"
        parameters: ["Id"]
        extract_paths:
          - "DistributionConfig.Origins.Items[*].CustomOriginConfig.OriginSslProtocols"
      
    # Evidence storage strategy
    evidence_storage:
      s3_prefix: "cloudfront/distributions"
      file_format: "json"
      evidence_key: "ssl_protocols"
      
    # Compliance evaluation logic  
    evaluation:
      type: "contains_check"
      fail_conditions: ["SSLv3"]
      pass_conditions: ["TLSv1.2", "TLSv1.1"]
```

### **Step 2: Evidence Collection Strategy**

#### **A. S3 Evidence Organization**
```
s3://compliance-evidence-bucket/
├── account-123456789/
│   ├── cloudfront/
│   │   ├── distributions/
│   │   │   ├── evidence-2024-01-15.json
│   │   │   └── metadata.json
│   │   └── web-acls/
│   ├── ec2/
│   │   ├── security-groups/
│   │   └── network-interfaces/
│   ├── iam/
│   │   ├── password-policy/
│   │   └── users/
│   └── collection-metadata.json
├── account-987654321/
└── evidence-index.json  # Master index for AI agent
```

#### **B. Evidence File Structure**
```json
{
  "collection_timestamp": "2024-01-15T10:30:00Z",
  "account_id": "123456789",
  "service": "cloudfront",
  "resource_type": "distributions",
  "evidence": [
    {
      "resource_id": "distribution-xyz",
      "resource_arn": "arn:aws:cloudfront::123456789:distribution/xyz",
      "ssl_protocols": {
        "origins": [
          {
            "origin_id": "origin1",
            "ssl_protocols": ["TLSv1.2", "TLSv1.1"]
          }
        ]
      },
      "evidence_hash": "sha256:abc123...",
      "related_controls": ["1.2.5", "1.2.8"]
    }
  ]
}
```

#### **C. Evidence Index for AI Agent**
```json
{
  "index_version": "1.0",
  "last_updated": "2024-01-15T10:30:00Z",
  "control_mappings": {
    "1.2.5": {
      "description": "CloudFront SSL protocols check",
      "evidence_locations": [
        "s3://bucket/account-123/cloudfront/distributions/evidence-2024-01-15.json",
        "s3://bucket/account-456/cloudfront/distributions/evidence-2024-01-15.json"
      ],
      "evaluation_logic": "check_ssl_protocols_for_sslv3",
      "last_collected": "2024-01-15T10:30:00Z"
    }
  }
}
```

### **Step 3: AI Agent Retrieval Strategy**

#### **A. Query Processing Flow**
```
User: "Check Control 1.2.5 for account 123456789"

AI Agent:
1. Load evidence index from S3
2. Find control 1.2.5 → get evidence file locations
3. Retrieve evidence files for account 123456789
4. Apply evaluation logic
5. Return compliance status with details
```

#### **B. Evidence Evaluation Logic**
```python
# Stored evaluation logic for each control
evaluation_functions = {
    "1.2.5": {
        "function": "evaluate_ssl_protocols",
        "parameters": {
            "fail_if_contains": ["SSLv3"],
            "evidence_path": "ssl_protocols.origins[*].ssl_protocols"
        }
    }
}
```

## 🔄 **Implementation Workflow**

### **Guidance Analysis Process**
```
1. Parse AWS Config Rules PDF
   ↓
2. Extract: Control ID → Config Rule → Guidance Text
   ↓  
3. Human/AI Analysis: Convert guidance to boto3 implementation
   ↓
4. Create implementation mapping YAML/JSON
   ↓
5. Generate evidence collection scripts
   ↓
6. Test and validate evidence collection
   ↓
7. Deploy to production evidence collection system
```

### **Evidence Collection Process** 
```
1. Scheduled job runs (daily/weekly)
   ↓
2. For each account:
   a. Load implementation mappings
   b. Execute boto3 calls
   c. Extract relevant evidence
   d. Store in structured S3 format
   ↓
3. Update evidence index
   ↓
4. Generate collection summary report
```

### **Audit Query Process**
```
1. User/AI asks: "Check Control X.Y.Z"
   ↓
2. AI Agent:
   a. Load evidence index
   b. Find evidence file locations
   c. Retrieve and parse evidence
   d. Apply evaluation logic
   e. Return compliance status
```

## 🧠 **Guidance → Implementation Examples**

### **Example 1: CloudFront SSL Protocols**
```yaml
# From guidance text
guidance: "NON_COMPLIANT if any 'OriginSslProtocols' includes 'SSLv3'"

# To implementation
implementation:
  boto3_calls:
    - method: "cloudfront.list_distributions()"
      extract: "DistributionList.Items[*].Id"
    - method: "cloudfront.get_distribution_config(Id={distribution_id})"
      extract: "DistributionConfig.Origins.Items[*].CustomOriginConfig.OriginSslProtocols"
  
  evidence_storage:
    key: "ssl_protocols"
    format: "list"
    
  evaluation:
    compliance_check: "not_contains"
    fail_values: ["SSLv3"]
```

### **Example 2: EC2 Security Groups**
```yaml
guidance: "NON_COMPLIANT if network interface is not attached to security group"

implementation:
  boto3_calls:
    - method: "ec2.describe_network_interfaces()"
      extract: "NetworkInterfaces[*]"
  
  evidence_storage:
    key: "network_interfaces"
    fields: ["NetworkInterfaceId", "Groups", "Status"]
    
  evaluation:
    compliance_check: "has_security_groups"
    required: "Groups length > 0"
```

### **Example 3: IAM Password Policy**
```yaml
guidance: "NON_COMPLIANT if password policy does not meet requirements"

implementation:
  boto3_calls:
    - method: "iam.get_account_password_policy()"
      extract: "PasswordPolicy"
  
  evidence_storage:
    key: "password_policy"
    format: "object"
    
  evaluation:
    compliance_check: "policy_requirements"
    requirements:
      MinimumPasswordLength: ">= 8"
      RequireUppercaseCharacters: true
      RequireLowercaseCharacters: true
      RequireNumbers: true
```

## 📊 **Evidence Collection Prioritization**

### **Phase 1: Core Services (Start Here)**
1. **CloudFront** - SSL protocols, WAF associations
2. **EC2** - Security groups, network interfaces  
3. **IAM** - Password policies, user permissions
4. **S3** - Bucket policies, encryption
5. **VPC** - Security groups, NACLs

### **Phase 2: Extended Services**
1. **RDS** - Encryption, backup settings
2. **Lambda** - Environment variables, VPC config
3. **API Gateway** - Authentication, logging
4. **ELB** - SSL policies, access logs

### **Phase 3: Advanced Services**  
1. **KMS** - Key policies, rotation
2. **CloudTrail** - Logging configuration
3. **Config** - Configuration recording
4. **GuardDuty** - Threat detection

## 🎯 **Success Metrics**

1. **Evidence Coverage**: % of PCI DSS controls with automated evidence collection
2. **Collection Efficiency**: Evidence collection time vs manual auditing  
3. **Query Speed**: AI agent response time for compliance queries
4. **Cost Optimization**: Reduced boto3 API calls during audits
5. **Accuracy**: Compliance evaluation accuracy vs manual review

## 🚀 **Next Steps**

1. **Analyze AWS Config PDF**: Extract all control mappings
2. **Create Implementation Mappings**: Start with 5-10 core controls
3. **Build Evidence Collection Prototype**: Test with one service (CloudFront)
4. **Design S3 Evidence Schema**: Standardize evidence storage format
5. **Prototype AI Agent Retrieval**: Test evidence lookup and evaluation

This strategy creates a **scalable, cost-effective compliance auditing system** that separates evidence collection from audit queries! 🎯 