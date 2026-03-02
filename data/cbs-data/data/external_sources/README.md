# External Data Sources for KIIRA-PAY

Deze directory bevat data van externe bronnen die relevant zijn voor energie-analyse, -handel en -optimalisatie.

## 📁 Directory Structuur

### 🇳🇱 Nederlandse Bronnen

#### **`tennet/`** - TenneT TSO (Transmission System Operator)
- **Wat:** Real-time en historische elektriciteitsdata
- **Data:**
  - Stroomproductie per energiebron (real-time)
  - Netbelasting en -capaciteit
  - Onbalansprijzen (imbalance pricing)
  - Cross-border flows
  - Windverwachtingen en -realisatie
- **API:** https://www.tennet.org/english/operational_management/system_data_relating_to_ongoing_hour.aspx
- **Frequentie:** Real-time (15-min intervals), dagelijks, jaarlijks
- **Licentie:** Open data
- **Prioriteit:** ⭐⭐⭐ MUST HAVE

#### **`knmi/`** - Koninklijk Nederlands Meteorologisch Instituut
- **Wat:** Weer- en klimaatdata Nederland
- **Data:**
  - Historische weerdata (temperatuur, wind, zon, neerslag)
  - Klimaatscenario's
  - Weerverwachtingen
  - Zonnestraling en zonne-uren
  - Windsnelheden op verschillende hoogtes
- **API:** https://www.knmi.nl/kennis-en-datacentrum/achtergrond/data-ophalen-vanuit-een-script
- **Frequentie:** Uurlijks, dagelijks, maandelijks
- **Licentie:** Open data (met bronvermelding)
- **Prioriteit:** ⭐⭐⭐ MUST HAVE

#### **`cpb/`** - Centraal Planbureau
- **Wat:** Economische analyses en prognoses
- **Data:**
  - Macro-economische vooruitzichten
  - Energieprijsprognoses
  - Economische groeivoorspellingen
  - Sectoranalyses (incl. energie)
- **Bron:** https://www.cpb.nl/cijfers
- **Frequentie:** Kwartaal, jaarlijks
- **Licentie:** Open data
- **Prioriteit:** ⭐⭐ SHOULD HAVE

#### **`pdok/`** - Publieke Dienstverlening Op de Kaart
- **Wat:** Geografische en kadastrale data
- **Data:**
  - Gebouwen en adressen (BAG)
  - Energielabels gebouwen
  - Topografische data
  - Windturbine locaties
  - Zonnepaneel installaties
- **API:** https://www.pdok.nl/
- **Frequentie:** Periodiek updates
- **Licentie:** Open data
- **Prioriteit:** ⭐⭐ SHOULD HAVE

#### **`rdw/`** - Rijksdienst voor het Wegverkeer
- **Wat:** Voertuig- en mobiliteitsdata
- **Data:**
  - Elektrische voertuigen (EV) registraties
  - Laadpaallocaties en -gebruik
  - Brandstofverbruik voertuigen
  - Voertuigpark samenstelling
- **API:** https://opendata.rdw.nl/
- **Frequentie:** Maandelijks
- **Licentie:** Open data (CC0)
- **Prioriteit:** ⭐⭐ SHOULD HAVE

#### **`rijkswaterstaat/`** - Rijkswaterstaat
- **Wat:** Infrastructuur en verkeerdata
- **Data:**
  - Verkeersintensiteit (energieverbruik transport)
  - Waterwegen en scheepvaart
  - Infrastructuur energie-netwerk
- **API:** https://www.ndw.nu/
- **Frequentie:** Real-time, dagelijks
- **Licentie:** Open data
- **Prioriteit:** ⭐ NICE TO HAVE

### 🇪🇺 Europese Bronnen

#### **`entso-e/`** - European Network of Transmission System Operators
- **Wat:** Pan-Europees elektriciteitsnetwerk data
- **Data:**
  - Cross-border electricity flows
  - Day-ahead en intraday prijzen
  - Productie en consumptie per land
  - Transmissiecapaciteit
- **API:** https://transparency.entsoe.eu/
- **Frequentie:** Real-time, dagelijks
- **Licentie:** Open data (registratie vereist)
- **Prioriteit:** ⭐⭐⭐ MUST HAVE

#### **`eurostat/`** - Europees Bureau voor de Statistiek
- **Wat:** EU-brede statistische data
- **Data:**
  - Energie balansen EU landen
  - Prijzen energie per land
  - Hernieuwbare energie aandelen
  - CO2 emissies
- **API:** https://ec.europa.eu/eurostat/web/main/data/web-services
- **Frequentie:** Maandelijks, jaarlijks
- **Licentie:** Open data
- **Prioriteit:** ⭐⭐ SHOULD HAVE

#### **`ecb/`** - Europese Centrale Bank
- **Wat:** Financiële en economische data
- **Data:**
  - Rentetarieven
  - Inflatie
  - Wisselkoersen
  - Economische indicatoren
- **API:** https://sdw.ecb.europa.eu/
- **Frequentie:** Dagelijks, maandelijks
- **Licentie:** Open data
- **Prioriteit:** ⭐ NICE TO HAVE

### 🌍 Internationale Bronnen

#### **`iea/`** - International Energy Agency
- **Wat:** Mondiale energie-analyse en -statistieken
- **Data:**
  - World Energy Outlook
  - Energie balansen wereldwijd
  - Beleid en best practices
  - Technologie trends
- **Bron:** https://www.iea.org/data-and-statistics
- **Frequentie:** Jaarlijks, rapporten
- **Licentie:** Deels open, deels beperkt
- **Prioriteit:** ⭐⭐ SHOULD HAVE

#### **`irena/`** - International Renewable Energy Agency
- **Wat:** Hernieuwbare energie wereldwijd
- **Data:**
  - Renewable capacity statistics
  - Kostenontwikkelingen
  - Policy databases
  - Technology data
- **Bron:** https://www.irena.org/Data
- **Frequentie:** Jaarlijks
- **Licentie:** Open data
- **Prioriteit:** ⭐⭐ SHOULD HAVE

#### **`nasa/`** - NASA Earth Observations
- **Wat:** Satelliet-based klimaat en weer data
- **Data:**
  - Solar irradiance (zonnestraling)
  - Temperatuur
  - Cloud cover
  - Vegetatie indices
- **API:** https://power.larc.nasa.gov/
- **Frequentie:** Dagelijks, historisch
- **Licentie:** Open data
- **Prioriteit:** ⭐⭐ SHOULD HAVE

### ☀️ Zonne-energie Specifiek

#### **`pvgis/`** - Photovoltaic Geographical Information System
- **Wat:** Zonne-energie potentie en productie
- **Data:**
  - Solar radiation databases
  - PV performance calculations
  - Optimal tilt angles
  - Historical solar data
- **API:** https://re.jrc.ec.europa.eu/pvg_tools/en/
- **Frequentie:** Historisch + real-time
- **Licentie:** Open data (EU)
- **Prioriteit:** ⭐⭐⭐ MUST HAVE (voor solar trading)

#### **`solcast/`** - Solcast Solar Forecasting
- **Wat:** High-resolution solar forecasting
- **Data:**
  - Solar irradiance forecasts
  - Cloud tracking
  - PV power forecasts
  - Historical actuals
- **API:** https://solcast.com/
- **Frequentie:** Real-time forecasts (15-min)
- **Licentie:** Commercieel (hobbyist tier beschikbaar)
- **Prioriteit:** ⭐⭐ SHOULD HAVE

### 🌤️ Weer Services

#### **`openweather/`** - OpenWeatherMap
- **Wat:** Weer data en voorspellingen
- **Data:**
  - Current weather
  - 5-day / 3-hour forecasts
  - Historical weather data
  - Weather alerts
- **API:** https://openweathermap.org/api
- **Frequentie:** Real-time, voorspellingen
- **Licentie:** Freemium (1000 calls/day gratis)
- **Prioriteit:** ⭐⭐ SHOULD HAVE

---

## 🎯 Download Prioriteiten

### PHASE 1 - Critical (Start direct)
1. ✅ **CBS** - Basis Nederlandse energie statistieken (DONE)
2. 🔄 **TenneT** - Real-time marktdata en netinformatie
3. 🔄 **KNMI** - Weerdata voor forecasting
4. 🔄 **ENTSO-E** - Europese marktdata

### PHASE 2 - Important (Volgende sprint)
5. 🔄 **PVGIS** - Zonne-energie berekeningen
6. 🔄 **Eurostat** - EU-brede vergelijkingen
7. 🔄 **NASA** - Satelliet weer/klimaat data
8. 🔄 **CPB** - Economische voorspellingen

### PHASE 3 - Valuable (Later)
9. 🔄 **RDW** - EV en mobiliteitsdata
10. 🔄 **PDOK** - Geografische gebouw/installatie data
11. 🔄 **IEA/IRENA** - Internationale benchmarks
12. 🔄 **OpenWeather/Solcast** - Commercial weather APIs

---

## 📊 Data Strategie per Bron

### Real-time Sources (streaming/frequent polling)
- TenneT (15-min)
- ENTSO-E (hourly)
- OpenWeather (hourly)
- Solcast (15-min)

### Daily Updates
- KNMI (dagelijkse weer data)
- RDW (registratie updates)
- Rijkswaterstaat (verkeerdata)

### Weekly/Monthly Updates
- CBS (nieuwe releases)
- CPB (publicaties)
- Eurostat (maandelijkse stats)

### Yearly/Periodic
- IEA (rapporten)
- IRENA (statistics)
- ECB (economische data)
- PDOK (gebouwen/infra updates)

---

## 🔧 Technische Implementatie

### Voor elke bron:
1. **API wrapper script** - `download_<source>.py`
2. **Data schema** - Standaardiseer naar gemeenschappelijk format
3. **Update scheduler** - Cron jobs of airflow DAGs
4. **Validation** - Data quality checks
5. **Documentation** - README per bron met details

### Data formats:
- **Time series:** Parquet (efficient) of CSV
- **Metadata:** JSON
- **Geospatial:** GeoJSON of Shapefile
- **Large files:** Compressed (gzip)

---

## 🚀 Next Steps

1. ✅ Directory structuur aangemaakt
2. 🔄 Download scripts per prioritaire bron
3. 🔄 API credentials/keys setup (waar nodig)
4. 🔄 Data harmonisatie (timestamps, units, formats)
5. 🔄 Integration met dashboard
6. 🔄 ML feature engineering pipeline

---

**Status:** 🏗️ Structure created - Ready for data ingestion  
**Maintainer:** KIIRA-PAY Team  
**Last Updated:** February 14, 2025
