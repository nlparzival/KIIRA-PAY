# EXTRA-DATA-SOURCES.md
## Gratis API's Voor Energie-Arbitrage (Naast TenneT)

---

## ☀️ WEER DATA (Essentieel!)

### 1. **KNMI Data API** ⭐⭐⭐⭐⭐
**Wat:** Nederlands weer, historisch + forecast
**Waarom cruciaal:**
- Zon → zonnepanelen → lage prijzen
- Wind → windmolens → lage prijzen
- Koude → hoog verbruik → hoge prijzen
- Regen/bewolking → minder zon → hogere prijzen

**API:** https://www.knmi.nl/kennis-en-datacentrum/achtergrond/data-ophalen-vanuit-een-script
**Rate limit:** Redelijk ruim (geen harde limiet)
**Gratis:** ✅ Volledig gratis

**Data:**
- Temperatuur (°C)
- Zonneschijn (uren/dag)
- Windsnelheid (m/s)
- Neerslag (mm)
- Bewolking (%)
- Luchtvochtigheid

**Use case:**
```python
# Als zon > 8 uur/dag:
if sunshine_hours > 8:
    # Veel solar productie verwacht
    # Prijzen gaan waarschijnlijk dalen middag
    strategy = "WAIT_TO_BUY"  # Koop in middag dip
```

**Download:**
```bash
# Historisch weer (dagelijks)
curl "https://www.daggegevens.knmi.nl/klimatologie/daggegevens" \
  -d "start=20250101" \
  -d "end=20251231" \
  -d "vars=TEMP:SQ:FH" > knmi_2025.txt
```

---

### 2. **Copernicus Climate Data** ⭐⭐⭐⭐
**Wat:** EU climate/weer data (satelliet)
**Waarom handig:**
- Solar irradiance (GHI - Global Horizontal Irradiance)
- Wind op verschillende hoogtes
- Europees netwerk (ook België, Duitsland relevant)

**API:** https://cds.climate.copernicus.eu/
**Gratis:** ✅ Account nodig maar gratis
**Rate limit:** Genereus

**Data:**
- Solar radiation (W/m²)
- Wind speed (10m, 100m hoogte)
- Temperature
- Cloud cover

**Use case:**
```python
# Als solar irradiance > 800 W/m²:
if ghi > 800:
    # Massive solar production
    # Prijzen crash middag 12-15u
    if hour in [12, 13, 14, 15]:
        action = "BUY_CHEAP"
```

---

### 3. **Open-Meteo** ⭐⭐⭐⭐⭐
**Wat:** Open-source weer API (beste gratis optie!)
**Waarom TOP:**
- Geen API key nodig!
- Geen rate limits (fair use)
- Forecast 16 dagen vooruit
- Historisch vanaf 1940

**API:** https://open-meteo.com/
**Gratis:** ✅✅✅ Volledig gratis, geen key, geen limits!
**Documentation:** https://open-meteo.com/en/docs

**Data:**
- Temperature, humidity, wind
- Solar radiation (GHI, DHI, DNI)
- Cloud cover
- Precipitation

**Example:**
```bash
# Forecast Amsterdam 7 dagen
curl "https://api.open-meteo.com/v1/forecast?latitude=52.37&longitude=4.89&hourly=temperature_2m,windspeed_10m,shortwave_radiation&timezone=Europe/Amsterdam"

# Historisch 2025
curl "https://archive-api.open-meteo.com/v1/archive?latitude=52.37&longitude=4.89&start_date=2025-01-01&end_date=2025-12-31&hourly=temperature_2m,windspeed_10m,shortwave_radiation"
```

**🔥 Recommended: Dit is de beste weer API!**

---

## ⚡ ENERGIE DATA

### 4. **ENTSO-E Transparency Platform** ⭐⭐⭐⭐⭐
**Wat:** Europese transmission data
**Waarom cruciaal:**
- **Day-ahead prijzen** (EPEX SPOT) - DE prijs!
- Cross-border flows (import/export)
- Generation per source (wind, solar, gas)
- Load forecasts

**API:** https://transparency.entsoe.eu/
**Gratis:** ✅ Account + API key gratis
**Rate limit:** Ruim (400 req/dag)

**Data:**
- Day-ahead prices (€/MWh) - **Essentieel!**
- Intraday prices
- Actual generation (wind, solar, gas, nuclear)
- Total load
- Cross-border flows (NL-DE, NL-BE, NL-UK)

**Use case:**
```python
# Compare day-ahead vs settlement (imbalance)
day_ahead_price = 0.20  # €/kWh
settlement_price = 0.35  # €/kWh (TenneT)

spread = settlement_price - day_ahead_price  # €0.15
if spread > 0.10:
    # Huge imbalance premium
    # Grid is stressed
    strategy = "CONSERVATIVE"
```

**Download:**
```python
import requests

api_key = "YOUR_ENTSOE_KEY"
url = "https://web-api.tp.entsoe.eu/api"
params = {
    "securityToken": api_key,
    "documentType": "A44",  # Day-ahead prices
    "in_Domain": "10YNL----------L",  # Netherlands
    "out_Domain": "10YNL----------L",
    "periodStart": "202501010000",
    "periodEnd": "202601010000"
}
response = requests.get(url, params=params)
```

**🔥 Dit is essentieel! Day-ahead prijzen zijn de baseline voor arbitrage.**

---

### 5. **CBS StatLine** ⭐⭐⭐
**Wat:** Centraal Bureau voor de Statistiek (NL data)
**Waarom handig:**
- Energieverbruik per sector
- Productie cijfers
- Economische indicatoren

**API:** https://opendata.cbs.nl/
**Gratis:** ✅ Volledig open data
**Rate limit:** Geen

**Data:**
- Elektriciteitsverbruik NL (totaal)
- Hernieuwbare energie productie
- Gas verbruik

**Use case:**
- Macro trends (verbruik stijgt/daalt)
- Seizoen patronen
- Niet real-time, maar goed voor long-term analyse

---

### 6. **RVO.nl Energie Data** ⭐⭐
**Wat:** Rijksdienst voor Ondernemend Nederland
**Data:**
- SDE++ subsidie registers (waar zitten zonneparken?)
- Warmtepomp/battery installaties
- Laadpaal locaties

**Website:** https://www.rvo.nl/onderwerpen/duurzaam-ondernemen/energie-en-milieu-innovaties/statistieken-en-publicaties

**Gratis:** ✅ Open data
**Format:** CSV downloads (niet echt API)

**Use case:**
- Weet waar veel solar/wind capacity zit
- Voorspel lokale overproductie

---

## 🌍 SATELLIET DATA

### 7. **NASA POWER API** ⭐⭐⭐⭐
**Wat:** NASA solar/weather data (satelliet)
**Waarom geweldig:**
- Global coverage
- Zeer accurate solar irradiance
- Historisch vanaf 1981!
- Gratis, geen key nodig

**API:** https://power.larc.nasa.gov/
**Gratis:** ✅ Volledig gratis
**Rate limit:** Redelijk (50 req/min)

**Data:**
- Solar irradiance (GHI, DNI, DHI)
- Temperature
- Wind speed
- Humidity

**Example:**
```bash
# Amsterdam solar data 2025
curl "https://power.larc.nasa.gov/api/temporal/daily/point?parameters=ALLSKY_SFC_SW_DWN&community=RE&longitude=4.89&latitude=52.37&start=20250101&end=20251231&format=JSON"
```

**Use case:**
```python
# NASA GHI (Global Horizontal Irradiance)
if ghi > 900:  # W/m²
    # Perfect solar day
    # Prijzen gaan kelderen 11-16u
```

---

### 8. **Copernicus Sentinel Satellite** ⭐⭐⭐
**Wat:** EU Earth observation satellites
**Data:**
- Cloud cover (real-time)
- Land temperature
- Atmospheric data

**API:** https://scihub.copernicus.eu/
**Gratis:** ✅ Account nodig
**Rate limit:** Fair use

**Use case:**
- Real-time cloud detection
- Als wolken boven NL → solar productie daalt → prijzen stijgen

---

## 💹 FINANCIEEL / COMMODITIES

### 9. **ECB Exchange Rates** ⭐⭐
**Wat:** European Central Bank wisselkoersen
**Relevantie:** Als je energie handelt met België/Duitsland

**API:** https://sdw.ecb.europa.eu/
**Gratis:** ✅

---

### 10. **EIA (US Energy Information)** ⭐⭐
**Wat:** Gas/oil prijzen (US maar global relevant)
**API:** https://www.eia.gov/opendata/
**Gratis:** ✅ API key gratis

**Use case:**
- Gas prijzen → gas power plants → energieprijzen

---

## 🚗 MOBILITEIT (Voor EV Arbitrage)

### 11. **Open Charge Map** ⭐⭐⭐
**Wat:** Global EV charging station database
**API:** https://openchargemap.org/
**Gratis:** ✅

**Data:**
- Laadpaal locaties
- Vermogen (kW)
- Beschikbaarheid

**Use case:**
- Waar zijn veel EV's? (hoge demand)
- Congestion prediction

---

### 12. **RDW Open Data** ⭐⭐⭐
**Wat:** Nederlandse voertuig registratie
**API:** https://opendata.rdw.nl/
**Gratis:** ✅ Volledig open

**Data:**
- Elektrische voertuigen per regio
- Laadpaal registratie
- Nieuwe EV verkoop

**Use case:**
- EV adoptie trend
- Waar veel EV's = hoge charging demand

---

## 📅 KALENDER / EVENTS

### 13. **Nederlandse Feestdagen API** ⭐⭐
**Wat:** Feestdagen, schoolvakanties
**Gratis:** ✅ 

**Use case:**
```python
if is_holiday or is_school_vacation:
    # Ander verbruikspatroon
    # Kantoren dicht → lager verbruik
    # Thuis meer verbruik → ander patroon
```

---

## 🏭 INDUSTRIE

### 14. **Port of Rotterdam API** ⭐⭐
**Wat:** Haven activiteit, scheepvaart
**API:** https://www.portofrotterdam.com/nl/data-en-digitalisering

**Use case:**
- Veel scheepvaart = veel industrieel verbruik
- Industrie = grote energy user

---

## 🎯 PRIORITEIT LIJST

### Must Have (Voor MVP):
1. ✅ **TenneT APIs** (settlement, balance, merit order, FRR) - Al gedaan!
2. ⭐⭐⭐⭐⭐ **Open-Meteo** - Beste weer API, geen key!
3. ⭐⭐⭐⭐⭐ **ENTSO-E** - Day-ahead prijzen (essentieel!)
4. ⭐⭐⭐⭐ **KNMI** - Nederlands weer (backup/compare)

### Nice to Have (Week 2):
5. ⭐⭐⭐⭐ **NASA POWER** - Solar irradiance
6. ⭐⭐⭐ **CBS StatLine** - Macro trends
7. ⭐⭐⭐ **RDW Open Data** - EV data

### Later (Advanced):
8. Copernicus Sentinel
9. Port of Rotterdam
10. ECB, EIA

---

## 🚀 ACTIE PLAN

### Deze Week (Naast TenneT):

**1. ENTSO-E Day-Ahead Prijzen** (essentieel!)
```bash
# Register: https://transparency.entsoe.eu/
# Get API key
# Download day-ahead prices 2025
```

**2. Open-Meteo Weer** (makkelijk!)
```bash
# Geen key nodig, direct:
curl "https://archive-api.open-meteo.com/v1/archive?latitude=52.37&longitude=4.89&start_date=2025-01-01&end_date=2025-12-31&hourly=temperature_2m,windspeed_10m,shortwave_radiation,cloudcover" > open_meteo_2025.json
```

**3. KNMI (optioneel backup)**
```bash
# Download daggegevens
curl "https://www.daggegevens.knmi.nl/klimatologie/daggegevens" \
  -d "start=20250101" \
  -d "end=20251231" \
  -d "vars=ALL" > knmi_2025.txt
```

---

## 📊 DATA PRIORITIES

### Absolute Must-Have:
1. **TenneT Settlement Prices** → Real-time prijzen
2. **ENTSO-E Day-Ahead** → Baseline prijzen
3. **Open-Meteo Weer** → Solar/wind production proxy

### High Value:
4. **TenneT Balance Delta** → Grid stress
5. **TenneT Merit Order** → Market depth
6. **KNMI** → NL specific weer

### Nice to Have:
7. **NASA POWER** → Accurate solar
8. **TenneT FRR/Metered** → Extra features
9. **CBS** → Macro trends

---

## 💡 WAAROM DEZE DATA WAARDEVOL IS

### Day-Ahead Prijzen (ENTSO-E)
```
Scenario: 
Day-ahead prijs: €0.20/kWh (gepland)
Settlement prijs: €0.40/kWh (actual imbalance)

Spread: €0.20 → HUGE arbitrage opportunity!
Als spread > €0.10: Grid is stressed, wees conservatief
```

### Weer Data (Open-Meteo)
```
Scenario:
Forecast: Zonnig, 900 W/m² solar irradiance
Action: Wacht tot middag (12-15u)
Prijzen dalen door solar flood
Laad battery/EV tijdens dip
```

### Wind Data
```
Scenario:
Windsnelheid > 12 m/s (veel wind)
→ Windmolens draaien op max
→ Overproductie 's nachts
→ Lage prijzen 22:00-06:00
Action: Nachtelijke arbitrage
```

---

## 🔥 QUICK START (2 Extra APIs Nu)

### 1. Open-Meteo (5 min, geen key!)
```bash
cd /Users/moesa/KIIRA-PAY/tennet-data/data

# Download 2025 weer data
curl "https://archive-api.open-meteo.com/v1/archive?latitude=52.37&longitude=4.89&start_date=2025-01-01&end_date=2025-12-31&hourly=temperature_2m,windspeed_10m,shortwave_radiation,cloudcover,precipitation&timezone=Europe/Amsterdam&format=csv" -o open_meteo_2025.csv
```

### 2. ENTSO-E Registratie (10 min)
```
1. https://transparency.entsoe.eu/usrm/user/createPublicUser
2. Registreer account
3. Email verificatie
4. Login → Settings → Generate API key
5. Copy key
```

Wacht op approval (zoals TenneT), daarna downloaden.

---

## ✅ SAMENVATTING

**Essentieel (naast TenneT):**
- ⭐⭐⭐⭐⭐ **ENTSO-E** (day-ahead prijzen)
- ⭐⭐⭐⭐⭐ **Open-Meteo** (weer, gratis, geen key!)

**Nice to have:**
- ⭐⭐⭐⭐ **KNMI** (NL weer backup)
- ⭐⭐⭐⭐ **NASA POWER** (solar irradiance)

**Total downloads:**
- TenneT: 6 APIs ✅ (in progress)
- Open-Meteo: 1 curl (done in 5 min!)
- ENTSO-E: 1 API (wacht op key)
- KNMI: 1 curl (5 min)

**Total: ~10 data sources, allemaal gratis!** 🎉

---

*Wil je dat ik nu de download scripts voor Open-Meteo en ENTSO-E maak?*
