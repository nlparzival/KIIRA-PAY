#!/usr/bin/env python3
"""
Download ALL must-have CBS datasets (189 total) with robust error handling.
Skips already downloaded files and provides detailed progress tracking.
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List
import time
from cbs_api import CBSAPIClient

# Directories
SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR / "data" / "complete"
PRIORITIZED_FILE = SCRIPT_DIR / "cbs_prioritized_datasets.json"
SUMMARY_FILE = DATA_DIR / "download_summary_must_have.json"

def load_must_have_datasets() -> List[Dict]:
    """Load all must-have priority datasets."""
    with open(PRIORITIZED_FILE, 'r', encoding='utf-8') as f:
        all_datasets = json.load(f)
    
    must_have = [ds for ds in all_datasets if ds.get('priority') == 'must-have']
    print(f"✓ Loaded {len(must_have)} must-have datasets")
    return must_have

def already_downloaded(dataset_id: str) -> bool:
    """Check if dataset is already downloaded."""
    file_path = DATA_DIR / f"{dataset_id}.json"
    return file_path.exists() and file_path.stat().st_size > 100  # Must be > 100 bytes

def download_dataset(client: CBSAPIClient, dataset_id: str, name: str) -> Dict:
    """Download a single dataset with error handling."""
    try:
        print(f"\n📥 Downloading: {dataset_id} - {name[:60]}...")
        
        # Fetch data
        df = client.get_typed_data(dataset_id)
        
        if df is None or df.empty:
            return {
                "id": dataset_id,
                "name": name,
                "status": "empty",
                "error": "No data returned",
                "rows": 0,
                "columns": 0
            }
        
        # Save to JSON
        file_path = DATA_DIR / f"{dataset_id}.json"
        data_dict = df.to_dict(orient='records')
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump({
                'metadata': {
                    'dataset_id': dataset_id,
                    'name': name,
                    'downloaded_at': datetime.now().isoformat(),
                    'rows': len(df),
                    'columns': len(df.columns)
                },
                'data': data_dict
            }, f, indent=2, ensure_ascii=False)
        
        file_size_mb = file_path.stat().st_size / (1024 * 1024)
        print(f"   ✓ Saved {len(df):,} rows × {len(df.columns)} cols ({file_size_mb:.2f} MB)")
        
        return {
            "id": dataset_id,
            "name": name,
            "status": "success",
            "rows": len(df),
            "columns": len(df.columns),
            "size_mb": round(file_size_mb, 2),
            "downloaded_at": datetime.now().isoformat()
        }
        
    except Exception as e:
        error_msg = str(e)
        print(f"   ✗ ERROR: {error_msg}")
        return {
            "id": dataset_id,
            "name": name,
            "status": "failed",
            "error": error_msg,
            "rows": 0,
            "columns": 0
        }

def save_progress(results: List[Dict], start_time: datetime):
    """Save current progress to summary file."""
    successful = [r for r in results if r['status'] == 'success']
    failed = [r for r in results if r['status'] == 'failed']
    empty = [r for r in results if r['status'] == 'empty']
    
    duration = (datetime.now() - start_time).total_seconds()
    
    summary = {
        "download_timestamp": datetime.now().isoformat(),
        "duration_seconds": round(duration, 2),
        "total_attempted": len(results),
        "successful": len(successful),
        "failed": len(failed),
        "empty": len(empty),
        "total_rows": sum(r.get('rows', 0) for r in successful),
        "total_size_mb": round(sum(r.get('size_mb', 0) for r in successful), 2),
        "results": results
    }
    
    with open(SUMMARY_FILE, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

def main():
    """Download all must-have datasets."""
    start_time = datetime.now()
    print("=" * 80)
    print("CBS MUST-HAVE DATASETS DOWNLOADER")
    print("=" * 80)
    
    # Ensure data directory exists
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    # Load datasets
    datasets = load_must_have_datasets()
    print(f"Target: {len(datasets)} datasets")
    
    # Check what's already downloaded
    already_done = sum(1 for ds in datasets if already_downloaded(ds['id']))
    print(f"Already downloaded: {already_done}")
    print(f"To download: {len(datasets) - already_done}")
    
    # Initialize client
    client = CBSAPIClient()
    results = []
    
    # Download each dataset
    for i, dataset in enumerate(datasets, 1):
        dataset_id = dataset['id']
        name = dataset.get('name', 'Unknown')
        
        print(f"\n[{i}/{len(datasets)}] {dataset_id}")
        
        # Skip if already downloaded
        if already_downloaded(dataset_id):
            print(f"   ⏭  Already downloaded, skipping...")
            results.append({
                "id": dataset_id,
                "name": name,
                "status": "skipped",
                "reason": "already_downloaded"
            })
            continue
        
        # Download
        result = download_dataset(client, dataset_id, name)
        results.append(result)
        
        # Save progress every 10 datasets
        if i % 10 == 0:
            save_progress(results, start_time)
            print(f"\n💾 Progress saved ({i}/{len(datasets)})")
        
        # Rate limiting
        time.sleep(0.5)
    
    # Final summary
    save_progress(results, start_time)
    
    print("\n" + "=" * 80)
    print("DOWNLOAD COMPLETE")
    print("=" * 80)
    
    successful = [r for r in results if r['status'] == 'success']
    failed = [r for r in results if r['status'] == 'failed']
    skipped = [r for r in results if r['status'] == 'skipped']
    
    print(f"✓ Successful: {len(successful)}")
    print(f"⏭ Skipped: {len(skipped)}")
    print(f"✗ Failed: {len(failed)}")
    print(f"Total rows: {sum(r.get('rows', 0) for r in successful):,}")
    print(f"Total size: {sum(r.get('size_mb', 0) for r in successful):.2f} MB")
    print(f"Duration: {(datetime.now() - start_time).total_seconds():.1f}s")
    print(f"\nResults saved to: {SUMMARY_FILE}")
    
    if failed:
        print("\n⚠️  Failed datasets:")
        for r in failed[:10]:  # Show first 10 failures
            print(f"   - {r['id']}: {r.get('error', 'Unknown error')}")
        if len(failed) > 10:
            print(f"   ... and {len(failed) - 10} more")

if __name__ == "__main__":
    main()
