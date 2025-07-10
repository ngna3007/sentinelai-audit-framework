#!/bin/bash

echo "🚀 AWS Auto-Inventory LocalStack Test Setup"
echo "==========================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
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

# Check if Docker is running
if ! docker info >/dev/null 2>&1; then
    print_error "Docker is not running. Please start Docker and try again."
    exit 1
fi

# Check if LocalStack Auth Token is set
if [ -z "$LOCALSTACK_AUTH_TOKEN" ]; then
    print_warning "LOCALSTACK_AUTH_TOKEN not set. LocalStack Pro features may not work."
    print_warning "You can get a free auth token at: https://app.localstack.cloud/"
    read -p "Do you want to continue with LocalStack Community Edition? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_error "Exiting. Please set LOCALSTACK_AUTH_TOKEN environment variable."
        exit 1
    fi
fi

print_status "Starting LocalStack..."

# Stop any existing LocalStack containers
docker-compose -f docker-compose-localstack.yml down 2>/dev/null

# Start LocalStack
docker-compose -f docker-compose-localstack.yml up -d

print_status "Waiting for LocalStack to be ready..."

# Wait for LocalStack to be healthy
max_attempts=60
attempt=0
while [ $attempt -lt $max_attempts ]; do
    if curl -s http://localhost:4566/_localstack/health >/dev/null 2>&1; then
        print_success "LocalStack is ready!"
        break
    fi
    
    echo -n "."
    sleep 2
    attempt=$((attempt + 1))
done

if [ $attempt -eq $max_attempts ]; then
    print_error "LocalStack failed to start within 2 minutes"
    docker-compose -f docker-compose-localstack.yml logs
    exit 1
fi

echo ""

# Set up AWS CLI profile for LocalStack
print_status "Setting up AWS CLI profile for LocalStack..."

aws configure set aws_access_key_id test --profile localstack
aws configure set aws_secret_access_key test --profile localstack
aws configure set region us-east-1 --profile localstack
aws configure set output json --profile localstack

print_success "AWS CLI profile 'localstack' configured"

# Make initialization scripts executable
print_status "Making initialization scripts executable..."
chmod +x init-scripts/*.sh

print_status "LocalStack services status:"
curl -s http://localhost:4566/_localstack/health | jq '.' 2>/dev/null || echo "Could not parse health status"

print_success "✅ LocalStack is ready for testing!"
print_status "LocalStack Dashboard: http://localhost:4566/_localstack/health"
print_status "Next steps:"
echo "  1. Run: ./test-aws-auto-inventory.sh"
echo "  2. Or manually run: cd .. && python -m aws_auto_inventory.cli localstack_setup/config_pci_dss_compliance_localstack.json" 