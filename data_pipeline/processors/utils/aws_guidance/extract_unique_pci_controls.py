#!/usr/bin/env python3
"""
Extract unique PCI controls with their associated AWS Config rules from aws_config_mappings.json
"""

from json import load, dump
from pathlib import Path
from collections import defaultdict
from datetime import datetime
import sys

def extract_unique_pci_controls(input_file_path, output_file_path):
    """
    Extract unique PCI controls with all their associated AWS config rules and guidance.
    
    Args:
        input_file_path: Path to the aws_config_mappings.json file
        output_file_path: Path where to save the unique PCI controls JSON
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
    
    # Extract unique PCI controls with their AWS config rules
    unique_controls = {}
    
    print(f"Processing {data['total_mappings']} mappings...")
    
    for mapping in data['mappings']:
        control_id = mapping['control_id']
        control_description = mapping['control_description']
        aws_config_rule = mapping['aws_config_rule']
        guidance = mapping['guidance']
        
        # Initialize control if not seen before
        if control_id not in unique_controls:
            unique_controls[control_id] = {
                'control_id': control_id,
                'control_description': control_description,
                'aws_config_rules': []
            }
        
        # Add the AWS config rule and guidance to this control
        config_rule_entry = {
            'aws_config_rule': aws_config_rule,
            'guidance': guidance
        }
        
        # Check if this exact rule+guidance combination already exists for this control
        # (to avoid duplicates)
        if config_rule_entry not in unique_controls[control_id]['aws_config_rules']:
            unique_controls[control_id]['aws_config_rules'].append(config_rule_entry)
    
    # Convert to list and sort by control_id
    controls_list = list(unique_controls.values())
    controls_list.sort(key=lambda x: x['control_id'])
    
    # Sort AWS config rules within each control alphabetically
    for control in controls_list:
        control['aws_config_rules'].sort(key=lambda x: x['aws_config_rule'])
    
    # Create output structure
    output_data = {
        'extraction_info': {
            'source_file': str(input_file_path),
            'extraction_date': datetime.now().isoformat(),
            'total_unique_controls': len(controls_list),
            'total_config_rule_mappings': sum(len(c['aws_config_rules']) for c in controls_list),
            'source_mappings_count': data['total_mappings']
        },
        'unique_pci_controls': controls_list
    }
    
    # Generate summary statistics
    rule_counts = [len(control['aws_config_rules']) for control in controls_list]
    avg_rules_per_control = sum(rule_counts) / len(rule_counts) if rule_counts else 0
    max_rules_per_control = max(rule_counts) if rule_counts else 0
    min_rules_per_control = min(rule_counts) if rule_counts else 0
    
    output_data['extraction_info']['statistics'] = {
        'avg_rules_per_control': round(avg_rules_per_control, 2),
        'max_rules_per_control': max_rules_per_control,
        'min_rules_per_control': min_rules_per_control
    }
    
    # Save to output file
    try:
        # Ensure output directory exists
        output_path = Path(output_file_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file_path, 'w', encoding='utf-8') as f:
            dump(output_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Successfully extracted {len(controls_list)} unique PCI controls")
        print(f"📁 Saved to: {output_file_path}")
        print(f"📊 Statistics:")
        print(f"   - Total config rule mappings: {output_data['extraction_info']['total_config_rule_mappings']}")
        print(f"   - Average rules per control: {avg_rules_per_control:.2f}")
        print(f"   - Control with most rules: {max_rules_per_control} rules")
        print(f"   - Control with fewest rules: {min_rules_per_control} rules")
        
        return True
        
    except Exception as e:
        print(f"Error: Failed to save output file - {e}")
        return False

def preview_controls(output_file_path, num_controls=3):
    """Preview a few controls to show the structure"""
    try:
        with open(output_file_path, 'r', encoding='utf-8') as f:
            data = load(f)
        
        print(f"\n📋 Preview of first {num_controls} controls:")
        print("=" * 60)
        
        for i, control in enumerate(data['unique_pci_controls'][:num_controls]):
            print(f"\n{i+1}. Control: {control['control_id']}")
            print(f"   Description: {control['control_description'][:80]}...")
            print(f"   AWS Config Rules ({len(control['aws_config_rules'])}):")
            
            for j, rule in enumerate(control['aws_config_rules'][:3]):  # Show first 3 rules
                print(f"     {j+1}. {rule['aws_config_rule']}")
                print(f"        Guidance: {rule['guidance'][:60]}...")
            
            if len(control['aws_config_rules']) > 3:
                print(f"     ... and {len(control['aws_config_rules']) - 3} more rules")
        
        print("=" * 60)
        
    except Exception as e:
        print(f"Error previewing controls: {e}")

def main():
    """Main execution function"""
    
    # File paths
    input_file = "shared_data/outputs/aws_config_guidance/aws_config_mappings.json"
    output_file = "shared_data/outputs/aws_config_guidance/unique_pci_controls.json"
    
    print("🔍 Extracting unique PCI controls with AWS Config rules...")
    print(f"📂 Input:  {input_file}")
    print(f"📂 Output: {output_file}")
    print("-" * 60)
    
    success = extract_unique_pci_controls(input_file, output_file)
    
    if success:
        print("\n🎉 Extraction completed successfully!")
        preview_controls(output_file)
        print(f"\nYou can now use the unique PCI controls file for Bedrock Knowledge Base chunking.")
    else:
        print("\n❌ Extraction failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()