.PHONY: help extract csv workflow validate clean migrate-info

# PCI DSS Control Processing Service (Compatibility Layer)
# =======================================================
# This service provides compatibility commands that use the centralized
# data_pipeline. The symlinks have been removed as migration is complete.

# Quick extraction using centralized pipeline
extract:
	@echo "🔗 Using centralized data_pipeline..."
	cd ../../ && python data_pipeline/cli.py extract pci-dss --verbose
	@echo "✅ Controls extracted to: shared_data/outputs/pci_dss_v4/controls/"

csv:
	@echo "🔗 Using centralized data_pipeline..."
	cd ../../ && python data_pipeline/cli.py generate csv --verbose
	@echo "✅ CSV generated to: shared_data/outputs/pci_dss_v4/bedrock/"

workflow:
	@echo "🔗 Using centralized data_pipeline..."
	cd ../../ && python data_pipeline/cli.py workflow --verbose
	@echo "✅ Complete workflow finished!"

validate:
	@echo "🔗 Using centralized data_pipeline..."
	cd ../../ && python data_pipeline/cli.py validate
	@echo "✅ Validation complete!"

# Cleanup
clean:
	@echo "🧹 Cleaning centralized output directories..."
	@if [ -d "../../shared_data/outputs/pci_dss_v4/controls" ]; then \
		echo "Cleaning shared_data/outputs/pci_dss_v4/controls/"; \
		rm -rf ../../shared_data/outputs/pci_dss_v4/controls/*; \
	fi
	@if [ -d "../../shared_data/outputs/pci_dss_v4/bedrock" ]; then \
		echo "Cleaning shared_data/outputs/pci_dss_v4/bedrock/"; \
		rm -rf ../../shared_data/outputs/pci_dss_v4/bedrock/*; \
	fi
	@echo "✅ Cleanup complete!"

# Migration information
migrate-info:
	@echo "📋 Migration Information"
	@echo "======================="
	@echo ""
	@echo "🎯 Migration COMPLETED - rag_service ready for RAG"
	@echo ""
	@echo "📁 Data Structure:"
	@echo "  Source documents: ../../shared_data/documents/"
	@echo "  Extracted controls: ../../shared_data/outputs/pci_dss_v4/controls/"
	@echo "  CSV files: ../../shared_data/outputs/pci_dss_v4/bedrock/"
	@echo ""
	@echo "🚀 Use centralized data_pipeline for full functionality:"
	@echo "  cd ../../"
	@echo "  python data_pipeline/cli.py workflow --verbose"
	@echo ""
	@echo "🔗 Compatibility commands (this Makefile):"
	@echo "  make extract   - Extract controls via centralized pipeline"
	@echo "  make csv       - Generate CSV via centralized pipeline"
	@echo "  make workflow  - Run complete workflow"
	@echo "  make validate  - Validate extraction quality"

# Help
help: migrate-info
	@echo ""
	@echo "📖 Available Commands:"
	@echo "  extract        - Extract PCI DSS controls"
	@echo "  csv           - Generate CSV for Bedrock"
	@echo "  workflow      - Complete extraction workflow"
	@echo "  validate      - Validate extraction quality"
	@echo "  clean         - Clean output directories"
	@echo "  migrate-info  - Show migration information"
	@echo "  help          - Show this help" 