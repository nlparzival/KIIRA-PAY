# TRADEBUSINESS.md
## Autonome Energie-Arbitrage Node voor Bedrijven & Vastgoed

---

## 🎯 HET KERNIDEE

**Plug-and-play hardware (Raspberry Pi 5 + Jetson Orin) die je in de meterkast installeert en autonoom geld verdient door slim energie te kopen, opslaan en verkopen.**

### Wat Doet Het?
- Leest realtime energieverbruik via P1-poort van slimme meter
- Stuurt slimme apparaten aan via Modbus/MQTT:
  - EV-laders (laden wanneer stroom goedkoop is)
  - Thuisbatterijen (laden laag, ontladen hoog)
  - Warmtepompen (voorverwarmen bij lage prijzen)
  - Zonnepanelen (optimaal verkopen)
- Maakt automatisch arbitrage-beslissingen op basis van:
  - Day-ahead prijzen (TenneT)
  - Imbalance markt
  - Weer (Copernicus)
  - Lokaal verbruikspatroon
- **Verdient geld voor de eigenaar** door slim te laden/ontladen

---

## 💰 HET VERDIENMODEL

### Voor De Klant: Passief Inkomen
- **Geen voorinvestering**: Wij installeren de hardware
- **Geen gedoe**: Systeem werkt volledig autonoom
- **Direct zichtbare winst**: Dashboard toont dagelijks verdiende €€
- **Gemiddelde ROI**: €50-500/maand afhankelijk van setup
  - Klein appartement (EV-lader): €50-100/maand
  - Huis met batterij + EV: €150-300/maand
  - Bedrijfspand met grootverbruik: €300-1000+/maand

### Voor Ons: Micro-Fee Model (SaaS)
- **10-30% van de winst** die de node maakt
- **Recurring revenue**: Elke dag, elke node
- **Schaalbaar**: 100 nodes = 100x revenue
- **Low churn**: Hardware staat in meterkast, klant ziet passief inkomen

**Rekenvoorbeeld:**
- 1 node verdient €200/maand voor klant
- Wij nemen 20% = €40/maand
- 100 nodes = €4.000/maand recurring
- 1.000 nodes = €40.000/maand recurring
- Hardware cost: €580/node (eenmalig)
- Break-even per node: ~15 maanden

---

## 🔧 DE HARDWARE

### Basis Setup (€580)
- **Raspberry Pi 5** (8GB RAM): €80
  - Energiezuinig (5-15W)
  - Lokale processing
  - 24/7 beschikbaar
- **Jetson Orin Nano** (optioneel voor AI): €500
  - Snellere beslissingen
  - Edge AI inferencing
  - Alleen nodig bij complexe setups

### Connectiviteit
- **P1-kabel**: €15-30 (slimme meter uitlezen)
- **Modbus/MQTT gateway**: €50-100 (apparaten aansturen)
- **4G/5G backup**: €10/maand (indien geen WiFi)

### Installatie
- **Meterkast montage**: 1-2 uur
- **Software configuratie**: 30 min
- **Testing & commissioning**: 1 uur
- **Totale installatiekosten**: €150-300 (eenmalig)

---

## 📊 BUSINESSCASE

### Revenue Streams

#### 1. **Arbitrage Winst (Primair)**
**Hoe het werkt:**
- Energieprijzen variëren **10-100x per dag**
- Day-ahead markt: €0,05 - €0,50/kWh
- Negatieve prijzen: tot €-0,10/kWh (betaald om te verbruiken!)
- Imbalance markt: extra volatiliteit

**Praktijkvoorbeeld (Huis met EV + Batterij):**
- EV verbruikt 15 kWh/dag
- Zonder node: gemiddeld €0,25/kWh = €3,75/dag
- Met node: laden bij €0,10/kWh = €1,50/dag
- **Besparing: €2,25/dag = €67,50/maand**
- Bij verkoop overtollige batterijcapaciteit: +€50/maand
- **Totaal: €117,50/maand voor klant**
- **Voor ons (20%): €23,50/maand**

#### 2. **Imbalance Markt (Advanced)**
- Grid heeft continue balanceringsbehoefte
- Betaalt voor flexibiliteit (bijv. uitstellen EV-laden)
- **Extra revenue**: €20-100/maand per node

#### 3. **Dataverkoop (Optioneel)**
- Geanonimiseerd verbruikspatroon
- Verkoopbaar aan energiebedrijven, DSO's, onderzoekers
- **Extra revenue**: €5-20/maand per node

#### 4. **Virtual Power Plant (Scale)**
- Bij 100+ nodes: grid-level actor
- Aggregatie van flexibiliteit
- Hogere prijzen voor gebundelde capaciteit
- **Premium**: 5-10% hogere fee mogelijk

---

## 🎯 DE DOELGROEPEN

### Fase 1: Early Adopters (0-20 nodes)
**Profiel:**
- Tech-savvy vrienden/netwerk
- Hebben EV en/of thuisbatterij
- Interesse in passief inkomen
- Bereid om beta-tester te zijn

**Pitch:**
> "Gratis hardware installatie. Jij verdient €100-300/maand passief. Ik neem 20% van wat je verdient. Geen risico voor jou."

### Fase 2: VvE's (20-200 nodes)
**Profiel:**
- Appartementencomplexen met 10-50 units
- Collectieve laadpalen
- Interesse in verduurzaming
- Beheerder die besparingen wil aantonen

**Pitch:**
> "Installeer in elk appartement. Bewoners delen in de winst. VvE krijgt dashboard met collectieve besparingen. Installatiekosten terugverdiend in 12 maanden."

### Fase 3: Commercieel Vastgoed (200-1000 nodes)
**Profiel:**
- Kantoorpanden, hotels, winkelcentra
- Hoog energieverbruik (€5k-50k/maand)
- ESG-doelstellingen
- Facility managers met budget

**Pitch:**
> "Reduceer energiekosten met 15-30%. ROI in 8-12 maanden. Verbeter ESG-score. Geen CAPEX, alleen winstdeling."

### Fase 4: Industriële Klanten (1000+ nodes)
**Profiel:**
- Fabrieken, datacenters, logistiek
- Megawatt-schaal verbruik
- Eigen transformators
- Directe netaansluiting

**Pitch:**
> "Word grid-level actor. Verdien aan flexibiliteit. Reduceer netkosten. Enterprise SLA & support."

---

## 🚀 DE ROADMAP

### Maand 1-3: Proof of Concept
**Doel:** Aantonen dat het werkt
- [ ] Hardware bouwen (1x Pi 5 + Jetson setup)
- [ ] P1-poort koppeling testen
- [ ] EV-lader aansturen (Modbus/MQTT)
- [ ] Live data ophalen (TenneT day-ahead prijzen)
- [ ] Simpel arbitrage-algoritme (if price < threshold: charge)
- [ ] Dashboard bouwen (Streamlit/Grafana)
- [ ] **Testen bij 1-2 vrienden**
- [ ] Meten: €€ verdient per dag/week/maand

**KPI's:**
- Technische stabiliteit: >95% uptime
- Financieel: €50-150/maand besparingen aantoonbaar
- Klant feedback: "Zou je dit aanraden?" -> Yes

### Maand 4-6: Pilot Uitrol
**Doel:** Schalen naar 10-20 nodes
- [ ] Hardware inkoop (bulk discount)
- [ ] Standaard installatieproces documenteren
- [ ] Remote monitoring & updates (over-the-air)
- [ ] Customer support proces (Telegram/WhatsApp)
- [ ] Juridisch: contract template (winstdeling, liability)
- [ ] **Rekruteren 10-20 early adopters**
- [ ] A/B testen: verschillende fee % (15% vs 25%)

**KPI's:**
- 15+ actieve nodes
- Gemiddeld €100/maand winst per node
- Ons: €1.500-2.000/maand recurring revenue
- Churn: <10%

### Maand 7-12: VvE Strategie
**Doel:** Eerste VvE contract (50-100 units)
- [ ] VvE pitch deck & ROI calculator
- [ ] Referentiecase (testimonials pilots)
- [ ] Collectieve dashboard (gebouw-niveau)
- [ ] Installatie logistiek (1 dag, 10 units)
- [ ] Partnership met installateurs
- [ ] **Eerste VvE deal sluiten**

**KPI's:**
- 1-3 VvE's getekend
- 100+ actieve nodes
- €8.000-10.000/maand recurring revenue
- NPS > 50

### Jaar 2: Commerciële Schaalgroei
**Doel:** 500-1000 nodes, break-even
- [ ] Sales team (2-3 FTE)
- [ ] Partnerships: vastgoedbeheerders, energiebedrijven
- [ ] Enterprise features: SLA, dedicated support, white-label
- [ ] Marketing: case studies, SEO, LinkedIn ads
- [ ] Virtual Power Plant: aggregatie layer
- [ ] **Revenue target: €40k-80k/maand**

---

## 🔌 DE TECHNIEK (Praktisch)

### Wat De Node Doet (Stap-voor-Stap)

**Elke 15 minuten:**
1. **Lees P1-poort**: Actueel verbruik (kW), totaal verbruik (kWh)
2. **Haal prijzen op**: TenneT API (day-ahead, imbalance)
3. **Check weer**: Copernicus (komende 6-24u zon/wind)
4. **Check apparaten**: Status EV (batterij %), thuisbatterij (SoC %), warmtepomp (temp)
5. **Bereken optimale actie**:
   - Als prijs < €0,10/kWh EN EV < 80%: Start laden
   - Als prijs > €0,30/kWh EN batterij > 80%: Ontladen naar grid
   - Als zon verwacht EN batterij < 50%: Niet verkopen (wachten op zon)
6. **Stuur commando**: Modbus/MQTT naar EV-lader of batterij-inverter
7. **Log data**: Supabase (actie, prijs, winst)
8. **Update dashboard**: Realtime metrics

**Elke dag (00:00):**
- Bereken totale winst van gisteren
- Stuur notificatie naar klant: "Vandaag €4,50 verdiend! 🎉"
- Log naar admin dashboard (ons)

### Software Stack
- **OS**: Raspberry Pi OS (Debian)
- **Runtime**: Python 3.11+
- **Key libraries**:
  - `pymodbus` (Modbus communicatie)
  - `paho-mqtt` (MQTT voor smart devices)
  - `requests` (API calls TenneT etc.)
  - `pandas` (data processing)
  - `dsmr-parser` (P1-poort parsing)
- **Database**: SQLite lokaal + Supabase cloud backup
- **Dashboard**: Streamlit (voor klant) + Grafana (voor ons)
- **Updates**: GitHub Actions -> OTA updates

### Hardware Integratie

#### P1-Poort (Slimme Meter)
```python
# Uitlezen slimme meter (DSMR 5.0)
from dsmr_parser import telegram_specifications
from dsmr_parser.clients import SerialReader

serial_reader = SerialReader(
    device='/dev/ttyUSB0',
    serial_settings={'baudrate': 115200},
    telegram_specification=telegram_specifications.V5
)

for telegram in serial_reader.read():
    current_usage = telegram.CURRENT_ELECTRICITY_USAGE.value  # kW
    total_usage = telegram.ELECTRICITY_USED_TARIFF_1.value    # kWh
    print(f"Actueel verbruik: {current_usage} kW")
```

#### EV-Lader (Modbus)
```python
# Aansturen EV-lader (bijv. Wallbox Commander)
from pymodbus.client import ModbusTcpClient

client = ModbusTcpClient('192.168.1.50')  # IP van lader
client.connect()

# Start laden met 16A (3.7 kW)
client.write_register(5004, 16, unit=1)
print("EV laden gestart")

# Stop laden
client.write_register(5004, 0, unit=1)
print("EV laden gestopt")
```

#### Thuisbatterij (MQTT)
```python
# Aansturen thuisbatterij (bijv. Tesla Powerwall)
import paho.mqtt.client as mqtt

client = mqtt.Client()
client.connect("192.168.1.60", 1883)

# Laden starten
client.publish("battery/charge", "start")

# Ontladen naar grid
client.publish("battery/discharge", "3000")  # 3 kW
```

---

## 📈 FINANCIËLE PROJECTIE

### Cost Structure (Per Node)

**Eenmalig:**
- Hardware: €580 (Pi 5 + Jetson)
- Installatie: €200 (arbeid + materiaal)
- **Totaal CAPEX: €780**

**Maandelijks (Per Node):**
- 4G/5G data: €10 (optioneel)
- Cloud storage (Supabase): €0,50
- Support (geamortiseerd): €5
- **Totaal OPEX: €15,50/maand**

### Revenue (Per Node)

**Conservatief scenario:**
- Klant verdient: €100/maand
- Onze fee (20%): €20/maand
- OPEX: €15,50
- **Netto marge: €4,50/maand/node**
- Break-even: 174 maanden ❌ (Te lang!)

**Realistisch scenario:**
- Klant verdient: €200/maand
- Onze fee (20%): €40/maand
- OPEX: €15,50
- **Netto marge: €24,50/maand/node**
- Break-even: 32 maanden (~3 jaar) ⚠️

**Optimistisch scenario:**
- Klant verdient: €400/maand (commercieel vastgoed)
- Onze fee (25%): €100/maand
- OPEX: €15,50
- **Netto marge: €84,50/maand/node**
- Break-even: 9 maanden ✅

### Business Model Optimalisatie

**Optie 1: Verhoog Fee**
- 30% i.p.v. 20% (klant verdient nog steeds €140/maand)
- Netto marge: €44,50/maand
- Break-even: 17 maanden

**Optie 2: Hardware Lease**
- Klant betaalt €50/maand lease (vast)
- Wij behouden fee op winst (20%)
- Snellere CAPEX recovery
- **Aanbevolen voor commercieel vastgoed**

**Optie 3: Freemium**
- Basis features: gratis (5% fee)
- Advanced features: €20/maand + 15% fee
- Virtual Power Plant: €50/maand + 10% fee

---

## 🎯 GO-TO-MARKET STRATEGIE

### Fase 1: Direct Netwerk (Maand 1-6)
**Kanaal:** Persoonlijk netwerk, vrienden, familie
**Boodschap:** "Help me testen, jij verdient gratis geld"
**Investering:** €0
**Target:** 10-20 nodes

### Fase 2: VvE's via Partners (Maand 6-12)
**Kanaal:** VvE-beheerders, installateurs, duurzaamheidsadvies
**Boodschap:** "Bewezen besparingen, geef jouw klanten passief inkomen"
**Investering:** €5k (marketing materiaal, demo setup)
**Target:** 100+ nodes

### Fase 3: B2B Sales (Jaar 2)
**Kanaal:** LinkedIn, cold outreach, beurzen, partnerships
**Boodschap:** "Reduceer energiekosten 20-30%, ROI <12 maanden"
**Investering:** €50k (sales team, marketing)
**Target:** 500-1000 nodes

### Fase 4: Platform Play (Jaar 3+)
**Kanaal:** API, white-label, partnerships met utilities
**Boodschap:** "Plug into our Virtual Power Plant"
**Investering:** €200k+ (platform development, compliance)
**Target:** 5000+ nodes

---

## ⚖️ JURIDISCH & COMPLIANCE

### Energie Handel
- **Vraag:** Mogen wij zonder vergunning energie terugleveren?
- **Antwoord:** Ja, tot 10 kW (kleinverbruik regeling)
- **Boven 10 kW:** Vergunning nodig van ACM
- **Onze strategie:** Start <10 kW, schaal via aggregatie

### Liability
- **Vraag:** Wie is aansprakelijk bij schade (bijv. brand)?
- **Contract clause:** "Node op eigen risico, wij niet aansprakelijk voor hardware defecten"
- **Verzekering:** Aansprakelijkheidsverzekering (€500/jaar)

### GDPR (Privacy)
- **Data verzameld:** Verbruik per 15 min, geen persoonlijke data
- **Opt-out:** Klant kan data-sharing uitschakelen (alleen arbitrage)
- **Storage:** EU servers (Supabase Frankfurt)

### Garantie
- **Hardware:** 1 jaar fabrieksgarantie (Pi/Jetson)
- **Software:** Best-effort support, geen SLA (beta fase)
- **Uptime:** Streven 95%, geen garantie

---

## 🚧 RISICO'S & MITIGATIE

### Technisch
**Risico:** Hardware faalt, node offline
**Mitigatie:** 
- Monitoring (Grafana alerts)
- Auto-restart (systemd)
- Remote toegang (SSH VPN)
- Warranty replacement binnen 48u

**Risico:** API's onbeschikbaar (TenneT downtime)
**Mitigatie:**
- Fallback naar cached data
- Conservatieve default strategie (niet handelen)

### Financieel
**Risico:** Energieprijzen stabiliseren (minder arbitrage kansen)
**Mitigatie:**
- Diversificatie: imbalance, demand response, dataverkoop
- Contract aanpassing: minimale fee + variabel

**Risico:** Break-even duurt te lang (32 maanden)
**Mitigatie:**
- Focus op high-value klanten eerst (commercieel)
- Hardware lease model (snellere cash flow)
- Verhoog fee naar 25-30%

### Markt
**Risico:** Grote spelers (Eneco, Vattenfall) lanceren zelfde dienst
**Mitigatie:**
- First-mover advantage: netwerk effects
- Focus op niche: VvE's, MKB (niet retail)
- Flexibeler & goedkoper (geen legacy)

**Risico:** Regulering verandert (subsidies wegvallen)
**Mitigatie:**
- Arbitrage werkt zonder subsidie
- Lobby via branche-organisatie
- Pivot naar B2B (minder afhankelijk van retail subsidies)

---

## 📞 KLANT SUPPORT & SUCCESS

### Onboarding (Eerste Week)
- Dag 0: Installatie (2-3 uur op locatie)
- Dag 1: Test run (monitoring samen met klant)
- Dag 3: Check-in call (alles werkend?)
- Dag 7: Eerste winst-rapportage (€€ dashboard)

### Ongoing Support
- **Dashboard:** 24/7 toegang via app/web
- **Notifications:** Dagelijkse winst-update (push notificatie)
- **Support kanaal:** WhatsApp/Telegram groep (response <24u)
- **Maandelijkse rapportage:** PDF met totaal verdiend, trends, tips

### Churn Preventie
- **Quarterly Business Review:** "Hoe kunnen we meer voor je verdienen?"
- **Referral bonus:** €50 per nieuwe klant die zij aanbrengen
- **Community:** Slack/Discord met andere klanten (best practices)

---

## 🎯 SUCCESS METRICS (KPI's)

### Product Metrics
- **Uptime:** >95% (gemiddeld per node)
- **Arbitrage winst:** €100-400/maand per node
- **Response tijd:** <15 min (van prijswijziging tot actie)
- **Forecast accuracy:** >70% (prijs voorspelling 6u vooruit)

### Business Metrics
- **MRR (Monthly Recurring Revenue):** €40k target @ 1000 nodes
- **CAC (Customer Acquisition Cost):** <€200
- **LTV (Lifetime Value):** >€2000 (5+ jaar gemiddeld)
- **LTV/CAC ratio:** >10x
- **Churn:** <5% per jaar
- **NPS (Net Promoter Score):** >50

### Operational Metrics
- **Install time:** <3 uur per node
- **Support tickets:** <2 per node per maand
- **Resolution time:** <24u
- **Remote fix rate:** >80% (geen on-site nodig)

---

## 🌍 LONG-TERM VISIE (5-10 Jaar)

### Virtual Power Plant (VPP)
**Bij 1000+ nodes:**
- Totaal vermogen: 5-10 MW flexibiliteit
- Grid-level actor (TSO/DSO contracts)
- Frequentie regulatie diensten
- **Extra revenue:** €50-200/node/maand

### White-Label Platform
**Verkoop aan:**
- Energiebedrijven (Eneco, Essent)
- Installateurs (SolarEdge, Wallbox)
- Vastgoedbeheerders

**Model:** €10k setup fee + €5/node/maand licentie

### Internationale Expansie
**Landen met hoge prijsvolatiliteit:**
- Duitsland (veel wind, veel variatie)
- UK (island grid, veel arbitrage)
- Scandinavië (hydro + wind)
- Australië (veel zon, duur net)

**Strategie:** Partner met lokale installateurs, zelfde software

### Exit Scenario's
1. **Acquisitie door energiebedrijf:** €50-100M (bij 5000+ nodes)
2. **Acquisitie door tech/IoT speler:** €30-50M (Schneider, Siemens)
3. **IPO:** Bij €20M+ ARR, mature markt
4. **Cash cow:** Blijf independent, €5-10M/jaar winst

---

## ✅ NEXT STEPS (Deze Week!)

### Dag 1-2: Hardware Setup
- [ ] Bestel Pi 5 + Jetson Orin (€580)
- [ ] Bestel P1-kabel (€25)
- [ ] Bestel Modbus gateway (€80) OF test met WiFi smart plug

### Dag 3-4: Software Proof of Concept
- [ ] Python script: P1-poort uitlezen
- [ ] Python script: TenneT API ophalen (day-ahead prijzen)
- [ ] Python script: Simpele logica (if price < €0,15: print "CHARGE")
- [ ] Test met dummy data (geen echte actie)

### Dag 5-7: Live Test
- [ ] Koppel aan eigen slimme meter (P1)
- [ ] Koppel aan WiFi smart plug (als EV-lader simulatie)
- [ ] Laat 1 week draaien
- [ ] Meet: Hoeveel € had ik kunnen besparen?

### Week 2: Dashboard + Eerste Klant
- [ ] Streamlit dashboard (basis)
- [ ] Benader 2-3 vrienden met EV
- [ ] Doe gratis pilot (2 weken)
- [ ] Verzamel feedback

### Week 3-4: Iterate & Scale
- [ ] Fix bugs uit pilot
- [ ] Documenteer installatieproces
- [ ] Maak pitch deck (1-pager voor klanten)
- [ ] Zoek 5 meer beta-testers

---

## 💡 WAAROM DIT GAAT WERKEN

### Timing is Perfect
- **EV adoptie:** 2026 is het kantelpunt (>20% van nieuwe auto's)
- **Thuisbatterijen:** Prijs gedaald 70% sinds 2020
- **Energieprijzen:** Volatiliteit blijft door hernieuwbaar (wind/zon)
- **Regulering:** NL stimuleert flexibiliteit (SDE++, saldering afbouw)

### Unique Value Proposition
- **Voor klant:** Verdien geld terwijl je slaapt, geen gedoe
- **Voor ons:** Recurring revenue, moeilijk te kopiëren (hardware + lokaal)
- **Voor grid:** Helpt stabiliseren, vermijdt netuitbreiding

### Competitive Moat
1. **First-mover:** Nog geen directe concurrenten op deze schaal
2. **Network effects:** Meer nodes = betere collectieve strategie
3. **Data:** Unique verbruiksdata = waardevoller algoritme
4. **Switching cost:** Eenmaal geïnstalleerd, waarom wisselen?

### Minimal Downside
- **Pilot kost:** €1500-2000 (3 nodes)
- **Tijd investering:** 40-80 uur (2-4 weken part-time)
- **Als het niet werkt:** Hardware doorverkopen, geleerde lessen meenemen
- **Als het WEL werkt:** €10k-100k+ MRR binnen 12-24 maanden

---

## 🚀 CONCLUSIE

**Dit is GEEN AlphaZero mega-AI project.**
**Dit is NIET een platform voor alle energie-assets.**

**Dit IS:**
- Een simpele, praktische hardware-box
- Die je in een meterkast hangt
- En autonoom geld verdient
- Door slim energie te kopen/verkopen
- Met een SaaS micro-fee model
- Schaalbaar van 10 naar 10.000 nodes

**Het enige wat we hoeven te bewijzen:**
> "Deze box verdient €100-400/maand voor de eigenaar, betrouwbaar en autonoom."

Als dat lukt, is de rest sales & executie.

**LET'S BUILD IT! 🔥**

---

*Versie 1.0 - 12 februari 2026*
*Status: Ready to execute*
