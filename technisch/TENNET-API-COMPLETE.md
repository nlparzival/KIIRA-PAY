# TENNET-API-COMPLETE.md
## Volledige TenneT API Analyse voor Energie-Arbitrage Simulatie

---

## 🎯 WELKE API'S HEBBEN WE NODIG?

### ✅ ESSENTIEEL (Voor Simulatie & Productie)

#### 1. **Settlement Prices** (Imbalance Prijzen)
**Endpoint:** `GET /publications/v1/settlement-prices`

**Wat is het?**
- **Imbalance prijzen per 15-minuten interval (PTU)**
- Dit is DE prijs waarop je energy kunt kopen/verkopen op de onbalans markt
- **DIT IS DE BELANGRIJKSTE API** voor arbitrage!

**Rate Limits:**
- Production: 1 req/sec, 5 req/min, **25 req/dag** ⚠️
- Acceptance: 1 req/sec, 60 req/min, 300 req/dag

**Gebruik voor simulatie:**
- Download historische data (max 25x per dag)
- Formaat: JSON, CSV, XML
- Timestamps: UTC of Local

**Code voorbeeld:**
```python
import requests

api_key = "YOUR_API_KEY"
headers = {"x-api-key": api_key}

# Haal 1 dag settlement prices op
url = "https://api.tennet.eu/publications/v1/settlement-prices"
params = {
    "from": "2025-06-01T00:00:00Z",
    "to": "2025-06-02T00:00:00Z",
    "format": "json"
}

response = requests.get(url, headers=headers, params=params)
data = response.json()

# Data structuur:
# {
#   "timestamp": "2025-06-01T14:00:00Z",
#   "price_eur_mwh": 85.50,  # €/MWh
#   "price_eur_kwh": 0.0855  # €/kWh (zelf berekenen)
# }
```

**Waarom essentieel:**
> Dit is de prijs waarop je real-time energie koopt/verkoopt als prosumer!

---

#### 2. **Balance Delta** (Grid Balancing Status)
**Endpoint:** `GET /publications/v1/balance-delta`

**Wat is het?**
- Verschil tussen vraag en aanbod op het grid (MW)
- Positief = overschot (lage prijzen waarschijnlijk)
- Negatief = tekort (hoge prijzen waarschijnlijk)
- **Voorspeller voor price swings**

**Rate Limits:**
- Production: 1 req/sec, 24 req/min, **3000 req/dag** ✅ (Ruim!)
- Acceptance: 1 req/sec, 60 req/min, 3000 req/dag

**Gebruik voor simulatie:**
- Feature voor ML model (correlatie met prijzen)
- Helpt voorspellen price spikes

**Code voorbeeld:**
```python
url = "https://api.tennet.eu/publications/v1/balance-delta"
params = {
    "from": "2025-06-01T00:00:00Z",
    "to": "2025-06-02T00:00:00Z"
}

response = requests.get(url, headers=headers, params=params)
data = response.json()

# Data: {"timestamp": "...", "balance_delta_mw": -250}
# Negatief = tekort → prijzen stijgen waarschijnlijk
```

---

#### 3. **Balance Delta High-Res** (Real-time Grid Status)
**Endpoint:** `GET /publications/v1/balance-delta-high-res/latest`

**Wat is het?**
- **5-secondes resolutie** (super high-frequency!)
- Laatste 30 minuten data
- **Voor real-time trading** (niet simulatie)

**Rate Limits:**
- Production: 1 req/sec, 10 req/min, **8 req/dag** (voor historical) ⚠️
- Voor `/latest`: 5x per minuut toegestaan (bij 12th second: 00:00:13, 00:00:25, etc.)

**Gebruik:**
- **NIET voor simulatie** (te veel data, rate limits te laag)
- **WEL voor productie** (Pi 5 real-time monitoring)

**Strategie:**
```python
# Productie: Poll /latest elke 12 seconden
import time

while True:
    response = requests.get(
        "https://api.tennet.eu/publications/v1/balance-delta-high-res/latest",
        headers=headers
    )
    data = response.json()
    # Returns: laatste 30 min @ 5-sec resolutie
    
    time.sleep(12)  # Wait for next data refresh
```

---

#### 4. **Reconciliation Prices** (Day-Ahead/Market Prijzen)
**Endpoint:** `GET /publications/v1/reconciliation-prices`

**Wat is het?**
- Gewogen marktprijs voor afrekening over langere periode
- Minder volatiel dan settlement prices
- **Benchmark prijs** (vergelijk met imbalance)

**Rate Limits:**
- 1 req/sec, 60 req/min, **300 req/dag** ✅

**Gebruik:**
- Baseline prijs voor arbitrage berekening
- Als imbalance > reconciliation + €0.05: SELL
- Als imbalance < reconciliation - €0.05: BUY

---

### 🔧 HANDIG (Advanced Features)

#### 5. **Merit Order List** (Bid Prijzen aFRR/mFRR)
**Endpoint:** `GET /publications/v1/merit-order-list`

**Wat is het?**
- Bids van balancing providers (prijzen + volumes)
- Shows market depth (hoeveel capaciteit beschikbaar per prijs)
- **Voor advanced strategies** (market making)

**Rate Limits:**
- Production: 1 req/sec, 10 req/min, **600 req/dag** ✅

**Gebruik:**
- Voorspel price direction (veel lage bids = prijzen dalen)
- Niet essentieel voor MVP

---

#### 6. **Frequency Restoration Reserve Activations** (FRR)
**Endpoint:** `GET /publications/v1/frequency-restoration-reserve-activations`

**Wat is het?**
- Volumes van geactiveerde balancing energie
- Emergency reserves
- **Indicator voor grid stress**

**Rate Limits:**
- 1 req/sec, 60 req/min, **1500 req/dag** ✅ (Veel!)

**Gebruik:**
- Feature voor ML model
- High activations = grid stress = prijzen volatiel

---

#### 7. **Metered Injections** (Load/Consumption Data)
**Endpoint:** `GET /publications/v1/metered-injections`

**Wat is het?**
- Totale load (verbruik) zichtbaar door transmission netwerk
- Feed in - exports + imports
- **Macro-level demand data**

**Rate Limits:**
- Production: 1 req/sec, 5 req/min, **25 req/dag** ⚠️

**Gebruik:**
- Feature voor demand forecasting
- Niet essentieel voor MVP

---

#### 8. **Settled Imbalance Volumes**
**Endpoint:** `GET /publications/v1/settled-imbalance-volumes`

**Wat is het?**
- Volumes settled door TenneT met programme-responsible parties
- **Historische afrekening data**

**Rate Limits:**
- Production: 1 req/sec, 5 req/min, **25 req/dag** ⚠️

**Gebruik:**
- Voor analyse/research
- Niet real-time bruikbaar

---

#### 9. **Reconciliation Control Data**
**Endpoint:** `GET /publications/v1/reconciliation-control-data`

**Wat is het?**
- Raw data om reconciliation prices zelf te berekenen
- **Voor nerds** 🤓

**Rate Limits:**
- 1 req/sec, 12 req/min, **1500 req/dag** ✅

**Gebruik:**
- Advanced: Build eigen pricing model
- Overkill voor MVP

---

## 📊 PRIORITEIT VOOR SIMULATIE (UPDATED!)

### MVP Simulatie (Week 1-2)

#### ⭐⭐⭐⭐⭐ CRITICAL (Must Have):
1. **Settlement Prices**
   - DE arbitrage prijs
   - Download 1 jaar historische data (bulk download)
   - Formaat: CSV (makkelijkst)
   - **Waarom:** Dit is letterlijk de prijs waarop je handelt

2. **Balance Delta**
   - Grid status (overschot/tekort)
   - 3000/dag = genoeg voor 1 jaar data in 1 dag
   - **Waarom:** Correlatie met prijzen (tekort = duur, overschot = goedkoop)

#### ⭐⭐⭐⭐ HIGH VALUE (Should Have):
3. **Merit Order List** 🔥
   - Bid prijzen + volumes van balancing providers
   - 600/dag = ruim genoeg
   - **Waarom je dit WEL wilt:**
     - **Market depth insight:** Zie hoeveel capaciteit beschikbaar is per prijsniveau
     - **Price prediction:** Als er veel lage bids zijn, prijzen gaan waarschijnlijk dalen
     - **Supply curve:** Je ziet de complete supply curve van de markt
     - **Early warning:** Weinig bids = grid stress = prijzen stijgen
   - **Use case in agent:**
     ```python
     # Als merit order weinig volume heeft < €100/MWh:
     if merit_order_volume_below_100 < 500_MW:
         # Grid is tight, prijzen gaan stijgen
         strategy = "CONSERVATIVE"  # Verkoop niet te vroeg
     else:
         # Veel capaciteit, prijzen blijven stabiel
         strategy = "AGGRESSIVE"  # Handel vrijelijk
     ```

4. **Frequency Restoration Reserve Activations (FRR)** 🔥
   - Volumes van geactiveerde balancing energie
   - 1500/dag = veel!
   - **Waarom je dit WEL wilt:**
     - **Grid stress indicator:** Hoge activaties = grid in problemen = prijzen volatiel
     - **Emergency reserves:** Als emergency energy wordt gebruikt = extreme situatie
     - **Pattern recognition:** FRR activaties voorspellen settlement price spikes
   - **Use case in agent:**
     ```python
     # Als FRR activations > 1000 MW:
     if frr_activated_volume > 1000:
         # Grid is in stress mode
         # Settlement prijzen gaan waarschijnlijk spiken
         action = "HOLD"  # Wacht op hogere prijzen om te verkopen
         risk_multiplier = 2.0  # Verhoog risk buffer
     ```

5. **Metered Injections** 🔥
   - Totale load (consumption) door transmission netwerk
   - 25/dag = beetje krap maar haalbaar
   - **Waarom je dit WEL wilt (je had gelijk!):**
     - **Demand forecasting:** Zie macro-level consumption patterns
     - **Correlation met prijzen:** Hoog verbruik = hoge prijzen
     - **Time-of-day patterns:** Industrieel verbruik vs huishoudelijk
     - **Weather correlation:** Check of veel verbruik = weinig zon (correlatie)
   - **Use case in agent:**
     ```python
     # Als metered injections > 12 GW (hoog verbruik):
     if metered_load > 12_000:  # MW
         # Hoog verbruik = meestal hogere prijzen
         if battery_soc > 80%:
             action = "SELL"  # Profit van hoge demand
     ```

#### ⭐⭐⭐ MEDIUM VALUE (Nice to Have):
6. **Reconciliation Prices**
   - Benchmark/baseline prijs
   - 300/dag = genoeg
   - **Waarom:** Compare settlement vs baseline (arbitrage spread)

7. **Settled Imbalance Volumes**
   - Volumes settled door TenneT met parties
   - 25/dag = krap
   - **Waarom toch handig:**
     - **Market participation:** Zie hoe actief de markt is
     - **Imbalance patterns:** Zijn programma's structureel kort/lang?
     - **Crowdedness indicator:** Veel imbalance = veel arbitrage players
   - **Use case:**
     ```python
     # Als imbalance volumes structureel hoog:
     if avg_imbalance_volume > 500_MW:
         # Markt is actief, veel trading
         # Spreads zijn waarschijnlijk smaller
         min_profit_threshold = 0.08  # Verhoog threshold
     ```

#### ⭐⭐ LOW PRIORITY (Later):
8. **Reconciliation Control Data**
   - Raw data om reconciliation prices te berekenen
   - 1500/dag = genoeg
   - **Waarom low priority:** Overkill, reconciliation prices zijn al beschikbaar

9. **Balance Delta High-Res**
   - 5-seconde resolutie
   - 8/dag voor historical (te weinig)
   - **Waarom low priority:** Voor simulatie te granular, wel voor productie

---

## 🎯 AANBEVOLEN API STACK

### Voor Simulatie (Week 1-4):

**Download Priority:**
1. ✅ Settlement Prices (bulk download)
2. ✅ Balance Delta (52 calls voor 1 jaar)
3. ✅ Merit Order List (52 calls) 🆕
4. ✅ FRR Activations (52 calls) 🆕
5. ✅ Metered Injections (365 calls = 15 dagen) 🆕
6. ✅ Reconciliation Prices (12 calls)
7. ⚠️ Settled Imbalance Volumes (365 calls = 15 dagen, optioneel)

**Total API calls:**
- Week sampling (52 calls × 4 APIs) = 208 calls
- Daily sampling voor Metered Injections = 365 calls
- **Totaal: ~600 calls = 2-3 dagen spreiden**

**Rate limit strategie:**
```python
# Dag 1: Settlement (bulk) + Balance Delta (52) + Merit Order (52)
# Dag 2: FRR Activations (52) + Reconciliation (12)
# Dag 3-17: Metered Injections (25/dag × 15 dagen)
# OF: Metered Injections per week (52 calls) voor lagere resolutie
```

---

## 🧠 WAAROM DEZE API's ZO WAARDEVOL ZIJN

### Merit Order List = Market Microstructure 📊
**Denk aan een order book bij crypto/stocks:**
```
Bid Price (€/MWh) | Volume (MW)
----------------------------------
50                | 200
75                | 500
100               | 800  ← Veel volume hier!
125               | 300
150               | 100  ← Weinig volume, tight market
```

**Als agent dit ziet:**
- Veel volume @ €100 = prijzen blijven rond €100 (stable)
- Weinig volume @ €150 = als demand stijgt, price spike naar €150+
- **Predictive power!**

**Feature voor ML model:**
```python
features = {
    'settlement_price': 0.085,
    'balance_delta': -250,
    'merit_order_volume_50_100': 1500,  # MW beschikbaar €50-100
    'merit_order_volume_100_150': 400,  # MW beschikbaar €100-150
    'merit_order_volume_150_plus': 50,  # MW beschikbaar >€150
}

# Als volume_150_plus laag is:
if features['merit_order_volume_150_plus'] < 100:
    prediction = "HIGH_RISK_OF_SPIKE"
```

---

### FRR Activations = Grid Stress Sensor 🚨
**Frequency Restoration Reserve wordt geactiveerd als:**
- Grid frequency < 49.9 Hz of > 50.1 Hz (emergency)
- Normale balancing niet genoeg is
- **This is the canary in the coal mine!**

**Correlation met prijzen:**
```
FRR Activated > 500 MW → Settlement prices vaak >€0.40/kWh
FRR Activated > 1000 MW → Settlement prices soms >€0.80/kWh
FRR Activated = 0 MW → Prijzen stabiel, normale range
```

**Use in agent:**
```python
def risk_assessment(frr_activated):
    if frr_activated > 1000:
        return "EXTREME_VOLATILITY"  # Don't trade, too risky
    elif frr_activated > 500:
        return "HIGH_VOLATILITY"  # Increase margins
    elif frr_activated > 100:
        return "MODERATE"  # Normal trading
    else:
        return "STABLE"  # Aggressive trading OK
```

---

### Metered Injections = Demand Signal 📈
**Dit is de macro verbruiksmeter van heel Nederland:**
```
Typical patterns:
- Night (00:00-06:00): 8-10 GW
- Morning peak (07:00-09:00): 12-14 GW
- Midday (10:00-15:00): 11-13 GW
- Evening peak (18:00-21:00): 13-15 GW (highest!)
```

**Correlation met prijzen:**
```
Metered Load > 14 GW → Prijzen gemiddeld €0.28/kWh
Metered Load < 10 GW → Prijzen gemiddeld €0.18/kWh
```

**Why this matters:**
- **Forecast demand:** Als load stijgt, prijzen gaan stijgen
- **Anomaly detection:** Load veel hoger dan normaal = event (cold snap)
- **Solar correlation:** Hoge load + weinig zon = dure stroom

**Use in agent:**
```python
def demand_adjusted_strategy(metered_load, hour):
    # Expected load voor dit uur
    expected_load = load_profile[hour]  # Historical average
    
    # Actual vs expected
    delta = metered_load - expected_load
    
    if delta > 1000:  # 1 GW hoger dan normaal
        # Abnormaal hoog verbruik
        # Prijzen gaan stijgen
        strategy = "SELL_BIAS"  # Verkoop battery power
    elif delta < -1000:
        # Abnormaal laag verbruik (veel zon, warm weer)
        # Prijzen gaan dalen
        strategy = "BUY_BIAS"  # Laad battery
    else:
        strategy = "NEUTRAL"
    
    return strategy
```

---

## 🔥 ADVANCED FEATURE ENGINEERING

### Combine All APIs = Super Features

```python
# Feature set voor ML model
features = {
    # Price (target)
    'settlement_price': 0.085,
    
    # Grid status
    'balance_delta': -250,  # MW (negatief = tekort)
    
    # Market depth
    'merit_order_total_volume': 2500,  # MW
    'merit_order_avg_price': 95,  # €/MWh
    'merit_order_price_spread': 120,  # Max - min
    
    # Grid stress
    'frr_activated_volume': 150,  # MW
    'frr_activated_last_hour': 300,  # Trend
    
    # Demand
    'metered_load': 12_500,  # MW
    'metered_load_vs_expected': +800,  # Delta vs historical avg
    
    # Time features
    'hour': 14,
    'day_of_week': 2,  # Tuesday
    'is_weekend': False,
    
    # Derived features
    'price_momentum': +0.015,  # Price change vs 1h ago
    'volatility_1h': 0.045,  # Std of prices last hour
}

# ML model uses ALL of this to predict:
predicted_price_next_hour = model.predict(features)
```

---

## 📊 DATA DOWNLOAD STRATEGIE (UPDATED)

### Optie 1: Weekly Sampling (Fast, 3 dagen)
```python
# Voor alle APIs: 1x per week downloaden
# Pro: Snel, rate limits geen probleem
# Con: Lagere resolutie (52 datapoints/jaar)

date_range = pd.date_range('2025-01-01', '2026-01-01', freq='7D')
# = 52 weeks

for each_api in [settlement, balance_delta, merit_order, frr, reconciliation]:
    download_weekly(api, date_range)  # 52 calls

# Metered Injections: weekly OK (macro trend)
download_weekly(metered_injections, date_range)  # 52 calls

# Total: 52 × 6 = 312 calls = 2-3 dagen
```

### Optie 2: Daily Sampling (Better, 15 dagen)
```python
# Voor kritische APIs: daily
# Pro: Hoge resolutie, betere training data
# Con: Meer API calls, langzamer

# Settlement: bulk download (geen limiet)
# Balance Delta: daily (3000/dag = OK)
# Merit Order: daily (600/dag = OK)
# FRR: daily (1500/dag = OK)
# Metered Injections: daily (25/dag = 15 dagen nodig)
# Reconciliation: daily (300/dag = OK)

# Dag 1-10: Metered Injections (25×10 = 250 dagen)
# Dag 11-15: Metered Injections (25×5 = 125 dagen) → Total 365
# Parallel: Balance Delta, Merit Order, FRR, Reconciliation

# Total: 15 dagen voor complete dataset
```

### Optie 3: Hybrid (Recommended, 5 dagen)
```python
# Critical APIs: daily
settlement_prices = bulk_download()  # 1x
balance_delta = download_daily('2025-01-01', '2026-01-01')  # 3000/dag OK

# High value APIs: daily BUT split over dagen
# Dag 1: Merit Order (365 calls, past binnen 600 limit)
# Dag 2-15: Metered Injections (25/dag)
# Dag 1: FRR (365 calls, past binnen 1500 limit)
# Dag 1: Reconciliation (365 calls, past binnen 300... WAIT!)

# Fix voor Reconciliation (300/dag limiet):
# Dag 1: Reconciliation (300 dagen)
# Dag 2: Reconciliation (65 dagen)

# Total: ~5 dagen voor complete dataset @ daily resolution
```

---

## 🎯 AANBEVOLEN AANPAK

### Week 1: Core Data
```bash
Dag 1: Setup
- Registreer TenneT developer account
- Get API key
- Test 1 API call

Dag 2: Bulk + Fast APIs
- Settlement Prices (bulk download)
- Balance Delta (365 calls via script)
- FRR Activations (365 calls via script)
- Merit Order List (365 calls via script)

Dag 3-4: Slow APIs (rate limited)
- Reconciliation Prices (365 calls, 2 dagen)

Dag 5-20: Metered Injections
- 25 calls/dag × 15 dagen = 365 dagen data
- OF: Weekly (52 calls) voor sneller resultaat
```

### Week 2: Data Processing
```bash
Dag 1: Merge datasets
- Align timestamps (UTC)
- Resample naar 15-min intervals
- Handle missing values

Dag 2: Feature engineering
- Price momentum, volatility
- Merit order features (volume bands)
- FRR stress indicators
- Demand delta vs expected

Dag 3: Exploratory analysis
- Correlaties plotten
- Patterns identificeren
- Outliers detecteren
```

### Week 3-4: Simulatie
```bash
Dag 1-3: Build agents
- Naive threshold
- Rule-based (met merit order + FRR features)
- ML model (LSTM with all features)

Dag 4-7: Backtest & optimize
- Run simulatie
- Compare agents
- Tune parameters
- Validate robustness
```

---

## 💡 EXTRA API's DIE OOK INTERESSANT ZIJN

### ENTSO-E Transparency Platform
**Wat:** Day-ahead prices (EPEX SPOT)
**Waarom handig:**
- Compare settlement vs day-ahead (spread = arbitrage opportunity)
- Day-ahead is voorspelbaar (gepubliceerd 14:00 voor volgende dag)

**API:** https://transparency.entsoe.eu/
**Rate limits:** Vrij genereus (unlimited voor personal use)

**Use case:**
```python
# Als day-ahead = €0.20 en settlement = €0.35:
spread = settlement_price - day_ahead_price  # €0.15
if spread > 0.10:
    # Grote imbalance premium
    # Markt is tight
    action = "AVOID_BUYING"  # Te duur
```

### KNMI Weer API
**Wat:** Weer forecast + historisch (zon, wind, temp)
**Waarom handig:**
- Zon forecast → solar production → prijzen dalen
- Wind forecast → wind production → prijzen dalen
- Cold snap → hoog verbruik → prijzen stijgen

**API:** https://dataplatform.knmi.nl/
**Rate limits:** Redelijk ruim

**Use case:**
```python
# Als veel zon verwacht (volgende 6u):
if solar_forecast_ghi > 800:  # W/m²
    # Veel solar production verwacht
    # Prijzen gaan waarschijnlijk dalen
    if battery_soc > 60%:
        action = "SELL_NOW"  # Verkoop voor de solar flood
```

---

## ✅ FINALE AANBEVELING

### Start Met (MVP Week 1-2):
1. ✅ Settlement Prices (bulk)
2. ✅ Balance Delta (daily)
3. ✅ Merit Order List (daily) 🆕
4. ✅ FRR Activations (daily) 🆕
5. ⚠️ Metered Injections (weekly = 52 calls, snel) 🆕

**Totaal: ~500 calls = 2-3 dagen**

### Add Later (Week 3-4):
6. ✅ Reconciliation Prices
7. ✅ ENTSO-E Day-ahead (bonus)
8. ✅ KNMI Weer (bonus)

### Features Priority:
**Agent V1 (Naive):** Alleen settlement price
**Agent V2 (Rule-based):** + Balance delta + FRR stress
**Agent V3 (Advanced):** + Merit order + Metered load
**Agent V4 (ML):** Alle features + weather

---

**Je had helemaal gelijk! Merit Order, FRR en Metered Injections zijn zeer waardevol. Zullen we nu het download script bouwen?** 🚀
