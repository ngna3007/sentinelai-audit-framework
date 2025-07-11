.PHONY: install install-dev test lint format extract extract-csv extract-all analyze validate clean help

# Installation
install:
	pip3 install -r requirements.txt

install-dev:
	pip3 install -r requirements.txt -r requirements-dev.txt

# Testing and quality for modular architecture
test:
	pytest -v

lint:
	mypy extractors/ utils/ --ignore-missing-imports
	flake8 extractors/ utils/

format:
	black extractors/ utils/ notebooks/
	isort extractors/ utils/ notebooks/

# Modular PCI DSS Control Extraction
extract:
	python -m extractors.pci_dss_v4_0_1.main extract --verbose
	@echo "✅ Control extraction complete! Check extracted_controls/ directory"

extract-csv:
	python -m extractors.pci_dss_v4_0_1.main csv --verbose
	@echo "✅ CSV generation complete! Check ingest/bedrock/ directory"

extract-all:
	python -m extractors.pci_dss_v4_0_1.main all --verbose
	@echo "✅ Complete workflow finished! Controls and CSV files ready"

# Custom extraction options
extract-custom:
	@echo "Usage: make extract-custom ARGS='--chunk-size 400 --output-dir /tmp/controls'"
	python -m extractors.pci_dss_v4_0_1.main extract $(ARGS)

extract-csv-custom:
	@echo "Usage: make extract-csv-custom ARGS='--chunk-size 400'"
	python -m extractors.pci_dss_v4_0_1.main csv $(ARGS)

# Analysis and validation (legacy tools for comparison)
analyze-legacy:
	@echo "Note: Legacy analysis tools in utils/ for comparison"
	python utils/simple_control_finder.py 2>/dev/null || echo "Legacy tool unavailable"

# Quality metrics and validation
quality-check:
	python -c "import json, os; files = [f for f in os.listdir('extracted_controls') if f.endswith('.json')] if os.path.exists('extracted_controls') else []; total_controls = len(files); print(f'✅ Found {total_controls} extracted controls'); print('✅ Extraction appears complete (256+ controls)' if total_controls >= 256 else f'⚠️  Only {total_controls} controls found, expected 256+') if files else print('❌ No extracted_controls directory found. Run: make extract')"

# Development helpers
dev-extract:
	python -m extractors.pci_dss_v4_0_1.main extract --verbose --output-dir extracted_controls_dev

show-help:
	python -m extractors.pci_dss_v4_0_1.main --help

# Cleanup
clean:
	rm -rf extracted_controls/*
	rm -rf ingest/bedrock/*
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -name "*.pyc" -delete
	@echo "✅ Cleaned output and cache files"

clean-all: clean
	rm -rf extracted_controls/
	rm -rf ingest/bedrock/
	@echo "✅ Removed all output directories"

# Help
help:
	@echo "🎯 PCI DSS Control Extractor - Modular Architecture"
	@echo "=================================================="
	@echo ""
	@echo "📦 Installation:"
	@echo "  install         - Install runtime dependencies"
	@echo "  install-dev     - Install development dependencies"
	@echo ""
	@echo "🚀 Main Extraction Commands:"
	@echo "  extract         - Extract controls from markdown (main workflow)"
	@echo "  extract-csv     - Generate CSV for Bedrock Knowledge Base"
	@echo "  extract-all     - Complete workflow (extract + csv)"
	@echo ""
	@echo "⚙️  Custom Options:"
	@echo "  extract-custom     - Custom extraction: make extract-custom ARGS='--chunk-size 400'"
	@echo "  extract-csv-custom - Custom CSV: make extract-csv-custom ARGS='--chunk-size 400'"
	@echo ""
	@echo "🧪 Testing & Quality:"
	@echo "  test            - Run tests"
	@echo "  lint            - Run type checking and linting"
	@echo "  format          - Format code with black and isort"
	@echo "  quality-check   - Check extraction completeness"
	@echo ""
	@echo "🛠️  Development:"
	@echo "  dev-extract     - Extract to dev directory"
	@echo "  show-help       - Show detailed extractor help"
	@echo "  analyze-legacy  - Run legacy analysis tools"
	@echo ""
	@echo "🧹 Cleanup:"
	@echo "  clean           - Clean output and cache files"
	@echo "  clean-all       - Remove all output directories"
	@echo ""
	@echo "📖 Quick Start:"
	@echo "  make install && make extract-all" 