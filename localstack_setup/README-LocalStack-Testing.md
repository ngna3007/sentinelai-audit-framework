# 🧪 Testing AWS Auto-Inventory with LocalStack

This guide explains how to test the AWS Auto-Inventory tool using LocalStack, allowing you to test all the PCI DSS compliance scanning features without needing real AWS resources.

## 🎯 What This Setup Provides

- **Complete AWS Simulation**: LocalStack provides 50+ AWS services
- **Real Testing**: Use your actual PCI DSS compliance configuration
- **No AWS Costs**: Everything runs locally
- **Safe Environment**: No risk of affecting real AWS resources
- **Full Feature Testing**: Test all inventory scanning capabilities

## 📋 Prerequisites

1. **Docker** and **Docker Compose** installed
2. **AWS CLI** installed and configured
3. **Python 3.7+** with the AWS Auto-Inventory tool
4. **curl** and **jq** (optional, for health checks)

## 🚀 Quick Start

### 1. Get LocalStack Auth Token (Optional but Recommended)

For the best experience with all AWS services:

1. Visit [https://app.localstack.cloud/](https://app.localstack.cloud/)
2. Sign up for a free account
3. Get your auth token
4. Set it as an environment variable:

```bash
export LOCALSTACK_AUTH_TOKEN=your-token-here
```

### 2. Start LocalStack and Initialize Infrastructure

```bash
# Make sure you're in the aws-auto-inventory directory
cd aws-auto-inventory

# Run the setup script
cd localstack_setup
./setup-localstack.sh
```

### 2a. Alternative: Quick Start Scripts

For the fastest setup, you have two options:

**Option A: From the localstack_setup directory:**
```bash
cd localstack_setup
./quick-start.sh
```

**Option B: From the project root (recommended):**
```bash
./localstack_setup/run-localstack-from-root.sh
```

The second option provides an interactive menu and ensures all files are created in the correct directories.

This script will:
- Start LocalStack with all required AWS services
- Wait for LocalStack to be ready
- Configure AWS CLI profile for LocalStack
- Set up the testing environment

### 3. Run the Complete Test

```bash
# Run the full test suite (from localstack_setup directory)
./test-aws-auto-inventory.sh
```

This script will:
- Populate LocalStack with comprehensive test infrastructure
- Create 50+ AWS resources across multiple services
- Run AWS Auto-Inventory with your PCI DSS compliance config
- Generate Excel and JSON reports

## 📂 What Gets Created in LocalStack

The test setup creates a realistic AWS environment including:

### 🏗️ Core Infrastructure
- VPC with public/private subnets
- Internet Gateway and NAT Gateway
- Security Groups and Network ACLs
- Route Tables and VPC Endpoints
- EC2 instances with encrypted EBS volumes
- SSH key pairs and snapshots

### 💾 Storage & Databases
- S3 buckets with encryption, versioning, logging
- RDS instances (MySQL, PostgreSQL, Aurora)
- DynamoDB tables with encryption
- ElastiCache clusters (Redis, Memcached)
- Redshift data warehouse
- DocumentDB and Neptune clusters
- EFS file systems with access points

### ⚡ Compute & Containers
- Lambda functions with different runtimes
- ECS clusters with Fargate tasks
- EKS Kubernetes clusters
- ECR container repositories
- EMR big data clusters

### 🔒 Security & Compliance
- IAM users, roles, groups, and policies
- KMS encryption keys and aliases
- Secrets Manager secrets
- CloudTrail audit trails
- GuardDuty threat detection
- Security Hub compliance monitoring
- AWS Config rules and compliance
- ACM SSL certificates

### 📊 Monitoring & Analytics
- CloudWatch log groups and alarms
- Kinesis data streams
- Athena workgroups
- MSK Kafka clusters
- SNS topics and SQS queues

### 🌐 Networking & Applications
- Application Load Balancers
- API Gateway REST and HTTP APIs
- CloudFront distributions
- Route53 hosted zones
- WAF web ACLs
- Network Firewall policies

## 📊 Expected Results

After running the test, you should see:

1. **Excel Report**: `pci-dss-compliance-inventory-localstack.xlsx`
2. **JSON Report**: Detailed scan results in JSON format
3. **Console Output**: Summary of discovered resources

The reports will contain all the LocalStack-created resources, demonstrating that AWS Auto-Inventory successfully:
- Connects to LocalStack endpoints
- Scans multiple AWS services
- Extracts resource configurations
- Applies PCI DSS compliance mapping
- Generates formatted reports

## 🔧 Advanced Usage

### Manual Testing

After running `./setup-localstack.sh`, you can manually test individual components:

```bash
# Check LocalStack health
curl http://localhost:4566/_localstack/health

# List S3 buckets
aws --profile localstack s3 ls

# Check EC2 instances
aws --profile localstack ec2 describe-instances

# Run inventory scan manually (from project root)
cd ..
python -m aws_auto_inventory.cli localstack_setup/config_pci_dss_compliance_localstack.json
```

### Custom Configuration

You can modify the PCI DSS configuration to test specific services:

1. Edit `config_pci_dss_compliance.json`
2. Add/remove specific sheets or services
3. Re-run the test script

### LocalStack Pro Features

With a LocalStack Pro auth token, you get:
- More realistic AWS service behavior
- Advanced security features
- Better compliance simulation
- Enhanced monitoring capabilities

## 🐛 Troubleshooting

### LocalStack Won't Start
```bash
# Check Docker status
docker info

# View LocalStack logs
docker-compose -f docker-compose-localstack.yml logs

# Restart LocalStack
docker-compose -f docker-compose-localstack.yml down
docker-compose -f docker-compose-localstack.yml up -d
```

### AWS Auto-Inventory Errors
```bash
# Check if you're in the right directory (should be project root)
ls aws_auto_inventory/

# Try different execution methods
python -m aws_auto_inventory.cli localstack_setup/config_pci_dss_compliance_localstack.json
cd aws_auto_inventory && python cli.py ../localstack_setup/config_pci_dss_compliance_localstack.json
```

### Missing Services
Some services may not be available in LocalStack Community Edition. This is normal and expected.

## 🛑 Cleanup

### Stop LocalStack
```bash
# From localstack_setup directory
docker-compose -f docker-compose-localstack.yml down

# Or from project root
cd localstack_setup && docker-compose -f docker-compose-localstack.yml down
```

### Remove All Data
```bash
# From localstack_setup directory
docker-compose -f docker-compose-localstack.yml down -v
rm -rf localstack_volume/
```

## 🎯 Summary of Changes for Subdirectory Structure

Since the LocalStack files are now in the `localstack_setup/` subdirectory, here are the key usage patterns:

### From Project Root (Recommended):
```bash
# Interactive menu with all options
./localstack_setup/run-localstack-from-root.sh

# Manual commands
cd localstack_setup
./setup-localstack.sh
./test-aws-auto-inventory.sh
cd ..
```

### From localstack_setup Directory:
```bash
cd localstack_setup
./quick-start.sh
# or
./setup-localstack.sh
./test-aws-auto-inventory.sh
```

The scripts automatically handle:
- ✅ Correct path resolution for config files
- ✅ Running AWS Auto-Inventory from the right directory  
- ✅ Creating output files in accessible locations
- ✅ Proper cleanup of temporary files

## 📚 Understanding the Test Results

The LocalStack test validates that AWS Auto-Inventory can:

1. **Connect to Alternative Endpoints**: Tests endpoint URL configuration
2. **Handle Multiple Services**: Scans 50+ AWS service types
3. **Process Complex Configurations**: Works with realistic resource setups
4. **Generate Compliance Reports**: Produces PCI DSS compliance mappings
5. **Handle Errors Gracefully**: Manages missing or unsupported services

This comprehensive testing approach ensures AWS Auto-Inventory works reliably in various AWS environments and can be trusted for real compliance auditing.

## 🎉 Success Indicators

Your test was successful if you see:
- ✅ LocalStack started and healthy
- ✅ Infrastructure deployed (150+ resources created)
- ✅ AWS Auto-Inventory scan completed
- ✅ Excel/JSON reports generated
- ✅ Resources detected across multiple service types

## 🆘 Getting Help

If you encounter issues:

1. Check the troubleshooting section above
2. Review LocalStack documentation: [https://docs.localstack.cloud/](https://docs.localstack.cloud/)
3. Check AWS Auto-Inventory logs and error messages
4. Ensure all prerequisites are installed and configured

Happy testing! 🚀 