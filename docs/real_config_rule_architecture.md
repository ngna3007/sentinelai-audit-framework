# Real Config Rule Architecture - Intelligent Compliance Auditing

## 🎯 **The Real Challenge**

The AWS Config Rules PDF is **guidance only** - it tells you what to check but not how to collect the evidence. You need a sophisticated system that bridges this gap.

### **What the PDF Provides (Limited)**
```
Control: 1.2.5
AWS Config Rule: cloudfront-no-deprecated-ssl-protocols
Guidance: NON_COMPLIANT if any 'OriginSslProtocols' includes 'SSLv3'
```

### **What You Need to Build (Implementation)**
```python
# 1. Which boto3 method to call
client = boto3.client('cloudfront')
response = client.get_distribution_config(Id='distribution_id')

# 2. Which response fields to extract and store
evidence = response['DistributionConfig']['Origins']['Items'][0]['CustomOriginConfig']['OriginSslProtocols']

# 3. How to evaluate compliance
is_compliant = 'SSLv3' not in evidence['Items']
```

## 🏗️ **Four-Layer Architecture**

### **Layer 1: Config Rule Mapping Processor**
```python
# data_pipeline/processors/config_mappings/aws_config_rule_processor.py
class AWSConfigRuleProcessor:
    """Extract mappings from AWS Config Rules PDF."""
    
    def extract_config_mappings(self, pdf_path: str) -> List[ConfigRuleMapping]:
        """Extract Control ID → Config Rule → Compliance Criteria mappings."""
        mappings = []
        
        tables = self.extract_tables_from_pdf(pdf_path)
        for table in tables:
            for row in table.rows:
                mapping = ConfigRuleMapping(
                    control_id=row['Control ID'],  # "1.2.5"
                    aws_config_rule=row['AWS Config Rule'],  # "cloudfront-no-deprecated-ssl-protocols"
                    compliance_criteria=row['Guidance'],  # "NON_COMPLIANT if..."
                    pci_description=row['Control Description']
                )
                mappings.append(mapping)
        
        return mappings
```

### **Layer 2: SDK Implementation Knowledge Base**
```python
# data_pipeline/processors/config_mappings/sdk_knowledge_base.py
class SDKImplementationKnowledgeBase:
    """
    Maps AWS Config Rules to actual boto3 implementation details.
    This is YOUR domain expertise codified into the system.
    """
    
    def __init__(self):
        self.implementations = {
            "cloudfront-no-deprecated-ssl-protocols": SDKImplementation(
                service="cloudfront",
                client_method="get_distribution_config",
                client_params={"Id": "{distribution_id}"},
                evidence_extraction_path="DistributionConfig.Origins.Items[*].CustomOriginConfig.OriginSslProtocols",
                resource_discovery_method="list_distributions",
                resource_id_field="Id"
            ),
            
            "ec2-security-group-attached-to-eni": SDKImplementation(
                service="ec2",
                client_method="describe_network_interfaces",
                client_params={},
                evidence_extraction_path="NetworkInterfaces[*].Groups",
                resource_discovery_method="describe_network_interfaces",
                resource_id_field="NetworkInterfaceId"
            ),
            
            "iam-password-policy": SDKImplementation(
                service="iam",
                client_method="get_account_password_policy",
                client_params={},
                evidence_extraction_path="PasswordPolicy",
                resource_discovery_method=None,  # Global resource
                resource_id_field=None
            )
        }
    
    def get_implementation(self, config_rule: str) -> SDKImplementation:
        """Get SDK implementation details for a config rule."""
        return self.implementations.get(config_rule)
    
    def add_implementation(self, config_rule: str, implementation: SDKImplementation):
        """Add new SDK implementation (for extensibility)."""
        self.implementations[config_rule] = implementation
```

### **Layer 3: Intelligent Evidence Collector**
```python
# sources/evidence_collection/intelligent_collector.py
class IntelligentEvidenceCollector:
    """
    Uses both config rule mappings AND SDK knowledge to collect evidence.
    """
    
    def __init__(self, config_mappings: List[ConfigRuleMapping], sdk_kb: SDKImplementationKnowledgeBase):
        self.config_mappings = config_mappings
        self.sdk_kb = sdk_kb
        self.aws_clients = {}
    
    def collect_evidence_for_control(self, control_id: str, account_id: str) -> ControlEvidence:
        """Collect evidence for a specific PCI DSS control."""
        
        # 1. Find what config rules are needed for this control
        relevant_mappings = [m for m in self.config_mappings if m.control_id == control_id]
        
        evidence = ControlEvidence(control_id=control_id, account_id=account_id)
        
        for mapping in relevant_mappings:
            # 2. Get SDK implementation details
            implementation = self.sdk_kb.get_implementation(mapping.aws_config_rule)
            if not implementation:
                continue
                
            # 3. Discover resources
            resources = self.discover_resources(account_id, implementation)
            
            # 4. Collect evidence for each resource
            for resource_id in resources:
                evidence_data = self.collect_resource_evidence(
                    account_id, resource_id, implementation
                )
                
                evidence.add_evidence(
                    config_rule=mapping.aws_config_rule,
                    resource_id=resource_id,
                    evidence_data=evidence_data,
                    compliance_criteria=mapping.compliance_criteria
                )
        
        return evidence
    
    def discover_resources(self, account_id: str, implementation: SDKImplementation) -> List[str]:
        """Discover resources that need to be checked."""
        if not implementation.resource_discovery_method:
            return [None]  # Global resource like IAM password policy
            
        client = self.get_aws_client(implementation.service, account_id)
        method = getattr(client, implementation.resource_discovery_method)
        
        response = method()
        
        # Extract resource IDs from response
        if implementation.service == "cloudfront":
            return [item['Id'] for item in response['DistributionList'].get('Items', [])]
        elif implementation.service == "ec2":
            return [item['NetworkInterfaceId'] for item in response['NetworkInterfaces']]
        # Add more resource discovery logic as needed
        
        return []
    
    def collect_resource_evidence(self, account_id: str, resource_id: str, implementation: SDKImplementation) -> Dict:
        """Collect evidence for a specific resource."""
        client = self.get_aws_client(implementation.service, account_id)
        method = getattr(client, implementation.client_method)
        
        # Prepare parameters
        params = implementation.client_params.copy()
        if resource_id and "{distribution_id}" in str(params):
            params = {k: v.format(distribution_id=resource_id) if isinstance(v, str) else v 
                     for k, v in params.items()}
        
        response = method(**params)
        
        # Extract relevant evidence using JSONPath-like extraction
        evidence_data = self.extract_evidence_from_response(
            response, implementation.evidence_extraction_path
        )
        
        return evidence_data
```

### **Layer 4: Evidence Processor & Compliance Evaluator**
```python
# data_pipeline/processors/evidence/compliance_evaluator.py
class ComplianceEvaluator:
    """
    Evaluates collected evidence against compliance criteria.
    """
    
    def evaluate_control_compliance(self, evidence: ControlEvidence) -> ComplianceResult:
        """Evaluate if evidence meets compliance requirements."""
        
        results = []
        for evidence_item in evidence.evidence_items:
            result = self.evaluate_evidence_item(evidence_item)
            results.append(result)
        
        overall_status = self.determine_overall_status(results)
        
        return ComplianceResult(
            control_id=evidence.control_id,
            account_id=evidence.account_id,
            overall_status=overall_status,
            individual_results=results,
            evaluation_timestamp=datetime.utcnow()
        )
    
    def evaluate_evidence_item(self, evidence_item: EvidenceItem) -> EvaluationResult:
        """Evaluate a single evidence item."""
        
        if evidence_item.config_rule == "cloudfront-no-deprecated-ssl-protocols":
            return self.evaluate_cloudfront_ssl_protocols(evidence_item)
        elif evidence_item.config_rule == "ec2-security-group-attached-to-eni":
            return self.evaluate_ec2_security_groups(evidence_item)
        elif evidence_item.config_rule == "iam-password-policy":
            return self.evaluate_iam_password_policy(evidence_item)
        
        return EvaluationResult(status="UNKNOWN", details="No evaluator implemented")
    
    def evaluate_cloudfront_ssl_protocols(self, evidence_item: EvidenceItem) -> EvaluationResult:
        """Evaluate CloudFront SSL protocols compliance."""
        ssl_protocols = evidence_item.evidence_data.get("Items", [])
        
        has_deprecated = any(protocol in ["SSLv3"] for protocol in ssl_protocols)
        
        if has_deprecated:
            return EvaluationResult(
                status="NON_COMPLIANT",
                details=f"Uses deprecated SSL protocols: {ssl_protocols}",
                evidence_summary={"ssl_protocols": ssl_protocols}
            )
        else:
            return EvaluationResult(
                status="COMPLIANT", 
                details=f"Uses secure SSL protocols: {ssl_protocols}",
                evidence_summary={"ssl_protocols": ssl_protocols}
            )
```

## 🗃️ **Data Schemas**

### **Config Rule Mapping Schema**
```python
@dataclass
class ConfigRuleMapping:
    control_id: str                    # "1.2.5"
    aws_config_rule: str              # "cloudfront-no-deprecated-ssl-protocols"
    compliance_criteria: str          # "NON_COMPLIANT if any 'OriginSslProtocols' includes 'SSLv3'"
    pci_description: str              # PCI DSS control description
```

### **SDK Implementation Schema**
```python
@dataclass
class SDKImplementation:
    service: str                      # "cloudfront"
    client_method: str               # "get_distribution_config"
    client_params: Dict[str, Any]    # {"Id": "{distribution_id}"}
    evidence_extraction_path: str    # JSONPath to extract evidence
    resource_discovery_method: Optional[str]  # "list_distributions"
    resource_id_field: Optional[str] # "Id"
```

### **Evidence Schema**
```python
@dataclass
class EvidenceItem:
    config_rule: str
    resource_id: str
    evidence_data: Dict[str, Any]    # Actual collected data
    compliance_criteria: str
    collection_timestamp: datetime
```

## 🚀 **Implementation Strategy**

### **Phase 1: Build the Knowledge Base**
1. Extract config rule mappings from AWS PDF
2. Create SDK implementation knowledge base for core services
3. Build evidence collection engine

### **Phase 2: Evidence Collection System**
1. Multi-account boto3 collector
2. Resource discovery mechanisms
3. Evidence data storage

### **Phase 3: Compliance Evaluation**
1. Rule-based evaluation engine
2. Compliance status determination
3. Reporting and recommendations

### **Phase 4: Extensibility**
1. Easy addition of new config rules
2. Custom compliance criteria
3. Integration with other frameworks

This architecture creates an **intelligent compliance auditing system** that bridges the gap between high-level guidance and actual implementation! 🎯 