# Proposed Data Pipeline Architecture for Compliance Audit Framework

## 🎯 **Current vs. Proposed Structure**

### Current Structure (Generic ETL)
```
data_pipeline/
├── extractors/compliance/pci_dss_v4_0_1/
├── schemas/
├── pipelines/
└── cli.py
```

### Proposed Structure (Domain-Specific)
```
data_pipeline/
├── sources/                    # Data ingestion from various sources
│   ├── s3/                    # S3 document retrieval
│   ├── local/                 # Local file handling
│   ├── config/                # Configuration management
│   └── __init__.py
├── processors/                # Core document processing
│   ├── compliance/            # Compliance-specific processors
│   │   ├── pci_dss/          # PCI DSS v4.0.1 processor
│   │   ├── iso27001/         # Future: ISO27001 processor
│   │   ├── nist_csf/         # Future: NIST CSF processor
│   │   └── __init__.py
│   ├── documents/            # Document processing utilities
│   │   ├── pdf/              # PDF extraction & conversion
│   │   ├── markdown/         # Markdown processing
│   │   └── tables/           # Table extraction & parsing
│   └── config/               # Configuration file processing
├── formatters/               # Output format generation
│   ├── knowledge_base/       # Bedrock KB format (chunks + metadata)
│   ├── database/            # Database-ready formats (CSV, JSON)
│   ├── storage/             # File storage formats
│   └── __init__.py
├── destinations/            # Output handling
│   ├── s3/                  # S3 uploads for KB sources
│   ├── bedrock/             # Knowledge Base creation
│   ├── database/            # Database ingestion
│   └── __init__.py
├── orchestration/           # Workflow management
│   ├── workflows/           # Pre-defined workflows
│   ├── triggers/            # Event-based triggers
│   └── monitoring/          # Pipeline monitoring
├── schemas/                 # Shared data models
│   ├── compliance/          # Compliance-specific schemas
│   ├── documents/           # Document schemas
│   └── config/              # Configuration schemas
└── cli.py                   # Unified CLI interface
```

## 🔄 **Your Flow Mapped to New Structure**

### 1. **Load PDF/Config from S3**
```python
# sources/s3/document_loader.py
class S3DocumentLoader:
    def download_compliance_document(self, bucket: str, key: str) -> DocumentSource
    def download_config_file(self, bucket: str, key: str) -> ConfigSource
    def list_available_frameworks(self) -> List[ComplianceFramework]

# sources/config/config_loader.py  
class ConfigLoader:
    def load_audit_config(self, source: str) -> AuditConfiguration
    def validate_config_schema(self, config: dict) -> ValidationResult
```

### 2a. **Extract & Chunk PDFs for Knowledge Base**
```python
# processors/documents/pdf/extractor.py
class PDFProcessor:
    def extract_text(self, pdf_path: str) -> DocumentContent
    def extract_tables(self, pdf_path: str) -> List[TableData]

# processors/compliance/pci_dss/control_processor.py
class PCIDSSControlProcessor:
    def extract_controls(self, content: DocumentContent) -> List[ComplianceControl]
    def validate_extraction_quality(self, controls: List[ComplianceControl]) -> QualityReport

# formatters/knowledge_base/chunker.py
class KnowledgeBaseChunker:
    def create_semantic_chunks(self, controls: List[ComplianceControl]) -> List[KBChunk]
    def optimize_for_embeddings(self, chunks: List[KBChunk]) -> List[OptimizedChunk]
```

### 2b. **Extract PDF to CSV/Table Format**
```python
# formatters/database/csv_generator.py
class DatabaseCSVGenerator:
    def generate_controls_csv(self, controls: List[ComplianceControl]) -> CSVOutput
    def generate_requirements_csv(self, controls: List[ComplianceControl]) -> CSVOutput
    def create_relational_schema(self, framework: ComplianceFramework) -> DatabaseSchema

# formatters/database/table_formatter.py
class TableFormatter:
    def format_for_postgres(self, data: Any) -> PostgreSQLFormat
    def format_for_mysql(self, data: Any) -> MySQLFormat
    def create_indexes(self, schema: DatabaseSchema) -> List[IndexDefinition]
```

### 2c. **Extract & Store Config Values**
```python
# processors/config/audit_config_processor.py
class AuditConfigProcessor:
    def parse_compliance_settings(self, config: dict) -> ComplianceSettings
    def extract_business_rules(self, config: dict) -> List[BusinessRule]
    def validate_framework_compatibility(self, settings: ComplianceSettings) -> bool

# formatters/database/config_formatter.py
class ConfigFormatter:
    def format_settings_for_db(self, settings: ComplianceSettings) -> DatabaseConfig
    def create_config_schema(self) -> ConfigSchema
```

## 🎛️ **Orchestration Layer**

### Workflow Definitions
```python
# orchestration/workflows/compliance_audit_workflow.py
class ComplianceAuditWorkflow:
    def run_full_audit(self, framework: ComplianceFramework, source_config: dict):
        # 1. Load documents and config
        # 2. Process compliance documents  
        # 3. Generate multiple output formats
        # 4. Upload to destinations
        # 5. Create Knowledge Base
        # 6. Ingest to database
        
    def run_incremental_update(self, changed_documents: List[str]):
        # Handle updates to existing frameworks
        
    def run_new_framework_onboarding(self, framework: ComplianceFramework):
        # Add support for new compliance framework
```

### Event-Based Triggers
```python
# orchestration/triggers/s3_triggers.py
class S3DocumentTrigger:
    def on_new_document_uploaded(self, event: S3Event):
        # Automatically process new compliance documents
        
    def on_config_updated(self, event: S3Event):
        # Reprocess affected workflows when config changes
```

## 🔌 **Destination Handlers**

### S3 & Knowledge Base
```python
# destinations/s3/kb_uploader.py
class KnowledgeBaseUploader:
    def upload_chunks_to_s3(self, chunks: List[KBChunk], bucket: str) -> S3Location
    def create_metadata_files(self, chunks: List[KBChunk]) -> List[MetadataFile]

# destinations/bedrock/kb_manager.py  
class BedrockKnowledgeBaseManager:
    def create_knowledge_base(self, name: str, chunks_location: S3Location) -> KnowledgeBaseId
    def update_knowledge_base(self, kb_id: str, new_chunks: S3Location) -> UpdateResult
    def configure_retrieval_settings(self, kb_id: str, settings: RetrievalConfig) -> bool
```

### Database Integration
```python
# destinations/database/ingestion_manager.py
class DatabaseIngestionManager:
    def create_compliance_tables(self, framework: ComplianceFramework) -> DatabaseSchema
    def ingest_controls(self, controls: List[ComplianceControl], schema: DatabaseSchema) -> IngestResult
    def ingest_config(self, config: ComplianceSettings, schema: DatabaseSchema) -> IngestResult
    def create_audit_views(self, framework: ComplianceFramework) -> List[ViewDefinition]
```

## 📋 **Benefits of This Architecture**

### 1. **Domain-Specific Design**
- ✅ **Compliance-focused**: Built specifically for audit frameworks
- ✅ **Extensible**: Easy to add new frameworks (ISO27001, NIST, SOC2)
- ✅ **Reusable**: Common document processing across frameworks

### 2. **Clear Separation of Concerns**
- 🔍 **Sources**: Handle data ingestion complexity
- ⚙️ **Processors**: Framework-specific business logic
- 📊 **Formatters**: Output format optimization
- 🎯 **Destinations**: Delivery to various systems

### 3. **Workflow Optimization**
- 🔄 **Parallel Processing**: Generate KB chunks and DB formats simultaneously
- 📈 **Incremental Updates**: Handle document changes efficiently
- 🎛️ **Event-Driven**: Automatic processing on S3 uploads

### 4. **Production Ready**
- 📊 **Monitoring**: Built-in quality metrics and error tracking
- 🔒 **Security**: Proper handling of sensitive compliance data
- 📈 **Scalable**: Can handle multiple frameworks and large documents

## 🚀 **Implementation Strategy**

### Phase 1: Restructure Existing Code
1. Move PCI DSS extractor to `processors/compliance/pci_dss/`
2. Create `sources/` for S3 and config loading
3. Split formatters into KB and database formatters
4. Create destination handlers

### Phase 2: Add Orchestration
1. Implement workflow management
2. Add S3 trigger handling
3. Create monitoring and error handling

### Phase 3: Multi-Framework Support
1. Add ISO27001 processor
2. Add NIST CSF processor
3. Create framework-agnostic interfaces

This architecture is **domain-specific, scalable, and production-ready** for your compliance audit framework! 