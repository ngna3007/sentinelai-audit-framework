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

## Usage

### Command Line Interface

```bash
# Process AWS Config rules with default settings
python cli.py aws-guidance process --verbose

# Process custom input file
python cli.py aws-guidance process --input-file custom.csv --output-dir custom/output

# Process PCI DSS to AWS Config rule mappings
python cli.py aws-guidance pci-mappings --verbose

# Process custom PCI mapping file
python cli.py aws-guidance pci-mappings --input-file custom.json --output-dir custom/output
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

## Development

### Adding New Features

1. Add core processing logic in `core/` or `pci_mapping/`
2. Update adapter.py for pipeline integration
3. Add CLI commands in cli.py
4. Update documentation

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