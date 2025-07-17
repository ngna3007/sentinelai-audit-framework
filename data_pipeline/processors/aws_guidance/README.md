# AWS Config Rules Guidance Processor

This module processes AWS Config Rules guidance data into database-friendly formats for compliance management and RAG applications.

## Overview

The AWS Config Rules guidance processor takes AWS Config rule mappings and transforms them into a structured format suitable for database import and RAG applications. It handles:

- Processing AWS Config rule descriptions and guidance
- Generating database-friendly CSV files
- Creating metadata for efficient querying
- Providing PostgreSQL schema definitions
- Processing PCI DSS to AWS Config rule mappings

## Directory Structure

```
aws_guidance/
├── core/
│   ├── __init__.py
│   ├── database_data_generator.py   # Main data processing logic
│   ├── content_processor.py         # Content processing utilities
│   ├── metadata_generators.py       # Metadata generation
│   └── text_processors.py          # Text processing utilities
├── pci_mapping/
│   ├── __init__.py
│   ├── process_pci_mapping.py      # PCI DSS to AWS Config mapping processor
│   └── examples/                   # Usage examples
├── examples/
│   └── database_import_example.py   # Usage examples
├── adapter.py                       # Pipeline integration adapter
└── README.md                        # This documentation
```

## Features

- **Database-Friendly Format**: Generates CSV files optimized for PostgreSQL import
- **Metadata Generation**: Creates structured metadata for efficient querying
- **Content Processing**: Combines rule descriptions and guidance into meaningful chunks
- **Pipeline Integration**: Seamlessly integrates with the centralized data pipeline
- **PCI DSS Mapping**: Processes PCI DSS control to AWS Config rule mappings
- **Multiple PDF Conversion Engines**: Support for both pymupdf4llm and docling engines
- **Advanced Document Processing**: Docling engine provides superior layout analysis and table detection

## Usage

### Command Line Interface

**Note**: The CLI paths have been updated to use the centralized data pipeline CLI.

```bash
# Process AWS Config rules with default settings
python data_pipeline/cli.py aws-guidance process --verbose

# Process custom input file
python data_pipeline/cli.py aws-guidance process --input-file custom.csv --output-dir custom/output

# Process PCI DSS to AWS Config rule mappings
python data_pipeline/cli.py aws-guidance pci-mappings --verbose

# Process custom PCI mapping file
python data_pipeline/cli.py aws-guidance pci-mappings --input-file custom.json --output-dir custom/output
```

### Python API

```python
from data_pipeline.processors.aws_guidance.adapter import AWSGuidancePipelineAdapter

# Initialize adapter
adapter = AWSGuidancePipelineAdapter()

# Process config rules
result = adapter.process_config_rules(
    input_file="path/to/rules.csv",
    output_dir="path/to/output"
)

# Process PCI DSS mappings
result = adapter.process_pci_mappings(
    input_file="path/to/mappings.json",
    output_dir="path/to/output"
)

if result.success:
    print(f"Generated {result.total_files} files")
```

## Output Structure

The processor generates the following files in the output directory:

```
database_import/
├── aws_config_rules.csv          # Main AWS Config rules data file
└── database_schema.json          # PostgreSQL schema definition

pci_aws_config_rule_mapping/
├── pci_aws_config_rule_mapping.csv    # PCI DSS to AWS Config mappings
├── pci_aws_config_rule_mapping_stats.json  # Processing statistics
└── database_schema.json              # PostgreSQL schema definition
```

### CSV Format

The AWS Config rules CSV file contains:
- `id`: UUID primary key
- `config_rule`: AWS Config rule name
- `chunk`: Combined rule description and guidance
- `metadata`: JSON object with additional data

The PCI mapping CSV file contains:
- `id`: UUID primary key
- `control_id`: PCI DSS control identifier
- `config_rules`: JSONB array of AWS Config rules and guidance

### Database Schema

The PostgreSQL schema includes:

- Primary key on UUID
- GIN index for JSON metadata
- Full text search capabilities
- Efficient querying support
- JSONB arrays for rule mappings

## PDF Conversion Engines

The system supports two PDF conversion engines for processing compliance documents:

### PyMuPDF4LLM (Default)
- **Speed**: Fast conversion (~2 minutes for large documents)
- **Optimization**: Specifically designed for LLM applications
- **Use Case**: Quick conversions and standard document processing
- **Installation**: `pip install pymupdf4llm`

### Docling (Advanced)
- **Quality**: Superior layout analysis and table detection
- **Features**: Advanced PDF understanding, reading order detection
- **Performance**: Slower processing (~13 minutes for large documents)
- **Use Case**: Complex compliance documents requiring high-quality extraction
- **Installation**: `pip install docling`

### Engine Selection

You can choose the conversion engine when processing PCI DSS documents:

```bash
# Use pymupdf4llm (default, fast)
python data_pipeline/processors/compliance_standards/pci_dss/main.py convert --engine pymupdf4llm

# Use docling (advanced, higher quality)
python data_pipeline/processors/compliance_standards/pci_dss/main.py convert --engine docling

# Manual input with docling
python data_pipeline/processors/compliance_standards/pci_dss/main.py convert --engine docling --source-path /path/to/document.pdf --output-file custom-name --output-folder /custom/output/
```

### Engine Comparison

| Feature | PyMuPDF4LLM | Docling | Recommendation |
|---------|-------------|---------|----------------|
| **Speed** | ~2 minutes | ~13 minutes | PyMuPDF4LLM |
| **Table Detection** | Basic | 6,161+ markers | **Docling** |
| **Header Structure** | Good | Excellent (119+ headers) | **Docling** |
| **Layout Analysis** | Standard | Advanced | **Docling** |
| **Quality** | Good | Excellent | **Docling** |
| **Resource Usage** | Low | High | PyMuPDF4LLM |
| **Compliance Documents** | Suitable | **Optimal** | **Docling** |

### Recommendations

- **For Development/Testing**: Use PyMuPDF4LLM for quick iterations
- **For Production/Compliance**: Use Docling for highest quality extraction
- **For Batch Processing**: Use Docling when processing time is not critical
- **For Real-time Processing**: Use PyMuPDF4LLM for speed requirements

## Development

### Adding New Features

1. Add core processing logic in `core/` or `pci_mapping/`
2. Update adapter.py for pipeline integration
3. Add CLI commands in the centralized CLI (`data_pipeline/cli.py`)
4. Update documentation
5. Test with both PDF conversion engines

### Running Tests

```bash
# Run unit tests
python -m pytest tests/

# Run integration tests
python -m pytest tests/integration/
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

See the main project license file. 