# PCI DSS Control Extractor - Modular Architecture

A modular, well-structured system for extracting PCI DSS controls from markdown and generating CSV files for Bedrock Knowledge Base.

## 🏗️ Architecture Overview

This extractor has been refactored from a monolithic 853-line file into a clean, modular architecture:

```
pci_dss/                        
├── __init__.py                # Module exports
├── adapter.py                 # Adapter to integrate PCI DSS extractor with centralized pipeline.
├── main.py                    # Primary entry point with CLI
├── core/                      # Core extraction modules
│   ├── __init__.py            # Module exports
│   ├── extractor.py           # Main orchestration logic (~350 lines)
│   ├── text_processors.py     # Text cleaning and parsing utilities
│   ├── content_builders.py    # Content assembly and formatting
│   ├── metadata_generators.py # Validation and production metadata
│   ├── csv_generator.py       # CSV generation for database import
│   └── pdf_converter.py       # PDF to markdown conversion
├── examples/example_usage.py  # Usage examples (needs update)
└── README.md                  # This file
```

### Key Benefits

- **🔧 Maintainable**: Each module has a single responsibility
- **🧪 Testable**: Components can be tested independently
- **📚 Readable**: Clear separation of concerns
- **🤝 Collaborative**: Easy for teammates to contribute
- **🔄 Extensible**: New features can be added cleanly

## 🚀 Quick Start

### For End Users

```bash
# Option 1: Run from project root directory (recommended)
cd /path/to/sentinelai-audit-framework

# Run complete workflow (extract + CSV generation)
python -m data_pipeline.processors.compliance_standards.pci_dss.main all

# Or run individual steps
python -m data_pipeline.processors.compliance_standards.pci_dss.main extract    # Extract controls only
python -m data_pipeline.processors.compliance_standards.pci_dss.main csv        # Generate CSV only

# Option 2: Run from pci_dss directory
cd /path/to/sentinelai-audit-framework/data_pipeline/processors/compliance_standards/pci_dss

# Run complete workflow (extract + CSV generation)
python main.py all

# Or run individual steps
python main.py extract    # Extract controls only
python main.py csv        # Generate CSV only
```

### For Development

```bash
# Navigate to the pci_dss directory
cd data_pipeline/processors/compliance_standards/pci_dss

# Run with development options
python main.py all --verbose                         # Detailed output
python main.py extract --output-dir /tmp/controls   # Custom output
python main.py csv --chunk-size 400                 # Custom token size
```

## 📋 Workflow Overview

The extraction process follows these steps:

1. **📄 Load Markdown**: Parse `PCI-DSS-v4_0_1-FULL.md`
2. **📊 Extract Tables**: Identify and parse table structures
3. **🎯 Detect Controls**: Find control IDs and handle continuations
4. **🔗 Build Content**: Assemble complete control content
5. **📝 Generate Metadata**: Create validation and production metadata
6. **💾 Save Files**: Output markdown, JSON, and CSV files
7. **📊 Generate Database Files**: Create single CSV and PostgreSQL schema

### Output Structure

```
shared_data/outputs/pci_dss_v4/controls/
├── control_1.1.1.md                    # Human-readable markdown
├── control_1.1.1_validate.json         # Debugging metadata
├── control_1.1.1_production.json       # Database-ready metadata
└── ... (one set per control)

shared_data/outputs/pci_dss_v4/database_import/
├── pci_dss_controls.csv                # Single CSV for PostgreSQL bulk import
├── database_schema.json                # PostgreSQL table schema & sample queries
├── control_*.csv                       # Optional individual files
└── ... (306 individual CSV files - optional)
```

## 🧩 Module Details

### `main.py` - Entry Point
- **Purpose**: CLI interface and workflow orchestration
- **Features**: Environment validation, error handling, progress reporting
- **Commands**: `extract`, `csv`, `all`

### `core/extractor.py` - Main Orchestrator
- **Purpose**: Coordinates the extraction process
- **Key Methods**: 
  - `load_markdown()`: Parse input file
  - `extract_tables()`: Find table structures
  - `extract_controls_from_tables()`: Complex control detection logic
  - `save_controls()`: Output generation

### `core/text_processors.py` - Text Utilities
- **TextProcessor**: Clean HTML, normalize whitespace
- **ControlIDDetector**: Find control IDs (1.2.3, A1.2.3, etc.)
- **SectionExtractor**: Extract testing procedures, guidance sections

### `core/content_builders.py` - Content Assembly
- **ControlContentBuilder**: Assemble complete control content
- **MarkdownFormatter**: Format for markdown output
- **ProductionContentFormatter**: Extract titles, status, procedures

### `core/metadata_generators.py` - Metadata Creation
- **ValidationMetadataGenerator**: Debugging metadata with quality scores
- **ProductionMetadataGenerator**: Database-ready metadata
- **MetadataFileManager**: File I/O operations

### `core/csv_generator.py` - CSV Export
- **CSVGenerator**: Generate CSV for PostgreSQL database import
- **Features**: Single CSV for bulk import, individual files optional, PostgreSQL schema

## 👥 For Teammates - Contributing

### Getting Started

1. **Understand the Architecture**: Review this README and the module docstrings
2. **Run the Tests**: Ensure everything works in your environment
3. **Make Small Changes**: Start with minor improvements
4. **Test Thoroughly**: Use the validation metadata to verify changes

### Development Workflow

```bash
# 1. Set up environment
cd /path/to/sentinelai-audit-framework
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt

# 2. Run extraction to establish baseline
python -m data_pipeline.processors.compliance_standards.pci_dss.main all --verbose

# 3. Make your changes
# Edit the relevant module in data_pipeline/processors/compliance_standards/pci_dss/core/

# 4. Test your changes
python -m data_pipeline.processors.compliance_standards.pci_dss.main extract --verbose
# Check validation metadata for quality scores

# 5. Verify CSV generation still works
python -m data_pipeline.processors.compliance_standards.pci_dss.main csv --verbose
```

### Common Tasks

#### Adding a New Section Type

1. Update `SectionExtractor.extract_guidance_sections()` in `text_processors.py`
2. Modify `ControlContentBuilder._assemble_final_content()` in `content_builders.py`
3. Update section detection in `SectionExtractor.analyze_control_sections()`

#### Improving Control Detection

1. Modify `ControlIDDetector` methods in `text_processors.py`
2. Update continuation logic in `extractor.py`
3. Test with problematic controls using validation metadata

#### Changing Output Format

1. Update `content_builders.py` for content formatting
2. Modify `metadata_generators.py` for metadata structure
3. Update `csv_generator.py` for CSV format

## 🔧 Configuration Options

### CLI Arguments

```bash
python main.py COMMAND [OPTIONS]

Commands:
  extract     Extract controls from markdown
  csv         Generate CSV (requires extracted controls)
  all         Run complete workflow

Options:
  --input-file PATH       Input markdown file (default: PCI-DSS-v4_0_1-FULL.md)
  --output-dir PATH       Output directory (default: extracted_controls)
  --csv-output PATH       CSV output directory (default: shared_data/outputs/pci_dss_v4/database_import)
  --chunk-size INT        Target chunk size in tokens (default: 300)
  --verbose, -v           Enable detailed output
  --help, -h              Show help message
```

### Environment Variables

```bash
# Optional: Override default paths
export PCI_DSS_INPUT_FILE="/path/to/PCI-DSS-v4_0_1-FULL.md"
export PCI_DSS_OUTPUT_DIR="/path/to/output"
```

## 📊 Quality Metrics

The system generates comprehensive quality metrics for each extracted control:

### Validation Metadata
- **Content Length**: Character and token counts
- **Section Analysis**: Which sections are present
- **Table Information**: Source tables and row counts
- **Quality Score**: 0-100 score based on completeness

### Quality Categories
- **High Quality (80-100%)**: Complete controls with all required sections
- **Medium Quality (60-79%)**: Most sections present, minor issues
- **Low Quality (<60%)**: Missing required sections or very short content

### Common Issues
- "Content too short": Check table extraction
- "Missing required section": Verify section detection logic
- "Many rows extracted": Review filtering logic

## 🐛 Troubleshooting

### Common Problems

#### "PCI-DSS-v4_0_1-FULL.md not found"
```bash
# Ensure you're in the correct directory
cd /path/to/rag_service
ls -la PCI-DSS-v4_0_1-FULL.md  # Should exist

# Or specify custom path
python -m extractors.pci_dss_v4_0_1.main extract --input-file /path/to/file.md
```

#### "No controls extracted"
```bash
# Run with verbose mode to see details
python -m extractors.pci_dss_v4_0_1.main extract --verbose

# Check the validation metadata for clues
cat extracted_controls/control_*_validate.json | head -20
```

#### "CSV generation fails"
```bash
# Ensure controls were extracted first
ls extracted_controls/control_*.md | wc -l  # Should show extracted files

# Run CSV generation separately with verbose output
python -m extractors.pci_dss_v4_0_1.main csv --verbose
```

### Debugging Tips

1. **Use Validation Metadata**: Check quality scores and issues
2. **Enable Verbose Mode**: Get detailed progress information
3. **Check Individual Controls**: Look at specific control files
4. **Review Table Sources**: Use table_sources in validation metadata

## 🔬 Testing Strategy

### Unit Testing
```bash
# Test individual components
python -m pytest tests/unit/test_text_processors.py
python -m pytest tests/unit/test_content_builders.py
```

### Integration Testing
```bash
# Test complete workflow
python -m pytest tests/integration/test_extraction_workflow.py
```

### Manual Testing
```bash
# Test with sample controls
python -c "
from data_pipeline.processors.compliance_standards.pci_dss.core.extractor import ControlExtractor
extractor = ControlExtractor('shared_data/documents/PCI-DSS-v4_0_1-FULL.md')
extractor.load_markdown()
controls = extractor.extract_all_controls()
print(f'Extracted {len(controls)} controls')
"
```

## 🗃️ PostgreSQL Database Setup

### Table Creation
```sql
-- Create the main table
CREATE TABLE pci_dss_controls (
    id UUID PRIMARY KEY NOT NULL,
    control_id VARCHAR(20) UNIQUE NOT NULL,
    chunk TEXT NOT NULL,
    metadata JSONB NOT NULL
);

-- Create GIN index for efficient JSON queries
CREATE INDEX idx_metadata_gin ON pci_dss_controls USING GIN (metadata);

-- Create index for control_id lookups
CREATE INDEX idx_control_id ON pci_dss_controls (control_id);
```

### Data Import
```bash
# Copy CSV data into PostgreSQL
psql -d your_database -c "
COPY pci_dss_controls FROM '/path/to/pci_dss_controls.csv' 
CSV HEADER;
"
```

### Sample Queries
```sql
-- Get all controls for requirement 1
SELECT id, control_id, chunk FROM pci_dss_controls 
WHERE (metadata->>'requirements_id') = '1';

-- Search for controls with testing procedures
SELECT id, control_id, metadata->>'control_category' 
FROM pci_dss_controls 
WHERE (metadata->>'has_testing_procedures')::boolean = true;

-- Full text search in control content
SELECT id, control_id FROM pci_dss_controls 
WHERE chunk ILIKE '%network security%';

-- Get controls by category
SELECT id, control_id, metadata->>'requirements_id'
FROM pci_dss_controls 
WHERE metadata->>'control_category' = 'network_security';

-- Get a specific control by control_id
SELECT * FROM pci_dss_controls 
WHERE control_id = '1.1.1';
```

## 📈 Performance Considerations

### Memory Usage
- **Large Files**: The extractor loads the entire markdown file into memory
- **Optimization**: Consider streaming for files >100MB

### Processing Time
- **Typical Performance**: ~30 seconds for full PCI DSS extraction
- **Bottlenecks**: Table parsing and continuation logic

### Token Counting
- **Accuracy**: Install `tiktoken` for precise token counts
- **Fallback**: Character-based estimation (chars/4) if tiktoken unavailable

### Database Performance
- **Bulk Import**: Single CSV file optimized for PostgreSQL COPY command
- **JSONB Indexing**: GIN index enables fast metadata queries
- **Query Optimization**: Use JSONB operators for efficient filtering

## 🔗 Integration Points

### With PostgreSQL Database
- **Input**: Extracted controls in `shared_data/outputs/pci_dss_v4/controls/`
- **CSV Output**: Ready for bulk import in `shared_data/outputs/pci_dss_v4/database_import/`
- **Import Command**: `COPY pci_dss_controls FROM 'pci_dss_controls.csv' CSV HEADER;`

### With Database Applications
- **Text Field**: Use `chunk` column for content
- **Metadata Fields**: JSONB `metadata` column with `control_id`, `standard`, `source`, etc.
- **Queries**: Use JSONB operators for flexible metadata filtering

### With Testing Framework
- **Validation Metadata**: Use for quality assessment
- **Integration Tests**: Test complete workflow
- **Performance Tests**: Monitor extraction speed

## 📚 Additional Resources

- **Original Implementation**: See `archive/` for comparison
- **Test Suite**: Check `tests/` for comprehensive testing
- **Documentation**: Module docstrings provide detailed API docs
- **Examples**: See `example_usage.py` for code samples

## 🤝 Support

For issues, questions, or contributions:

1. **Check Validation Metadata**: Often contains helpful debugging info
2. **Review Module Docstrings**: Detailed API documentation
3. **Run with `--verbose`**: Get detailed progress information
4. **Check Existing Tests**: Examples of expected behavior

---

**Happy Extracting! 🚀** 