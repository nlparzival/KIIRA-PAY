# 🎯 CBS & NETBEHEERDER DATA MASTERPLAN

**Datum:** 13 februari 2026  
**Status:** Research compleet - klaar voor implementatie

---

## 📊 OVERZICHT: WAT WE GAAN DOWNLOADEN

### **10 CBS Energie Tabellen** (via OData API ✅)
### **3 Grote Netbeheerders** (Liander, Enexis, Stedin)
### **1 Nationale Aggregator** (EDSN - dekt ALLE netbeheerders!)

---

## 🏆 TIER 1: PRIORITEIT (Start hier!)

### 1. ⭐⭐⭐⭐⭐ EDSN - Energie Data Services Nederland
**Waarom het belangrijkste:**
- Aggregeert data van ALLE netbeheerders (Liander, Enexis, Stedin, etc.)
- Verbruik per postcodegebied voor heel Nederland
- Één API = alle data (geen 5+ losse bronnen nodig)

**Data:**
- ✅ Kleinverbruik per postcodegebied (huishoudens)
- ✅ Grootverbruik per postcodegebied (bedrijven)
- ✅ Teruglevering (solar overproductie)
- ✅ Historische profielen

**Setup:**
1. Registreer op https://www.edsn.nl
2. Aanvraag API toegang (gratis, maar goedkeuring nodig)
3. Download postcodedata

**Impact:** 🔥🔥🔥🔥🔥  
**Tijd:** 1 uur setup + 1 uur download  
**Status:** 🔨 SCRIPT NOG TE MAKEN

---

### 2. ⭐⭐⭐⭐⭐ CBS 84575NED - Elektriciteitsproductie naar bron
**Waarom cruciaal:**
- Maandelijkse productie per energiebron
- Zie precies: hoeveel solar/wind/gas/kolen/nucleair
- Correleer met prijzen!

**Data:**
- Productie in GWh per maand
- Per bron: solar, wind, gas, kolen, nucleair, biomassa
- Historisch vanaf ~2010

**API:**
```
https://opendata.cbs.nl/ODataApi/odata/84575NED/TypedDataSet
```

**Impact:** 🔥🔥🔥🔥🔥  
**Tijd:** 30 minuten  
**Status:** ✅ API getest en werkend

---

### 3. ⭐⭐⭐⭐⭐ CBS 84859NED - Capaciteit elektriciteitsproductie
**Waarom belangrijk:**
- Totale geïnstalleerde capaciteit per bron
- Zie maximale potentieel (vooral solar/wind)
- Track groei hernieuwbare energie

**Data:**
- Capaciteit in MW per bron
- Jaarlijkse updates
- Historische trends

**API:**
```
https://opendata.cbs.nl/ODataApi/odata/84859NED/TypedDataSet
```

**Impact:** 🔥🔥🔥🔥  
**Tijd:** 20 minuten  
**Status:** ✅ API klaar

---

### 4. ⭐⭐⭐⭐ Liander Open Data - Solar/Wind per Postcodegebied
**Waarom waardevol:**
- Grootste netbeheerder (3.1M aansluitingen)
- Dekt: Noord-Holland, Gelderland, Flevoland, Friesland
- Exacte locatie van solar installaties

**Data:**
- Kleinverbruik per postcode
- Grootverbruik per postcode
- Zonnepanelen per postcode
- Laadpaaldata
- Capaciteitskaart (waar is netcongestie?)

**Download:**
- CSV files via https://www.liander.nl/partners/datadiensten/open-data
- Geen API - handmatige download of scraping

**Impact:** 🔥🔥🔥🔥  
**Tijd:** 30 minuten (CSV download)  
**Status:** 🔨 DOWNLOAD SCRIPT NOG TE MAKEN

---

## 🥈 TIER 2: HOGE WAARDE (Volgende stappen)

### 5. CBS 83989NED - Elektriciteitsprijzen Eindverbruikers
**Data:** Gemiddelde prijzen per kwartaal  
**Impact:** 🔥🔥🔥 Prijstrends  
**Tijd:** 20 min  
**API:** `https://opendata.cbs.nl/ODataApi/odata/83989NED/TypedDataSet`

### 6. CBS 70960ned - Hernieuwbare Energie
**Data:** Aandeel renewables, trends  
**Impact:** 🔥🔥🔥 Macro analyse  
**Tijd:** 20 min  
**API:** `https://opendata.cbs.nl/ODataApi/odata/70960ned/TypedDataSet`

### 7. Enexis Open Data
**Coverage:** Noord-Brabant, Limburg, Groningen (2.8M aansluitingen)  
**Data:** Vergelijkbaar met Liander  
**Impact:** 🔥🔥🔥 Regionale dekking  
**Tijd:** 30 min  
**URL:** https://www.enexisgroep.nl/over-ons/wat-we-doen/open-data

### 8. Stedin Open Data
**Coverage:** Zuid-Holland, Utrecht, Zeeland (2.5M aansluitingen)  
**Data:** Capaciteitskaart, transportvolumes  
**Impact:** 🔥🔥🔥 Congestie info  
**Tijd:** 30 min  
**URL:** https://www.stedin.net/zakelijk/open-data

---

## 🥉 TIER 3: NICE TO HAVE

### 9. CBS 82610NED - Elektriciteit Productie/Inzet (jaarlijks)
### 10. CBS 83882NED - Energieverbruik Woningen
### 11. CBS 83140NED - Energiebalans
### 12. CBS 85064NED - Elektriciteit/Warmte Productie

**Impact:** 🔥🔥 Aanvullende context  
**Tijd:** 1 uur totaal

---

## 🛠️ SCRIPTS DIE IK GA MAKEN

### Prioriteit 1 (Deze week):
```
✅ research_cbs_and_dso_apis.py      [KLAAR]
🔨 download_all_cbs_energy.py        [TE MAKEN] - Download alle 10 CBS tabellen
🔨 setup_edsn_guide.md               [TE MAKEN] - EDSN registratie handleiding
🔨 download_liander_data.py          [TE MAKEN] - Liander CSV downloader
```

### Prioriteit 2 (Later):
```
🔨 download_enexis_data.py           [TE MAKEN]
🔨 download_stedin_data.py           [TE MAKEN]
🔨 analyze_dso_coverage.py           [TE MAKEN] - Welke postcodes dekt elke DSO?
🔨 merge_all_energy_data.py          [TE MAKEN] - Combineer CBS + DSO data
```

---

## ⏱️ TIJDSINSCHATTING

### FASE 1: CBS Data (Kan NU direct)
- Script maken: 1 uur
- Download draaien: 30 minuten
- **Totaal: 1.5 uur**

### FASE 2: EDSN Setup (Wachttijd voor approval)
- Registratie: 15 minuten
- Wachten op goedkeuring: 1-3 dagen
- Download: 1 uur
- **Totaal: ~3 dagen (maar weinig actieve tijd)**

### FASE 3: DSO Open Data (Kan NU direct)
- Liander CSV download: 30 min
- Enexis CSV download: 30 min
- Stedin data: 30 min
- **Totaal: 1.5 uur**

### **GRAND TOTAAL: ~3 uur actieve tijd + 1-3 dagen EDSN approval**

---

## 🎯 AANBEVOLEN VOLGORDE

### VANDAAG (doe dit NU):
1. ✅ Maak `download_all_cbs_energy.py` (1 uur)
2. ✅ Download alle CBS tabellen (30 min)
3. ✅ Registreer EDSN account (15 min)
4. ✅ Download Liander CSV's (30 min)

**→ Na 2.5 uur heb je: CBS data + Liander data!**

### MORGEN (terwijl we wachten op EDSN):
5. Download Enexis data (30 min)
6. Download Stedin data (30 min)
7. Maak analyse script voor postcode coverage (1 uur)

### VOLGENDE WEEK (als EDSN approval binnen is):
8. Download EDSN data (1 uur)
9. Merge alles: CBS + EDSN + DSO's (2 uur)
10. Eerste analyse: waar zijn arbitrage kansen? (3 uur)

---

## 💰 WAAROM DIT GOUD WAARD IS

### CBS Data vertelt je:
- 📊 **Hoeveel** solar/wind er nationaal is
- 📈 **Trends**: groeit renewable snel?
- 💰 **Prijzen**: wat betalen eindverbruikers?

### DSO Data vertelt je:
- 📍 **Waar** is solar/wind geconcentreerd?
- 🏘️ **Welke postcodes** produceren/consumeren veel?
- ⚡ **Waar** is netcongestie? (= arbitrage kansen!)

### EDSN Data is de HOLY GRAIL:
- 🗺️ **Compleet Nederland** gedekt
- 📊 **Per postcode** verbruik/productie
- 🎯 **Precies** waar overproductie is op zonnige dagen
- 💎 **Direct** zien: waar zijn negatieve prijzen waarschijnlijk?

---

## 🚀 VOLGENDE STAP

**Wil je dat ik:**

### Optie A: Direct Beginnen 🔥
→ Ik maak NU `download_all_cbs_energy.py` en we draaien het  
→ Over 30 minuten heb je 10 CBS datasets  
→ Daarna Liander CSV's ophalen

### Optie B: Eerst Overleggen 💬
→ We bespreken exact welke data je prioriteit geeft  
→ Ik maak één mega-script dat alles doet  
→ Je drukt op "run" en over 3 uur is alles binnen

### Optie C: Gefaseerd ⏳
→ Week 1: CBS data  
→ Week 2: DSO data  
→ Week 3: EDSN data (als approval binnen is)

**Wat is jouw voorkeur?** 🤔
