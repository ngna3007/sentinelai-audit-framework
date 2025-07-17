#!/usr/bin/env python3
"""
Replace aws_config_rule and guidance in aws_config_mappings.json with canonical values from temp.json
"""
from json import load, dump
from pathlib import Path
from datetime import datetime

# File paths
MAPPINGS_PATH = "shared_data/outputs/aws_config_guidance/aws_config_mappings.json"
CANONICAL_PATH = "shared_data/outputs/aws_config_guidance/temp.json"

def main():
    print("🔄 Canonicalizing aws_config_mappings.json with temp.json...")
    print(f"📂 Source mappings: {MAPPINGS_PATH}")
    print(f"📂 Canonical rules: {CANONICAL_PATH}")
    print("=" * 60)
    
    # Load canonical rules from temp.json
    with open(CANONICAL_PATH, 'r', encoding='utf-8') as f:
        canonical_data = load(f)
    
    # Create mapping from rule name to canonical guidance
    canonical_map = {}
    for rule in canonical_data['unique_config_rules']:
        canonical_map[rule['aws_config_rule']] = rule['guidance']
    
    print(f"📋 Loaded {len(canonical_map)} canonical rules")
    
    # Load the mappings file
    with open(MAPPINGS_PATH, 'r', encoding='utf-8') as f:
        mappings_data = load(f)
    
    print(f"📋 Processing {mappings_data['total_mappings']} mappings...")
    
    # Track replacements
    replaced = 0
    not_found = set()
    rule_changes = {}  # Track rule name changes
    guidance_changes = {}  # Track guidance changes
    
    # Process each mapping
    for mapping in mappings_data['mappings']:
        original_rule = mapping['aws_config_rule']
        original_guidance = mapping['guidance']
        
        # Find canonical version (try exact match first, then fuzzy)
        canonical_rule = None
        canonical_guidance = None
        
        if original_rule in canonical_map:
            canonical_rule = original_rule
            canonical_guidance = canonical_map[original_rule]
        else:
            # Try fuzzy matching (case-insensitive, ignoring dashes/underscores)
            normalized_original = original_rule.lower().replace('-', '').replace('_', '')
            for rule_name in canonical_map.keys():
                normalized_canonical = rule_name.lower().replace('-', '').replace('_', '')
                if normalized_original == normalized_canonical:
                    canonical_rule = rule_name
                    canonical_guidance = canonical_map[rule_name]
                    break
        
        if canonical_rule and canonical_guidance:
            # Track changes
            if original_rule != canonical_rule:
                if original_rule not in rule_changes:
                    rule_changes[original_rule] = canonical_rule
            
            if original_guidance != canonical_guidance:
                if original_rule not in guidance_changes:
                    guidance_changes[original_rule] = {
                        'old': original_guidance[:80] + "..." if len(original_guidance) > 80 else original_guidance,
                        'new': canonical_guidance[:80] + "..." if len(canonical_guidance) > 80 else canonical_guidance
                    }
            
            # Apply canonical values
            mapping['aws_config_rule'] = canonical_rule
            mapping['guidance'] = canonical_guidance
            replaced += 1
        else:
            not_found.add(original_rule)
    
    # Update metadata
    mappings_data['canonicalization_info'] = {
        'canonicalized_date': datetime.now().isoformat(),
        'canonical_source': str(CANONICAL_PATH),
        'total_replacements': replaced,
        'rules_not_found': len(not_found),
        'rule_name_changes': len(rule_changes),
        'guidance_changes': len(guidance_changes)
    }
    
    # Save updated mappings
    with open(MAPPINGS_PATH, 'w', encoding='utf-8') as f:
        dump(mappings_data, f, indent=2, ensure_ascii=False)
    
    # Report results
    print(f"\n✅ Canonicalization completed!")
    print(f"📊 Results:")
    print(f"   - Total mappings processed: {mappings_data['total_mappings']}")
    print(f"   - Successfully replaced: {replaced}")
    print(f"   - Rules not found: {len(not_found)}")
    print(f"   - Rule name changes: {len(rule_changes)}")
    print(f"   - Guidance changes: {len(guidance_changes)}")
    
    if rule_changes:
        print(f"\n🔄 Rule name changes:")
        for original, canonical in sorted(rule_changes.items()):
            print(f"   - '{original}' → '{canonical}'")
    
    if not_found:
        print(f"\n⚠️  Rules not found in canonical list:")
        for rule in sorted(not_found):
            print(f"   - {rule}")
    
    if guidance_changes:
        print(f"\n📝 Guidance changes (first few):")
        for i, (rule, change) in enumerate(sorted(guidance_changes.items())):
            if i >= 5:  # Show only first 5
                print(f"   ... and {len(guidance_changes) - 5} more")
                break
            print(f"   - {rule}:")
            print(f"     Old: {change['old']}")
            print(f"     New: {change['new']}")
    
    print(f"\n📁 Updated file: {MAPPINGS_PATH}")
    print(f"📁 Backup available: {MAPPINGS_PATH.replace('.json', '_backup.json')}")

if __name__ == "__main__":
    main()