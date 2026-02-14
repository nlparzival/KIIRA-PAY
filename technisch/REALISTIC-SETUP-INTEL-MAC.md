# ⚠️ Realistic Setup: Intel MacBook 2017

**Hardware:** 2017 MacBook Pro 13" (2.3GHz dual-core Intel i5, 8GB RAM)  
**Datum:** 12 februari 2026  
**Reality Check:** Training deep learning op deze machine

---

## 💻 **HARDWARE REALITY CHECK**

### **Jouw MacBook Specs:**
```yaml
CPU: Intel Core i5 (2.3 GHz, 2 cores)
RAM: 8 GB DDR3
GPU: Intel Iris Plus Graphics 640 (integrated, 1.5GB)
macOS: Ventura

Deep Learning Capability:
  ❌ Geen Metal Performance Shaders (MPS) - dat is alleen Apple Silicon (M1/M2/M3)
  ❌ Geen CUDA - dat is alleen NVIDIA GPU's
  ❌ Geen goede GPU acceleratie voor PyTorch
  ✅ CPU-only training mogelijk, maar ZEER LANGZAAM
  ⚠️ 8GB RAM is aan de krappe kant voor deep learning
```

### **Training Time Reality (CPU-only):**
```python
# Kleine agent (100k parameters)
Training data: 1 week (168 hours)
Training time on Intel i5: 12-24 uur  # ⚠️ Slow but doable

# Medium agent (1M parameters)
Training data: 1 jaar (8760 hours)
Training time on Intel i5: 3-7 DAGEN  # ⚠️⚠️ Very slow

# Large agent (5M+ parameters)
Training time: WEKEN tot MAANDEN  # ❌ Niet realistisch

# Comparison:
M1/M2 MacBook (MPS): 10x sneller
Cloud GPU (A100): 100x sneller
```

---

## 🎯 **ADJUSTED STRATEGY**

### **Optie A: Train Locally (Feasible but Slow)**
```yaml
Aanpak:
  ✅ Start met ZEER kleine agent (< 100k parameters)
  ✅ Train op korte periode (1 week data)
  ✅ Overnight training (12-24 uur)
  ✅ Proof of concept
  
  ⚠️ Upgraden naar grotere agent = onhaalbaar op deze laptop
  ⚠️ 8GB RAM = kan crashen bij grote datasets
  
When to use:
  - Experimenteren met architecture
  - Testen van code
  - Debugging
  - Kleine proof-of-concepts
```

### **Optie B: Cloud Training (Recommended)** ⭐⭐⭐⭐⭐
```yaml
Aanpak:
  ✅ Develop lokaal (code, dashboard, data pipelines)
  ✅ Train in cloud (goedkope GPU's)
  ✅ Download trained model
  ✅ Run inference lokaal (veel lichter dan training)
  
Goedkope Cloud GPU Opties:
  1. Google Colab (FREE tier!)
     - Tesla T4 GPU (gratis)
     - ~15 GB RAM
     - Limitations: 12 uur sessies, kan interrupted worden
     - Cost: €0 (of €10/maand voor Colab Pro)
  
  2. Kaggle Notebooks (FREE!)
     - Tesla P100 GPU (gratis)
     - 30 uur/week GPU time
     - 16 GB RAM
     - Cost: €0
  
  3. RunPod / Lambda Labs (Pay-as-you-go)
     - RTX 4090: €0.40/uur
     - A40: €0.60/uur
     - Only pay when training
     - Cost: ~€5-20 voor MVP training
  
  4. Vast.ai (Spotmarkt)
     - RTX 3090: €0.20-0.40/uur
     - Cheapest option
     - Less reliable (spot instances)

Best Strategy:
  - Use Google Colab FREE for MVP (€0)
  - If need more: Kaggle (€0) or RunPod (€5-20 total)
```

### **Optie C: Pre-trained Models (Smartest?)** ⭐⭐⭐⭐⭐
```yaml
Aanpak:
  ✅ Use existing time-series models (pre-trained)
  ✅ Fine-tune on energy data (veel sneller dan from scratch)
  ✅ Transfer learning
  
Options:
  1. TimeGPT (Nixtla) - Time-series foundation model
  2. Chronos (Amazon) - Pre-trained forecasting
  3. Lag-Llama - Time-series transformer
  4. TiDE (Google) - Time-series dense encoder
  
Benefits:
  - Train in minutes/hours instead of days/weeks
  - Better performance (pre-trained knowledge)
  - Works on CPU (smaller models)
  - State-of-art architectures

Possible for our use case:
  - Start with pre-trained forecasting model
  - Fine-tune on electricity prices
  - Add RL layer on top for decision-making
```

---

## 🐍 **WAT IS PYTORCH?** (ELI5)

### **PyTorch = Deep Learning Framework**
```python
# Wat is PyTorch?
"""
PyTorch is een library (software pakket) voor het bouwen van 
neural networks (kunstmatige hersenen).

Analogie:
- Python = taal (zoals Nederlands)
- PyTorch = gereedschapskist voor AI bouwen
- Net zoals je pandas gebruikt voor data, gebruik je PyTorch voor AI

Gemaakt door: Meta/Facebook (open-source, gratis)
Alternatief: TensorFlow (Google), maar PyTorch is populairder
"""

# Simpel voorbeeld:
import torch
import torch.nn as nn

# Define a neural network (agent's brain)
class SimpleAgent(nn.Module):
    def __init__(self):
        super().__init__()
        self.layer1 = nn.Linear(10, 64)   # Input layer
        self.layer2 = nn.Linear(64, 32)   # Hidden layer
        self.layer3 = nn.Linear(32, 3)    # Output layer (3 actions)
    
    def forward(self, state):
        x = torch.relu(self.layer1(state))
        x = torch.relu(self.layer2(x))
        action = self.layer3(x)
        return action

# Create agent
agent = SimpleAgent()

# Train it (simpel voorbeeld)
state = torch.randn(10)  # Random state
action = agent(state)     # Agent decides action
print(action)             # [0.5, -0.2, 0.8] → probabilities per action
```

### **Waarom PyTorch?**
```yaml
Pros:
  ✅ Industry standard (gebruikt door OpenAI, Meta, Tesla, etc.)
  ✅ Pythonic (makkelijk te leren als je Python kent)
  ✅ Dynamic computation graph (flexibel)
  ✅ Grote community (veel tutorials, hulp)
  ✅ Gratis & open-source

Cons for Intel Mac:
  ⚠️ Geen GPU acceleratie (alleen CPU)
  ⚠️ Langzaam op oude hardware
  ⚠️ Geen MPS backend (alleen Apple Silicon)

Alternatives:
  - TensorFlow (Google) - Vergelijkbaar, maar minder populair
  - JAX (Google) - Sneller, maar complexer
  - Keras (high-level API) - Simpeler, maar minder flexibel
```

---

## 🗄️ **IS SUPABASE GOEDE KEUZE?**

### **TL;DR: JA! ✅** (Vooral voor jouw situatie)

### **Waarom Supabase Perfect Is:**
```yaml
1. MANAGED DATABASE (geen DevOps):
   ✅ Jij hoeft geen PostgreSQL te installeren/beheren
   ✅ Geen Docker nodig (scheelt resources op 8GB RAM machine)
   ✅ Automatic backups
   ✅ Altijd online (geen localhost crashes)

2. GRATIS TIER:
   ✅ 500 MB database (genoeg voor 1-2 jaar data)
   ✅ 1 GB storage (genoeg voor modellen)
   ✅ Unlimited API requests
   ✅ €0/maand

3. PYTHON SDK:
   ✅ Easy to use (pip install supabase)
   ✅ Query builder (geen SQL nodig)
   ✅ Real-time subscriptions

4. FUTURE-PROOF:
   ✅ Als je later upgradet (nieuwe MacBook, cloud), 
      database blijft hetzelfde
   ✅ Team collaboration (multiple developers)
   ✅ Production-ready

5. SAVES YOUR LAPTOP:
   ✅ Database draait in cloud (niet op jouw 8GB RAM)
   ✅ Jouw laptop = alleen development
   ✅ Minder overhead, minder crashes
```

### **Code Voorbeeld:**
```python
# Install
pip install supabase

# Connect (super simpel)
from supabase import create_client, Client

supabase: Client = create_client(
    "https://your-project.supabase.co",
    "your-api-key"
)

# Insert data (1 regel!)
supabase.table('market_prices').insert({
    'timestamp': '2024-01-01 12:00:00',
    'price_day_ahead': 65.5
}).execute()

# Query data (makkelijk)
response = supabase.table('market_prices')\
    .select('*')\
    .gte('timestamp', '2024-01-01')\
    .lte('timestamp', '2024-01-31')\
    .execute()

prices = response.data  # List of dicts
```

### **Alternatieven (Waarom Slechter):**
```yaml
SQLite (lokaal bestand):
  ❌ Geen real-time updates
  ❌ Geen cloud backup
  ❌ Niet schaalbaar
  ✅ Wel gratis & simpel

PostgreSQL lokaal (Docker):
  ❌ Gebruikt veel RAM (2-4 GB)
  ❌ Jij moet beheren
  ❌ Crashes bij laptop restart
  ✅ Wel volledige controle

MongoDB Atlas:
  ✅ Ook managed & gratis tier
  ⚠️ NoSQL (niet ideaal voor time-series)
  ⚠️ Minder features dan Supabase

Conclusie: Supabase = beste keuze voor MVP! ✅
```

---

## 🎯 **REVISED MVP STRATEGY**

### **Stack (Adjusted for Intel Mac):**
```yaml
Local Development (op jouw MacBook):
  - Code editor (VS Code)
  - Python 3.11
  - Streamlit (dashboard)
  - Data pipelines (fetch ENTSO-E, etc.)
  - Small experiments
  
  RAM usage: ~2-3 GB (safe for 8GB machine)

Database (in cloud):
  - Supabase PostgreSQL
  - Stores all data
  - No load on your laptop
  
  Cost: €0

Training (in cloud):
  - Google Colab (FREE) or Kaggle
  - Train agent on GPU
  - Download trained model (.pth file)
  - Upload to Supabase Storage
  
  Cost: €0 (Colab free tier)

Inference (op jouw MacBook):
  - Load trained model
  - Run predictions (CPU-only, but fast enough)
  - Inference is 100x lighter than training
  
  RAM usage: ~1-2 GB
```

### **Workflow:**
```python
# 1. DEVELOP LOCALLY (MacBook)
# Write code, test pipelines, build dashboard
$ python data/ingest/entsoe.py  # Fetch data
$ streamlit run dashboard/app.py  # View dashboard

# 2. TRAIN IN CLOUD (Google Colab)
# Upload code to Colab notebook
# Train agent on free GPU (12 hours max session)
!python agent/train.py --epochs 100
# Download trained model: agent_v1.pth

# 3. DEPLOY MODEL (Supabase Storage)
# Upload model to Supabase
supabase.storage.from_('models').upload(
    'agent_v1.pth',
    open('agent_v1.pth', 'rb')
)

# 4. RUN INFERENCE (MacBook)
# Download model, run predictions
model = torch.load('agent_v1.pth')
action = model(state)  # Fast! (< 10ms)
```

---

## 📦 **INSTALLATION PLAN**

### **Step 1: Python Setup (30 min)**
```bash
# Check Python version (need 3.10+)
python3 --version

# If < 3.10, install from python.org
# Download: https://www.python.org/downloads/

# Install poetry (package manager)
curl -sSL https://install.python-poetry.org | python3 -

# OR use pip + venv
python3 -m venv venv
source venv/bin/activate
```

### **Step 2: Install Libraries (15 min)**
```bash
# Create requirements.txt
cat > requirements.txt << EOF
# Core
numpy==1.24.3
pandas==2.0.3

# Deep Learning (CPU-only, smaller download)
torch==2.1.0  # Will auto-detect CPU-only
torchvision==0.16.0

# Dashboard
streamlit==1.29.0
plotly==5.18.0

# Database
supabase==2.3.0

# Data APIs
requests==2.31.0
entsoe-py==0.6.1

# Utils
python-dotenv==1.0.0
EOF

# Install (this will take 10-15 min, PyTorch is large)
pip install -r requirements.txt
```

### **Step 3: Supabase Setup (15 min)**
```bash
# 1. Go to https://supabase.com
# 2. Sign up (gratis, GitHub login)
# 3. Create new project
#    - Name: kiira-energy-agent
#    - Database password: [choose strong password]
#    - Region: Europe (Frankfurt or Amsterdam)
# 4. Wait 2-3 min for project to spin up
# 5. Copy API keys from Settings → API

# 6. Create .env file
cat > .env << EOF
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_KEY=your-anon-key-here
EOF
```

### **Step 4: Test Everything (15 min)**
```python
# test_setup.py
import torch
import streamlit as st
from supabase import create_client
import pandas as pd
import numpy as np

print("✅ PyTorch version:", torch.__version__)
print("✅ Streamlit version:", st.__version__)
print("✅ Pandas version:", pd.__version__)
print("✅ NumPy version:", np.__version__)

# Test PyTorch
x = torch.randn(10, 10)
print("✅ PyTorch tensor created:", x.shape)

# Test Supabase connection
supabase = create_client(
    "https://xxxxx.supabase.co",
    "your-key"
)
print("✅ Supabase connected")

# Test simple neural network
class TinyNet(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.fc = torch.nn.Linear(10, 1)
    
    def forward(self, x):
        return self.fc(x)

model = TinyNet()
output = model(torch.randn(1, 10))
print("✅ Neural network works:", output.shape)

print("\n🎉 ALL SYSTEMS GO! Ready to build agent.")
```

```bash
# Run test
python test_setup.py
```

---

## 🚀 **WEEK 1 PLAN (REALISTIC)**

### **Day 1: Setup (3-4 uur)**
```bash
✅ Install Python, PyTorch, Streamlit
✅ Create Supabase project
✅ Run test_setup.py
✅ Create project structure
```

### **Day 2: Database (2-3 uur)**
```bash
✅ Design Supabase schema (tables)
✅ Create tables via Supabase UI
✅ Test insert/query data
✅ Write helper functions (database/client.py)
```

### **Day 3-4: Data Pipeline (4-6 uur)**
```bash
✅ ENTSO-E API client (electricity prices)
✅ Download 1 week test data
✅ Store in Supabase
✅ Verify data quality
```

### **Day 5: Streamlit Dashboard (3-4 uur)**
```bash
✅ Create minimal dashboard
✅ Show price chart (last 7 days)
✅ Display data statistics
✅ Test locally: streamlit run dashboard/app.py
```

### **Day 6-7: Tiny Agent (Optional)**
```bash
✅ Build VERY simple agent (< 50k params)
✅ Train on laptop overnight (12 uur)
✅ Test if it learns ANYTHING
✅ If works → plan cloud training for bigger agent
```

---

## 💡 **KEY DECISIONS**

### **✅ Do Locally (MacBook):**
- Code development
- Data pipeline (fetching APIs)
- Dashboard (Streamlit)
- Inference (running trained models)
- Debugging & testing

### **☁️ Do in Cloud:**
- Agent training (Google Colab FREE tier)
- Database (Supabase)
- Large data processing (if needed)

### **💰 Costs:**
```
Supabase: €0 (free tier)
Google Colab: €0 (free tier, 12hr sessions)
PyTorch: €0 (open-source)
Streamlit: €0 (local or Streamlit Cloud free)

Optional later:
  Colab Pro: €10/maand (longer sessions, faster GPU)
  RunPod: €5-20 one-time (voor intensive training)

Total MVP cost: €0 🎉
```

---

## 🎯 **FINAL RECOMMENDATIONS**

### **1. Accept Hardware Limitations:**
```
Your MacBook is perfect for:
  ✅ Development
  ✅ Dashboard
  ✅ Data pipelines
  ✅ Testing small models

Your MacBook is NOT good for:
  ❌ Training large neural networks
  ❌ Processing massive datasets in RAM
  
Solution: Use cloud for heavy lifting (gratis!)
```

### **2. Smart Architecture:**
```
Develop → Train → Deploy
   ↓        ↓        ↓
MacBook → Colab → MacBook
  (code)  (GPU)  (inference)
```

### **3. Start Small, Prove Concept:**
```
Week 1: Infrastructure + tiny agent
Week 2: If promising → scale up in cloud
Week 3: If works → add more features
Week 4: Production-ready MVP
```

---

## 🚀 **READY TO START?**

**Ik kan nu voor je maken:**

**A) Installation Guide** - Stap-voor-stap setup voor jouw MacBook
**B) Supabase Schema** - Complete database design
**C) Data Pipeline** - ENTSO-E API client (eerste data source)
**D) Minimal Dashboard** - Streamlit app (toon 1 chart)
**E) Google Colab Notebook** - Training template (GPU training)

**Wat heeft prioriteit? Laten we beginnen!** 🚀

**PS:** PyTorch installer is ~500MB, duurt ~10 min op goede internet. Supabase setup is 5 min via web interface. Geen bloated software, alles redelijk licht.
