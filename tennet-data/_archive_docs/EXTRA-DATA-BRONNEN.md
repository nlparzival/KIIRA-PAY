# 🔋 EXTRA NEDERLANDSE DATA BRONNEN - COMPLETE LIJST

**Datum:** 13 februari 2026  
**Status:** Te onderzoeken & downloaden

---

## 📊 CBS - EXTRA ENERGIE & TRANSPORT DATA

### 🔋 Energie Verbruik
```
Potentiële tabellen:
- Energieverbruik per sector (huishoudens, industrie, diensten)
- Gasverbruik per provincie
- Elektriciteitsverbruik per provincie
- Energiekosten en prijzen
- Energiearmoede statistieken
- Warmteverbruik per regio
```

### 🚗 Transport & Mobiliteit  
```
CBS Tabellen:
- Personenauto's per brandstofsoort
- Elektrische voertuigen stock
- Laadpalen ontwikkeling
- Voertuigkilometers per type
- Benzine & diesel verkoop
- Brandstofprijzen
- Modal split (auto/trein/fiets)
- Verkeersintensiteit
```

### 🏭 Industrie & Sectoren
```
- Energieverbruik industrie per sector
- Zware industrie (staal, chemie, raffinaderijen)
- Glastuinbouw energieverbruik
- Datacenters energieverbruik
- Energiesubsidies per sector
```

### 🌡️ Klimaat & Emissies
```
- CO2 emissies per sector
- Broeikasgassen totaal
- Luchtkwaliteit (NOx, PM2.5, PM10)
- Klimaatdoelen voortgang
- Carbon footprint per inwoner
```

### 🏠 Gebouwen & Woningen
```
- Energielabels woningen (A-G)
- Isolatie maatregelen
- Warmtepompen installaties
- Zonnepanelen op daken (aantal & vermogen)
- Gasaansluitingen vs all-electric
- Warmtenetten aansluitingen
```

---

## 🚗 RDW (Rijksdienst voor het Wegverkeer)

**Website:** https://opendata.rdw.nl/  
**Status:** ✅ 100% OPEN DATA, geen registratie

### Beschikbare Datasets:

#### 1. **Voertuigregistratie**
```
- Alle voertuigen in NL (kenteken niveau!)
- Merk, model, bouwjaar
- Brandstoftype (benzine, diesel, elektr, hybride, LPG, waterstof)
- CO2 uitstoot
- Gewicht, vermogen
- APK status
- Export status
```

#### 2. **Elektrische Voertuigen**
```
- Alle EV's in Nederland
- Actieradius (WLTP)
- Batterij capaciteit
- Laadsnelheid
- Subsidies (via RVO gekoppeld)
```

#### 3. **Laadpalen**
```
- Alle publieke laadpalen NL
- Locatie (GPS coordinaten!)
- Aantal aansluitingen
- Vermogen (kW)
- Exploitant
- Gebruik statistieken
```

#### 4. **Brandstof Verkoop**
```
- Benzine verkoop per maand
- Diesel verkoop per maand
- LPG verkoop
- Elektrisch laden (kWh)
```

**Formaat:** CSV, JSON  
**Update:** Maandelijks  
**Volume:** 10M+ voertuigen, 100K+ laadpalen

---

## 🗺️ PDOK (Publieke Dienstverlening Op de Kaart)

**Website:** https://www.pdok.nl/  
**Status:** ✅ OPEN DATA, WFS/WMS services

### Energie Gerelateerde Datasets:

#### 1. **BAG (Basisregistratie Adressen en Gebouwen)**
```
- Alle gebouwen in NL met coordinaten
- Bouwjaar
- Oppervlakte
- Gebruiksdoel (wonen, industrie, kantoor, etc.)
- Combineer met energielabels!
```

#### 2. **Energielabels (EP-Online via PDOK)**
```
- Energielabel per adres (A++ tot G)
- Registratiedatum
- Theoretisch energieverbruik
- Aanbevelingen
```

#### 3. **Warmtenetten**
```
- Locaties warmtenetten
- Capaciteit
- Aansluitingen
```

#### 4. **Windmolens & Zonneparken**
```
- Locaties alle windmolens
- Vermogen per turbine
- Zonneparken locaties
- Capaciteit per park
```

#### 5. **Laagspanningsnetten**
```
- Grid infrastructuur (indien beschikbaar)
- Transformatorhuisjes
- Stations
```

---

## 🌍 ANDERE OPEN DATA BRONNEN

### 1. **RVO (Rijksdienst voor Ondernemend Nederland)**
**Website:** https://www.rvo.nl/onderwerpen/duurzaam-ondernemen/energie-en-milieu-innovaties  

```
Datasets:
- Subsidie overzicht (ISDE, SDE++, etc.)
- Zonnepanelen subsidies per postcode
- Warmtepomp subsidies
- Isolatie subsidies
- Energiebesparing projecten
```

### 2. **Klimaatmonitor**
**Website:** https://klimaatmonitor.databank.nl/  

```
Datasets:
- CO2 uitstoot per gemeente
- Hernieuwbare energie per gemeente
- Energieverbruik per gemeente
- Warmtebehoefte per wijk
- Zonnepanelen per gemeente
```

### 3. **KNMI (Koninklijk Nederlands Meteorologisch Instituut)**
**API:** https://www.knmi.nl/kennis-en-datacentrum/achtergrond/data-ophalen-vanuit-een-script  

```
Extra data:
- Historische weer data (1901-nu!)
- Klimaat scenario's
- Zonnestraling per uur (historisch)
- Wind data per station
- Neerslag radar
```

### 4. **EMIS (Emissieregistratie)**
**Website:** https://www.emissieregistratie.nl/  

```
Datasets:
- Industriële emissies per bedrijf
- Luchtkwaliteit metingen
- Verkeer emissies
- Landbouw emissies
```

### 5. **NEa (Nederlandse Emissieautoriteit)**
**Website:** https://www.emissieautoriteit.nl/  

```
Datasets:
- CO2 handel data
- Emissierechten
- Industrie rapportages
```

### 6. **PBL (Planbureau voor de Leefomgeving)**
**Website:** https://www.pbl.nl/  

```
Datasets:
- Klimaatscenario's
- Energietransitie prognoses
- Kosten-baten analyses
- Ruimtelijke ordening & energie
```

---

## 🎯 PRIORITEIT DOWNLOADS

### HIGH PRIORITY (Direct beschikbaar, grote impact)

1. **RDW Voertuigen** ⚡
   - 10M+ kentekens met brandstoftype
   - EV groei tracking
   - Vervoer energie footprint
   ```bash
   URL: https://opendata.rdw.nl/resource/m9d7-ebf2.json
   API: Socrata API, geen key
   ```

2. **RDW Laadpalen** 🔌
   - 100K+ laadpalen met locaties
   - Grid belasting analyse
   - EV infrastructuur groei
   ```bash
   URL: https://opendata.rdw.nl/resource/w4rt-e856.json
   ```

3. **CBS Voertuigkilometers** 🚗
   - Energieverbruik transport
   - Modal split trends
   ```bash
   CBS Statline: Zoek "voertuigkilometers"
   ```

4. **Klimaatmonitor** 🌍
   - Gemeente niveau energie data
   - Hernieuwbare energie per regio
   ```bash
   https://klimaatmonitor.databank.nl/
   Download CSV exports
   ```

5. **PDOK Energielabels** 🏠
   - Alle gebouwen met energielabel
   - Renovatie potentieel
   ```bash
   WFS: https://service.pdok.nl/rvo/ep-online/wfs/v1_0
   ```

### MEDIUM PRIORITY (Interessant, extra context)

6. **CBS Energieprijzen**
   - Elektriciteit & gas prijzen
   - Correlatie met verbruik

7. **CBS Industrie verbruik**
   - Per sector breakdown
   - Grootste verbruikers

8. **RVO Subsidies**
   - Zonnepanelen, warmtepompen
   - Geografische verdeling

9. **KNMI Historisch**
   - Lange termijn weer trends
   - Klimaatverandering impact

### LOW PRIORITY (Nice to have)

10. **EMIS Emissies**
11. **NEa CO2 handel**
12. **PBL Scenario's**

---

## 🚀 DIRECT TE DOWNLOADEN

### RDW API Endpoints (NO AUTH NEEDED!)

```bash
# Alle voertuigen (10M+ records!)
https://opendata.rdw.nl/resource/m9d7-ebf2.json?$limit=50000

# Elektrische voertuigen
https://opendata.rdw.nl/resource/w4rt-e856.json

# Laadpalen
https://opendata.rdw.nl/resource/t3gg-hs5f.json

# Brandstofverbruik
https://opendata.rdw.nl/resource/8ys7-d773.json
```

### CBS Extra Tabellen

```bash
# Via OData API (we kennen dit al):
https://odata4.cbs.nl/CBS/84976NED/Observations  # Energieprijzen
https://odata4.cbs.nl/CBS/70846ned/Observations  # Voertuigkilometers
https://odata4.cbs.nl/CBS/83699NED/Observations  # Gebouwen energielabels
```

### PDOK WFS Services

```bash
# Energielabels (WFS)
https://service.pdok.nl/rvo/ep-online/wfs/v1_0?service=WFS&request=GetCapabilities

# BAG Gebouwen
https://service.pdok.nl/lv/bag/wfs/v2_0?service=WFS&request=GetCapabilities
```

---

## 📊 WAT DIT TOEVOEGT AAN JE ANALYSE

### Met RDW Data:
```
✅ Transport energie footprint
✅ EV adoptie per regio
✅ Laadpaal groei vs EV groei
✅ Brandstofverbruik trends
✅ Voorspel grid belasting van EV's
✅ Correlatie EV's met zonnepanelen (eigen laden)
```

### Met PDOK Data:
```
✅ Energielabels op kaart
✅ Renovatie potentieel per wijk
✅ Warmtenetten coverage
✅ Windmolens vs consumptie matching
```

### Met Extra CBS Data:
```
✅ Complete energie balans (productie + verbruik + transport)
✅ Prijzen vs verbruik correlatie
✅ Sector breakdown (wie gebruikt wat)
✅ Energiearmoede analyse
```

### Combined Analysis:
```
🎯 Complete Nederlandse Energie Ecosysteem
   - Productie (CBS + Stedin/Liander)
   - Verbruik (Stedin/Liander + CBS sectoren)
   - Transport (RDW voertuigen)
   - Gebouwen (PDOK energielabels)
   - Klimaat (KNMI weer + CBS emissies)
   - Infrastructuur (RDW laadpalen + PDOK netten)
```

---

## 🔥 NEXT STEPS - SUPER DATASET

### Fase 1: RDW Data (NOW!)
```bash
python download_rdw_vehicles.py
python download_rdw_laadpalen.py
```
**Result:** 10M+ voertuigen, 100K+ laadpalen

### Fase 2: Extra CBS (Easy)
```bash
python download_extra_cbs.py
# - Voertuigkilometers
# - Energieprijzen
# - Gebouwen labels
```

### Fase 3: PDOK/Klimaatmonitor (Medium)
```bash
python download_pdok_energielabels.py
python scrape_klimaatmonitor.py
```

### Fase 4: Integratie Dashboard
```python
# Dashboard v3.0:
# - Transport tab (RDW)
# - Gebouwen tab (PDOK)
# - Gemeente tab (Klimaatmonitor)
# - Complete analyse
```

---

**Wil je dat ik nu de RDW voertuigen data ga downloaden?** 🚗⚡  
**10 miljoen kentekens met brandstoftype, EV's, emissies, etc!**
