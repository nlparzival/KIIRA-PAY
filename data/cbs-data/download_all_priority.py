#!/usr/bin/env python3
"""
Download ALLE priority CBS datasets (must-have + should-have).
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
    """Download een dataset en sla op."""
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
            
            # Get metadata
            try:
                metadata = api.get_dataset_info(dataset_id)
                if metadata:
                    meta_file = dataset_dir / f"{dataset_id}_metadata.json"
                    with open(meta_file, 'w') as f:
                        json.dump(metadata, f, indent=2)
            except:
                pass
            
            print(f"   ✅ {rows:,} rows, {len(data.columns)} columns")
            return {'status': 'success', 'rows': rows, 'columns': len(data.columns)}
        else:
            print(f"   ⚠️  No data")
            return {'status': 'empty'}
    
    except Exception as e:
        error = str(e)[:100]
        print(f"   ❌ {error}")
        return {'status': 'error', 'error': error}

def main():
    print("=" * 80)
    print("📥 CBS PRIORITY DATASETS DOWNLOAD (MUST-HAVE + SHOULD-HAVE)")
    print("=" * 80)
    print()
    
    # Load datasets
    with open('/Users/moesa/KIIRA-PAY/cbs-data/cbs_prioritized_datasets.json', 'r') as f:
        data = json.load(f)
    
    # Combine must-have and should-have
    all_priority = data['must_have'] + data['should_have']
    
    # Get unique datasets
    seen = set()
    unique_datasets = []
    for ds in all_priority:
        if ds['id'] not in seen:
            seen.add(ds['id'])
            unique_datasets.append(ds)
    
    output_dir = Path('/Users/moesa/KIIRA-PAY/cbs-data/data/complete')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Check what's already downloaded
    already_done = [ds for ds in unique_datasets if dataset_already_downloaded(ds['id'], output_dir)]
    to_download = [ds for ds in unique_datasets if not dataset_already_downloaded(ds['id'], output_dir)]
    
    print(f"📊 Total unique priority datasets: {len(unique_datasets)}")
    print(f"✅ Already downloaded: {len(already_done)}")
    print(f"⬇️  To download: {len(to_download)}")
    print(f"⏱️  Estimated time: ~{len(to_download) * 2 / 60:.0f} minutes")
    print()
    
    if len(to_download) == 0:
        print("✨ All datasets already downloaded!")
        return
    
    # Initialize API
    api = CBSDataAPI()
    results = []
    start_time = datetime.now()
    
    for i, ds in enumerate(unique_datasets, 1):
        ds_id = ds['id']
        ds_name = ds['title']
        priority = ds.get('priority', 'unknown')
        
        print(f"[{i}/{len(unique_datasets)}] {ds_id} - {ds_name[:55]}")
        print(f"   Priority: {priority}")
        
        # Skip if already downloaded
        if dataset_already_downloaded(ds_id, output_dir):
            print(f"   ⏭️  Already downloaded")
            results.append({'id': ds_id, 'status': 'skipped'})
            continue
        
        # Download
        result = download_dataset(api, ds_id, ds_name, output_dir)
        result['id'] = ds_id
        result['name'] = ds_name
        result['priority'] = priority
        results.append(result)
        
        # Progress update every 10
        if i % 10 == 0:
            successful = len([r for r in results if r['status'] == 'success'])
            elapsed = (datetime.now() - start_time).total_seconds()
            print(f"\n📊 Progress: {i}/{len(unique_datasets)} | Success: {successful} | Time: {elapsed/60:.1f}min\n")
        
        time.sleep(1.0)  # Rate limiting
    
    # Save summary
    summary_file = output_dir / 'download_summary_all_priority.json'
    summary = {
        'download_timestamp': datetime.now().isoformat(),
        'total_datasets': len(unique_datasets),
        'successful': len([r for r in results if r['status'] == 'success']),
        'failed': len([r for r in results if r['status'] in ['error', 'empty']]),
        'skipped': len([r for r in results if r['status'] == 'skipped']),
        'results': results
    }
    
    with open(summary_file, 'w') as f:
        json.dump(summary, f, indent=2)
    
    # Print summary
    elapsed = (datetime.now() - start_time).total_seconds()
    successful = [r for r in results if r['status'] == 'success']
    
    print("\n" + "=" * 80)
    print("✅ DOWNLOAD COMPLETE")
    print("=" * 80)
    print(f"⏱️  Time: {elapsed/60:.1f} minutes")
    print(f"📊 Total: {summary['total_datasets']}")
    print(f"✅ Success: {summary['successful']}")
    print(f"❌ Failed: {summary['failed']}")
    print(f"⏭️  Skipped: {summary['skipped']}")
    print(f"📈 Total rows: {sum(r.get('rows', 0) for r in successful):,}")
    print(f"\n💾 Saved to: {output_dir}")
    print(f"📄 Summary: {summary_file}")

if __name__ == "__main__":
    main()
