import json
import os

def extract_config_rules_direct():
    """Direct Python extraction without MCP agents - for testing data structure"""
    print("🔧 Direct Config Rules Extraction Test")
    print("=" * 50)
    
    requirement_dir = "requirement"
    evidence_dir = "evidence"
    
    # Create evidence directory
    os.makedirs(evidence_dir, exist_ok=True)
    
    if not os.path.exists(requirement_dir):
        print("❌ requirement/ directory not found")
        return False
    
    req_files = [f for f in os.listdir(requirement_dir) if f.endswith('.json')]
    print(f"📄 Found {len(req_files)} requirement files:")
    
    all_config_rules = []
    controls_found = {}
    
    for file in req_files:
        file_path = os.path.join(requirement_dir, file)
        print(f"\n📖 Reading {file}...")
        
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            print(f"   📋 File structure:")
            for key in data.keys():
                print(f"      - {key}: {type(data[key]).__name__}")
            
            # Extract control_id (might be in different fields)
            control_id = data.get('control_id') or data.get('id') or file.replace('.json', '').replace('_', '.')
            print(f"   🎯 Control ID: {control_id}")
            
            # Extract requirement text
            requirement = data.get('requirement', 'Not found')
            print(f"   📝 Requirement: {requirement[:100]}...")
            
            # Extract config rules - handle different structures
            config_rules = []
            if 'config_rules' in data:
                raw_rules = data['config_rules']
                print(f"   🔧 Config rules type: {type(raw_rules)}")
                print(f"   🔧 Config rules length: {len(raw_rules) if isinstance(raw_rules, list) else 'Not a list'}")
                
                if isinstance(raw_rules, list):
                    for i, rule in enumerate(raw_rules):
                        if isinstance(rule, dict):
                            # Rule is an object with rule_name and guidance
                            rule_name = rule.get('rule_name', f'unknown_rule_{i}')
                            config_rules.append(rule_name)
                            print(f"      - {rule_name}")
                        elif isinstance(rule, str):
                            # Rule is just a string
                            config_rules.append(rule)
                            print(f"      - {rule}")
                        else:
                            print(f"      - Unknown rule type: {type(rule)}")
                            
                print(f"   ✅ Extracted {len(config_rules)} rule names")
                all_config_rules.extend(config_rules)
                
                controls_found[control_id] = {
                    "file": file,
                    "requirement": requirement,
                    "config_rules": config_rules,
                    "config_rules_count": len(config_rules)
                }
            else:
                print("   ❌ No 'config_rules' field found")
                
        except Exception as e:
            print(f"   ❌ Error reading {file}: {e}")
    
    # Create unique list
    unique_rules = list(set(all_config_rules))
    unique_rules.sort()
    
    # Create summary
    summary = {
        "files_processed": req_files,
        "total_files": len(req_files),
        "controls_found": controls_found,
        "all_unique_rules": unique_rules,
        "total_unique_rules": len(unique_rules),
        "extraction_method": "direct_python"
    }
    
    # Save summary
    summary_file = os.path.join(evidence_dir, "config_rules_summary.json")
    with open(summary_file, 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"\n📊 SUMMARY:")
    print(f"   📄 Files processed: {len(req_files)}")
    print(f"   🎯 Controls found: {len(controls_found)}")
    print(f"   📋 Total config rules: {len(all_config_rules)}")
    print(f"   🔧 Unique config rules: {len(unique_rules)}")
    print(f"   💾 Summary saved to: {summary_file}")
    
    print(f"\n📝 First 10 unique config rules:")
    for i, rule in enumerate(unique_rules[:10]):
        print(f"   {i+1}. {rule}")
    if len(unique_rules) > 10:
        print(f"   ... and {len(unique_rules) - 10} more")
    
    return True

def test_mcp_agent_simulation():
    """Simulate what the MCP agent should do based on the extracted data"""
    print(f"\n🤖 MCP Agent Simulation")
    print("=" * 50)
    
    summary_file = "evidence/config_rules_summary.json"
    if not os.path.exists(summary_file):
        print("❌ No summary file found. Run direct extraction first.")
        return False
    
    with open(summary_file, 'r') as f:
        summary = json.load(f)
    
    print("🎯 This is what your MCP agent should collect for AWS Config:")
    print(f"   📋 Total unique config rules to query: {summary['total_unique_rules']}")
    
    # Simulate AWS Config boto3 calls structure
    print(f"\n🔧 Simulated AWS Config Evidence Structure:")
    simulated_evidence = {}
    
    for rule_name in summary['all_unique_rules'][:5]:  # Show first 5
        simulated_evidence[rule_name] = {
            "status": "SIMULATED - would call get_compliance_details_by_config_rule()",
            "would_execute": f"config.get_compliance_details_by_config_rule(ConfigRuleName='{rule_name}')"
        }
        print(f"   - {rule_name}: Ready for AWS Config query")
    
    if summary['total_unique_rules'] > 5:
        print(f"   ... and {summary['total_unique_rules'] - 5} more rules ready")
    
    # Save simulated evidence
    evidence_file = "evidence/simulated_evidence.json" 
    with open(evidence_file, 'w') as f:
        json.dump(simulated_evidence, f, indent=2)
    
    print(f"\n✅ Simulated evidence saved to: {evidence_file}")
    return True

def main():
    print("🚀 Simple Config Rules Extraction Test")
    print("This test uses direct Python instead of MCP agents")
    print("=" * 60)
    
    try:
        # Step 1: Direct extraction
        extraction_success = extract_config_rules_direct()
        
        if extraction_success:
            # Step 2: Simulate MCP agent behavior
            simulation_success = test_mcp_agent_simulation()
            
            if simulation_success:
                print(f"\n🎉 SUCCESS! Config rules extraction working correctly")
                print(f"\n🔮 Next steps:")
                print(f"   1. Start Docker daemon")
                print(f"   2. Your MCP agent should read these {json.load(open('evidence/config_rules_summary.json'))['total_unique_rules']} config rules")
                print(f"   3. Execute get_compliance_details_by_config_rule() for each rule")
                print(f"   4. Save results to evidence/all_evidence.json")
                return 0
            else:
                print(f"\n❌ Simulation failed")
                return 1
        else:
            print(f"\n❌ Extraction failed")
            return 1
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return 1

if __name__ == "__main__":
    exit_code = main()
    exit(exit_code)