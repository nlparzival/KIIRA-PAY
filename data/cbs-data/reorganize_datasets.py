#!/usr/bin/env python3
"""
Reorganiseer CBS datasets in categorie mappen.
Moved from flat structure naar categorized structure.
"""

import json
import shutil
from pathlib import Path

def reorganize_datasets():
    """Move datasets to category folders."""
    
    # Load categorized info
    with open('cbs_datasets_categorized.json', 'r') as f:
        categorized = json.load(f)
    
    # Build mapping: dataset_id -> category
    dataset_to_category = {}
    
    categories = ['energie', 'hernieuwbaar', 'co2', 'verbruik', 'productie']
    for category in categories:
        if category in categorized:
            for ds in categorized[category]:
                ds_id = ds.get('id', '')
                if ds_id:
                    # Als dataset in meerdere categories zit, eerste wint
                    if ds_id not in dataset_to_category:
                        dataset_to_category[ds_id] = category
    
    # Create category folders
    complete_dir = Path('data/complete')
    for category in categories:
        category_dir = complete_dir / category
        category_dir.mkdir(exist_ok=True)
        print(f"✓ Created: {category_dir}")
    
    # Create 'other' for uncategorized
    other_dir = complete_dir / 'other'
    other_dir.mkdir(exist_ok=True)
    
    print("\n" + "=" * 80)
    print("MOVING DATASETS TO CATEGORIES...")
    print("=" * 80)
    
    moved = {cat: 0 for cat in categories}
    moved['other'] = 0
    skipped = 0
    
    # Move each dataset
    for ds_dir in complete_dir.iterdir():
        if not ds_dir.is_dir():
            continue
        
        # Skip category folders
        if ds_dir.name in categories + ['other']:
            continue
        
        ds_id = ds_dir.name
        category = dataset_to_category.get(ds_id, 'other')
        
        # Target location
        target_dir = complete_dir / category / ds_id
        
        # Check if already exists
        if target_dir.exists():
            print(f"⏭  {ds_id:15} -> {category:15} (already exists)")
            skipped += 1
            continue
        
        # Move
        try:
            shutil.move(str(ds_dir), str(target_dir))
            print(f"✓ {ds_id:15} -> {category:15}")
            moved[category] += 1
        except Exception as e:
            print(f"✗ {ds_id:15} -> ERROR: {e}")
    
    # Summary
    print("\n" + "=" * 80)
    print("REORGANIZATION COMPLETE")
    print("=" * 80)
    
    for category in categories + ['other']:
        count = moved[category]
        print(f"  {category:15} {count:4} datasets")
    
    print(f"\n  Skipped:        {skipped:4} (already in place)")
    print(f"  Total moved:    {sum(moved.values()):4}")
    
    # Verify structure
    print("\n" + "=" * 80)
    print("FINAL STRUCTURE:")
    print("=" * 80)
    
    for category in categories + ['other']:
        category_dir = complete_dir / category
        if category_dir.exists():
            count = len([d for d in category_dir.iterdir() if d.is_dir()])
            print(f"  data/complete/{category:15} {count:4} datasets")
    
    print("\n✨ Done!")

if __name__ == "__main__":
    reorganize_datasets()
