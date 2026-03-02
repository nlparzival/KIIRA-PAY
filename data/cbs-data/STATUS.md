# CBS Open Data Integratie - Klaar Voor Dashboard

**Status:** ✅ Data gecatalogeerd, API client ready  
**Datum:** 14 februari 2026

## 📁 Essentiële Files

### Code
- **`cbs_api.py`** - Complete CBS Open Data API client
  - Alle API functies geïmplementeerd
  - Rate limiting & error handling
  - Ready voor productie gebruik

### Data
- **`all_cbs_datasets.json`** - Alle 1,904 CBS datasets met metadata
- **`cbs_datasets_categorized.json`** - Gefilterde datasets per categorie  
- **`cbs_prioritized_datasets.json`** - Must-have (189) & should-have (345) lists

### Documentatie
- **`README.md`** - Project overview en quick start
- **`CBS_COMPLETE_CATALOG.md`** - Complete catalog van alle 534 priority datasets

### Directories
- **`data/`** - Voor cached dataset results
- **`examples/`** - Voorbeeldcode voor API gebruik

## 🎯 Volgende Stappen

### 1. Validatie Uitvoeren (optioneel)

Als je wilt testen welke datasets werken:

```python
from cbs_api import CBSDataAPI

api = CBSDataAPI()

# Test een specifieke dataset
info = api.get_dataset_info('82610ENG')  # Hernieuwbare energie
data = api.get_dataset_data('82610ENG', max_rows=10)
print(f"Dataset: {info.get('Title')}")
print(f"Rows: {len(data)}")
```

### 2. Dashboard Integratie Starten

Pick de belangrijkste datasets uit `cbs_prioritized_datasets.json` (sorted by score):

**Top Priority (score 100+):**
- Hernieuwbare energie productie
- Elektriciteitsbalans  
- Energieprijzen CPI
- CO2 emissies
- Energieverbruik huishoudens

### 3. Implementatie Stappen

1. **Caching Layer**
   - Build `cbs_cache.py` voor dataset caching
   - Scheduled refresh (dagelijks/wekelijks)

2. **Data Transformation**
   - Parse CBS data naar dashboard format
   - Time series aggregatie
   - Unit conversies

3. **API Endpoints**
   - `/api/cbs/energy/renewable`
   - `/api/cbs/prices/electricity`
   - `/api/cbs/emissions/co2`
   - etc.

4. **Frontend Components**
   - Charts & visualizations
   - Historical trends
   - Comparison views

## 📊 Dataset Overview

**Totaal Beschikbaar:** 1,904 CBS datasets  
**Relevant voor energie:** 534 datasets  
**Must-have (score >=70):** 189 datasets  
**Should-have (score 40-69):** 345 datasets

**Categorieën:**
- Energie: ~45 must-have datasets
- Hernieuwbaar: ~25 must-have datasets  
- Prijzen: ~35 must-have datasets
- Verbruik: ~30 must-have datasets
- Productie: ~25 must-have datasets
- CO2: ~15 must-have datasets
- Economie: ~14 must-have datasets

## 🔧 CBS API Client Usage

### Basic Usage

```python
from cbs_api import CBSDataAPI

api = CBSDataAPI()

# Get dataset info
info = api.get_dataset_info('82610ENG')

# Get data
data = api.get_dataset_data('82610ENG')

# Get specific year
data_2024 = api.get_dataset_data('82610ENG', filters={'Perioden': '2024JJ00'})

# Get periods
periods = api.get_periods('82610ENG')
```

### Convenience Methods

```python
# Pre-configured methods voor belangrijke datasets
renewable = api.get_renewable_electricity(year=2024)
electricity = api.get_electricity_netherlands(year=2024)
emissions = api.get_co2_emissions(year=2024)
prices = api.get_energy_prices_cpi(start_year=2020)
```

### Batch Operations

```python
# Fetch multiple datasets at once
datasets = ['82610ENG', '85268NED', '70960NED']
results = api.get_multiple_datasets(datasets)

# Get all must-have datasets
all_data = api.get_all_must_haves(year=2024)
```

## 📝 Notes

- CBS API heeft geen officiële rate limits, maar we gebruiken conservatieve delays (0.5s)
- Datasets worden regelmatig bijgewerkt door CBS (check Modified date)
- Niet alle datasets hebben recentste jaar data (sommige lopen achter)
- English EN datasets zijn beschikbaar voor internationale gebruikers
- OData filters zijn beschikbaar voor advanced queries

## 🔗 Resources

- **CBS Open Data Portal:** https://opendata.cbs.nl/
- **OData API Docs:** https://www.cbs.nl/nl-nl/onze-diensten/open-data/databank-cbs-statline-als-open-data
- **Dataset Browser:** https://opendata.cbs.nl/dataportaal/

---

**Project:** KIIRA-PAY Energy Dashboard  
**Module:** CBS Open Data Integration  
**Last Updated:** 14 februari 2026
