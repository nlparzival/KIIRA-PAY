#!/usr/bin/env python3
"""
Download TOP 200 CBS datasets voor KIIRA-PAY.
Focus op energie, economie, prijzen, verbruik.
"""

import sys
import json
from pathlib import Path
from datetime import datetime
import time

sys.path.insert(0, '/Users/moesa/KIIRA-PAY/cbs-data')
from cbs_api import CBSDataAPI

def dataset_already_downloaded(dataset_id, output_dir):
    """Check if dataset already exists."""
    dataset_dir = output_dir / dataset_id
    json_file = dataset_dir / f"{dataset_id}_full_data.json"
    return json_file.exists()

def download_dataset(api, dataset_id, dataset_name, output_dir):
    """Download a dataset."""
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
            
            print(f"   ✅ {rows:,} rows, {len(data.columns)} cols")
            return {'status': 'success', 'rows': rows, 'columns': len(data.columns)}
        else:
            print(f"   ⚠️  Empty")
            return {'status': 'empty'}
    
    except Exception as e:
        error = str(e)[:80]
        print(f"   ❌ {error}")
        return {'status': 'error', 'error': error}

def get_top_datasets(n=200):
    """Get top N datasets from categorized list."""
    with open('/Users/moesa/KIIRA-PAY/cbs-data/cbs_datasets_categorized.json', 'r') as f:
        data = json.load(f)
    
    # Priority categories
    priority_cats = ['energie', 'hernieuwbaar', 'co2', 'prijzen', 'verbruik', 'productie', 'economie']
    
    all_datasets = []
    seen = set()
    
    # Get datasets from priority categories
    for cat in priority_cats:
        if cat in data and isinstance(data[cat], list):
            for ds in data[cat]:
                ds_id = ds.get('id', ds.get('Identifier', ''))
                if ds_id and ds_id not in seen:
                    seen.add(ds_id)
                    all_datasets.append({
                        'id': ds_id,
                        'title': ds.get('title', ds.get('Title', 'Unknown'))[:80],
                        'category': cat
                    })
    
    return all_datasets[:n]

def main():
    print("=" * 80)
    print("📥 CBS MASS DOWNLOAD - TOP 200 DATASETS")
    print("=" * 80)
    print()
    
    # Get datasets
    datasets = get_top_datasets(200)
    output_dir = Path('/Users/moesa/KIIRA-PAY/cbs-data/data/complete')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Filter already downloaded
    to_download = [ds for ds in datasets if not dataset_already_downloaded(ds['id'], output_dir)]
    already_done = len(datasets) - len(to_download)
    
    print(f"📊 Target datasets: {len(datasets)}")
    print(f"✅ Already done: {already_done}")
    print(f"⬇️  To download: {len(to_download)}")
    print(f"⏱️  Est. time: ~{len(to_download) * 1.5 / 60:.0f} minutes")
    print()
    
    if len(to_download) == 0:
        print("✨ All datasets already downloaded!")
        return
    
    # Download
    api = CBSDataAPI()
    results = []
    start_time = datetime.now()
    successful_count = 0
    
    for i, ds in enumerate(to_download, 1):
        ds_id = ds['id']
        ds_name = ds['title']
        category = ds['category']
        
        print(f"[{i}/{len(to_download)}] {ds_id} ({category})")
        print(f"  {ds_name[:70]}")
        
        result = download_dataset(api, ds_id, ds_name, output_dir)
        result['id'] = ds_id
        result['category'] = category
        results.append(result)
        
        if result['status'] == 'success':
            successful_count += 1
        
        # Progress update
        if i % 20 == 0:
            elapsed = (datetime.now() - start_time).total_seconds()
            rate = i / elapsed if elapsed > 0 else 0
            remaining = (len(to_download) - i) / rate if rate > 0 else 0
            
            print(f"\n📊 Progress: {i}/{len(to_download)} ({i/len(to_download)*100:.0f}%)")
            print(f"⏱️  Elapsed: {elapsed/60:.1f}min | Remaining: ~{remaining/60:.1f}min")
            print(f"✅ Success rate: {successful_count}/{i} ({successful_count/i*100:.0f}%)\n")
        
        time.sleep(1.0)
    
    # Final summary
    elapsed = (datetime.now() - start_time).total_seconds()
    successful = [r for r in results if r['status'] == 'success']
    failed = [r for r in results if r['status'] in ['error', 'empty']]
    
    print("\n" + "=" * 80)
    print("✅ DOWNLOAD COMPLETE")
    print("=" * 80)
    print(f"⏱️  Time: {elapsed/60:.1f} minutes")
    print(f"✅ Success: {len(successful)} ({len(successful)/len(results)*100:.0f}%)")
    print(f"❌ Failed: {len(failed)}")
    print(f"📈 Total rows: {sum(r.get('rows', 0) for r in successful):,}")
    
    # Save summary
    summary = {
        'timestamp': datetime.now().isoformat(),
        'target_datasets': len(datasets),
        'already_had': already_done,
        'attempted': len(to_download),
        'successful': len(successful),
        'failed': len(failed),
        'total_rows': sum(r.get('rows', 0) for r in successful),
        'duration_minutes': round(elapsed/60, 2),
        'results': results
    }
    
    summary_file = output_dir / 'download_summary_top200.json'
    with open(summary_file, 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"💾 Summary: {summary_file}")
    
    # Show failures if any
    if failed and len(failed) <= 20:
        print(f"\n❌ Failed datasets:")
        for r in failed:
            print(f"  - {r['id']}: {r.get('error', 'empty')[:50]}")

if __name__ == "__main__":
    main()
