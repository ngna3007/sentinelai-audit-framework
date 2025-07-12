# Actual Workflow Architecture - SentinelAI Audit Framework

## 🎯 **Current Reality vs. Proposed Architecture**

### **A/ PDF Processing Requirements**

#### **Multiple Document Types with Different Processors**
```
shared_data/documents/
├── PCI-DSS-v4_0_1.pdf              # ✅ Compliance Standards (306 controls)
├── AWSOperationalBestPracticesPCIDSS4.pdf  # 🚧 Implementation Guidelines  
└── [future compliance PDFs]        # 🔮 ISO27001, NIST CSF, etc.
```

#### **Current vs. Needed Processors**
```python
# ✅ CURRENT: PCI Standards Processor
data_pipeline/processors/compliance/pci_dss/
├── control_extractor.py           # Extracts 306 controls
├── table_parser.py               # Handles complex tables
└── quality_validator.py          # 95% quality score

# 🚧 NEEDED: AWS Best Practices Processor  
data_pipeline/processors/implementation/aws_practices/
├── practice_extractor.py         # Extract implementation patterns
├── code_snippet_parser.py        # Parse CloudFormation/code examples
└── mapping_generator.py          # Map practices to PCI controls

# 🔮 FUTURE: Additional Processors
data_pipeline/processors/compliance/iso27001/
data_pipeline/processors/implementation/azure_practices/
```

### **B/ Evidence Collection Requirements**

#### **Multi-Account Config Collection**
```python
# 🚧 TO BE BUILT: Enhanced Evidence Collector
services/evidence_collector/
├── collectors/
│   ├── aws_config_collector.py   # Collect from multiple AWS accounts
│   ├── azure_collector.py        # Future: Azure configs  
│   └── gcp_collector.py          # Future: GCP configs
├── processors/
│   ├── config_normalizer.py      # Standardize different formats
│   ├── compliance_mapper.py      # Map configs to requirements
│   └── evidence_validator.py     # Validate collected evidence
└── storage/
    ├── s3_uploader.py            # Archive to S3
    └── db_ingestion.py           # Store in PostgreSQL
```

## 🏗️ **Optimized Architecture for Your Workflow**

### **Phase 1: Document Processing Pipeline**

```
data_pipeline/
├── processors/
│   ├── documents/               # Document-type-specific processors
│   │   ├── compliance_standards/    # PCI DSS, ISO27001, etc.
│   │   │   ├── pci_dss_processor.py     # ✅ Current (306 controls)
│   │   │   └── iso27001_processor.py    # 🔮 Future
│   │   ├── implementation_guides/      # AWS, Azure best practices
│   │   │   ├── aws_practices_processor.py   # 🚧 Needed
│   │   │   └── azure_practices_processor.py # 🔮 Future
│   │   └── shared/                     # Common utilities
│   │       ├── pdf_extractor.py       # PDF text extraction
│   │       ├── table_parser.py        # Table structure detection
│   │       └── content_chunker.py     # Semantic chunking
│   └── evidence/                # Evidence collection processing
│       ├── config_processors/       # Config-specific processing
│       │   ├── aws_config_processor.py
│       │   └── compliance_mapper.py
│       └── validators/             # Evidence validation
├── formatters/
│   ├── bedrock/                # Knowledge Base formatting
│   │   ├── semantic_chunker.py     # Optimize for embeddings
│   │   └── metadata_generator.py   # KB metadata
│   ├── database/               # PostgreSQL formatting  
│   │   ├── schema_generator.py     # Create DB schemas
│   │   ├── csv_formatter.py       # Database-ready CSV
│   │   └── json_formatter.py      # Structured JSON
│   └── storage/                # S3 archive formatting
│       ├── evidence_packager.py   # Package evidence sets
│       └── metadata_indexer.py    # Create searchable indexes
└── destinations/
    ├── bedrock/                # Bedrock Knowledge Base
    ├── database/               # Aurora PostgreSQL
    └── storage/                # S3 Evidence Store
```

### **Phase 2: Evidence Collection Integration**

```python
# services/evidence_collector/main.py
class EvidenceCollector:
    def collect_aws_configs(self, accounts: List[str]) -> EvidenceSet:
        """Collect configs from multiple AWS accounts."""
        evidence = EvidenceSet()
        
        for account in accounts:
            # Use boto3 to collect various AWS configs
            ec2_configs = self.collect_ec2_configs(account)
            vpc_configs = self.collect_vpc_configs(account) 
            iam_configs = self.collect_iam_configs(account)
            
            evidence.add_account_data(account, {
                'ec2': ec2_configs,
                'vpc': vpc_configs,
                'iam': iam_configs
            })
        
        return evidence
    
    def process_and_store(self, evidence: EvidenceSet):
        """Process evidence and store in dual format."""
        # 1. Normalize and validate
        processor = ConfigProcessor()
        normalized = processor.normalize_evidence(evidence)
        
        # 2. Format for PostgreSQL
        db_formatter = DatabaseFormatter()
        db_data = db_formatter.format_for_postgres(normalized)
        
        # 3. Format for S3 storage
        s3_formatter = StorageFormatter()
        s3_package = s3_formatter.package_evidence(normalized)
        
        # 4. Store in both destinations
        DatabaseIngestion().store_evidence(db_data)
        S3Storage().upload_evidence_package(s3_package)
```

## 🔄 **Workflow Orchestration**

### **A/ PDF Processing Workflow**
```python
# orchestration/workflows/document_workflow.py
class DocumentProcessingWorkflow:
    
    def process_compliance_standard(self, pdf_path: str) -> ProcessingResult:
        """Process compliance standards like PCI DSS."""
        # 1. Detect document type
        doc_type = self.detect_document_type(pdf_path)
        
        # 2. Route to appropriate processor
        if doc_type == 'pci_dss':
            processor = PCIDSSProcessor()
        elif doc_type == 'iso27001':
            processor = ISO27001Processor()
        
        # 3. Extract content
        controls = processor.extract_controls(pdf_path)
        
        # 4. Generate dual outputs
        kb_chunks = BedrockFormatter().format_for_kb(controls)
        db_data = DatabaseFormatter().format_for_postgres(controls)
        
        # 5. Store in destinations
        self.store_in_bedrock_kb(kb_chunks)
        self.store_in_database(db_data)
        
        return ProcessingResult(controls=len(controls))
    
    def process_implementation_guide(self, pdf_path: str) -> ProcessingResult:
        """Process implementation guides like AWS best practices."""
        # 1. Use implementation guide processor
        processor = AWSPracticesProcessor()
        practices = processor.extract_practices(pdf_path)
        
        # 2. Map to compliance requirements
        mapper = ComplianceMapper()
        mapped_practices = mapper.map_to_pci_controls(practices)
        
        # 3. Generate outputs
        kb_chunks = BedrockFormatter().format_practices_for_kb(mapped_practices)
        db_data = DatabaseFormatter().format_practices_for_postgres(mapped_practices)
        
        # 4. Store
        self.store_in_bedrock_kb(kb_chunks)
        self.store_in_database(db_data)
        
        return ProcessingResult(practices=len(practices))
```

### **B/ Evidence Collection Workflow**
```python
# orchestration/workflows/evidence_workflow.py
class EvidenceCollectionWorkflow:
    
    def collect_multi_account_evidence(self, accounts: List[str]) -> CollectionResult:
        """Collect evidence from multiple AWS accounts."""
        # 1. Collect from all accounts
        collector = EvidenceCollector()
        evidence_set = collector.collect_aws_configs(accounts)
        
        # 2. Process and normalize
        processor = EvidenceProcessor()
        processed = processor.normalize_and_validate(evidence_set)
        
        # 3. Map to compliance requirements
        mapper = ComplianceMapper()
        compliance_evidence = mapper.map_to_requirements(processed)
        
        # 4. Generate outputs
        # S3 first for archival
        s3_package = StorageFormatter().package_evidence(compliance_evidence)
        S3Storage().upload_evidence_package(s3_package)
        
        # Then database for querying
        db_data = DatabaseFormatter().format_evidence_for_postgres(compliance_evidence)
        DatabaseIngestion().store_evidence(db_data)
        
        return CollectionResult(
            accounts=len(accounts),
            evidence_items=len(compliance_evidence),
            s3_location=s3_package.location,
            db_records=len(db_data)
        )
```

## 🎯 **Immediate Implementation Plan**

### **Week 1-2: AWS Best Practices Processor**
```python
# 🚧 Priority 1: Build AWS practices processor
data_pipeline/processors/documents/implementation_guides/aws_practices_processor.py

class AWSPracticesProcessor:
    def extract_practices(self, pdf_path: str) -> List[ImplementationPractice]:
        """Extract AWS implementation practices from PDF."""
        # Different from PCI DSS - focuses on code examples, configurations
        pass
    
    def map_to_pci_controls(self, practices: List[ImplementationPractice]) -> List[MappedPractice]:
        """Map AWS practices to PCI DSS controls."""
        # Creates relationships between implementation and requirements
        pass
```

### **Week 3-4: Evidence Collector Enhancement**
```python
# 🚧 Priority 2: Build evidence collector
services/evidence_collector/collectors/aws_config_collector.py

class AWSConfigCollector:
    def __init__(self, assume_role_arn: str = None):
        self.session = boto3.Session()
        if assume_role_arn:
            self.session = self.assume_cross_account_role(assume_role_arn)
    
    def collect_ec2_evidence(self) -> EC2Evidence:
        """Collect EC2 security configurations."""
        ec2 = self.session.client('ec2')
        # Collect security groups, NACLs, instances, etc.
        pass
    
    def collect_vpc_evidence(self) -> VPCEvidence:
        """Collect VPC network configurations."""
        # Collect VPC settings, subnets, route tables, etc.
        pass
```

### **Week 5-6: Dual Output Integration**
```python
# 🚧 Priority 3: Enhance formatters for dual output
data_pipeline/formatters/bedrock/semantic_chunker.py
data_pipeline/formatters/database/postgres_formatter.py

# Both should work from same processed data
class DualOutputFormatter:
    def format_for_both_destinations(self, data: ProcessedData) -> DualOutput:
        bedrock_chunks = self.format_for_bedrock(data)
        postgres_data = self.format_for_postgres(data)
        return DualOutput(bedrock_chunks, postgres_data)
```

## 🎊 **Key Architectural Benefits**

### 1. **Document-Type-Specific Processing**
- ✅ **Standards Documents**: PCI DSS (306 controls) - working
- 🚧 **Implementation Guides**: AWS best practices - different parsing needed
- 🔮 **Future Extensible**: ISO27001, NIST CSF, Azure guides

### 2. **Local-First with Cloud Migration Path**
- ✅ **Current**: Process local PDFs
- 🔄 **Migration Ready**: Easy to add S3 source handlers later
- 🚀 **Event-Driven**: Can add S3 triggers when ready

### 3. **Dual Output Optimization**
- 🧠 **Bedrock KB**: Semantic chunks optimized for RAG
- 🗄️ **PostgreSQL**: Structured data for compliance reporting
- 📦 **S3 Archive**: Evidence storage and backup

### 4. **Evidence Collection Integration**
- ⚙️ **Config Collection**: Multi-account AWS config gathering
- 🔄 **Processing**: Normalize and map to compliance requirements
- 💾 **Dual Storage**: PostgreSQL for querying + S3 for archival

This architecture **matches your exact workflow** and scales naturally as you move to cloud infrastructure! 🚀 