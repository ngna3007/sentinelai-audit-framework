#!/usr/bin/env python3
"""
Remove duplicate mappings from aws_config_mappings.json
"""
import json
from pathlib import Path
from datetime import datetime
from collections import Counter

# File paths
MAPPINGS_PATH = "shared_data/outputs/aws_config_guidance/aws_config_mappings.json"

def main():
    print("🧹 Removing duplicate mappings from aws_config_mappings.json...")
    print(f"📂 Source file: {MAPPINGS_PATH}")
    print("=" * 60)
    
    # Load the mappings file
    with open(MAPPINGS_PATH, 'r', encoding='utf-8') as f:
        mappings_data = json.load(f)
    
    original_count = len(mappings_data['mappings'])
    print(f"📋 Original mappings: {original_count}")
    
    # Create tuples for duplicate detection
    mapping_tuples = []
    mapping_objects = []
    
    for mapping in mappings_data['mappings']:
        # Create tuple for duplicate detection (control_id, aws_config_rule, guidance)
        mapping_tuple = (
            mapping['control_id'],
            mapping['aws_config_rule'], 
            mapping['guidance']
        )
        mapping_tuples.append(mapping_tuple)
        mapping_objects.append(mapping)
    
    # Count occurrences
    counter = Counter(mapping_tuples)
    duplicates = {k: v for k, v in counter.items() if v > 1}
    
    print(f"📊 Found {len(duplicates)} duplicate mapping combinations")
    total_duplicate_instances = sum(v - 1 for v in duplicates.values())
    print(f"📊 Total duplicate instances to remove: {total_duplicate_instances}")
    
    if duplicates:
        print(f"\n🔍 Duplicate mappings found:")
        print("-" * 40)
        
        # Sort by control_id for easier reading
        sorted_duplicates = sorted(duplicates.items(), key=lambda x: x[0][0])
        
        for i, ((control_id, aws_config_rule, guidance), count) in enumerate(sorted_duplicates, 1):
            print(f"{i:2d}. Control: {control_id}")
            print(f"    Rule: {aws_config_rule}")
            print(f"    Occurrences: {count}")
    
    # Remove duplicates - keep only unique mappings
    seen = set()
    unique_mappings = []
    removed_count = 0
    
    for i, (mapping_tuple, mapping_obj) in enumerate(zip(mapping_tuples, mapping_objects)):
        if mapping_tuple not in seen:
            # First occurrence - keep it
            seen.add(mapping_tuple)
            unique_mappings.append(mapping_obj)
        else:
            # Duplicate - remove it
            removed_count += 1
    
    # Update mappings data
    mappings_data['mappings'] = unique_mappings
    mappings_data['total_mappings'] = len(unique_mappings)
    
    # Add deduplication metadata
    if 'deduplication_info' not in mappings_data:
        mappings_data['deduplication_info'] = {}
    
    mappings_data['deduplication_info'].update({
        'last_deduplicated': datetime.now().isoformat(),
        'original_count': original_count,
        'duplicates_removed': removed_count,
        'final_count': len(unique_mappings),
        'duplicate_combinations_found': len(duplicates)
    })
    
    # Save the deduplicated file
    with open(MAPPINGS_PATH, 'w', encoding='utf-8') as f:
        json.dump(mappings_data, f, indent=2, ensure_ascii=False)
    
    # Report results
    print(f"\n✅ Deduplication completed!")
    print(f"📊 Results:")
    print(f"   - Original mappings: {original_count}")
    print(f"   - Duplicates removed: {removed_count}")
    print(f"   - Final unique mappings: {len(unique_mappings)}")
    print(f"   - Reduction: {original_count - len(unique_mappings)} mappings")
    
    if removed_count == total_duplicate_instances:
        print(f"✅ Expected removal count matches actual: {removed_count}")
    else:
        print(f"⚠️  Expected {total_duplicate_instances}, removed {removed_count}")
    
    print(f"\n📁 Updated file: {MAPPINGS_PATH}")
    print(f"📁 Backup available: {MAPPINGS_PATH.replace('.json', '_backup.json')}")
    
    # Verify the result
    expected_final = original_count - total_duplicate_instances
    if len(unique_mappings) == expected_final:
        print(f"✅ Final count {len(unique_mappings)} matches expected {expected_final}")
    else:
        print(f"⚠️  Final count {len(unique_mappings)} differs from expected {expected_final}")

if __name__ == "__main__":
    main() 