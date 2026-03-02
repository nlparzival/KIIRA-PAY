#!/usr/bin/env python3
"""
Download ALLE CBS priority datasets (must + should + nice).
Total: ~92 unique datasets
"""

import sys
import json
from pathlib import Path
from datetime import datetime
import time

sys.path.insert(0, '/Users/moesa/KIIRA-PAY/cbs-data')
from cbs_api import CBSDataAPI

def dataset_already_downloaded(dataset_id, output_dir):
    """Check if dataset is already downloaded."""
    dataset_dir = output_dir / dataset_id
    json_file = dataset_dir / f"{dataset_id}_full_data.json"
    return json_file.exists()

def download_dataset(api, dataset_id, dataset_name, output_dir):
    """Download een dataset."""
    try:
        data = api.get_dataset_data(dataset_id)
        
        if data is not None and not data.empty:
            rows = len(data)
            
            dataset_dir = output_dir / dataset_id
            dataset_dir.mkdir(parents=True, exist_ok=True)
            
            # Save JSON
            json_file = dataset_dir / f"{dataset_id}_full_data.json"
            data.to_json(json_file, orient='records', indent=2)
            
            # Save CSV
            csv_file = dataset_dir / f"{dataset_id}_full_data.csv"
            data.to_csv(csv_file, index=False)
            
            print(f"   ✅ {rows:,} rows")
            return {'status': 'success', 'rows': rows, 'columns': len(data.columns)}
        else:
            print(f"   ⚠️  Empty")
            return {'status': 'empty'}
    
    except Exception as e:
        error = str(e)[:80]
        print(f"   ❌ {error}")
        return {'status': 'error', 'error': error}

def main():
    print("=" * 80)
    print("📥 CBS MASS DOWNLOAD - ALL PRIORITY DATASETS")
    print("=" * 80)
    print()
    
    # Load ALL datasets
    with open('/Users/moesa/KIIRA-PAY/cbs-data/cbs_prioritized_datasets.json', 'r') as f:
        data = json.load(f)
    
    # Combine ALL priority levels
    all_datasets = data['must_have'] + data['should_have'] + data['nice_to_have']
    
    # Get unique
    seen = set()
    unique_datasets = []
    for ds in all_datasets:
        if ds['id'] not in seen:
            seen.add(ds['id'])
            unique_datasets.append(ds)
    
    output_dir = Path('/Users/moesa/KIIRA-PAY/cbs-data/data/complete')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Filter to download
    to_download = [ds for ds in unique_datasets if not dataset_already_downloaded(ds['id'], output_dir)]
    already_done = len(unique_datasets) - len(to_download)
    
    print(f"📊 Total unique datasets: {len(unique_datasets)}")
    print(f"✅ Already downloaded: {already_done}")
    print(f"⬇️  To download: {len(to_download)}")
    print(f"⏱️  Estimated time: ~{len(to_download) * 1.5 / 60:.0f} minutes")
    print()
    
    if len(to_download) == 0:
        print("✨ Everything already downloaded!")
        return
    
    # Download
    api = CBSDataAPI()
    results = []
    start_time = datetime.now()
    
    for i, ds in enumerate(to_download, 1):
        ds_id = ds['id']
        ds_name = ds['title'][:60]
        priority = ds.get('priority', 'unknown')
        
        print(f"[{i}/{len(to_download)}] {ds_id} - {ds_name}")
        
        result = download_dataset(api, ds_id, ds_name, output_dir)
        result['id'] = ds_id
        result['priority'] = priority
        results.append(result)
        
        # Progress
        if i % 10 == 0:
            elapsed = (datetime.now() - start_time).total_seconds()
            successful = len([r for r in results if r['status'] == 'success'])
            print(f"\n📊 Progress: {i}/{len(to_download)} | ✅ {successful} | ⏱️ {elapsed/60:.1f}min\n")
        
        time.sleep(1.0)
    
    # Summary
    elapsed = (datetime.now() - start_time).total_seconds()
    successful = [r for r in results if r['status'] == 'success']
    failed = [r for r in results if r['status'] in ['error', 'empty']]
    
    print("\n" + "=" * 80)
    print("✅ DOWNLOAD COMPLETE")
    print("=" * 80)
    print(f"⏱️  Time: {elapsed/60:.1f} min")
    print(f"✅ Success: {len(successful)}")
    print(f"❌ Failed: {len(failed)}")
    print(f"📈 Total rows: {sum(r.get('rows', 0) for r in successful):,}")
    
    # Save summary
    summary = {
        'timestamp': datetime.now().isoformat(),
        'total_datasets': len(unique_datasets),
        'already_had': already_done,
        'attempted': len(to_download),
        'successful': len(successful),
        'failed': len(failed),
        'total_rows': sum(r.get('rows', 0) for r in successful),
        'results': results
    }
    
    summary_file = output_dir / 'download_summary_complete.json'
    with open(summary_file, 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"💾 Summary saved: {summary_file}")

if __name__ == "__main__":
    main()
