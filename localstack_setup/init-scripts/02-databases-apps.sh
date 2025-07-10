#!/bin/bash

echo "=== Setting up Databases and Application Services ==="

# Set AWS CLI to use LocalStack
export AWS_ACCESS_KEY_ID=test
export AWS_SECRET_ACCESS_KEY=test
export AWS_DEFAULT_REGION=us-east-1
export AWS_ENDPOINT_URL=http://localhost:4566

echo "🗄️  Setting up RDS..."

# Create RDS subnet group
aws rds create-db-subnet-group --db-subnet-group-name pci-db-subnet-group --db-subnet-group-description "PCI Compliance DB Subnet Group" --subnet-ids subnet-12345 subnet-67890

# Create RDS instances
aws rds create-db-instance \
    --db-instance-identifier pci-mysql-primary \
    --db-instance-class db.t3.micro \
    --engine mysql \
    --master-username admin \
    --master-user-password SecurePassword123! \
    --allocated-storage 20 \
    --storage-encrypted \
    --vpc-security-group-ids sg-12345 \
    --db-subnet-group-name pci-db-subnet-group \
    --backup-retention-period 7 \
    --storage-type gp2

aws rds create-db-instance \
    --db-instance-identifier pci-postgres-secondary \
    --db-instance-class db.t3.micro \
    --engine postgres \
    --master-username postgres \
    --master-user-password SecurePassword123! \
    --allocated-storage 20 \
    --storage-encrypted \
    --vpc-security-group-ids sg-12345 \
    --db-subnet-group-name pci-db-subnet-group \
    --backup-retention-period 7

# Create RDS cluster (Aurora)
aws rds create-db-cluster \
    --db-cluster-identifier pci-aurora-cluster \
    --engine aurora-mysql \
    --master-username admin \
    --master-user-password SecurePassword123! \
    --storage-encrypted \
    --vpc-security-group-ids sg-12345 \
    --db-subnet-group-name pci-db-subnet-group \
    --backup-retention-period 7

# Create manual snapshot
aws rds create-db-snapshot \
    --db-instance-identifier pci-mysql-primary \
    --db-snapshot-identifier pci-mysql-snapshot-manual

echo "📊 Setting up DynamoDB..."

# Create DynamoDB tables
aws dynamodb create-table \
    --table-name PCI-UserData \
    --attribute-definitions \
        AttributeName=UserId,AttributeType=S \
    --key-schema \
        AttributeName=UserId,KeyType=HASH \
    --billing-mode PAY_PER_REQUEST \
    --sse-specification Enabled=true

aws dynamodb create-table \
    --table-name PCI-TransactionLog \
    --attribute-definitions \
        AttributeName=TransactionId,AttributeType=S \
        AttributeName=Timestamp,AttributeType=N \
    --key-schema \
        AttributeName=TransactionId,KeyType=HASH \
        AttributeName=Timestamp,KeyType=RANGE \
    --billing-mode PAY_PER_REQUEST \
    --sse-specification Enabled=true

echo "⚡ Setting up Lambda Functions..."

# Create a simple Lambda function zip
echo 'exports.handler = async (event) => { console.log("PCI Compliance Function executed"); return { statusCode: 200, body: "Success" }; };' > /tmp/lambda-function.js
cd /tmp && zip lambda-function.zip lambda-function.js

# Create Lambda functions
aws lambda create-function \
    --function-name PCI-DataProcessor \
    --runtime nodejs18.x \
    --role arn:aws:iam::000000000000:role/LambdaExecutionRole \
    --handler lambda-function.handler \
    --zip-file fileb://lambda-function.zip \
    --timeout 30 \
    --memory-size 256

aws lambda create-function \
    --function-name PCI-AuditLogger \
    --runtime nodejs18.x \
    --role arn:aws:iam::000000000000:role/LambdaExecutionRole \
    --handler lambda-function.handler \
    --zip-file fileb://lambda-function.zip \
    --timeout 60 \
    --memory-size 512

echo "🗄️  Setting up ElastiCache..."

# Create ElastiCache subnet group
aws elasticache create-cache-subnet-group \
    --cache-subnet-group-name pci-cache-subnet-group \
    --cache-subnet-group-description "PCI Compliance Cache Subnet Group" \
    --subnet-ids subnet-12345 subnet-67890

# Create Redis cluster
aws elasticache create-cache-cluster \
    --cache-cluster-id pci-redis-cluster \
    --engine redis \
    --cache-node-type cache.t3.micro \
    --num-cache-nodes 1 \
    --cache-subnet-group-name pci-cache-subnet-group \
    --security-group-ids sg-12345 \
    --at-rest-encryption-enabled \
    --transit-encryption-enabled

# Create Memcached cluster
aws elasticache create-cache-cluster \
    --cache-cluster-id pci-memcached-cluster \
    --engine memcached \
    --cache-node-type cache.t3.micro \
    --num-cache-nodes 2 \
    --cache-subnet-group-name pci-cache-subnet-group \
    --security-group-ids sg-12345

# Create replication group
aws elasticache create-replication-group \
    --replication-group-id pci-redis-replication \
    --description "PCI Redis Replication Group" \
    --cache-node-type cache.t3.micro \
    --cache-subnet-group-name pci-cache-subnet-group \
    --security-group-ids sg-12345 \
    --at-rest-encryption-enabled \
    --transit-encryption-enabled

echo "🏭 Setting up Redshift..."

# Create Redshift cluster
aws redshift create-cluster \
    --cluster-identifier pci-data-warehouse \
    --node-type dc2.large \
    --cluster-type single-node \
    --master-username admin \
    --master-user-password SecurePassword123! \
    --encrypted \
    --publicly-accessible false

echo "📄 Setting up DocumentDB..."

# Create DocumentDB subnet group
aws docdb create-db-subnet-group \
    --db-subnet-group-name pci-docdb-subnet-group \
    --db-subnet-group-description "PCI DocumentDB Subnet Group" \
    --subnet-ids subnet-12345 subnet-67890

# Create DocumentDB cluster
aws docdb create-db-cluster \
    --db-cluster-identifier pci-document-cluster \
    --engine docdb \
    --master-username admin \
    --master-user-password SecurePassword123! \
    --storage-encrypted \
    --vpc-security-group-ids sg-12345 \
    --db-subnet-group-name pci-docdb-subnet-group \
    --backup-retention-period 7

echo "🔍 Setting up OpenSearch..."

# Create OpenSearch domain
aws opensearch create-domain \
    --domain-name pci-search-domain \
    --elasticsearch-version 7.10 \
    --elasticsearch-cluster-config InstanceType=t3.small.search,InstanceCount=1 \
    --ebs-options EBSEnabled=true,VolumeType=gp2,VolumeSize=10 \
    --encryption-at-rest-options Enabled=true \
    --node-to-node-encryption-options Enabled=true \
    --domain-endpoint-options EnforceHTTPS=true

echo "🌐 Setting up EFS..."

# Create EFS file system
EFS_ID=$(aws efs create-file-system \
    --performance-mode generalPurpose \
    --throughput-mode provisioned \
    --provisioned-throughput-in-mibps 100 \
    --encrypted \
    --query 'FileSystemId' --output text)

echo "Created EFS: $EFS_ID"

# Create EFS access point
aws efs create-access-point \
    --file-system-id $EFS_ID \
    --posix-user Uid=1000,Gid=1000 \
    --root-directory Path="/secure",CreationInfo="{OwnerUid=1000,OwnerGid=1000,Permissions=755}"

echo "🚀 Setting up Neptune..."

# Create Neptune subnet group
aws neptune create-db-subnet-group \
    --db-subnet-group-name pci-neptune-subnet-group \
    --db-subnet-group-description "PCI Neptune Subnet Group" \
    --subnet-ids subnet-12345 subnet-67890

# Create Neptune cluster
aws neptune create-db-cluster \
    --db-cluster-identifier pci-graph-cluster \
    --engine neptune \
    --storage-encrypted \
    --vpc-security-group-ids sg-12345 \
    --db-subnet-group-name pci-neptune-subnet-group \
    --backup-retention-period 7

echo "📧 Setting up SES..."

# Verify email addresses for SES
aws ses verify-email-identity --email-address admin@example.com
aws ses verify-email-identity --email-address security@example.com

# Create SES configuration set
aws ses create-configuration-set --configuration-set Name=PCI-SecurityAlerts

echo "📩 Setting up SNS..."

# Create SNS topics
TOPIC_SECURITY=$(aws sns create-topic --name PCI-SecurityAlerts --query 'TopicArn' --output text)
TOPIC_BACKUP=$(aws sns create-topic --name PCI-BackupNotifications --query 'TopicArn' --output text)

echo "Created SNS Topics: $TOPIC_SECURITY, $TOPIC_BACKUP"

echo "📬 Setting up SQS..."

# Create SQS queues
aws sqs create-queue --queue-name PCI-ProcessingQueue --attributes '{
    "MessageRetentionPeriod": "1209600",
    "VisibilityTimeoutSeconds": "300",
    "KmsMasterKeyId": "alias/aws/sqs"
}'

aws sqs create-queue --queue-name PCI-DeadLetterQueue --attributes '{
    "MessageRetentionPeriod": "1209600"
}'

echo "✅ Databases and Application Services setup complete!" 