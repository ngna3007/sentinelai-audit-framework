import json
import os
import boto3
from botocore.exceptions import ClientError

def fetch_evidence_data_direct(control_id):
    """Direct Python evidence collection - Fast and reliable"""
    print("🔧 Direct Evidence Collection (Fast & Reliable)")
    print("=" * 50)
    
    # Build requirement file path
    req_file_path = f"requirement/{control_id.replace('.', '_')}.json"
    
    # Read config rules from requirement file
    try:
        if not os.path.exists(req_file_path):
            print(f"❌ Requirement file not found: {req_file_path}")
            return False
            
        with open(req_file_path, 'r') as f:
            data = json.load(f)
        
        config_rules = data.get('config_rules', [])
        rule_names = []
        
        for rule in config_rules:
            if isinstance(rule, dict) and 'rule_name' in rule:
                rule_names.append(rule['rule_name'])
        
        print(f"📋 Found {len(rule_names)} config rules in {control_id}")
        
        if not rule_names:
            print(f"❌ No config rules found in {req_file_path}")
            return False
        
    except Exception as e:
        print(f"❌ Error reading requirement file: {e}")
        return False
    
    # Check AWS credentials
    try:
        session = boto3.Session()
        sts = session.client('sts')
        identity = sts.get_caller_identity()
        print(f"✅ AWS credentials valid - Account: {identity['Account']}")
    except Exception as e:
        print(f"❌ AWS credentials issue: {e}")
        return False
    
    # Connect to AWS Config
    try:
        config_client = session.client('config')
        print("✅ Connected to AWS Config")
        
    except Exception as e:
        print(f"❌ Failed to connect to AWS Config: {e}")
        return False
    
    # Collect evidence for each rule
    all_evidence = {}
    success_count = 0
    error_count = 0
    
    print(f"\n🔍 Querying {len(rule_names)} AWS Config rules...")
    
    for i, rule_name in enumerate(rule_names, 1):
        try:
            print(f"   {i}/{len(rule_names)}: {rule_name}...", end="")
            
            compliance_details = config_client.get_compliance_details_by_config_rule(
                ConfigRuleName=rule_name
            )
            
            all_evidence[rule_name] = compliance_details
            success_count += 1
            print(" ✅")
            
        except ClientError as e:
            all_evidence[rule_name] = {"error": str(e)}
            error_count += 1
            if 'NoSuchConfigRuleException' in str(e):
                print(" ❌ (rule not found)")
            else:
                print(f" ❌ ({str(e)[:50]}...)")
        except Exception as e:
            all_evidence[rule_name] = {"error": str(e)}
            error_count += 1
            print(f" ❌ ({str(e)[:50]}...)")
    
    # Save evidence
    os.makedirs("evidence", exist_ok=True)
    evidence_file = "evidence/all_evidence.json"
    
    try:
        with open(evidence_file, 'w') as f:
            json.dump(all_evidence, f, indent=2, default=str)
        
        print(f"\n📊 Evidence Collection Summary:")
        print(f"   ✅ Successful: {success_count}")
        print(f"   ❌ Failed: {error_count}")
        print(f"   📈 Success rate: {(success_count/(success_count+error_count))*100:.1f}%")
        print(f"   💾 Saved to: {evidence_file}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error saving evidence file: {e}")
        return False

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python evidence_only.py <control_id>")
        print("Example: python evidence_only.py 1.3.1")
        sys.exit(1)
    
    control_id = sys.argv[1]
    success = fetch_evidence_data_direct(control_id)
    
    if success:
        print("🎉 Evidence collection completed!")
    else:
        print("❌ Evidence collection failed!")