# Energy Arbitrage Node - Ground Zero Use Case
**Project Aurelius - First Vertical**

> **Status:** Pilot Ready  
> **Laatste Update:** 11 februari 2026  
> **Doel:** Technische + economische + juridische blauwdruk voor eerste use case

---

## 🎯 Executive Summary

**The Pitch:**
> "We turn your home battery into a revenue-generating asset. Earn €500-1,000/year by automatically buying low, selling high, and stabilizing the grid—all while you sleep."

**Why Energy is Ground Zero:**
1. **Measurable:** kWh, Watt, Hz = objective metrics
2. **Urgent:** Nederland heeft €40 miljard netcongestie-probleem
3. **Legal:** EU Green Deal + CSRD vereisen innovatie
4. **Economic:** Clear ROI (payback <2 jaar)
5. **Scalable:** Same tech works for EV, industrial batteries, etc.

**The Physics:**
- Dutch grid frequency = 50.00 Hz (target)
- Deviation = ±0.2 Hz (normal)
- >0.5 Hz = grid instability → blackout risk
- Our agents detect deviations in **<10ms** and respond in **<100ms**

**The Economics:**
- Household battery: 10 kWh (€5,000 investment)
- Arbitrage revenue: €800/year
- Grid stability bonus: €200/year
- Total: **€1,000/year = 20% ROI**

**The Market:**
- 1.5M Dutch households with solar panels
- 200k have batteries (growing 50%/year)
- TAM: €200M/year (energy arbitrage alone)

---

## ⚡ The Technical Architecture

### Hardware Stack

```
[Physical Layer]
├── Solar Panels (existing)
│   └── DC output → Inverter
├── Home Battery (existing)
│   ├── Tesla Powerwall (13.5 kWh)
│   ├── Sonnen Eco (10 kWh)
│   ├── LG Chem RESU (9.8 kWh)
│   └── Enphase IQ Battery (10 kWh)
├── Smart Meter (P1 port)
│   └── DSMR 5.0 (Dutch standard)
├── Aurelius Edge Gateway (new)
│   ├── Raspberry Pi 4 or Industrial IoT device
│   ├── Local HSM chip (TPM 2.0)
│   ├── 4G/5G modem (fallback connectivity)
│   └── LoRaWAN radio (mesh network)
└── Grid Connection
    └── Monitored by DSO (Stedin, Liander)
```

---

### Software Stack

```
[Agent Intelligence - Cloud]
├── Aurelius Gateway (central)
│   ├── Market Data Feed (real-time prices)
│   ├── Grid Frequency Monitor (TenneT API)
│   ├── Weather Forecast (solar production prediction)
│   └── Decision Engine (RL algorithm)
├── Digital Euro Account (agent's wallet)
└── eIDAS Wallet (signing keys in HSM)

[Agent Intelligence - Edge]
├── Local Controller (on Raspberry Pi)
│   ├── Battery State Monitor (SoC, SoH)
│   ├── Solar Production Monitor (real-time)
│   ├── Load Monitor (household consumption)
│   ├── Safety Controller (circuit breakers)
│   └── Fallback Mode (if cloud disconnected)
└── Communication
    ├── MQTT (lightweight, secure)
    ├── WebSocket (real-time updates)
    └── LoRaWAN (mesh, peer-to-peer)
```

---

### Data Flows

**1. Market Opportunity Detection (Cloud → Edge)**

```
[Step 1: Market Scan]
TenneT API → Grid Frequency = 49.85 Hz (LOW)
Price API → Spot Price = €0.30/kWh (HIGH)
Weather API → Cloud coverage increasing (solar production dropping)

[Step 2: Decision Engine]
Aurelius AI → "OPPORTUNITY: Sell battery power to grid"
Calculate:
  Revenue = 5 kWh × €0.30 = €1.50
  Battery degradation = 5 kWh × €0.02 = €0.10 (wear)
  Net = €1.40
  Decision: SELL

[Step 3: Command]
Cloud → Edge Gateway: "DISCHARGE 5kWh over 30 minutes"
Signed with eIDAS wallet (cryptographic proof)

[Step 4: Edge Execution]
Edge Gateway → Battery Inverter: "Discharge 5kW"
Monitor: Voltage, current, temperature (safety)
Fallback: If any parameter out of range → ABORT

[Step 5: Physical Action]
Battery → Grid: 5 kWh delivered
Smart Meter → Confirm: Export registered
TenneT → Grid frequency restored to 49.95 Hz ✅

[Step 6: Settlement]
Digital Euro Transfer:
  From: TenneT (grid operator)
  To: Agent EUID-001 (household battery)
  Amount: €1.50
  Clearing: <1 second
```

**Total latency: 180ms (detection → decision → payment → action)**

---

**2. Peer-to-Peer Energy Trading (Edge ↔ Edge)**

```
[Scenario: Neighbor needs power, you have surplus]

[Step 1: Neighbor's Agent Broadcasts]
Agent B → LoRaWAN mesh: "BUYING 2 kWh, willing to pay €0.25/kWh"

[Step 2: Your Agent Responds]
Agent A → Check: Battery SoC = 80% (have surplus)
Agent A → LoRaWAN mesh: "SELLING 2 kWh at €0.25/kWh"

[Step 3: Smart Contract Execution]
Aurelius Gateway → Match: Agent A ↔ Agent B
Generate transaction:
  From: Agent A (EUID-001)
  To: Agent B (EUID-002)
  Amount: 2 kWh
  Price: €0.50 (2 × €0.25)

[Step 4: Payment (Digital Euro)]
Agent B → Transfer €0.50 → Agent A
Gateway → Verify: Payment received ✅

[Step 5: Physical Delivery]
Agent A → Discharge 2 kWh to local grid
Smart Meter A → Export: +2 kWh
Smart Meter B → Import: +2 kWh
DSO → Confirm: Local balancing (no long-distance transmission)

[Step 6: Verification]
Both agents → Confirm delivery
Gateway → Update ledger (immutable proof)
```

**Why this is revolutionary:**
- No intermediary needed (peer-to-peer)
- Near-zero transmission loss (neighbors, not distant plants)
- €0.50 transaction settled in <1 second (vs. monthly billing)

---

## 💰 The Economics (Detailed)

### Revenue Streams for Agent Owner

#### 1. Energy Arbitrage (Buy Low, Sell High)

**Daily Cycle:**
```
00:00-07:00 (Night)
  Grid Price: €0.08/kWh (cheap, low demand)
  Action: CHARGE battery from grid
  Cost: 10 kWh × €0.08 = €0.80

12:00-14:00 (Noon)
  Solar: Producing 5 kWh (free)
  Battery: Already full
  Action: Sell solar directly to grid
  Revenue: 5 kWh × €0.25 = €1.25

17:00-21:00 (Evening)
  Grid Price: €0.35/kWh (expensive, peak demand)
  Action: DISCHARGE battery to grid
  Revenue: 8 kWh × €0.35 = €2.80

22:00-24:00 (Late evening)
  Grid Price: €0.12/kWh (medium)
  Action: Use remaining battery for own consumption
  Savings: 2 kWh × €0.12 = €0.24

DAILY NET REVENUE:
  Revenue: €1.25 + €2.80 + €0.24 = €4.29
  Cost: €0.80
  Net: €3.49/day × 365 days = €1,274/year
```

**Assumptions:**
- Price spread exists 80% of days (weather-dependent)
- Battery cycles: 1.5/day (within warranty limits)
- Degradation: €100/year (factored in)

**Net Revenue: €1,274 - €100 = €1,174/year**

---

#### 2. Grid Balancing Services (Frequency Response)

**How it works:**
- TenneT pays for "spinning reserve" (instant power on demand)
- Traditional: Large gas plants idle (expensive, polluting)
- Aurelius: Distributed batteries (cheap, clean)

**Payment:**
- Availability fee: €5/kW/month (for being ready)
- Activation fee: €0.50/kWh (when actually used)

**Example:**
- Battery capacity: 5 kW (can discharge at max 5kW)
- Availability: 5 kW × €5 × 12 months = €300/year
- Activation: ~10 times/month × 2 kWh × €0.50 × 12 = €120/year
- **Total: €420/year**

**Why TenneT loves this:**
- Cheaper than gas plants (€5/kW vs. €15/kW)
- Faster response (<100ms vs. 10 seconds)
- Zero emissions (vs. gas CO₂)

---

#### 3. Capacity Market (Congestion Management)

**Problem:**
- Grid operator: "This street's transformer is overloaded at 6pm"
- Traditional solution: Upgrade transformer (€500k, 2 years)
- Aurelius solution: Pay batteries to NOT charge during peak

**Payment:**
- DSO: "Don't charge 5-7pm, we'll pay you €0.10/kWh foregone"
- Agent: "OK, I'll charge at 11pm instead (when price is lower anyway)"
- Result: DSO saves €500k, agent earns €50/year extra

**Total Capacity Revenue: €50-100/year**

---

#### 4. CO₂ Certificates (Future)

**As EU carbon market tightens:**
- Avoided emissions = tradable certificates
- 1 kWh from battery (vs. grid) = ~0.5 kg CO₂ saved
- Price: €80/ton CO₂ (current ETS price)

**Example:**
- 1,000 kWh/year arbitrage = 500 kg CO₂ saved
- Value: 0.5 ton × €80 = €40/year

**Status:** Not yet implemented (waiting for regulatory clarity)

---

### Total Annual Revenue per Agent

```
Energy Arbitrage:        €1,174
Grid Balancing:          €420
Capacity Market:         €75
CO₂ Certificates:        €40 (future)
─────────────────────────────
TOTAL:                   €1,709/year
```

**Less:**
- Aurelius fees (0.1% of transactions): ~€50/year
- Subscription (Basic tier): €60/year
- Battery degradation: €100/year

**NET TO OWNER: €1,500/year**

**ROI on €5,000 battery: 30%/year** 🚀

---

## 📊 Market Analysis

### Addressable Market (Netherlands)

**Current State:**
- Households with solar: 1.5M (2026)
- Households with solar + battery: 200k (2026)
- Growth rate: 50%/year (battery adoption accelerating)

**TAM (Total Addressable Market):**
- 200k batteries × €1,500/year = **€300M/year** (current)
- 1M batteries × €1,500/year = **€1.5B/year** (2030 projection)

**SAM (Serviceable Addressable Market):**
- Assume 50% willing to try agent-based system
- SAM = **€750M/year** (2030)

**SOM (Serviceable Obtainable Market):**
- Assume we capture 20% (network effects + first-mover)
- SOM = **€150M/year** (2030)

**Aurelius Revenue (at 10% fee):**
- €150M × 10% = **€15M/year from Netherlands alone**

**European Extrapolation:**
- EU households with solar: ~15M (10x Netherlands)
- EU market for Aurelius: **€150M/year** (conservative)

---

### Competitive Landscape

**Current Players:**

| Company | Approach | Weakness |
|---------|----------|----------|
| **Sonnen** | Battery + community | Proprietary (only Sonnen batteries) |
| **Tibber** | Smart pricing app | Manual (not autonomous) |
| **Jedlix** | EV smart charging | EVs only, no batteries |
| **Powerpeers** | P2P energy trading | Pre-agreed contracts (slow) |
| **Tesla Autobidder** | Virtual Power Plant | Tesla-only, US-focused |

**Aurelius Advantages:**
1. **Hardware agnostic** (works with any battery)
2. **Fully autonomous** (zero human intervention)
3. **Legal by design** (eIDAS + EUinc compliance)
4. **Real-time settlement** (Digital Euro, not monthly billing)
5. **Pan-European** (works across all EU countries)

**Result:** We're not competing with them. We're building the infrastructure they'll use.

---

## 🔬 Technical Challenges & Solutions

### Challenge 1: Battery Degradation

**Problem:**
- Lithium batteries degrade with each charge/discharge cycle
- Typical warranty: 10 years or 3,650 cycles (1/day)
- Arbitrage requires 1.5-2 cycles/day → Exceeds warranty

**Solution: Intelligent Degradation Management**

```typescript
class BatteryHealthOptimizer {
  async decideTrade(
    opportunity: TradeOpportunity,
    battery: BatteryState
  ): Promise<boolean> {
    // Calculate degradation cost
    const degradationCost = this.calculateDegradation(
      battery.stateOfHealth,
      battery.temperature,
      opportunity.cycleDepth // Shallow cycles = less degradation
    );

    // Only trade if profit > degradation
    const netProfit = opportunity.revenue - degradationCost;

    if (netProfit > MINIMUM_PROFIT_THRESHOLD) {
      return true; // Execute trade
    }

    return false; // Skip this opportunity
  }

  private calculateDegradation(
    SoH: number,
    temp: number,
    depth: number
  ): number {
    // Based on Battery University research
    // Shallow cycles (20-80% SoC) = 0.01% degradation
    // Deep cycles (0-100% SoC) = 0.05% degradation
    // High temp (>30°C) = 2x degradation

    let baseDegradation = depth > 0.6 ? 0.05 : 0.01;
    if (temp > 30) baseDegradation *= 2;

    // Cost per % degradation = Battery Replacement Cost / 100
    const replacementCost = 5000; // €5k for 10 kWh battery
    return (baseDegradation / 100) * replacementCost;
  }
}
```

**Result:** Agent only trades when profit >> degradation. Battery lasts longer than without agent.

---

### Challenge 2: Grid Safety

**Problem:**
- If 10,000 batteries discharge simultaneously → Grid overload
- If agents misbehave → Blackout risk

**Solution: Coordinated Dispatch**

```typescript
class GridSafetyCoordinator {
  async coordinateDischarge(
    agents: Agent[],
    targetPower: number // e.g., 5 MW needed
  ): Promise<DispatchPlan> {
    // 1. Check grid constraints
    const gridCapacity = await this.dsoAPI.getCapacity();

    // 2. Distribute load
    const dispatchPlan = this.optimizeDispatch({
      agents,
      targetPower,
      constraints: [
        { type: "transformer", max: gridCapacity.transformer },
        { type: "cable", max: gridCapacity.cable },
        { type: "frequency", range: [49.8, 50.2] }
      ]
    });

    // 3. Stagger activation (avoid simultaneous surge)
    dispatchPlan.stagger(100); // 100ms intervals

    return dispatchPlan;
  }
}
```

**Result:** 10,000 agents act as one coordinated "virtual power plant", not 10,000 independent actors.

---

### Challenge 3: Communication Reliability

**Problem:**
- Internet outage = agent offline = no revenue + safety risk

**Solution: Multi-Path Communication + Local Fallback**

```
[Primary Path]
Agent → 4G/5G → Cloud → Decision → 4G/5G → Agent

[Fallback 1: LoRaWAN Mesh]
Agent → LoRaWAN → Neighbor Agent → LoRaWAN → Cloud

[Fallback 2: Local Autonomy]
If cloud unreachable for >5 minutes:
  - Switch to local mode
  - Use pre-programmed rules:
    * SoC < 20% → Charge from grid
    * SoC > 80% + Grid Frequency < 49.9 → Discharge
    * Else → Do nothing
  - Resume cloud control when connection restored
```

**Result:** 99.95% uptime (vs. 99.5% for single-path systems)

---

### Challenge 4: Cybersecurity

**Problem:**
- Hacker takes control of 10,000 batteries → Grid weapon

**Solution: Multi-Layer Security (Defense in Depth)**

```
[Layer 1: Physical]
- Edge gateway in tamper-proof enclosure
- TPM chip (hardware root of trust)

[Layer 2: Network]
- mTLS (mutual authentication)
- VPN tunnel (encrypted)
- Firewall (only specific ports open)

[Layer 3: Application]
- Every command signed with eIDAS key
- Rate limiting (max 10 commands/minute)
- Anomaly detection (unusual behavior → block)

[Layer 4: Circuit Breakers]
- Max discharge rate: 5 kW (hardware limit)
- Max daily cycles: 3 (prevent battery abuse)
- Geographic spread: Max 10% of local grid capacity

[Layer 5: Human Override]
- Owner can disable agent via mobile app
- DSO can emergency-disconnect via API
- TenneT has "kill switch" for grid-level threat
```

**Result:** Even if hacker compromises software, physical limits prevent grid damage.

---

## 🏛️ Legal & Regulatory Compliance

### Energy Market Regulations

**Elektriciteitswet 1998 (Dutch Electricity Act)**

**Key Requirement:**
- Only licensed "energy suppliers" can sell electricity

**Our Approach:**
- Agent is NOT a supplier
- Agent is a "prosumer" (producer + consumer) trading surplus
- Falls under "net metering" exemption (saldering)

**Legal Basis:**
- Article 31a: Prosumers may offset consumption with production
- EU Directive 2018/2001 (RED II): Right to self-consume and sell surplus

---

**EU Electricity Directive 2019/944**

**Key Requirement:**
- "Active customers" must be able to participate in all markets

**Our Approach:**
- Agents are "active customers" under Article 15
- Must have non-discriminatory access to:
  - Day-ahead markets ✅
  - Intraday markets ✅
  - Balancing markets ✅

**Compliance:**
- Register each agent with TenneT (Market Party ID)
- Use standard ENTSO-E protocols (IEC 61970, IEC 61968)
- Settlement via existing market mechanisms

---

### Data Protection (GDPR)

**Challenge:**
- Energy usage data = personal data (GDPR Article 4)
- Can reveal: when you're home, what appliances you use, etc.

**Our Approach:**

**1. Data Minimization (Article 5.1.c)**
- Agent only accesses aggregate data (kWh totals, not appliance-level)
- Smart meter P1 port data (legally allowed for consumer)

**2. Purpose Limitation (Article 5.1.b)**
- Data used ONLY for energy optimization
- Never sold or shared (except anonymized, aggregated for research)

**3. Privacy by Design (Article 25)**
- Edge processing (data stays local when possible)
- Encrypted in transit and at rest
- Agent owner can export/delete all data (GDPR Article 20)

**4. Consent (Article 6.1.a)**
- Clear consent form: "Agent will access your smart meter data to optimize energy trading"
- Granular controls: "Allow balancing market participation: YES/NO"

---

### Safety Standards

**EN 50549-1 (Grid Connection Requirements)**

**Key Requirements:**
- Must disconnect if grid frequency out of range (47.5-51.5 Hz)
- Must support "anti-islanding" (prevent powering dead grid)
- Must respond to DSO control signals

**Compliance:**
- Battery inverters are already EN 50549 certified (Tesla, Sonnen, etc.)
- Our agent sends commands THROUGH inverter (inherits safety features)
- Additional software layer: Double-check before any action

---

## 🧪 Pilot Program Design

### Phase 1: Proof of Concept (50 households, Q2 2026)

**Location:** Amsterdam-Noord (Overhoeks neighborhood)

**Why here:**
- High solar penetration (30% of homes)
- Modern grid (smart meters already installed)
- Tech-savvy residents (early adopters)
- Single DSO (Liander = easier coordination)

**Selection Criteria:**
- Must have solar + battery (10+ kWh)
- Must have stable internet (4G backup provided)
- Must sign participation agreement (liability, data sharing)

**Hardware Deployment:**
- Aurelius Edge Gateway: €200/unit (subsidized to €0 for pilot)
- Installation: Professional (certified electrician)
- Timeline: 2 weeks (10 homes/day)

**Monitoring:**
- Daily: Energy flows, transaction volumes, errors
- Weekly: Battery health, user satisfaction (NPS score)
- Monthly: Financial results (revenue per household)

**Success Metrics:**
- Technical: 95%+ uptime, zero safety incidents
- Economic: >€500/year revenue per household
- Regulatory: DNB/AFM approval for wider rollout

---

### Phase 2: Neighborhood Scale (200 households, Q3 2026)

**Expand to:**
- 3 additional neighborhoods (Rotterdam, Utrecht, Den Haag)
- Mix of urban/suburban (test different grid conditions)

**New Features:**
- Peer-to-peer trading (neighbor-to-neighbor)
- Capacity market participation (defer charging during peak)
- Mobile app (user dashboard, controls)

**Partnerships:**
- DSO: Stedin (Rotterdam) + Enexis (Den Haag)
- Energy supplier: Greenchoice or Vandebron (customer acquisition)
- Bank: ING or ABN (Digital Euro integration, if available)

---

### Phase 3: City Scale (2,000 households, Q4 2026)

**Full Market Test:**
- Open enrollment (anyone with battery can join)
- Multiple cities across Netherlands
- Tiered pricing (Basic/Pro/Enterprise)

**Grid Impact Study:**
- Partner with TU Delft (research collaboration)
- Measure: Grid stability, congestion reduction, CO₂ impact
- Publish results (credibility for regulatory approval)

---

## 📈 Success Stories (Projected)

### Household 1: The Retiree (Amsterdam)

**Profile:**
- Solar: 12 panels (3 kWp)
- Battery: Tesla Powerwall 2 (13.5 kWh)
- Motivation: "Extra income + climate action"

**Before Aurelius:**
- Annual solar revenue: €200 (feed-in tariff)
- Battery mostly unused (just backup for outages)

**After Aurelius (Year 1):**
- Solar revenue: €200 (same)
- Battery arbitrage: €900
- Grid balancing: €400
- **Total: €1,500 (+€1,300)**

**Quote:**
> "I didn't even know my battery could do this. It's like having a money printer in my garage, except it's helping the planet."

---

### Household 2: The Young Family (Rotterdam)

**Profile:**
- Solar: 8 panels (2 kWp)
- Battery: Sonnen Eco (10 kWh)
- EV: Tesla Model 3
- Motivation: "Optimize everything"

**Before Aurelius:**
- EV charging cost: €1,200/year (charged from grid at peak prices)
- Solar revenue: €150

**After Aurelius (Year 1):**
- EV charging cost: €600 (charged from battery during cheap hours)
- Solar revenue: €150
- Battery arbitrage: €700
- **Savings: €600 + €700 = €1,300**

**Quote:**
> "We used to worry about when to charge the car. Now the agent handles it. We save money without thinking about it."

---

### Household 3: The Small Business (Utrecht)

**Profile:**
- Bakery with large freezers (high electricity use)
- Solar: 50 panels (15 kWp)
- Battery: Industrial (50 kWh)
- Motivation: "Cut costs + resilience"

**Before Aurelius:**
- Electricity cost: €12,000/year
- Grid outage risk (spoiled food)

**After Aurelius (Year 1):**
- Electricity cost: €9,000 (self-consumption optimized)
- Battery revenue (capacity market): €2,000
- Avoided losses (backup power): €1,000
- **Net savings: €6,000/year**

**Quote:**
> "This paid for itself in 6 months. And we haven't had a single outage since. It's like having our own mini power plant."

---

## 🎯 Next Steps

### Technical Development (Q1 2026)

- [ ] Edge gateway firmware (Raspberry Pi + TPM)
- [ ] Cloud platform (Rust backend, PostgreSQL)
- [ ] Battery integration (Tesla, Sonnen, LG Chem APIs)
- [ ] Smart meter integration (DSMR P1 parser)
- [ ] Grid APIs (TenneT frequency, APX price feed)
- [ ] Mobile app (React Native, iOS + Android)

### Regulatory (Q1-Q2 2026)

- [ ] DNB Innovation Hub application
- [ ] AFM AI Act compliance docs
- [ ] TenneT Market Party registration
- [ ] Liander/Stedin pilot approval
- [ ] Privacy Impact Assessment (GDPR Article 35)

### Partnerships (Q1-Q2 2026)

- [ ] Greenchoice/Vandebron (customer acquisition)
- [ ] ING/ABN (Digital Euro integration)
- [ ] Solar installers (distribution channel)
- [ ] Battery manufacturers (OEM partnerships)

### Fundraising (Q1-Q2 2026)

- [ ] Pitch deck (15 slides)
- [ ] Financial model (5-year, detailed)
- [ ] Demo video (agent in action)
- [ ] Investor meetings (Finch, Rubio, others)
- [ ] Target: €2M seed closed by Q2 end

---

## 🔬 Research Questions (TU Delft Collaboration)

**1. Grid Stability Impact**
- Question: At what penetration level (% of homes with agents) do we measurably improve grid stability?
- Method: Simulation (PowerFactory) + real-world pilot data
- Timeline: Q3-Q4 2026

**2. Battery Degradation Models**
- Question: Can we extend battery life by optimizing trade timing?
- Method: Accelerated aging tests + field data
- Timeline: Q2-Q4 2026

**3. Market Design**
- Question: What auction mechanism maximizes social welfare (grid + agents + consumers)?
- Method: Game theory + agent-based modeling
- Timeline: Q3 2026 - Q1 2027

**4. Behavioral Economics**
- Question: How much control do users want? (Full autonomy vs. oversight)
- Method: A/B testing in pilot (different UI designs)
- Timeline: Q2-Q3 2026

---

**This is Ground Zero. This is where we prove that autonomous economic agents are not science fiction—they're the future of infrastructure.**

