# PCI DSS Control Extraction Service

## Overview

The PCI DSS Control Extraction service provides a **modular, maintainable architecture** for extracting PCI DSS v4.0.1 compliance controls from markdown documents into structured formats optimized for RAG ingestion and vector search.

## 🎉 **Extraction Results**
- **✅ 256 controls extracted** with token-based analysis
- **✅ 25 appendix controls** (A1, A2, A3 requirements)
- **✅ Multiple output formats**: Markdown (human), JSON (validation), JSON (production)
- **✅ Quality scoring**: 0-100 quality metrics per control
- **✅ CSV generation**: Ready for Bedrock Knowledge Base

## Quick Start

### Prerequisites
- Python 3.9+
- pip

### Installation
```bash
make install
```

### Extract Controls (New Modular Architecture)
```bash
# Complete workflow (recommended)
python -m extractors.pci_dss_v4_0_1.main all

# Or step by step:
python -m extractors.pci_dss_v4_0_1.main extract  # Extract controls
python -m extractors.pci_dss_v4_0_1.main csv      # Generate CSV for Bedrock

# With custom parameters
python -m extractors.pci_dss_v4_0_1.main extract --verbose --output-dir /tmp/controls
python -m extractors.pci_dss_v4_0_1.main csv --chunk-size 400
```

## Directory Structure

```
rag_service/
├── extractors/                     # 🎯 Modular extraction framework
│   ├── __init__.py                      # Framework-level interface
│   └── pci_dss_v4_0_1/                 # PCI DSS v4.0.1 specific extractor
│       ├── main.py                      # CLI entry point
│       ├── README.md                    # Comprehensive documentation
│       ├── example_usage.py             # Usage examples
│       ├── __init__.py                  # Module interface
│       └── core/                        # Modular components
│           ├── __init__.py
│           ├── extractor.py             # Core orchestration (~350 lines)
│           ├── text_processors.py      # Text cleaning & parsing
│           ├── content_builders.py     # Content assembly & formatting
│           ├── metadata_generators.py  # Validation & production metadata
│           └── bedrock_csv_generator.py # CSV generation for Bedrock
│
├── data/                           # 📊 Input data and summaries
│   ├── PCI-DSS-v4_0_1-FULL.md          # Source document
│   └── EXTRACTION_SUMMARY.md           # Extraction results summary
│
├── docs/                           # 📖 Documentation
│   └── ARCHITECTURE_SUMMARY.md         # Architecture overview
│
├── extracted_controls/             # 📋 Generated control outputs
│   ├── control_*.md                     # Human-readable markdown
│   ├── control_*.json                   # Machine-readable JSON
│   └── (256 controls × 2 formats)
│
├── ingest/                         # 📥 Data processing pipelines
│   └── bedrock/                         # Bedrock Knowledge Base ready files
│
├── notebooks/                      # 📓 Analysis and development notebooks
├── utils/                          # 🛠️ Utility scripts (legacy)
├── archive/                        # 📦 Legacy code (preserved)
├── README.md                       # 📖 This file
├── Makefile                        # 🔧 Build automation
├── requirements.txt                # 📦 Core dependencies
├── requirements-dev.txt            # 📦 Development dependencies
└── pytest.ini                     # 🧪 Testing configuration
```

## Development Guide

### Setup Development Environment
```bash
make install-dev
```

### Running Tests
```bash
make test
```

### Code Quality
```bash
make lint
make format
```

## Modular Architecture

### Core Design Principles
- **Single Responsibility**: Each module has a clear, focused purpose
- **Testability**: Individual components can be tested in isolation
- **Maintainability**: Easy to modify and extend specific functionality
- **Token-aware**: Optimized for embedding generation and vector search

### Component Overview

#### **1. Main Entry Point (`main.py`)**
CLI interface for all extraction operations:
```bash
python -m extractors.pci_dss_v4_0_1.main extract    # Extract controls
python -m extractors.pci_dss_v4_0_1.main csv        # Generate CSV
python -m extractors.pci_dss_v4_0_1.main all        # Complete workflow
python -m extractors.pci_dss_v4_0_1.main --help     # Show help
```

#### **2. Core Orchestration (`core/extractor.py`)**
- Central coordinator (reduced from 853 → ~350 lines)
- Document loading and control detection
- Workflow orchestration without monolithic complexity

#### **3. Text Processing (`core/text_processors.py`)**
- `TextProcessor`: HTML cleaning, whitespace normalization
- `ControlIDDetector`: Pattern matching (1.2.3, A1.2.3, etc.)
- `SectionExtractor`: Testing procedures and guidance extraction

#### **4. Content Building (`core/content_builders.py`)**
- `ControlContentBuilder`: Assembles complete control content
- `MarkdownFormatter`: Consistent markdown formatting
- Structured output optimized for vector search

#### **5. Metadata Generation (`core/metadata_generators.py`)**
- `ValidationMetadataGenerator`: Quality scoring (0-100) with debugging
- `ProductionMetadataGenerator`: Database/vector search ready metadata
- `MetadataFileManager`: Consistent file I/O operations

#### **6. CSV Generation (`core/bedrock_csv_generator.py`)**
- `BedrockCSVGenerator`: Token-aware chunking for Knowledge Base
- Smart chunking that respects content boundaries
- Quality score integration and source references

## Usage Examples

### Basic Extraction
```python
from extractors.pci_dss_v4_0_1.core import ControlExtractor

# Initialize and run extraction
extractor = ControlExtractor("data/PCI-DSS-v4_0_1-FULL.md")
extractor.load_markdown()
extractor.extract_all_controls()
extractor.save_controls("extracted_controls")

# Print summary
extractor.print_summary()
```

### Component-Level Usage
```python
from extractors.pci_dss_v4_0_1.core import (
    TextProcessor, 
    ControlContentBuilder,
    ValidationMetadataGenerator
)

# Use individual components
processor = TextProcessor()
builder = ControlContentBuilder()
metadata_gen = ValidationMetadataGenerator()

# Process text through pipeline
cleaned_text = processor.clean_html(raw_text)
control_content = builder.build_control_content(control_data)
metadata = metadata_gen.generate_metadata(control_content)
```

### CSV Generation for Bedrock
```python
from extractors.pci_dss_v4_0_1.core import BedrockCSVGenerator

# Generate CSV for Bedrock Knowledge Base
generator = BedrockCSVGenerator(controls_dir="extracted_controls")
generator.generate_bedrock_files()
```

## Output Formats

### 1. **Markdown Files** (`.md`)
Human-readable format optimized for review:
```markdown
Control 1.2.8

Defined Approach Requirements:
[Main requirement content]

Testing Procedures:
[Testing procedure content]

Guidance:
[Purpose, Examples, Good Practice]
```

### 2. **Validation JSON** (`.json`)
Development format with quality metrics:
```json
{
  "control_id": "1.2.8",
  "content": "...",
  "quality_score": 95,
  "token_count": 245,
  "debug_info": {...}
}
```

### 3. **Production JSON** (`.prod.json`)
Database-ready format:
```json
{
  "control_id": "1.2.8",
  "content": "...",
  "metadata": {
    "framework": "PCI_DSS_v4_0_1",
    "section": "Authentication",
    "token_count": 245
  }
}
```

### 4. **CSV Files** (Bedrock Ready)
Token-aware chunks for Knowledge Base ingestion with quality scores and source references.

## Migration from Legacy

### What Changed ✅
- **853-line monolith** → **6 focused modules** (~350 lines each)
- **Single entry point** → **CLI interface with commands**
- **Basic output** → **Multiple formats with quality scoring**
- **Character-based** → **Token-based analysis**

### What Stayed ✅
- All extraction logic preserved
- Output quality maintained
- Existing extracted_controls/ directory compatible
- Same high-quality results with better maintainability

## Architecture Benefits

1. **📈 Maintainability**: Clear separation of concerns
2. **🧪 Testability**: Individual components can be unit tested  
3. **📚 Documentation**: Comprehensive docs for team collaboration
4. **🚀 Extensibility**: Easy to add new frameworks or modify logic
5. **💡 Developer Experience**: Clear workflows and examples
6. **🎯 Quality**: Token-based analysis and quality scoring
7. **🔗 Integration**: Ready for Bedrock Knowledge Base and vector search

**Ready for production use and team collaboration!** 🎉 