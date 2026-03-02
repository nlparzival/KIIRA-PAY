import os
import json
from pathlib import Path
from collections import defaultdict

data_dir = Path("data/complete")
categories = {}
stats = defaultdict(lambda: {"datasets": 0, "files": 0, "csv": 0, "json": 0, "parquet": 0, "size_mb": 0})

for category_dir in data_dir.iterdir():
    if not category_dir.is_dir() or category_dir.name.startswith('.'):
        continue
    
    category = category_dir.name
    dataset_ids = set()
    
    for item in category_dir.iterdir():
        if item.is_dir():
            dataset_ids.add(item.name)
            
            for file in item.iterdir():
                if file.is_file():
                    stats[category]["files"] += 1
                    
                    if file.suffix == '.csv':
                        stats[category]["csv"] += 1
                    elif file.suffix == '.json':
                        stats[category]["json"] += 1
                    elif file.suffix == '.parquet':
                        stats[category]["parquet"] += 1
                    
                    try:
                        stats[category]["size_mb"] += file.stat().st_size / (1024 * 1024)
                    except:
                        pass
    
    stats[category]["datasets"] = len(dataset_ids)

# Print results
print("\n" + "="*80)
print("CBS DATASET CATEGORIZATION SUMMARY")
print("="*80)

total_datasets = 0
total_files = 0
total_size = 0

for category in sorted(stats.keys()):
    s = stats[category]
    total_datasets += s["datasets"]
    total_files += s["files"]
    total_size += s["size_mb"]
    
    print(f"\n📁 {category.upper()}")
    print(f"   Datasets: {s['datasets']}")
    print(f"   Files:    {s['files']} (CSV: {s['csv']}, JSON: {s['json']}, Parquet: {s['parquet']})")
    print(f"   Size:     {s['size_mb']:.2f} MB")

print("\n" + "="*80)
print(f"TOTAL: {total_datasets} datasets | {total_files} files | {total_size:.2f} MB")
print("="*80 + "\n")

# Save detailed report
report = {
    "summary": {
        "total_datasets": total_datasets,
        "total_files": total_files,
        "total_size_mb": round(total_size, 2)
    },
    "categories": {cat: dict(stats[cat]) for cat in stats}
}

with open("data/complete/categorization_report.json", "w") as f:
    json.dump(report, f, indent=2)

print("✅ Report saved to: data/complete/categorization_report.json")
