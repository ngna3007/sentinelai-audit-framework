import boto3
import json

def collect_aws_config_evidence(config_rules):
    config = boto3.client('config')
    all_evidence = {}
    
    for rule in config_rules:
        rule_name = rule['rule_name']
        try:
            compliance_details = config.get_compliance_details_by_config_rule(
                ConfigRuleName=rule_name
            )
            all_evidence[rule_name] = compliance_details
        except Exception as e:
            all_evidence[rule_name] = {"error": str(e)}
    
    return all_evidence

def main():
    # Read the JSON file with config rules
    with open('requirement/1_3_1.json', 'r') as f:
        data = json.load(f)
    
    config_rules = data['config_rules']
    
    # Collect evidence
    result = collect_aws_config_evidence(config_rules)
    
    # Ensure evidence directory exists
    import os
    os.makedirs('evidence', exist_ok=True)
    
    # Save to evidence file
    with open('evidence/all_evidence.json', 'w') as f:
        json.dump(result, f, indent=2)
    
    print("Evidence collection completed successfully!")

if __name__ == "__main__":
    main()