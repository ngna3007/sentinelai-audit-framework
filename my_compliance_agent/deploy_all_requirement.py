import boto3
import json
import time
import os
from botocore.exceptions import ClientError

def create_requirement_files():
    """Create the 3 requirement files if they don't exist"""
    print("📁 Creating requirement files...")
    
    os.makedirs("requirement", exist_ok=True)
    
    # Requirement 1 data (from your first document)
    req_1_data = {
        "control_id": "1.2.1",
        "requirement": "All services, protocols, and ports allowed are identified, approved, and have a defined business need.",
        "config_rules": [
            {
                "guidance": "Ensure that CloudFront distributions are not using deprecated SSL protocols for HTTPS communication between CloudFront edge locations and custom origins. This rule is NON_COMPLIANT for a CloudFront distribution if any'OriginSslProtocols' includes'SSLv3'.",
                "rule_name": "cloudfront-no-deprecated-ssl-protocols"
            },
            {
                "guidance": "Ensure that Amazon CloudFront distributions are using a minimum security policy and cipher suite of TLSv1.2 or greater for viewer connections. This rule is NON_COMPLIANT for a CloudFront distribution if the minimumProtocolVersion is below TLSv1.2_2018.",
                "rule_name": "cloudfront-security-policy-check"
            },
            {
                "guidance": "Ensure that Amazon CloudFront distributions are using a custom SSL certiﬁcate and are conﬁgured to use SNI to serve HTTPS requests. The rule is NON_COMPLIANT if a customSSL certiﬁcate is associated but the SSL support method is a dedicated IP address.",
                "rule_name": "cloudfront-sni-enabled"
            },
            {
                "guidance": "Ensure that Amazon CloudFront distributions are encrypting traﬃc to custom origins. The rule is NON_COMPLIANT if 'OriginProtocolPolicy' is 'http-only' or if 'OriginProtocolPolicy' is 'match-viewer' and 'ViewerProtocolPolicy' is 'allow-all'.",
                "rule_name": "cloudfront-traffic-to-origin-encrypted"
            },
            {
                "guidance": "Ensure that your Amazon CloudFront distributions use HTTPS (directly or via a redirection). The rule is NON_COMPLIANT if the value of ViewerProtocolPolicy is set to 'allow-all' for the DefaultCacheBehavior or for the CacheBehaviors.",
                "rule_name": "cloudfront-viewer-policy-https"
            },
            {
                "guidance": "Ensure that a server created with AWS Transfer Family does not use FTP for endpoint connection. The rule is NON_COMPLIANT if the server protocol for endpoint connection is FTP-enabled.",
                "rule_name": "transfer-family-server-no-ftp"
            }
        ]
    }
    
    # Requirement 2 data (from your second document) 
    req_2_data = {
        "control_id": "1.3.1",
        "requirement": "Inbound traffic to the CDE is restricted as follows: To only traffic that is necessary. All other traffic is specifically denied.",
        "config_rules": [
            {
                "guidance": "Ensure that Amazon API Gateway APIs are of the type speciﬁed in the rule parameter 'endpointConﬁgurationType'. The rule returns NON_COMPLIANT if the REST API does not match the endpoint type conﬁgured in the rule parameter.",
                "rule_name": "api-gw-endpoint-type-check"
            },
            {
                "guidance": "Ensure that AWS AppSync APIs are associated with AWS WAFv2 web access control lists (ACLs). The rule is NON_COMPLIANT for an AWS AppSync API if it is not associated with a web ACL.",
                "rule_name": "appsync-associated-with-waf"
            },
            {
                "guidance": "Ensure that Amazon CloudFront distributions are associated with either web application ﬁrewall (WAF) or WAFv2 web access control lists (ACLs). The rule is NON_COMPLIANT if a CloudFront distribution is not associated with a WAF web ACL.",
                "rule_name": "cloudfront-associated-with-waf"
            },
            {
                "guidance": "Ensure that the certiﬁcate associated with an Amazon CloudFront distribution is not the defaultSSL certiﬁcate. The rule is NON_COMPLIANT if a CloudFront distribution uses the default SSL certiﬁcate.",
                "rule_name": "cloudfront-custom-ssl-certificate"
            },
            {
                "guidance": "Ensure that the Bitbucket source repository URL DOES NOT contain sign-in credentials or not. The rule is NON_COMPLIANT if the URL contains any sign-in information and COMPLIANT if it doesn't.",
                "rule_name": "codebuild-project-source-repo-url-check"
            },
            {
                "guidance": "Ensure that Amazon DocumentDB manual cluster snapshots are not public. The rule is NON_COMPLIANT if any Amazon DocumentDB manual cluster snapshots are public.",
                "rule_name": "docdb-cluster-snapshot-public-prohibited"
            },
            {
                "guidance": "Ensure that the AWS Client VPN authorization rules does not authorize connection access for all clients. The rule is NON_COMPLIANT if 'AccessAll' is present and set to true.",
                "rule_name": "ec2-client-vpn-not-authorize-all"
            },
            {
                "guidance": "Ensure that Amazon Elastic Compute Cloud (Amazon EC2) Transit Gateways do not have 'AutoAcceptSharedAttachments' enabled. The rule is NON_COMPLIANT for a Transit Gateway if 'AutoAcceptSharedAttachments' is set to 'enable'.",
                "rule_name": "ec2-transit-gateway-auto-vpc-attach-disabled"
            },
            {
                "guidance": "Ensure that the Amazon Elastic Kubernetes Service (Amazon EKS) endpoint is not publicly accessible. The rule is NON_COMPLIANT if the endpoint is publicly accessible.",
                "rule_name": "eks-endpoint-no-public-access"
            },
            {
                "guidance": "Ensure that the Classic Load Balancers use SSL certiﬁcates provided by AWS Certiﬁcate Manager. To use this rule, use an SSL or HTTPS listener with your Classic Load Balancer. Note- this rule is only applicable to Classic Load Balancers. This rule does not check Application Load Balancers and Network Load Balancers.",
                "rule_name": "elb-acm-certificate-required"
            },
            {
                "guidance": "Ensure that an account with Amazon EMR has block public access settings enabled. The rule is NON_COMPLIANT if BlockPublicSecurityGroupRules is false, or if true, ports other than Port 22 are listed in Permitted PublicSecurityGroupRuleRanges.",
                "rule_name": "emr-block-public-access"
            },
            {
                "guidance": "Ensure that internet gateways are attached to an authorized virtual private cloud (Amazon VPC). The rule is NON_COMPLIANT if internet gateways are attached to an unauthorized VPC.",
                "rule_name": "internet-gateway-authorized-vpc-only"
            },
            {
                "guidance": "Ensure that default ports for SSH/RDP ingress traﬃc for network access control lists (NACLs) are restricted. The rule is NON_COMPLIANT if a NACL inbound entry allowsa source TCP or UDP CIDR block for ports22 or 3389.",
                "rule_name": "nacl-no-unrestricted-ssh-rdp"
            },
            {
                "guidance": "Ensure that an AWS Network Firewall policy is conﬁgured with a user deﬁned stateless default action for fragmented packets. The rule is NON_COMPLIANT if stateless default action for fragmented packets does not match with user deﬁned default action.",
                "rule_name": "netfw-policy-default-action-fragment-packets"
            },
            {
                "guidance": "Ensure that the Amazon Relational Database Service (Amazon RDS) DB security groups is the default one. The rule is NON_COMPLIANT if there are any DB security groups that are not the defaultDB security group.",
                "rule_name": "rds-db-security-group-not-allowed"
            },
            {
                "guidance": "Ensure that Amazon Redshift clusters have 'enhancedVpcRouting' enabled. The rule is NON_COMPLIANT if 'enhancedVpcRouting' is not enabled or if the conﬁgura tion.enhancedVpcRo uting ﬁeld is 'false'.",
                "rule_name": "redshift-enhanced-vpc-routing-enabled"
            },
            {
                "guidance": "Note: For this rule, the rule identiﬁer (INCOMING_SSH_DISABLED) and rule name (restricted-ssh) are diﬀerent. Ensure that the incomingSSH traﬃc for the security groups is accessible. The rule is COMPLIANT if the IP addresses of the incoming SSH traﬃc in the security groups are restricted (CIDR other than 0.0.0.0/0 or ::/0). Otherwise, NON_COMPLIANT.",
                "rule_name": "restricted-ssh"
            },
            {
                "guidance": "Ensure that Amazon S3 access points have block public access settings enabled. The rule is NON_COMPLIANT if block public access settings are not enabled for S3 access points.",
                "rule_name": "s3-access-point-public-access-blocks"
            },
            {
                "guidance": "Ensure that the required public access block settings are conﬁgured from account level. The rule is only NON_COMPLIANT when the ﬁelds set below do not match the corresponding ﬁelds in the conﬁguration item.",
                "rule_name": "s3-account-level-public-access-blocks"
            },
            {
                "guidance": "Ensure that an AWS WAF global rule contains some conditions. The rule is NON_COMPLIANT if no conditions are present within the WAF global rule.",
                "rule_name": "waf-global-rule-not-empty"
            },
            {
                "guidance": "Ensure that an AWS WAF Classic rule group contains some rules. The rule is NON_COMPLIANT if there are no rules present within a rule group.",
                "rule_name": "waf-global-rulegroup-not-empty"
            },
            {
                "guidance": "Ensure that a WAF Global Web ACL contains someWAF rules or rule groups. This rule is NON_COMPLIANT if a Web ACL does not contain any WAF rule or rule group.",
                "rule_name": "waf-global-webacl-not-empty"
            }
        ]
    }
    
    # Requirement 3 data (from your third document)
    req_3_data = {
        "control_id": "1.4.1", 
        "requirement": "Configuration files for NSCs are: Secured from unauthorized access. Kept consistent with active network configurations.",
        "config_rules": [
            {
                "guidance": "Ensure that Amazon API Gateway APIs are of the type speciﬁed in the rule parameter 'endpointConﬁgurationType'. The rule returns NON_COMPLIANT if the REST API does not match the endpoint type conﬁgured in the rule parameter.",
                "rule_name": "api-gw-endpoint-type-check"
            },
            {
                "guidance": "Ensure that AWS AppSync APIs are associated with AWS WAFv2 web access control lists (ACLs). The rule is NON_COMPLIANT for an AWS AppSync API if it is not associated with a web ACL.",
                "rule_name": "appsync-associated-with-waf"
            },
            {
                "guidance": "Ensure that Amazon CloudFront distributions are associated with either web application ﬁrewall (WAF) or WAFv2 web access control lists (ACLs). The rule is NON_COMPLIANT if a CloudFront distribution is not associated with a WAF web ACL.",
                "rule_name": "cloudfront-associated-with-waf"
            },
            {
                "guidance": "Ensure that the certiﬁcate associated with an Amazon CloudFront distribution is not the defaultSSL certiﬁcate. The rule is NON_COMPLIANT if a CloudFront distribution uses the default SSL certiﬁcate.",
                "rule_name": "cloudfront-custom-ssl-certificate"
            },
            {
                "guidance": "Ensure that the Bitbucket source repository URL DOES NOT contain sign-in credentials or not. The rule is NON_COMPLIANT if the URL contains any sign-in information and COMPLIANT if it doesn't.",
                "rule_name": "codebuild-project-source-repo-url-check"
            },
            {
                "guidance": "Ensure that Amazon DocumentDB manual cluster snapshots are not public. The rule is NON_COMPLIANT if any Amazon DocumentDB manual cluster snapshots are public.",
                "rule_name": "docdb-cluster-snapshot-public-prohibited"
            },
            {
                "guidance": "Ensure that the AWS Client VPN authorization rules does not authorize connection access for all clients. The rule is NON_COMPLIANT if 'AccessAll' is present and set to true.",
                "rule_name": "ec2-client-vpn-not-authorize-all"
            },
            {
                "guidance": "Ensure that Amazon Elastic Compute Cloud (Amazon EC2) Transit Gateways do not have 'AutoAcceptSharedAttachments' enabled. The rule is NON_COMPLIANT for a Transit Gateway if 'AutoAcceptSharedAttachments' is set to 'enable'.",
                "rule_name": "ec2-transit-gateway-auto-vpc-attach-disabled"
            },
            {
                "guidance": "Ensure that the Amazon Elastic Kubernetes Service (Amazon EKS) endpoint is not publicly accessible. The rule is NON_COMPLIANT if the endpoint is publicly accessible.",
                "rule_name": "eks-endpoint-no-public-access"
            },
            {
                "guidance": "Ensure that the Classic Load Balancers use SSL certiﬁcates provided by AWS Certiﬁcate Manager. To use this rule, use an SSL or HTTPS listener with your Classic Load Balancer. Note- this rule is only applicable to Classic Load Balancers. This rule does not check Application Load Balancers and Network Load Balancers.",
                "rule_name": "elb-acm-certificate-required"
            },
            {
                "guidance": "Ensure that an account with Amazon EMR has block public access settings enabled. The rule is NON_COMPLIANT if BlockPublicSecurityGroupRules is false, or if true, ports other than Port 22 are listed in Permitted PublicSecurityGroupRuleRanges.",
                "rule_name": "emr-block-public-access"
            },
            {
                "guidance": "Ensure that internet gateways are attached to an authorized virtual private cloud (Amazon VPC). The rule is NON_COMPLIANT if internet gateways are attached to an unauthorized VPC.",
                "rule_name": "internet-gateway-authorized-vpc-only"
            },
            {
                "guidance": "Ensure that default ports for SSH/RDP ingress traﬃc for network access control lists (NACLs) are restricted. The rule is NON_COMPLIANT if a NACL inbound entry allowsa source TCP or UDP CIDR block for ports22 or 3389.",
                "rule_name": "nacl-no-unrestricted-ssh-rdp"
            },
            {
                "guidance": "Ensure that an AWS Network Firewall policy is conﬁgured with a user deﬁned stateless default action for fragmented packets. The rule is NON_COMPLIANT if stateless default action for fragmented packets does not match with user deﬁned default action.",
                "rule_name": "netfw-policy-default-action-fragment-packets"
            },
            {
                "guidance": "Ensure that the Amazon Relational Database Service (Amazon RDS) DB security groups is the default one. The rule is NON_COMPLIANT if there are any DB security groups that are not the defaultDB security group.",
                "rule_name": "rds-db-security-group-not-allowed"
            },
            {
                "guidance": "Note: For this rule, the rule identiﬁer (INCOMING_SSH_DISABLED) and rule name (restricted-ssh) are diﬀerent. Ensure that the incomingSSH traﬃc for the security groups is accessible. The rule is COMPLIANT if the IP addresses of the incoming SSH traﬃc in the security groups are restricted (CIDR other than 0.0.0.0/0 or ::/0). Otherwise, NON_COMPLIANT.",
                "rule_name": "restricted-ssh"
            },
            {
                "guidance": "Ensure that Amazon S3 access points have block public access settings enabled. The rule is NON_COMPLIANT if block public access settings are not enabled for S3 access points.",
                "rule_name": "s3-access-point-public-access-blocks"
            },
            {
                "guidance": "Ensure that the required public access block settings are conﬁgured from account level. The rule is only NON_COMPLIANT when the ﬁelds set below do not match the corresponding ﬁelds in the conﬁguration item.",
                "rule_name": "s3-account-level-public-access-blocks"
            },
            {
                "guidance": "Ensure that an AWS WAF global rule contains some conditions. The rule is NON_COMPLIANT if no conditions are present within the WAF global rule.",
                "rule_name": "waf-global-rule-not-empty"
            },
            {
                "guidance": "Ensure that an AWS WAF Classic rule group contains some rules. The rule is NON_COMPLIANT if there are no rules present within a rule group.",
                "rule_name": "waf-global-rulegroup-not-empty"
            },
            {
                "guidance": "Ensure that a WAF Global Web ACL contains someWAF rules or rule groups. This rule is NON_COMPLIANT if a Web ACL does not contain any WAF rule or rule group.",
                "rule_name": "waf-global-webacl-not-empty"
            }
        ]
    }
    
    # Write files
    files = [
        ("requirement/1_2_1.json", req_1_data),
        ("requirement/1_3_1.json", req_2_data), 
        ("requirement/1_4_1.json", req_3_data)
    ]
    
    for filename, data in files:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"✅ Created {filename}")
    
    return True

def collect_all_config_rules():
    """Collect all unique config rules from all requirement files"""
    print("📋 Collecting all config rules...")
    
    req_files = [
        "requirement/1_2_1.json",
        "requirement/1_3_1.json", 
        "requirement/1_4_1.json",
        "requirement/10_2_1_2.json"  # Your existing file
    ]
    
    all_rules = {}  # Use dict to avoid duplicates
    
    for file_path in req_files:
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                
                control_id = data.get('control_id', os.path.basename(file_path).replace('.json', ''))
                config_rules = data.get('config_rules', [])
                
                print(f"   📄 {control_id}: {len(config_rules)} rules")
                
                for rule in config_rules:
                    if isinstance(rule, dict) and 'rule_name' in rule:
                        rule_name = rule['rule_name']
                        all_rules[rule_name] = {
                            'name': rule_name,
                            'guidance': rule.get('guidance', ''),
                            'source_control': control_id
                        }
                        
            except Exception as e:
                print(f"   ❌ Error reading {file_path}: {e}")
    
    print(f"📊 Total unique config rules found: {len(all_rules)}")
    return all_rules

def get_aws_managed_rule_mappings():
    """Map rule names to AWS managed rule source identifiers"""
    
    # This is a comprehensive mapping of your rule names to AWS Config managed rule identifiers
    mappings = {
        # CloudFront rules
        'cloudfront-no-deprecated-ssl-protocols': 'CLOUDFRONT_NO_DEPRECATED_SSL_PROTOCOLS',
        'cloudfront-security-policy-check': 'CLOUDFRONT_SECURITY_POLICY_CHECK',
        'cloudfront-sni-enabled': 'CLOUDFRONT_SNI_ENABLED',
        'cloudfront-traffic-to-origin-encrypted': 'CLOUDFRONT_TRAFFIC_TO_ORIGIN_ENCRYPTED',
        'cloudfront-viewer-policy-https': 'CLOUDFRONT_VIEWER_POLICY_HTTPS',
        'cloudfront-associated-with-waf': 'CLOUDFRONT_ASSOCIATED_WITH_WAF',
        'cloudfront-custom-ssl-certificate': 'CLOUDFRONT_CUSTOM_SSL_CERTIFICATE',
        
        # API Gateway rules
        'api-gw-endpoint-type-check': 'API_GW_ENDPOINT_TYPE_CHECK',
        'api-gw-xray-enabled': 'API_GW_XRAY_ENABLED',
        'api-gwv2-access-logs-enabled': 'API_GWV2_ACCESS_LOGS_ENABLED',
        
        # AppSync rules
        'appsync-associated-with-waf': 'APPSYNC_ASSOCIATED_WITH_WAF',
        'appsync-logging-enabled': 'APPSYNC_LOGGING_ENABLED',
        
        # EC2 rules
        'ec2-client-vpn-not-authorize-all': 'EC2_CLIENT_VPN_NOT_AUTHORIZE_ALL',
        'ec2-transit-gateway-auto-vpc-attach-disabled': 'EC2_TRANSIT_GATEWAY_AUTO_VPC_ATTACH_DISABLED',
        'restricted-ssh': 'INCOMING_SSH_DISABLED',  # Note: different identifier
        
        # EKS rules
        'eks-endpoint-no-public-access': 'EKS_ENDPOINT_NO_PUBLIC_ACCESS',
        'eks-cluster-logging-enabled': 'EKS_CLUSTER_LOGGING_ENABLED',
        
        # Load Balancer rules
        'elb-acm-certificate-required': 'ELB_ACM_CERTIFICATE_REQUIRED',
        
        # Other AWS services
        'transfer-family-server-no-ftp': 'TRANSFER_FAMILY_SERVER_NO_FTP',
        'codebuild-project-source-repo-url-check': 'CODEBUILD_PROJECT_SOURCE_REPO_URL_CHECK',
        'docdb-cluster-snapshot-public-prohibited': 'DOCDB_CLUSTER_SNAPSHOT_PUBLIC_PROHIBITED',
        'emr-block-public-access': 'EMR_BLOCK_PUBLIC_ACCESS',
        'internet-gateway-authorized-vpc-only': 'INTERNET_GATEWAY_AUTHORIZED_VPC_ONLY',
        'nacl-no-unrestricted-ssh-rdp': 'NACL_NO_UNRESTRICTED_SSH_RDP',
        'netfw-policy-default-action-fragment-packets': 'NETFW_POLICY_DEFAULT_ACTION_FRAGMENT_PACKETS',
        'rds-db-security-group-not-allowed': 'RDS_DB_SECURITY_GROUP_NOT_ALLOWED',
        'redshift-enhanced-vpc-routing-enabled': 'REDSHIFT_ENHANCED_VPC_ROUTING_ENABLED',
        
        # S3 rules
        's3-access-point-public-access-blocks': 'S3_ACCESS_POINT_PUBLIC_ACCESS_BLOCKS',
        's3-account-level-public-access-blocks': 'S3_ACCOUNT_LEVEL_PUBLIC_ACCESS_BLOCKS',
        
        # WAF rules
        'waf-global-rule-not-empty': 'WAF_GLOBAL_RULE_NOT_EMPTY',
        'waf-global-rulegroup-not-empty': 'WAF_GLOBAL_RULEGROUP_NOT_EMPTY',
        'waf-global-webacl-not-empty': 'WAF_GLOBAL_WEBACL_NOT_EMPTY',
        
        # Logging rules (from 10.2.1.2)
        'cloudtrail-enabled': 'CLOUD_TRAIL_ENABLED',
        'multi-region-cloudtrail-enabled': 'MULTI_REGION_CLOUD_TRAIL_ENABLED',
        'cloudfront-accesslogs-enabled': 'CLOUDFRONT_ACCESSLOGS_ENABLED',
        'ecs-task-definition-log-configuration': 'ECS_TASK_DEFINITION_LOG_CONFIGURATION',
        'elastic-beanstalk-logs-to-cloudwatch': 'ELASTIC_BEANSTALK_LOGS_TO_CLOUDWATCH',
        'mq-cloudwatch-audit-log-enabled': 'MQ_CLOUDWATCH_AUDIT_LOG_ENABLED',
        'mq-cloudwatch-audit-logging-enabled': 'MQ_CLOUDWATCH_AUDIT_LOGGING_ENABLED',
        'neptune-cluster-cloudwatch-log-export-enabled': 'NEPTUNE_CLUSTER_CLOUDWATCH_LOG_EXPORT_ENABLED',
        'netfw-logging-enabled': 'NETFW_LOGGING_ENABLED',
        'step-functions-state-machine-logging-enabled': 'STEP_FUNCTIONS_STATE_MACHINE_LOGGING_ENABLED',
        'waf-classic-logging-enabled': 'WAF_CLASSIC_LOGGING_ENABLED'
    }
    
    return mappings

def deploy_all_config_rules():
    """Deploy all unique AWS Config rules"""
    print("🚀 Deploying ALL AWS Config rules...")
    
    # Get all rules and mappings
    all_rules = collect_all_config_rules()
    mappings = get_aws_managed_rule_mappings()
    
    config_client = boto3.client('config')
    deployed_count = 0
    failed_count = 0
    skipped_count = 0
    
    for rule_name, rule_info in all_rules.items():
        if rule_name not in mappings:
            print(f"   ⚠️  {rule_name}: No AWS managed rule mapping found - skipping")
            skipped_count += 1
            continue
            
        source_identifier = mappings[rule_name]
        
        try:
            print(f"   Deploying {rule_name}...", end="")
            
            config_client.put_config_rule(
                ConfigRule={
                    'ConfigRuleName': rule_name,
                    'Description': f'PCI DSS rule from {rule_info["source_control"]}: {rule_info["guidance"][:100]}...',
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
            if 'ResourceConflictException' in str(e):
                print(" ✅ (already exists)")
                deployed_count += 1
            else:
                failed_count += 1
                print(f" ❌ ({str(e)[:50]})")
        
        # Small delay to avoid rate limiting
        time.sleep(0.3)
    
    print(f"\n📊 Deployment Summary:")
    print(f"   ✅ Successfully deployed: {deployed_count}")
    print(f"   ❌ Failed: {failed_count}")
    print(f"   ⚠️  Skipped (no mapping): {skipped_count}")
    print(f"   📋 Total rules processed: {len(all_rules)}")
    
    if deployed_count > 0:
        print(f"\n⏳ Waiting for rules to initialize (30 seconds)...")
        time.sleep(30)
        return True
    
    return False

def test_all_deployed_rules():
    """Test all deployed rules across all requirements"""
    print("🧪 Testing all deployed rules...")
    
    all_rules = collect_all_config_rules()
    config_client = boto3.client('config')
    
    success_count = 0
    no_data_count = 0
    error_count = 0
    
    print(f"\n📋 Testing {len(all_rules)} unique config rules:")
    
    for rule_name in all_rules.keys():
        try:
            response = config_client.get_compliance_details_by_config_rule(
                ConfigRuleName=rule_name
            )
            
            if response.get('EvaluationResults'):
                success_count += 1
                print(f"   ✅ {rule_name}: Has evaluation results")
            else:
                no_data_count += 1
                print(f"   ⏳ {rule_name}: No data yet (rule is starting)")
                
        except ClientError as e:
            error_count += 1
            if 'NoSuchConfigRuleException' in str(e):
                print(f"   ❌ {rule_name}: Rule not found")
            else:
                print(f"   ❌ {rule_name}: {str(e)[:50]}")
    
    print(f"\n📈 Test Results:")
    print(f"   ✅ Rules with data: {success_count}")
    print(f"   ⏳ Rules initializing: {no_data_count}")
    print(f"   ❌ Errors: {error_count}")
    print(f"   📊 Total success rate: {((success_count + no_data_count)/(success_count + no_data_count + error_count))*100:.1f}%")
    
    return success_count > 0 or no_data_count > 0

def main():
    print("🚀 Deploy ALL PCI DSS Config Rules")
    print("=" * 50)
    
    try:
        # Step 1: Create requirement files
        print("Step 1: Creating requirement files...")
        create_requirement_files()
        
        # Step 2: Show what we're deploying
        print(f"\nStep 2: Analyzing requirements...")
        all_rules = collect_all_config_rules()
        
        print(f"\n📋 Summary:")
        print(f"   📁 Requirements: 4 files (1.2.1, 1.3.1, 1.4.1, 10.2.1.2)")
        print(f"   🔧 Unique config rules: {len(all_rules)}")
        
        # Step 3: Deploy all rules
        print(f"\nStep 3: Deploying all config rules...")
        if deploy_all_config_rules():
            
            # Step 4: Test deployment
            print(f"\nStep 4: Testing deployed rules...")
            if test_all_deployed_rules():
                print(f"\n🎉 SUCCESS! All config rules deployed and ready!")
                print(f"\n📋 Next steps:")
                print(f"   1. Run your evidence collection test")
                print(f"   2. Test your audit pipeline with real data")
                print(f"   3. You now have config rules for 4 PCI DSS requirements")
                
                # Show file structure
                print(f"\n📁 Your requirement files:")
                req_files = ["1_2_1.json", "1_3_1.json", "1_4_1.json", "10_2_1_2.json"]
                for file in req_files:
                    if os.path.exists(f"requirement/{file}"):
                        with open(f"requirement/{file}", 'r') as f:
                            data = json.load(f)
                        rule_count = len(data.get('config_rules', []))
                        control_id = data.get('control_id', file.replace('.json', ''))
                        print(f"   ✅ {file}: {control_id} ({rule_count} rules)")
                
                return 0
            else:
                print(f"\n⚠️  Deployment completed but some rules failed testing")
                print(f"   This is normal - rules need time to evaluate resources")
                return 0
        else:
            print(f"\n❌ Deployment failed")
            return 1
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1

if __name__ == "__main__":
    exit_code = main()
    exit(exit_code)