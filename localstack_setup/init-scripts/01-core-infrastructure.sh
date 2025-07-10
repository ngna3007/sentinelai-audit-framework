#!/bin/bash

echo "=== Setting up Core Infrastructure for PCI DSS Compliance Testing ==="

# Set AWS CLI to use LocalStack
export LOCALSTACK_AUTH_TOKEN=ls-hOVobaQE-voMA-lumo-PAHE-35566553f7a6
export AWS_ACCESS_KEY_ID=test
export AWS_SECRET_ACCESS_KEY=test
export AWS_DEFAULT_REGION=us-east-1
export AWS_ENDPOINT_URL=http://localhost:4566

# Function to wait for service availability
wait_for_service() {
    local service=$1
    echo "Waiting for $service to be available..."
    while ! aws $service help >/dev/null 2>&1; do
        sleep 1
    done
    echo "$service is ready"
}

echo "🏗️  Setting up VPC and Networking..."

# Create VPC
VPC_ID=$(aws ec2 create-vpc --cidr-block 10.0.0.0/16 --query 'Vpc.VpcId' --output text)
echo "Created VPC: $VPC_ID"

# Create Internet Gateway
IGW_ID=$(aws ec2 create-internet-gateway --query 'InternetGateway.InternetGatewayId' --output text)
aws ec2 attach-internet-gateway --vpc-id $VPC_ID --internet-gateway-id $IGW_ID
echo "Created Internet Gateway: $IGW_ID"

# Create subnets
SUBNET_PUBLIC=$(aws ec2 create-subnet --vpc-id $VPC_ID --cidr-block 10.0.1.0/24 --availability-zone us-east-1a --query 'Subnet.SubnetId' --output text)
SUBNET_PRIVATE=$(aws ec2 create-subnet --vpc-id $VPC_ID --cidr-block 10.0.2.0/24 --availability-zone us-east-1b --query 'Subnet.SubnetId' --output text)
echo "Created Subnets: $SUBNET_PUBLIC (public), $SUBNET_PRIVATE (private)"

# Create route table for public subnet
ROUTE_TABLE_PUBLIC=$(aws ec2 create-route-table --vpc-id $VPC_ID --query 'RouteTable.RouteTableId' --output text)
aws ec2 create-route --route-table-id $ROUTE_TABLE_PUBLIC --destination-cidr-block 0.0.0.0/0 --gateway-id $IGW_ID
aws ec2 associate-route-table --subnet-id $SUBNET_PUBLIC --route-table-id $ROUTE_TABLE_PUBLIC

# Create NAT Gateway
NAT_ALLOCATION=$(aws ec2 allocate-address --domain vpc --query 'AllocationId' --output text)
NAT_GW_ID=$(aws ec2 create-nat-gateway --subnet-id $SUBNET_PUBLIC --allocation-id $NAT_ALLOCATION --query 'NatGateway.NatGatewayId' --output text)
echo "Created NAT Gateway: $NAT_GW_ID"

# Create Security Groups
SG_WEB=$(aws ec2 create-security-group --group-name web-sg --description "Web server security group" --vpc-id $VPC_ID --query 'GroupId' --output text)
SG_DB=$(aws ec2 create-security-group --group-name db-sg --description "Database security group" --vpc-id $VPC_ID --query 'GroupId' --output text)

# Add security group rules
aws ec2 authorize-security-group-ingress --group-id $SG_WEB --protocol tcp --port 80 --cidr 0.0.0.0/0
aws ec2 authorize-security-group-ingress --group-id $SG_WEB --protocol tcp --port 443 --cidr 0.0.0.0/0
aws ec2 authorize-security-group-ingress --group-id $SG_DB --protocol tcp --port 3306 --source-group $SG_WEB

echo "Created Security Groups: $SG_WEB (web), $SG_DB (database)"

# Create Network ACLs
NACL_ID=$(aws ec2 create-network-acl --vpc-id $VPC_ID --query 'NetworkAcl.NetworkAclId' --output text)
aws ec2 create-network-acl-entry --network-acl-id $NACL_ID --rule-number 100 --protocol tcp --rule-action allow --port-range From=80,To=80 --cidr-block 0.0.0.0/0
echo "Created Network ACL: $NACL_ID"

# Enable VPC Flow Logs
aws ec2 create-flow-logs --resource-type VPC --resource-ids $VPC_ID --traffic-type ALL --log-destination-type cloud-watch-logs --log-group-name /aws/vpc/flowlogs

echo "💾 Setting up S3 Buckets..."

# Create S3 buckets with various configurations
aws s3 mb s3://pci-compliance-logs-bucket
aws s3 mb s3://pci-compliance-data-bucket
aws s3 mb s3://pci-compliance-backups-bucket

# Set bucket encryption
aws s3api put-bucket-encryption --bucket pci-compliance-data-bucket --server-side-encryption-configuration '{
    "Rules": [
        {
            "ApplyServerSideEncryptionByDefault": {
                "SSEAlgorithm": "AES256"
            }
        }
    ]
}'

# Set bucket versioning
aws s3api put-bucket-versioning --bucket pci-compliance-data-bucket --versioning-configuration Status=Enabled

# Set bucket public access block
aws s3api put-public-access-block --bucket pci-compliance-data-bucket --public-access-block-configuration "BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true"

# Set bucket logging
aws s3api put-bucket-logging --bucket pci-compliance-data-bucket --bucket-logging-status '{
    "LoggingEnabled": {
        "TargetBucket": "pci-compliance-logs-bucket",
        "TargetPrefix": "access-logs/"
    }
}'

echo "👤 Setting up IAM..."

# Create IAM roles
aws iam create-role --role-name PCI-ComplianceRole --assume-role-policy-document '{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Service": "ec2.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        }
    ]
}'

aws iam create-role --role-name LambdaExecutionRole --assume-role-policy-document '{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Service": "lambda.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        }
    ]
}'

# Create IAM users
aws iam create-user --user-name pci-admin-user
aws iam create-user --user-name pci-readonly-user

# Create IAM groups
aws iam create-group --group-name PCI-Administrators
aws iam create-group --group-name PCI-ReadOnlyUsers

# Create IAM policies
aws iam create-policy --policy-name PCI-CompliancePolicy --policy-document '{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:PutObject"
            ],
            "Resource": "arn:aws:s3:::pci-compliance-data-bucket/*"
        }
    ]
}'

# Set account password policy
aws iam update-account-password-policy --minimum-password-length 12 --require-symbols --require-numbers --require-uppercase-characters --require-lowercase-characters --allow-users-to-change-password --max-password-age 90

echo "🖥️  Setting up EC2 Instances..."

# Create key pair
aws ec2 create-key-pair --key-name pci-compliance-key --query 'KeyMaterial' --output text > pci-compliance-key.pem

# Get a valid AMI ID for LocalStack (use Amazon Linux 2)
AMI_ID=$(aws ec2 describe-images --owners amazon --filters "Name=name,Values=amzn2-ami-hvm-*" --query 'Images[0].ImageId' --output text 2>/dev/null || echo "ami-0abcdef1234567890")

# Launch EC2 instances
INSTANCE_WEB=$(aws ec2 run-instances --image-id $AMI_ID --count 1 --instance-type t2.micro --key-name pci-compliance-key --security-group-ids $SG_WEB --subnet-id $SUBNET_PUBLIC --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=PCI-Web-Server},{Key=Environment,Value=Production}]' --query 'Instances[0].InstanceId' --output text)

INSTANCE_DB=$(aws ec2 run-instances --image-id $AMI_ID --count 1 --instance-type t2.micro --key-name pci-compliance-key --security-group-ids $SG_DB --subnet-id $SUBNET_PRIVATE --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=PCI-DB-Server},{Key=Environment,Value=Production}]' --query 'Instances[0].InstanceId' --output text)

echo "Created EC2 Instances: $INSTANCE_WEB (web), $INSTANCE_DB (database)"

# Create EBS volumes
VOLUME_DATA=$(aws ec2 create-volume --size 20 --volume-type gp3 --availability-zone us-east-1a --encrypted --tag-specifications 'ResourceType=volume,Tags=[{Key=Name,Value=PCI-Data-Volume}]' --query 'VolumeId' --output text)
echo "Created EBS Volume: $VOLUME_DATA"

# Create snapshots
aws ec2 create-snapshot --volume-id $VOLUME_DATA --description "PCI Compliance data backup"

echo "🔐 Setting up KMS..."

# Create KMS keys
KMS_KEY=$(aws kms create-key --description "PCI Compliance encryption key" --query 'KeyMetadata.KeyId' --output text)
aws kms create-alias --alias-name alias/pci-compliance-key --target-key-id $KMS_KEY
echo "Created KMS Key: $KMS_KEY"

echo "✅ Core Infrastructure setup complete!" 