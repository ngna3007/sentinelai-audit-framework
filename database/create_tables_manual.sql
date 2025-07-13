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
