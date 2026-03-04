# KIIRA-PAY Data Repository

**Central data storage for all KIIRA-PAY energy-related datasets**

This is the master data directory containing all datasets from various sources used by KIIRA-PAY for energy analysis, forecasting, and trading.

---

## 📁 Directory Structure

```
data/
├── cbs-data/              # Statistics Netherlands (CBS) - National statistics
├── tennet-data/           # TenneT - Dutch electricity grid operator
├── entso-e/               # ENTSO-E - European electricity data
├── eurostat/              # Eurostat - European statistics
├── ecb/                   # European Central Bank - Economic indicators
├── knmi/                  # Royal Netherlands Meteorological Institute
├── rijkswaterstaat/       # Dutch Ministry of Infrastructure
├── pdok/                  # Dutch Public Geospatial Data
├── rdw/                   # Dutch Vehicle Authority
├── cpb/                   # Netherlands Bureau for Economic Policy Analysis
├── iea/                   # International Energy Agency
├── irena/                 # International Renewable Energy Agency
├── nasa/                  # NASA - Satellite and climate data
├── pvgis/                 # Photovoltaic Geographical Information System
├── solcast/               # Solar irradiance forecasts
└── openweather/           # OpenWeather - Weather forecasts and historical
```

---

## 🎯 Data Source Overview

### 🇳🇱 Dutch National Sources

#### **CBS (Statistics Netherlands)**
- **Type:** Historical statistical data
- **Coverage:** ~807 datasets downloaded, all must-have & should-have present
- **Categories:** Energy, consumption, production, prices, emissions, CO2, renewables
- **Update:** Quarterly/Annual
- **Status:** ✅ Complete & validated
- **Size:** ~4 GB lokaal (waarvan ~1.6 GB in 16 grote bestanden die niet op GitHub staan)
- **⚠️ Let op:** 16 bestanden >50MB staan alleen lokaal, niet op GitHub. Zie `cbs-data/README.md` voor details en hoe je ze opnieuw kunt downloaden.

#### **TenneT**
- **Type:** Real-time and historical electricity grid data
- **Coverage:** Day-ahead prices, imbalance prices, capacity, flows
- **Update:** Real-time / 15-minute intervals
- **Status:** ✅ Active
- **API:** Available

#### **KNMI (Royal Netherlands Meteorological Institute)**
- **Type:** Weather data (temperature, wind, solar radiation, precipitation)
- **Coverage:** Historical (1900+) and forecasts
- **Update:** Hourly / Daily
- **Status:** 🔄 Planned
- **API:** Available

#### **Rijkswaterstaat**
- **Type:** Infrastructure and traffic data
- **Coverage:** Roads, waterways, energy impact
- **Update:** Real-time
- **Status:** 🔄 Planned
- **API:** Available

#### **PDOK (Public Geospatial Data)**
- **Type:** Geospatial datasets (buildings, infrastructure, land use)
- **Coverage:** Netherlands-wide GIS data
- **Update:** Quarterly
- **Status:** 🔄 Planned
- **API:** WMS/WFS services

#### **RDW (Vehicle Authority)**
- **Type:** Electric vehicle registrations, charging infrastructure
- **Coverage:** All registered vehicles in NL
- **Update:** Monthly
- **Status:** 🔄 Planned
- **API:** Open data portal

#### **CPB (Bureau for Economic Policy Analysis)**
- **Type:** Economic forecasts and analysis
- **Coverage:** GDP, inflation, energy economic indicators
- **Update:** Quarterly
- **Status:** 🔄 Planned
- **Access:** Publications and reports

---

### 🇪🇺 European Sources

#### **ENTSO-E**
- **Type:** European electricity transmission data
- **Coverage:** All European TSOs, cross-border flows, prices
- **Update:** Real-time / Hourly
- **Status:** 🔄 Planned
- **API:** Transparency Platform API

#### **Eurostat**
- **Type:** European statistical data
- **Coverage:** Energy, economy, population across EU
- **Update:** Monthly/Quarterly
- **Status:** 🔄 Planned
- **API:** Available

#### **ECB (European Central Bank)**
- **Type:** Economic and financial indicators
- **Coverage:** Interest rates, exchange rates, economic growth
- **Update:** Daily/Monthly
- **Status:** 🔄 Planned
- **API:** SDW (Statistical Data Warehouse)

---

### 🌍 International Sources

#### **IEA (International Energy Agency)**
- **Type:** Global energy statistics and analysis
- **Coverage:** Production, consumption, prices worldwide
- **Update:** Annual/Monthly
- **Status:** 🔄 Planned
- **Access:** Paid + some open data

#### **IRENA (International Renewable Energy Agency)**
- **Type:** Renewable energy statistics
- **Coverage:** Global renewable capacity, generation, costs
- **Update:** Annual
- **Status:** 🔄 Planned
- **Access:** Open data portal

#### **NASA**
- **Type:** Satellite data, climate, solar radiation
- **Coverage:** Global atmospheric and surface data
- **Update:** Varies (daily to annual)
- **Status:** 🔄 Planned
- **API:** Multiple APIs (POWER, EarthData)

---

### ☀️ Solar & Weather Specialized

#### **PVGIS**
- **Type:** Solar radiation and PV performance data
- **Coverage:** Europe and global
- **Update:** Historical + forecasts
- **Status:** 🔄 Planned
- **API:** JRC PVGIS API

#### **Solcast**
- **Type:** High-resolution solar irradiance forecasts
- **Coverage:** Global, 1-2km resolution
- **Update:** Real-time / 5-minute
- **Status:** 🔄 Planned
- **API:** Commercial API

#### **OpenWeather**
- **Type:** Weather forecasts and historical data
- **Coverage:** Global weather data
- **Update:** Real-time / Hourly
- **Status:** 🔄 Planned
- **API:** Free tier + paid

---

## 📊 Data Status Summary

| Source | Status | Datasets | Size | Priority |
|--------|--------|----------|------|----------|
| CBS | ✅ Complete | 730 | 907 MB | High |
| TenneT | ✅ Active | ~50 | ~200 MB | High |
| ENTSO-E | 🔄 Planned | TBD | TBD | High |
| KNMI | 🔄 Planned | TBD | TBD | High |
| Eurostat | 🔄 Planned | TBD | TBD | Medium |
| RDW | 🔄 Planned | TBD | TBD | Medium |
| IRENA | 🔄 Planned | TBD | TBD | Medium |
| PDOK | 🔄 Planned | TBD | TBD | Low |
| Rijkswaterstaat | 🔄 Planned | TBD | TBD | Low |
| CPB | 🔄 Planned | TBD | TBD | Low |
| IEA | 🔄 Planned | TBD | TBD | Low |
| ECB | 🔄 Planned | TBD | TBD | Low |
| NASA | 🔄 Planned | TBD | TBD | Low |
| PVGIS | 🔄 Planned | TBD | TBD | Low |
| Solcast | 🔄 Planned | TBD | TBD | Low |
| OpenWeather | 🔄 Planned | TBD | TBD | Low |

---

## 🚀 Usage

Each data source has its own directory with:
- `README.md` - Description, API info, usage instructions
- `scripts/` - Download and processing scripts
- `raw/` - Raw downloaded data
- `processed/` - Cleaned and processed data
- `metadata/` - Metadata and data dictionaries

### Example Usage

```python
# Load CBS energy data
from pathlib import Path
import pandas as pd

cbs_data = pd.read_csv('cbs-data/data/complete/energie/83300ENG/83300ENG_full_data.csv')

# Load TenneT prices
tennet_prices = pd.read_csv('tennet-data/data/day_ahead_prices.csv')

# Combine and analyze
combined = pd.merge(cbs_data, tennet_prices, on='date')
```

---

## 🔧 Maintenance

### Update Frequencies

- **Real-time:** TenneT, ENTSO-E, OpenWeather (automated)
- **Hourly/Daily:** KNMI, Rijkswaterstaat (automated)
- **Weekly:** RDW (automated)
- **Monthly:** Eurostat, IEA (automated)
- **Quarterly:** CBS, CPB (manual + automated)
- **Annual:** IRENA (manual)

### Scripts

```bash
# Update all data sources
./scripts/update_all_data.sh

# Update specific source
./scripts/update_cbs.sh
./scripts/update_tennet.sh
./scripts/update_knmi.sh
```

---

## 📈 Data Quality

- **Validation:** All data validated before use
- **Cleaning:** Automated cleaning pipelines
- **Versioning:** Time-stamped snapshots
- **Backup:** Regular backups to cloud storage
- **Documentation:** Comprehensive metadata for all datasets

---

## 🔐 Access & Licenses

### Open Data (Free)
- CBS, TenneT, KNMI, PDOK, RDW, Eurostat, IRENA, NASA POWER

### API Key Required (Free Tier)
- ENTSO-E, OpenWeather, PVGIS

### Paid/Licensed
- IEA (some datasets), Solcast (commercial), ECB (free but registration)

### Academic Access
- Some datasets available through academic licenses

---

## 🎯 Next Steps

1. ✅ CBS data - Complete (730 datasets, validated)
2. ✅ TenneT data - Active
3. 🔄 ENTSO-E - Set up API integration
4. 🔄 KNMI - Download historical weather data
5. 🔄 Eurostat - Identify and download key energy datasets
6. 🔄 RDW - Download EV and charging station data
7. 🔄 IRENA - Download renewable energy statistics

---

## 📞 Support

For data issues or questions:
- Check individual data source READMEs
- See scripts in each directory
- Consult original data source documentation

---

**Last Updated:** February 14, 2025  
**Maintainer:** KIIRA-PAY Team  
**Status:** 🚀 Active development
