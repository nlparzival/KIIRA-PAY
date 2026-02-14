# 📓 Google Colab Explained (+ VS Code Integration)

**Datum:** 12 februari 2026  
**Vraag:** Wat is Google Colab precies? VS Code extensie?

---

## 🤔 **WAT IS GOOGLE COLAB?**

### **Simpele Uitleg:**
```
Google Colab = Jupyter Notebook in de cloud met GRATIS GPU's

Analogie:
- Google Docs = Word in je browser
- Google Colab = Python notebook in je browser met GPU

Je schrijft Python code in je browser
→ Code draait op Google's servers (niet jouw laptop)
→ Met gratis GPU toegang!
```

### **Visueel:**
```
┌─────────────────────────────────────────────────────┐
│         JOUW BROWSER (Chrome/Safari)                │
│  ┌───────────────────────────────────────────────┐  │
│  │  Google Colab Interface                       │  │
│  │  ┌─────────────────────────────────────────┐  │  │
│  │  │  # Cell 1: Install packages             │  │  │
│  │  │  !pip install torch numpy               │  │  │
│  │  │  ▶ Run                                   │  │  │
│  │  └─────────────────────────────────────────┘  │  │
│  │  ┌─────────────────────────────────────────┐  │  │
│  │  │  # Cell 2: Train model                  │  │  │
│  │  │  model = NeuralNetwork()                │  │  │
│  │  │  model.train()  # Draait op GPU!        │  │  │
│  │  │  ▶ Run                                   │  │  │
│  │  └─────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘
                      ↓ Internet
┌─────────────────────────────────────────────────────┐
│         GOOGLE'S SERVERS (Cloud)                    │
│  ┌───────────────────────────────────────────────┐  │
│  │  Virtual Machine                              │  │
│  │  - CPU: 2 cores                               │  │
│  │  - RAM: 12-13 GB                              │  │
│  │  - GPU: Tesla T4 (GRATIS!)                    │  │
│  │  - Disk: 100 GB temporary                     │  │
│  └───────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘
```

---

## 🆓 **GRATIS TIER (Wat krijg je?):**

```yaml
Hardware:
  CPU: 2-core Intel Xeon
  RAM: ~12-13 GB
  GPU: Tesla T4 (16 GB VRAM) 🔥
  Storage: ~100 GB (tijdelijk)

Limitations:
  Session duration: Max 12 uur (dan disconnect)
  Idle timeout: 90 minuten (als je niks doet)
  GPU availability: Soms vol (peak hours)
  Daily limit: ~12 uur GPU time per dag
  
  ⚠️ Na 12 uur wordt VM gereset
  ⚠️ Files worden gewist (moet je downloaden)
  ⚠️ Packages moet je opnieuw installeren

Cost: €0/maand

Colab Pro (€10/maand):
  - Langere sessies (24 uur)
  - Betere GPU's (T4, P100, soms V100)
  - Minder timeouts
  - Meer RAM (25 GB)
  
Colab Pro+ (€50/maand):
  - Nog betere GPU's (A100 soms)
  - Achtergrond uitvoering
  - Langste sessies
```

---

## 🎯 **HOE WERKT HET? (Step-by-Step)**

### **Optie 1: Web Interface (Klassiek)**

```bash
# Stap 1: Ga naar Google Colab
https://colab.research.google.com/

# Stap 2: Maak nieuw notebook
File → New notebook

# Stap 3: Kies GPU
Runtime → Change runtime type → Hardware accelerator: GPU → Save

# Stap 4: Schrijf code in cells
# Cell 1:
!pip install torch torchvision

# Cell 2: Test GPU
import torch
print(torch.cuda.is_available())  # Should print: True

# Cell 3: Train model
model = NeuralNetwork()
model.train()  # Draait op GPU!

# Stap 5: Download resultaten
from google.colab import files
files.download('trained_model.pth')
```

---

## 💻 **VS CODE EXTENSIE?**

### **Reality Check:**

```yaml
Er bestaat een Colab extensie, MAAR:
  ⚠️ Officiële integratie is beperkt/buggy
  ⚠️ Lastig om remote kernel te connecten
  ⚠️ Niet stable genoeg voor productie

Beter: Gebruik Colab in browser
  ✅ Stabiel
  ✅ Alle features
  ✅ Makkelijk
```

### **Alternatieve Workflow (Aanbevolen):**

```bash
# 1. DEVELOP in VS Code (lokaal)
# Schrijf agent code in .py files

# 2. COPY/PASTE naar Colab notebook
# Of upload files naar Colab

# 3. TRAIN in Colab browser
# Met GPU, 1-4 uur

# 4. DOWNLOAD trained model
# Save to Supabase of lokaal

# 5. CONTINUE in VS Code
# Load model, run inference
```

---

## 🔄 **PRACTICAL WORKFLOW (Best Practice)**

### **Workflow A: Hybrid (Recommended)**

```bash
# 1. DEVELOP LOCALLY (VS Code op MacBook)
# agent/model.py
import torch
import torch.nn as nn

class EnergyAgent(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(100, 256)
        self.fc2 = nn.Linear(256, 10)
    
    def forward(self, x):
        x = torch.relu(self.fc1(x))
        return self.fc2(x)

# agent/train.py
from model import EnergyAgent

def train():
    model = EnergyAgent()
    # Training loop...
    return model

# 2. CREATE COLAB NOTEBOOK
# Copy code to Colab cells:
"""
Cell 1: Setup
!pip install torch numpy pandas

Cell 2: Define model
# Paste agent/model.py code

Cell 3: Train
from model import EnergyAgent
model = train()  # GPU!

Cell 4: Download
from google.colab import files
files.download('model.pth')
"""

# 3. RUN IN COLAB (browser)
# Runtime → Run all
# Wacht 1-4 uur

# 4. USE LOCALLY (VS Code)
model = EnergyAgent()
model.load_state_dict(torch.load('model.pth'))
model.eval()  # Inference (fast!)
```

---

## 📊 **COLAB EXAMPLE: Energy Agent**

```python
# === Colab Notebook: train_energy_agent.ipynb ===

# ═══════════════════════════════════════════════════
# Cell 1: Setup
# ═══════════════════════════════════════════════════
!pip install -q torch numpy pandas supabase

import torch
print(f"GPU: {torch.cuda.is_available()}")
print(f"GPU name: {torch.cuda.get_device_name(0)}")
# Output: GPU: True, GPU name: Tesla T4

# ═══════════════════════════════════════════════════
# Cell 2: Upload/Clone Code
# ═══════════════════════════════════════════════════
# Option A: Upload files
from google.colab import files
uploaded = files.upload()

# Option B: Clone from GitHub
!git clone https://github.com/jouw-user/kiira-pay.git
%cd kiira-pay

# ═══════════════════════════════════════════════════
# Cell 3: Download Data
# ═══════════════════════════════════════════════════
from supabase import create_client

supabase = create_client("url", "key")
response = supabase.table('market_prices').select('*').execute()
print(f"Downloaded {len(response.data)} rows")

# ═══════════════════════════════════════════════════
# Cell 4: Train Model
# ═══════════════════════════════════════════════════
model = EnergyAgent().cuda()  # Move to GPU!

for epoch in range(100):
    # Training loop...
    loss = train_step()
    print(f"Epoch {epoch}, Loss: {loss}")

# ═══════════════════════════════════════════════════
# Cell 5: Save & Download
# ═══════════════════════════════════════════════════
torch.save(model.state_dict(), 'agent.pth')

# Download to MacBook
files.download('agent.pth')

# Or upload to Supabase
with open('agent.pth', 'rb') as f:
    supabase.storage.from_('models').upload('agent_v1.pth', f)

print("✅ Done!")
```

---

## 🎯 **WANNEER COLAB, WANNEER LOKAAL?**

```yaml
Use Colab When:
  ✅ Training neural networks (heavy)
  ✅ Need GPU (10-100x sneller)
  ✅ Processing large datasets
  ✅ Hyperparameter tuning

Use Lokaal (VS Code) When:
  ✅ Writing code (development)
  ✅ Running inference (predictions)
  ✅ Data preprocessing (light)
  ✅ Dashboard
  ✅ Git version control

Hybrid:
  ✅ Develop locally → Train Colab → Deploy locally
```

---

## 💰 **KOSTEN:**

```
Google Colab Free:
  - Tesla T4 GPU: €0
  - 12 uur/dag: €0
  - 12 GB RAM: €0
  
Compare:
  - AWS p3.2xlarge (Tesla V100): ~€3/uur
  - RunPod RTX 4090: ~€0.40/uur
  - Lambda Labs A100: ~€1/uur
  
Colab Free = INSANE value! 🔥
```

---

## 🎯 **MIJN AANBEVELING:**

### **Voor KIIRA-PAY:**

```yaml
1. Develop in VS Code (lokaal)
   - Python files
   - Git commits
   - Dashboard testing

2. Train in Colab (browser)
   - Copy code to notebook
   - Run with GPU
   - 1-2x per week

3. Deploy locally (MacBook)
   - Load trained model
   - Run inference
   - Real-time dashboard

Don't bother with:
  ❌ VS Code → Colab remote kernel (buggy)
  ❌ Complex integrations
  
Keep it simple:
  ✅ VS Code voor code
  ✅ Colab browser voor training
  ✅ Copy/paste tussen beiden
```

---

## 🚀 **QUICK START:**

```bash
# 1. Ga naar colab.research.google.com
# 2. File → New notebook
# 3. Runtime → Change runtime type → GPU
# 4. Test:

!nvidia-smi  # Check GPU
# Should see Tesla T4

import torch
print(torch.cuda.is_available())  # True

# 5. Start training! 🔥
```

---

## 📋 **NEXT STEPS:**

Ik kan voor je maken:
- **A)** 📓 Ready-to-use Colab training notebook
- **B)** 🔄 Workflow diagram (VS Code ↔ Colab)
- **C)** 📝 Step-by-step Colab tutorial
- **D)** 🎯 Best practices guide

**Wat wil je eerst?** 🚀

---

## 💡 **TL;DR:**

```
Wat is Colab?
  → Jupyter notebook in browser met gratis GPU

Hoe gebruik je het?
  → Ga naar colab.research.google.com
  → Maak notebook
  → Schrijf Python code
  → Draait op Google servers (niet jouw laptop!)
  → Download results

VS Code extensie?
  → Bestaat, maar buggy
  → Beter: gebruik Colab in browser
  → Copy/paste code tussen VS Code en Colab

Kosten?
  → €0 (gratis tier met Tesla T4 GPU!)

Voor ons project?
  → Develop in VS Code (MacBook)
  → Train in Colab (GPU, 1-2x/week)
  → Deploy locally (inference)
  → Simpel en gratis! 💪
```
