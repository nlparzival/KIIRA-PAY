# NASA POWER API - Complete Data Beschikbaar

## 📡 Wat Is NASA POWER?

**NASA Prediction Of Worldwide Energy Resources**
- Satelliet data vanaf 1981
- Global coverage
- Gratis, geen API key
- Speciaal voor renewable energy applicaties

---

## 🌞 Data Beschikbaar Voor Energie Arbitrage

### ☀️ SOLAR (Meest Belangrijk)

#### 1. **ALLSKY_SFC_SW_DWN** ⭐⭐⭐⭐⭐
**Wat:** All Sky Surface Shortwave Downward Irradiance
**Units:** kW-hr/m²/day
**Betekenis:** Totale zonnestraling die grond bereikt (inclusief bewolking)
**Use case:** 
```python
if solar_irradiance > 5.0:  # kWh/m²/day
    # Zonnige dag, veel solar productie
    # Prijzen dalen waarschijnlijk 11-16u
```

#### 2. **CLRSKY_SFC_SW_DWN** ⭐⭐⭐⭐
**Wat:** Clear Sky Surface Shortwave Downward
**Units:** kW-hr/m²/day
**Betekenis:** Zonnestraling bij heldere hemel (zonder wolken)
**Use case:** Verschil tussen clear sky en all sky = wolken effect

#### 3. **ALLSKY_SFC_PAR_TOT** ⭐⭐⭐
**Wat:** Photosynthetically Active Radiation
**Units:** MJ/m²/day
**Use case:** Plant growth related (minder relevant voor energie)

---

### 🌡️ TEMPERATUUR

#### 4. **T2M** ⭐⭐⭐⭐⭐
**Wat:** Temperature at 2 Meters
**Units:** °C
**Betekenis:** Luchttemperatuur op 2m hoogte
**Use case:**
```python
if temp < 0:  # Vorst
    # Hoog verbruik (verwarming)
    # Hoge prijzen verwacht
elif temp > 25:  # Warm
    # Airco verbruik stijgt
    # Ook hogere prijzen
```

#### 5. **T2M_MAX** ⭐⭐⭐⭐
**Wat:** Maximum Temperature at 2 Meters
**Units:** °C

#### 6. **T2M_MIN** ⭐⭐⭐⭐
**Wat:** Minimum Temperature at 2 Meters
**Units:** °C

#### 7. **T2MDEW** ⭐⭐
**Wat:** Dew/Frost Point at 2 Meters
**Units:** °C

---

### 💨 WIND

#### 8. **WS10M** ⭐⭐⭐⭐⭐
**Wat:** Wind Speed at 10 Meters
**Units:** m/s
**Betekenis:** Windsnelheid op 10m hoogte
**Use case:**
```python
if wind_speed > 12:  # m/s (sterke wind)
    # Veel windenergie productie
    # Lage prijzen, vooral 's nachts
```

#### 9. **WS10M_MAX** ⭐⭐⭐
**Wat:** Maximum Wind Speed at 10 Meters
**Units:** m/s

#### 10. **WS10M_MIN** ⭐⭐
**Wat:** Minimum Wind Speed at 10 Meters
**Units:** m/s

#### 11. **WS50M** ⭐⭐⭐⭐
**Wat:** Wind Speed at 50 Meters
**Units:** m/s
**Betekenis:** Windsnelheid op turbine hoogte
**Use case:** Betere indicator voor wind power production

---

### 💧 NEERSLAG & VOCHTIGHEID

#### 12. **PRECTOTCORR** ⭐⭐⭐⭐
**Wat:** Precipitation Corrected
**Units:** mm/day
**Betekenis:** Totale neerslag per dag
**Use case:** Regen = minder zon = minder solar

#### 13. **RH2M** ⭐⭐⭐
**Wat:** Relative Humidity at 2 Meters
**Units:** %
**Betekenis:** Luchtvochtigheid

---

### ☁️ BEWOLKING

#### 14. **CLOUD_AMT** ⭐⭐⭐⭐
**Wat:** Cloud Amount
**Units:** %
**Betekenis:** Bewolking percentage
**Use case:**
```python
if cloud_amount > 80:
    # Bewolkt, weinig zon
    # Solar productie laag
    # Prijzen hoger
```

---

### 🌍 ATMOSFEER

#### 15. **PS** ⭐⭐
**Wat:** Surface Pressure
**Units:** kPa
**Betekenis:** Luchtdruk

#### 16. **QV2M** ⭐
**Wat:** Specific Humidity at 2 Meters
**Units:** g/kg

---

## 🎯 Meest Waardevolle Voor Arbitrage

### Top 5 NASA POWER Parameters:

1. **ALLSKY_SFC_SW_DWN** ⭐⭐⭐⭐⭐
   - Solar irradiance (DE solar indicator)
   - Direct correlatie met zonnepaneel productie

2. **T2M** ⭐⭐⭐⭐⭐
   - Temperatuur (verwarming/airco verbruik)
   - Extreme temp = hoge prijzen

3. **WS10M** of **WS50M** ⭐⭐⭐⭐⭐
   - Wind speed (windmolen productie)
   - Hoge wind = lage prijzen (vooral 's nachts)

4. **PRECTOTCORR** ⭐⭐⭐⭐
   - Neerslag (zon indicator)
   - Regen = minder solar = hogere prijzen

5. **CLOUD_AMT** ⭐⭐⭐⭐
   - Bewolking (solar blocker)
   - Directe impact op solar productie

---

## 📥 Download Alle Relevante Parameters

```bash
# NASA POWER - All important parameters for energy
curl "https://power.larc.nasa.gov/api/temporal/daily/point?\
parameters=ALLSKY_SFC_SW_DWN,CLRSKY_SFC_SW_DWN,\
T2M,T2M_MAX,T2M_MIN,\
WS10M,WS10M_MAX,WS50M,\
PRECTOTCORR,RH2M,CLOUD_AMT,PS\
&community=RE\
&longitude=4.89\
&latitude=52.37\
&start=20250101\
&end=20251231\
&format=JSON" -o data/nasa_power_full_2025.json
```

---

## 📊 NASA vs Open-Meteo Vergelijking

| Feature | NASA POWER | Open-Meteo |
|---------|------------|------------|
| **Solar Irradiance** | ⭐⭐⭐⭐⭐ Zeer accurate (satelliet) | ⭐⭐⭐⭐ Goed |
| **Temperature** | ⭐⭐⭐⭐ Daily avg | ⭐⭐⭐⭐⭐ Hourly |
| **Wind** | ⭐⭐⭐⭐ Meerdere hoogtes | ⭐⭐⭐⭐ 10m + 100m |
| **Temporal Res** | ⚠️ Daily only | ✅ Hourly |
| **Historical** | ✅ Vanaf 1981 | ✅ Vanaf 1940 |
| **Forecast** | ❌ Nee | ✅ 16 dagen |
| **API Key** | ❌ Niet nodig | ❌ Niet nodig |
| **Rate Limit** | ~50 req/min | ~Unlimited |
| **Best For** | Solar accuracy | Hourly granularity |

---

## 💡 Gebruik Beide!

**Strategie:**
1. **Open-Meteo:** Hourly data voor simulation (primair)
2. **NASA POWER:** Cross-validate solar data (accuracy check)

**Als solar irradiance verschilt:**
```python
open_meteo_solar = 850  # W/m² (hourly avg)
nasa_solar = 5.2  # kWh/m²/day

# Convert NASA to W/m² avg
nasa_avg_wm2 = (nasa_solar * 1000) / 24  # ~217 W/m²

# Check consistency
if abs(open_meteo_solar - nasa_avg_wm2*4) < 100:
    # Data consistent, use it
    pass
```

---

## 🚀 Downloaded Data

✅ **Already Downloaded:**
- `data/nasa_power_2025.json` (31 KB)
- Parameters: Solar, Temp, Wind, Humidity, Precipitation
- 365 days, daily resolution

**To download full set:**
```bash
curl "https://power.larc.nasa.gov/api/temporal/daily/point?parameters=ALLSKY_SFC_SW_DWN,CLRSKY_SFC_SW_DWN,T2M,T2M_MAX,T2M_MIN,WS10M,WS10M_MAX,WS50M,PRECTOTCORR,RH2M,CLOUD_AMT&community=RE&longitude=4.89&latitude=52.37&start=20250101&end=20251231&format=JSON" -o data/nasa_power_full_2025.json
```

---

## 📋 Parameters Samenvatting

**Gedownload (nu):**
- ALLSKY_SFC_SW_DWN (Solar irradiance)
- T2M (Temperature)
- WS10M (Wind speed)
- RH2M (Humidity)
- PRECTOTCORR (Precipitation)

**Extra te downloaden:**
- CLRSKY_SFC_SW_DWN (Clear sky solar)
- T2M_MAX, T2M_MIN (Min/max temp)
- WS50M (Wind at 50m)
- WS10M_MAX (Max wind)
- CLOUD_AMT (Cloud cover)

**Total parameters beschikbaar: 50+**
**Relevant voor energie: ~15**
**Echt nodig: ~8**

---

## ✅ Wat Heb Je Nu?

1. ✅ **Basic NASA POWER data** (5 parameters, 365 days)
2. ✅ **Open-Meteo data** (6 parameters, 8760 hours)

**Recommendation:** Gebruik Open-Meteo als primair (hourly), NASA als validation/backup (daily).

---

*NASA POWER is gratis, accurate, en perfect als backup/validation voor Open-Meteo! 🛰️*
