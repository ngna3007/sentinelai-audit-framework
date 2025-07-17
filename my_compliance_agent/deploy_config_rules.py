import boto3
import json
import time
from botocore.exceptions import ClientError

def setup_aws_config():
    """Check and setup AWS Config prerequisites with better error handling"""
    print("🔧 Setting up AWS Config prerequisites...")
    
    config_client = boto3.client('config')
    sts = boto3.client('sts')
    account_id = sts.get_caller_identity()['Account']
    
    try:
        # Check if configuration recorder exists and is valid
        recorders = config_client.describe_configuration_recorders()
        recorder_exists = len(recorders['ConfigurationRecorders']) > 0
        
        if recorder_exists:
            recorder_name = recorders['ConfigurationRecorders'][0]['name']
            print(f"📋 Found existing recorder: {recorder_name}")
            
            # Check if recorder is actually working
            try:
                recorder_status = config_client.describe_configuration_recorder_status()
                is_recording = recorder_status['ConfigurationRecordersStatus'][0]['recording']
                print(f"📊 Recorder status: {'Recording' if is_recording else 'Stopped'}")
                
                if not is_recording:
                    print("🔄 Attempting to start existing recorder...")
                    try:
                        config_client.start_configuration_recorder(
                            ConfigurationRecorderName=recorder_name
                        )
                        print("✅ Started existing configuration recorder")
                        return True
                    except ClientError as start_error:
                        print(f"❌ Failed to start existing recorder: {start_error}")
                        print("🔧 Will recreate the recorder...")
                        # Delete broken recorder and recreate
                        try:
                            config_client.delete_configuration_recorder(
                                ConfigurationRecorderName=recorder_name
                            )
                            print("🗑️ Deleted broken recorder")
                            recorder_exists = False
                        except ClientError as delete_error:
                            print(f"❌ Failed to delete broken recorder: {delete_error}")
                            return False
                else:
                    print("✅ Configuration recorder is already running")
                    return True
                    
            except ClientError as status_error:
                print(f"❌ Error checking recorder status: {status_error}")
                print("🔧 Will recreate the recorder...")
                # Delete and recreate
                try:
                    config_client.delete_configuration_recorder(
                        ConfigurationRecorderName=recorder_name
                    )
                    print("🗑️ Deleted broken recorder")
                    recorder_exists = False
                except ClientError:
                    pass  # Continue with recreation
        
        if not recorder_exists:
            print("🔨 Creating new configuration recorder...")
            
            # Create or ensure IAM role exists
            iam = boto3.client('iam')
            role_name = 'aws-config-role'
            role_arn = f"arn:aws:iam::{account_id}:role/{role_name}"
            
            try:
                role_doc = {
                    "Version": "2012-10-17",
                    "Statement": [
                        {
                            "Effect": "Allow",
                            "Principal": {"Service": "config.amazonaws.com"},
                            "Action": "sts:AssumeRole"
                        }
                    ]
                }
                
                iam.create_role(
                    RoleName=role_name,
                    AssumeRolePolicyDocument=json.dumps(role_doc)
                )
                
                iam.attach_role_policy(
                    RoleName=role_name,
                    PolicyArn='arn:aws:iam::aws:policy/service-role/ConfigRole'
                )
                
                # Wait a bit for role to propagate
                time.sleep(10)
                print("✅ Created IAM role for Config")
                
            except ClientError as e:
                if 'EntityAlreadyExists' in str(e):
                    print("✅ IAM role already exists")
                else:
                    print(f"❌ Error creating IAM role: {e}")
                    return False
            
            # Create or ensure S3 bucket exists
            s3 = boto3.client('s3')
            bucket_name = f"aws-config-bucket-{account_id}"
            
            try:
                # Check if bucket exists first
                s3.head_bucket(Bucket=bucket_name)
                print(f"✅ S3 bucket already exists: {bucket_name}")
            except ClientError as e:
                if e.response['Error']['Code'] == '404':
                    # Bucket doesn't exist, create it
                    try:
                        region = boto3.Session().region_name
                        if region == 'us-east-1':
                            s3.create_bucket(Bucket=bucket_name)
                        else:
                            s3.create_bucket(
                                Bucket=bucket_name,
                                CreateBucketConfiguration={'LocationConstraint': region}
                            )
                        print(f"✅ Created S3 bucket: {bucket_name}")
                    except ClientError as create_error:
                        print(f"❌ Error creating S3 bucket: {create_error}")
                        return False
                else:
                    print(f"❌ Error checking S3 bucket: {e}")
                    return False
            
            # Create or ensure delivery channel exists
            try:
                channels = config_client.describe_delivery_channels()
                if not channels['DeliveryChannels']:
                    config_client.put_delivery_channel(
                        DeliveryChannel={
                            'name': 'default',
                            's3BucketName': bucket_name
                        }
                    )
                    print("✅ Created delivery channel")
                else:
                    print("✅ Delivery channel already exists")
            except ClientError as e:
                print(f"❌ Error with delivery channel: {e}")
                return False
            
            # Create configuration recorder
            try:
                config_client.put_configuration_recorder(
                    ConfigurationRecorder={
                        'name': 'default',
                        'roleARN': role_arn,
                        'recordingGroup': {
                            'allSupported': True,
                            'includeGlobalResourceTypes': True
                        }
                    }
                )
                print("✅ Created configuration recorder")
                
                # Start the recorder
                time.sleep(5)  # Brief wait before starting
                config_client.start_configuration_recorder(
                    ConfigurationRecorderName='default'
                )
                print("✅ Started configuration recorder")
                
            except ClientError as e:
                print(f"❌ Error creating/starting configuration recorder: {e}")
                return False
    
    except ClientError as e:
        print(f"❌ Error in Config setup: {e}")
        return False
    
    return True

def deploy_config_rules():
    """Deploy all required AWS Config rules"""
    
    # Mapping of your rule names to AWS managed rule identifiers
    rule_mappings = {
        'api-gw-xray-enabled': 'API_GW_XRAY_ENABLED',
        'api-gwv2-access-logs-enabled': 'API_GWV2_ACCESS_LOGS_ENABLED', 
        'appsync-logging-enabled': 'APPSYNC_LOGGING_ENABLED',
        'cloudfront-accesslogs-enabled': 'CLOUDFRONT_ACCESSLOGS_ENABLED',
        'cloudtrail-enabled': 'CLOUD_TRAIL_ENABLED',
        'ecs-task-definition-log-configuration': 'ECS_TASK_DEFINITION_LOG_CONFIGURATION',
        'eks-cluster-logging-enabled': 'EKS_CLUSTER_LOGGING_ENABLED',
        'elastic-beanstalk-logs-to-cloudwatch': 'ELASTIC_BEANSTALK_LOGS_TO_CLOUDWATCH',
        'mq-cloudwatch-audit-log-enabled': 'MQ_CLOUDWATCH_AUDIT_LOG_ENABLED',
        'mq-cloudwatch-audit-logging-enabled': 'MQ_CLOUDWATCH_AUDIT_LOGGING_ENABLED',
        'multi-region-cloudtrail-enabled': 'MULTI_REGION_CLOUD_TRAIL_ENABLED',
        'neptune-cluster-cloudwatch-log-export-enabled': 'NEPTUNE_CLUSTER_CLOUDWATCH_LOG_EXPORT_ENABLED',
        'netfw-logging-enabled': 'NETFW_LOGGING_ENABLED',
        'step-functions-state-machine-logging-enabled': 'STEP_FUNCTIONS_STATE_MACHINE_LOGGING_ENABLED',
        'waf-classic-logging-enabled': 'WAF_CLASSIC_LOGGING_ENABLED'
    }
    
    config_client = boto3.client('config')
    deployed_count = 0
    failed_count = 0
    
    print(f"🚀 Deploying {len(rule_mappings)} AWS Config rules...")
    
    for rule_name, source_identifier in rule_mappings.items():
        try:
            print(f"   Deploying {rule_name}...", end="")
            
            config_client.put_config_rule(
                ConfigRule={
                    'ConfigRuleName': rule_name,
                    'Description': f'Auto-deployed rule for PCI DSS compliance testing',
                    'Source': {
                        'Owner': 'AWS',
                        'SourceIdentifier': source_identifier
                    },
                    'ConfigRuleState': 'ACTIVE'
                }
            )
            
            deployed_count += 1
            print(" ✅")
            
        except ClientError as e:
            failed_count += 1
            if 'ResourceConflictException' in str(e):
                print(" ✅ (already exists)")
                deployed_count += 1
                failed_count -= 1
            else:
                print(f" ❌ ({str(e)[:50]})")
        
        # Small delay to avoid rate limiting
        time.sleep(0.5)
    
    print(f"\n📊 Deployment Summary:")
    print(f"   ✅ Successfully deployed: {deployed_count}")
    print(f"   ❌ Failed: {failed_count}")
    
    if deployed_count > 0:
        print(f"\n⏳ Waiting for rules to initialize (30 seconds)...")
        time.sleep(30)
        return True
    
    return False

def test_deployed_rules():
    """Test that the deployed rules can be queried"""
    print("🧪 Testing deployed rules...")
    
    # Use your existing config rules from the requirement file
    try:
        with open("requirement/10_2_1_2.json", 'r') as f:
            data = json.load(f)
        
        config_rules = data.get('config_rules', [])
        rule_names = [rule['rule_name'] for rule in config_rules if isinstance(rule, dict)]
        
    except Exception as e:
        print(f"❌ Error reading requirement file: {e}")
        return False
    
    config_client = boto3.client('config')
    success_count = 0
    
    for rule_name in rule_names:
        try:
            response = config_client.get_compliance_details_by_config_rule(
                ConfigRuleName=rule_name
            )
            success_count += 1
            print(f"   ✅ {rule_name}: Ready")
            
        except ClientError as e:
            if 'NoSuchConfigRuleException' in str(e):
                print(f"   ❌ {rule_name}: Still not found")
            else:
                print(f"   ⏳ {rule_name}: {str(e)[:50]}")
    
    print(f"\n📈 Test Results:")
    print(f"   ✅ Working rules: {success_count}/{len(rule_names)}")
    
    return success_count > 0

def cleanup_rules():
    """Optional: Clean up all deployed rules"""
    print("🧹 Cleaning up deployed Config rules...")
    
    try:
        with open("requirement/10_2_1_2.json", 'r') as f:
            data = json.load(f)
        
        config_rules = data.get('config_rules', [])
        rule_names = [rule['rule_name'] for rule in config_rules if isinstance(rule, dict)]
        
    except Exception as e:
        print(f"❌ Error reading requirement file: {e}")
        return False
    
    config_client = boto3.client('config')
    deleted_count = 0
    
    for rule_name in rule_names:
        try:
            config_client.delete_config_rule(ConfigRuleName=rule_name)
            deleted_count += 1
            print(f"   🗑️ Deleted {rule_name}")
        except ClientError as e:
            print(f"   ❌ Failed to delete {rule_name}: {e}")
    
    print(f"✅ Deleted {deleted_count} rules")
    return True

def main():
    print("🚀 AWS Config Rules Deployment for Testing")
    print("=" * 50)
    
    print("Choose an action:")
    print("1. Setup Config + Deploy all rules")
    print("2. Deploy rules only") 
    print("3. Test existing rules")
    print("4. Cleanup all rules")
    
    choice = input("Enter choice (1-4): ").strip()
    
    try:
        if choice == "1":
            print(f"\n{'='*50}")
            print("FULL SETUP: CONFIG + RULES")
            print(f"{'='*50}")
            
            if setup_aws_config():
                print("\n⏳ Waiting for Config to stabilize (60 seconds)...")
                time.sleep(60)
                
                if deploy_config_rules():
                    test_deployed_rules()
                    print(f"\n🎉 Setup complete! Your boto3 evidence collection should now work!")
                
        elif choice == "2":
            print(f"\n{'='*50}")
            print("DEPLOYING RULES ONLY")
            print(f"{'='*50}")
            
            if deploy_config_rules():
                test_deployed_rules()
                print(f"\n🎉 Rules deployed! Test your evidence collection now!")
                
        elif choice == "3":
            print(f"\n{'='*50}")
            print("TESTING EXISTING RULES")
            print(f"{'='*50}")
            
            test_deployed_rules()
            
        elif choice == "4":
            print(f"\n{'='*50}")
            print("CLEANING UP RULES")
            print(f"{'='*50}")
            
            confirm = input("Are you sure you want to delete all Config rules? (y/N): ")
            if confirm.lower() == 'y':
                cleanup_rules()
            else:
                print("Cleanup cancelled")
                
        else:
            print("Invalid choice")
            return 1
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    exit(exit_code)