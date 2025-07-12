# Restructured Data Pipeline - Config Rule Mapping & Evidence Collection

## 🏗️ **New Structure Overview**

```
data_pipeline/
├── sources/                          # Data ingestion
│   ├── config/                      # Configuration file sources
│   ├── evidence_collection/         # Multi-account AWS config collection
│   ├── local/                       # Local file handling
│   └── s3/                          # S3 document retrieval
├── processors/                       # Core processing logic
│   ├── compliance_standards/        # Compliance framework processors
│   │   ├── pci_dss/                # ✅ PCI DSS v4.0.1 (306 controls)
│   │   │   ├── core/               # Existing extractor modules
│   │   │   ├── adapter.py          # Pipeline integration
│   │   │   ├── main.py             # CLI interface
│   │   │   └── README.md           # Documentation
│   │   └── iso27001/               # 🔮 Future: ISO27001 processor
│   ├── config_mappings/            # 🚧 AWS Config Rule mapping extraction
│   ├── config_processor/           # 🚧 Multi-account config processing
│   ├── evidence/                   # 🚧 Evidence validation & evaluation
│   └── shared/                     # Common utilities
├── formatters/                      # Output format generation
│   ├── knowledge_base/             # Bedrock KB format (semantic chunks)
│   ├── database/                   # PostgreSQL format (structured data)
│   └── storage/                    # S3 archive format (evidence packages)
├── destinations/                    # Output handling
│   ├── bedrock/                    # Bedrock Knowledge Base management
│   ├── database/                   # Aurora PostgreSQL ingestion
│   └── s3/                         # S3 uploads & archival
├── orchestration/                   # Workflow management
│   ├── workflows/                  # Pre-defined audit workflows
│   ├── triggers/                   # Event-based triggers
│   └── monitoring/                 # Pipeline monitoring
├── schemas/                        # Shared data models
├── notebooks/                      # Analysis notebooks
└── cli.py                          # Unified CLI interface
```

## 🎯 **Component Responsibilities**

### **1. Sources - Data Ingestion**
```python
# sources/evidence_collection/ - NEW
# Multi-account AWS config collection using boto3
class MultiAccountCollector:
    def collect_from_accounts(self, accounts: List[str]) -> EvidenceSet
    def assume_cross_account_role(self, account: str, role: str) -> Session
```

### **2. Processors - Core Logic**

#### **Compliance Standards** (Multi-Framework Support)
```python
# processors/compliance_standards/pci_dss/ - EXISTING (306 controls)
# Already working PCI DSS processor - no changes needed

# processors/compliance_standards/iso27001/ - FUTURE
class ISO27001Processor:
    def extract_controls(self, pdf_path: str) -> List[ISO27001Control]
```

#### **Config Mappings** (NEW - Critical Component)
```python
# processors/config_mappings/ - NEW
class AWSConfigRuleProcessor:
    def extract_config_mappings(self, pdf_path: str) -> List[ConfigRuleMapping]
    # Extracts: Control ID → AWS Config Rule → Guidance
    # From: AWSOperationalBestPracticesPCIDSS4.pdf
```

#### **Config Processor** (NEW - Your Request)
```python
# processors/config_processor/ - NEW
class MultiAccountConfigProcessor:
    def normalize_configs(self, raw_configs: Dict) -> NormalizedConfigs
    def validate_against_rules(self, configs: NormalizedConfigs) -> ValidationResults
    def generate_compliance_status(self, validations: ValidationResults) -> ComplianceStatus
```

#### **Evidence Processor** (NEW)
```python
# processors/evidence/ - NEW  
class EvidenceProcessor:
    def evaluate_compliance(self, evidence: Evidence, rules: ConfigRules) -> ComplianceResult
    def generate_recommendations(self, results: ComplianceResult) -> List[Recommendation]
```

### **3. Formatters - Multi-Output Support**

#### **Knowledge Base Formatter**
```python
# formatters/knowledge_base/
# Creates semantic chunks for Bedrock KB
class BedrockChunker:
    def chunk_compliance_content(self, controls: List[Control]) -> List[KBChunk]
    def optimize_for_embeddings(self, chunks: List[KBChunk]) -> List[OptimizedChunk]
```

#### **Database Formatter**
```python
# formatters/database/
# Creates structured data for PostgreSQL
class PostgreSQLFormatter:
    def format_audit_results(self, results: AuditResults) -> DatabaseSchema
    def create_compliance_tables(self, framework: ComplianceFramework) -> TableDefinitions
```

#### **Storage Formatter**
```python
# formatters/storage/
# Creates evidence packages for S3 archival
class S3StorageFormatter:
    def package_evidence_set(self, evidence: EvidenceSet) -> S3Package
    def create_audit_metadata(self, audit: AuditSession) -> AuditMetadata
```

## 🔄 **Workflow Integration**

### **Document Processing Workflow**
```
PCI-DSS-v4_0_1.pdf → processors/compliance_standards/pci_dss/ → 306 controls
AWSOperationalBestPracticesPCIDSS4.pdf → processors/config_mappings/ → Config blueprints
```

### **Evidence Collection Workflow**
```
Multi-account configs → sources/evidence_collection/ → processors/config_processor/ → 
formatters/{database,storage}/ → destinations/{database,s3}/
```

### **Compliance Evaluation Workflow**
```
Config blueprints + Collected evidence → processors/evidence/ → 
ComplianceResults → formatters/knowledge_base/ → destinations/bedrock/
```

## 🚀 **Implementation Priorities**

### **Phase 1: Config Mapping Processor** ✅ Current Focus
1. `processors/config_mappings/aws_config_rule_processor.py`
2. Extract table data from AWS Config PDF
3. Create ConfigRuleMapping schema

### **Phase 2: Enhanced Evidence Collector**
1. `sources/evidence_collection/multi_account_collector.py`
2. `processors/config_processor/config_normalizer.py`
3. Integration with services/evidence_collector

### **Phase 3: Compliance Evaluator**
1. `processors/evidence/compliance_evaluator.py`
2. Rule-based evaluation engine
3. Automated compliance reporting

### **Phase 4: Dual Output System**
1. Enhanced formatters for Bedrock KB + PostgreSQL
2. S3 evidence archival
3. Compliance dashboard

## 🎊 **Key Benefits of New Structure**

### 1. **Framework Extensibility**
- ✅ **PCI DSS**: Working (306 controls)
- 🚧 **Config Mappings**: Foundation for automated auditing
- 🔮 **ISO27001**: Easy to add using same patterns

### 2. **Evidence-Driven Architecture**
- 🔍 **Collection**: Multi-account AWS config gathering
- ⚙️ **Processing**: Normalize and validate configs  
- 📊 **Evaluation**: Automated compliance checking
- 💾 **Storage**: Dual output (DB + Archive)

### 3. **AI Integration Ready**
- 🧠 **Bedrock KB**: Semantic search over compliance content
- 🤖 **Evidence AI**: Query compliance status via natural language
- 📈 **Continuous Monitoring**: Automated compliance tracking

This structure **perfectly matches your config rule mapping workflow** and scales for multi-framework compliance auditing! 🎯 