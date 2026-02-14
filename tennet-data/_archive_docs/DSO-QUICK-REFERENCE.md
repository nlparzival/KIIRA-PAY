# DSO Data Quick Reference

## 📊 AVAILABLE NOW - Direct Download Links

### STEDIN (Rotterdam, Den Haag, Utrecht, Zeeland)
**18 years of data available (2009-2026)**

#### Most Recent (Priority 1) - ~200 MB
- ✅ 2026: Stedin main area
- ✅ 2025: Stedin + Zeeland separate files  
- ✅ 2024: Stedin + Zeeland separate files
- ✅ 2023: Stedin + Zeeland separate files
- ✅ 2022: Stedin main area

#### Historical Available
- 2019-2021 (ZIP format)
- 2015-2018 (ZIP format)  
- 2009-2014 (ZIP format, optional)

**Data includes:**
- Postcode-level consumption (electricity + gas)
- Number of connections per area
- Connection types (3x25, 3x50, etc.)
- Smart meter penetration %
- Standard Year Consumption (SJV)
- Solar panel back-feed data

---

### LIANDER (Amsterdam, Noord-NL, Gelderland, Friesland)
**10+ datasets identified**

#### Confirmed Available (Priority 1) - ~100 MB
- ✅ Kleinverbruik (small consumers) 2023
- ✅ Grootverbruik (large consumers) 2023
- ✅ Zonnepanelen (solar panels) 2023

#### Additional Datasets (via portal)
- Terugleverdata (back-feed to grid)
- Opwekdata (generation data)
- Transportprognoses (transport forecasts)
- Liggingsgegevens (infrastructure location)
- Verbruiksprofielen grootverbruik (large consumer profiles)
- STORM onderstation data
- 15-minute bedrijfsmetingen (quarter-hourly measurements)
- Slimme meter historical data (2012-2014)

---

### ENEXIS (Noord-Brabant, Limburg, Groningen)
**Status:** Open data portal exists, datasets to be inventoried
**Website:** https://www.enexis.nl/zakelijk/open-data

---

## 🚀 Quick Start Commands

### Download Most Recent Data Only (~300 MB)
```bash
cd /Users/moesa/KIIRA-PAY/tennet-data
python download_all_dso_data.py 1
```

### Download Recent + Historical (2019-2026) (~1 GB)
```bash
python download_all_dso_data.py 2
```

### Download All Available (2009-2026) (~3-5 GB)
```bash
python download_all_dso_data.py 4
```

---

## 📂 Where Data Will Be Saved

```
data/dso/
├── stedin/
│   ├── stedin_verbruik_2026.csv
│   ├── stedin_verbruik_2025.csv
│   ├── stedin_zeeland_verbruik_2025.csv
│   ├── stedin_verbruik_2024.csv
│   ├── stedin_zeeland_verbruik_2024.csv
│   └── ... (older years)
├── liander/
│   ├── liander_kleinverbruik_2023.csv
│   ├── liander_grootverbruik_2023.csv
│   └── liander_solar_2023.csv
└── enexis/
    └── (to be added)
```

---

## 📊 What You Can Analyze

### With Current CBS + Weather Data + DSO Data

1. **Regional Energy Consumption**
   - Compare Amsterdam (Liander) vs Rotterdam (Stedin)
   - Urban vs rural patterns
   - Industrial vs residential areas

2. **Weather Impact Analysis**
   - Temperature vs heating/cooling demand
   - Solar irradiance vs solar generation
   - Wind speed vs consumption patterns

3. **Energy Transition Tracking**
   - Solar panel growth 2009-2026
   - Smart meter rollout progress
   - Electricity vs gas consumption trends
   - Grid back-feed (net production) growth

4. **Temporal Patterns**
   - Seasonal variations
   - Year-over-year changes
   - Crisis impact (COVID-19, energy crisis 2022)

5. **Spatial Analysis**
   - Postcode-level consumption maps
   - High-demand areas identification
   - Grid congestion risk zones

---

## 🎯 Recommended Dashboard Visualizations

### Page 1: Overview
- Total consumption NL (CBS national)
- Regional breakdown (Stedin vs Liander)
- Time series 2009-2026

### Page 2: Weather Correlation
- Temperature vs consumption scatter
- Solar irradiance vs solar generation
- Seasonal heatmaps

### Page 3: Energy Transition
- Solar panel growth chart
- Smart meter adoption %
- Grid back-feed trends
- Electricity vs gas balance

### Page 4: Geographic
- Postcode consumption map
- Regional heatmaps
- Infrastructure overlay

### Page 5: Forecasting
- Trend extrapolation
- Seasonal decomposition
- Weather-adjusted predictions

---

## 🔄 Next Steps After Download

1. **Integrate into Dashboard**
   ```python
   # Add to dashboard.py
   - Load Stedin + Liander data
   - Join with weather data
   - Create regional comparisons
   - Add interactive maps
   ```

2. **Data Quality Check**
   ```python
   - Verify column names across years
   - Check for missing data
   - Validate aggregation levels
   - Compare overlapping regions
   ```

3. **Advanced Analysis**
   ```python
   - Correlation analysis (weather vs consumption)
   - Time series decomposition
   - Anomaly detection
   - Predictive modeling
   ```

4. **Optional: Get More Data**
   - Register for EDSN (real-time data)
   - Inventory Enexis datasets
   - Request specific data via Partners in Energie

---

## ⚠️ Important Notes

### Data Privacy
- All data is pre-aggregated (min 10 connections)
- No individual household data
- Postcode-level only
- Fully GDPR compliant

### Data Format
- **Separator:** Tab or semicolon (varies by year)
- **Encoding:** UTF-8 or UTF-8-BOM
- **Decimal:** Comma (,)
- **Date format:** YYYYMMDD or DD-MM-YYYY

### Known Issues
- Stedin: Pre-2013 data may be incomplete (before C-AR system)
- Liander: Some datasets require manual portal navigation
- Encoding varies between years (script handles this)

---

## 📞 Support & Questions

### Official Data Sources
- **Stedin:** https://www.stedin.net/zakelijk/open-data
- **Liander:** https://www.liander.nl/over-ons/open-data
- **EDSN:** https://www.edsn.nl/
- **CBS:** https://opendata.cbs.nl/

### Data Requests
- **Partners in Energie:** https://www.partnersinenergie.nl/
- **Response time:** 10 working days
- **Cost:** Usually free for research/analysis

---

**Status:** Ready for download ✅
**Last updated:** 2025-01-18
**Total available:** 25+ datasets, 18 years history
