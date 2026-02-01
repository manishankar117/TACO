"""
Fix duplicate annotation IDs and category name inconsistencies in annotations.json
Addresses: https://github.com/pedropro/TACO/issues/12 (duplicate IDs)
Addresses: https://github.com/pedropro/TACO/issues/16 (category naming)
"""

import json
import argparse


def fix_duplicate_annotation_ids(data):
    """Fix duplicate annotation IDs in the dataset."""
    seen_ids = set()
    duplicates = []
    max_id = 0
    
    # Find duplicates and max ID
    for ann in data['annotations']:
        ann_id = ann['id']
        max_id = max(max_id, ann_id)
        if ann_id in seen_ids:
            duplicates.append(ann)
        else:
            seen_ids.add(ann_id)
    
    # Assign new unique IDs to duplicates
    for ann in duplicates:
        old_id = ann['id']
        max_id += 1
        ann['id'] = max_id
        print(f"Fixed duplicate annotation ID: {old_id} -> {max_id}")
    
    return len(duplicates)


def fix_category_names(data):
    """Fix category name inconsistencies in the dataset."""
    # Canonical names (matching map_*.csv files)
    name_fixes = {
        'Food can': 'Food Can',
    }
    
    fixed_count = 0
    for category in data['categories']:
        if category['name'] in name_fixes:
            old_name = category['name']
            category['name'] = name_fixes[old_name]
            print(f"Fixed category name: '{old_name}' -> '{category['name']}'")
            fixed_count += 1
    
    return fixed_count


def main():
    parser = argparse.ArgumentParser(
        description='Fix duplicate annotation IDs and category name inconsistencies in TACO annotations'
    )
    parser.add_argument(
        '--input', 
        default='./data/annotations.json', 
        help='Input annotations file path (default: ./data/annotations.json)'
    )
    parser.add_argument(
        '--output', 
        default=None, 
        help='Output file path (default: overwrite input file)'
    )
    args = parser.parse_args()
    
    # Determine output path
    output_path = args.output if args.output else args.input
    
    # Load annotations
    print(f"Loading annotations from: {args.input}")
    with open(args.input, 'r') as f:
        data = json.load(f)
    
    # Fix duplicate IDs
    print("\nChecking for duplicate annotation IDs...")
    dup_fixed = fix_duplicate_annotation_ids(data)
    print(f"Fixed {dup_fixed} duplicate annotation ID(s)")
    
    # Fix category names
    print("\nChecking for inconsistent category names...")
    cat_fixed = fix_category_names(data)
    print(f"Fixed {cat_fixed} category name(s)")
    
    # Save results
    print(f"\nSaving annotations to: {output_path}")
    with open(output_path, 'w') as f:
        json.dump(data, f, indent=2)
    
    print("\nDone!")


if __name__ == '__main__':
    main()
