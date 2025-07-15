# SentinelAI Data Pipeline

A centralized ETL (Extract, Transform, Load) system for compliance document processing, providing both **structured database processing** and **general RAG/knowledge base preparation**. The system handles compliance frameworks like PCI DSS v4.0.1, AWS Config guidance, and any document that needs to be chunked for vector databases.

## 🏗️ Architecture Overview

### System Components

The SentinelAI Data Pipeline consists of 5 main architectural components:

1. **AWS Auto-Inventory Tool** (`../aws-auto-inventory/`) - AWS resource scanning
2. **Data Pipeline** (`./`) - **Core ETL system for compliance documents** 
3. **Database Layer** (`../database/`) - Supabase integration and persistence
4. **Services** (`../services/`) - RAG, orchestration, and API services
5. **LocalStack Testing** (`../localstack_setup/`) - AWS simulation environment

### 🆕 Dual Processing Architecture

The data pipeline now supports two distinct processing categories:

#### 📊 **DATABASE Processing**
- **Purpose**: Structured document processing for database storage
- **Features**: Regex/logic-heavy extraction, framework-specific processors
- **Use Cases**: Control extraction, compliance mapping, structured data
- **Output**: Database-ready JSON/CSV with rich metadata

#### 🧠 **KNOWLEDGEBASE Processing** 
- **Purpose**: General document processing for RAG and vector databases
- **Features**: Universal chunking, text preprocessing, semantic splitting
- **Use Cases**: Document chunking, vector embeddings, RAG applications
- **Output**: Clean chunks optimized for vector database ingestion

### Data Pipeline Directory Structure

```
data_pipeline/
├── cli.py                          # 🎯 Main CLI interface (RESTRUCTURED)
├── pipelines/                      # Core orchestration
│   └── compliance_pipeline.py      # Main pipeline logic
├── processors/                     # 🔧 Modular processing components
│   ├── pdf_converter/             # Universal PDF conversion
│   │   ├── engines/               # PyMuPDF4LLM & Docling engines
│   │   ├── processors/            # Document-specific processors
│   │   └── universal_converter.py # Main converter orchestrator
│   ├── text_processors/          # Text processing utilities
│   │   ├── general_text_processor.py      # 🆕 General-purpose preprocessing
│   │   ├── aws_guidance/
│   │   └── compliance_standards/pci_dss/
│   ├── chunking/                  # Content chunking and formatting
│   │   ├── general/               # 🆕 General-purpose chunking
│   │   │   ├── recursive_chunking_processor.py
│   │   │   └── semantic_chunking_processor.py  # 🆕 Semantic chunking
│   │   ├── aws_guidance/
│   │   └── compliance_standards/pci_dss/
│   ├── metadata_generators/       # Metadata generation by document type
│   │   ├── aws_guidance/
│   │   └── compliance_standards/pci_dss/
│   ├── output_generators/         # Final output generation
│   │   ├── aws_guidance/
│   │   └── compliance_standards/pci_dss/
│   ├── adapters/                  # Pipeline integration adapters
│   │   ├── pci_dss_adapter.py
│   │   └── aws_guidance_adapter.py
│   ├── utils/                     # Shared utilities
│   └── compliance_standards/      # Framework-specific processors
├── schemas/                       # Data models and validation
│   ├── base.py                   # Foundation schemas
│   └── compliance.py             # Compliance-specific models
├── destinations/                  # Output destinations
├── formatters/                   # Output formatting
├── orchestration/                # Workflow orchestration
└── sources/                      # Input sources
```

### Modular Architecture Benefits

- **🔄 Single Responsibility**: Each module has one focused purpose
- **🧩 Composable**: Components can be mixed and matched
- **🧪 Testable**: Isolated modules are easy to test
- **📈 Scalable**: Add new frameworks without disrupting existing code
- **🔧 Maintainable**: Clear separation of concerns
- **🎯 Dual Purpose**: Supports both structured and RAG processing

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- Required packages (install via requirements files)

### Installation

1. **Install core dependencies:**
   ```bash
   pip install click pydantic PyYAML pathlib
   ```

2. **Install PDF processing engines:**
   ```bash
   # Fast conversion (recommended)
   pip install pymupdf4llm
   
   # Advanced layout analysis (optional)
   pip install docling
   
   # 🆕 Advanced layout analysis with VLM picture annotation (optional)
   pip install "docling[vlm]"
   ```

3. **🆕 Install chunking library:**
   ```bash
   # For recursive chunking and overlap processing
   pip install chonkie
   
   # For semantic chunking (with embedding capabilities)
   pip install "chonkie[semantic,st]"
   ```

4. **Install text processing dependencies:**
   ```bash
   pip install tiktoken spacy nltk
   ```

5. **For AWS integration:**
   ```bash
   pip install boto3
   ```

### Quick Start

**Note:** All commands should be run from the `data_pipeline/` directory:
```bash
cd data_pipeline/
```

1. **Check system status:**
   ```bash
   python cli.py status
   ```

2. **View available command groups:**
   ```bash
   python cli.py --help
   ```

3. **For database processing (structured):**
   ```bash
   python cli.py database --help
   ```

4. **For knowledgebase processing (RAG):**
   ```bash
   python cli.py knowledgebase --help
   ```

## 📖 CLI Reference Guide - NEW STRUCTURE

### 🆕 Main Command Structure

```bash
python cli.py [OPTIONS] COMMAND [ARGS]...
```

**Command Groups:**
- `database` - Structured document processing for database storage
- `knowledgebase` - General document processing for RAG/vector databases  
- `convert` - Document format conversion utilities
- `status` - System status and statistics

### 📊 DATABASE Commands - Structured Processing

Database processing handles framework-specific extraction with regex/logic for structured data storage.

#### **database pci-dss** - PCI DSS Processing

##### **convert** - PDF to Markdown Conversion
```bash
python cli.py database pci-dss convert [OPTIONS]
```

**Options:**
- `--pdf-file TEXT` - Input PDF file (default: shared_data/documents/PCI-DSS-v4_0_1.pdf)
- `--output-file TEXT` - Output markdown file (default: PCI-DSS-v4_0_1-FULL.md)
- `--engine [pymupdf4llm|docling|docling_vlm]` - PDF conversion engine
- `--verbose` - Enable verbose output

**Examples:**
```bash
# Convert with docling engine
python cli.py database pci-dss convert --engine docling --verbose

# 🆕 Convert with VLM picture annotation
python cli.py database pci-dss convert --engine docling_vlm --verbose

# Convert custom PDF with VLM
python cli.py database pci-dss convert \
  --pdf-file /path/to/custom.pdf \
  --output-file custom-output.md \
  --engine docling_vlm
```

##### **extract** - Control Extraction
```bash
python cli.py database pci-dss extract [OPTIONS]
```

**Options:**
- `--input-file TEXT` - Input markdown file (default: PCI-DSS-v4_0_1-FULL.md)
- `--output-dir TEXT` - Output directory (default: shared_data/outputs/pci_dss_v4/controls)
- `--verbose` - Enable verbose output

**Examples:**
```bash
# Extract controls with verbose output
python cli.py database pci-dss extract --verbose

# Extract from custom file
python cli.py database pci-dss extract \
  --input-file custom-document.md \
  --output-dir /path/to/output \
  --verbose
```

##### **csv** - Database-Ready CSV Generation
```bash
python cli.py database pci-dss csv [OPTIONS]
```

**Options:**
- `--input-dir TEXT` - Input directory with extracted controls
- `--output-dir TEXT` - CSV output directory
- `--chunk-size INTEGER` - Target chunk size in tokens (default: 300)
- `--verbose` - Enable verbose output

#### **database aws-guidance** - AWS Config Processing

##### **process** - Process AWS Config Rules
```bash
python cli.py database aws-guidance process [OPTIONS]
```

**Options:**
- `--input-file TEXT` - Input CSV file with AWS Config rules
- `--output-dir TEXT` - Output directory for processed files
- `--verbose` - Enable verbose output

### 🧠 KNOWLEDGEBASE Commands - RAG Processing

Knowledgebase processing handles general document chunking for vector databases and RAG applications.

#### **knowledgebase chunk** - 🆕 Universal Document Chunking

**Description:** Chunk any markdown document using different chunking strategies with the chonkie library. Choose between recursive and semantic chunking approaches.

Available chunking methods:
- **recursive**: Traditional recursive chunking with overlap
- **semantic**: Semantic chunking based on content similarity
- **hybrid**: Hierarchical chunking using docling for document structure

#### **knowledgebase chunk recursive** - Recursive Chunking

**Description:** Chunk documents using recursive chunking with overlap refinement for better context continuity.

```bash
python cli.py knowledgebase chunk recursive [OPTIONS]
```

**Options:**
- `--input-file TEXT` - Input markdown file to chunk **[required]**
- `--output-dir TEXT` - Output directory (default: shared_data/outputs/knowledgebase/chunks)
- `--chunk-size INTEGER` - Target chunk size in tokens (default: 512)
- `--overlap FLOAT` - Overlap percentage between chunks (default: 0.25 = 25%)
- `--source TEXT` - Custom source identifier (defaults to filename)
- `--verbose` - Enable verbose output

**Examples:**
```bash
# Chunk any document with defaults
python cli.py knowledgebase chunk recursive \
  --input-file shared_data/documents/PCI-DSS-v4_0_1-docling.md \
  --verbose

# Custom chunking parameters
python cli.py knowledgebase chunk recursive \
  --input-file /path/to/document.md \
  --chunk-size 1024 \
  --overlap 0.5 \
  --source "Technical_Manual" \
  --verbose
```

#### **knowledgebase chunk semantic** - 🆕 Semantic Chunking

**Description:** Chunk documents using semantic similarity to ensure that related content stays together in the same chunk.

```bash
python cli.py knowledgebase chunk semantic [OPTIONS]
```

**Options:**
- `--input-file TEXT` - Input markdown file to chunk **[required]**
- `--output-dir TEXT` - Output directory (default: shared_data/outputs/knowledgebase/chunks)
- `--chunk-size INTEGER` - Target chunk size in tokens (default: 1024)
- `--threshold FLOAT` - Similarity threshold for semantic chunking (default: 0.5)
- `--embedding-model TEXT` - Embedding model for semantic analysis (default: minishlab/potion-base-8M)
- `--source TEXT` - Custom source identifier (defaults to filename)
- `--verbose` - Enable verbose output

**Examples:**
```bash
# Semantic chunking with defaults
python cli.py knowledgebase chunk semantic \
  --input-file shared_data/documents/PCI-DSS-v4_0_1-docling.md \
  --verbose

# Custom semantic parameters
python cli.py knowledgebase chunk semantic \
  --input-file /path/to/document.md \
  --chunk-size 1024 \
  --threshold 0.7 \
  --source "Technical_Manual" \
  --verbose

# Process ISO27001 document with semantic chunking
python cli.py knowledgebase chunk semantic \
  --input-file iso27001-standard.md \
  --source "ISO27001_Standard" \
  --chunk-size 768 \
  --threshold 0.6 \
  --verbose
```

**Output Format:**
- **CSV**: 5 columns - `chunk_id`, `chunk_index`, `text`, `token_count`, `source`
- **JSON**: Detailed chunk data with metadata
- **Metadata**: Processing statistics and configuration

#### **knowledgebase chunk hybrid** - 🆕 Hierarchical Chunking

**Description:** Chunk documents using hierarchical/hybrid chunking with docling's advanced document structure analysis. Works best with PDF documents.

```bash
python cli.py knowledgebase chunk hybrid [OPTIONS]
```

**Options:**
- `--input-file TEXT` - Input PDF or markdown file to chunk **[required]**
- `--output-dir TEXT` - Output directory (default: shared_data/outputs/knowledgebase/chunks)
- `--chunk-size INTEGER` - Target chunk size in characters (default: 1024)
- `--enable-ocr` - Enable OCR processing for PDFs (default: True)
- `--enable-table-structure` - Enable table structure recognition (default: True)
- `--source TEXT` - Custom source identifier (defaults to filename)
- `--verbose` - Enable verbose output

**Examples:**
```bash
# Hierarchical chunking with PDF (recommended)
python cli.py knowledgebase chunk hybrid \
  --input-file shared_data/documents/PCI-DSS-v4_0_1.pdf \
  --verbose

# Advanced hierarchical chunking with custom settings
python cli.py knowledgebase chunk hybrid \
  --input-file technical-report.pdf \
  --chunk-size 2048 \
  --source "Technical_Manual" \
  --enable-ocr \
  --enable-table-structure \
  --verbose

# Hierarchical chunking with markdown fallback
python cli.py knowledgebase chunk hybrid \
  --input-file document.md \
  --enable-ocr=false \
  --verbose
```

**Key Features:**
- 🏗️ **Document Structure Preservation**: Maintains heading hierarchy and section relationships
- 📊 **Advanced PDF Analysis**: Uses docling's layout analysis for structure detection
- 🔍 **OCR Support**: Extracts text from scanned PDFs and images
- 📋 **Table Structure Recognition**: Detects and preserves table layouts
- 🧭 **Hierarchical Context**: Each chunk includes parent section information
- 📄 **Dual Input Support**: Works with both PDF and markdown files
- 🚀 **Performance Optimized**: Multi-threaded processing with hardware acceleration

**Output Format:**
- **CSV**: 7 columns - `chunk_id`, `chunk_index`, `text`, `token_count`, `source`, `hierarchical_level`, `parent_sections`
- **JSON**: Detailed chunk data with full hierarchical context
- **Metadata**: Processing statistics and structural analysis

#### **knowledgebase embedding** - 🆕 Vector Embedding Generation

**Description:** Generate embeddings from CSV text data using various embedding models including baai/bge-m3. Supports both Chonkie and SentenceTransformers implementations.

```bash
python cli.py knowledgebase embedding [OPTIONS]
```

**Options:**
- `--input-file TEXT` - Input CSV file with text data **[required]**
- `--output-dir TEXT` - Output directory (default: shared_data/outputs/knowledgebase/embeddings)
- `--model-name TEXT` - Embedding model name (default: BAAI/bge-m3)
- `--batch-size INTEGER` - Batch size for processing (default: 32)
- `--use-chonkie` - Use Chonkie embedding implementation (default: True)
- `--verbose` - Enable verbose output

**Examples:**
```bash
# Generate embeddings with default baai/bge-m3 model
python cli.py knowledgebase embedding \
  --input-file chunks.csv \
  --verbose

# Use custom model with SentenceTransformers
python cli.py knowledgebase embedding \
  --input-file data.csv \
  --model-name "sentence-transformers/all-MiniLM-L6-v2" \
  --batch-size 16 \
  --verbose

# Process chunked PCI DSS data
python cli.py knowledgebase embedding \
  --input-file shared_data/outputs/knowledgebase/chunks/PCI-DSS-v4_0_1-docling_chunks.csv \
  --model-name "BAAI/bge-m3" \
  --use-chonkie \
  --verbose
```

**Key Features:**
- 🤖 **Multiple Model Support**: baai/bge-m3, sentence-transformers, custom models
- 🔧 **Dual Implementation**: Chonkie and SentenceTransformers backends
- 📊 **Batch Processing**: Efficient processing with configurable batch sizes
- 🗂️ **Parquet Output**: Preserves vector data in optimized format
- 🧹 **Data Validation**: Automatic filtering of empty/null text entries
- 📈 **Progress Tracking**: Detailed metadata and processing statistics

**Input Requirements:**
- CSV file with a 'text' column containing the text to embed
- Text entries should be non-empty and meaningful

**Output Format:**
- **Parquet**: Original CSV data + 'embedding' column with vector arrays
- **Metadata**: Processing statistics, model information, and configuration

### 🔄 CONVERT Commands - Document Conversion

#### **convert pdf-to-md** - Universal PDF Conversion
```bash
python cli.py convert pdf-to-md [OPTIONS]
```

**Options:**
- `--pdf-file TEXT` - Input PDF file path **[required]**
- `--output-file TEXT` - Output markdown file path
- `--engine [pymupdf4llm|docling|docling_vlm]` - Conversion engine (default: pymupdf4llm)
- `--verbose` - Enable verbose output

**Examples:**
```bash
# Basic conversion
python cli.py convert pdf-to-md --pdf-file document.pdf

# Advanced conversion with docling
python cli.py convert pdf-to-md \
  --pdf-file complex-document.pdf \
  --engine docling \
  --output-file processed-document.md \
  --verbose

# 🆕 VLM-enhanced conversion with picture annotation
python cli.py convert pdf-to-md \
  --pdf-file document.pdf \
  --engine docling_vlm \
  --verbose
```

#### **🆕 convert image-describe** - VLM Image Description
```bash
python cli.py convert image-describe [OPTIONS]
```

**Options:**
- `--image-file TEXT` - Input image file path **[required]**
- `--output-file TEXT` - Output markdown file path (optional)
- `--vision-model [granite_vision|smolvlm]` - Vision Language Model (default: granite_vision)
- `--custom-prompt TEXT` - Custom prompt for image description
- `--verbose` - Enable verbose output

**Examples:**
```bash
# Basic image description
python cli.py convert image-describe --image-file diagram.png

# Custom image description with output file
python cli.py convert image-describe \
  --image-file security-diagram.jpg \
  --output-file diagram-description.md \
  --vision-model granite_vision \
  --custom-prompt "Describe this security architecture diagram focusing on compliance controls"

# Using SmolVLM model
python cli.py convert image-describe \
  --image-file chart.png \
  --vision-model smolvlm \
  --verbose
```

### 📊 SYSTEM Commands

#### **status** - Pipeline Status
```bash
python cli.py status
```

**Sample Output:**
```
📊 Pipeline Status
==============================
🎯 Supported frameworks: 1
   • ComplianceFramework.PCI_DSS_V4

📈 Database Processing Statistics:
PCI_DSS_V4:
   📄 Markdown files: 306
   📋 JSON files: 306
   📊 CSV files: 1
   ⏰ Status: Available

🧠 Knowledgebase Processing:
   📊 Chunk CSV files: 2
   📋 Chunk JSON files: 4
```

## 🔧 Processing Technologies

### PDF Conversion Engines

#### 🚀 PyMuPDF4LLM (Default)
- **Speed**: Fast conversion optimized for LLM processing
- **Features**: Page selection, efficient text extraction
- **Best for**: Quick processing, specific page extraction
- **Output**: LLM-optimized markdown

#### 🎯 Docling (Advanced)
- **Quality**: Superior layout analysis and table detection
- **Features**: Advanced document understanding, structure preservation
- **Best for**: Complex documents, production-quality extraction
- **Output**: High-fidelity document representation

#### 🆕 🤖 Docling VLM (Vision Language Model)
- **Quality**: Superior layout analysis + automated picture annotation
- **Features**: All Docling features + VLM-powered image description
- **Vision Models**: Granite Vision, SmolVLM support
- **Best for**: Documents with diagrams, charts, technical illustrations
- **Output**: Enhanced markdown with detailed image descriptions
- **Requirements**: VLM models downloaded on first use (~1-2GB per model)

### 🆕 Chunking Technology

#### 🔀 Recursive Chunking (Chonkie)
- **Method**: Hierarchical splitting using customizable rules
- **Features**: Semantic boundaries, overlap refinement, token counting
- **Best for**: RAG applications, vector database ingestion, fast processing
- **Configuration**: Adjustable chunk size, overlap percentage, source tagging

#### 🧠 Semantic Chunking (Chonkie) - 🆕 NEW
- **Method**: Embedding-based similarity analysis for content grouping
- **Features**: Semantic coherence, related content preservation, embedding models
- **Best for**: Complex documents, knowledge preservation, context-aware RAG
- **Configuration**: Similarity threshold, embedding model selection, chunk size target

#### 📝 Text Preprocessing
- **Whitespace normalization**: Removes excessive spaces and newlines
- **Artifact removal**: Cleans docling/pandoc conversion artifacts
- **Structure preservation**: Maintains headers and semantic boundaries
- **Token accuracy**: Improves token counting by removing noise

## 📂 Data Flow & File Locations - UPDATED

### Input Locations
- **Source PDFs**: `../shared_data/documents/`
- **Processed Markdown**: Generated dynamically or provided

### 🆕 Output Structure
```
../shared_data/outputs/
├── pci_dss_v4/                    # DATABASE processing outputs
│   ├── controls/                  # Individual control JSON files
│   │   ├── control_1.1.1_production.json
│   │   ├── control_1.1.2_production.json
│   │   └── ... (306 controls)
│   ├── bedrock/                   # AWS Bedrock Knowledge Base CSVs
│   │   ├── pci_dss_controls.csv
│   │   └── csv_metadata_template.json
│   └── database_import/           # PostgreSQL bulk import files
│       ├── pci_controls.csv
│       └── schema.sql
├── aws_config_guidance/           # DATABASE processing outputs
│   ├── processed_data/
│   │   └── aws_config_rule_full_mapping.csv
│   └── database_import/
├── knowledgebase/                 # 🆕 KNOWLEDGEBASE processing outputs
│   ├── chunks/                    # General document chunks
│   │   ├── document-name_chunks.csv
│   │   ├── document-name_chunks.json
│   │   └── document-name_metadata.json
│   └── embeddings/                # 🆕 Vector embeddings
│       ├── document-name_embeddings.parquet
│       └── document-name_embedding_metadata.json
└── configs/                       # Configuration outputs
```

## 🛠️ Common Workflows - UPDATED

### 1. 📊 Database Processing Workflow

#### Process PCI DSS for Database Storage
```bash
# Complete PCI DSS workflow
python cli.py database pci-dss convert --engine docling --verbose
python cli.py database pci-dss extract --verbose
python cli.py database pci-dss csv --verbose

# Check results
python cli.py status
```

#### Process AWS Guidance for Database
```bash
# Process AWS Config guidance
python cli.py database aws-guidance process --verbose
```

### 2. 🧠 Knowledgebase Processing Workflow

#### Chunk Documents for RAG/Vector Database
```bash
# Chunk PCI DSS document with recursive chunking
python cli.py knowledgebase chunk recursive \
  --input-file shared_data/documents/PCI-DSS-v4_0_1-docling.md \
  --source "PCI_DSS_v4" \
  --verbose

# Chunk PCI DSS document with semantic chunking
python cli.py knowledgebase chunk semantic \
  --input-file shared_data/documents/PCI-DSS-v4_0_1-docling.md \
  --source "PCI_DSS_v4" \
  --verbose

# Chunk PCI DSS document with hierarchical chunking (recommended for PDFs)
python cli.py knowledgebase chunk hybrid \
  --input-file shared_data/documents/PCI-DSS-v4_0_1.pdf \
  --source "PCI_DSS_v4_Hierarchical" \
  --chunk-size 1024 \
  --enable-ocr \
  --enable-table-structure \
  --verbose

# Chunk any compliance document with semantic chunking
python cli.py knowledgebase chunk semantic \
  --input-file /path/to/iso27001.md \
  --source "ISO27001" \
  --chunk-size 1024 \
  --threshold 0.7 \
  --verbose

# Chunk technical documentation with recursive chunking
python cli.py knowledgebase chunk recursive \
  --input-file technical-manual.md \
  --source "Tech_Manual" \
  --chunk-size 768 \
  --overlap 0.3 \
  --verbose

# Generate embeddings from chunked data
python cli.py knowledgebase embedding \
  --input-file shared_data/outputs/knowledgebase/chunks/document_chunks.csv \
  --model-name "BAAI/bge-m3" \
  --verbose
```

### 3. 🔄 Hybrid Workflow

#### Process Document for Both Database and RAG
```bash
# Step 1: Convert PDF
python cli.py convert pdf-to-md \
  --pdf-file document.pdf \
  --engine docling \
  --verbose

# Step 2: Database processing (if compliance framework)
python cli.py database pci-dss extract \
  --input-file document.md \
  --verbose

# Step 3: Knowledgebase processing (for RAG) - Choose chunking method
python cli.py knowledgebase chunk recursive \
  --input-file document.md \
  --source "Compliance_Doc" \
  --verbose

# OR use semantic chunking for better context preservation
python cli.py knowledgebase chunk semantic \
  --input-file document.md \
  --source "Compliance_Doc" \
  --verbose

# OR use hierarchical chunking for best structure preservation (recommended for PDFs)
python cli.py knowledgebase chunk hybrid \
  --input-file document.pdf \
  --source "Compliance_Doc" \
  --verbose

# Step 4: Generate embeddings for vector database
python cli.py knowledgebase embedding \
  --input-file shared_data/outputs/knowledgebase/chunks/document_chunks.csv \
  --model-name "BAAI/bge-m3" \
  --verbose

# Check status
python cli.py status
```

### 4. 📈 Performance Optimization

#### Chunk Size Optimization for Different Use Cases
```bash
# For short context RAG (faster retrieval) - Recursive
python cli.py knowledgebase chunk recursive \
  --input-file document.md \
  --chunk-size 256 \
  --overlap 0.2

# For long context RAG (more comprehensive) - Semantic
python cli.py knowledgebase chunk semantic \
  --input-file document.md \
  --chunk-size 1024 \
  --threshold 0.6

# For balanced approach - Recursive
python cli.py knowledgebase chunk recursive \
  --input-file document.md \
  --chunk-size 512 \
  --overlap 0.25

# For semantic coherence - Semantic chunking
python cli.py knowledgebase chunk semantic \
  --input-file document.md \
  --chunk-size 768 \
  --threshold 0.5

# For structural coherence - Hierarchical chunking (best for PDFs)
python cli.py knowledgebase chunk hybrid \
  --input-file document.pdf \
  --chunk-size 1024 \
  --enable-ocr \
  --enable-table-structure
```

## 📈 Performance & Quality Metrics - UPDATED

### Expected Output Volumes

#### Database Processing
- **PCI DSS v4.0.1**: 306 controls across 12 requirements
- **Processing Time**: 2-5 minutes for complete workflow
- **Quality Score**: Target 95%+ for validation

#### Knowledgebase Processing
- **Chunk Count**: Varies by document size and chunk settings
- **Token Efficiency**: 34.6% reduction through preprocessing
- **Processing Time**: 1-3 minutes for large documents
- **Chunk Quality**: Semantic boundaries with overlap refinement

### 🆕 Chunking Quality Indicators
- ✅ **Accurate token counting** - 45% size reduction through preprocessing
- ✅ **Semantic boundaries** - Hierarchical recursive splitting
- ✅ **Context overlap** - Configurable overlap for better RAG performance (recursive)
- ✅ **🆕 Semantic coherence** - Embedding-based content grouping (semantic)
- ✅ **🆕 Related content preservation** - Similarity-based chunk boundaries
- ✅ **Clean output** - 5-column CSV format optimized for vector databases
- ✅ **Source tagging** - Custom source identification for multi-document systems

### Quality Indicators
- ✅ **306 controls extracted** - Complete PCI DSS coverage
- ✅ **Multi-table handling** - Complex control structures processed
- ✅ **Metadata generation** - Rich metadata for each control
- ✅ **Universal chunking** - Any document type supported
- ✅ **Preprocessing optimization** - Improved token accuracy

## 🚨 Troubleshooting - UPDATED

### Common Issues & Solutions

#### **Chonkie Installation Issues**
```bash
# Error: chonkie not available
# Solution: Install chonkie library
pip install chonkie

# For semantic chunking capabilities
pip install "chonkie[semantic,st]"

# For full features
pip install chonkie[all]
```

#### **Import Errors**
```bash
# Error: ModuleNotFoundError
# Solution: Check Python path and install dependencies
pip install -r requirements.txt
export PYTHONPATH="${PYTHONPATH}:/path/to/sentinelai-audit-framework"
```

#### **PDF Conversion Failures**
```bash
# Try alternative engine
python cli.py convert pdf-to-md \
  --pdf-file problematic.pdf \
  --engine docling \
  --verbose

# Check file permissions and format
file /path/to/document.pdf
```

#### **🆕 VLM-Related Issues**
```bash
# Error: VLM not available
# Solution: Install docling with VLM support
pip install "docling[vlm]"

# Error: VLM model download timeout
# Solution: Ensure stable internet connection and sufficient disk space
# VLM models are ~1-2GB and downloaded on first use

# Error: Authentication error with HuggingFace
# Solution: Set up HuggingFace token if accessing gated models
export HUGGINGFACE_TOKEN="your_token_here"

# Error: VLM processing too slow
# Solution: Use CPU-only mode or smaller models
python cli.py convert pdf-to-md \
  --pdf-file document.pdf \
  --engine docling \
  --verbose  # Use regular docling if VLM is not needed

# Image description not working
# Solution: Check if VLM is properly configured
python -c "from processors.pdf_converter.engines.docling_vlm_engine import DoclingVLMEngine; print(f'VLM Available: {DoclingVLMEngine.is_vlm_available()}')"
```

#### **Chunking Quality Issues**
```bash
# Check preprocessing effectiveness with recursive chunking
python cli.py knowledgebase chunk recursive \
  --input-file document.md \
  --verbose

# Try different chunk sizes with recursive chunking
python cli.py knowledgebase chunk recursive \
  --input-file document.md \
  --chunk-size 768 \
  --overlap 0.3 \
  --verbose

# Try semantic chunking for better content coherence
python cli.py knowledgebase chunk semantic \
  --input-file document.md \
  --chunk-size 1024 \
  --threshold 0.6 \
  --verbose

# Try hierarchical chunking for best document structure preservation
python cli.py knowledgebase chunk hybrid \
  --input-file document.pdf \
  --chunk-size 1024 \
  --enable-ocr \
  --enable-table-structure \
  --verbose

# Semantic chunking with different embedding models
python cli.py knowledgebase chunk semantic \
  --input-file document.md \
  --embedding-model "sentence-transformers/all-MiniLM-L6-v2" \
  --verbose
```

#### **Low Control Count (Database Processing)**
```bash
# Re-run with verbose mode to see issues
python cli.py database pci-dss extract --verbose

# Validate PDF conversion quality first
python cli.py convert pdf-to-md \
  --pdf-file source.pdf \
  --engine docling \
  --verbose
```

#### **Embedding Issues**
```bash
# Missing dependencies
pip install 'chonkie[semantic,st]' sentence-transformers

# Test embedding processor
python -c "from processors.embedding.embedding_processor import EmbeddingProcessor; print('✅ Import successful')"

# Memory issues with large models
python cli.py knowledgebase embedding \
  --input-file data.csv \
  --model-name "sentence-transformers/all-MiniLM-L6-v2" \
  --batch-size 16 \
  --verbose

# Try different implementations
python cli.py knowledgebase embedding \
  --input-file data.csv \
  --use-chonkie \
  --verbose

# Check GPU availability for faster processing
python -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}')"
```

### Debug Mode
Enable verbose output for detailed troubleshooting:
```bash
# Database processing
python cli.py database pci-dss extract --verbose

# Knowledgebase processing - Recursive
python cli.py knowledgebase chunk recursive --input-file document.md --verbose

# Knowledgebase processing - Semantic
python cli.py knowledgebase chunk semantic --input-file document.md --verbose

# Knowledgebase processing - Embeddings
python cli.py knowledgebase embedding --input-file data.csv --verbose
```

## 🔮 Roadmap - UPDATED

### Currently Supported
- ✅ PCI DSS v4.0.1 (306 controls) - Database processing
- ✅ AWS Config Rules guidance - Database processing
- ✅ Universal PDF conversion (PyMuPDF4LLM + Docling)
- ✅ 🆕 **General document chunking** - Knowledgebase processing
- ✅ 🆕 **Recursive chunking with overlap** - RAG optimization
- ✅ 🆕 **Semantic chunking with embeddings** - Advanced content coherence
- ✅ 🆕 **Hierarchical chunking with docling** - Document structure preservation
- ✅ 🆕 **Text preprocessing and artifact removal**
- ✅ 🆕 **Vector embedding generation** - Knowledgebase processing with baai/bge-m3
- ✅ PostgreSQL database integration
- ✅ Vector database CSV format

### Planned Additions
- 📋 **Semantic search integration** - RAG enhancements
- 📋 ISO 27001 processor - Database processing
- 📋 NIST Cybersecurity Framework - Database processing
- 📋 SOC 2 Type II controls - Database processing
- 📋 Advanced NLP processing
- 📋 Multi-language document support
- 📋 **Batch processing for multiple documents**

## 🤝 Contributing - UPDATED

This system follows modular architecture principles:

### For Database Processing
1. **Add new frameworks** in `processors/compliance_standards/`
2. **Create adapters** in `processors/adapters/` for integration
3. **Add CLI commands** in the `database` command group

### For Knowledgebase Processing
1. **Extend chunking methods** in `processors/chunking/general/`
2. **Add preprocessing** in `processors/text_processors/general_text_processor.py`
3. **Add CLI commands** in the `knowledgebase` command group

### General Guidelines
4. **Extend PDF engines** in `processors/pdf_converter/engines/`
5. **Follow typing standards** and import conventions
6. **Test CLI integration** with new command structure
7. **Update documentation** for new features

## 📞 Support

For questions or issues:
1. Check this README for common solutions
2. Run commands with `--verbose` for detailed output
3. Use `python cli.py status` to check system health
4. Review output files in `../shared_data/outputs/` for results
5. 🆕 Check both `database` and `knowledgebase` processing outputs

### Command Structure Quick Reference
```bash
# Database processing (structured)
python cli.py database [framework] [operation]

# Knowledgebase processing (RAG)
python cli.py knowledgebase [operation]

# System utilities
python cli.py convert|status
```

---

**SentinelAI Data Pipeline** - Dual-purpose document processing for database storage and RAG applications.