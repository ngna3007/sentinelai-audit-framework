# Config Rule Mapping Architecture - Automated Compliance Checking

## 🎯 **Understanding the Real Workflow**

### **The Two Critical Documents**
```
shared_data/documents/
├── PCI-DSS-v4_0_1.pdf                    # 📋 REQUIREMENTS (306 controls)
│   └── "What needs to be compliant"      # ✅ Already processed  
└── AWSOperationalBestPracticesPCIDSS4.pdf # 🗺️ IMPLEMENTATION MAP
    └── "How to check compliance in AWS"   # 🚧 Need to process
```

### **Config Rule Mapping Table Structure**
From your screenshot, the AWS Config PDF contains:

| Column | Purpose | Example |
|--------|---------|---------|
| **Control ID** | PCI DSS requirement | `1.2.8` |
| **Control Description** | What needs to be checked | `Network security controls (NSCs) are configured and maintained` |
| **AWS Config Rule** | Which AWS service/config to check | `cloudfront-associated-with-waf` |
| **Guidance** | Specific validation criteria | `Ensure CloudFront distributions are associated with WAF` |

## 🏗️ **Revised Architecture: Config Rule Mapping System**

### **1. Config Rule Mapping Processor**
```python
# data_pipeline/processors/documents/config_mapping/aws_config_rule_processor.py
class AWSConfigRuleProcessor:
    """
    Extract PCI DSS → AWS Config Rule mappings from the AWS Config PDF.
    This creates the blueprint for evidence collection.
    """
    
    def extract_config_mappings(self, pdf_path: str) -> List[ConfigRuleMapping]:
        """Extract control-to-config-rule mappings."""
        mappings = []
        
        # Extract table data from PDF
        tables = self.extract_tables_from_pdf(pdf_path)
        
        for table in tables:
            for row in table.rows:
                mapping = ConfigRuleMapping(
                    control_id=row['Control ID'],
                    control_description=row['Control Description'],
                    aws_config_rule=row['AWS Config Rule'],
                    guidance=row['Guidance'],
                    compliance_check_type=self.determine_check_type(row['AWS Config Rule'])
                )
                mappings.append(mapping)
        
        return mappings
    
    def create_compliance_blueprint(self, mappings: List[ConfigRuleMapping]) -> ComplianceBlueprint:
        """Create lookup table for evidence collection."""
        blueprint = ComplianceBlueprint()
        
        for mapping in mappings:
            blueprint.add_control_check(
                control_id=mapping.control_id,
                aws_service=self.extract_service_from_rule(mapping.aws_config_rule),
                config_rule=mapping.aws_config_rule,
                validation_criteria=mapping.guidance
            )
        
        return blueprint
```

### **2. Evidence Collector with Config Rule Integration**
```python
# services/evidence_collector/collectors/config_rule_collector.py
class ConfigRuleBasedCollector:
    """
    Collect evidence based on the config rule mappings.
    Uses the compliance blueprint to know exactly what to collect.
    """
    
    def __init__(self, compliance_blueprint: ComplianceBlueprint):
        self.blueprint = compliance_blueprint
        self.aws_clients = {}
    
    def collect_evidence_for_control(self, control_id: str, account_id: str) -> ControlEvidence:
        """Collect evidence for a specific PCI DSS control."""
        # Get the config rules needed for this control
        required_checks = self.blueprint.get_checks_for_control(control_id)
        
        evidence = ControlEvidence(control_id=control_id, account_id=account_id)
        
        for check in required_checks:
            if check.aws_service == 'cloudfront':
                evidence.add_cloudfront_evidence(
                    self.collect_cloudfront_config(account_id, check.config_rule)
                )
            elif check.aws_service == 'ec2':
                evidence.add_ec2_evidence(
                    self.collect_ec2_config(account_id, check.config_rule)
                )
            elif check.aws_service == 'iam':
                evidence.add_iam_evidence(
                    self.collect_iam_config(account_id, check.config_rule)
                )
            # ... etc for other services
        
        return evidence
    
    def collect_cloudfront_config(self, account_id: str, config_rule: str) -> CloudFrontEvidence:
        """Collect CloudFront configurations for compliance checking."""
        client = self.get_aws_client('cloudfront', account_id)
        
        if config_rule == 'cloudfront-associated-with-waf':
            distributions = client.list_distributions()
            evidence = CloudFrontEvidence()
            
            for dist in distributions['DistributionList'].get('Items', []):
                waf_config = client.get_distribution_config(Id=dist['Id'])
                evidence.add_distribution(
                    distribution_id=dist['Id'],
                    has_waf=bool(waf_config.get('WebACLId')),
                    waf_id=waf_config.get('WebACLId')
                )
            
            return evidence
```

### **3. Compliance Evaluator**
```python
# data_pipeline/processors/evidence/compliance_evaluator.py
class ComplianceEvaluator:
    """
    Evaluate collected evidence against PCI DSS requirements using the config rule mappings.
    """
    
    def __init__(self, compliance_blueprint: ComplianceBlueprint):
        self.blueprint = compliance_blueprint
    
    def evaluate_control_compliance(self, control_id: str, evidence: ControlEvidence) -> ComplianceResult:
        """Evaluate if collected evidence meets PCI DSS control requirements."""
        required_checks = self.blueprint.get_checks_for_control(control_id)
        results = []
        
        for check in required_checks:
            if check.config_rule == 'cloudfront-associated-with-waf':
                result = self.evaluate_cloudfront_waf_association(
                    evidence.cloudfront_evidence, 
                    check.validation_criteria
                )
            elif check.config_rule == 'ec2-security-group-attached-to-eni':
                result = self.evaluate_ec2_security_groups(
                    evidence.ec2_evidence,
                    check.validation_criteria
                )
            # ... etc
            
            results.append(result)
        
        return ComplianceResult(
            control_id=control_id,
            overall_status=self.determine_overall_status(results),
            check_results=results,
            evidence_summary=evidence.summary()
        )
    
    def evaluate_cloudfront_waf_association(self, cf_evidence: CloudFrontEvidence, criteria: str) -> CheckResult:
        """Evaluate CloudFront WAF association compliance."""
        total_distributions = len(cf_evidence.distributions)
        distributions_with_waf = sum(1 for d in cf_evidence.distributions if d.has_waf)
        
        is_compliant = distributions_with_waf == total_distributions
        
        return CheckResult(
            config_rule='cloudfront-associated-with-waf',
            status='COMPLIANT' if is_compliant else 'NON_COMPLIANT',
            details=f"{distributions_with_waf}/{total_distributions} distributions have WAF",
            evidence=cf_evidence.to_dict()
        )
```

### **4. Enhanced Evidence Collector Service**
```python
# services/evidence_collector/main.py
class EnhancedEvidenceCollector:
    """
    Main evidence collector that uses config rule mappings for targeted collection.
    """
    
    def __init__(self, compliance_blueprint_path: str):
        # Load the compliance blueprint created from AWS Config PDF
        self.blueprint = ComplianceBlueprint.load(compliance_blueprint_path)
        self.collector = ConfigRuleBasedCollector(self.blueprint)
        self.evaluator = ComplianceEvaluator(self.blueprint)
    
    def run_compliance_audit(self, accounts: List[str]) -> AuditReport:
        """Run complete compliance audit across multiple accounts."""
        audit_report = AuditReport()
        
        for account_id in accounts:
            print(f"🔍 Auditing account: {account_id}")
            account_results = {}
            
            # Get all PCI DSS controls that have AWS config rule mappings
            controls_to_check = self.blueprint.get_all_controls()
            
            for control_id in controls_to_check:
                print(f"   Checking control {control_id}...")
                
                # 1. Collect evidence for this control
                evidence = self.collector.collect_evidence_for_control(control_id, account_id)
                
                # 2. Evaluate compliance
                result = self.evaluator.evaluate_control_compliance(control_id, evidence)
                
                account_results[control_id] = result
            
            audit_report.add_account_results(account_id, account_results)
        
        return audit_report
    
    def store_audit_results(self, audit_report: AuditReport):
        """Store audit results in PostgreSQL and S3."""
        # 1. Store structured results in PostgreSQL
        db_formatter = DatabaseFormatter()
        db_data = db_formatter.format_audit_results(audit_report)
        DatabaseIngestion().store_audit_results(db_data)
        
        # 2. Archive raw evidence in S3
        s3_formatter = StorageFormatter()
        s3_package = s3_formatter.package_audit_evidence(audit_report)
        S3Storage().upload_audit_package(s3_package)
        
        # 3. Create Bedrock KB content for AI querying
        kb_formatter = BedrockFormatter()
        kb_content = kb_formatter.format_compliance_guidance(audit_report, self.blueprint)
        BedrockKnowledgeBase().update_compliance_content(kb_content)
```

## 🔄 **Complete Workflow**

### **Step 1: Extract Config Rule Mappings (One-time)**
```bash
# Process the AWS Config Rules PDF to create compliance blueprint
python -m data_pipeline.cli extract-config-mappings \
    --pdf shared_data/documents/AWSOperationalBestPracticesPCIDSS4.pdf \
    --output shared_data/blueprints/aws_pci_dss_mappings.json
```

### **Step 2: Run Evidence Collection**
```bash
# Collect evidence from multiple AWS accounts using the blueprint
python -m services.evidence_collector.main audit \
    --blueprint shared_data/blueprints/aws_pci_dss_mappings.json \
    --accounts account1,account2,account3 \
    --output-db postgres://aurora.aws.com/compliance \
    --output-s3 s3://compliance-evidence/audit-2024-01/
```

### **Step 3: Generate Compliance Report**
```bash
# Generate comprehensive compliance report
python -m data_pipeline.cli generate-compliance-report \
    --audit-date 2024-01-15 \
    --format dashboard \
    --output shared_data/reports/pci_dss_compliance_2024_01.html
```

## 🎯 **Data Schema Examples**

### **Config Rule Mapping Schema**
```python
@dataclass
class ConfigRuleMapping:
    control_id: str                    # "1.2.8"
    control_description: str           # "Network security controls..."
    aws_config_rule: str              # "cloudfront-associated-with-waf"
    guidance: str                     # "Ensure CloudFront distributions..."
    aws_service: str                  # "cloudfront"
    compliance_check_type: str        # "association_check"
    required_parameters: Dict[str, Any] # Rule-specific parameters
```

### **Evidence Schema**
```python
@dataclass  
class ControlEvidence:
    control_id: str
    account_id: str
    collection_timestamp: datetime
    cloudfront_evidence: Optional[CloudFrontEvidence] = None
    ec2_evidence: Optional[EC2Evidence] = None
    iam_evidence: Optional[IAMEvidence] = None
    # ... other service evidence
```

### **Compliance Result Schema**
```python
@dataclass
class ComplianceResult:
    control_id: str
    account_id: str
    overall_status: Literal['COMPLIANT', 'NON_COMPLIANT', 'INSUFFICIENT_DATA']
    check_results: List[CheckResult]
    evidence_summary: Dict[str, Any]
    recommendations: List[str]
    evaluation_timestamp: datetime
```

## 🚀 **Implementation Priority**

### **Week 1: Config Rule Mapping Processor**
1. Build table extraction from AWS Config PDF
2. Create ConfigRuleMapping schema
3. Generate compliance blueprint JSON

### **Week 2: Evidence Collector Enhancement**
1. Add config-rule-based collection logic
2. Implement service-specific collectors (CloudFront, EC2, IAM)
3. Add cross-account role assumption

### **Week 3: Compliance Evaluator**
1. Build rule evaluation engine
2. Implement service-specific compliance checks
3. Generate compliance results

### **Week 4: Integration & Reporting**
1. Integrate with PostgreSQL storage
2. Create S3 evidence archival
3. Build compliance dashboard

This architecture turns your evidence collector into an **intelligent compliance auditor** that knows exactly what to check and how to evaluate it! 🎯 