# Digitale Euro & ECB - Kennisdocument
**Europese Centrale Bank CBDC Implementatie**

> **Status:** Living Document - Research Based  
> **Laatste Update:** 11 februari 2026  
> **Bron:** Officiële ECB documentatie en publicaties

---

## 📋 Executive Summary

De Digitale Euro is een **Central Bank Digital Currency (CBDC)** - digitaal centraal bankgeld voor retailbetalingen - uitgegeven door de Europese Centrale Bank. Het is **GEEN** cryptocurrency, maar een digitale vorm van contant geld, gedekt door de ECB.

**Cruciale Kenmerken voor Project Aurelius:**
- ✅ **Niet programmeerbaar** - De Digitale Euro is "dom" geld (geen smart contracts)
- ✅ **Offline functionaliteit** - Werkt zonder internetverbinding
- ✅ **Privacy** - ECB kan niet zien wie wat koopt
- ✅ **Gratis** - Geen kosten voor gebruikers
- ✅ **Holding limits** - Maximum bedrag per wallet (financiële stabiliteit)
- ✅ **Bank intermediaries** - Banken blijven de distributiekanalen

**Dit is precies waarom Aurelius nodig is:** De Digitale Euro mist de intelligentie die agents nodig hebben. Wij bouwen die laag.

---

## 🗓️ Timeline & Status (Stand: Februari 2026)

### Historisch Overzicht

**September 2020:** Eurosystem High-Level Task Force start experimenteel werk

**Oktober 2021 - Oktober 2023:** Investigation Phase
- Prototyping exercises
- Marktparticipanten onderzoek
- Focus groups met burgers
- Technische design keuzes

**November 2023 - Oktober 2025:** Preparation Phase
- Finaliseren Digital Euro Rulebook
- Selectie van platform providers
- Ontwikkeling infrastructuur

**Oktober 2025:** Governing Council besluit om door te gaan naar volgende fase

**November 2025:** Current Phase begint
- Focus op: Technical readiness
- Focus op: Market engagement  
- Focus op: Legislative support

### Toekomst

**2026:** EU wetgeving wordt verwacht
- Digital Euro Regulation moet door Europees Parlement
- Implementatie van juridisch kader
- Finale technische specificaties

**2029:** **Target date voor eerste uitgifte** (eerste issuance)
- Aanname: EU wetgeving wordt in 2026 goedgekeurd
- Technische readiness moet compleet zijn
- Markt moet voorbereid zijn

---

## 🏗️ Architectuur & Technische Kenmerken

### De "Domme" CBDC - Waarom Aurelius Nodig Is

**Wat de Digitale Euro NIET is:**
- ❌ Geen programmeerbaar geld (geen smart contracts)
- ❌ Geen cryptocurrency (volledig gecentraliseerd)
- ❌ Geen blockchain per se (technologie nog niet definitief)
- ❌ Geen AI-capabilities
- ❌ Geen gedelegeerde besluitvorming
- ❌ Geen context-aware logica

**Wat de Digitale Euro WEL is:**
- ✅ Digitaal equivalent van cash
- ✅ Altijd nominale waarde (€1 = €1)
- ✅ Backed by ECB (risicovrij)
- ✅ Onbeperkt bruikbaar (zoals cash, geen restricties op gebruik)

**ECB's eigen woorden:**
> "The digital euro would never become programmable money though. Programmable money is digital money used for a restricted purpose or duration, like a voucher. By contrast, the digital euro will be unrestricted and always maintain its value – just like cash. We don't want the digital euro to come with any constraints on where, when or with whom people and business could use it."

**Dit is de gap die Aurelius vult:**
- Digitale Euro = "Dom" transport medium (zoals glasvezel)
- Aurelius Gateway = Intelligente orchestratielaag (zoals IP-protocol)
- Agents = Applicaties die de intelligentie gebruiken

---

### Online vs. Offline Betalingen

#### Online Payments
**Mechanisme:**
1. Gebruiker heeft Digital Euro wallet bij bank of intermediair
2. Betaling gaat via backend infrastructuur
3. Settlement gebeurt real-time op ECB systemen
4. Banken/intermediaries faciliteren de transactie

**Voor Aurelius:**
- API-integratie met bank intermediaries
- Real-time settlement verification
- Cryptografische bewijzen van transacties
- Audit trail voor compliance

#### Offline Payments
**Mechanisme:**
1. Digital Euro wordt lokaal opgeslagen op device (phone, card)
2. Peer-to-peer transacties zonder internet
3. Privacy vergelijkbaar met cash (geen centrale tracking)
4. Later synchronisatie met backend bij reconnect

**Voor Aurelius:**
- Agents moeten offline transactions kunnen verwerken
- Delayed settlement reconciliation
- Conflictresolutie bij dubbele uitgaven
- Hardware security module (HSM) integratie voor keys

**Privacy Implicatie:**
- ECB ziet bij offline transacties **niets** totdat device resynchroniseert
- Voor Aurelius: Escrow mechanisms moeten hiermee omgaan

---

### Holding Limits (Wallet Limieten)

**Het Probleem:**
Als iedereen onbeperkt Digital Euro's kan houden, vluchten deposito's uit banken → financiële instabiliteit.

**De Oplossing:**
ECB stelt een **maximum bedrag** per wallet in (bedrag nog niet publiek).

**Mechanisme:**
```
IF wallet_balance > holding_limit:
    THEN overschot wordt automatisch:
        - Teruggestort naar gekoppeld bankaccount
        - OF transactie wordt geweigerd
        - OF "waterfall" naar andere accounts

Gebruikers kunnen meer betalen door:
    - Wallet te linken aan bankrekening
    - Meerdere transacties (onder limiet)
```

**Voor Aurelius:**
- Agents moeten rekening houden met holding limits
- Automatische fund management (sweep naar bankrekening)
- Split payments als transactie > wallet limit
- Optimization: Minimaliseer aantal Digital Euro conversies

**Strategische Impact:**
- Digitale Euro is voor **betalingen**, niet voor **sparen**
- Dit maakt Aurelius' liquiditeitsmanagement cruciaal
- Agents moeten slim "parkeren" van geld regelen

---

### Conditional Payments (Limited Functionality)

**Wat ECB toestaat:**
- ✅ Recurring payments (huurbetalingen, abonnementen)
- ✅ Pay-on-delivery (betaling bij levering)
- ✅ Pay-per-use (betalen naar gebruik)
- ✅ Milestone-based payments (betaling bij mijlpalen)

**Wat ECB NIET toestaat:**
- ❌ Programmable money (restricties op gebruik)
- ❌ Expiring money (geld met houdbaarheidsdatum)
- ❌ Conditional money (alleen besteedbaar bij X)

**Voor Aurelius:**
Dit is **PERFECT** voor ons. Wij bouwen de intelligentie rond "domme" conditional payments:

```
ECB conditional payment:
  "Pay €50 IF delivery confirmed"

Aurelius orchestration:
  1. Agent monitort delivery status (IoT sensor)
  2. Cryptografische proof van levering
  3. Agent triggert ECB conditional payment
  4. Governance check (was leverancier legit?)
  5. Audit trail voor compliance
  6. Learning: Update betrouwbaarheidsscore leverancier
```

**We wrappen ECB's simpele conditionals in intelligente besluitvorming.**

---

## 🔐 Privacy & Data Protection

### ECB's Privacy Garanties

**Wat ECB NIET kan zien:**
- ❌ Wie je bent (bij individuele transactie)
- ❌ Wat je koopt
- ❌ Waar je bent
- ❌ Met wie je handelt

**Wat ECB WEL kan zien (geaggregeerd):**
- ✅ Totale transactievolumes
- ✅ Macroeconomische trends
- ✅ Systemic risk indicators

**Privacy Levels:**

**Level 1: Offline Payments**
- Privacy = Cash equivalent
- Geen centrale database entry
- Alleen device-to-device transfer
- ECB ziet niets totdat resync

**Level 2: Online Small Payments**
- Pseudonymisatie
- ECB ziet transactie, niet identiteit
- Banken/intermediaries weten wie je bent (KYC)

**Level 3: Large Payments**
- Enhanced Due Diligence (AML/CTF)
- Volledige traceability voor toezichthouders
- Drempelwaarde: Waarschijnlijk €10,000+ (EU norm)

### Implicaties voor Aurelius

**Voordeel:**
- Wij kunnen meer privacy bieden dan banken (ons doel is niet data-mining)
- Agent-to-agent transacties blijven pseudoniem

**Uitdaging:**
- Wij moeten compliance garanderen zonder privacy te schenden
- Zero-Knowledge Proofs zijn cruciaal
- "Proof of Compliance" zonder "Disclosure of Transaction Details"

**Ons Concurrentievoordeel:**
- Banken willen je data (business model)
- ECB wil geen data (mandate is stabiliteit)
- Aurelius = Privacy-preserving orchestrator (als neutraal platform)

---

## 🏦 Rol van Banken & Intermediaries

### Twee-Laags Model

**Laag 1: ECB (Wholesale)**
- Geeft Digital Euro uit
- Beheert settlement systeem
- Garandeert backing
- Handhaaft monetair beleid

**Laag 2: Banken & PSP's (Retail)**
- Distribueren Digital Euro aan burgers
- Bieden wallet services
- Doen KYC/AML checks
- Bieden klantenservice

**Aurelius positie:** Wij zijn een **Laag 3** - Application/Orchestration Layer
```
Laag 1: ECB (Monetary Authority)
    ↓
Laag 2: Banken (Distribution & Compliance)
    ↓
Laag 3: AURELIUS (Intelligence & Automation)
    ↓
Laag 4: Agents (Execution)
```

### Intermediary Types

**Type 1: Banken**
- Bestaande relaties met klanten
- Volledige KYC/AML capabilities
- Kunnen Digital Euro wallets aan bestaande accounts koppelen

**Type 2: Payment Service Providers (PSP's)**
- Fintechs, betaaldiensten
- Moeten licensed zijn (PSD2/PSD3)
- Kunnen Digital Euro accepteren/distribueren

**Type 3: Public Intermediaries**
- ECB overweegt publieke wallet optie
- Voor financial inclusion (mensen zonder bankrekening)
- Basis functionaliteit, gratis

**Aurelius strategie:**
- Partner met **Type 2** (PSP's) voor onboarding
- Integreer met **Type 1** (Banken) voor bestaande klanten
- Mogelijk: Zelf **Type 2** licentie aanvragen voor directe toegang

---

## 💰 Kosten & Economics

### Voor Eindgebruikers

**Gratis:**
- ✅ Digital Euro wallets (basis)
- ✅ Betalingen doen
- ✅ Betalingen ontvangen
- ✅ Peer-to-peer transfers
- ✅ Online en offline transacties

**Mogelijk betaald (door banken bepaald):**
- ⚠️ Premium wallet features
- ⚠️ Integration met andere diensten
- ⚠️ Cross-border (buiten Eurozone)

### Voor Banken

**ECB Schatting: €4 miljard tot €5.8 miljard** totaal voor Eurozone bankensector

**Kostenposten:**
- IT infrastructuur updates
- Wallet systemen
- Compliance systemen (AML/CTF)
- Klantenservice training
- Legacy system integratie

**Shared Infrastructure:**
- ECB stimuleert dat banken infrastructuur delen
- Lagere kosten door synergieën
- Standardisatie vermindert duplicatie

**Voor Aurelius:**
- Wij kunnen een deel van deze kosten overnemen (SaaS model)
- Banken betalen ons voor agent-orchestration services
- Revenue model: Fee per transactie (klein, maar schaalbaar)

---

## 🌍 Pan-European Acceptance

### De Interoperabiliteitsuitdaging

**Huidige situatie:**
- 13 van 20 Eurozone landen afhankelijk van internationale kaartschema's (Visa/Mastercard)
- Geen Europese digitale betaaloplossing die hele Eurozone dekt
- Fragmentatie per land (iDEAL Nederland, Giropay Duitsland, etc.)

**Digital Euro oplossing:**
- ✅ Werkt in alle 20 Eurozone landen
- ✅ Elke merchant die digitale betalingen accepteert, MOET Digital Euro accepteren (wettelijk verplicht, naar verwachting)
- ✅ Geen cross-border fees binnen Eurozone

**Voor Aurelius:**
- **Massive opportunity:** Wij worden de orchestrator voor 343 miljoen mensen
- Één integratie = toegang tot hele markt
- Network effects: Hoe meer agents, hoe waardevoller het netwerk

---

## ⚖️ Juridisch & Regulatory Framework

### Verwachte Wetgeving (2026)

**Digital Euro Regulation (proposal verwacht):**

**Pillar 1: Legal Tender Status**
- Digital Euro wordt wettelijk betaalmiddel
- Merchants MOETEN accepteren (zoals cash)
- Uitzonderingen mogelijk (heel kleine bedrijven)

**Pillar 2: Privacy & Data Protection**
- GDPR compliance verplicht
- Data minimalisatie principes
- ECB mag geen persoonsgegevens verzamelen

**Pillar 3: Financial Stability**
- Holding limits (zie eerder)
- Conversie regels (Digital Euro ↔ bankgeld)
- Kapitaalvereisten voor intermediaries

**Pillar 4: AML/CTF**
- KYC bij wallet opening
- Transaction monitoring voor grote bedragen
- Suspicious Activity Reports (SAR's)

**Pillar 5: Competition & Innovation**
- Open access voor licensed PSP's
- API standards voor third-party developers
- Anti-monopoly provisions (voorkomen dat Big Tech domineert)

### Implicaties voor Aurelius

**Voordeel:**
- **Pillar 5** geeft ons legale ruimte om te innoveren
- API standards = wij kunnen integreren
- Anti-monopoly = ECB wil diversity (wij zijn die diversity)

**Compliance vereist:**
- Wij moeten PSP-licentie hebben (of via partner)
- AML/CTF systemen zijn must-have
- Audit trails voor toezichthouder
- Data protection officer (GDPR)

**Strategische Positie:**
- Wij zijn geen concurrent van banken (Laag 2)
- Wij zijn geen concurrent van ECB (Laag 1)
- Wij zijn enabler van nieuwe use cases (Laag 3)
- Dit maakt ons politiek acceptabel

---

## 🏛️ Governance & Besluitvorming

### Wie Beslist Over de Digital Euro?

**Level 1: ECB Governing Council**
- 6 Executive Board members
- 20 Governors van nationale centrale banken
- Besluit over monetair beleid en uitgave

**Level 2: Europees Parlement & Raad**
- Stellen wetgeving vast (Digital Euro Regulation)
- Democratische legitimiteit
- Kunnen ECB mandaat aanpassen

**Level 3: Eurosystem (ECB + NCB's)**
- Implementatie en operationele beslissingen
- Technische standaarden
- Day-to-day management

**Level 4: Nationale toezichthouders**
- AFM (Nederland), BaFin (Duitsland), etc.
- Handhaven regels voor intermediaries
- Lokale compliance

### Stakeholder Input

**ECB heeft geconsulteerd met:**
- ✅ 343 miljoen Eurozone burgers (surveys, focus groups)
- ✅ Banken en PSP's (industry consultations)
- ✅ Merchants en retailers (acceptance requirements)
- ✅ Tech companies (infrastructure providers)
- ✅ Privacy advocates (civil society)
- ✅ Academici en economen (research input)

**Aurelius strategie:**
- **Wij moeten in deze stakeholder-dialoog**
- Positie: "We are the innovation layer that ECB needs but cannot build"
- Target: Piero Cipollone (Executive Board member voor Digital Euro)
- Forum: ECB Innovation Platform (wij moeten participant worden)

---

## 🚧 Risks & Limitations (Vanuit ECB Perspectief)

### Risk 1: Financial Stability

**Scenario:** "Digital Euro Rush"
- Mensen verplaatsen massaal deposits van banken naar Digital Euro
- Banken verliezen funding
- Credit crunch (banken kunnen niet meer lenen)
- Economische krimp

**ECB's Mitigatie:**
- Holding limits (zie eerder)
- Remuneration policy (Digital Euro krijgt 0% rente, ontmoedigt sparen)
- Waterfall mechanisms (overschot gaat automatisch terug naar bank)

**ECB's Analyse:**
> "The use of the digital euro for day-to-day payments would not harm financial stability – even under a highly unlikely and extreme crisis scenario worse than any real crisis during the first 25 years of the euro."

**Voor Aurelius:**
- Dit is geen risico voor ons (wij faciliteren betalingen, niet sparen)
- Wij helpen zelfs (agents houden geen grote balances, maar doen veel kleine transacties)

---

### Risk 2: Privacy vs. AML Conflict

**De Spanning:**
- Burgers willen privacy (zoals cash)
- Toezichthouders willen transparantie (AML/CTF)
- Hoe balanceer je dit?

**ECB's Aanpak:**
- Tiered privacy (kleine betalingen = meer privacy)
- Threshold-based monitoring (alleen grote bedragen worden gescreened)
- Pseudonymization (niet anoniem, maar niet direct identificeerbaar)

**Voor Aurelius:**
- Wij kunnen deze spanning verlichten met Zero-Knowledge Proofs
- "Proof of Compliance" zonder "Disclosure of Data"
- Concurrentievoordeel: Privacy-preserving compliance

---

### Risk 3: Technological Lock-in

**Scenario:**
- ECB kiest specifieke technologie (bijv. DLT variant)
- Later blijkt dit suboptimaal
- Migratie is duur en complex

**ECB's Mitigatie:**
- Technology-agnostic design
- Modular architecture
- Open standards (niet vendor lock-in)
- Iterative approach (niet big bang)

**Voor Aurelius:**
- **Voordeel:** Onze orchestratielaag is technologie-agnostisch
- Wij kunnen werken met elke onderliggende CBDC technologie
- Wij zijn niet "married" to one tech stack

---

### Risk 4: Low Adoption

**Scenario:**
- Mensen blijven liever gewoon bankapps gebruiken
- Merchants zien geen meerwaarde
- Digital Euro wordt "flop"

**ECB's Mitigatie:**
- Legal tender status (merchants moeten accepteren)
- Free for users (geen fee-barrière)
- Better than existing solutions (offline, privacy, pan-European)

**Voor Aurelius:**
- **Dit is PRECIES waarom wij nodig zijn**
- Zonder killer apps blijft Digital Euro inderdaad "meh"
- Wij bouwen de killer apps (autonomous energy trading, M2M payments, IoT orchestration)
- Wij maken Digital Euro relevant door use cases die anders niet mogelijk zijn

---

## 🔬 Technical Experiments & Prototypes

### ECB Experimentation Work (2020-2023)

**Prototypes gebouwd:**

**Prototype 1: Offline Payment Device**
- NFC-based peer-to-peer transfers
- Cryptographic security zonder online connection
- Battery-powered, card-factor

**Prototype 2: E-commerce Integration**
- API voor online merchants
- Instant settlement
- Fraud prevention mechanisms

**Prototype 3: Cross-border Payments**
- Integration met andere CBDC's (experimental)
- Atomic swaps (Digital Euro ↔ Other CBDC)
- Settlement finality

**Prototype 4: Conditional Payments**
- Smart triggers (pay-on-delivery, etc.)
- Escrow mechanisms
- Dispute resolution

### Innovation Platform

**ECB heeft Innovation Platform** waar private partijen kunnen experimenteren.

**Participants tot nu toe:**
- Banks (ABN AMRO, ING, Deutsche Bank, etc.)
- Tech companies (Amazon, Google Pay, Apple Pay)
- Fintechs (diverse startups)

**Voor Aurelius:**
- **WIJ MOETEN HIERAAN DEELNEMEN**
- Geeft ons:
  - Early access tot specs
  - Directe lijn met ECB
  - Legitimiteit als innovator
  - Test environment voor prototypes
- Action item: Apply voor Innovation Platform membership

---

## 📊 Market Sizing & Opportunity

### Eurozone Retail Payments (2025 data)

**Totale retail betalingen per jaar:** ~150 miljard transacties

**Verdeling:**
- Cash: 40% (dalend)
- Kaarten (debit/credit): 45%
- Bank transfers: 10%
- Andere (PayPal, etc.): 5%

**Gemiddelde transactiewaarde:**
- Cash: €12
- Kaarten: €38
- Bank transfers: €1,200

**Digital Euro Potential:**
- ECB verwacht 25-40% van retail payments binnen 5 jaar na launch
- **37.5-60 miljard transacties per jaar**
- Bij €0.001 fee per transactie = €37.5M - €60M markt (alleen voor gateway fees)

**Aurelius Opportunity:**
Niet in volume payments (te competitief), maar in **high-value orchestration**:
- M2M payments (IoT devices): Kleine transacties, enorme volume
- Conditional payments: Complexiteit = marge
- Cross-agent settlements: Vertrouwen = waarde
- Compliance-as-a-Service: Banken betalen voor onze governance layer

**Target: 5% van Digital Euro-enabled transactions via Aurelius agents = €1.9M - €3M fees/year (conservatief)**

**Schaaleffect:** Bij 1% van Eurozone huishoudens (1.5M agents) × €200/year orchestration value = **€300M jaarlijkse waarde**

---

## 🎯 Strategic Implications voor Project Aurelius

### Threat Analysis

**Threat 1: ECB bouwt zelf een orchestratielaag**
- Likelihood: Low
- ECB focus is infrastructuur, niet applicaties
- Precedent: Internet (overheid bouwde TCP/IP, niet apps)
- Mitigatie: Wij positioneren als **complementary**, niet concurrent

**Threat 2: Big Tech neemt deze ruimte in (Apple Pay, Google Pay)**
- Likelihood: Medium-High
- Zij hebben distribution (miljarden users)
- Zij hebben geld (R&D budgets)
- Mitigatie: 
  - Wij focussen op B2B en M2M (niet hun terrein)
  - Wij zijn privacy-first (hun zwakte)
  - Wij zijn regulated entity (vertrouwen)

**Threat 3: Banken bouwen eigen agent-platforms**
- Likelihood: Medium
- Zij hebben klanten en compliance
- Zij hebben legacy infrastructuur (advantage en nadeel)
- Mitigatie:
  - Wij zijn technology partner VAN banken
  - White-label onze oplossing
  - Focus op waar zij zwak zijn (IoT, M2M, AI-orchestration)

### Opportunity Analysis

**Opportunity 1: Early Mover Advantage**
- Digital Euro launch is 2029
- Wij kunnen 2027-2028 pilots doen
- Network effects = winner-takes-most

**Opportunity 2: Regulatory Arbitrage (legaal)**
- ECB wil diversity in ecosystem
- Anti-monopoly mandaat betekent ruimte voor ons
- Wij kunnen dingen doen die banken niet mogen/kunnen

**Opportunity 3: EU Green Deal Synergy**
- Energie is prioriteit (onze pilot!)
- Sustainability credentials (ESG)
- Politieke steun (klimaatdoelen)

---

## 🗺️ Go-to-Market Roadmap (Aurelius × Digital Euro)

### Phase 0: Preparation (Nu - Q4 2026)

**Acties:**
1. Apply voor ECB Innovation Platform membership
2. Build relationshipSmet Piero Cipollone's team
3. Partner met één PSP voor Digital Euro access
4. Ontwikkel proof-of-concept met testnet
5. Legal: Obtain PSP license (of via partner)

### Phase 1: Pilot (Q1 2027 - Q4 2027)

**Energie pilot in Nederland:**
- 100 huishoudens in Utrecht
- Digital Euro testnet access (ECB sandbox)
- Partner: Liander (netbeheerder) + ING (bank)
- Metrics: Transaction volume, latency, user satisfaction

**Success criteria:**
- 10,000+ transactions executed
- <100ms latency (gateway overhead)
- 0 security incidents
- Positive user feedback (>70% satisfaction)

### Phase 2: Scale (2028)

**Als Digital Euro regulation is aangenomen:**
- Scale pilot to 10,000 huishoudens
- Expand to 3 cities (Utrecht, Amsterdam, Rotterdam)
- Add use cases (EV charging, solar trading)
- Partnerships met 5+ energy providers

### Phase 3: Launch (2029+)

**Concurrent met Digital Euro launch:**
- Aurelius Gateway live in productie
- Target: 100,000 agents in eerste jaar
- Expand beyond energy (logistics, IoT, healthcare)
- International expansion (andere Eurozone landen)

---

## 📚 Key ECB Publications (Must-Read)

**Foundational Documents:**
1. **Digital Euro Rulebook** (Expected 2026) - De bijbel voor implementatie
2. **Investigation Phase Report** (Oct 2023) - Design choices & rationale
3. **Financial Stability Impact Assessment** (2025) - Risks & mitigations

**Technical Specifications:**
4. **Digital Euro API Standards** (TBD) - Hoe developers integreren
5. **Offline Payment Protocol** (TBD) - Cryptographic specs
6. **Conditional Payments Specification** (TBD) - Smart triggers

**Stakeholder Engagement:**
7. **Fit in Payment Ecosystem Report** (Oct 2025) - Hoe Digital Euro co-exists met bestaande oplossingen
8. **Investment Costs Analysis** (Oct 2025) - Kosten voor banken

**Regular Updates:**
- Monthly: ECB Press Conferences (Lagarde & Cipollone)
- Quarterly: ECON Committee updates (European Parliament)
- Ad-hoc: Publications op ecb.europa.eu/euro/digital_euro

---

## 🔗 Kritieke Contacten & Stakeholders

### ECB Digital Euro Team

**Piero Cipollone**
- Executive Board Member
- Verantwoordelijk voor Digital Euro project
- Target voor strategic engagement

**Evelien Witlox**
- Digital Euro Project Head
- Operational lead
- Key contact voor Innovation Platform

### European Commission

**DG FISMA** (Directorate-General for Financial Stability, Financial Services and Capital Markets Union)
- Schrijft Digital Euro Regulation
- Target voor policy input

### National Central Banks

**De Nederlandsche Bank (DNB)**
- Dutch implementation
- Partner voor Nederland-pilot

### European Parliament

**ECON Committee** (Economic and Monetary Affairs)
- Oversight over ECB
- Democratic accountability
- Target voor transparency & legitimiteit

---

## 🚨 Critical Unknowns (Nog Te Bepalen)

**Open Vragen die Aurelius' Architectuur Beïnvloeden:**

1. **Holding Limit:** Wat is het exacte bedrag?
   - Impact op onze liquidity management
   - Bepaalt hoe vaak agents moeten "sweepen"

2. **API Specifications:** Welke endpoints krijgen we?
   - RESTful? gRPC? GraphQL?
   - Authentication mechanisms (OAuth2? mTLS?)
   - Rate limits en throttling

3. **Offline Payment Reconciliation:** Hoe werkt conflict resolution?
   - Wat als twee devices verschillende versies claimen?
   - Double-spending prevention mechanisme
   - Timing van resynchronization

4. **Conditional Payment Limits:** Welke soorten conditionals zijn toegestaan?
   - Time-based? Event-based? Multi-signature?
   - Complexity limits (gas equivalent?)

5. **Cross-border (non-Eurozone):** Werkt Digital Euro met andere CBDC's?
   - mBridge protocol? Other standards?
   - Exchange rate mechanisms
   - Settlement finality

6. **Fee Structure:** Mag Aurelius fees charged over Digital Euro transacties?
   - ECB zegt "gratis voor users", maar intermediaries?
   - B2B vs B2C distinction
   - Compliance fees (AML/CTF diensten)

---

## 💡 Aurelius Unique Value Proposition (vs Digital Euro Alone)

**Digital Euro geeft ons:**
- ✅ Infrastructure (rails)
- ✅ Legitimiteit (ECB backing)
- ✅ Pan-European reach
- ✅ Zero settlement risk

**Aurelius voegt toe:**
- 🚀 **Intelligence:** Context-aware besluitvorming (Deontic Logic)
- 🚀 **Autonomy:** Agents die 24/7 opereren zonder menselijke input
- 🚀 **Governance:** Compliance-as-Code (Kaufmann filters, AML automation)
- 🚀 **Orchestration:** Complexe multi-party workflows
- 🚀 **Antifragility:** Systeem dat leert van failures (Evolutionary Immune)
- 🚀 **Privacy:** Zero-Knowledge Proofs voor confidential transactions

**Elevator Pitch:**
> "Digital Euro is zoals HTTP - essentieel, maar basaal. Aurelius is zoals het hele web - de applicatielaag die het interessant maakt. ECB bouwt de snelweg, wij bouwen de zelfrijdende auto's die erop rijden."

---

## ✅ Action Items voor Aurelius Team

**Immediate (Q1 2026):**
- [ ] Apply ECB Innovation Platform membership
- [ ] Contact Evelien Witlox's team voor exploratory meeting
- [ ] Research PSP licensing requirements (PSD2/PSD3)
- [ ] Join ECB Digital Euro stakeholder consultations

**Short-term (Q2-Q3 2026):**
- [ ] Build prototype met Digital Euro sandbox (als beschikbaar)
- [ ] Partner identification: Welke bank/PSP wordt onze intermediary?
- [ ] Legal entity setup: Waar vestig je Aurelius? (Netherlands? Luxembourg?)
- [ ] Fundraising: Investeerders interested in "CBDC infrastructure layer"

**Medium-term (Q4 2026 - 2027):**
- [ ] Pilot design met Liander/TenneT (energie use case)
- [ ] Technical integration met Digital Euro testnet
- [ ] Regulatory approval voor pilot (AFM/DNB)
- [ ] Team scaling (hiring engineers, compliance officers)

**Long-term (2028+):**
- [ ] Production launch concurrent met Digital Euro
- [ ] Geographic expansion (Germany, France, Italy)
- [ ] Vertical expansion (logistics, healthcare, beyond energy)
- [ ] Strategic partnerships (Big Tech? Banks? Both?)

---

## 📖 Glossary

**CBDC:** Central Bank Digital Currency - Digitaal geld uitgegeven door centrale bank

**PSP:** Payment Service Provider - Licensed partij die betaaldiensten mag aanbieden

**PSD2/PSD3:** Payment Services Directive - EU wetgeving voor betaaldiensten

**eIDAS:** Electronic Identification and Trust Services - EU framework voor digitale identiteit

**KYC:** Know Your Customer - Identificatie van klanten (AML vereiste)

**AML/CTF:** Anti-Money Laundering / Counter-Terrorism Financing

**ECON:** European Parliament Committee on Economic and Monetary Affairs

**NCB:** National Central Bank (bijv. DNB voor Nederland)

**DLT:** Distributed Ledger Technology (blockchain, etc.)

**mTLS:** Mutual Transport Layer Security - Cryptografisch authenticatie protocol

**TEE:** Trusted Execution Environment - Hardware-backed secure computing

---

**Dit document wordt bijgewerkt naarmate ECB meer informatie publiceert. Check regelmatig voor updates.**

---

**Laatste bronnen geraadpleegd:**
- ecb.europa.eu/euro/digital_euro (11 feb 2026)
- ECB Governing Council Decision (Oct 2025)
- Latest publications: Feb 2026
