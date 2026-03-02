#!/usr/bin/env python3
"""
Explore and validate categorized CBS datasets.
Shows detailed information per category and allows deep-dive into specific datasets.
"""

import os
import json
import pandas as pd
from pathlib import Path
from collections import defaultdict
import sys

def load_categorization_report():
    """Load the categorization report."""
    report_path = Path("data/complete/categorization_report.json")
    if report_path.exists():
        with open(report_path) as f:
            return json.load(f)
    return None

def explore_category(category_name):
    """Explore all datasets in a specific category."""
    category_path = Path(f"data/complete/{category_name}")
    
    if not category_path.exists():
        print(f"❌ Category '{category_name}' not found!")
        return
    
    print(f"\n{'='*80}")
    print(f"📁 EXPLORING: {category_name.upper()}")
    print(f"{'='*80}\n")
    
    datasets = []
    
    for dataset_dir in sorted(category_path.iterdir()):
        if not dataset_dir.is_dir():
            continue
        
        dataset_id = dataset_dir.name
        csv_file = dataset_dir / f"{dataset_id}_full_data.csv"
        json_file = dataset_dir / f"{dataset_id}_full_data.json"
        metadata_file = dataset_dir / f"{dataset_id}_metadata.json"
        
        info = {
            "id": dataset_id,
            "has_csv": csv_file.exists(),
            "has_json": json_file.exists(),
            "has_metadata": metadata_file.exists(),
            "csv_size_mb": 0,
            "row_count": 0,
            "title": "Unknown"
        }
        
        if csv_file.exists():
            info["csv_size_mb"] = csv_file.stat().st_size / (1024 * 1024)
            try:
                df = pd.read_csv(csv_file)
                info["row_count"] = len(df)
                info["columns"] = list(df.columns)
            except Exception as e:
                info["error"] = str(e)
        
        if metadata_file.exists():
            try:
                with open(metadata_file) as f:
                    metadata = json.load(f)
                    info["title"] = metadata.get("Title", "Unknown")
                    info["description"] = metadata.get("Description", "")
            except:
                pass
        
        datasets.append(info)
    
    # Print summary
    print(f"Found {len(datasets)} datasets\n")
    
    for i, ds in enumerate(datasets, 1):
        status = "✅" if ds["has_csv"] and ds["has_json"] else "⚠️"
        print(f"{status} {i}. {ds['id']}")
        print(f"   Title: {ds['title'][:70]}")
        print(f"   Size:  {ds['csv_size_mb']:.2f} MB | Rows: {ds['row_count']:,}")
        
        if "error" in ds:
            print(f"   ⚠️  Error: {ds['error']}")
        
        print()
    
    return datasets

def show_dataset_preview(category_name, dataset_id, rows=10):
    """Show a preview of a specific dataset."""
    csv_file = Path(f"data/complete/{category_name}/{dataset_id}/{dataset_id}_full_data.csv")
    
    if not csv_file.exists():
        print(f"❌ Dataset not found: {dataset_id}")
        return
    
    print(f"\n{'='*80}")
    print(f"📄 DATASET PREVIEW: {dataset_id}")
    print(f"{'='*80}\n")
    
    # Load metadata
    metadata_file = csv_file.parent / f"{dataset_id}_metadata.json"
    if metadata_file.exists():
        with open(metadata_file) as f:
            metadata = json.load(f)
            print(f"Title: {metadata.get('Title', 'Unknown')}")
            print(f"Description: {metadata.get('Description', 'N/A')[:200]}")
            print()
    
    # Load and preview data
    df = pd.read_csv(csv_file)
    
    print(f"Shape: {df.shape[0]:,} rows × {df.shape[1]} columns")
    print(f"Size: {csv_file.stat().st_size / (1024*1024):.2f} MB")
    print()
    
    print("Columns:")
    for col in df.columns:
        dtype = df[col].dtype
        non_null = df[col].notna().sum()
        print(f"  - {col} ({dtype}) - {non_null:,}/{len(df):,} non-null")
    print()
    
    print(f"First {rows} rows:")
    print(df.head(rows).to_string())
    print()
    
    # Basic statistics
    print("Statistics:")
    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
    if len(numeric_cols) > 0:
        print(df[numeric_cols].describe().to_string())
    else:
        print("  No numeric columns found")
    print()

def find_datasets_by_keyword(keyword, category=None):
    """Search for datasets by keyword in titles/descriptions."""
    print(f"\n{'='*80}")
    print(f"🔍 SEARCHING FOR: '{keyword}'")
    if category:
        print(f"   In category: {category}")
    print(f"{'='*80}\n")
    
    base_path = Path("data/complete")
    categories_to_search = [category] if category else [d.name for d in base_path.iterdir() if d.is_dir()]
    
    results = []
    
    for cat in categories_to_search:
        cat_path = base_path / cat
        if not cat_path.exists():
            continue
        
        for dataset_dir in cat_path.iterdir():
            if not dataset_dir.is_dir():
                continue
            
            dataset_id = dataset_dir.name
            metadata_file = dataset_dir / f"{dataset_id}_metadata.json"
            
            if metadata_file.exists():
                with open(metadata_file) as f:
                    metadata = json.load(f)
                    title = metadata.get("Title", "").lower()
                    description = metadata.get("Description", "").lower()
                    
                    if keyword.lower() in title or keyword.lower() in description:
                        results.append({
                            "category": cat,
                            "id": dataset_id,
                            "title": metadata.get("Title", "Unknown"),
                            "description": metadata.get("Description", "")[:150]
                        })
    
    if results:
        print(f"Found {len(results)} matching datasets:\n")
        for i, result in enumerate(results, 1):
            print(f"{i}. [{result['category']}] {result['id']}")
            print(f"   {result['title']}")
            print(f"   {result['description']}...")
            print()
    else:
        print("No datasets found matching your search.")
    
    return results

def show_category_summary():
    """Show summary of all categories."""
    report = load_categorization_report()
    
    if not report:
        print("❌ No categorization report found. Run analyze_categories.py first.")
        return
    
    print(f"\n{'='*80}")
    print("📊 CBS DATASET CATEGORIZATION SUMMARY")
    print(f"{'='*80}\n")
    
    summary = report["summary"]
    print(f"Total Datasets: {summary['total_datasets']}")
    print(f"Total Files:    {summary['total_files']}")
    print(f"Total Size:     {summary['total_size_mb']:.2f} MB")
    print()
    
    categories = report["categories"]
    
    print("Categories:")
    for cat in sorted(categories.keys()):
        stats = categories[cat]
        pct = (stats['datasets'] / summary['total_datasets']) * 100
        bar = "█" * int(pct / 2)
        print(f"  {cat:15s} {stats['datasets']:3d} datasets {pct:5.1f}% {bar}")
    
    print()

def main():
    """Main interactive exploration tool."""
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "summary":
            show_category_summary()
        
        elif command == "category" and len(sys.argv) > 2:
            category = sys.argv[2]
            explore_category(category)
        
        elif command == "preview" and len(sys.argv) > 3:
            category = sys.argv[2]
            dataset_id = sys.argv[3]
            rows = int(sys.argv[4]) if len(sys.argv) > 4 else 10
            show_dataset_preview(category, dataset_id, rows)
        
        elif command == "search" and len(sys.argv) > 2:
            keyword = sys.argv[2]
            category = sys.argv[3] if len(sys.argv) > 3 else None
            find_datasets_by_keyword(keyword, category)
        
        else:
            print("❌ Unknown command or missing arguments")
            print_usage()
    else:
        print_usage()

def print_usage():
    """Print usage instructions."""
    print("\n" + "="*80)
    print("CBS DATASET EXPLORER")
    print("="*80 + "\n")
    print("Usage:")
    print("  python explore_categories.py summary")
    print("  python explore_categories.py category <name>")
    print("  python explore_categories.py preview <category> <dataset_id> [rows]")
    print("  python explore_categories.py search <keyword> [category]")
    print()
    print("Examples:")
    print("  python explore_categories.py summary")
    print("  python explore_categories.py category energie")
    print("  python explore_categories.py preview energie 83300ENG 20")
    print("  python explore_categories.py search solar hernieuwbaar")
    print("  python explore_categories.py search CO2")
    print()
    print("Available categories:")
    categories = sorted([d.name for d in Path("data/complete").iterdir() if d.is_dir() and not d.name.startswith('.')])
    for cat in categories:
        print(f"  - {cat}")
    print()

if __name__ == "__main__":
    main()
