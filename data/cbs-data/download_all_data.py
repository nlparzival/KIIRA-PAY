#!/usr/bin/env python3
"""
Download ALLE data van de top CBS datasets en sla op voor offline gebruik.
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
            print(f"   ✅ Got {rows} rows")
            
            # Create output directory
            dataset_dir = output_dir / dataset_id
            dataset_dir.mkdir(parents=True, exist_ok=True)
            
            # Save as CSV
            csv_file = dataset_dir / f"{dataset_id}_full_data.csv"
            data.to_csv(csv_file, index=False)
            print(f"   💾 Saved CSV: {csv_file}")
            
            # Save as JSON
            json_file = dataset_dir / f"{dataset_id}_full_data.json"
            data.to_json(json_file, orient='records', indent=2)
            print(f"   💾 Saved JSON: {json_file}")
            
            # Get metadata
            metadata = api.get_dataset_info(dataset_id)
            if metadata:
                meta_file = dataset_dir / f"{dataset_id}_metadata.json"
                with open(meta_file, 'w') as f:
                    json.dump(metadata, f, indent=2)
                print(f"   📋 Saved metadata: {meta_file}")
            
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

def main():
    print("=" * 80)
    print("📥 CBS DATA DOWNLOAD - COMPLETE DATASETS")
    print("=" * 80)
    print()
    
    # Initialize API
    api = CBSDataAPI()
    
    # Output directory
    output_dir = Path('/Users/moesa/KIIRA-PAY/cbs-data/data/complete')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Top 10 datasets voor dashboard (uitgebreid van 5 naar 10)
    datasets = [
        # Huidige 5
        ('82610ENG', 'Renewable Electricity Production'),
        ('70802eng', 'Wind Energy Production'),
        ('80324ned', 'Energy Prices'),
        ('82369ENG', 'Industry Energy Consumption'),
        ('83109ENG', 'CO2 Avoided by Renewable Energy'),
        # Nieuwe 5
        ('70789eng', 'Renewable Electricity Import/Export'),
        ('71457eng', 'Renewable Energy Capacity'),
        ('82610NED', 'Hernieuwbare Elektriciteit (NL)'),
        ('84917ENG', 'Renewable Energy Consumption by Source'),
        ('70802ned', 'Windenergie (NL)'),
    ]
    
    print(f"Downloading {len(datasets)} datasets to: {output_dir}")
    print()
    
    results = []
    
    for dataset_id, dataset_name in datasets:
        result = download_and_save_dataset(api, dataset_id, dataset_name, output_dir)
        results.append(result)
        
        # Small delay between requests
        import time
        time.sleep(1)
    
    # Save summary
    summary_file = output_dir / 'download_summary.json'
    summary = {
        'download_timestamp': datetime.now().isoformat(),
        'total_datasets': len(datasets),
        'successful': len([r for r in results if r['status'] == 'success']),
        'failed': len([r for r in results if r['status'] != 'success']),
        'results': results
    }
    
    with open(summary_file, 'w') as f:
        json.dump(summary, f, indent=2)
    
    # Print summary
    print("\n" + "=" * 80)
    print("📊 DOWNLOAD SUMMARY")
    print("=" * 80)
    print()
    print(f"Total datasets: {summary['total_datasets']}")
    print(f"✅ Successful: {summary['successful']}")
    print(f"❌ Failed: {summary['failed']}")
    print()
    
    # Show successful downloads
    successful = [r for r in results if r['status'] == 'success']
    if successful:
        print("✅ Successfully downloaded:")
        for r in successful:
            print(f"   {r['id']:15s} - {r['rows']:6,d} rows, {r['columns']:3d} cols, {r['periods']:3d} periods")
    
    # Show failures
    failed = [r for r in results if r['status'] != 'success']
    if failed:
        print("\n❌ Failed downloads:")
        for r in failed:
            print(f"   {r['id']:15s} - {r.get('error', 'Unknown error')[:60]}")
    
    print()
    print(f"💾 Data saved to: {output_dir}")
    print(f"📋 Summary saved to: {summary_file}")
    print("=" * 80)

if __name__ == "__main__":
    main()
