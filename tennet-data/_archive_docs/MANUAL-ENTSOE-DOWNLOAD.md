# Handmatig ENTSO-E Data Downloaden (GEEN API NODIG!)

## 🎯 Waarom Handmatig Downloaden?

Je wacht nog op API token van ENTSO-E, maar je kunt **NU AL** historische data downloaden via hun publiekelijke web interface!

---

## 📊 Wat Haal Je Op?

### ✅ Day-Ahead Prijzen (Nederland)
- **Wat:** Stroomprijs per uur, 1 dag vooruit bepaald
- **Format:** €/MWh
- **Resolutie:** Uurlijks (24 datapunten per dag)
- **Gebruiken voor:** Arbitrage basisprijs, seasonaliteit, tijdspatronen

### ✅ Imbalance Prijzen (optioneel)
- **Wat:** Onbalans prijzen (vergelijkbaar met TenneT settlement prices)
- **Format:** €/MWh
- **Resolutie:** Per 15 minuten of uurlijks
- **Gebruiken voor:** Real-time arbitrage simulatie

### ✅ Actual Load (verbruik)
- **Wat:** Totale elektriciteitsvraag in Nederland
- **Format:** MW
- **Gebruiken voor:** Correlatie met prijzen (hoge vraag = hogere prijzen)

### ✅ Generation by Source
- **Wat:** Hoeveel stroom geproduceerd door wind, solar, gas, etc.
- **Gebruiken voor:** Renewables impact op prijzen

---

## 🚀 STAP-VOOR-STAP HANDLEIDING

### Stap 1: Open de Transparency Platform

Ga naar: **https://transparency.entsoe.eu/**

Je hoeft **NIET** in te loggen voor basis data downloads!

---

### Stap 2: Navigeer naar Day-Ahead Prijzen

1. Klik op **"Transmission"** (in het menu)
2. Klik op **"Day-Ahead Prices"**
3. Of ga direct naar: https://transparency.entsoe.eu/transmission-domain/r2/dayAheadPrices/show

---

### Stap 3: Configureer je Download

#### A. Selecteer Gebied
- **Bidding Zone:** Kies **"NL - Netherlands, TSO: TenneT NL"**

#### B. Selecteer Tijdsperiode
Voor simulatie training, haal minimaal **1 jaar** data op:
- **Start:** 1 januari 2024 (of eerder)
- **End:** 31 december 2024

💡 **Tip:** Download per maand of per kwartaal als 1 jaar te groot is

#### C. Selecteer Data Type
- **Metric:** Day-Ahead Prices
- **Unit:** EUR/MWh

---

### Stap 4: Download de Data

1. Klik op **"Export"** of **"Download"** knop
2. Kies formaat: **CSV** (makkelijkst voor Python)
3. Klik op **"Download"**
4. Sla het bestand op in: `/Users/moesa/KIIRA-PAY/tennet-data/data/`
5. Hernoem naar: `entsoe_day_ahead_2024.csv`

---

### Stap 5: Herhaal voor Andere Datasets (Optioneel)

#### Imbalance Prijzen
1. Ga naar: **"Balancing"** → **"Imbalance Prices"**
2. Selecteer **NL**, zelfde tijdsperiode
3. Download als `entsoe_imbalance_2024.csv`

#### Actual Load
1. Ga naar: **"Consumption"** → **"Actual Total Load"**
2. Selecteer **NL**, zelfde tijdsperiode
3. Download als `entsoe_load_2024.csv`

#### Generation by Source
1. Ga naar: **"Generation"** → **"Actual Generation per Production Type"**
2. Selecteer **NL**, zelfde tijdsperiode
3. Download als `entsoe_generation_2024.csv`

---

## 📂 Verwachte Bestandsstructuur

Na downloaden:

```
tennet-data/data/
├── open_meteo_2025.csv           ✅ (al binnen)
├── nasa_power_full_2025.json     ✅ (al binnen)
├── knmi_2025.txt                 ✅ (al binnen)
├── entsoe_day_ahead_2024.csv     🆕 (handmatig downloaden)
├── entsoe_imbalance_2024.csv     🆕 (optioneel)
├── entsoe_load_2024.csv          🆕 (optioneel)
└── entsoe_generation_2024.csv    🆕 (optioneel)
```

---

## 🔍 Data Formaat Check

### Day-Ahead Prijzen CSV

Verwacht formaat:

```csv
DateTime,Price [EUR/MWh]
01.01.2024 00:00,65.50
01.01.2024 01:00,58.20
01.01.2024 02:00,52.10
...
```

Of:

```csv
MTU,Day-ahead Price [EUR/MWh]
01.01.2024 00:00 - 01.01.2024 01:00,65.50
01.01.2024 01:00 - 01.01.2024 02:00,58.20
...
```

💡 **Datum/tijd formaat kan variëren**, maar altijd per uur!

---

## 🐍 Python Script om Data te Valideren

Na downloaden, valideer de data:

```bash
cd /Users/moesa/KIIRA-PAY/tennet-data
python3 validate_entsoe_manual.py
```

(Script wordt zo gemaakt!)

---

## ⚡ Wat Kun Je NU AL Doen?

Met je huidige data + handmatig gedownloade ENTSO-E prijzen:

### 1️⃣ Prijs Voorspelling
- Train een ML model om day-ahead prijzen te voorspellen
- Features: weer (Open-Meteo), solar (NASA), seizoen, tijd-van-dag

### 2️⃣ Arbitrage Simulatie (Simpel)
- Simuleer een batterij die koopt bij lage prijzen, verkoopt bij hoge prijzen
- Basis strategie: koop als prijs < daggemiddelde, verkoop als > daggemiddelde

### 3️⃣ Data Exploratie
- Correlatie tussen weer en prijzen
- Identificeer pricing patterns (weekenden vs weekdagen, seizoenen)
- Visualiseer prijsvolatiliteit

### 4️⃣ Benchmarking
- Bereken potentiële winst van perfect arbitrage
- Vergelijk met naïeve strategieën

---

## 🎯 Timeline

| Stap | Status | ETA |
|------|--------|-----|
| Handmatig ENTSO-E day-ahead download | 🟡 TODO | **10 min** |
| Validatie script maken | 🟡 Wachten | **5 min** |
| Data exploratie notebook | 🟡 Wachten | **20 min** |
| Simpele arbitrage simulatie | 🟡 Wachten | **30 min** |
| TenneT API key binnen | ⏳ Wachten | **Onbekend** |
| ENTSO-E API token binnen | ⏳ Wachten | **Onbekend** |

---

## 📚 Relevante Links

- ENTSO-E Transparency: https://transparency.entsoe.eu/
- Day-Ahead Prijzen: https://transparency.entsoe.eu/transmission-domain/r2/dayAheadPrices/show
- Imbalance Prijzen: https://transparency.entsoe.eu/balancing-domain/r3/imbalancePrices/show
- Documentatie: https://transparency.entsoe.eu/content/static_content/Static%20content/web%20api/Guide.html

---

## 🆘 Problemen?

### "Geen download knop zichtbaar"
→ Scrollen naar beneden na query uitvoeren
→ Of gebruik de "Export" knop rechtsboven

### "File is te groot"
→ Download per maand in plaats van heel jaar
→ Of filter op specifieke weken

### "CSV formaat onleesbaar"
→ Open in Excel/Numbers om te inspecteren
→ Of gebruik pandas: `pd.read_csv('file.csv', sep=';')`

### "Timestamps zijn raar"
→ ENTSO-E gebruikt vaak UTC
→ Nederland is UTC+1 (winter) of UTC+2 (zomer)
→ Conversie gebeurt in validation script

---

## ✨ Next Step

**→ Download NU 1 jaar ENTSO-E day-ahead prijzen!**

Als je klaar bent, laat me weten en ik maak:
1. ✅ Validation script voor handmatige downloads
2. ✅ Data exploratie notebook
3. ✅ Simpele arbitrage simulatie

Je hoeft niet meer te wachten op API keys om te starten! 🚀
