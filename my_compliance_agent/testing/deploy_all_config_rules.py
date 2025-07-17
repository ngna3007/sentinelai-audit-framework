#!/usr/bin/env python3
"""
Deploy ALL AWS Config Rules Script
Deploys all available AWS managed Config rules using explicit credentials
Includes prerequisite setup and comprehensive deployment
"""

import json
import os
import boto3
import time
from botocore.exceptions import ClientError, NoCredentialsError
from datetime import datetime


class AWSConfigRulesDeployer:
    def __init__(self, access_key_id, secret_access_key, session_token=None, region='us-east-1'):
        """Initialize with explicit credentials"""
        self.region = region
        
        try:
            # Create session with explicit credentials
            self.session = boto3.Session(
                aws_access_key_id=access_key_id,
                aws_secret_access_key=secret_access_key,
                aws_session_token=session_token,
                region_name=region
            )
            
            # Initialize clients
            self.config_client = self.session.client('config')
            self.sts_client = self.session.client('sts')
            self.iam_client = self.session.client('iam')
            self.s3_client = self.session.client('s3')
            
            # Get account info
            identity = self.sts_client.get_caller_identity()
            self.account_id = identity['Account']
            self.user_arn = identity['Arn']
            
            print(f"✅ Connected to AWS Account: {self.account_id}")
            print(f"📍 Region: {self.region}")
            
        except Exception as e:
            raise Exception(f"❌ AWS connection failed: {e}")

    def setup_config_prerequisites(self):
        """Setup AWS Config prerequisites (IAM role, S3 bucket, delivery channel)"""
        print(f"\n🔧 Setting up AWS Config prerequisites...")
        
        try:
            # Step 1: Create or verify IAM role for Config
            role_name = 'aws-config-role'
            role_arn = f"arn:aws:iam::{self.account_id}:role/{role_name}"
            
            print(f"   Creating IAM role: {role_name}...")
            
            trust_policy = {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Effect": "Allow",
                        "Principal": {"Service": "config.amazonaws.com"},
                        "Action": "sts:AssumeRole"
                    }
                ]
            }
            
            try:
                self.iam_client.create_role(
                    RoleName=role_name,
                    AssumeRolePolicyDocument=json.dumps(trust_policy),
                    Description='AWS Config service role for compliance monitoring'
                )
                print(f"   ✅ Created IAM role")
            except ClientError as e:
                if 'EntityAlreadyExists' in str(e):
                    print(f"   ✅ IAM role already exists")
                else:
                    raise e
            
            # Attach required policies
            policies = [
                'arn:aws:iam::aws:policy/service-role/ConfigRole',
                'arn:aws:iam::aws:policy/service-role/AWS_ConfigRole'
            ]
            
            for policy_arn in policies:
                try:
                    self.iam_client.attach_role_policy(
                        RoleName=role_name,
                        PolicyArn=policy_arn
                    )
                except ClientError as e:
                    if 'NoSuchEntity' not in str(e):
                        pass  # Policy might already be attached
            
            print(f"   ✅ Attached required policies")
            
            # Step 2: Create or verify S3 bucket
            bucket_name = f"aws-config-bucket-{self.account_id}-{self.region}"
            
            print(f"   Creating S3 bucket: {bucket_name}...")
            
            try:
                if self.region == 'us-east-1':
                    self.s3_client.create_bucket(Bucket=bucket_name)
                else:
                    self.s3_client.create_bucket(
                        Bucket=bucket_name,
                        CreateBucketConfiguration={'LocationConstraint': self.region}
                    )
                print(f"   ✅ Created S3 bucket")
            except ClientError as e:
                if 'BucketAlreadyOwnedByYou' in str(e) or 'BucketAlreadyExists' in str(e):
                    print(f"   ✅ S3 bucket already exists")
                else:
                    raise e
            
            # Step 3: Setup bucket policy for Config
            bucket_policy = {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Sid": "AWSConfigBucketPermissionsCheck",
                        "Effect": "Allow",
                        "Principal": {"Service": "config.amazonaws.com"},
                        "Action": "s3:GetBucketAcl",
                        "Resource": f"arn:aws:s3:::{bucket_name}",
                        "Condition": {
                            "StringEquals": {
                                "AWS:SourceAccount": self.account_id
                            }
                        }
                    },
                    {
                        "Sid": "AWSConfigBucketExistenceCheck", 
                        "Effect": "Allow",
                        "Principal": {"Service": "config.amazonaws.com"},
                        "Action": "s3:ListBucket",
                        "Resource": f"arn:aws:s3:::{bucket_name}",
                        "Condition": {
                            "StringEquals": {
                                "AWS:SourceAccount": self.account_id
                            }
                        }
                    },
                    {
                        "Sid": "AWSConfigBucketDelivery",
                        "Effect": "Allow", 
                        "Principal": {"Service": "config.amazonaws.com"},
                        "Action": "s3:PutObject",
                        "Resource": f"arn:aws:s3:::{bucket_name}/AWSLogs/{self.account_id}/Config/*",
                        "Condition": {
                            "StringEquals": {
                                "s3:x-amz-acl": "bucket-owner-full-control",
                                "AWS:SourceAccount": self.account_id
                            }
                        }
                    }
                ]
            }
            
            try:
                self.s3_client.put_bucket_policy(
                    Bucket=bucket_name,
                    Policy=json.dumps(bucket_policy)
                )
                print(f"   ✅ Applied S3 bucket policy")
            except ClientError as e:
                print(f"   ⚠️ Warning: Could not set bucket policy: {e}")
            
            # Step 4: Create delivery channel
            print(f"   Setting up delivery channel...")
            
            try:
                self.config_client.put_delivery_channel(
                    DeliveryChannel={
                        'name': 'default',
                        's3BucketName': bucket_name,
                        's3KeyPrefix': 'AWSLogs'
                    }
                )
                print(f"   ✅ Created delivery channel")
            except ClientError as e:
                if 'MaxNumberOfDeliveryChannelsExceededException' in str(e):
                    print(f"   ✅ Delivery channel already exists")
                else:
                    print(f"   ⚠️ Delivery channel issue: {e}")
            
            # Step 5: Create configuration recorder
            print(f"   Setting up configuration recorder...")
            
            try:
                self.config_client.put_configuration_recorder(
                    ConfigurationRecorder={
                        'name': 'default',
                        'roleARN': role_arn,
                        'recordingGroup': {
                            'allSupported': True,
                            'includeGlobalResourceTypes': True,
                            'resourceTypes': []
                        }
                    }
                )
                print(f"   ✅ Created configuration recorder")
            except ClientError as e:
                if 'MaxNumberOfConfigurationRecordersExceededException' in str(e):
                    print(f"   ✅ Configuration recorder already exists")
                else:
                    print(f"   ⚠️ Configuration recorder issue: {e}")
            
            # Step 6: Start configuration recorder
            print(f"   Starting configuration recorder...")
            time.sleep(10)  # Allow IAM propagation
            
            try:
                self.config_client.start_configuration_recorder(
                    ConfigurationRecorderName='default'
                )
                print(f"   ✅ Started configuration recorder")
            except ClientError as e:
                if 'NoAvailableDeliveryChannelException' in str(e):
                    print(f"   ❌ Cannot start recorder: No delivery channel available")
                    return False
                elif 'InvalidRoleException' in str(e):
                    print(f"   ❌ Cannot start recorder: Invalid IAM role")
                    return False
                else:
                    print(f"   ⚠️ Recorder start issue: {e}")
            
            print(f"✅ AWS Config prerequisites setup complete!")
            return True
            
        except Exception as e:
            print(f"❌ Error setting up prerequisites: {e}")
            return False

    def get_all_aws_managed_rules(self):
        """Get comprehensive list of all AWS managed Config rules"""
        return [
            'ACCESS_KEYS_ROTATED', 'ACM_CERTIFICATE_EXPIRATION_CHECK', 'ALB_HTTP_DROP_INVALID_HEADER_ENABLED',
            'ALB_HTTP_TO_HTTPS_REDIRECTION_CHECK', 'ALB_WAF_ENABLED', 'API_GW_CACHE_ENABLED_AND_ENCRYPTED',
            'API_GW_EXECUTION_LOGGING_ENABLED', 'API_GW_SSL_ENABLED', 'API_GW_XRAY_ENABLED',
            'API_GWV2_ACCESS_LOGS_ENABLED', 'APPSYNC_LOGGING_ENABLED', 'APPROVED_AMIS_BY_ID',
            'APPROVED_AMIS_BY_TAG', 'AUTOSCALING_GROUP_ELB_HEALTHCHECK_REQUIRED', 'BACKUP_PLAN_MIN_FREQUENCY_AND_MIN_RETENTION_CHECK',
            'BACKUP_RECOVERY_POINT_ENCRYPTED', 'BACKUP_RECOVERY_POINT_MANUAL_DELETION_DISABLED', 'BACKUP_RECOVERY_POINT_MINIMUM_RETENTION_CHECK',
            'BEANSTALK_ENHANCED_HEALTH_REPORTING_ENABLED', 'CLOUD_TRAIL_CLOUD_WATCH_LOGS_ENABLED', 'CLOUD_TRAIL_ENABLED',
            'CLOUD_TRAIL_ENCRYPTION_ENABLED', 'CLOUD_TRAIL_LOG_FILE_VALIDATION_ENABLED', 'CLOUDFORMATION_STACK_DRIFT_DETECTION_CHECK',
            'CLOUDFORMATION_STACK_NOTIFICATION_CHECK', 'CLOUDFRONT_ACCESSLOGS_ENABLED', 'CLOUDFRONT_ASSOCIATED_WITH_WAF',
            'CLOUDFRONT_CUSTOM_SSL_CERTIFICATE', 'CLOUDFRONT_DEFAULT_ROOT_OBJECT_CONFIGURED', 'CLOUDFRONT_ORIGIN_ACCESS_IDENTITY_ENABLED',
            'CLOUDFRONT_ORIGIN_FAILOVER_ENABLED', 'CLOUDFRONT_S3_ORIGIN_NON_EXISTENT_BUCKET', 'CLOUDFRONT_S3_ORIGIN_ACCESS_CONTROL_ENABLED',
            'CLOUDFRONT_SECURITY_POLICY_CHECK', 'CLOUDFRONT_SNI_ENABLED', 'CLOUDFRONT_TRAFFIC_TO_ORIGIN_ENCRYPTED',
            'CLOUDFRONT_VIEWER_POLICY_HTTPS', 'CLOUDTRAIL_S3_DATAEVENTS_ENABLED', 'CLOUDTRAIL_SECURITY_TRAIL_ENABLED',
            'CLOUDWATCH_ALARM_ACTION_CHECK', 'CLOUDWATCH_ALARM_RESOURCE_CHECK', 'CLOUDWATCH_ALARM_SETTINGS_CHECK',
            'CLOUDWATCH_LOG_GROUP_ENCRYPTED', 'CMK_BACKING_KEY_ROTATION_ENABLED', 'CODEBUILD_PROJECT_ARTIFACT_ENCRYPTION',
            'CODEBUILD_PROJECT_ENVIRONMENT_PRIVILEGED_CHECK', 'CODEBUILD_PROJECT_LOGGING_ENABLED', 'CODEBUILD_PROJECT_S3_LOGS_ENCRYPTED',
            'CODEBUILD_PROJECT_SOURCE_REPO_URL_CHECK', 'CODEDEPLOY_AUTO_ROLLBACK_MONITOR_ENABLED', 'CODEDEPLOY_LAMBDA_ALLATONCE_TRAFFIC_SHIFT_DISABLED',
            'CODEPIPELINE_DEPLOYMENT_COUNT_CHECK', 'CODEPIPELINE_REGION_FANOUT_CHECK', 'CW_LOGGROUP_RETENTION_PERIOD_CHECK',
            'DAX_ENCRYPTION_ENABLED', 'DB_INSTANCE_BACKUP_ENABLED', 'DMS_REPLICATION_NOT_PUBLIC', 'DYNAMODB_AUTOSCALING_ENABLED',
            'DYNAMODB_IN_BACKUP_PLAN', 'DYNAMODB_PITR_ENABLED', 'DYNAMODB_TABLE_ENCRYPTED_KMS', 'DYNAMODB_TABLE_ENCRYPTION_ENABLED',
            'DYNAMODB_THROUGHPUT_LIMIT_CHECK', 'EBS_ENCRYPTED_VOLUMES', 'EBS_IN_BACKUP_PLAN', 'EBS_OPTIMIZED_INSTANCE',
            'EBS_SNAPSHOT_PUBLIC_READ_PROHIBITED', 'EBS_SNAPSHOT_PUBLIC_WRITE_PROHIBITED', 'EC2_EBS_ENCRYPTION_BY_DEFAULT',
            'EC2_IMDSV2_CHECK', 'EC2_INSTANCE_DETAILED_MONITORING_ENABLED', 'EC2_INSTANCE_MANAGED_BY_SSM', 'EC2_INSTANCE_MULTIPLE_ENI_CHECK',
            'EC2_INSTANCE_NO_PUBLIC_IP', 'EC2_INSTANCE_PROFILE_ATTACHED', 'EC2_MANAGEDINSTANCE_APPLICATIONS_BLACKLISTED',
            'EC2_MANAGEDINSTANCE_APPLICATIONS_REQUIRED', 'EC2_MANAGEDINSTANCE_ASSOCIATION_COMPLIANCE_STATUS_CHECK', 'EC2_MANAGEDINSTANCE_INVENTORY_BLACKLISTED',
            'EC2_MANAGEDINSTANCE_PATCH_COMPLIANCE_STATUS_CHECK', 'EC2_MANAGEDINSTANCE_PLATFORM_CHECK', 'EC2_SECURITY_GROUP_ATTACHED_TO_ENI',
            'EC2_STOPPED_INSTANCE', 'ECR_PRIVATE_IMAGE_SCANNING_ENABLED', 'ECR_PRIVATE_LIFECYCLE_POLICY_CONFIGURED', 'ECR_PRIVATE_TAG_IMMUTABILITY_ENABLED',
            'ECS_AWSVPC_NETWORKING_ENABLED', 'ECS_CONTAINERS_NONPRIVILEGED', 'ECS_CONTAINERS_READONLY_ACCESS', 'ECS_CONTAINER_INSIGHTS_ENABLED',
            'ECS_FARGATE_LATEST_PLATFORM_VERSION', 'ECS_NO_ENVIRONMENT_SECRETS', 'ECS_TASK_DEFINITION_LOG_CONFIGURATION', 'ECS_TASK_DEFINITION_MEMORY_HARD_LIMIT',
            'ECS_TASK_DEFINITION_NONROOT_USER', 'ECS_TASK_DEFINITION_PID_MODE_CHECK', 'ECS_TASK_DEFINITION_USER_FOR_HOST_MODE_CHECK', 'EFS_ENCRYPTED_CHECK',
            'EFS_IN_BACKUP_PLAN', 'EIP_ATTACHED', 'EKS_CLUSTER_LOGGING_ENABLED', 'EKS_CLUSTER_OLDEST_SUPPORTED_VERSION',
            'EKS_CLUSTER_SUPPORTED_VERSION', 'EKS_ENDPOINT_NO_PUBLIC_ACCESS', 'EKS_SECRETS_ENCRYPTED', 'ELASTIC_BEANSTALK_LOGS_TO_CLOUDWATCH',
            'ELASTIC_BEANSTALK_MANAGED_UPDATES_ENABLED', 'ELASTICSEARCH_ENCRYPTED_AT_REST', 'ELASTICSEARCH_IN_VPC_ONLY', 'ELASTICSEARCH_LOGS_TO_CLOUDWATCH',
            'ELASTICSEARCH_NODE_TO_NODE_ENCRYPTION_CHECK', 'ELB_ACM_CERTIFICATE_REQUIRED', 'ELB_CROSS_ZONE_LOAD_BALANCING_ENABLED', 'ELB_CUSTOM_SECURITY_POLICY_SSL_CHECK',
            'ELB_DELETION_PROTECTION_ENABLED', 'ELB_LOGGING_ENABLED', 'ELB_PREDEFINED_SECURITY_POLICY_SSL_CHECK', 'ELB_TLS_HTTPS_LISTENERS_ONLY',
            'ELASTICSEARCH_DOMAIN_ERROR_LOGGING_ENABLED', 'EMR_KERBEROS_ENABLED', 'EMR_MASTER_NO_PUBLIC_IP', 'ENCRYPTED_VOLUMES',
            'FSX_RESOURCES_PROTECTED_BY_BACKUP_PLAN', 'GUARDDUTY_ENABLED_CENTRALIZED', 'GUARDDUTY_NON_ARCHIVED_FINDINGS', 'IAM_CUSTOMER_POLICY_BLOCKED_KMS_ACTIONS',
            'IAM_GROUP_HAS_USERS_CHECK', 'IAM_NO_INLINE_POLICY_CHECK', 'IAM_PASSWORD_POLICY', 'IAM_POLICY_BLACKLISTED_CHECK',
            'IAM_POLICY_IN_USE', 'IAM_POLICY_NO_STATEMENTS_WITH_ADMIN_ACCESS', 'IAM_POLICY_NO_STATEMENTS_WITH_FULL_ACCESS', 'IAM_ROLE_MANAGED_POLICY_CHECK',
            'IAM_ROOT_ACCESS_KEY_CHECK', 'IAM_USER_GROUP_MEMBERSHIP_CHECK', 'IAM_USER_MFA_ENABLED', 'IAM_USER_NO_POLICIES_CHECK',
            'IAM_USER_UNUSED_CREDENTIALS_CHECK', 'INCOMING_SSH_DISABLED', 'INSTANCES_IN_VPC', 'INTERNET_GATEWAY_AUTHORIZED_VPC_ONLY',
            'KMS_CMK_NOT_SCHEDULED_FOR_DELETION', 'LAMBDA_CONCURRENCY_CHECK', 'LAMBDA_DLQ_CHECK', 'LAMBDA_FUNCTION_PUBLIC_READ_PROHIBITED',
            'LAMBDA_FUNCTION_PUBLIC_WRITE_PROHIBITED', 'LAMBDA_FUNCTION_SETTINGS_CHECK', 'LAMBDA_INSIDE_VPC', 'MFA_ENABLED_FOR_IAM_CONSOLE_ACCESS',
            'MQ_CLOUDWATCH_AUDIT_LOG_ENABLED', 'MQ_CLOUDWATCH_AUDIT_LOGGING_ENABLED', 'MULTI_REGION_CLOUD_TRAIL_ENABLED', 'NACL_NO_UNRESTRICTED_SSH_RDP',
            'NETFW_LOGGING_ENABLED', 'NETFW_MULTI_AZ_ENABLED', 'NETFW_POLICY_DEFAULT_ACTION_FRAGMENT_PACKETS', 'NETFW_POLICY_DEFAULT_ACTION_FULL_PACKETS',
            'NETFW_POLICY_RULE_GROUP_ASSOCIATED', 'NETFW_STATELESS_RULE_GROUP_NOT_EMPTY', 'NEPTUNE_CLUSTER_CLOUDWATCH_LOG_EXPORT_ENABLED', 'NEPTUNE_CLUSTER_COPY_TAGS_TO_SNAPSHOT_ENABLED',
            'NEPTUNE_CLUSTER_DELETION_PROTECTION_ENABLED', 'NEPTUNE_CLUSTER_ENCRYPTED', 'NEPTUNE_CLUSTER_IAM_DATABASE_AUTHENTICATION_ENABLED', 'NEPTUNE_CLUSTER_SNAPSHOT_ENCRYPTED',
            'NEPTUNE_CLUSTER_SNAPSHOT_PUBLIC_PROHIBITED', 'OPENSEARCH_ACCESS_CONTROL_ENABLED', 'OPENSEARCH_AUDIT_LOGGING_ENABLED', 'OPENSEARCH_DATA_NODE_FAULT_TOLERANCE',
            'OPENSEARCH_ENCRYPTED_AT_REST', 'OPENSEARCH_HTTPS_REQUIRED', 'OPENSEARCH_IN_VPC_ONLY', 'OPENSEARCH_LOGS_TO_CLOUDWATCH',
            'OPENSEARCH_NODE_TO_NODE_ENCRYPTION_CHECK', 'RDS_CLUSTER_COPY_TAGS_TO_SNAPSHOTS_ENABLED', 'RDS_CLUSTER_DEFAULT_PORT_CHECK', 'RDS_CLUSTER_DELETION_PROTECTION_ENABLED',
            'RDS_CLUSTER_IAM_AUTHENTICATION_ENABLED', 'RDS_CLUSTER_MULTI_AZ_ENABLED', 'RDS_DB_CLUSTER_SNAPSHOT_ENCRYPTED', 'RDS_DB_INSTANCE_BACKUP_ENABLED',
            'RDS_ENHANCED_MONITORING_ENABLED', 'RDS_INSTANCE_DEFAULT_PORT_CHECK', 'RDS_INSTANCE_DELETION_PROTECTION_ENABLED', 'RDS_INSTANCE_IAM_AUTHENTICATION_ENABLED',
            'RDS_INSTANCE_PUBLIC_READ_PROHIBITED', 'RDS_INSTANCE_PUBLIC_WRITE_PROHIBITED', 'RDS_LOGGING_ENABLED', 'RDS_MULTI_AZ_SUPPORT',
            'RDS_SNAPSHOT_ENCRYPTED', 'RDS_SNAPSHOTS_PUBLIC_PROHIBITED', 'RDS_STORAGE_ENCRYPTED', 'REDSHIFT_AUDIT_LOGGING_ENABLED',
            'REDSHIFT_BACKUP_ENABLED', 'REDSHIFT_CLUSTER_CONFIGURATION_CHECK', 'REDSHIFT_CLUSTER_KMS_ENABLED', 'REDSHIFT_CLUSTER_MAINTENANCESETTINGS_CHECK',
            'REDSHIFT_CLUSTER_PUBLIC_READ_WRITE_PROHIBITED', 'REDSHIFT_DEFAULT_ADMIN_CHECK', 'REDSHIFT_DEFAULT_DB_NAME_CHECK', 'REDSHIFT_ENHANCED_VPC_ROUTING_ENABLED',
            'REDSHIFT_REQUIRE_TLS_SSL', 'RESTRICTED_INCOMING_TRAFFIC', 'ROOT_HARDWARE_MFA_ENABLED', 'S3_ACCOUNT_LEVEL_PUBLIC_ACCESS_BLOCKS',
            'S3_ACCOUNT_LEVEL_PUBLIC_READ_PROHIBITED', 'S3_ACCOUNT_LEVEL_PUBLIC_WRITE_PROHIBITED', 'S3_BUCKET_BLACKLISTED_ACTIONS_PROHIBITED', 'S3_BUCKET_DEFAULT_LOCK_ENABLED',
            'S3_BUCKET_LEVEL_PUBLIC_ACCESS_PROHIBITED', 'S3_BUCKET_LEVEL_PUBLIC_READ_PROHIBITED', 'S3_BUCKET_LEVEL_PUBLIC_WRITE_PROHIBITED', 'S3_BUCKET_LOGGING_ENABLED',
            'S3_BUCKET_NOTIFICATION_ENABLED', 'S3_BUCKET_POLICY_GRANTEE_CHECK', 'S3_BUCKET_POLICY_NOT_MORE_PERMISSIVE', 'S3_BUCKET_PUBLIC_READ_PROHIBITED',
            'S3_BUCKET_PUBLIC_WRITE_PROHIBITED', 'S3_BUCKET_REPLICATION_ENABLED', 'S3_BUCKET_SERVER_SIDE_ENCRYPTION_ENABLED', 'S3_BUCKET_SSL_REQUESTS_ONLY',
            'S3_BUCKET_VERSIONING_ENABLED', 'S3_EVENT_NOTIFICATIONS_ENABLED', 'SAGEMAKER_ENDPOINT_CONFIGURATION_KMS_KEY_CONFIGURED', 'SAGEMAKER_NOTEBOOK_INSTANCE_KMS_KEY_CONFIGURED',
            'SAGEMAKER_NOTEBOOK_NO_DIRECT_INTERNET_ACCESS', 'SECRETSMANAGER_ROTATION_ENABLED_CHECK', 'SECRETSMANAGER_SCHEDULED_ROTATION_SUCCESS_CHECK', 'SECURITYHUB_ENABLED',
            'SERVICE_VPC_ENDPOINT_ENABLED', 'SHIELD_ADVANCED_ENABLED_AUTO_RENEW', 'SHIELD_DRT_ACCESS', 'SNS_ENCRYPTED_KMS',
            'SNS_TOPIC_MESSAGE_DELIVERY_NOTIFICATION_ENABLED', 'SQS_QUEUE_MESSAGE_DELIVERY_NOTIFICATION_ENABLED', 'SSM_DOCUMENT_NOT_PUBLIC', 'STEP_FUNCTIONS_STATE_MACHINE_LOGGING_ENABLED',
            'SUBNET_AUTO_ASSIGN_PUBLIC_IP_DISABLED', 'VPC_DEFAULT_SECURITY_GROUP_CLOSED', 'VPC_FLOW_LOGS_ENABLED', 'VPC_NETWORK_ACL_UNUSED_CHECK',
            'VPC_PEERING_DNS_RESOLUTION_CHECK', 'VPC_SG_OPEN_ONLY_TO_AUTHORIZED_PORTS', 'WAF_CLASSIC_LOGGING_ENABLED', 'WAF_GLOBAL_RULEGROUP_NOT_EMPTY',
            'WAF_GLOBAL_RULE_NOT_EMPTY', 'WAF_GLOBAL_WEBACL_NOT_EMPTY', 'WAF_REGIONAL_RULEGROUP_NOT_EMPTY', 'WAF_REGIONAL_RULE_NOT_EMPTY',
            'WAF_REGIONAL_WEBACL_NOT_EMPTY', 'WAFV2_LOGGING_ENABLED', 'WAFV2_RULEGROUP_NOT_EMPTY', 'WAFV2_WEBACL_NOT_EMPTY'
        ]

    def deploy_all_config_rules(self):
        """Deploy all AWS managed Config rules"""
        print(f"\n🚀 Deploying ALL AWS Config Rules...")
        print("=" * 60)
        
        all_rules = self.get_all_aws_managed_rules()
        
        print(f"📊 Total rules to deploy: {len(all_rules)}")
        print(f"⏱️ Estimated time: {len(all_rules) * 2 // 60} minutes")
        
        # Confirm before proceeding
        proceed = input(f"\nDeploy all {len(all_rules)} Config rules? (y/N): ").strip().lower()
        if proceed != 'y':
            print("❌ Deployment cancelled by user")
            return False
        
        deployed_count = 0
        failed_count = 0
        already_exists_count = 0
        deployment_results = {}
        
        print(f"\n🔄 Starting deployment...")
        
        for i, rule_identifier in enumerate(all_rules, 1):
            try:
                print(f"   {i:3d}/{len(all_rules)}: {rule_identifier:<50}", end="")
                
                # Create friendly rule name (lowercase with hyphens)
                rule_name = rule_identifier.lower().replace('_', '-')
                
                # Deploy the rule
                self.config_client.put_config_rule(
                    ConfigRule={
                        'ConfigRuleName': rule_name,
                        'Description': f'AWS managed rule: {rule_identifier}',
                        'Source': {
                            'Owner': 'AWS',
                            'SourceIdentifier': rule_identifier
                        },
                        'ConfigRuleState': 'ACTIVE'
                    }
                )
                
                deployed_count += 1
                deployment_results[rule_identifier] = {
                    'status': 'deployed',
                    'rule_name': rule_name
                }
                print(" ✅")
                
            except ClientError as e:
                error_code = e.response.get('Error', {}).get('Code', 'Unknown')
                
                if 'ResourceConflictException' in str(e) or 'ConflictException' in str(e):
                    already_exists_count += 1
                    deployment_results[rule_identifier] = {
                        'status': 'already_exists',
                        'rule_name': rule_name
                    }
                    print(" ✅ (exists)")
                elif 'InsufficientPermissionsException' in str(e):
                    failed_count += 1
                    deployment_results[rule_identifier] = {
                        'status': 'failed',
                        'error': 'Insufficient permissions'
                    }
                    print(" ❌ (perms)")
                elif 'NoAvailableConfigurationRecorderException' in str(e):
                    failed_count += 1
                    deployment_results[rule_identifier] = {
                        'status': 'failed',
                        'error': 'No Config recorder'
                    }
                    print(" ❌ (no recorder)")
                else:
                    failed_count += 1
                    deployment_results[rule_identifier] = {
                        'status': 'failed',
                        'error': str(e)[:50]
                    }
                    print(f" ❌ ({error_code})")
            
            except Exception as e:
                failed_count += 1
                deployment_results[rule_identifier] = {
                    'status': 'failed',
                    'error': str(e)[:50]
                }
                print(f" ❌ (error)")
            
            # Small delay to avoid rate limiting
            if i % 10 == 0:
                time.sleep(2)
            else:
                time.sleep(0.2)
        
        # Save deployment results
        os.makedirs("evidence", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_file = f"evidence/config_rules_deployment_{timestamp}.json"
        
        deployment_summary = {
            'deployment_metadata': {
                'timestamp': datetime.utcnow().isoformat() + 'Z',
                'account_id': self.account_id,
                'region': self.region,
                'total_rules': len(all_rules),
                'newly_deployed': deployed_count,
                'already_existed': already_exists_count,
                'failed': failed_count,
                'success_rate_percent': round(((deployed_count + already_exists_count) / len(all_rules)) * 100, 1)
            },
            'deployment_results': deployment_results
        }
        
        with open(results_file, 'w') as f:
            json.dump(deployment_summary, f, indent=2)
        
        # Print summary
        print(f"\n📊 Deployment Summary:")
        print(f"   ✅ Newly deployed: {deployed_count}")
        print(f"   ♻️ Already existed: {already_exists_count}")
        print(f"   ❌ Failed: {failed_count}")
        print(f"   📈 Success rate: {deployment_summary['deployment_metadata']['success_rate_percent']}%")
        print(f"   💾 Results saved to: {results_file}")
        
        return deployment_summary['deployment_metadata']['success_rate_percent'] > 80


def main():
    print("🚀 AWS Config Rules Mass Deployment Tool")
    print("=" * 60)
    
    print("Enter AWS credentials for target account:")
    access_key_id = input("AWS Access Key ID: ").strip()
    secret_access_key = input("AWS Secret Access Key: ").strip()
    session_token = input("AWS Session Token (optional, press Enter to skip): ").strip()
    if not session_token:
        session_token = None
    
    region = input("AWS Region (default: us-east-1): ").strip()
    if not region:
        region = 'us-east-1'
    
    try:
        # Initialize deployer
        deployer = AWSConfigRulesDeployer(
            access_key_id=access_key_id,
            secret_access_key=secret_access_key,
            session_token=session_token,
            region=region
        )
        
        print("\nChoose deployment option:")
        print("1. Setup prerequisites + Deploy all rules (recommended for new accounts)")
        print("2. Deploy all rules only (if Config is already setup)")
        print("3. Setup prerequisites only")
        
        choice = input("Enter choice (1-3): ").strip()
        
        if choice == "1":
            print(f"\n{'='*60}")
            print("FULL SETUP: PREREQUISITES + ALL RULES DEPLOYMENT")
            print(f"{'='*60}")
            
            # Setup prerequisites
            if deployer.setup_config_prerequisites():
                print("\n⏳ Waiting for Config to stabilize (60 seconds)...")
                time.sleep(60)
                
                # Deploy all rules
                success = deployer.deploy_all_config_rules()
                
                if success:
                    print(f"\n🎉 SUCCESS! All Config rules deployed!")
                    print(f"💡 You can now run evidence collection scripts")
                else:
                    print(f"\n⚠️ Deployment completed with some failures")
                    print(f"💡 Check the results file for details")
            else:
                print(f"\n❌ Prerequisites setup failed - cannot deploy rules")
                return 1
        
        elif choice == "2":
            print(f"\n{'='*60}")
            print("DEPLOYING ALL CONFIG RULES")
            print(f"{'='*60}")
            
            success = deployer.deploy_all_config_rules()
            
            if success:
                print(f"\n🎉 SUCCESS! All Config rules deployed!")
            else:
                print(f"\n⚠️ Deployment completed with some failures")
        
        elif choice == "3":
            print(f"\n{'='*60}")
            print("SETTING UP CONFIG PREREQUISITES ONLY")
            print(f"{'='*60}")
            
            if deployer.setup_config_prerequisites():
                print(f"\n🎉 SUCCESS! AWS Config prerequisites setup complete!")
                print(f"💡 You can now deploy rules using option 2")
            else:
                print(f"\n❌ Prerequisites setup failed")
                return 1
        
        else:
            print("❌ Invalid choice")
            return 1
    
    except KeyboardInterrupt:
        print(f"\n\n❌ Deployment interrupted by user")
        return 1
    
    except Exception as e:
        print(f"\n❌ Deployment failed: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit_code = main()
    exit(exit_code)