#!/usr/bin/env python3
"""
Quick validation: test top 30 must-have CBS datasets
"""

import sys
import json
from pathlib import Path

# Add cbs-data to path
sys.path.insert(0, '/Users/moesa/KIIRA-PAY/cbs-data')

from cbs_api import CBSDataAPI

def test_dataset(api, dataset_id, title):
    """Quick test of a single dataset."""
    try:
        # Try to get basic info and data
        info = api.get_dataset_info(dataset_id)
        data = api.get_dataset_data(dataset_id, top=5)
        
        if info and data is not None and not data.empty:
            return {
                'status': '✅ USABLE',
                'rows': len(data),
                'title_from_api': info.get('Title', 'Unknown')
            }
        elif info and (data is None or data.empty):
            return {'status': '⚠️  EMPTY', 'rows': 0}
        else:
            return {'status': '❌ NO DATA', 'rows': 0}
    except Exception as e:
        error_msg = str(e)
        if '404' in error_msg or 'not found' in error_msg.lower():
            return {'status': '❌ NOT FOUND', 'error': 'Dataset niet gevonden'}
        elif 'timeout' in error_msg.lower():
            return {'status': '⏱️  TIMEOUT', 'error': 'Te traag'}
        else:
            return {'status': '❌ ERROR', 'error': error_msg[:80]}

def main():
    print("=" * 80)
    print("🚀 CBS DATASETS VALIDATIE - TOP 30 MUST-HAVE")
    print("=" * 80)
    print()
    
    # Load prioritized datasets
    data_file = Path('/Users/moesa/KIIRA-PAY/cbs-data/cbs_prioritized_datasets.json')
    with open(data_file, 'r') as f:
        data = json.load(f)
    
    must_have = data['must_have'][:30]  # Top 30
    
    print(f"Testing {len(must_have)} hoogste priority datasets...\n")
    
    api = CBSDataAPI()
    
    results = {
        'usable': [],
        'empty': [],
        'errors': []
    }
    
    for i, ds in enumerate(must_have, 1):
        dataset_id = ds['id']
        title = ds['title']
        category = ds.get('category', 'unknown')
        score = ds.get('score', 0)
        
        print(f"[{i:2d}/30] {title[:55]}")
        print(f"        ID: {dataset_id} | Score: {score} | Category: {category}")
        
        result = test_dataset(api, dataset_id, title)
        
        print(f"        {result['status']}", end='')
        if result['status'] == '✅ USABLE':
            print(f" - {result['rows']} rows beschikbaar")
            results['usable'].append({
                'id': dataset_id,
                'title': title,
                'category': category,
                'score': score,
                'rows': result['rows']
            })
        elif 'error' in result:
            print(f" - {result.get('error', 'Unknown error')}")
            results['errors'].append({
                'id': dataset_id,
                'title': title,
                'error': result.get('error')
            })
        else:
            print()
            results['empty'].append({'id': dataset_id, 'title': title})
        
        print()
        
        # Rate limiting
        import time
        time.sleep(0.5)
    
    # Summary
    print("=" * 80)
    print("📊 SAMENVATTING")
    print("=" * 80)
    print()
    print(f"✅ Bruikbaar:  {len(results['usable'])}/{len(must_have)} ({len(results['usable'])/len(must_have)*100:.0f}%)")
    print(f"⚠️  Leeg:       {len(results['empty'])}")
    print(f"❌ Errors:     {len(results['errors'])}")
    print()
    
    if results['usable']:
        print("🎯 TOP BRUIKBARE DATASETS:")
        for i, ds in enumerate(results['usable'][:10], 1):
            print(f"  {i:2d}. {ds['title'][:60]}")
            print(f"      ID: {ds['id']} | Category: {ds['category']} | Score: {ds['score']}")
        print()
    
    # Save results
    output_file = Path('/Users/moesa/KIIRA-PAY/cbs-data/validation_results_top30.json')
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Volledige resultaten opgeslagen: {output_file}")
    print("=" * 80)

if __name__ == "__main__":
    main()
