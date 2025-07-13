# Database Module - Supabase Integration & CLI

A comprehensive database layer for the SentinelAI Audit Framework, providing Supabase integration, repository pattern implementation, and a powerful CLI for managing compliance audit data.

## 🏗️ Architecture Overview

This database module implements a clean architecture with clear separation of concerns:

```
database/
├── auth/                     # 🔐 Authentication & connection management
│   ├── __init__.py          # Package exports
│   ├── connection.py        # Database connection handling
│   ├── credentials.py       # Credential management
│   └── supabase_client.py   # Supabase client setup
├── importers/               # 📥 Data import functionality
│   ├── __init__.py          # Package exports
│   ├── __main__.py          # Module execution support
│   ├── main.py              # Standalone CLI
│   ├── bulk_import.py       # Bulk CSV import orchestration
│   └── csv_importer.py      # Individual CSV file import
├── migrations/              # 🗃️ Database schema management
│   ├── __init__.py          # Package exports
│   ├── create_tables.py     # Table creation logic
│   ├── migration_runner.py  # Migration orchestration
│   └── schema_validator.py  # Schema validation
├── models/                  # 📊 Data models
│   ├── aws_config.py        # AWS Config rule models
│   └── pci_controls.py      # PCI DSS control models
├── repositories/            # 🔄 Data access layer (Repository pattern)
│   ├── __init__.py          # Package exports
│   ├── base.py              # Base repository class
│   ├── aws_config_repository.py      # AWS Config data access
│   ├── pci_control_repository.py     # PCI control data access
│   └── pci_aws_mapping_repository.py # Mapping data access
├── cli.py                   # 🖥️ Main CLI interface
├── create_tables_manual.sql # 📋 Manual table creation script
└── requirements.txt         # 📦 Python dependencies
```

### Key Benefits

- **🔧 Repository Pattern**: Clean data access abstraction with CRUD operations
- **🔐 Secure Authentication**: Supabase integration with credential management
- **📥 Bulk Import System**: Efficient CSV processing with validation and error handling
- **🗃️ Schema Management**: Automated migrations with rollback capabilities
- **🖥️ Comprehensive CLI**: Full-featured command-line interface for all operations
- **📊 Type Safety**: Pydantic models for data validation and structure

## 🚀 Quick Start

### Prerequisites

1. **Supabase Account**: Database credentials and project URL
2. **Python Environment**: Python 3.8+ with virtual environment
3. **Project Setup**: SentinelAI Audit Framework installed

### Environment Setup

```bash
# 1. Navigate to database directory
cd /path/to/sentinelai-audit-framework/database

# 2. Initialize environment file
python cli.py auth init

# 3. Edit .env file with your Supabase credentials
# SUPABASE_URL=your-project-url
# SUPABASE_SERVICE_ROLE_KEY=your-service-key
# SUPABASE_ANON_KEY=your-anon-key

# 4. Test connection
python cli.py auth check
```

### Basic Operations

```bash
# Run database migrations
python cli.py db migrate

# Import data from CSV files
python cli.py import-data bulk --source /path/to/csv/files

# List imported data
python cli.py data list pci_dss_controls --limit 5

# Show database statistics
python cli.py data stats
```

## 📋 CLI Reference

The CLI provides four main command groups for comprehensive database management:

### Authentication Commands

```bash
# Initialize .env file with template
python cli.py auth init

# Check Supabase credentials and connection
python cli.py auth check
```

### Database Operations

```bash
# Run database migrations (create tables, indexes)
python cli.py db migrate
python cli.py db migrate --validate         # Run with schema validation
python cli.py db migrate --dry-run          # Show what would be done

# Rollback specific tables
python cli.py db rollback pci_dss_controls
python cli.py db rollback table1 table2     # Multiple tables
```

### Data Management

```bash
# List records from tables
python cli.py data list pci_dss_controls
python cli.py data list aws_config_rules_guidance --limit 20
python cli.py data list all --format json   # All tables in JSON format

# Clear all records (use with caution)
python cli.py data clear pci_dss_controls
python cli.py data clear all                # Clear all tables

# Seed database with test data
python cli.py data seed

# Show database statistics
python cli.py data stats
```

### Data Import Operations

```bash
# Bulk import from CSV files
python cli.py import-data bulk
python cli.py import-data bulk --source /custom/path/to/csvs
python cli.py import-data bulk --batch-size 500 --no-validate
python cli.py import-data bulk --no-progress    # Silent import
```

### Standalone Importer CLI

```bash
# Use importers as standalone module
python -m database.importers --help
python -m database.importers info
python -m database.importers csv file.csv table_name
python -m database.importers bulk /path/to/csvs

# Or run directly
python database/importers/main.py --help
```

## 🗃️ Database Schema

### Table Descriptions

#### `pci_dss_controls`
Stores PCI DSS v4.0.1 compliance controls with detailed metadata.

```sql
CREATE TABLE pci_dss_controls (
    id UUID PRIMARY KEY NOT NULL DEFAULT gen_random_uuid(),
    control_id VARCHAR(20) NOT NULL UNIQUE,
    requirement TEXT,
    chunk TEXT NOT NULL,
    metadata JSONB NOT NULL
);
```

**Key Fields:**
- `control_id`: Unique identifier (e.g., "1.1.1", "12.3.4")
- `chunk`: Control content optimized for vector databases
- `metadata`: JSONB with control category, requirements, testing procedures

#### `aws_config_rules_guidance`
AWS Config rule documentation and guidance for compliance mapping.

```sql
CREATE TABLE aws_config_rules_guidance (
    id UUID PRIMARY KEY NOT NULL DEFAULT gen_random_uuid(),
    config_rule VARCHAR(100) NOT NULL UNIQUE,
    chunk TEXT NOT NULL,
    metadata JSONB NOT NULL
);
```

**Key Fields:**
- `config_rule`: AWS Config rule name
- `chunk`: Rule documentation and guidance
- `metadata`: Rule category, compliance frameworks, parameters

#### `pci_aws_config_rule_mappings`
Mappings between PCI DSS controls and AWS Config rules.

```sql
CREATE TABLE pci_aws_config_rule_mappings (
    id UUID PRIMARY KEY NOT NULL DEFAULT gen_random_uuid(),
    control_id VARCHAR(20) NOT NULL UNIQUE,
    config_rules JSONB NOT NULL
);
```

**Key Fields:**
- `control_id`: PCI DSS control identifier
- `config_rules`: Array of AWS Config rules and metadata

### Performance Indexes

```sql
-- PCI DSS Controls
CREATE UNIQUE INDEX idx_control_id ON pci_dss_controls (control_id);
CREATE INDEX idx_metadata_gin ON pci_dss_controls USING GIN (metadata);

-- AWS Config Rules
CREATE UNIQUE INDEX idx_config_rule ON aws_config_rules_guidance (config_rule);
CREATE INDEX idx_metadata_gin_aws ON aws_config_rules_guidance USING GIN (metadata);

-- Mappings
CREATE UNIQUE INDEX idx_mapping_control_id ON pci_aws_config_rule_mappings (control_id);
CREATE INDEX idx_config_rules_gin ON pci_aws_config_rule_mappings USING GIN (config_rules);
```

### Sample Queries

```sql
-- Get all controls for requirement 1
SELECT control_id, chunk 
FROM pci_dss_controls 
WHERE (metadata->>'requirements_id') = '1';

-- Search for network security controls
SELECT control_id, metadata->>'control_category'
FROM pci_dss_controls 
WHERE chunk ILIKE '%network security%';

-- Find AWS Config rules for a PCI control
SELECT config_rules 
FROM pci_aws_config_rule_mappings 
WHERE control_id = '1.1.1';

-- Get control statistics by category
SELECT 
    metadata->>'control_category' as category,
    COUNT(*) as control_count
FROM pci_dss_controls 
GROUP BY metadata->>'control_category';
```

## 🧩 Module Details

### `auth/` - Authentication & Connection Management

**Purpose**: Secure Supabase authentication and connection handling

#### `connection.py` - Database Connection
- **DatabaseConnection**: Singleton pattern for connection management
- **Features**: Connection pooling, retry logic, health checks
- **Usage**: `from database.auth.connection import db_connection`

#### `credentials.py` - Credential Management
- **CredentialManager**: Environment variable management
- **Validation**: Credential format and accessibility checks
- **Security**: No credential logging or exposure

#### `supabase_client.py` - Supabase Client
- **Client Factory**: Configured Supabase client creation
- **Authentication**: Service role and anonymous key handling
- **Configuration**: Timeout, retry, and connection settings

### `importers/` - Data Import System

**Purpose**: Efficient CSV data import with validation and error handling

#### `bulk_import.py` - Bulk Import Orchestration
- **BulkImporter**: Orchestrates multiple CSV file imports
- **Validation**: Pre-import schema and data validation
- **Progress Tracking**: Real-time import progress and statistics
- **Error Handling**: Comprehensive error collection and reporting

#### `csv_importer.py` - CSV File Processing
- **CsvImporter**: Individual CSV file processing
- **Batch Processing**: Configurable batch sizes for memory efficiency
- **Data Cleaning**: Automatic data cleaning and transformation
- **Type Safety**: UUID generation and data type validation

#### `main.py` - Standalone CLI
- **Independent Usage**: Run importers without main CLI
- **Module Support**: `python -m database.importers`
- **Command Options**: csv, bulk, info commands

### `migrations/` - Schema Management

**Purpose**: Database schema versioning and migration management

#### `migration_runner.py` - Migration Orchestration
- **MigrationRunner**: Automated schema deployment
- **Validation**: Pre-migration schema validation
- **Rollback**: Safe table rollback capabilities
- **Dry Run**: Preview changes before execution

#### `create_tables.py` - Table Creation Logic
- **Schema Definition**: Complete table and index definitions
- **Constraint Management**: Foreign keys and unique constraints
- **Index Optimization**: Performance-optimized index creation

#### `schema_validator.py` - Schema Validation
- **Validation Rules**: Schema consistency and integrity checks
- **Compatibility**: Cross-version schema compatibility
- **Error Detection**: Schema drift and inconsistency detection

### `models/` - Data Models

**Purpose**: Type-safe data structures and validation

#### `pci_controls.py` - PCI DSS Models
- **PciControl**: Complete control data structure
- **Validation**: Pydantic-based field validation
- **Serialization**: JSON and dictionary conversion methods

#### `aws_config.py` - AWS Config Models
- **AwsConfigRule**: Config rule data structure
- **PciAwsConfigMapping**: Control-to-rule mapping model
- **Relationships**: Model relationship definitions

### `repositories/` - Data Access Layer

**Purpose**: Repository pattern implementation for clean data access

#### `base.py` - Base Repository
- **BaseRepository**: Common CRUD operation patterns
- **Error Handling**: Standardized error handling and logging
- **Transaction Support**: Database transaction management
- **Query Optimization**: Efficient query patterns

#### `pci_control_repository.py` - PCI Control Data Access
- **CRUD Operations**: Create, read, update, delete controls
- **Search Functions**: Full-text search and filtering
- **Bulk Operations**: Efficient bulk insert and update
- **Metadata Queries**: JSONB metadata searching

#### `aws_config_repository.py` - AWS Config Data Access
- **Rule Management**: AWS Config rule CRUD operations
- **Guidance Retrieval**: Rule documentation and guidance
- **Integration**: PCI control mapping integration

#### `pci_aws_mapping_repository.py` - Mapping Data Access
- **Mapping Management**: Control-to-rule mapping operations
- **Relationship Queries**: Complex relationship queries
- **Bulk Mapping**: Efficient bulk mapping operations

## 💾 Data Import/Export

### Bulk Import Process

The bulk import system processes CSV files from the data pipeline with comprehensive validation:

```bash
# Standard import from shared_data/outputs
python cli.py import-data bulk

# Custom source directory
python cli.py import-data bulk --source /path/to/csvs

# Performance optimization
python cli.py import-data bulk --batch-size 2000 --no-validate
```

#### Import Workflow

1. **📁 Directory Scan**: Locate recognized CSV files
2. **🔍 Pre-validation**: Schema and data integrity checks
3. **📊 Progress Setup**: Initialize progress tracking
4. **⚡ Batch Processing**: Process files in configurable batches
5. **✅ Validation**: Post-import data verification
6. **📈 Statistics**: Import summary and performance metrics

### Supported CSV Formats

#### `pci_dss_controls.csv`
```csv
id,control_id,requirement,chunk,metadata
uuid,1.1.1,"Requirement text","Control content","{\"category\": \"network\"}"
```

#### `aws_config_rules_guidance.csv`
```csv
id,config_rule,chunk,metadata
uuid,ec2-security-group-attached-to-eni,"Rule guidance","{\"compliance\": [\"PCI\"]}"
```

#### `pci_aws_config_rule_mapping.csv`
```csv
id,control_id,config_rules
uuid,1.1.1,"[{\"rule\": \"ec2-security-group-attached-to-eni\", \"weight\": 0.8}]"
```

### Data Validation

- **Required Fields**: Validates presence of mandatory columns
- **Data Types**: UUID, JSON, and text field validation
- **Relationships**: Cross-table relationship integrity
- **Duplicates**: Duplicate detection and handling
- **Size Limits**: Content size and batch size validation

### Error Handling

```bash
# Import with detailed error reporting
python cli.py import-data bulk --verbose

# Common error scenarios:
# - Missing required columns
# - Invalid JSON in metadata fields
# - Duplicate control IDs
# - Connection timeouts
# - Schema mismatches
```

## 🔧 Configuration

### Environment Variables

Create `.env` file in the database directory:

```bash
# Supabase Configuration (Required)
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
SUPABASE_ANON_KEY=your-anon-key

# Optional Configuration
DB_BATCH_SIZE=1000
DB_TIMEOUT=30
DB_RETRY_COUNT=3
DB_POOL_SIZE=10

# Logging Configuration
LOG_LEVEL=INFO
ENABLE_SQL_LOGGING=false
```

### CLI Configuration Options

#### Global Options
- `--verbose, -v`: Enable detailed output
- `--quiet, -q`: Suppress non-essential output
- `--config PATH`: Custom configuration file path

#### Import Options
- `--batch-size INT`: Batch size for imports (default: 1000)
- `--validate/--no-validate`: Enable/disable pre-import validation
- `--progress/--no-progress`: Show/hide progress indicators
- `--source PATH`: Custom CSV source directory

#### Database Options
- `--dry-run`: Preview changes without execution
- `--force`: Force operations without confirmation
- `--timeout INT`: Operation timeout in seconds

### Connection Settings

```python
# Custom connection configuration
from database.auth.connection import DatabaseConnection

# Override default settings
config = {
    'timeout': 60,
    'retry_count': 5,
    'pool_size': 20,
    'max_overflow': 30
}

db = DatabaseConnection(config)
```

## 🐛 Troubleshooting

### Common Issues & Solutions

#### Connection Problems

**Issue**: "Unable to connect to Supabase"
```bash
# 1. Check credentials
python cli.py auth check

# 2. Verify .env file
cat .env | grep SUPABASE

# 3. Test basic connection
python -c "from database.auth.connection import db_connection; print(db_connection.get_client())"
```

**Issue**: "Authentication failed"
```bash
# 1. Regenerate service role key in Supabase dashboard
# 2. Update .env file
# 3. Restart any long-running processes
```

#### Import Failures

**Issue**: "CSV validation failed"
```bash
# 1. Check CSV format and headers
head -5 /path/to/problematic.csv

# 2. Validate specific file
python -m database.importers csv /path/to/file.csv table_name --verbose

# 3. Check for encoding issues
file /path/to/file.csv
```

**Issue**: "Batch import timeout"
```bash
# 1. Reduce batch size
python cli.py import-data bulk --batch-size 500

# 2. Increase timeout
export DB_TIMEOUT=120

# 3. Import individual files
python -m database.importers csv problematic_file.csv table_name
```

#### Schema Issues

**Issue**: "Table doesn't exist"
```bash
# 1. Run migrations
python cli.py db migrate

# 2. Check Supabase dashboard for tables
# 3. Manual table creation if needed
psql -f create_tables_manual.sql
```

**Issue**: "Schema validation failed"
```bash
# 1. Check current schema
python cli.py db migrate --dry-run

# 2. Manual schema inspection
python -c "
from database.repositories import PciControlRepository
repo = PciControlRepository()
print(repo.get_table_info())
"
```

### Debugging Techniques

#### Verbose Mode
```bash
# Enable detailed logging for all operations
python cli.py --verbose [command]

# Specific debug scenarios
python cli.py import-data bulk --verbose  # Import debugging
python cli.py db migrate --verbose        # Migration debugging
```

#### Connection Testing
```bash
# Test connection components
python -c "
from database.auth import db_connection, credential_manager
print('Credentials:', credential_manager.validate())
print('Connection:', db_connection.test_connection())
"
```

#### Data Validation
```bash
# Validate specific data
python -c "
from database.repositories import PciControlRepository
repo = PciControlRepository()
controls = repo.get_all(limit=5)
for control in controls:
    print(f'{control.control_id}: {len(control.chunk)} chars')
"
```

### Performance Issues

#### Slow Imports
```bash
# 1. Increase batch size
python cli.py import-data bulk --batch-size 2000

# 2. Disable validation for known good data
python cli.py import-data bulk --no-validate

# 3. Monitor database performance in Supabase dashboard
```

#### Memory Usage
```bash
# 1. Process files individually for large datasets
for file in *.csv; do
    python -m database.importers csv "$file" table_name
done

# 2. Monitor memory usage
ps aux | grep python
```

## 👥 Development Guide

### Contributing to the Database Module

#### Setting Up Development Environment

```bash
# 1. Clone and navigate to project
cd /path/to/sentinelai-audit-framework/database

# 2. Create development environment
python -m venv dev-env
source dev-env/bin/activate  # or dev-env\Scripts\activate on Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up test database
cp .env.example .env.test
# Edit .env.test with test database credentials

# 5. Run test migrations
python cli.py db migrate --config .env.test
```

#### Repository Pattern Extension

Adding a new repository for custom data types:

```python
# 1. Create model in models/
from dataclasses import dataclass
from typing import Dict, Any
from uuid import UUID

@dataclass
class CustomModel:
    id: UUID
    name: str
    data: Dict[str, Any]
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CustomModel':
        # Implementation
        pass

# 2. Create repository in repositories/
from .base import BaseRepository
from ..models.custom_model import CustomModel

class CustomRepository(BaseRepository):
    def __init__(self):
        super().__init__('custom_table')
    
    def create(self, model: CustomModel) -> CustomModel:
        # Implementation
        pass
    
    def get_by_name(self, name: str) -> CustomModel:
        # Custom query implementation
        pass

# 3. Add to repositories/__init__.py
from .custom_repository import CustomRepository
__all__.append('CustomRepository')

# 4. Create migration for new table
# Add to migrations/create_tables.py
```

#### Testing Strategy

```bash
# Unit tests for individual components
python -m pytest tests/unit/test_repositories.py
python -m pytest tests/unit/test_importers.py

# Integration tests for complete workflows
python -m pytest tests/integration/test_import_workflow.py
python -m pytest tests/integration/test_migration_workflow.py

# Manual testing with development data
python cli.py data seed  # Load test data
python cli.py data list all --limit 3  # Verify data
python cli.py data clear all  # Clean up
```

#### Code Style Guidelines

```python
# Repository method patterns
def get_by_criteria(self, **criteria) -> List[Model]:
    """Get records matching criteria with proper error handling"""
    try:
        # Implementation with proper logging
        self.logger.info(f"Querying {self.table_name} with criteria: {criteria}")
        result = self.client.table(self.table_name).select("*").match(criteria).execute()
        return [Model.from_dict(item) for item in result.data]
    except Exception as e:
        self.logger.error(f"Failed to query {self.table_name}: {str(e)}")
        raise

# Error handling patterns
def safe_operation(self, operation_name: str):
    """Standard error handling wrapper"""
    try:
        # Operation implementation
        self.logger.info(f"Starting {operation_name}")
        result = self._perform_operation()
        self.logger.info(f"Completed {operation_name}")
        return result
    except Exception as e:
        self.logger.error(f"Failed {operation_name}: {str(e)}")
        raise DatabaseError(f"{operation_name} failed: {str(e)}")
```

#### Adding New CLI Commands

```python
# Add to cli.py
@cli.group()
def custom():
    """Custom operations"""
    pass

@custom.command()
@click.option('--param', help='Parameter description')
def new_command(param):
    """New command description"""
    # Implementation
    click.echo(f"Executing with param: {param}")

# Test the new command
python cli.py custom new-command --param value
```

### Performance Optimization

#### Database Query Optimization

```python
# Use proper indexing for common queries
def get_controls_by_category(self, category: str) -> List[PciControl]:
    """Optimized query using GIN index on metadata"""
    return self.client.table(self.table_name).select("*").match({
        "metadata->>control_category": category
    }).execute()

# Batch operations for efficiency
def bulk_insert(self, models: List[Model], batch_size: int = 1000):
    """Efficient bulk insert with batching"""
    for i in range(0, len(models), batch_size):
        batch = models[i:i + batch_size]
        batch_data = [model.to_dict() for model in batch]
        self.client.table(self.table_name).insert(batch_data).execute()
```

#### Memory Management

```python
# Generator patterns for large datasets
def iter_all_controls(self, batch_size: int = 1000):
    """Memory-efficient iteration over all controls"""
    offset = 0
    while True:
        batch = self.get_batch(offset, batch_size)
        if not batch:
            break
        for control in batch:
            yield control
        offset += batch_size

# Usage
for control in repository.iter_all_controls():
    process_control(control)  # Process without loading all into memory
```

## 🔗 Integration Points

### Data Pipeline Integration

The database module integrates seamlessly with the data pipeline:

```bash
# Data pipeline generates CSV files
python -m data_pipeline.processors.compliance_standards.pci_dss.main all

# Database imports generated CSV files
python cli.py import-data bulk --source shared_data/outputs/pci_dss_v4/database_import/

# Verify imported data
python cli.py data stats
```

#### Integration Workflow
1. **Data Pipeline**: Extracts controls from compliance documents
2. **CSV Generation**: Creates database-ready CSV files
3. **Database Import**: Validates and imports CSV data
4. **Repository Access**: Provides clean API for data access
5. **Service Integration**: RAG service queries imported data

### Shared Data Structure

```
shared_data/outputs/
├── pci_dss_v4/
│   ├── controls/              # Individual control files
│   └── database_import/       # CSV files for database import
│       ├── pci_dss_controls.csv
│       └── database_schema.json
├── aws_config_guidance/
│   └── aws_config_rules_guidance.csv
└── configs/
    └── pci_aws_config_rule_mapping.csv
```

### Service Integration

#### RAG Service Integration
```python
# RAG service uses repository pattern for data access
from database.repositories import PciControlRepository

class ComplianceRAG:
    def __init__(self):
        self.pci_repo = PciControlRepository()
    
    def search_controls(self, query: str) -> List[PciControl]:
        return self.pci_repo.search_by_content(query)
```

#### Evidence Collection Integration
```python
# Evidence collection stores findings in database
from database.repositories import BaseRepository

class EvidenceRepository(BaseRepository):
    def store_evidence(self, control_id: str, evidence: Dict):
        # Store compliance evidence linked to controls
        pass
```

### AWS Integration

#### Config Rule Mapping
```python
# Query AWS Config rules for PCI controls
from database.repositories import PciAwsConfigMappingRepository

mapping_repo = PciAwsConfigMappingRepository()
aws_rules = mapping_repo.get_rules_for_control("1.1.1")

# Use in AWS Config evaluation
for rule in aws_rules:
    evaluate_aws_config_rule(rule['rule'], rule['parameters'])
```

#### Cross-Service Data Flow
```
Data Pipeline → CSV Files → Database Import → Repository Layer → Services
     ↓              ↓             ↓              ↓               ↓
PCI Extractor → pci_controls.csv → Bulk Import → PciControlRepo → RAG Service
AWS Processor → aws_rules.csv → CSV Import → AwsConfigRepo → Config Evaluator
Mapping Gen → mappings.csv → Validation → MappingRepo → Evidence Collector
```

## 📈 Performance & Scaling

### Batch Processing Optimization

#### Import Performance
```bash
# Optimal batch sizes for different scenarios
python cli.py import-data bulk --batch-size 500   # Conservative (reliable)
python cli.py import-data bulk --batch-size 1000  # Default (balanced)
python cli.py import-data bulk --batch-size 2000  # Aggressive (fast)

# Monitor performance
time python cli.py import-data bulk --verbose
```

#### Memory Usage Guidelines
- **Small datasets** (<1000 records): Default batch size (1000)
- **Medium datasets** (1000-10000 records): Batch size 500-1000
- **Large datasets** (>10000 records): Batch size 200-500
- **Memory constrained**: Use streaming import with individual files

### Database Optimization

#### Index Strategy
```sql
-- Primary indexes for fast lookups
CREATE UNIQUE INDEX idx_control_id ON pci_dss_controls (control_id);
CREATE UNIQUE INDEX idx_config_rule ON aws_config_rules_guidance (config_rule);

-- GIN indexes for JSON queries
CREATE INDEX idx_metadata_gin ON pci_dss_controls USING GIN (metadata);
CREATE INDEX idx_config_rules_gin ON pci_aws_config_rule_mappings USING GIN (config_rules);

-- Composite indexes for common query patterns
CREATE INDEX idx_control_category ON pci_dss_controls ((metadata->>'control_category'));
CREATE INDEX idx_requirements_id ON pci_dss_controls ((metadata->>'requirements_id'));
```

#### Query Performance
```python
# Efficient JSONB queries
def get_controls_by_requirement(self, req_id: str) -> List[PciControl]:
    """Use JSONB operator for fast metadata queries"""
    result = self.client.table('pci_dss_controls').select("*").match({
        "metadata->>requirements_id": req_id
    }).execute()
    return [PciControl.from_dict(item) for item in result.data]

# Avoid full table scans
def search_controls_efficiently(self, term: str) -> List[PciControl]:
    """Use full-text search instead of ILIKE when possible"""
    result = self.client.table('pci_dss_controls').select("*").text_search(
        'chunk', term
    ).execute()
    return [PciControl.from_dict(item) for item in result.data]
```

### Monitoring & Metrics

#### Performance Monitoring
```bash
# Import performance tracking
python cli.py import-data bulk --verbose 2>&1 | grep -E "(Progress|Imported)"

# Database connection monitoring
python -c "
from database.auth.connection import db_connection
print(f'Active connections: {db_connection.get_connection_count()}')
print(f'Health status: {db_connection.check_health()}')
"
```

#### Key Metrics to Monitor
- **Import Speed**: Records per second during bulk imports
- **Connection Health**: Active connections and timeouts
- **Query Performance**: Response times for common queries
- **Memory Usage**: Peak memory during large operations
- **Error Rates**: Failed operations and retry counts

### Scaling Considerations

#### Horizontal Scaling
- **Read Replicas**: Use Supabase read replicas for query scaling
- **Connection Pooling**: Configure appropriate pool sizes
- **Caching**: Implement repository-level caching for frequent queries

#### Vertical Scaling
- **Batch Size Tuning**: Optimize batch sizes for available memory
- **Index Optimization**: Monitor and optimize index usage
- **Query Optimization**: Use EXPLAIN ANALYZE for slow queries

#### Best Practices
- Monitor Supabase dashboard for performance metrics
- Use connection pooling for high-concurrency scenarios
- Implement retry logic with exponential backoff
- Cache frequently accessed data at the repository level
- Use bulk operations for large data manipulations

---

## 🤝 Support & Resources

For issues, questions, or contributions:

1. **Check CLI Help**: `python cli.py --help` for command reference
2. **Verbose Mode**: Use `--verbose` flag for detailed debugging information
3. **Authentication**: Verify Supabase credentials with `python cli.py auth check`
4. **Repository Patterns**: Review existing repositories for implementation examples
5. **Integration Examples**: Check data pipeline integration workflows

### Additional Resources

- **Supabase Documentation**: [supabase.com/docs](https://supabase.com/docs)
- **Repository Pattern**: Clean architecture data access patterns
- **CLI Framework**: Click library for command-line interfaces
- **Performance Optimization**: PostgreSQL query optimization techniques

---

**Happy Database Managing! 🗃️**