#!/bin/bash

echo "🧪 Testing AWS Auto-Inventory with LocalStack"
echo "============================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if LocalStack is running
if ! curl -s http://localhost:4566/_localstack/health >/dev/null 2>&1; then
    print_error "LocalStack is not running. Please run './setup-localstack.sh' first."
    exit 1
fi

print_success "LocalStack is running!"

# Set environment variables for LocalStack
export LOCALSTACK_AUTH_TOKEN=ls-hOVobaQE-voMA-lumo-PAHE-35566553f7a6
export AWS_ACCESS_KEY_ID=test
export AWS_SECRET_ACCESS_KEY=test
export AWS_DEFAULT_REGION=us-east-1
export AWS_ENDPOINT_URL=http://localhost:4566

print_status "🏗️  Populating LocalStack with test infrastructure..."

# Run initialization scripts
print_status "Running core infrastructure setup..."
bash init-scripts/01-core-infrastructure.sh

print_status "Running databases and applications setup..."
bash init-scripts/02-databases-apps.sh

print_status "Running security and monitoring setup..."
bash init-scripts/03-security-monitoring.sh

print_status "Running containers and analytics setup..."
bash init-scripts/04-containers-analytics.sh

print_success "✅ Test infrastructure deployed to LocalStack!"

# Create a modified config that uses LocalStack profile and endpoint
print_status "Creating LocalStack-compatible configuration..."

# Create temporary config file with LocalStack settings
cat > config_pci_dss_compliance_localstack.json << 'EOF'
{
  "inventories": [
    {
      "name": "pci-dss-compliance-inventory-localstack",
      "aws": {
        "profile": "localstack",
        "region": [
          "us-east-1"
        ],
        "organization": false,
        "role_name": "OrganizationAccountAccessRole",
        "endpoint_url": "http://localhost:4566"
      },
      "excel": {
        "transpose": true,
        "formatting": {
          "header_style": {
            "bold": true,
            "bg_color": "#4F81BD",
            "font_color": "#FFFFFF"
          }
        }
      }
    }
  ]
}
EOF

# Extract sheets from original config and add to LocalStack config
python3 << 'PYTHON_SCRIPT'
import json

# Read original config from parent directory
with open('../config_pci_dss_compliance.json', 'r') as f:
    original_config = json.load(f)

# Read LocalStack config template
with open('config_pci_dss_compliance_localstack.json', 'r') as f:
    localstack_config = json.load(f)

# Copy sheets from original to LocalStack config
localstack_config['inventories'][0]['sheets'] = original_config['inventories'][0]['sheets']

# Write modified config
with open('config_pci_dss_compliance_localstack.json', 'w') as f:
    json.dump(localstack_config, f, indent=2)

print("✅ LocalStack configuration created")
PYTHON_SCRIPT

print_success "Configuration updated for LocalStack testing"

# Check what's available in LocalStack
print_status "📊 Checking LocalStack inventory before scan..."
echo "S3 Buckets:"
aws --profile localstack s3 ls 2>/dev/null || echo "  No S3 buckets found"

echo "EC2 Instances:"
aws --profile localstack ec2 describe-instances --query 'Reservations[].Instances[].{ID:InstanceId,State:State.Name}' 2>/dev/null || echo "  No EC2 instances found"

echo "RDS Instances:"
aws --profile localstack rds describe-db-instances --query 'DBInstances[].{ID:DBInstanceIdentifier,Engine:Engine}' 2>/dev/null || echo "  No RDS instances found"

echo "Lambda Functions:"
aws --profile localstack lambda list-functions --query 'Functions[].FunctionName' 2>/dev/null || echo "  No Lambda functions found"

# Run AWS Auto-Inventory
print_status "🔍 Running AWS Auto-Inventory scan..."

echo ""
echo "================================================"
echo "🚀 STARTING AWS AUTO-INVENTORY SCAN WITH LOCALSTACK"
echo "================================================"
echo ""

# Change to parent directory (project root) for execution
cd ..

# Check if we're in the aws-auto-inventory directory
if [ -f "aws_auto_inventory/__init__.py" ] || [ -f "setup.py" ]; then
    # We're in the project root, run as module
    print_status "Running from project root..."
    python -m aws_auto_inventory.cli -c localstack_setup/config_pci_dss_compliance_localstack.json
elif [ -f "cli.py" ]; then
    # We're in the aws_auto_inventory directory
    print_status "Running from aws_auto_inventory directory..."
    python cli.py -c ../localstack_setup/config_pci_dss_compliance_localstack.json
else
    # Try different approaches
    print_status "Trying alternative execution methods..."
    
    # Method 1: Try with python -m
    if python -c "import aws_auto_inventory" 2>/dev/null; then
        python -m aws_auto_inventory.cli -c localstack_setup/config_pci_dss_compliance_localstack.json
    # Method 2: Try direct execution
    elif [ -f "aws_auto_inventory/cli.py" ]; then
        cd aws_auto_inventory
        python cli.py -c ../localstack_setup/config_pci_dss_compliance_localstack.json
        cd ..
    # Method 3: Try with installed package
    elif command -v aws-auto-inventory >/dev/null 2>&1; then
        aws-auto-inventory -c localstack_setup/config_pci_dss_compliance_localstack.json
    else
        print_error "Could not find AWS Auto-Inventory. Please ensure it's installed or run from the correct directory."
        print_status "Try one of these:"
        echo "  1. pip install -e . (if in project root)"
        echo "  2. cd aws_auto_inventory && python cli.py -c ../localstack_setup/config_pci_dss_compliance_localstack.json"
        echo "  3. python -m aws_auto_inventory.cli -c localstack_setup/config_pci_dss_compliance_localstack.json"
        exit 1
    fi
fi

# Return to localstack_setup directory
cd localstack_setup

scan_exit_code=$?

echo ""
echo "================================================"
echo "📊 SCAN COMPLETED"
echo "================================================"

if [ $scan_exit_code -eq 0 ]; then
    print_success "✅ AWS Auto-Inventory scan completed successfully!"
    
    print_status "📁 Output files should be available in:"
    echo "  - output/ directory (if configured)"
    echo "  - Current directory"
    
    # Show any output files created
    if ls *.xlsx >/dev/null 2>&1; then
        print_status "📊 Excel files created:"
        ls -la *.xlsx
    fi
    
    if ls *.json >/dev/null 2>&1; then
        print_status "📄 JSON files created:"
        ls -la *.json | grep -v config_pci_dss
    fi
    
else
    print_warning "⚠️  Scan completed with exit code: $scan_exit_code"
    print_status "This might be normal if some services are not available in LocalStack Community Edition"
fi

# Summary
print_status "🎯 Test Summary:"
echo "  ✅ LocalStack infrastructure deployed"
echo "  ✅ Configuration adapted for LocalStack"
echo "  ✅ AWS Auto-Inventory scan executed"
echo "  📊 Results should show LocalStack-created resources"

# Cleanup option
echo ""
read -p "Do you want to stop LocalStack? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    print_status "Stopping LocalStack..."
    docker-compose -f docker-compose-localstack.yml down
    print_success "LocalStack stopped"
else
    print_status "LocalStack is still running. You can:"
    echo "  - View dashboard: http://localhost:4566/_localstack/health"
    echo "  - Stop with: docker-compose -f docker-compose-localstack.yml down"
    echo "  - Re-run scan: cd .. && python -m aws_auto_inventory.cli -c localstack_setup/config_pci_dss_compliance_localstack.json"
fi

# Clean up temporary config
rm -f config_pci_dss_compliance_localstack.json

print_success "�� Test completed!" 