#!/usr/bin/env python3
"""
Recategoriseer 'other' datasets naar logische categorieën.
Vooral prijzen, woningen, arbeid.
"""

import shutil
from pathlib import Path
import json

def recategorize_other():
    """Move datasets from 'other' to better categories."""
    
    complete_dir = Path('data/complete')
    other_dir = complete_dir / 'other'
    
    # Load categorized info
    with open('cbs_datasets_categorized.json', 'r') as f:
        categorized = json.load(f)
    
    # Create mapping based on keywords
    moves = {}
    
    for ds_dir in other_dir.iterdir():
        if not ds_dir.is_dir():
            continue
        
        ds_id = ds_dir.name
        
        # Find in categorized
        ds_info = None
        for cat, datasets in categorized.items():
            if isinstance(datasets, list):
                for ds in datasets:
                    if ds.get('id') == ds_id:
                        ds_info = {'category': cat, 'title': ds.get('title', '').lower()}
                        break
        
        if not ds_info:
            continue
        
        title = ds_info['title']
        orig_cat = ds_info['category']
        
        # Determine new category based on keywords
        if 'prijs' in orig_cat or 'price' in orig_cat or 'cost' in orig_cat:
            new_cat = 'prijzen'
        elif 'woning' in title or 'dwelling' in title or 'hous' in title or 'building' in title:
            new_cat = 'woningen'
        elif 'arbeid' in title or 'labour' in title or 'employment' in title:
            new_cat = 'arbeid'
        elif 'inkomen' in title or 'income' in title:
            new_cat = 'economie'
        elif 'milieu' in title or 'environment' in title:
            new_cat = 'co2'  # environmental → co2 category
        else:
            new_cat = 'prijzen'  # Default for most 'other' (they're mostly prices)
        
        moves[ds_id] = new_cat
    
    # Create new category folders
    new_categories = set(moves.values())
    for cat in new_categories:
        cat_dir = complete_dir / cat
        cat_dir.mkdir(exist_ok=True)
        print(f"✓ Ensured category: {cat}")
    
    print("\n" + "=" * 80)
    print("MOVING DATASETS FROM 'OTHER':")
    print("=" * 80)
    
    moved_count = {}
    
    for ds_id, new_cat in sorted(moves.items()):
        source = other_dir / ds_id
        target = complete_dir / new_cat / ds_id
        
        if target.exists():
            print(f"⏭  {ds_id:15} → {new_cat:15} (already exists)")
            continue
        
        try:
            shutil.move(str(source), str(target))
            print(f"✓ {ds_id:15} → {new_cat:15}")
            moved_count[new_cat] = moved_count.get(new_cat, 0) + 1
        except Exception as e:
            print(f"✗ {ds_id:15} → ERROR: {e}")
    
    # Check what's left in other
    remaining = len([d for d in other_dir.iterdir() if d.is_dir()])
    
    print("\n" + "=" * 80)
    print("RECATEGORIZATION COMPLETE")
    print("=" * 80)
    
    for cat, count in sorted(moved_count.items()):
        print(f"  → {cat:15} {count:3} datasets moved")
    
    print(f"\n  Remaining in 'other': {remaining}")
    
    # Final structure
    print("\n" + "=" * 80)
    print("FINAL STRUCTURE:")
    print("=" * 80)
    
    all_categories = ['energie', 'hernieuwbaar', 'co2', 'verbruik', 'productie', 
                     'prijzen', 'woningen', 'arbeid', 'economie', 'other']
    
    for cat in all_categories:
        cat_dir = complete_dir / cat
        if cat_dir.exists():
            count = len([d for d in cat_dir.iterdir() if d.is_dir()])
            if count > 0:
                print(f"  data/complete/{cat:15} {count:4} datasets")
    
    print("\n✨ Done!")

if __name__ == "__main__":
    recategorize_other()
