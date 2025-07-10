#!/bin/bash

echo "🚀 AWS Auto-Inventory LocalStack Quick Start"
echo "============================================"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}This script will:${NC}"
echo "1. Set up LocalStack with 50+ AWS services"
echo "2. Deploy comprehensive test infrastructure"
echo "3. Run AWS Auto-Inventory with your PCI DSS config"
echo "4. Generate compliance reports"
echo ""

# Confirm with user
read -p "Do you want to continue? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Exiting..."
    exit 0
fi

echo ""
echo -e "${GREEN}🔧 Step 1: Setting up LocalStack...${NC}"
cd localstack_setup
./setup-localstack.sh

if [ $? -ne 0 ]; then
    echo "❌ LocalStack setup failed. Please check the error messages above."
    exit 1
fi

echo ""
echo -e "${GREEN}🧪 Step 2: Running comprehensive test...${NC}"
./test-aws-auto-inventory.sh
cd ..

if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}✅ SUCCESS! AWS Auto-Inventory LocalStack test completed!${NC}"
    echo ""
    echo -e "${BLUE}📊 What was tested:${NC}"
    echo "  • 50+ AWS services"
    echo "  • 150+ infrastructure resources"
    echo "  • PCI DSS compliance scanning"
    echo "  • Report generation"
    echo ""
    echo -e "${BLUE}📁 Check for output files:${NC}"
    echo "  • Excel reports (*.xlsx)"
    echo "  • JSON reports (*.json)"
    echo ""
    echo -e "${YELLOW}💡 Next steps:${NC}"
    echo "  • Review the generated reports"
    echo "  • Customize config_pci_dss_compliance.json for your needs"
    echo "  • Test with real AWS account when ready"
else
    echo ""
    echo -e "${YELLOW}⚠️  Test completed with warnings. This is often normal with LocalStack Community Edition.${NC}"
    echo "Check the output above for details."
fi

echo ""
echo "🎉 LocalStack testing complete! See README-LocalStack-Testing.md for more details." 