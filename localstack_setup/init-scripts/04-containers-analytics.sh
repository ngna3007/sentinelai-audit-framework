#!/bin/bash

echo "=== Setting up Container Services and Analytics ==="

# Set AWS CLI to use LocalStack
export AWS_ACCESS_KEY_ID=test
export AWS_SECRET_ACCESS_KEY=test
export AWS_DEFAULT_REGION=us-east-1
export AWS_ENDPOINT_URL=http://localhost:4566

echo "🐳 Setting up ECS..."

# Create ECS cluster
aws ecs create-cluster --cluster-name PCI-ApplicationCluster

# Register task definition
aws ecs register-task-definition \
    --family pci-web-app \
    --network-mode awsvpc \
    --requires-compatibilities FARGATE \
    --cpu 256 \
    --memory 512 \
    --execution-role-arn arn:aws:iam::000000000000:role/ecsTaskExecutionRole \
    --container-definitions '[
        {
            "name": "pci-web-container",
            "image": "nginx:latest",
            "portMappings": [
                {
                    "containerPort": 80,
                    "protocol": "tcp"
                }
            ],
            "essential": true,
            "logConfiguration": {
                "logDriver": "awslogs",
                "options": {
                    "awslogs-group": "/aws/ecs/pci-application",
                    "awslogs-region": "us-east-1",
                    "awslogs-stream-prefix": "web"
                }
            }
        }
    ]'

# Register another task definition for background processing
aws ecs register-task-definition \
    --family pci-background-processor \
    --network-mode awsvpc \
    --requires-compatibilities FARGATE \
    --cpu 512 \
    --memory 1024 \
    --execution-role-arn arn:aws:iam::000000000000:role/ecsTaskExecutionRole \
    --container-definitions '[
        {
            "name": "pci-processor-container",
            "image": "alpine:latest",
            "command": ["sh", "-c", "while true; do echo Processing PCI data; sleep 60; done"],
            "essential": true,
            "logConfiguration": {
                "logDriver": "awslogs",
                "options": {
                    "awslogs-group": "/aws/ecs/pci-application", 
                    "awslogs-region": "us-east-1",
                    "awslogs-stream-prefix": "processor"
                }
            }
        }
    ]'

# Create ECS service
aws ecs create-service \
    --cluster PCI-ApplicationCluster \
    --service-name pci-web-service \
    --task-definition pci-web-app:1 \
    --desired-count 2 \
    --launch-type FARGATE \
    --network-configuration '{
        "awsvpcConfiguration": {
            "subnets": ["subnet-12345"],
            "securityGroups": ["sg-12345"],
            "assignPublicIp": "ENABLED"
        }
    }'

echo "☸️  Setting up EKS..."

# Create EKS cluster
aws eks create-cluster \
    --name pci-kubernetes-cluster \
    --version 1.28 \
    --role-arn arn:aws:iam::000000000000:role/eks-service-role \
    --resources-vpc-config subnetIds=subnet-12345,subnet-67890,securityGroupIds=sg-12345 \
    --logging '{
        "enable": [
            {
                "types": ["api", "audit", "authenticator", "controllerManager", "scheduler"]
            }
        ]
    }'

echo "📦 Setting up ECR..."

# Create ECR repositories
aws ecr create-repository \
    --repository-name pci-compliance/web-app \
    --image-scanning-configuration scanOnPush=true \
    --encryption-configuration encryptionType=AES256

aws ecr create-repository \
    --repository-name pci-compliance/data-processor \
    --image-scanning-configuration scanOnPush=true \
    --encryption-configuration encryptionType=AES256

aws ecr create-repository \
    --repository-name pci-compliance/security-scanner \
    --image-scanning-configuration scanOnPush=true \
    --encryption-configuration encryptionType=AES256

echo "📊 Setting up Kinesis..."

# Create Kinesis streams
aws kinesis create-stream \
    --stream-name PCI-TransactionStream \
    --shard-count 2

aws kinesis create-stream \
    --stream-name PCI-AuditLogStream \
    --shard-count 1

aws kinesis create-stream \
    --stream-name PCI-SecurityEventStream \
    --shard-count 1

# Enable server-side encryption
aws kinesis enable-stream-encryption \
    --stream-name PCI-TransactionStream \
    --encryption-type KMS \
    --key-id alias/aws/kinesis

echo "🎯 Setting up Kinesis Analytics..."

# Create Kinesis Analytics application
aws kinesisanalytics create-application \
    --application-name PCI-FraudDetection \
    --application-description "Real-time fraud detection for PCI compliance" \
    --inputs '[
        {
            "NamePrefix": "TransactionInput",
            "KinesisStreamsInput": {
                "ResourceARN": "arn:aws:kinesis:us-east-1:000000000000:stream/PCI-TransactionStream",
                "RoleARN": "arn:aws:iam::000000000000:role/kinesis-analytics-role"
            },
            "InputSchema": {
                "RecordColumns": [
                    {
                        "Name": "transaction_id",
                        "SqlType": "VARCHAR(32)",
                        "Mapping": "$.transaction_id"
                    },
                    {
                        "Name": "amount",
                        "SqlType": "DECIMAL(10,2)",
                        "Mapping": "$.amount"
                    },
                    {
                        "Name": "timestamp",
                        "SqlType": "TIMESTAMP",
                        "Mapping": "$.timestamp"
                    }
                ],
                "RecordFormat": {
                    "RecordFormatType": "JSON",
                    "MappingParameters": {
                        "JSONMappingParameters": {
                            "RecordRowPath": "$"
                        }
                    }
                }
            }
        }
    ]'

echo "🚀 Setting up EMR..."

# Create EMR cluster
aws emr create-cluster \
    --name "PCI-DataAnalytics" \
    --release-label emr-6.15.0 \
    --instances '{
        "InstanceGroups": [
            {
                "Name": "Master",
                "Market": "ON_DEMAND",
                "InstanceRole": "MASTER",
                "InstanceType": "m5.xlarge",
                "InstanceCount": 1
            },
            {
                "Name": "Workers",
                "Market": "ON_DEMAND", 
                "InstanceRole": "CORE",
                "InstanceType": "m5.large",
                "InstanceCount": 2
            }
        ],
        "Ec2KeyName": "pci-compliance-key",
        "KeepJobFlowAliveWhenNoSteps": true,
        "Ec2SubnetId": "subnet-12345"
    }' \
    --applications Name=Hadoop Name=Spark Name=Hive \
    --service-role EMR_DefaultRole \
    --ec2-attributes InstanceProfile=EMR_EC2_DefaultRole \
    --security-configuration '{
        "EncryptionConfiguration": {
            "AtRestEncryptionConfiguration": {
                "S3EncryptionConfiguration": {
                    "EncryptionMode": "SSE-S3"
                },
                "LocalDiskEncryptionConfiguration": {
                    "EncryptionKeyProviderType": "AwsKms",
                    "AwsKmsKey": "alias/aws/elasticmapreduce"
                }
            },
            "InTransitEncryptionConfiguration": {
                "TLSEncryptionConfiguration": {
                    "CertificateProviderType": "PEM",
                    "S3Object": "s3://pci-compliance-logs-bucket/certificates/"
                }
            }
        }
    }'

echo "🔍 Setting up Athena..."

# Create Athena workgroup
aws athena create-work-group \
    --name PCI-AnalyticsWorkgroup \
    --description "Workgroup for PCI compliance analytics" \
    --configuration '{
        "ResultConfigurationUpdates": {
            "OutputLocation": "s3://pci-compliance-logs-bucket/athena-results/",
            "EncryptionConfiguration": {
                "EncryptionOption": "SSE_S3"
            }
        },
        "EnforceWorkGroupConfiguration": true,
        "PublishCloudWatchMetrics": true
    }'

echo "🏭 Setting up MSK (Managed Streaming for Kafka)..."

# Create MSK cluster
aws kafka create-cluster \
    --cluster-name PCI-EventStreaming \
    --broker-node-group-info '{
        "InstanceType": "kafka.t3.small",
        "ClientSubnets": ["subnet-12345", "subnet-67890"],
        "SecurityGroups": ["sg-12345"],
        "StorageInfo": {
            "EBSStorageInfo": {
                "VolumeSize": 20
            }
        }
    }' \
    --kafka-version 2.8.1 \
    --number-of-broker-nodes 2 \
    --encryption-info '{
        "EncryptionAtRest": {
            "DataVolumeKMSKeyId": "alias/aws/kafka"
        },
        "EncryptionInTransit": {
            "ClientBroker": "TLS",
            "InCluster": true
        }
    }' \
    --enhanced-monitoring PER_TOPIC_PER_BROKER

echo "💻 Setting up WorkSpaces..."

# Create WorkSpaces directory
aws workspaces create-workspace-directory \
    --directory-id d-1234567890 \
    --subnet-ids subnet-12345 subnet-67890 \
    --enable-internet-access \
    --enable-work-docs

# Create WorkSpace
aws workspaces create-workspaces \
    --workspaces '[
        {
            "DirectoryId": "d-1234567890",
            "UserName": "pci-admin",
            "BundleId": "wsb-123456789",
            "UserVolumeEncryptionEnabled": true,
            "RootVolumeEncryptionEnabled": true,
            "WorkspaceProperties": {
                "RunningMode": "AUTO_STOP",
                "RunningModeAutoStopTimeoutInMinutes": 60,
                "ComputeTypeName": "STANDARD"
            },
            "Tags": [
                {
                    "Key": "Environment",
                    "Value": "PCI-Compliance"
                }
            ]
        }
    ]'

echo "🖥️  Setting up AppStream..."

# Create AppStream fleet
aws appstream create-fleet \
    --name PCI-SecureDesktop \
    --image-name AppStream-WinServer2019-07-16-2021 \
    --instance-type stream.standard.medium \
    --compute-capacity DesiredInstances=1 \
    --vpc-config SubnetIds=subnet-12345,SecurityGroupIds=sg-12345 \
    --stream-view DESKTOP \
    --max-user-duration-in-seconds 3600 \
    --disconnect-timeout-in-seconds 300 \
    --idle-disconnect-timeout-in-seconds 600 \
    --enable-default-internet-access false

# Create AppStream stack
aws appstream create-stack \
    --name PCI-SecureApplications \
    --description "Secure applications for PCI compliance" \
    --display-name "PCI Secure Apps" \
    --storage-connectors '[
        {
            "ConnectorType": "HOMEFOLDERS",
            "ResourceIdentifier": "pci-compliance-data-bucket"
        }
    ]' \
    --user-settings '[
        {
            "Action": "CLIPBOARD_COPY_FROM_LOCAL_DEVICE",
            "Permission": "DISABLED"
        },
        {
            "Action": "CLIPBOARD_COPY_TO_LOCAL_DEVICE", 
            "Permission": "DISABLED"
        },
        {
            "Action": "FILE_UPLOAD",
            "Permission": "DISABLED"
        },
        {
            "Action": "FILE_DOWNLOAD",
            "Permission": "DISABLED"
        }
    ]'

echo "🧠 Setting up SageMaker..."

# Create SageMaker notebook instance
aws sagemaker create-notebook-instance \
    --notebook-instance-name PCI-MLAnalytics \
    --instance-type ml.t3.medium \
    --role-arn arn:aws:iam::000000000000:role/SageMakerExecutionRole \
    --subnet-id subnet-12345 \
    --security-group-ids sg-12345 \
    --kms-key-id alias/aws/sagemaker \
    --direct-internet-access Disabled \
    --volume-size-in-gb 20 \
    --root-access Disabled

echo "📧 Setting up WorkMail..."

# Create WorkMail organization
aws workmail create-organization \
    --directory-id d-1234567890 \
    --alias pci-compliance-mail \
    --enable-interoperability false \
    --kms-key-id alias/aws/workmail \
    --domains '[
        {
            "DomainName": "pci-compliance.example.com",
            "HostedZoneId": "Z123456789"
        }
    ]'

echo "🔄 Setting up Transfer Family..."

# Create SFTP server
aws transfer create-server \
    --endpoint-type VPC \
    --endpoint-details VpcId=vpc-12345,SubnetIds=subnet-12345,SecurityGroupIds=sg-12345 \
    --protocols SFTP \
    --identity-provider-type SERVICE_MANAGED \
    --logging-role arn:aws:iam::000000000000:role/transfer-logging-role \
    --security-policy-name TransferSecurityPolicy-2020-06

echo "🔄 Setting up DMS..."

# Create DMS replication instance
aws dms create-replication-instance \
    --replication-instance-identifier pci-replication-instance \
    --replication-instance-class dms.t3.micro \
    --allocated-storage 20 \
    --vpc-security-group-ids sg-12345 \
    --replication-subnet-group-identifier pci-dms-subnet-group \
    --publicly-accessible false \
    --storage-encrypted \
    --kms-key-id alias/aws/dms

echo "📡 Setting up MQ..."

# Create Amazon MQ broker
aws mq create-broker \
    --broker-name PCI-MessageBroker \
    --deployment-mode SINGLE_INSTANCE \
    --engine-type ACTIVEMQ \
    --engine-version 5.17.6 \
    --host-instance-type mq.t3.micro \
    --auto-minor-version-upgrade \
    --publicly-accessible false \
    --security-groups sg-12345 \
    --subnet-ids subnet-12345 \
    --users '[
        {
            "Username": "admin",
            "Password": "SecurePassword123!",
            "ConsoleAccess": true
        }
    ]' \
    --logs '{
        "Audit": true,
        "General": true
    }' \
    --encryption-options '{
        "UseAwsOwnedKey": false,
        "KmsKeyId": "alias/aws/mq"
    }'

echo "🛡️  Setting up AWS Backup..."

# Create backup vault
aws backup create-backup-vault \
    --backup-vault-name PCI-ComplianceVault \
    --encryption-key-arn arn:aws:kms:us-east-1:000000000000:key/12345678-1234-1234-1234-123456789012

# Create backup plan
aws backup create-backup-plan \
    --backup-plan '{
        "BackupPlanName": "PCI-CompliancePlan",
        "Rules": [
            {
                "RuleName": "DailyBackups",
                "TargetBackupVault": "PCI-ComplianceVault",
                "ScheduleExpression": "cron(0 5 ? * * *)",
                "StartWindowMinutes": 480,
                "CompletionWindowMinutes": 10080,
                "Lifecycle": {
                    "MoveToColdStorageAfterDays": 30,
                    "DeleteAfterDays": 120
                },
                "RecoveryPointTags": {
                    "Environment": "PCI-Compliance"
                }
            }
        ]
    }'

echo "✅ Container Services and Analytics setup complete!" 