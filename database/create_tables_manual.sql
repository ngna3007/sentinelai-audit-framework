-- Manual Table Creation Script for Supabase Dashboard
-- Copy and paste these SQL commands into your Supabase SQL Editor

-- Table 1: PCI DSS Controls
CREATE TABLE IF NOT EXISTS pci_dss_controls (
    id UUID PRIMARY KEY NOT NULL DEFAULT gen_random_uuid(),
    control_id VARCHAR(20) NOT NULL,
    requirement TEXT,
    chunk TEXT NOT NULL,
    metadata JSONB NOT NULL
);

-- Index for PCI DSS Controls
CREATE UNIQUE INDEX IF NOT EXISTS idx_control_id ON pci_dss_controls (control_id);
CREATE INDEX IF NOT EXISTS idx_metadata_gin ON pci_dss_controls USING GIN (metadata);

-- Table 2: AWS Config Rules Guidance
CREATE TABLE IF NOT EXISTS aws_config_rules_guidance (
    id UUID PRIMARY KEY NOT NULL DEFAULT gen_random_uuid(),
    config_rule VARCHAR(100) NOT NULL,
    chunk TEXT NOT NULL,
    metadata JSONB NOT NULL
);

-- Index for AWS Config Rules
CREATE UNIQUE INDEX IF NOT EXISTS idx_config_rule ON aws_config_rules_guidance (config_rule);
CREATE INDEX IF NOT EXISTS idx_metadata_gin_aws ON aws_config_rules_guidance USING GIN (metadata);

-- Table 3: PCI AWS Config Rule Mappings
CREATE TABLE IF NOT EXISTS pci_aws_config_rule_mappings (
    id UUID PRIMARY KEY NOT NULL DEFAULT gen_random_uuid(),
    control_id VARCHAR(20) NOT NULL UNIQUE,
    config_rules JSONB NOT NULL
);

-- Index for Mappings
CREATE UNIQUE INDEX IF NOT EXISTS idx_mapping_control_id ON pci_aws_config_rule_mappings (control_id);
CREATE INDEX IF NOT EXISTS idx_config_rules_gin ON pci_aws_config_rule_mappings USING GIN (config_rules);

-- Knowledge Base Table
-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS vector;

-- Table 4: Knowledge Base Embeddings
CREATE TABLE IF NOT EXISTS knowledge_base (
    uuid UUID PRIMARY KEY NOT NULL DEFAULT gen_random_uuid(),
    content TEXT NOT NULL,
    embedding VECTOR(1024) NOT NULL,
    metadata JSONB NOT NULL,
    content_tsvector TSVECTOR GENERATED ALWAYS AS (to_tsvector('english', content)) STORED,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes for Knowledge Base

-- Vector similarity search indexes
CREATE INDEX IF NOT EXISTS idx_kb_vector_cosine ON knowledge_base USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);
CREATE INDEX IF NOT EXISTS idx_kb_vector_l2 ON knowledge_base USING ivfflat (embedding vector_l2_ops) WITH (lists = 100);
CREATE INDEX IF NOT EXISTS idx_kb_vector_ip ON knowledge_base USING ivfflat (embedding vector_ip_ops) WITH (lists = 100);

-- Full-text search index using stored tsvector (optimized for compliance/security domain)
CREATE INDEX IF NOT EXISTS idx_kb_content_fts ON knowledge_base USING GIN (content_tsvector);

-- Metadata indexes for filtering
CREATE INDEX IF NOT EXISTS idx_kb_metadata_gin ON knowledge_base USING GIN (metadata);
CREATE INDEX IF NOT EXISTS idx_kb_source_doc ON knowledge_base USING btree ((metadata->>'source_document'));
CREATE INDEX IF NOT EXISTS idx_kb_document_type ON knowledge_base USING btree ((metadata->>'document_type'));
CREATE INDEX IF NOT EXISTS idx_kb_framework ON knowledge_base USING btree ((metadata->>'framework'));
CREATE INDEX IF NOT EXISTS idx_kb_framework_version ON knowledge_base USING btree ((metadata->>'framework_version'));

-- Key topics index for topic-based filtering
CREATE INDEX IF NOT EXISTS idx_kb_key_topics ON knowledge_base USING GIN ((metadata->'key_topics'));

-- Composite index for framework + document type queries
CREATE INDEX IF NOT EXISTS idx_kb_framework_doctype ON knowledge_base USING btree ((metadata->>'framework'), (metadata->>'document_type'));

-- Timestamp indexes for temporal queries
CREATE INDEX IF NOT EXISTS idx_kb_created_at ON knowledge_base USING btree (created_at);
CREATE INDEX IF NOT EXISTS idx_kb_updated_at ON knowledge_base USING btree (updated_at);