# SIMULATIE-STRATEGIE
## Virtual Money Trading Simulation voor Energie-Arbitrage

---

## 🎯 HET DOEL

**Voordat we hardware uitrollen: Test alle strategieën in een simulatie met:**
- Echte historische data (TenneT prijzen, weer, etc.)
- Virtueel geld (€1000 startkapitaal)
- Meerdere agents met verschillende strategieën
- Realistische constraints (batterij limieten, EV schedules, etc.)
- Complete metrics (winst, Sharpe ratio, drawdown, etc.)

**Output:**
> "Strategie X verdient €237/maand met 89% betrouwbaarheid. Klaar voor productie."

---

## 🏗️ ARCHITECTUUR

### De Simulatie Loop

```
┌─────────────────────────────────────────────────────────────┐
│                    SIMULATION ENVIRONMENT                    │
│                                                              │
│  ┌──────────────┐      ┌──────────────┐     ┌──────────────┐│
│  │ Real Data    │      │ Virtual      │     │ Constraints  ││
│  │ - TenneT     │────▶ │ Portfolio    │◀────│ - Battery    ││
│  │ - Weather    │      │ - €1000 cash │     │ - EV schedule││
│  │ - Grid       │      │ - 10 kWh bat │     │ - Max charge ││
│  └──────────────┘      └──────────────┘     └──────────────┘│
│         │                      │                      │      │
│         ▼                      ▼                      ▼      │
│  ┌──────────────────────────────────────────────────────────┐│
│  │              AGENT STRATEGIES (meerdere)                 ││
│  │                                                          ││
│  │  Agent 1: Naive Threshold (buy < €0.15, sell > €0.25)  ││
│  │  Agent 2: ML Predictor (LSTM forecast)                  ││
│  │  Agent 3: Rule-based (if sun + low price: charge)      ││
│  │  Agent 4: Greedy (always cheapest moment)              ││
│  │  Agent 5: Risk-averse (conservative, avoid volatility) ││
│  └──────────────────────────────────────────────────────────┘│
│         │                                                     │
│         ▼                                                     │
│  ┌──────────────────────────────────────────────────────────┐│
│  │                 ACTION EXECUTOR                          ││
│  │  - Simulate buy/sell/hold                               ││
│  │  - Update virtual portfolio                             ││
│  │  - Apply transaction costs                              ││
│  │  - Enforce constraints                                  ││
│  └──────────────────────────────────────────────────────────┘│
│         │                                                     │
│         ▼                                                     │
│  ┌──────────────────────────────────────────────────────────┐│
│  │                    METRICS LOGGER                        ││
│  │  - Profit per agent per day                             ││
│  │  - Win rate, Sharpe ratio, max drawdown                 ││
│  │  - Action log (what, when, why)                         ││
│  └──────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│                      DASHBOARD                               │
│  - Realtime profit chart (per agent)                        │
│  - Leaderboard (best performing strategy)                   │
│  - Action timeline (what did agents do?)                    │
│  - Risk metrics (volatility, drawdown)                      │
└─────────────────────────────────────────────────────────────┘
```

---

## 📊 DATA SOURCES (Echte Data)

### 1. TenneT Day-Ahead Prijzen (Gratis)
**API:** `https://transparency.entsoe.eu/api`
**Data:**
- Uurprijzen (€/MWh) voor volgende dag
- Beschikbaar: 14:00 (voor volgende dag)
- Historisch: 2015-nu

**Simulatie gebruik:**
```python
# Download 1 jaar historische data
dates = pd.date_range('2025-01-01', '2025-12-31', freq='H')
prices_df = fetch_tennet_prices(dates)
# Loop door elk uur en laat agents beslissen
```

### 2. Imbalance Prijzen (TenneT)
**Data:**
- 15-min prijzen (real-time balancing)
- Veel volatieler dan day-ahead
- Extra arbitrage kansen

### 3. Weer Data (Copernicus / KNMI)
**Data:**
- Zon intensiteit (GHI - Global Horizontal Irradiance)
- Windsnelheid
- Bewolking
- Forecast 48u vooruit

**Impact:**
- Veel zon = lagere prijzen (oversupply)
- Weinig wind 's nachts = hogere prijzen
- Agents kunnen dit anticiperen

### 4. Simulatie Van Huishoudelijk Verbruik
**Profiel data (synthetisch maar realistisch):**
- Wakker worden: 07:00 (douche, koffie) → 2 kW
- Overdag: 10:00-16:00 (laag verbruik) → 0.5 kW
- Avond: 18:00-23:00 (koken, TV) → 3 kW
- Nacht: 23:00-07:00 (koelkast, standby) → 0.3 kW

**EV Rijpatroon:**
- Maandag-Vrijdag: 08:00-18:00 rijden (30 km = 6 kWh)
- Weekend: 10:00-14:00 rijden (50 km = 10 kWh)
- EV moet voor 07:00 vol zijn (constraint!)

---

## 🤖 AGENT STRATEGIEËN

### Agent 1: **Naive Threshold** (Baseline)
**Logica:**
```python
if price < 0.15:
    action = "BUY"  # Laad batterij/EV
elif price > 0.25:
    action = "SELL"  # Ontlaad batterij naar grid
else:
    action = "HOLD"
```

**Verwachting:** Werkt OK, maar mist nuance (weer, EV constraints)

---

### Agent 2: **ML Predictor** (LSTM Forecast)
**Logica:**
1. Train LSTM op historische prijzen (1 jaar data)
2. Forecast volgende 6 uur
3. Als forecast stijging > 20%: koop nu
4. Als forecast daling > 20%: verkoop nu

**Features:**
- Prijs laatste 24u
- Dag van week (zondag = goedkoper)
- Uur van dag
- Weer (zon/wind forecast)

**Verwachting:** Beste performance, maar complex

---

### Agent 3: **Rule-Based Expert System**
**Logica:**
```python
# Regel 1: Zorg dat EV vol is voor 07:00
if time == "05:00" and ev_battery < 80%:
    action = "CHARGE_EV" (override prijs)

# Regel 2: Zon + lage prijs = koop
if sun_forecast > 500 W/m² and price < 0.20:
    action = "BUY"

# Regel 3: Windstil + avond = duur, verkoop
if wind < 3 m/s and hour in [18,19,20,21]:
    action = "SELL"

# Regel 4: Batterij vol + hoge prijs = verkoop
if battery > 90% and price > 0.30:
    action = "SELL"
```

**Verwachting:** Solide, interpreteerbaar, geen training nodig

---

### Agent 4: **Greedy Optimizer**
**Logica:**
1. Kijk naar day-ahead prijzen (24u vooruit)
2. Sorteer uren: goedkoopst → duurst
3. Koop in goedkoopste 4 uren
4. Verkoop in duurste 4 uren

**Constraint:** Respecteer EV schema (moet vol zijn 's ochtends)

**Verwachting:** Theoretisch optimaal, maar geen rekening met onzekerheid

---

### Agent 5: **Risk-Averse Conservative**
**Logica:**
- Alleen handelen bij **extreme** prijzen (<€0.10 of >€0.35)
- Houd altijd 50% batterij reserve (safety buffer)
- Verkoop nooit alles (voor noodgeval)
- Max 2 trades per dag (minimale transactiekosten)

**Verwachting:** Laagste winst, maar ook laagste risico (Sharpe ratio test)

---

## 💰 VIRTUAL PORTFOLIO

### Startcondities (Realistisch Huishouden)
```python
portfolio = {
    "cash": 1000,  # Virtueel startkapitaal (voor admin)
    "battery": {
        "capacity_kwh": 10,  # Thuisbatterij
        "current_soc": 50,   # State of Charge (%)
        "max_charge_kw": 3,  # Max 3 kW laden
        "max_discharge_kw": 3,
        "efficiency": 0.90   # 90% round-trip efficiency
    },
    "ev": {
        "capacity_kwh": 60,  # Nissan Leaf
        "current_soc": 80,
        "max_charge_kw": 7,  # 32A 1-fase
        "daily_usage_kwh": 6,  # 30 km/dag
        "must_be_full_by": "07:00"
    },
    "solar_panels": {
        "capacity_kwp": 5,   # 5 kWp (optioneel)
        "enabled": True
    }
}
```

### Acties & Kosten
```python
actions = {
    "BUY": {
        "effect": "battery.soc += kwh",
        "cost": "price_per_kwh * kwh + €0.01 transactie",
        "constraint": "battery.soc <= 100%"
    },
    "SELL": {
        "effect": "battery.soc -= kwh",
        "revenue": "price_per_kwh * kwh - €0.01 transactie",
        "constraint": "battery.soc >= 20% (reserve)"
    },
    "CHARGE_EV": {
        "effect": "ev.soc += kwh",
        "cost": "price_per_kwh * kwh",
        "constraint": "ev.soc <= 100%, max 7 kW"
    },
    "SOLAR_SELF_USE": {
        "effect": "Reduce grid draw",
        "revenue": "Avoided cost (no buy from grid)"
    },
    "SOLAR_SELL": {
        "effect": "Sell excess solar",
        "revenue": "price_per_kwh * kwh (often low)"
    }
}
```

---

## 📈 METRICS & KPI's

### Per Agent, Per Dag:
```python
metrics = {
    # Financieel
    "total_profit_eur": 0.0,
    "daily_profit_eur": [],
    "cumulative_profit_eur": [],
    "avg_profit_per_month": 0.0,
    
    # Risk metrics
    "sharpe_ratio": 0.0,  # Return / volatility
    "max_drawdown_eur": 0.0,  # Grootste verlies periode
    "win_rate": 0.0,  # % dagen met winst
    "profit_factor": 0.0,  # Total wins / total losses
    
    # Operationeel
    "total_trades": 0,
    "avg_trades_per_day": 0.0,
    "transaction_costs_eur": 0.0,
    "battery_cycles": 0,  # Slijtage metric
    
    # Constraint violations
    "ev_not_ready_count": 0,  # Hoe vaak was EV niet vol 's ochtends
    "battery_overdischarge_count": 0,
    
    # Strategie specifiek
    "actions_log": [
        {"timestamp": "2025-06-15 14:00", "action": "BUY", "kwh": 5, "price": 0.12, "reason": "Low price"}
    ]
}
```

### Leaderboard Metrics
```python
leaderboard = {
    "Agent 2 (ML Predictor)": {
        "rank": 1,
        "total_profit": 287.50,
        "sharpe_ratio": 1.8,
        "win_rate": 73%
    },
    "Agent 3 (Rule-based)": {
        "rank": 2,
        "total_profit": 245.00,
        "sharpe_ratio": 2.1,  # Lagere volatiliteit!
        "win_rate": 68%
    },
    # ... etc
}
```

---

## 🛠️ IMPLEMENTATIE

### Tech Stack
```python
# Core
- Python 3.11+
- pandas (data handling)
- numpy (math)

# ML (voor Agent 2)
- PyTorch / TensorFlow (LSTM)
- scikit-learn (metrics)

# Data
- requests (API calls)
- sqlite3 (local cache)

# Visualization
- Streamlit (dashboard)
- plotly (interactive charts)
- matplotlib/seaborn (static charts)

# Backtesting
- backtrader (optional, trading framework)
- vectorbt (optional, fast backtesting)
```

### Project Structure
```
/kiira-pay/simulation/
├── data/
│   ├── tennet_prices.csv      # Downloaded historical data
│   ├── weather_data.csv
│   └── household_profile.csv
├── agents/
│   ├── base_agent.py          # Abstract base class
│   ├── naive_threshold.py
│   ├── ml_predictor.py
│   ├── rule_based.py
│   ├── greedy_optimizer.py
│   └── risk_averse.py
├── environment/
│   ├── portfolio.py           # Virtual battery/EV/cash
│   ├── market.py              # Price engine
│   ├── constraints.py         # EV schedule, battery limits
│   └── simulator.py           # Main simulation loop
├── metrics/
│   ├── calculator.py          # Profit, Sharpe, drawdown
│   └── logger.py              # Action logging
├── dashboard/
│   └── app.py                 # Streamlit dashboard
├── notebooks/
│   └── exploration.ipynb      # Data analysis
├── config.py                  # Settings
├── main.py                    # Run simulation
└── requirements.txt
```

---

## 🚀 MVP SIMULATION (Week 1-2)

### Stap 1: Data Verzamelen (Dag 1-2)
```python
# scripts/download_data.py
import requests
import pandas as pd

def download_tennet_prices(start_date, end_date):
    """Download 1 jaar day-ahead prijzen"""
    url = "https://transparency.entsoe.eu/api"
    params = {
        "documentType": "A44",  # Day-ahead prices
        "in_Domain": "10YNL----------L",  # Nederland
        "out_Domain": "10YNL----------L",
        "periodStart": start_date,
        "periodEnd": end_date
    }
    # API call + parse XML
    df = parse_tennet_response(response)
    df.to_csv("data/tennet_prices.csv")
    return df

# Download 2025 data (vol jaar)
prices = download_tennet_prices("20250101", "20251231")
print(f"Downloaded {len(prices)} hours of price data")
```

### Stap 2: Simpele Agent Bouwen (Dag 3-4)
```python
# agents/naive_threshold.py
class NaiveThresholdAgent:
    def __init__(self, buy_threshold=0.15, sell_threshold=0.25):
        self.buy_threshold = buy_threshold
        self.sell_threshold = sell_threshold
    
    def decide(self, state):
        """
        state = {
            'price': 0.18,  # €/kWh
            'battery_soc': 50,  # %
            'ev_soc': 80,
            'hour': 14
        }
        """
        if state['price'] < self.buy_threshold:
            return {"action": "BUY", "kwh": 3}  # Max charge
        elif state['price'] > self.sell_threshold:
            return {"action": "SELL", "kwh": 2}  # Partial discharge
        else:
            return {"action": "HOLD", "kwh": 0}
```

### Stap 3: Simulator (Dag 5-7)
```python
# environment/simulator.py
class EnergySimulator:
    def __init__(self, agents, start_date, end_date):
        self.agents = agents
        self.data = load_price_data(start_date, end_date)
        self.portfolios = {agent.name: Portfolio() for agent in agents}
        self.metrics = {agent.name: Metrics() for agent in agents}
    
    def run(self):
        """Run simulation hour-by-hour"""
        for timestamp, row in self.data.iterrows():
            state = {
                'price': row['price_eur_kwh'],
                'hour': timestamp.hour,
                'day_of_week': timestamp.dayofweek
            }
            
            # Each agent makes decision
            for agent in self.agents:
                portfolio = self.portfolios[agent.name]
                state['battery_soc'] = portfolio.battery_soc
                state['ev_soc'] = portfolio.ev_soc
                
                # Agent decides
                action = agent.decide(state)
                
                # Execute action
                portfolio, cost = self.execute(action, state['price'])
                
                # Log metrics
                self.metrics[agent.name].log(timestamp, action, cost, portfolio)
        
        # Return results
        return self.metrics
```

### Stap 4: Run & Analyze (Dag 8)
```python
# main.py
from agents import NaiveThresholdAgent, RuleBasedAgent
from environment import EnergySimulator

# Create agents
agents = [
    NaiveThresholdAgent(name="Naive_15_25", buy=0.15, sell=0.25),
    NaiveThresholdAgent(name="Naive_10_30", buy=0.10, sell=0.30),
    RuleBasedAgent(name="RuleBased_v1"),
]

# Run simulation (1 jaar data)
sim = EnergySimulator(agents, start_date="2025-01-01", end_date="2025-12-31")
results = sim.run()

# Print results
for agent_name, metrics in results.items():
    print(f"\n{agent_name}:")
    print(f"  Total Profit: €{metrics.total_profit:.2f}")
    print(f"  Avg per month: €{metrics.avg_monthly_profit:.2f}")
    print(f"  Win rate: {metrics.win_rate:.1f}%")
    print(f"  Sharpe ratio: {metrics.sharpe_ratio:.2f}")
    print(f"  Max drawdown: €{metrics.max_drawdown:.2f}")

# Output:
# Naive_15_25:
#   Total Profit: €1,245.00
#   Avg per month: €103.75
#   Win rate: 62.0%
#   Sharpe ratio: 1.2
#   Max drawdown: €87.50
```

---

## 📊 DASHBOARD (Streamlit)

### Live Simulation View
```python
# dashboard/app.py
import streamlit as st
import plotly.express as px

st.title("🔋 Energy Arbitrage Simulation")

# Sidebar: Select agents to compare
agents_selected = st.multiselect("Select Agents", all_agents)

# Main view: Cumulative profit chart
fig = px.line(
    data,
    x='date',
    y='cumulative_profit',
    color='agent',
    title="Cumulative Profit Over Time"
)
st.plotly_chart(fig)

# Metrics row
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Profit", "€1,245", "+€23 today")
col2.metric("Win Rate", "62%", "+3%")
col3.metric("Sharpe Ratio", "1.2", "⚠️ volatiel")
col4.metric("Trades/day", "4.2", "-0.5")

# Action timeline
st.subheader("Recent Actions (Agent 2)")
st.dataframe(action_log.tail(20))

# Leaderboard
st.subheader("🏆 Leaderboard")
leaderboard_df = pd.DataFrame([
    {"Agent": "ML Predictor", "Profit": "€1,450", "Sharpe": 1.8, "Win%": "73%"},
    {"Agent": "Rule-based", "Profit": "€1,245", "Sharpe": 2.1, "Win%": "68%"},
    {"Agent": "Naive 15/25", "Profit": "€987", "Sharpe": 1.1, "Win%": "61%"},
])
st.table(leaderboard_df)
```

### Screenshot Mockup:
```
┌────────────────────────────────────────────────────────────┐
│  🔋 Energy Arbitrage Simulation                            │
├────────────────────────────────────────────────────────────┤
│  Select Agents: [x] ML Predictor  [x] Rule-based  [ ] ...  │
├────────────────────────────────────────────────────────────┤
│  📈 Cumulative Profit Over Time                            │
│     €                                                       │
│  1500┤        ╭─────ML Predictor                           │
│  1000┤     ╭──┴─────Rule-based                             │
│   500┤  ╭──┴────────Naive                                  │
│      └──────────────────────────────▶ Time                 │
├────────┬────────┬────────┬────────────────────────────────┤
│ Profit │ Win %  │ Sharpe │ Trades/day                      │
│ €1,245 │  62%   │  1.2   │    4.2                          │
│ +€23   │  +3%   │ ⚠️     │   -0.5                          │
├────────────────────────────────────────────────────────────┤
│  Recent Actions (Agent 2 - ML Predictor)                   │
│  2025-06-15 14:00  BUY   5 kWh @ €0.12  Profit: +€2.50    │
│  2025-06-15 18:00  SELL  3 kWh @ €0.28  Profit: +€3.20    │
│  2025-06-15 22:00  HOLD  -              -                  │
├────────────────────────────────────────────────────────────┤
│  🏆 Leaderboard                                            │
│  1. ML Predictor    €1,450  Sharpe: 1.8  Win: 73%         │
│  2. Rule-based      €1,245  Sharpe: 2.1  Win: 68%         │
│  3. Naive 15/25     €987    Sharpe: 1.1  Win: 61%         │
└────────────────────────────────────────────────────────────┘
```

---

## 🎯 VALIDATION CRITERIA

### Voordat We Hardware Uitrollen:

#### ✅ Minimum Viable Performance
- **Winst:** >€100/maand gemiddeld (over 1 jaar simulatie)
- **Win rate:** >60% (meer winst-dagen dan verlies-dagen)
- **Sharpe ratio:** >1.0 (risk-adjusted return OK)
- **Max drawdown:** <€200 (geen grote verliezen)
- **EV constraint violations:** 0 (EV altijd vol 's ochtends)

#### ✅ Robustness Tests
- **Verschillende jaren:** Test 2023, 2024, 2025 data (consistent?)
- **Extreme events:** Winter storm (hoge prijzen), zonnige zomer (lage prijzen)
- **Parameter sensitivity:** Wat als batterij 5 kWh i.p.v. 10 kWh?
- **Transaction costs:** Wat als kosten 2x hoger? (stress test)

#### ✅ Best Strategy Selection
- **Winner:** Agent met hoogste Sharpe ratio (niet alleen profit!)
- **Backup:** Agent met laagste max drawdown (voor risk-averse klanten)
- **Hybrid:** Combinatie van meerdere strategieën? (ensemble)

---

## 🚀 ROADMAP

### Week 1: Data + Baseline
- [ ] Download TenneT prices (2025 vol jaar)
- [ ] Download KNMI weer data (optioneel)
- [ ] Build Naive Threshold agent
- [ ] Build simple simulator
- [ ] Run first backtest (1 agent, 1 jaar)
- [ ] **Output:** "Agent verdient €X/maand"

### Week 2: Multiple Agents + Dashboard
- [ ] Build Rule-based agent
- [ ] Build Greedy optimizer agent
- [ ] Add constraint checking (EV, battery)
- [ ] Add metrics calculator (Sharpe, drawdown)
- [ ] Build Streamlit dashboard (basic)
- [ ] **Output:** Leaderboard + comparison

### Week 3: ML Agent (Optioneel)
- [ ] Feature engineering (price patterns)
- [ ] Train LSTM (forecast next 6h)
- [ ] Integrate ML agent in simulator
- [ ] Compare vs rule-based
- [ ] **Output:** "ML is X% beter/slechter"

### Week 4: Validation + Productize
- [ ] Robustness tests (verschillende jaren)
- [ ] Parameter tuning (optimal thresholds)
- [ ] Select best strategy
- [ ] Export winning strategy to Pi 5 code
- [ ] **Output:** Production-ready agent code

---

## 💡 WAAROM DIT CRUCIAAL IS

### 1. **De-risk Hardware Uitrol**
> "We weten dat strategie X €150/maand verdient voordat we €10k in hardware stoppen"

### 2. **Pitch Material**
> "Kijk, hier is de simulatie. Over 2025 had je €1,450 verdiend. Wil je dit in productie?"

### 3. **Continuous Improvement**
> "Elke maand nieuwe data → retrain → deploy betere agent"

### 4. **A/B Testing**
> "Helft van nodes draait strategie A, helft strategie B. Meten welke beter is."

### 5. **Risk Management**
> "Max drawdown €200 = klant verliest max €200 in slechtste scenario. Acceptabel?"

---

## 🔥 NEXT STEPS (Deze Week!)

### Optie A: Quick & Dirty (2-3 dagen)
```python
# 1. Download 1 maand TenneT data (gratis)
prices = download_tennet("2025-06-01", "2025-06-30")

# 2. Hardcode simpele agent
def simple_strategy(price):
    if price < 0.15:
        return "BUY"
    elif price > 0.25:
        return "SELL"
    else:
        return "HOLD"

# 3. Loop door elke dag
profit = 0
for timestamp, price in prices.iterrows():
    action = simple_strategy(price)
    if action == "BUY":
        profit -= price * 5  # Koop 5 kWh
    elif action == "SELL":
        profit += price * 5  # Verkoop 5 kWh

print(f"1 maand profit: €{profit:.2f}")
# Expected output: €30-80 (depends on month)
```

### Optie B: Proper Setup (1-2 weken)
- Volledige simulator met portfolio, constraints, metrics
- 3-5 agents met verschillende strategieën
- Streamlit dashboard
- 1 jaar backtest
- Production-ready code

---

**Wat wil je eerst doen?**
1. **Quick PoC** (2 dagen, snel resultaat)?
2. **Proper simulator** (2 weken, solide basis)?
3. **Ik schrijf de code** (main.py + agents)?

Zeg het maar! 🚀
