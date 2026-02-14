# Energy Data Collector
## Download alle data voor energie-arbitrage AI

Python scripts om alle benodigde data te downloaden:
- TenneT APIs (6 endpoints)
- ENTSO-E Day-Ahead Prices
- Open-Meteo weather data
- NASA POWER solar/weather data
- KNMI NL weather data

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Setup API Keys
```bash
cp .env.example .env
# Edit .env en voeg je API keys toe:
# - TENNET_API_KEY=... (zodra je hem krijgt)
# - ENTSOE_API_TOKEN=... (zodra je hem krijgt)
```

### 3. Download Data

#### Weather Data (No API Key Needed) ✅
```bash
# Open-Meteo (hourly weather)
python download_data.py --source open-meteo --year 2025

# NASA POWER (daily solar/weather)
python download_data.py --source nasa --year 2025

# KNMI (NL weather, all stations)
python download_data.py --source knmi --year 2025
```

#### TenneT Data (Requires API Key) ⏳
```bash
# Test connection first
python test_api.py

# Download all TenneT APIs
python download_data.py --year 2025
```

#### ENTSO-E Prices (Requires API Token) ⏳
```bash
# Test connection first
python test_entsoe_api.py

# Download day-ahead prices
python download_entsoe_prices.py --year 2025
```

## 📊 Data Sources

## 📊 Data Sources

### ✅ Already Working (No API Key):
1. **Open-Meteo** - Hourly weather data (temp, wind, solar, clouds, rain)
2. **NASA POWER** - Daily solar/weather data (11 parameters)
3. **KNMI** - NL weather stations (all variables)

### ⏳ Requires API Key (Approval Pending):

#### TenneT APIs (6 endpoints):
1. **Settlement Prices** - Imbalance prijzen (15 min intervals)
2. **Balance Delta** - Grid status (overschot/tekort)
3. **Merit Order List** - Bid prijzen en volumes
4. **FRR Activations** - Emergency reserve activaties
5. **Metered Injections** - Totaal NL verbruik
6. **Reconciliation Prices** - Gewogen marktprijzen

#### ENTSO-E API:
1. **Day-Ahead Prices** - Elektriciteit prijzen (hourly, EUR/MWh)

## 📁 Output Files

```
data/
├── open_meteo_2025.csv              ✅ (335 KB, hourly)
├── nasa_power_full_2025.json        ✅ (67 KB, daily)
├── knmi_2025.txt                    ✅ (7.8 MB, daily)
├── settlement_prices_2025.csv       ⏳ TenneT
├── balance_delta_2025.csv           ⏳ TenneT
├── merit_order_2025.csv             ⏳ TenneT
├── frr_activations_2025.csv         ⏳ TenneT
├── metered_injections_2025.csv      ⏳ TenneT
├── reconciliation_prices_2025.csv   ⏳ TenneT
└── entsoe_dayahead_2025.csv         ⏳ ENTSO-E
```

**Current: 8.2 MB | Expected Total: ~35-70 MB**

## ⚡ Rate Limits & Best Practices

### TenneT APIs
Script respecteert automatisch alle rate limits:
- Settlement Prices: 25/dag (gebruik bulk download)
- Balance Delta: 3000/dag
- Merit Order: 600/dag
- FRR: 1500/dag
- Metered Injections: 25/dag
- Reconciliation: 300/dag

### ENTSO-E API
- Geen officiële rate limit gedocumenteerd
- Script gebruikt 1 sec delay tussen requests (veilig)
- Downloads per maand om response size te beperken

## 📖 Documentation

### API Guides:
- **TenneT**: See `TENNET-API-COMPLETE.md` in `/technisch/`
- **ENTSO-E**: See `ENTSOE-API-GUIDE.md` (troubleshooting included!)
- **Extra Sources**: See `EXTRA-DATA-SOURCES.md` in `/technisch/`

### Setup Guides:
- **Full Project**: See `START-HIER.md`
- **API Setup**: See `SETUP.md`
- **Current Status**: See `STATUS.md`

## 🆘 Troubleshooting

### ENTSO-E: Kan API Token Niet Vinden?
```bash
# Lees de uitgebreide troubleshooting guide:
cat ENTSOE-API-GUIDE.md

# Key points:
# 1. Account moet eerst goedgekeurd worden (1-3 dagen)
# 2. Check email voor approval notification
# 3. Zoek "Web API" tab in Account Settings
# 4. Als je het niet vindt: manual download mogelijk via dashboard
```

### TenneT: API Key Nog Niet Ontvangen?
```bash
# Check email dagelijks (1-2 werkdagen verwacht)
# Controleer spam folder
# Account status: https://www.tennet.org/
```

### Python Dependencies Issues?
```bash
# Gebruik asdf voor versie management:
asdf install python 3.11.0
asdf local python 3.11.0
pip install -r requirements.txt
```

## 🚀 Next Steps

1. **Wait for API approvals** (check email daily)
2. **Start data exploration** with current weather data
3. **Build simulator** with mock price data
4. **Integrate real prices** when TenneT/ENTSO-E keys arrive
5. **Train agents** on complete historical dataset
