# ✅ TenneT API Project Klaar!

## 📁 Project Structuur

```
/Users/moesa/KIIRA-PAY/tennet-data/
├── README.md              ← Overview
├── SETUP.md               ← Stap-voor-stap setup guide
├── requirements.txt       ← Python dependencies (✅ installed)
├── .env.example          ← API key template
├── .env                  ← Jouw API key (edit deze!)
├── test_api.py           ← Test script
├── download_data.py      ← Download script
└── data/                 ← Downloaded CSV files (komen hier)
```

---

## 🚀 Volgende Stappen

### 1️⃣ **Registreer TenneT Account** (5 min)

Ga naar: https://developer.tennet.eu/register/

- Registreer account
- Verificeer email
- Login en create application
- **Copy API key**

---

### 2️⃣ **Voeg API Key Toe** (1 min)

```bash
cd /Users/moesa/KIIRA-PAY/tennet-data

# Edit .env file
nano .env
```

Vervang `your_api_key_here` met je echte key.

Save (Ctrl+X, Y, Enter).

---

### 3️⃣ **Test API** (1 min)

```bash
python test_api.py
```

**Expected:**
```
✅ Settlement Prices: OK
✅ Balance Delta: OK
✅ Merit Order List: OK
✅ FRR Activations: OK
✅ Metered Injections: OK
✅ Reconciliation Prices: OK

🎉 Success! All 6 APIs working!
```

---

### 4️⃣ **Download Data** (1-15 dagen)

**Quick start (weekly sampling, 1 dag):**
```bash
python download_data.py --year 2025 --sampling weekly
```

**Full resolution (daily, 2-15 dagen):**
```bash
python download_data.py --year 2025 --sampling daily
```

**Download loopt automatisch:**
- Respecteert rate limits
- Pauzeert automatisch bij limit
- Hervat automatisch
- Laat gewoon draaien!

---

### 5️⃣ **Manual Download** (5 min)

Settlement Prices moet je handmatig downloaden:

1. Ga naar: https://www.tennet.eu/nl-en/grids-and-markets/transparency-data-netherlands/download-page-transparency
2. Selecteer "Settlement Prices"
3. Period: 2025-01-01 to 2025-12-31
4. Format: CSV
5. Download
6. Save as: `data/settlement_prices_2025.csv`

---

## 📊 Expected Output

Na downloaden heb je:

```
data/
├── settlement_prices_2025.csv      (manual)
├── balance_delta_2025.csv          (auto)
├── merit_order_2025.csv            (auto)
├── frr_activations_2025.csv        (auto)
├── metered_injections_2025.csv     (auto - slowest!)
└── reconciliation_prices_2025.csv  (auto)
```

**Total: ~30-50 MB data**

---

## ⏱️ Timeline

| Sampling | Time |
|----------|------|
| Weekly   | ~1 dag |
| Daily    | 2-15 dagen (Metered Injections is traag: 25/dag limit) |

**Tip:** Start met weekly voor snelle resultaten!

---

## 📚 Documentation

- Setup guide: `SETUP.md`
- API docs: `/Users/moesa/KIIRA-PAY/technisch/TENNET-API-COMPLETE.md`
- Simulation: `/Users/moesa/KIIRA-PAY/technisch/SIMULATIE-STRATEGIE.md`

---

## 🔥 Next: Wat Doen Met De Data?

**Optie 1: Excel Analyse** (simpel)
- Open CSV files in Excel/Numbers
- Plot prijzen over tijd
- Zoek patronen

**Optie 2: Python Analyse** (later)
- Build agents
- Backtest strategieën
- Dashboard

**Optie 3: Wacht Tot Alle Data Binnen Is**
- Laat download lopen
- Ga koffie halen ☕
- Check morgen/volgende week

---

## ✅ Checklist

- [ ] TenneT account registered
- [ ] API key in .env
- [ ] test_api.py succesvol
- [ ] download_data.py running
- [ ] Settlement prices manually downloaded
- [ ] All CSV files in data/
- [ ] **🎉 KLAAR!**

---

**Veel succes! 🚀**

Vragen? Check SETUP.md voor troubleshooting.
