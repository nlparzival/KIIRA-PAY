# CBS Open Data - Relevante Datasets voor KIIRA-PAY

Dit document bevat alle CBS datasets die relevant zijn voor het KIIRA-PAY Energy Dashboard.

---

## 🔋 ELEKTRICITEIT & ENERGIE

### 1. Elektriciteit en warmte; productie en inzet naar energiedrager
- **Dataset ID**: `83989NED`
- **Frequentie**: Jaarlijks
- **Periode**: 1998 - heden
- **Inhoud**:
  - Elektriciteitsproductie per energiebron (PJ)
  - Warmteproductie (PJ)
  - Energiebronnen: Gas, Kolen, Olie, Kernenergie, Wind, Zon, Biomassa
  - Bruto/netto productie
- **API Endpoint**: `https://opendata.cbs.nl/ODataApi/odata/83989NED`
- **Prioriteit**: ⭐⭐⭐⭐⭐ (Essentieel)
- **Use Case**: Energiemix visualisatie, bronnen verdeling

### 2. Hernieuwbare energie; verbruik naar energiebron
- **Dataset ID**: `00372ed`
- **Frequentie**: Jaarlijks
- **Periode**: 1990 - heden
- **Inhoud**:
  - Hernieuwbare energie verbruik (PJ)
  - Percentage hernieuwbaar van totaal
  - Per bron: Wind, Zon, Waterkracht, Biomassa, Geothermie
  - Trends over tijd
- **API Endpoint**: `https://opendata.cbs.nl/ODataApi/odata/00372ed`
- **Prioriteit**: ⭐⭐⭐⭐⭐ (Essentieel)
- **Use Case**: Duurzaamheid tracker, klimaatdoelen progress

### 3. Energiebalans; aanbod, omzetting en verbruik
- **Dataset ID**: `84575NED`
- **Frequentie**: Jaarlijks
- **Periode**: 2016 - heden
- **Inhoud**:
  - Primair energieaanbod
  - Energietransformatie
  - Finaal energieverbruik per sector
  - Import/Export energiedragers
- **API Endpoint**: `https://opendata.cbs.nl/ODataApi/odata/84575NED`
- **Prioriteit**: ⭐⭐⭐⭐ (Hoog)
- **Use Case**: Complete energiebalans, sector analyse

### 4. Elektriciteit in Nederland; productie en verbruik
- **Dataset ID**: `70846ned`
- **Frequentie**: Jaarlijks
- **Periode**: 1980 - heden
- **Inhoud**:
  - Bruto elektriciteitsproductie (miljard kWh)
  - Netto productie
  - Invoer/Uitvoer elektriciteit
  - Binnenlands verbruik
- **API Endpoint**: `https://opendata.cbs.nl/ODataApi/odata/70846ned`
- **Prioriteit**: ⭐⭐⭐⭐ (Hoog)
- **Use Case**: Import/export analyse, zelfvoorziening

---

## 💰 PRIJZEN

### 5. Energieprijzen; gaslevering aan kleinverbruikers
- **Dataset ID**: `82380NED`
- **Frequentie**: Maandelijks
- **Periode**: 2008 - heden
- **Inhoud**:
  - Gasprijs per m³ (euro)
  - Inclusief/exclusief belasting
  - Verschillende verbruiksklassen
- **API Endpoint**: `https://opendata.cbs.nl/ODataApi/odata/82380NED`
- **Prioriteit**: ⭐⭐⭐ (Gemiddeld)
- **Use Case**: Prijstrends, consument impact

### 6. Consumentenprijzen; prijsindex (CPI)
- **Dataset ID**: `81309NED`
- **Frequentie**: Maandelijks
- **Periode**: 2015 - heden
- **Inhoud**:
  - CPI energie (2015=100)
  - Elektriciteit prijsindex
  - Gas prijsindex
- **API Endpoint**: `https://opendata.cbs.nl/ODataApi/odata/81309NED`
- **Prioriteit**: ⭐⭐⭐ (Gemiddeld)
- **Use Case**: Inflatie correctie, kosten ontwikkeling

---

## 🏭 SECTOREN & VERBRUIK

### 7. Energieverbruik particuliere huishoudens; woningtype en regio
- **Dataset ID**: `81528NED`
- **Frequentie**: Jaarlijks
- **Periode**: 2010 - heden
- **Inhoud**:
  - Energieverbruik per huishouden (GJ)
  - Gas, elektriciteit verbruik
  - Per woningtype en regio
- **API Endpoint**: `https://opendata.cbs.nl/ODataApi/odata/81528NED`
- **Prioriteit**: ⭐⭐ (Laag)
- **Use Case**: Consument profiling, regionale analyse

### 8. Energieverbruik bedrijven; bedrijfstak
- **Dataset ID**: `81309NED`
- **Frequentie**: Jaarlijks
- **Periode**: 2000 - heden
- **Inhoud**:
  - Energieverbruik per sector (PJ)
  - Industrie, landbouw, diensten
  - Elektriciteit en gas apart
- **API Endpoint**: `https://opendata.cbs.nl/ODataApi/odata/81309NED`
- **Prioriteit**: ⭐⭐ (Laag)
- **Use Case**: B2B inzichten, industrie analyse

---

## 🌍 EMISSIES & KLIMAAT

### 9. CO2-emissies; nationale rekeningen
- **Dataset ID**: `83300NED`
- **Frequentie**: Jaarlijks
- **Periode**: 1990 - heden
- **Inhoud**:
  - CO2 uitstoot per sector (Mton)
  - Energie gerelateerde emissies
  - Trends over tijd
- **API Endpoint**: `https://opendata.cbs.nl/ODataApi/odata/83300NED`
- **Prioriteit**: ⭐⭐⭐ (Gemiddeld)
- **Use Case**: Carbon footprint, klimaat impact

---

## 📋 PRIORITEITEN VOOR MVP

### Must Have (Sprint 1):
1. ⭐⭐⭐⭐⭐ **83989NED** - Elektriciteitsproductie per bron
2. ⭐⭐⭐⭐⭐ **00372ed** - Hernieuwbare energie verbruik

### Should Have (Sprint 2):
3. ⭐⭐⭐⭐ **84575NED** - Energiebalans
4. ⭐⭐⭐⭐ **70846ned** - Import/Export elektriciteit
5. ⭐⭐⭐ **82380NED** - Energieprijzen

### Nice to Have (Sprint 3):
6. ⭐⭐⭐ **83300NED** - CO2 emissies
7. ⭐⭐ **81528NED** - Huishouden verbruik

---

## 🎯 Dashboard Integratie Plan

### Tab: "🇳🇱 Nederlandse Energie"

**Sectie 1: Energiemix** (Dataset: 83989NED)
- Pie chart: Productie per bron (actueel jaar)
- Bar chart: Trend over 10 jaar
- KPI's: % Fossiel vs % Hernieuwbaar

**Sectie 2: Duurzaamheid** (Dataset: 00372ed)
- Line chart: Hernieuwbaar percentage over tijd
- Progress bar: Naar 50% doel
- Breakdown: Wind, Zon, Biomassa

**Sectie 3: Import/Export** (Dataset: 70846ned)
- Area chart: Productie vs Verbruik
- KPI: Netto import/export
- Zelfvoorziening percentage

**Sectie 4: Prijstrends** (Dataset: 82380NED, 81309NED)
- Multi-line chart: Gas & Elektriciteit prijzen
- YoY vergelijking
- Correlatie met TenneT settlement prices

---

## 📝 Notes

- Alle CBS datasets zijn **gratis** en **open data**
- **OData API** - gestandaardiseerd, makkelijk te integreren
- **JSON format** - direct bruikbaar in Python/Pandas
- Update frequentie varieert: maandelijks tot jaarlijks
- Historische data beschikbaar vanaf jaren '80/'90

---

## 🔄 Update Log

- **2026-02-13**: Initiële dataset selectie
- [ ] API client implementatie
- [ ] Dashboard integratie
