#!/usr/bin/env python3
"""
Download ALLE energie-gerelateerde CBS datasets.
Categorieën: energie, hernieuwbaar, co2, verbruik, productie
Total: ~1,218 datasets
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
        error = str(e)[:100]
        print(f"   ❌ {error}")
        return {'status': 'error', 'error': error}

def get_all_energie_datasets():
    """Get ALL energie-related datasets."""
    with open('/Users/moesa/KIIRA-PAY/cbs-data/cbs_datasets_categorized.json', 'r') as f:
        data = json.load(f)
    
    # ALL energie categories
    energie_cats = ['energie', 'hernieuwbaar', 'co2', 'verbruik', 'productie']
    
    all_datasets = []
    seen = set()
    
    for cat in energie_cats:
        if cat in data and isinstance(data[cat], list):
            for ds in data[cat]:
                ds_id = ds.get('id', '')
                if ds_id and ds_id not in seen:
                    seen.add(ds_id)
                    all_datasets.append({
                        'id': ds_id,
                        'title': ds.get('title', 'Unknown')[:80],
                        'category': cat
                    })
    
    return all_datasets

def main():
    print("=" * 80)
    print("🔋 CBS ENERGIE MASS DOWNLOAD - ALLE ENERGIE DATASETS")
    print("=" * 80)
    print()
    
    # Get ALL energie datasets
    datasets = get_all_energie_datasets()
    output_dir = Path('/Users/moesa/KIIRA-PAY/cbs-data/data/complete')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Filter to download
    to_download = [ds for ds in datasets if not dataset_already_downloaded(ds['id'], output_dir)]
    already_done = len(datasets) - len(to_download)
    
    print(f"🔋 Energie datasets available: {len(datasets)}")
    print(f"✅ Already downloaded: {already_done}")
    print(f"⬇️  To download: {len(to_download)}")
    print(f"⏱️  Estimated time: ~{len(to_download) * 1.5 / 60:.0f} minutes ({len(to_download) * 1.5 / 3600:.1f} hours)")
    print()
    
    if len(to_download) == 0:
        print("✨ All energie datasets already downloaded!")
        return
    
    print("Categorieën breakdown:")
    from collections import Counter
    cat_counts = Counter([ds['category'] for ds in to_download])
    for cat, count in cat_counts.items():
        print(f"  {cat:20} {count:4} to download")
    print()
    
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
        
        result = download_dataset(api, ds_id, ds_name, output_dir)
        result['id'] = ds_id
        result['category'] = category
        results.append(result)
        
        if result['status'] == 'success':
            successful_count += 1
        
        # Progress update every 50
        if i % 50 == 0:
            elapsed = (datetime.now() - start_time).total_seconds()
            rate = i / elapsed if elapsed > 0 else 0
            remaining = (len(to_download) - i) / rate if rate > 0 else 0
            
            # Save progress
            progress = {
                'timestamp': datetime.now().isoformat(),
                'processed': i,
                'total': len(to_download),
                'successful': successful_count,
                'elapsed_minutes': elapsed/60,
                'remaining_minutes': remaining/60
            }
            with open(output_dir / 'download_energie_progress.json', 'w') as f:
                json.dump(progress, f, indent=2)
            
            print(f"\n{'='*80}")
            print(f"📊 PROGRESS: {i}/{len(to_download)} ({i/len(to_download)*100:.1f}%)")
            print(f"⏱️  Elapsed: {elapsed/60:.1f}min | Remaining: ~{remaining/60:.1f}min (~{remaining/3600:.1f}h)")
            print(f"✅ Success: {successful_count}/{i} ({successful_count/i*100:.0f}%)")
            print(f"{'='*80}\n")
        
        time.sleep(1.0)
    
    # Final summary
    elapsed = (datetime.now() - start_time).total_seconds()
    successful = [r for r in results if r['status'] == 'success']
    failed = [r for r in results if r['status'] in ['error', 'empty']]
    
    print("\n" + "=" * 80)
    print("✅ DOWNLOAD COMPLETE")
    print("=" * 80)
    print(f"⏱️  Total time: {elapsed/60:.1f} minutes ({elapsed/3600:.1f} hours)")
    print(f"✅ Success: {len(successful)} ({len(successful)/len(results)*100:.0f}%)")
    print(f"❌ Failed: {len(failed)}")
    print(f"📈 Total rows: {sum(r.get('rows', 0) for r in successful):,}")
    print(f"💾 Total size: ~{sum(r.get('rows', 0) for r in successful) * 0.001:.0f} MB estimated")
    
    # Save summary
    summary = {
        'timestamp': datetime.now().isoformat(),
        'total_energie_datasets': len(datasets),
        'already_had': already_done,
        'attempted': len(to_download),
        'successful': len(successful),
        'failed': len(failed),
        'total_rows': sum(r.get('rows', 0) for r in successful),
        'duration_minutes': round(elapsed/60, 2),
        'duration_hours': round(elapsed/3600, 2),
        'results': results
    }
    
    summary_file = output_dir / 'download_summary_energie_complete.json'
    with open(summary_file, 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"\n💾 Summary saved: {summary_file}")
    
    # Category breakdown
    print(f"\nSuccessful downloads per category:")
    from collections import Counter
    success_by_cat = Counter([r['category'] for r in successful])
    for cat, count in sorted(success_by_cat.items(), key=lambda x: x[1], reverse=True):
        print(f"  {cat:20} {count:4} datasets")

if __name__ == "__main__":
    main()
