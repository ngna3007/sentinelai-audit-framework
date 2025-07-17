# Database CLI Instructions

Quick reference guide for running the database CLI and managing the knowledge base.

## 📋 Prerequisites

1. **Supabase Setup**: You need a Supabase project with appropriate credentials
2. **Python Environment**: Python 3.8+ with required dependencies installed
3. **Environment Variables**: Configured `.env` file with Supabase credentials
4. **Run from Project Root**: Always run CLI commands from the project root directory

## 🚀 Initial Setup

### 1. Environment Configuration

```bash
# Navigate to project root directory
cd /path/to/sentinelai-audit-framework/

# Create environment file
python database/cli.py auth init

# Edit .env file with your credentials
# SUPABASE_URL=https://your-project.supabase.co
# SUPABASE_KEY=your-supabase-anon-key
# SUPABASE_SERVICE_KEY=your-supabase-service-key

# Verify credentials
python database/cli.py auth check
```

### 2. Database Schema Setup

**Option A: Manual Setup (Recommended)**
1. Copy contents from `create_tables_manual.sql`
2. Open your Supabase SQL Editor
3. Paste and execute the SQL commands
4. Verify tables are created

**Option B: Using CLI Migration**
```bash
# Run migrations (creates tables automatically)
python database/cli.py db migrate
```

## 💾 Knowledge Base Workflow

### Step 1: Prepare Knowledge Base Data

```bash
# Prepare data from parquet files and metadata
python database/cli.py data prepare-kb

# Custom data directory (if needed)
python database/cli.py data prepare-kb --data-dir /path/to/embeddings/

# Custom batch size (if needed)
python database/cli.py data prepare-kb --batch-size 500
```

**Expected Output:**
```
🔄 Preparing knowledge base data...
✅ Knowledge base data preparation completed!
   📁 Output directory: shared_data/outputs/knowledgebase/embeddings/prepared_data
   📊 Total records: 1740
   📦 Batch files: 2
   💾 SQL script: insert_knowledge_base.sql

🚀 Next steps:
   1. Run the SQL table creation script in Supabase
   2. Use: python -m database.cli data import-kb
```

### Step 2: Import Knowledge Base Data

```bash
# Import all prepared batch files
python database/cli.py data import-kb

# Import specific batch file
python database/cli.py data import-kb --batch-file knowledge_base_batch_001.json

# Dry run (see what would be imported)
python database/cli.py data import-kb --dry-run
```

**Expected Output:**
```
🔄 Importing knowledge base data...
✅ Imported 1000 records from knowledge_base_batch_001.json
✅ Imported 740 records from knowledge_base_batch_002.json

🎉 Knowledge base import completed! Total records imported: 1740
```

### Step 3: Verify Import

```bash
# Check database statistics
python database/cli.py data stats

# List knowledge base records
python database/cli.py data list knowledge_base --limit 5

# Search knowledge base
python database/cli.py data search-kb --query "PCI DSS network segmentation"
```

## 🔍 Common Operations

### View Data

```bash
# List all tables
python database/cli.py data list all

# List specific table
python database/cli.py data list pci_dss_controls --limit 10

# View in JSON format
python database/cli.py data list aws_config_rules_guidance --format json
```

### Search Knowledge Base

```bash
# Basic search
python database/cli.py data search-kb --query "encryption requirements"

# Search with framework filter
python database/cli.py data search-kb --query "network security" --framework-filter "PCI-DSS"

# Search with source filter
python database/cli.py data search-kb --query "AWS Config" --source-filter "PCI-DSS-v4_0_1-AWSConfig-Guidance"

# Limit results
python database/cli.py data search-kb --query "compliance" --limit 3
```

### Database Management

```bash
# View database statistics
python database/cli.py data stats

# Clear specific table (careful!)
python database/cli.py data clear knowledge_base

# Seed test data
python database/cli.py data seed --sample-size 50
```

## 🐛 Troubleshooting

### Common Issues

#### 1. "Unable to connect to Supabase"
```bash
# Check credentials
python database/cli.py auth check

# Verify .env file exists and has correct format
cat .env | grep SUPABASE
```

#### 2. "Table doesn't exist"
```bash
# Create tables manually in Supabase SQL Editor
# Copy/paste contents from create_tables_manual.sql

# Or use CLI migration
python database/cli.py db migrate
```

#### 3. "No batch files found to import"
```bash
# First prepare the data
python database/cli.py data prepare-kb

# Then import
python database/cli.py data import-kb
```

#### 4. "pgvector extension not found"
```bash
# In Supabase SQL Editor, run:
# CREATE EXTENSION IF NOT EXISTS vector;
# CREATE EXTENSION IF NOT EXISTS pg_trgm;
```

### Debug Commands

```bash
# Run with verbose output
python database/cli.py --verbose data import-kb

# Check prepared data directory
ls -la shared_data/outputs/knowledgebase/embeddings/prepared_data/

# Test connection
python -c "
from database.auth.supabase_client import SupabaseClient
client = SupabaseClient().get_client()
print('Connection successful!')
"
```

## 📊 Expected Data Structure

After successful import, you should have:

### Knowledge Base Table Structure
- **uuid**: Primary key (UUID)
- **content**: Text content (up to 2558 characters)
- **embedding**: 1024-dimensional vector
- **metadata**: JSON with document metadata

### Sample Metadata Structure
```json
{
  "chunk_id": "12345678-1234-1234-1234-123456789abc",
  "chunk_index": 42,
  "token_count": 1024,
  "source": "PCI-DSS-v4_0_1-docling-pic-annot",
  "document_name": "PCI DSS v4.0.1 Standard",
  "framework": "PCI-DSS",
  "framework_version": "4.0.1",
  "document_type": "standard",
  "key_topics": ["network", "security", "compliance"]
}
```

## 📈 Performance Tips

### Batch Size Optimization
- **Small datasets** (<1000 records): Use default batch size (1000)
- **Large datasets** (>5000 records): Use batch size 500-1000
- **Memory constrained**: Use batch size 200-500

### Import Performance
```bash
# Faster import (skip validation for known good data)
python database/cli.py data import-kb --no-validate

# Monitor import progress
python database/cli.py data import-kb --verbose
```

## 🔐 Security Notes

- Never commit `.env` files to version control
- Use service role key for admin operations
- Use anon key for read-only operations
- Regularly rotate Supabase keys

## 📚 Data Sources

The knowledge base contains processed data from:
- **PCI DSS v4.0.1 Standard** (1,012 chunks)
- **AWS Config Rules Guidance** (247 chunks)
- **AWS Well-Architected Security Pillar** (260 chunks)
- **Various AWS compliance guides** (221 chunks total)

## 🤝 Getting Help

If you encounter issues:

1. **Check CLI help**: `python database/cli.py --help`
2. **Use verbose mode**: `python database/cli.py --verbose [command]`
3. **Verify credentials**: `python database/cli.py auth check`
4. **Check database stats**: `python database/cli.py data stats`
5. **Review logs**: Look for error messages in CLI output

## 📋 Quick Reference

### Most Common Commands
```bash
# Setup
python database/cli.py auth init && python database/cli.py auth check

# Knowledge base workflow
python database/cli.py data prepare-kb
python database/cli.py data import-kb
python database/cli.py data search-kb --query "your search term"

# Verification
python database/cli.py data stats
python database/cli.py data list knowledge_base --limit 5
```

### File Locations
- **CLI**: `database/cli.py`
- **SQL Schema**: `database/create_tables_manual.sql`
- **Data Preparation**: `database/prepare_knowledge_base_data.py`
- **Source Data**: `shared_data/outputs/knowledgebase/embeddings/`
- **Prepared Data**: `shared_data/outputs/knowledgebase/embeddings/prepared_data/`

---

**Success!** 🎉 Your knowledge base should now be ready for semantic search and RAG applications.