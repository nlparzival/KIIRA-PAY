# CBS Open Data - Energy Datasets

This directory contains validated and categorized CBS (Statistics Netherlands) open data related to energy, with supporting economic and social datasets.

## 📁 Directory Structure

### `/complete/` - Main Dataset Repository (730 datasets)

Organized into 8 categories:

#### Energy & Environment (491 datasets)
- **`energie/`** (145 datasets, 139 MB) - Core energy statistics
- **`hernieuwbaar/`** (74 datasets, 76 MB) - Renewable energy
- **`verbruik/`** (161 datasets, 306 MB) - Energy consumption
- **`productie/`** (64 datasets, 167 MB) - Energy production
- **`co2/`** (47 datasets, 30 MB) - Emissions and climate

#### Economic & Social (239 datasets)
- **`prijzen/`** (97 datasets, 84 MB) - Energy prices and economics
- **`woningen/`** (38 datasets, 44 MB) - Residential energy and housing
- **`arbeid/`** (104 datasets, 62 MB) - Labor market and employment

### `/removed_health_datasets/` - Archived Non-Energy Data (40 datasets)

Datasets that were incorrectly categorized as energy-related. These contain health and social statistics and are kept separately for reference.

## 📊 Dataset Format

Each dataset is stored in its own directory with a standardized structure:

```
complete/<category>/<dataset_id>/
├── <dataset_id>_full_data.csv      # Main data table
├── <dataset_id>_full_data.json     # Metadata about the dataset
├── <dataset_id>_metadata.json      # Additional metadata (if available)
├── <dataset_id>_periods.json       # Time periods covered (if available)
└── <dataset_id>_dimensions.json    # Data dimensions (if available)
```

### Example
```
complete/energie/83300ENG/
├── 83300ENG_full_data.csv
├── 83300ENG_full_data.json
├── 83300ENG_metadata.json
└── 83300ENG_periods.json
```

## 🔍 Data Quality

- **Validated:** All datasets content-validated to ensure correct categorization
- **Cleaned:** 40 non-energy datasets removed and archived
- **Recategorized:** 287 datasets moved to correct categories
- **Complete:** 730 validated energy-related datasets
- **Size:** 907 MB total

## 🚀 Usage

### Explore Categories
```bash
# Show summary of all categories
python explore_categories.py summary

# Explore a specific category
python explore_categories.py category energie

# Preview a dataset
python explore_categories.py preview energie 83300ENG

# Search for datasets
python explore_categories.py search "solar"
```

### Load Data in Python
```python
import pandas as pd
from pathlib import Path

# Load a specific dataset
dataset_id = "83300ENG"
category = "energie"
data_path = Path(f"complete/{category}/{dataset_id}/{dataset_id}_full_data.csv")
df = pd.read_csv(data_path)

# Load metadata
import json
metadata_path = data_path.parent / f"{dataset_id}_full_data.json"
with open(metadata_path) as f:
    metadata = json.load(f)
```

### Bulk Loading
```python
from pathlib import Path
import pandas as pd

def load_category_datasets(category):
    """Load all datasets from a category."""
    category_path = Path(f"complete/{category}")
    datasets = {}
    
    for dataset_dir in category_path.iterdir():
        if not dataset_dir.is_dir():
            continue
        
        dataset_id = dataset_dir.name
        csv_file = dataset_dir / f"{dataset_id}_full_data.csv"
        
        if csv_file.exists():
            datasets[dataset_id] = pd.read_csv(csv_file)
    
    return datasets

# Load all energy datasets
energy_data = load_category_datasets("energie")
print(f"Loaded {len(energy_data)} energy datasets")
```

## 📈 Dataset Coverage

### Temporal Coverage
- **Historical:** 1990-present for most datasets
- **Frequency:** Annual, quarterly, monthly (varies by dataset)
- **Forecasts:** Available for some datasets

### Geographic Coverage
- **National:** Netherlands-wide statistics
- **Regional:** Province-level breakdowns
- **Local:** Municipality-level data (where available)
- **International:** Comparisons with EU and global data

### Sectoral Coverage
- Households and residential
- Industry and manufacturing
- Transport and mobility
- Agriculture and farming
- Services and commercial
- Public sector and government

## 🔧 Maintenance

### Scripts
- `analyze_categories.py` - Generate category summary statistics
- `explore_categories.py` - Interactive dataset exploration
- `validate_categories.py` - Content-based validation
- `cleanup_categories.py` - Recategorization and cleanup

### Reports
- `categorization_report.json` - Current state of all categories
- `validation_report.json` - Validation results and recommendations
- `cleanup_report.json` - Cleanup actions taken

## 📝 Data Dictionary

### Common Columns
- **ID** - Unique record identifier
- **Perioden** - Time period (year, quarter, month)
- **RegioS** - Geographic region
- Various measurement columns (specific to each dataset)

### Metadata Fields
- **Title** - Dataset title (Dutch/English)
- **Description** - Dataset description
- **Frequency** - Update frequency
- **Modified** - Last modification date
- **Source** - Data source (CBS)
- **License** - Open data license

## 🔗 Data Source

All data sourced from:
- **CBS Open Data Portal:** https://opendata.cbs.nl/
- **API Documentation:** https://www.cbs.nl/en-gb/our-services/open-data/cbs-open-data-api
- **License:** Open data, freely available for reuse

## ⚠️ Important Notes

1. **Updates:** CBS data is periodically updated. Run download scripts to get latest data.
2. **Validation:** Always validate data quality before use in production systems.
3. **Attribution:** When using CBS data, please cite the source appropriately.
4. **Missing Data:** Some datasets may have missing values or incomplete time series.
5. **Language:** Titles and metadata may be in Dutch or English (or both).

## 📞 Support

For questions about:
- **CBS Data:** Contact CBS via their website or API documentation
- **This Repository:** See main project documentation in `/cbs-data/README.md`
- **Data Issues:** Check validation reports or run validation scripts

---

**Last Updated:** February 14, 2025  
**Datasets:** 730 validated energy-related datasets  
**Total Size:** 907 MB  
**Status:** ✅ Cleaned, validated, and production-ready
