#!/usr/bin/env python3
"""
Extract unique AWS Config rules and their guidance from aws_config_mappings.json
"""

from json import load, dump
from pathlib import Path
from collections import defaultdict
from datetime import datetime
import sys

def extract_unique_config_rules(input_file_path, output_file_path):
    """
    Extract unique AWS config rules with their guidance from the mappings file.
    
    Args:
        input_file_path: Path to the aws_config_mappings.json file
        output_file_path: Path where to save the unique config rules JSON
    """
    
    # Read the input file
    try:
        with open(input_file_path, 'r', encoding='utf-8') as f:
            data = load(f)
    except FileNotFoundError:
        print(f"Error: Input file '{input_file_path}' not found.")
        return False
    except Exception as e:
        print(f"Error: Invalid JSON in input file - {e}")
        return False
    
    # Extract unique config rules with their guidance
    unique_rules = {}
    rule_variations = defaultdict(set)  # To track if same rule has different guidance
    
    print(f"Processing {data['total_mappings']} mappings...")
    
    for mapping in data['mappings']:
        aws_config_rule = mapping['aws_config_rule']
        guidance = mapping['guidance']
        
        # Track variations in guidance for the same rule
        rule_variations[aws_config_rule].add(guidance)
        
        # Store the rule and guidance (first occurrence)
        if aws_config_rule not in unique_rules:
            unique_rules[aws_config_rule] = {
                'aws_config_rule': aws_config_rule,
                'guidance': guidance,
                'related_controls': [mapping['control_id']]
            }
        else:
            # Add control_id to related_controls if not already present
            if mapping['control_id'] not in unique_rules[aws_config_rule]['related_controls']:
                unique_rules[aws_config_rule]['related_controls'].append(mapping['control_id'])
    
    # Check for rules with multiple guidance variations
    rules_with_variations = {rule: guidances for rule, guidances in rule_variations.items() if len(guidances) > 1}
    
    if rules_with_variations:
        print(f"\nWarning: Found {len(rules_with_variations)} rules with multiple guidance variations:")
        for rule, guidances in rules_with_variations.items():
            print(f"  - {rule}: {len(guidances)} different guidance texts")
            # For rules with variations, we'll keep the first one but note this
            unique_rules[rule]['guidance_variations'] = len(guidances)
            unique_rules[rule]['has_multiple_guidance'] = True
    
    # Create output structure
    output_data = {
        'extraction_info': {
            'source_file': str(input_file_path),
            'extraction_date': datetime.now().isoformat(),
            'total_unique_rules': len(unique_rules),
            'rules_with_multiple_guidance': len(rules_with_variations),
            'source_mappings_count': data['total_mappings']
        },
        'unique_config_rules': list(unique_rules.values())
    }
    
    # Sort rules alphabetically for easier reading
    output_data['unique_config_rules'].sort(key=lambda x: x['aws_config_rule'])
    
    # Save to output file
    try:
        # Ensure output directory exists
        output_path = Path(output_file_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file_path, 'w', encoding='utf-8') as f:
            dump(output_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Successfully extracted {len(unique_rules)} unique AWS Config rules")
        print(f"📁 Saved to: {output_file_path}")
        
        if rules_with_variations:
            print(f"⚠️  Note: {len(rules_with_variations)} rules had multiple guidance variations (using first occurrence)")
        
        return True
        
    except Exception as e:
        print(f"Error: Failed to save output file - {e}")
        return False

def main():
    """Main execution function"""
    
    # File paths
    input_file = "shared_data/outputs/aws_config_guidance/aws_config_mappings.json"
    output_file = "shared_data/outputs/aws_config_guidance/unique_aws_config_rules.json"
    
    print("🔍 Extracting unique AWS Config rules and guidance...")
    print(f"📂 Input:  {input_file}")
    print(f"📂 Output: {output_file}")
    print("-" * 60)
    
    success = extract_unique_config_rules(input_file, output_file)
    
    if success:
        print("\n🎉 Extraction completed successfully!")
        print(f"You can now use the unique config rules file for Bedrock Knowledge Base chunking.")
    else:
        print("\n❌ Extraction failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()