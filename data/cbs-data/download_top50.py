#!/usr/bin/env python3
"""
Download TOP 50 unieke CBS datasets voor uitgebreide analyse.
"""

import sys
import json
from pathlib import Path
from datetime import datetime

# Add cbs-data to path
sys.path.insert(0, '/Users/moesa/KIIRA-PAY/cbs-data')

from cbs_api import CBSDataAPI

def download_and_save_dataset(api, dataset_id, dataset_name, output_dir):
    """Download een dataset en sla op als JSON en CSV."""
    print(f"\n📥 Downloading {dataset_name} ({dataset_id})...")
    
    try:
        # Get data
        data = api.get_dataset_data(dataset_id)
        
        if data is not None and not data.empty:
            rows = len(data)
            print(f"   ✅ Got {rows:,} rows")
            
            # Create output directory
            dataset_dir = output_dir / dataset_id
            dataset_dir.mkdir(parents=True, exist_ok=True)
            
            # Save as CSV
            csv_file = dataset_dir / f"{dataset_id}_full_data.csv"
            data.to_csv(csv_file, index=False)
            print(f"   💾 Saved CSV: {csv_file.name}")
            
            # Save as JSON
            json_file = dataset_dir / f"{dataset_id}_full_data.json"
            data.to_json(json_file, orient='records', indent=2)
            print(f"   💾 Saved JSON: {json_file.name}")
            
            # Get metadata
            metadata = api.get_dataset_info(dataset_id)
            if metadata:
                meta_file = dataset_dir / f"{dataset_id}_metadata.json"
                with open(meta_file, 'w') as f:
                    json.dump(metadata, f, indent=2)
                print(f"   📋 Saved metadata")
            
            # Get periods
            periods = api.get_periods(dataset_id)
            if periods:
                periods_file = dataset_dir / f"{dataset_id}_periods.json"
                with open(periods_file, 'w') as f:
                    json.dump(periods, f, indent=2)
                print(f"   📅 Saved {len(periods)} periods")
            
            return {
                'id': dataset_id,
                'name': dataset_name,
                'status': 'success',
                'rows': rows,
                'columns': len(data.columns),
                'periods': len(periods) if periods else 0,
                'downloaded_at': datetime.now().isoformat()
            }
        else:
            print(f"   ❌ No data available")
            return {
                'id': dataset_id,
                'name': dataset_name,
                'status': 'empty',
                'error': 'No data returned'
            }
    
    except Exception as e:
        print(f"   ❌ Error: {str(e)[:100]}")
        return {
            'id': dataset_id,
            'name': dataset_name,
            'status': 'error',
            'error': str(e)[:200]
        }

def dataset_already_downloaded(dataset_id, output_dir):
    """Check if dataset is already downloaded."""
    dataset_dir = output_dir / dataset_id
    json_file = dataset_dir / f"{dataset_id}_full_data.json"
    return json_file.exists()

def get_unique_top_datasets(n=50):
    """Get top N unique datasets from prioritized list."""
    with open('/Users/moesa/KIIRA-PAY/cbs-data/cbs_prioritized_datasets.json', 'r') as f:
        data = json.load(f)
    
    must_have = data['must_have']
    
    # Get unique datasets (same ID can appear multiple times for different categories)
    seen = set()
    unique_datasets = []
    
    for ds in must_have:
        ds_id = ds['id']
        if ds_id not in seen:
            seen.add(ds_id)
            unique_datasets.append({
                'id': ds_id,
                'title': ds['title'],
                'score': ds['score'],
                'category': ds['category']
            })
    
    return unique_datasets[:n]

def main():
    print("=" * 80)
    print("📥 CBS DATA MASS DOWNLOAD - TOP 50 DATASETS")
    print("=" * 80)
    print()
    
    # Initialize API
    api = CBSDataAPI()
    
    # Output directory
    output_dir = Path('/Users/moesa/KIIRA-PAY/cbs-data/data/complete')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Get top 50 unique datasets
    datasets = get_unique_top_datasets(50)
    
    # Check what's already downloaded
    already_done = [ds for ds in datasets if dataset_already_downloaded(ds['id'], output_dir)]
    to_download = [ds for ds in datasets if not dataset_already_downloaded(ds['id'], output_dir)]
    
    print(f"📊 Found {len(datasets)} unique top datasets")
    print(f"✅ Already downloaded: {len(already_done)}")
    print(f"⬇️  To download: {len(to_download)}")
    print(f"💾 Downloading to: {output_dir}")
    print(f"⏱️  Estimated time: ~{len(to_download) * 2 / 60:.0f} minutes")
    print()
    
    results = []
    start_time = datetime.now()
    
    for i, ds in enumerate(datasets, 1):
        print(f"\n{'='*80}")
        print(f"[{i}/{len(datasets)}] {ds['title'][:70]}")
        print(f"Score: {ds['score']} | Category: {ds['category']}")
        print(f"{'='*80}")
        
        # Skip if already downloaded
        if dataset_already_downloaded(ds['id'], output_dir):
            print(f"⏭️  Already downloaded, skipping...")
            results.append({
                'id': ds['id'],
                'name': ds['title'],
                'status': 'skipped',
                'reason': 'already_downloaded'
            })
            continue
        
        result = download_and_save_dataset(api, ds['id'], ds['title'], output_dir)
        results.append(result)
        
        # Progress update every 10
        if i % 10 == 0:
            elapsed = (datetime.now() - start_time).total_seconds()
            rate = i / elapsed if elapsed > 0 else 0
            remaining = (len(datasets) - i) / rate if rate > 0 else 0
            
            successful = len([r for r in results if r['status'] == 'success'])
            print(f"\n📊 Progress: {i}/{len(datasets)} ({i/len(datasets)*100:.1f}%)")
            print(f"⏱️  Elapsed: {elapsed/60:.1f}min, Remaining: ~{remaining/60:.1f}min")
            print(f"✅ Success: {successful}/{i} ({successful/i*100:.0f}%)")
        
        # Rate limiting
        import time
        time.sleep(1.5)
    
    # Save summary
    summary_file = output_dir / 'download_summary_top50.json'
    summary = {
        'download_timestamp': datetime.now().isoformat(),
        'total_datasets': len(datasets),
        'successful': len([r for r in results if r['status'] == 'success']),
        'failed': len([r for r in results if r['status'] != 'success']),
        'total_rows': sum(r.get('rows', 0) for r in results if r['status'] == 'success'),
        'results': results
    }
    
    with open(summary_file, 'w') as f:
        json.dump(summary, f, indent=2)
    
    # Print summary
    elapsed_total = (datetime.now() - start_time).total_seconds()
    
    print("\n" + "=" * 80)
    print("📊 DOWNLOAD COMPLETE - SUMMARY")
    print("=" * 80)
    print()
    print(f"⏱️  Total time: {elapsed_total/60:.1f} minutes")
    print(f"📊 Total datasets: {summary['total_datasets']}")
    print(f"✅ Successful: {summary['successful']} ({summary['successful']/summary['total_datasets']*100:.0f}%)")
    print(f"❌ Failed: {summary['failed']}")
    print(f"📈 Total rows downloaded: {summary['total_rows']:,}")
    print()
    
    # Show successful downloads
    successful = [r for r in results if r['status'] == 'success']
    if successful:
        print("✅ Successfully downloaded:")
        for r in sorted(successful, key=lambda x: x['rows'], reverse=True)[:20]:
            print(f"   {r['id']:15s} - {r['rows']:7,d} rows, {r['columns']:3d} cols")
    
    # Show failures
    failed = [r for r in results if r['status'] != 'success']
    if failed:
        print(f"\n❌ Failed downloads ({len(failed)}):")
        for r in failed[:10]:
            print(f"   {r['id']:15s} - {r.get('error', 'Unknown')[:60]}")
    
    print()
    print(f"💾 Data saved to: {output_dir}")
    print(f"📋 Summary saved to: {summary_file}")
    print("=" * 80)

if __name__ == "__main__":
    main()
