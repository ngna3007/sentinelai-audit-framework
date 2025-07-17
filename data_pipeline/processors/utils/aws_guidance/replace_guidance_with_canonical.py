#!/usr/bin/env python3
"""
Replace aws_config_rule and guidance in unique_pci_controls.json with canonical values from unique_aws_config_rules.json
"""
from json import load, dump
from pathlib import Path

# File paths
PCI_CONTROLS_PATH = "shared_data/outputs/aws_config_guidance/unique_pci_controls.json"
CANONICAL_RULES_PATH = "shared_data/outputs/aws_config_guidance/unique_aws_config_rules.json"


def main():
    # Load canonical rules
    with open(CANONICAL_RULES_PATH, 'r', encoding='utf-8') as f:
        canonical_data = load(f)
    canonical_map = {
        rule['aws_config_rule']: rule['guidance']
        for rule in canonical_data['unique_config_rules']
    }
    canonical_names = set(canonical_map.keys())

    # Load PCI controls
    with open(PCI_CONTROLS_PATH, 'r', encoding='utf-8') as f:
        pci_data = load(f)

    replaced = 0
    not_found = set()
    for control in pci_data['unique_pci_controls']:
        for rule in control['aws_config_rules']:
            rule_name = rule['aws_config_rule']
            if rule_name in canonical_map:
                # Replace guidance and ensure canonical rule name
                rule['aws_config_rule'] = rule_name  # Canonical name
                rule['guidance'] = canonical_map[rule_name]
                replaced += 1
            else:
                # Try to find a close match (case-insensitive, whitespace-insensitive)
                matches = [cn for cn in canonical_names if cn.lower().replace('-', '').replace('_', '') == rule_name.lower().replace('-', '').replace('_', '')]
                if matches:
                    canonical = matches[0]
                    rule['aws_config_rule'] = canonical
                    rule['guidance'] = canonical_map[canonical]
                    replaced += 1
                else:
                    not_found.add(rule_name)

    # Overwrite the file
    with open(PCI_CONTROLS_PATH, 'w', encoding='utf-8') as f:
        dump(pci_data, f, indent=2, ensure_ascii=False)

    print(f"Replaced {replaced} aws_config_rule+guidance pairs.")
    if not_found:
        print(f"Warning: {len(not_found)} rules not found in canonical list:")
        for nf in sorted(not_found):
            print(f"  - {nf}")
    else:
        print("All rules matched canonical list.")

if __name__ == "__main__":
    main()