#!/bin/bash

echo "🚀 AWS Auto-Inventory LocalStack Runner (from project root)"
echo "========================================================="

# Check if we're in the project root
if [ ! -f "aws_auto_inventory/__init__.py" ] && [ ! -f "setup.py" ]; then
    echo "❌ Error: This script must be run from the aws-auto-inventory project root directory"
    echo "Current directory: $(pwd)"
    echo "Please cd to the project root and run: ./localstack_setup/run-localstack-from-root.sh"
    exit 1
fi

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}This script will:${NC}"
echo "1. Set up LocalStack from the project root"
echo "2. Run AWS Auto-Inventory tests"
echo "3. Generate reports in the correct directory"
echo ""

# Ask what the user wants to do
echo "Choose an option:"
echo "1. Setup LocalStack only"
echo "2. Run tests only (requires LocalStack running)"
echo "3. Setup and run complete test"
echo "4. Quick start (setup + test + cleanup)"
echo ""
read -p "Enter your choice (1-4): " choice

case $choice in
    1)
        echo -e "${GREEN}Setting up LocalStack...${NC}"
        cd localstack_setup
        ./setup-localstack.sh
        cd ..
        ;;
    2)
        echo -e "${GREEN}Running tests...${NC}"
        cd localstack_setup
        ./test-aws-auto-inventory.sh
        cd ..
        ;;
    3)
        echo -e "${GREEN}Running setup and test...${NC}"
        cd localstack_setup
        ./setup-localstack.sh
        if [ $? -eq 0 ]; then
            ./test-aws-auto-inventory.sh
        fi
        cd ..
        ;;
    4)
        echo -e "${GREEN}Running quick start...${NC}"
        cd localstack_setup
        ./quick-start.sh
        cd ..
        ;;
    *)
        echo "Invalid choice. Exiting."
        exit 1
        ;;
esac

echo ""
echo -e "${GREEN}✅ Operation completed!${NC}"
echo ""
echo -e "${BLUE}📁 Output files should be in:${NC}"
echo "  - Current directory (project root)"
echo "  - output/ directory"
echo "  - localstack_setup/output/ directory"
echo ""
echo -e "${YELLOW}💡 Quick commands:${NC}"
echo "  - Check LocalStack: curl http://localhost:4566/_localstack/health"
echo "  - Stop LocalStack: cd localstack_setup && docker-compose -f docker-compose-localstack.yml down"
echo "  - Re-run test: ./localstack_setup/run-localstack-from-root.sh" 