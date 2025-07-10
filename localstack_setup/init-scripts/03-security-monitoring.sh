#!/bin/bash

echo "=== Setting up Security and Monitoring Services ==="

# Set AWS CLI to use LocalStack
export AWS_ACCESS_KEY_ID=test
export AWS_SECRET_ACCESS_KEY=test
export AWS_DEFAULT_REGION=us-east-1
export AWS_ENDPOINT_URL=http://localhost:4566

echo "👁️  Setting up CloudTrail..."

# Create CloudTrail
aws cloudtrail create-trail \
    --name PCI-AuditTrail \
    --s3-bucket-name pci-compliance-logs-bucket \
    --s3-key-prefix cloudtrail-logs/ \
    --include-global-service-events \
    --is-multi-region-trail \
    --enable-log-file-validation

# Start logging
aws cloudtrail start-logging --name PCI-AuditTrail

# Create additional trail for data events
aws cloudtrail create-trail \
    --name PCI-DataEventsTrail \
    --s3-bucket-name pci-compliance-logs-bucket \
    --s3-key-prefix data-events/ \
    --include-global-service-events \
    --is-multi-region-trail

echo "📊 Setting up CloudWatch..."

# Create CloudWatch log groups
aws logs create-log-group --log-group-name /aws/vpc/flowlogs
aws logs create-log-group --log-group-name /aws/lambda/pci-functions
aws logs create-log-group --log-group-name /aws/apigateway/access-logs
aws logs create-log-group --log-group-name /aws/rds/instance/pci-mysql-primary/audit
aws logs create-log-group --log-group-name /aws/ecs/pci-application
aws logs create-log-group --log-group-name /aws/eks/pci-cluster/cluster

# Create CloudWatch alarms
aws cloudwatch put-metric-alarm \
    --alarm-name "PCI-UnauthorizedAPIAccess" \
    --alarm-description "Alarm for unauthorized API access attempts" \
    --metric-name "4XXError" \
    --namespace "AWS/ApiGateway" \
    --statistic Sum \
    --period 300 \
    --threshold 10 \
    --comparison-operator GreaterThanThreshold \
    --evaluation-periods 1

aws cloudwatch put-metric-alarm \
    --alarm-name "PCI-HighCPUUsage" \
    --alarm-description "Alarm for high CPU usage" \
    --metric-name "CPUUtilization" \
    --namespace "AWS/EC2" \
    --statistic Average \
    --period 300 \
    --threshold 80 \
    --comparison-operator GreaterThanThreshold \
    --evaluation-periods 2

aws cloudwatch put-metric-alarm \
    --alarm-name "PCI-DatabaseConnections" \
    --alarm-description "Alarm for high database connections" \
    --metric-name "DatabaseConnections" \
    --namespace "AWS/RDS" \
    --statistic Average \
    --period 300 \
    --threshold 50 \
    --comparison-operator GreaterThanThreshold \
    --evaluation-periods 1

echo "⚙️  Setting up AWS Config..."

# Create configuration recorder
aws configservice put-configuration-recorder \
    --configuration-recorder name=PCI-ConfigRecorder,roleARN=arn:aws:iam::000000000000:role/aws-config-role,recordingGroup='{
        "allSupported": true,
        "includeGlobalResourceTypes": true,
        "resourceTypes": []
    }'

# Create delivery channel
aws configservice put-delivery-channel \
    --delivery-channel name=PCI-DeliveryChannel,s3BucketName=pci-compliance-logs-bucket,s3KeyPrefix=config/

# Start configuration recorder
aws configservice start-configuration-recorder --configuration-recorder-name PCI-ConfigRecorder

# Create Config rules
aws configservice put-config-rule \
    --config-rule '{
        "ConfigRuleName": "s3-bucket-public-access-prohibited",
        "Source": {
            "Owner": "AWS",
            "SourceIdentifier": "S3_BUCKET_PUBLIC_ACCESS_PROHIBITED"
        }
    }'

aws configservice put-config-rule \
    --config-rule '{
        "ConfigRuleName": "encrypted-volumes",
        "Source": {
            "Owner": "AWS",
            "SourceIdentifier": "ENCRYPTED_VOLUMES"
        }
    }'

aws configservice put-config-rule \
    --config-rule '{
        "ConfigRuleName": "rds-storage-encrypted",
        "Source": {
            "Owner": "AWS",
            "SourceIdentifier": "RDS_STORAGE_ENCRYPTED"
        }
    }'

echo "🛡️  Setting up GuardDuty..."

# Create GuardDuty detector
DETECTOR_ID=$(aws guardduty create-detector \
    --enable \
    --finding-publishing-frequency FIFTEEN_MINUTES \
    --query 'DetectorId' --output text)

echo "Created GuardDuty Detector: $DETECTOR_ID"

# Enable S3 protection
aws guardduty update-detector \
    --detector-id $DETECTOR_ID \
    --data-sources '{
        "S3Logs": {
            "Enable": true
        },
        "Kubernetes": {
            "AuditLogs": {
                "Enable": true
            }
        },
        "MalwareProtection": {
            "ScanEc2InstanceWithFindings": {
                "EbsVolumes": true
            }
        }
    }'

echo "🔒 Setting up Secrets Manager..."

# Create secrets
aws secretsmanager create-secret \
    --name PCI/database/credentials \
    --description "Database credentials for PCI compliance" \
    --secret-string '{"username":"admin","password":"SecurePassword123!"}'

aws secretsmanager create-secret \
    --name PCI/api/keys \
    --description "API keys for PCI compliance" \
    --secret-string '{"api_key":"secret-api-key-12345","webhook_secret":"webhook-secret-67890"}'

aws secretsmanager create-secret \
    --name PCI/encryption/keys \
    --description "Encryption keys for PCI compliance" \
    --secret-string '{"master_key":"master-encryption-key-abcdef"}'

echo "🔐 Setting up ACM Certificates..."

# Request ACM certificates
aws acm request-certificate \
    --domain-name "*.pci-compliance.example.com" \
    --subject-alternative-names "pci-compliance.example.com" \
    --validation-method DNS

aws acm request-certificate \
    --domain-name "api.pci-compliance.example.com" \
    --validation-method DNS

echo "🔍 Setting up Security Hub..."

# Enable Security Hub
aws securityhub enable-security-hub

# Subscribe to security standards
aws securityhub batch-enable-standards \
    --standards-subscription-requests StandardsArn=arn:aws:securityhub:::ruleset/finding-format/aws-foundational-security/v/1.0.0

aws securityhub batch-enable-standards \
    --standards-subscription-requests StandardsArn=arn:aws:securityhub:::standard/pci-dss/v/3.2.1

echo "🔎 Setting up Inspector..."

# Create assessment target
aws inspector create-assessment-target \
    --assessment-target-name PCI-EC2-Assessment \
    --resource-group-arn arn:aws:inspector:us-east-1:000000000000:resourcegroup/0-example

# Create assessment template  
aws inspector create-assessment-template \
    --assessment-target-arn arn:aws:inspector:us-east-1:000000000000:target/0-example \
    --assessment-template-name PCI-SecurityAssessment \
    --duration-in-seconds 3600 \
    --rules-package-arns arn:aws:inspector:us-east-1:316112463485:rulespackage/0-gEjTy7T7

echo "🔧 Setting up Systems Manager..."

# Create SSM parameters
aws ssm put-parameter \
    --name "/pci/database/endpoint" \
    --value "pci-mysql-primary.cluster-123.us-east-1.rds.amazonaws.com" \
    --type "SecureString" \
    --description "Database endpoint for PCI compliance"

aws ssm put-parameter \
    --name "/pci/application/config" \
    --value '{"debug":false,"encryption":true,"audit_level":"high"}' \
    --type "SecureString" \
    --description "Application configuration for PCI compliance"

# Create patch baseline
aws ssm create-patch-baseline \
    --name "PCI-PatchBaseline" \
    --operating-system "AMAZON_LINUX_2" \
    --approval-rules '{
        "PatchRules": [
            {
                "PatchFilterGroup": {
                    "PatchFilters": [
                        {
                            "Key": "CLASSIFICATION",
                            "Values": ["Security", "Bugfix", "Critical"]
                        }
                    ]
                },
                "ApproveAfterDays": 0,
                "EnableNonSecurity": false
            }
        ]
    }' \
    --approved-patches "[]" \
    --rejected-patches "[]"

echo "🏭 Setting up CloudFormation..."

# Create a simple CloudFormation stack
cat > /tmp/pci-infrastructure.yaml << 'EOF'
AWSTemplateFormatVersion: '2010-09-09'
Description: 'PCI Compliance Infrastructure Stack'
Resources:
  PCILogBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: pci-cloudformation-logs
      PublicAccessBlockConfiguration:
        BlockPublicAcls: true
        BlockPublicPolicy: true
        IgnorePublicAcls: true
        RestrictPublicBuckets: true
      BucketEncryption:
        ServerSideEncryptionConfiguration:
          - ServerSideEncryptionByDefault:
              SSEAlgorithm: AES256
Outputs:
  BucketName:
    Description: 'PCI Log Bucket Name'
    Value: !Ref PCILogBucket
EOF

aws cloudformation create-stack \
    --stack-name PCI-Infrastructure \
    --template-body file:///tmp/pci-infrastructure.yaml

echo "🚀 Setting up CodeBuild and CodePipeline..."

# Create CodeBuild project
aws codebuild create-project \
    --name PCI-SecurityScan \
    --description "Security scanning for PCI compliance" \
    --service-role arn:aws:iam::000000000000:role/codebuild-service-role \
    --artifacts type=NO_ARTIFACTS \
    --environment type=LINUX_CONTAINER,image=aws/codebuild/standard:5.0,computeType=BUILD_GENERAL1_MEDIUM \
    --source type=NO_SOURCE,buildspec="version: 0.2\nphases:\n  build:\n    commands:\n      - echo 'Running security scan'"

# Create CodePipeline
aws codepipeline create-pipeline \
    --pipeline '{
        "name": "PCI-SecurityPipeline",
        "roleArn": "arn:aws:iam::000000000000:role/codepipeline-service-role",
        "artifactStore": {
            "type": "S3",
            "location": "pci-compliance-logs-bucket"
        },
        "stages": [
            {
                "name": "Source",
                "actions": [
                    {
                        "name": "SourceAction",
                        "actionTypeId": {
                            "category": "Source",
                            "owner": "AWS",
                            "provider": "S3",
                            "version": "1"
                        },
                        "configuration": {
                            "S3Bucket": "pci-compliance-logs-bucket",
                            "S3ObjectKey": "source.zip"
                        },
                        "outputArtifacts": [
                            {
                                "name": "SourceOutput"
                            }
                        ]
                    }
                ]
            },
            {
                "name": "Build",
                "actions": [
                    {
                        "name": "BuildAction",
                        "actionTypeId": {
                            "category": "Build",
                            "owner": "AWS",
                            "provider": "CodeBuild",
                            "version": "1"
                        },
                        "configuration": {
                            "ProjectName": "PCI-SecurityScan"
                        },
                        "inputArtifacts": [
                            {
                                "name": "SourceOutput"
                            }
                        ]
                    }
                ]
            }
        ]
    }'

echo "🛡️  Setting up WAF..."

# Create WAF Web ACL (v2)
aws wafv2 create-web-acl \
    --name PCI-WebACL \
    --scope REGIONAL \
    --default-action Allow={} \
    --description "WAF for PCI compliance" \
    --rules '[
        {
            "Name": "SQLInjectionRule",
            "Priority": 1,
            "Statement": {
                "SqliMatchStatement": {
                    "FieldToMatch": {
                        "Body": {}
                    },
                    "TextTransformations": [
                        {
                            "Priority": 1,
                            "Type": "URL_DECODE"
                        }
                    ]
                }
            },
            "Action": {
                "Block": {}
            },
            "VisibilityConfig": {
                "SampledRequestsEnabled": true,
                "CloudWatchMetricsEnabled": true,
                "MetricName": "SQLInjectionRule"
            }
        }
    ]'

echo "🌍 Setting up Route53..."

# Create hosted zone
aws route53 create-hosted-zone \
    --name pci-compliance.example.com \
    --caller-reference $(date +%s) \
    --hosted-zone-config Comment="PCI Compliance domain"

echo "🔥 Setting up Network Firewall..."

# Create firewall policy
aws network-firewall create-firewall-policy \
    --firewall-policy-name PCI-FirewallPolicy \
    --firewall-policy '{
        "StatelessDefaultActions": ["aws:forward_to_sfe"],
        "StatelessFragmentDefaultActions": ["aws:forward_to_sfe"],
        "StatefulRuleGroupReferences": []
    }'

echo "📊 Setting up EventBridge..."

# Create custom event bus
aws events create-event-bus --name PCI-SecurityEvents

# Create EventBridge rule
aws events put-rule \
    --name PCI-SecurityAlertRule \
    --event-pattern '{
        "source": ["aws.guardduty", "aws.securityhub"],
        "detail-type": ["GuardDuty Finding", "Security Hub Findings - Imported"]
    }' \
    --state ENABLED \
    --description "Rule for PCI security alerts"

echo "✅ Security and Monitoring Services setup complete!" 