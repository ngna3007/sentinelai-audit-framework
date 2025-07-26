#!/usr/bin/env python3
"""
Database CLI for managing Supabase operations
"""

import click
import os
import sys
import json
from pathlib import Path
from dotenv import load_dotenv

# Fix relative imports for standalone execution
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from database.auth.credentials import CredentialManager
from database.migrations.migration_runner import MigrationRunner
from database.importers import BulkImporter
from database.repositories import AwsConfigRuleRepository, PciControlRepository, PciAwsConfigMappingRepository
from database.prepare_knowledge_base_data import KnowledgeBaseDataPreparator

# Load environment variables
load_dotenv()

@click.group()
def cli():
    """Database management CLI for Supabase operations"""
    pass

@cli.group()
def db():
    """Database operations"""
    pass

@db.command()
@click.option('--validate/--no-validate', default=True, help='Validate schemas before creation')
@click.option('--dry-run', is_flag=True, help='Show what would be done without making changes')
def migrate(validate, dry_run):
    """Run database migrations"""
    runner = MigrationRunner()
    results = runner.run_migration(validate_schemas=validate, dry_run=dry_run)
    
    if results['success']:
        click.echo("✅ Migration completed successfully!")
    else:
        click.echo("❌ Migration failed!")
        for error in results['errors']:
            click.echo(f"   - {error}")

@db.command()
@click.argument('tables', nargs=-1)
def rollback(tables):
    """Rollback specific tables"""
    runner = MigrationRunner()
    results = runner.rollback_tables(tables)
    
    for table, result in results.items():
        if result['success']:
            click.echo(f"✅ Rolled back table: {table}")
        else:
            click.echo(f"❌ Failed to rollback {table}: {result['error']}")

@cli.group()
def import_data():
    """Data import operations"""
    pass

@import_data.command()
@click.option('--source', type=click.Path(exists=True), help='Source directory containing CSV files')
@click.option('--batch-size', type=int, default=1000, help='Batch size for imports')
@click.option('--progress/--no-progress', default=True, help='Show progress indicators')
@click.option('--validate/--no-validate', default=True, help='Validate data before import')
def bulk(source, batch_size, progress, validate):
    """Run bulk import from CSV files"""
    importer = BulkImporter(batch_size=batch_size, show_progress=progress, validate_data=validate)
    results = importer.import_all(source_dir=source)
    
    if results['success']:
        click.echo("✅ Bulk import completed successfully!")
        for table, count in results['imported_counts'].items():
            click.echo(f"   - {table}: {count} records")
        if results.get('validation_warnings'):
            click.echo("⚠️  Validation warnings:")
            for warning in results['validation_warnings']:
                click.echo(f"   - {warning}")
    else:
        click.echo("❌ Bulk import failed!")
        for error in results['errors']:
            click.echo(f"   - {error}")
@cli.group()
def data():
    """Data management operations"""
    pass

@data.command(name='list')
@click.argument('table', type=click.Choice(['pci_dss_controls', 'aws_config_rules_guidance', 'pci_aws_config_rule_mappings', 'knowledge_base', 'all']))
@click.option('--limit', type=int, default=10, help='Number of records to show')
@click.option('--format', type=click.Choice(['table', 'json']), default='table', help='Output format')
def list_data(table, limit, format):
    """List records from database tables"""
    from database.repositories import AwsConfigRuleRepository, PciControlRepository, PciAwsConfigMappingRepository
    from database.auth.supabase_client import SupabaseClientWrapper
    
    repositories = {
        'pci_dss_controls': PciControlRepository(),
        'aws_config_rules_guidance': AwsConfigRuleRepository(), 
        'pci_aws_config_rule_mappings': PciAwsConfigMappingRepository()
    }
    
    if table == 'knowledge_base':
        _display_knowledge_base_data(limit, format)
    elif table == 'all':
        for table_name, repo in repositories.items():
            _display_table_data(table_name, repo, limit, format)
            click.echo()
        _display_knowledge_base_data(limit, format)
    else:
        repo = repositories[table]
        _display_table_data(table, repo, limit, format)

@data.command()
@click.argument('table', type=click.Choice(['pci_dss_controls', 'aws_config_rules_guidance', 'pci_aws_config_rule_mappings', 'all']))
@click.option('--confirm', is_flag=True, help='Skip confirmation prompt')
def clear(table, confirm):
    """Clear all records from database tables"""
    from database.repositories import AwsConfigRuleRepository, PciControlRepository, PciAwsConfigMappingRepository
    
    repositories = {
        'pci_dss_controls': PciControlRepository(),
        'aws_config_rules_guidance': AwsConfigRuleRepository(),
        'pci_aws_config_rule_mappings': PciAwsConfigMappingRepository()
    }
    
    if not confirm:
        if table == 'all':
            click.confirm(f'Are you sure you want to clear ALL tables?', abort=True)
        else:
            click.confirm(f'Are you sure you want to clear table "{table}"?', abort=True)
    
    if table == 'all':
        for table_name, repo in repositories.items():
            count = repo.delete_all()
            click.echo(f"✅ Cleared {count} records from {table_name}")
    else:
        repo = repositories[table]
        count = repo.delete_all()
        click.echo(f"✅ Cleared {count} records from {table}")

@data.command()
@click.option('--sample-size', type=int, default=100, help='Number of sample records to create')
def seed(sample_size):
    """Seed database with sample/test data"""
    from database.repositories import AwsConfigRuleRepository, PciControlRepository, PciAwsConfigMappingRepository
    from uuid import uuid4
    import json
    
    click.echo("🌱 Seeding database with sample data...")
    
    # Seed PCI Controls
    pci_repo = PciControlRepository()
    pci_controls = []
    for i in range(min(sample_size, 50)):  # Limit PCI controls to reasonable number
        control = {
            'id': str(uuid4()),
            'control_id': f'1.{i+1}',
            'requirement': f'Sample PCI DSS requirement {i+1}',
            'chunk': f'This is sample chunk content for PCI control 1.{i+1}',
            'metadata': {'source': 'seed_data', 'version': 'v4.0.1', 'section': 'requirement_1'}
        }
        pci_controls.append(control)
    
    # Insert in batches
    try:
        pci_repo.client.table('pci_dss_controls').insert(pci_controls).execute()
        click.echo(f"✅ Seeded {len(pci_controls)} PCI DSS controls")
    except Exception as e:
        click.echo(f"❌ Failed to seed PCI controls: {e}")
    
    # Seed AWS Config Rules
    aws_repo = AwsConfigRuleRepository()
    aws_rules = []
    config_rule_names = ['s3-bucket-public-access', 'ec2-security-group-attached-to-eni', 'iam-password-policy']
    
    for i, rule_name in enumerate(config_rule_names):
        for chunk_num in range(3):  # 3 chunks per rule
            rule = {
                'id': str(uuid4()),
                'config_rule': rule_name,
                'chunk': f'Sample guidance chunk {chunk_num+1} for {rule_name}',
                'metadata': {'source': 'seed_data', 'chunk_index': chunk_num, 'rule_type': 'managed'}
            }
            aws_rules.append(rule)
    
    try:
        aws_repo.client.table('aws_config_rules_guidance').insert(aws_rules).execute()
        click.echo(f"✅ Seeded {len(aws_rules)} AWS Config rule chunks")
    except Exception as e:
        click.echo(f"❌ Failed to seed AWS Config rules: {e}")
    
    # Seed mappings
    mapping_repo = PciAwsConfigMappingRepository()
    mappings = []
    for i in range(min(len(pci_controls), 10)):  # Create mappings for first 10 controls
        mapping = {
            'id': str(uuid4()),
            'control_id': f'1.{i+1}',
            'config_rules': [
                {'rule_name': config_rule_names[i % len(config_rule_names)], 'compliance_type': 'relevant'},
                {'rule_name': 'cloudtrail-enabled', 'compliance_type': 'supporting'}
            ]
        }
        mappings.append(mapping)
    
    try:
        mapping_repo.client.table('pci_aws_config_rule_mappings').insert(mappings).execute()
        click.echo(f"✅ Seeded {len(mappings)} PCI-AWS Config mappings")
    except Exception as e:
        click.echo(f"❌ Failed to seed mappings: {e}")
    
    click.echo("🌱 Database seeding completed!")

@data.command()
@click.option('--data-dir', default='shared_data/outputs/knowledgebase/embeddings', help='Directory containing parquet and metadata files')
@click.option('--batch-size', type=int, default=1000, help='Number of records per batch file')
def prepare_kb(data_dir, batch_size):
    """Prepare knowledge base data for insertion"""
    click.echo("🔄 Preparing knowledge base data...")
    click.echo(f"📁 Source directory: {data_dir}")
    
    try:
        preparator = KnowledgeBaseDataPreparator(data_dir)
        result = preparator.run(batch_size)
        
        click.echo("✅ Knowledge base data preparation completed!")
        click.echo(f"   📁 Output directory: {result['output_dir']}")
        click.echo(f"   📊 Total records: {result['stats']['total_records']}")
        click.echo(f"   📦 Batch files: {len(result['batch_files'])}")
        click.echo(f"   💾 SQL script: {result['sql_file']}")
        click.echo(f"\n🚀 Next steps:")
        click.echo(f"   1. Run the SQL table creation script in Supabase")
        click.echo(f"   2. Use: python -m database.cli data import-kb")
        
    except Exception as e:
        click.echo(f"❌ Failed to prepare knowledge base data: {e}")

@data.command()
@click.option('--batch-file', help='Specific batch file to import (if not provided, imports all)')
@click.option('--prepared-data-dir', default='shared_data/outputs/knowledgebase/embeddings/prepared_data', help='Directory with prepared data files')
@click.option('--dry-run', is_flag=True, help='Show what would be imported without making changes')
def import_kb(batch_file, prepared_data_dir, dry_run):
    """Import knowledge base data from prepared batch files"""
    import json
    from pathlib import Path
    from database.auth.supabase_client import SupabaseClientWrapper
    
    click.echo("🔄 Importing knowledge base data...")
    click.echo(f"📁 Prepared data directory: {prepared_data_dir}")
    
    try:
        client = SupabaseClientWrapper().get_client()
        
        # Handle both relative and absolute paths
        if Path(prepared_data_dir).is_absolute():
            prepared_dir = Path(prepared_data_dir)
        else:
            # For relative paths, resolve from the project root
            script_dir = Path(__file__).parent
            project_root = script_dir.parent
            prepared_dir = project_root / prepared_data_dir
        
        if not prepared_dir.exists():
            click.echo(f"❌ Prepared data directory not found: {prepared_dir}")
            click.echo("   Run: python -m database.cli data prepare-kb first")
            return
        
        if batch_file:
            batch_files_list = [prepared_dir / batch_file]
        else:
            batch_files_list = list(prepared_dir.glob("knowledge_base_batch_*.json"))
        
        if not batch_files_list:
            click.echo("❌ No batch files found to import")
            return
        
        total_imported = 0
        
        for batch_file_path in sorted(batch_files_list):
            if not batch_file_path.exists():
                click.echo(f"❌ Batch file not found: {batch_file_path}")
                continue
                
            with open(batch_file_path, 'r') as f:
                batch_data = json.load(f)
            
            if dry_run:
                click.echo(f"🔍 Would import {len(batch_data)} records from {batch_file_path.name}")
            else:
                try:
                    response = client.table('knowledge_base').insert(batch_data).execute()
                    imported_count = len(response.data)
                    total_imported += imported_count
                    click.echo(f"✅ Imported {imported_count} records from {batch_file_path.name}")
                except Exception as e:
                    click.echo(f"❌ Failed to import {batch_file_path.name}: {e}")
        
        if not dry_run:
            click.echo(f"\n🎉 Knowledge base import completed! Total records imported: {total_imported}")
        else:
            # Calculate total records that would be imported
            total_would_import = 0
            for f in batch_files_list:
                try:
                    with open(f, 'r') as file:
                        data = json.load(file)
                        total_would_import += len(data)
                except Exception as e:
                    click.echo(f"Warning: Could not read {f.name}: {e}")
            click.echo(f"\n🔍 Dry run completed. Would import {total_would_import} total records")
            
    except Exception as e:
        click.echo(f"❌ Failed to import knowledge base data: {e}")

@data.command()
@click.option('--query', help='Search query text')
@click.option('--limit', type=int, default=5, help='Number of results to return')
@click.option('--similarity-threshold', type=float, default=0.7, help='Minimum similarity threshold (0-1)')
@click.option('--source-filter', help='Filter by source document')
@click.option('--framework-filter', help='Filter by framework (e.g., PCI-DSS)')
def search_kb(query, limit, similarity_threshold, source_filter, framework_filter):
    """Search knowledge base using text similarity"""
    from database.auth.supabase_client import SupabaseClientWrapper
    
    if not query:
        click.echo("❌ Query text is required")
        return
    
    try:
        client = SupabaseClientWrapper().get_client()
        
        # Build the query
        query_builder = client.table('knowledge_base').select('uuid, content, metadata')
        
        # Add filters
        if source_filter:
            query_builder = query_builder.eq('metadata->>source', source_filter)
        if framework_filter:
            query_builder = query_builder.eq('metadata->>framework', framework_filter)
        
        # Execute full-text search using tsvector (optimized for compliance/security domain)
        # Using PostgreSQL's full-text search with ranking
        search_query = f"""
        SELECT uuid, content, metadata, ts_rank(content_tsvector, plainto_tsquery('english', %s)) as rank
        FROM knowledge_base
        WHERE content_tsvector @@ plainto_tsquery('english', %s)
        ORDER BY rank DESC
        LIMIT %s
        """
        
        # Build filters
        filters = []
        params = [query, query, limit]
        
        if source_filter:
            filters.append("metadata->>'source_document' = %s")
            params.insert(-1, source_filter)
        if framework_filter:
            filters.append("metadata->>'framework' = %s")
            params.insert(-1, framework_filter)
        
        if filters:
            search_query = search_query.replace(
                "WHERE content_tsvector", 
                f"WHERE {' AND '.join(filters)} AND content_tsvector"
            )
        
        # Execute the query using RPC (raw SQL)
        try:
            response = client.rpc('execute_sql', {'sql': search_query, 'params': params}).execute()
            results = response.data if response.data else []
        except:
            # Fallback to simple text search if RPC fails
            query_builder = client.table('knowledge_base').select('uuid, content, metadata')
            if source_filter:
                query_builder = query_builder.eq('metadata->>source_document', source_filter)
            if framework_filter:
                query_builder = query_builder.eq('metadata->>framework', framework_filter)
            response = query_builder.ilike('content', f'%{query}%').limit(limit).execute()
            results = response.data if response.data else []
        
        if not results:
            click.echo("🔍 No results found")
            return
        
        click.echo(f"🔍 Found {len(results)} results for: '{query}'")
        click.echo("=" * 60)
        
        for i, result in enumerate(results, 1):
            metadata = result['metadata']
            rank = result.get('rank', 0)
            click.echo(f"\n{i}. Document: {metadata.get('document_name', 'Unknown')}")
            click.echo(f"   Source: {metadata.get('source_document', 'Unknown')}")
            click.echo(f"   Framework: {metadata.get('framework', 'N/A')}")
            if rank:
                click.echo(f"   Relevance: {rank:.4f}")
            click.echo(f"   Content: {result['content'][:200]}{'...' if len(result['content']) > 200 else ''}")
            
    except Exception as e:
        click.echo(f"❌ Failed to search knowledge base: {e}")

@data.command()
def stats():
    """Show database statistics"""
    from database.repositories import AwsConfigRuleRepository, PciControlRepository, PciAwsConfigMappingRepository
    
    click.echo("📊 Database Statistics:")
    click.echo("=" * 50)
    
    # PCI Controls stats
    pci_repo = PciControlRepository()
    pci_stats = pci_repo.get_stats()
    click.echo("\n🔒 PCI DSS Controls:")
    click.echo(f"   Total records: {pci_stats['total_records']}")
    click.echo(f"   Unique control IDs: {pci_stats['unique_control_ids']}")
    click.echo(f"   Records with requirements: {pci_stats['records_with_requirements']}")
    click.echo(f"   Records without requirements: {pci_stats['records_without_requirements']}")
    
    # AWS Config stats
    aws_repo = AwsConfigRuleRepository()
    aws_stats = aws_repo.get_stats()
    click.echo("\n☁️  AWS Config Rules:")
    click.echo(f"   Total records: {aws_stats['total_records']}")
    click.echo(f"   Unique config rules: {aws_stats['unique_config_rules']}")
    
    # Mapping stats
    mapping_repo = PciAwsConfigMappingRepository()
    mapping_stats = mapping_repo.get_stats()
    click.echo("\n🔗 PCI-AWS Config Mappings:")
    click.echo(f"   Total mappings: {mapping_stats['total_mappings']}")
    click.echo(f"   Unique control IDs: {mapping_stats['unique_control_ids']}")
    click.echo(f"   Unique config rules: {mapping_stats['unique_config_rules']}")
    
    coverage = mapping_stats['coverage_stats']
    click.echo(f"   Coverage: {coverage['coverage_percentage']}%")
    click.echo(f"   Controls with rules: {coverage['controls_with_rules']}")
    click.echo(f"   Controls without rules: {coverage['controls_without_rules']}")
    
    # Knowledge base stats
    try:
        from database.auth.supabase_client import SupabaseClientWrapper
        client = SupabaseClientWrapper().get_client()
        kb_response = client.table('knowledge_base').select('uuid', count='exact').execute()
        kb_count = kb_response.count if kb_response.count else 0
        
        click.echo(f"\n💾 Knowledge Base:")
        click.echo(f"   Total records: {kb_count}")
        
        # Get framework distribution
        framework_response = client.table('knowledge_base').select('metadata').execute()
        frameworks = {}
        for record in framework_response.data:
            framework = record['metadata'].get('framework', 'Unknown')
            frameworks[framework] = frameworks.get(framework, 0) + 1
        
        click.echo(f"   Framework distribution:")
        for framework, count in sorted(frameworks.items()):
            click.echo(f"     {framework}: {count}")
            
    except Exception as e:
        click.echo(f"\n💾 Knowledge Base: Error loading stats - {e}")

def _display_knowledge_base_data(limit, format):
    """Helper function to display knowledge base data"""
    from database.auth.supabase_client import SupabaseClientWrapper
    
    click.echo(f"📋 KNOWLEDGE_BASE (showing {limit} records):")
    
    try:
        client = SupabaseClientWrapper().get_client()
        response = client.table('knowledge_base').select('uuid, content, metadata').limit(limit).execute()
        
        if not response.data:
            click.echo("   No records found")
            return
        
        if format == 'json':
            for record in response.data:
                click.echo(json.dumps(record, indent=2))
        else:
            for i, record in enumerate(response.data, 1):
                metadata = record['metadata']
                click.echo(f"   {i}. UUID: {record['uuid']}")
                click.echo(f"      Source: {metadata.get('source_document', 'Unknown')}")
                click.echo(f"      Framework: {metadata.get('framework', 'N/A')}")
                click.echo(f"      Document: {metadata.get('document_name', 'Unknown')}")
                click.echo(f"      Document Type: {metadata.get('document_type', 'Unknown')}")
                content = record['content']
                click.echo(f"      Content: {content[:100]}{'...' if len(content) > 100 else ''}")
                click.echo()
                
    except Exception as e:
        click.echo(f"   Error loading knowledge base data: {e}")

def _display_table_data(table_name, repository, limit, format):
    """Helper function to display table data"""
    click.echo(f"📋 {table_name.upper()} (showing {limit} records):")
    
    records = repository.find_all()[:limit]
    
    if format == 'json':
        import json
        for record in records:
            click.echo(json.dumps(record.to_dict(), indent=2))
    else:
        if not records:
            click.echo("   No records found")
            return
            
        # Simple table format
        for i, record in enumerate(records, 1):
            record_dict = record.to_dict()
            click.echo(f"   {i}. ID: {record_dict.get('id', 'N/A')}")
            
            # Show key fields based on table type
            if hasattr(record, 'control_id'):
                click.echo(f"      Control ID: {record_dict.get('control_id', 'N/A')}")
            if hasattr(record, 'config_rule'):
                click.echo(f"      Config Rule: {record_dict.get('config_rule', 'N/A')}")
            if hasattr(record, 'requirement'):
                req = record_dict.get('requirement', '')
                if req:
                    click.echo(f"      Requirement: {req[:100]}{'...' if len(req) > 100 else ''}")
            
            chunk = record_dict.get('chunk', '')
            if chunk:
                click.echo(f"      Chunk: {chunk[:100]}{'...' if len(chunk) > 100 else ''}")
            click.echo()

@cli.group()
def auth():
    """Authentication management"""
    pass

@auth.command()
def check():
    """Check Supabase credentials"""
    cred_manager = CredentialManager()
    if cred_manager.validate_credentials():
        click.echo("✅ Credentials are valid")
    else:
        click.echo("❌ Invalid or missing credentials")

@auth.command()
def init():
    """Initialize .env file"""
    cred_manager = CredentialManager()
    cred_manager.create_env_template()
    click.echo("✅ Created .env.template file")
    click.echo("⚠️  Rename to .env and add your credentials")

if __name__ == "__main__":
    cli()
