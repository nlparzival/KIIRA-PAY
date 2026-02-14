# 🛠️ MVP Tech Stack & Infrastructure

**Datum:** 12 februari 2026  
**Constraint:** MacBook only (geen cloud GPUs)  
**Goal:** Monolithic agent + dashboard + metrics + backend

---

## 💻 **HARDWARE REALITY CHECK**

### **MacBook Specs (Aannames):**
```yaml
Scenario A: M1/M2/M3 MacBook Pro
  CPU: 8-10 cores (Apple Silicon)
  GPU: 14-38 cores (Metal)
  RAM: 16-32 GB
  Neural Engine: 16 cores (AI acceleration)
  
  Training capability:
    ✅ Small models (< 10M parameters): OK
    ✅ Medium models (10-50M parameters): Slow but doable
    ❌ Large models (> 50M parameters): Too slow
  
  Reality: 
    - PyTorch has MPS (Metal Performance Shaders) backend
    - Can train models 5-10x faster than CPU-only
    - BUT: Still 50-100x slower than cloud GPUs (A100/H100)

Scenario B: Intel MacBook
  CPU: 4-8 cores (Intel)
  GPU: Intel Iris or AMD Radeon
  RAM: 16-32 GB
  
  Training capability:
    ⚠️ CPU-only training (slow!)
    ⚠️ No good GPU acceleration
    ❌ Not recommended for deep learning
```

### **Training Time Estimates (M2 MacBook Pro):**
```python
# Minimal Battery Agent
model_size = 100k parameters
training_data = 1 week (168 hours)
training_time = 2-4 hours  # ✅ Totally feasible

# Small Multi-Asset Agent  
model_size = 1M parameters
training_data = 1 year (8760 hours)
training_time = 1-2 days  # ✅ Doable

# Medium Multi-Asset Agent
model_size = 10M parameters
training_data = 3 years (26k hours)
training_time = 1-2 weeks  # ⚠️ Long but OK

# Large Multi-Asset Agent (AlphaZero-style)
model_size = 50M parameters
training_data = 3 years + self-play
training_time = 1-3 months  # ❌ Too slow, need cloud
```

**Conclusion:** Voor MVP blijven we bij **small-to-medium models** (< 5M parameters)

---

## 🏗️ **TECH STACK PROPOSAL**

### **Option A: Supabase-Centric (Your Suggestion)**

```
┌─────────────────────────────────────────────────────────┐
│                    FRONTEND                             │
│  Next.js + React + TypeScript + TailwindCSS            │
│  - Dashboard UI                                         │
│  - Real-time metrics (via Supabase Realtime)          │
│  - Charts: Recharts or Chart.js                        │
└─────────────────────────────────────────────────────────┘
                         ↕ HTTP/WebSocket
┌─────────────────────────────────────────────────────────┐
│                   SUPABASE                              │
│  ┌─────────────────────────────────────────────────┐   │
│  │  PostgreSQL Database                            │   │
│  │  - Time-series data (prices, weather, etc.)    │   │
│  │  - Agent decisions (actions, rewards)          │   │
│  │  - Training metrics (loss, accuracy)           │   │
│  │  - User accounts, API keys                     │   │
│  └─────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────┐   │
│  │  Edge Functions (Deno/TypeScript)               │   │
│  │  - Data ingestion (ENTSO-E, TenneT, etc.)     │   │
│  │  - Scheduled jobs (daily data pulls)           │   │
│  │  - API endpoints (agent queries)                │   │
│  └─────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────┐   │
│  │  Realtime (WebSocket)                           │   │
│  │  - Live metrics streaming                       │   │
│  │  - Agent decision updates                       │   │
│  └─────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────┐   │
│  │  Storage (S3-compatible)                        │   │
│  │  - Trained models (.pth files)                  │   │
│  │  - Historical data dumps                        │   │
│  │  - Training checkpoints                         │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
                         ↕ Python SDK
┌─────────────────────────────────────────────────────────┐
│                 AGENT TRAINING (Local)                  │
│  Python + PyTorch + MPS (Metal)                        │
│  - Agent neural network                                 │
│  - MCTS (Monte Carlo Tree Search)                      │
│  - Self-play training loop                             │
│  - Running on YOUR MacBook                             │
└─────────────────────────────────────────────────────────┘
```

#### **✅ PROS:**
```yaml
Supabase Benefits:
  ✅ PostgreSQL (excellent for time-series with TimescaleDB extension)
  ✅ Realtime updates (WebSocket out-of-box)
  ✅ Edge Functions (serverless data ingestion)
  ✅ Authentication (built-in)
  ✅ Storage (model artifacts)
  ✅ Free tier (500 MB database, 2 GB storage, 50k edge function invocations)
  ✅ Easy to scale later (just upgrade plan)
  ✅ Good Python SDK (supabase-py)
  ✅ Row-level security (if we add multi-tenancy later)
```

#### **❌ CONS:**
```yaml
Supabase Limitations:
  ⚠️ Edge Functions are Deno (not Python) → data pipelines in TS/JS
  ⚠️ No built-in job scheduler (need external cron or pg_cron extension)
  ⚠️ PostgreSQL not optimized for heavy time-series (but TimescaleDB helps)
  ⚠️ Free tier limits (500 MB = ~1 year of hourly data max)
  ⚠️ Edge function timeout (default 60s, max 150s)
```

---

### **Option B: Python-Native Stack (My Suggestion)**

```
┌─────────────────────────────────────────────────────────┐
│                    FRONTEND                             │
│  Streamlit (Python) or Gradio                          │
│  - Built-in dashboard components                        │
│  - Real-time metrics (native Python)                   │
│  - Charts: Plotly, Altair                              │
│  - Runs locally or deploy to Streamlit Cloud (free)   │
└─────────────────────────────────────────────────────────┘
                         ↕ Python API
┌─────────────────────────────────────────────────────────┐
│                  BACKEND (FastAPI)                      │
│  - REST API endpoints                                   │
│  - Agent inference (real-time decisions)               │
│  - Data ingestion pipelines                            │
│  - Background tasks (APScheduler)                      │
└─────────────────────────────────────────────────────────┘
                         ↕ SQLAlchemy ORM
┌─────────────────────────────────────────────────────────┐
│                 DATABASE (PostgreSQL)                   │
│  Self-hosted (Docker) or Supabase                      │
│  - TimescaleDB extension (time-series optimized)       │
│  - Agent state, decisions, metrics                     │
│  - Training history                                     │
└─────────────────────────────────────────────────────────┘
                         ↕
┌─────────────────────────────────────────────────────────┐
│            AGENT TRAINING (Same Process)                │
│  PyTorch + Python (runs on MacBook)                    │
│  - Saves models to local disk or Supabase Storage      │
│  - Logs metrics to database                            │
└─────────────────────────────────────────────────────────┘
```

#### **✅ PROS:**
```yaml
Python-Native Benefits:
  ✅ Everything in Python (agent, backend, dashboard)
  ✅ No context switching (JS ↔ Python)
  ✅ Streamlit dashboard = 100 lines of code (vs 1000+ for React)
  ✅ Built-in data viz (Plotly, Altair)
  ✅ Easy local development (no build steps)
  ✅ Fast iteration (change code → refresh browser)
  ✅ Can still use Supabase as database (supabase-py)
  ✅ APScheduler for cron jobs (no need for Edge Functions)
  ✅ Better control over data pipelines (pure Python)
```

#### **❌ CONS:**
```yaml
Python-Native Drawbacks:
  ⚠️ Streamlit less polished than Next.js (but fine for MVP)
  ⚠️ No built-in realtime (need to poll or use WebSocket manually)
  ⚠️ FastAPI + Streamlit = 2 processes (need orchestration)
  ⚠️ Deployment slightly more complex (vs Vercel for Next.js)
```

---

### **Option C: HYBRID (Best of Both)**

```
┌─────────────────────────────────────────────────────────┐
│                  FRONTEND (Streamlit)                   │
│  Python dashboard - Fast to build, easy to iterate     │
└─────────────────────────────────────────────────────────┘
                         ↕
┌─────────────────────────────────────────────────────────┐
│                DATABASE (Supabase PostgreSQL)           │
│  Managed PostgreSQL + Storage + Auth                   │
└─────────────────────────────────────────────────────────┘
                         ↕
┌─────────────────────────────────────────────────────────┐
│            AGENT TRAINING (Local Python)                │
│  PyTorch on MacBook → uploads to Supabase              │
└─────────────────────────────────────────────────────────┘
```

#### **✅ PROS:**
```yaml
Hybrid Benefits:
  ✅ Streamlit = fast dashboard development (MVP speed)
  ✅ Supabase = managed database (no DevOps)
  ✅ All Python (no JS/TS needed)
  ✅ Can migrate to Next.js later (keep Supabase)
  ✅ Best for solo developer
```

---

## 🎯 **MY RECOMMENDATION: HYBRID (Option C)**

### **Stack:**
```yaml
Frontend:
  - Streamlit (Python) ← Fast MVP dashboard
  - Deployment: Streamlit Cloud (free tier)

Backend:
  - FastAPI (Python) ← If needed later for API
  - OR: Just Streamlit + direct DB connection (simpler)

Database:
  - Supabase PostgreSQL (managed)
  - TimescaleDB extension (time-series)
  - Free tier: 500 MB (enough for MVP)

Storage:
  - Supabase Storage (model checkpoints)
  - Free tier: 1 GB

Agent Training:
  - PyTorch (Python)
  - MPS backend (Metal on MacBook)
  - Runs locally, saves to Supabase

Data Ingestion:
  - Python scripts (APScheduler for cron)
  - Run locally OR deploy to cloud later
  - Fetch ENTSO-E, TenneT, etc.

Monitoring:
  - Streamlit built-in metrics
  - Supabase dashboard (database queries)
```

---

## 📦 **PROJECT STRUCTURE**

```
KIIRA-PAY/
├── agent/                      # Agent training code
│   ├── models/
│   │   ├── neural_net.py      # PyTorch model
│   │   ├── mcts.py            # Monte Carlo Tree Search
│   │   └── trainer.py         # Training loop
│   ├── environment/
│   │   ├── simulator.py       # Energy market simulator
│   │   └── state.py           # State representation
│   └── train.py               # Main training script
│
├── data/                       # Data pipelines
│   ├── ingest/
│   │   ├── entsoe.py          # ENTSO-E API client
│   │   ├── tennet.py          # TenneT scraper
│   │   ├── copernicus.py      # Weather data
│   │   └── ttf_gas.py         # Gas prices
│   ├── processing/
│   │   ├── clean.py           # Data cleaning
│   │   └── features.py        # Feature engineering
│   └── scheduler.py           # APScheduler cron jobs
│
├── database/
│   ├── models.py              # SQLAlchemy models
│   ├── migrations/            # Database migrations
│   └── seed.py                # Initial data load
│
├── dashboard/                  # Streamlit dashboard
│   ├── app.py                 # Main dashboard
│   ├── pages/
│   │   ├── training.py        # Training metrics
│   │   ├── agent.py           # Agent performance
│   │   ├── data.py            # Data explorer
│   │   └── config.py          # Configuration
│   └── components/
│       ├── charts.py          # Reusable charts
│       └── metrics.py         # Metric cards
│
├── api/                        # FastAPI (optional, later)
│   ├── main.py
│   ├── routes/
│   └── dependencies.py
│
├── notebooks/                  # Jupyter notebooks (exploration)
│   ├── data_exploration.ipynb
│   ├── agent_testing.ipynb
│   └── backtesting.ipynb
│
├── tests/
│   ├── test_agent.py
│   ├── test_environment.py
│   └── test_data.py
│
├── docker-compose.yml          # Local PostgreSQL (if not using Supabase)
├── requirements.txt
├── pyproject.toml
└── README.md
```

---

## 🚀 **MVP IMPLEMENTATION PLAN**

### **Week 1: Setup & Data**
```bash
# Day 1-2: Infrastructure
- [ ] Setup Supabase project
- [ ] Create database schema (time-series tables)
- [ ] Setup Python env (PyTorch, Streamlit, supabase-py)
- [ ] Test MPS (Metal) on MacBook

# Day 3-5: Data Pipeline
- [ ] Implement ENTSO-E client (electricity prices)
- [ ] Implement TTF gas prices
- [ ] Implement Copernicus ERA5 (weather)
- [ ] Download 1 year historical data
- [ ] Store in Supabase

# Day 6-7: Basic Dashboard
- [ ] Streamlit app: data explorer
- [ ] Visualize prices, weather, correlations
- [ ] Verify data quality
```

### **Week 2: Agent v0.1**
```bash
# Day 8-10: Simple Environment
- [ ] Battery simulator (10 kWh)
- [ ] State: SoC, price, forecast
- [ ] Actions: charge/discharge/hold
- [ ] Reward: profit - degradation

# Day 11-12: Neural Network
- [ ] Policy network (128 → 64 → 3)
- [ ] Value network (128 → 64 → 1)
- [ ] Training loop (PPO or simple DQN)

# Day 13-14: Train & Validate
- [ ] Train on 1 week data (2-4 hours)
- [ ] Backtest on held-out data
- [ ] Compare vs naive baseline
- [ ] Visualize in dashboard
```

### **Week 3-4: Iterate & Expand**
```bash
# Week 3: Improve Agent
- [ ] Hyperparameter tuning
- [ ] Add more features (gas prices, grid frequency)
- [ ] Longer training (1 month data)
- [ ] Better reward shaping

# Week 4: Dashboard & Metrics
- [ ] Real-time metrics (loss, reward, profit)
- [ ] Agent decision visualization
- [ ] A/B comparison (agent vs baseline)
- [ ] Training progress tracking
```

---

## 🛠️ **TECH STACK DETAILS**

### **Python Libraries:**
```toml
[tool.poetry.dependencies]
python = "^3.11"

# Deep Learning
torch = "^2.1.0"              # PyTorch with MPS support
numpy = "^1.24.0"

# Dashboard
streamlit = "^1.29.0"
plotly = "^5.18.0"
altair = "^5.2.0"

# Database
supabase = "^2.3.0"           # Supabase Python client
sqlalchemy = "^2.0.0"
psycopg2-binary = "^2.9.0"
timescaledb = "^0.1.0"        # (via PostgreSQL extension)

# Data Ingestion
requests = "^2.31.0"
pandas = "^2.1.0"
xarray = "^2023.12.0"         # For NetCDF (ERA5 data)
cdsapi = "^0.6.1"             # Copernicus API
entsoe-py = "^0.6.0"          # ENTSO-E client

# Scheduling
apscheduler = "^3.10.0"

# API (optional)
fastapi = "^0.108.0"
uvicorn = "^0.25.0"

# Development
jupyter = "^1.0.0"
pytest = "^7.4.0"
black = "^23.12.0"
ruff = "^0.1.0"
```

### **Supabase Schema:**
```sql
-- Enable TimescaleDB extension
CREATE EXTENSION IF NOT EXISTS timescaledb;

-- Market prices (ENTSO-E)
CREATE TABLE market_prices (
    timestamp TIMESTAMPTZ NOT NULL,
    bidding_zone TEXT NOT NULL,     -- 'NL', 'DE', etc.
    price_day_ahead NUMERIC,         -- €/MWh
    price_imbalance_up NUMERIC,
    price_imbalance_down NUMERIC,
    PRIMARY KEY (timestamp, bidding_zone)
);

SELECT create_hypertable('market_prices', 'timestamp');

-- Weather data (ERA5)
CREATE TABLE weather (
    timestamp TIMESTAMPTZ NOT NULL,
    latitude NUMERIC NOT NULL,
    longitude NUMERIC NOT NULL,
    temperature NUMERIC,             -- °C
    solar_irradiance NUMERIC,        -- W/m²
    wind_speed NUMERIC,              -- m/s
    PRIMARY KEY (timestamp, latitude, longitude)
);

SELECT create_hypertable('weather', 'timestamp');

-- Gas prices (TTF)
CREATE TABLE commodity_prices (
    timestamp TIMESTAMPTZ NOT NULL PRIMARY KEY,
    ttf_gas NUMERIC,                 -- €/MWh
    eua_carbon NUMERIC,              -- €/ton CO2
    brent_oil NUMERIC                -- $/barrel
);

SELECT create_hypertable('commodity_prices', 'timestamp');

-- Agent decisions
CREATE TABLE agent_decisions (
    id BIGSERIAL PRIMARY KEY,
    timestamp TIMESTAMPTZ NOT NULL,
    agent_version TEXT,
    state JSONB,                     -- Full state at decision time
    action JSONB,                    -- Action taken
    reward NUMERIC,                  -- Immediate reward
    value_estimate NUMERIC           -- Agent's value estimate
);

CREATE INDEX idx_agent_decisions_timestamp ON agent_decisions(timestamp);

-- Training metrics
CREATE TABLE training_metrics (
    id BIGSERIAL PRIMARY KEY,
    timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    epoch INTEGER,
    step INTEGER,
    loss NUMERIC,
    policy_loss NUMERIC,
    value_loss NUMERIC,
    entropy NUMERIC,
    learning_rate NUMERIC,
    batch_reward NUMERIC
);

-- Model checkpoints (metadata, files stored in Supabase Storage)
CREATE TABLE model_checkpoints (
    id BIGSERIAL PRIMARY KEY,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    version TEXT UNIQUE,
    epoch INTEGER,
    metrics JSONB,                   -- Final metrics
    storage_path TEXT,               -- Path in Supabase Storage
    notes TEXT
);
```

---

## 📊 **DASHBOARD MOCKUP (Streamlit)**

```python
# dashboard/app.py
import streamlit as st
import plotly.graph_objects as go
from supabase import create_client
import pandas as pd

st.set_page_config(page_title="KIIRA Energy Agent", layout="wide")

# Sidebar navigation
page = st.sidebar.selectbox("Navigation", [
    "🏠 Overview",
    "📊 Training Metrics",
    "🤖 Agent Performance",
    "📈 Data Explorer",
    "⚙️ Configuration"
])

# Connect to Supabase
supabase = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"]
)

if page == "🏠 Overview":
    st.title("⚡ KIIRA Energy Agent Dashboard")
    
    # Metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Agent Version", "v0.1.2")
    with col2:
        st.metric("Training Epochs", "150 / 200")
    with col3:
        st.metric("Current Profit", "+€1,247", delta="+12%")
    with col4:
        st.metric("Avg Daily Reward", "€8.32", delta="+€0.45")
    
    # Recent decisions
    st.subheader("Recent Agent Decisions")
    decisions = supabase.table('agent_decisions')\
        .select('*')\
        .order('timestamp', desc=True)\
        .limit(10)\
        .execute()
    
    st.dataframe(pd.DataFrame(decisions.data))
    
    # Price chart
    st.subheader("Electricity Prices (Last 7 Days)")
    prices = supabase.table('market_prices')\
        .select('timestamp, price_day_ahead')\
        .gte('timestamp', 'now() - interval \'7 days\'')\
        .execute()
    
    df = pd.DataFrame(prices.data)
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df['timestamp'],
        y=df['price_day_ahead'],
        mode='lines',
        name='Day-Ahead Price'
    ))
    st.plotly_chart(fig, use_container_width=True)

elif page == "📊 Training Metrics":
    st.title("Training Metrics")
    
    # Fetch training history
    metrics = supabase.table('training_metrics')\
        .select('*')\
        .order('timestamp')\
        .execute()
    
    df = pd.DataFrame(metrics.data)
    
    # Loss curves
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Loss")
        fig = go.Figure()
        fig.add_trace(go.Scatter(y=df['loss'], name='Total Loss'))
        fig.add_trace(go.Scatter(y=df['policy_loss'], name='Policy Loss'))
        fig.add_trace(go.Scatter(y=df['value_loss'], name='Value Loss'))
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Reward")
        fig = go.Figure()
        fig.add_trace(go.Scatter(y=df['batch_reward'], name='Batch Reward'))
        st.plotly_chart(fig, use_container_width=True)

# ... more pages
```

---

## 💰 **COST ESTIMATE**

### **Supabase Free Tier:**
```yaml
Database:
  - 500 MB storage ✅ (enough for 1-2 years hourly data)
  - Unlimited API requests
  - Paused after 1 week inactivity (just wake up)

Storage:
  - 1 GB ✅ (enough for ~10 model checkpoints)

Edge Functions:
  - 500k invocations/month
  - (We don't need these for MVP)

Bandwidth:
  - 5 GB egress

Cost: $0/month (free tier sufficient for MVP)
```

### **Streamlit Cloud:**
```yaml
Community (Free):
  - 1 GB RAM
  - Shared CPU
  - Public apps only
  
Cost: $0/month
```

### **Total MVP Cost: $0/month** 🎉

### **When to Upgrade:**
```yaml
Supabase Pro ($25/month):
  - When database > 500 MB (around year 2-3 of data)
  - When need more compute (background workers)
  
Streamlit Team ($200/month):
  - When need private deployment
  - When need more resources
  
Cloud GPU (RunPod, Lambda Labs):
  - When model > 10M parameters (training too slow on MacBook)
  - Cost: ~$0.50-1.00/hour (A40/A100)
  - Only for intensive training, then stop
```

---

## 🚀 **NEXT STEPS**

### **Option 1: Start with Infrastructure (Recommended)**
```bash
# 1. Create Supabase project
# 2. Setup database schema
# 3. Test data ingestion (1 API)
# 4. Build minimal dashboard (show 1 chart)
# 5. Validate full stack works

Time: 1-2 days
Output: Working end-to-end pipeline (no agent yet)
```

### **Option 2: Start with Agent (Riskier)**
```bash
# 1. Build agent in isolation (no database)
# 2. Train on local CSV files
# 3. Add infrastructure later

Time: 2-3 days for agent
Risk: Integration issues later
```

**Ik raad Option 1 aan** - eerst de infrastructuur, dan de agent erbij.

---

## ❓ **Vragen voor jou:**

1. **MacBook specs?** (M1/M2/M3 of Intel? Hoeveel RAM?)
2. **Dashboard preferences?** (Streamlit = snel, Next.js = fancy)
3. **Start vandaag?** (Zal ik setup scripts maken?)
4. **Git repo?** (Wil je dit in KIIRA-PAY repo of aparte repo?)

**Laten we beginnen?** 🚀
