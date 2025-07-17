import json
import os
import boto3
from botocore.exceptions import ClientError

def fetch_all_config_rules_evidence():
    """Fetch evidence for ALL AWS Config rules using get_compliance_details_by_config_rule"""
    print("🔧 Complete Evidence Collection for ALL AWS Config Rules")
    print("=" * 60)
    
    # Explicit credentials (same as in your test file)
    access_key_id = "AKIARZJA6UM26HPX4INA"
    secret_access_key = "TAy1Q93hLOh8EKOmtHVxbkaJdO1S7FU/xWMbE9Ai"
    session_token = None
    region = 'ap-southeast-2'
    
    # This is the comprehensive list of ALL AWS managed Config rules
    all_aws_managed_rules = [
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
    
    print(f"📊 Total AWS managed Config rules to query: {len(all_aws_managed_rules)}")
    
    # Create session with explicit credentials (ignores environment)
    try:
        session = boto3.Session(
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key,
            aws_session_token=session_token,
            region_name=region
        )
        
        # Verify credentials
        sts = session.client('sts')
        identity = sts.get_caller_identity()
        print(f"✅ Connected to Account: {identity['Account']}")
        print(f"📍 Region: {region}")
        
    except Exception as e:
        print(f"❌ AWS credentials issue: {e}")
        return False
    
    # Connect to AWS Config and get deployed rules first
    try:
        config_client = session.client('config')
        print("✅ Connected to AWS Config")
        
        # Get deployed rules in account first (like your smart version)
        deployed_rules = []
        next_token = None
        
        try:
            while True:
                params = {}
                if next_token:
                    params['NextToken'] = next_token
                
                response = config_client.describe_config_rules(**params)
                rules = response.get('ConfigRules', [])
                deployed_rules.extend(rules)
                
                next_token = response.get('NextToken')
                if not next_token:
                    break
            
            print(f"📊 Found {len(deployed_rules)} deployed rules in account")
        except ClientError as e:
            print(f"⚠️ Could not get deployed rules: {e}")
            deployed_rules = []
        
    except Exception as e:
        print(f"❌ Failed to connect to AWS Config: {e}")
        return False
    
    # Only query DEPLOYED rules with get_compliance_details_by_config_rule
    all_evidence = {}
    success_count = 0
    error_count = 0
    
    print(f"\n🔍 Querying {len(deployed_rules)} DEPLOYED AWS Config rules with get_compliance_details_by_config_rule...")
    
    for i, rule in enumerate(deployed_rules, 1):
        rule_name = rule['ConfigRuleName']
        rule_source = rule.get('Source', {}).get('SourceIdentifier', 'UNKNOWN')
        
        try:
            print(f"   {i}/{len(deployed_rules)}: {rule_name}...", end="")
            
            # THIS IS THE KEY PART - Call get_compliance_details_by_config_rule for DEPLOYED rules only
            compliance_details = config_client.get_compliance_details_by_config_rule(
                ConfigRuleName=rule_name
            )
            
            all_evidence[rule_name] = {
                'compliance_details': compliance_details,
                'rule_source': rule_source,
                'rule_type': rule.get('Source', {}).get('Owner', 'UNKNOWN')
            }
            success_count += 1
            print(" ✅")
            
        except ClientError as e:
            all_evidence[rule_name] = {
                "error": str(e),
                'rule_source': rule_source,
                'rule_type': rule.get('Source', {}).get('Owner', 'UNKNOWN')
            }
            error_count += 1
            print(f" ❌ ({str(e)[:50]}...)")
        except Exception as e:
            all_evidence[rule_name] = {
                "error": str(e),
                'rule_source': rule_source,
                'rule_type': rule.get('Source', {}).get('Owner', 'UNKNOWN')
            }
            error_count += 1
            print(f" ❌ ({str(e)[:50]}...)")
    
    # Save evidence
    os.makedirs("evidence", exist_ok=True)
    evidence_file = "evidence/deployed_config_rules_evidence.json"
    
    try:
        with open(evidence_file, 'w') as f:
            json.dump(all_evidence, f, indent=2, default=str)
        
        print(f"\n📊 Smart Evidence Collection Summary:")
        print(f"   🔧 Total deployed rules queried: {len(deployed_rules)}")
        print(f"   ✅ Rules with compliance data: {success_count}")
        print(f"   ❌ Rules failed: {error_count}")
        print(f"   📈 Success rate: {(success_count/(success_count+error_count))*100:.1f}%")
        print(f"   💾 Saved to: {evidence_file}")
        
        # Show breakdown by rule type
        aws_managed = len([r for r in deployed_rules if r.get('Source', {}).get('Owner') == 'AWS'])
        custom_rules = len([r for r in deployed_rules if r.get('Source', {}).get('Owner') != 'AWS'])
        
        print(f"\n📋 Rule Type Breakdown:")
        print(f"   🏢 AWS Managed rules: {aws_managed}")
        print(f"   🔧 Custom/SecurityHub rules: {custom_rules}")
        
        # Show sample of actual compliance data found
        print(f"\n🔍 Sample of Rules with Compliance Data:")
        shown_count = 0
        for rule_name, evidence in all_evidence.items():
            if isinstance(evidence, dict) and 'compliance_details' in evidence and shown_count < 10:
                compliance_details = evidence['compliance_details']
                if 'EvaluationResults' in compliance_details:
                    eval_results = compliance_details['EvaluationResults']
                    if eval_results:
                        compliance_types = [result.get('ComplianceType', 'UNKNOWN') for result in eval_results]
                        unique_types = set(compliance_types)
                        rule_type = evidence.get('rule_type', 'UNKNOWN')
                        print(f"   ✅ {rule_name} ({rule_type}): {len(eval_results)} evaluations - {unique_types}")
                        shown_count += 1
                    else:
                        print(f"   ⏳ {rule_name}: Rule deployed but no evaluation results yet")
                        shown_count += 1
        
        if shown_count == 0:
            print("   ⚠️  No rules returned actual compliance evaluation data")
        
        print(f"\n💡 This is SMART evidence collection - only queries DEPLOYED rules!")
        print(f"   (Like your original file that shows YES/NO deployment status)")
        
        return True
        
    except Exception as e:
        print(f"❌ Error saving evidence file: {e}")
        return False

def main():
    print("🚀 Smart AWS Config Rules Evidence Collection")
    print("Fetches compliance details for DEPLOYED Config rules only (like your smart version)")
    print("=" * 80)
    
    try:
        print("=" * 50)
        print("FETCHING: DEPLOYED CONFIG RULES EVIDENCE")
        print("=" * 50)
        
        # Run smart evidence collection for DEPLOYED rules only
        evidence_result = fetch_all_config_rules_evidence()
        
        if evidence_result:
            print(f"\n🎉 SUCCESS! Smart evidence collection completed")
            print(f"📁 Check evidence/deployed_config_rules_evidence.json for detailed results")
            print(f"\n💡 This file contains get_compliance_details_by_config_rule results for")
            print(f"   ALL DEPLOYED Config rules in your account (like your smart checker)")
        else:
            print(f"\n❌ Evidence collection failed")
            return 1
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    exit(exit_code)