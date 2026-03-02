# TenneT API Setup Guide
## Stap-voor-stap instructies

## 📋 Stap 1: Installeer Python Dependencies

```bash
cd /Users/moesa/KIIRA-PAY/tennet-data

# Install packages
pip install -r requirements.txt
```

**Verwachte output:**
```
Successfully installed requests-2.31.0 pandas-2.1.0 python-dotenv-1.0.0
```

---

## 🔑 Stap 2: Registreer TenneT Account

1. Ga naar: **https://developer.tennet.eu/register/**

2. Vul in:
   - Email: (je email)
   - Name: (je naam)
   - Company: (optioneel)
   - Purpose: "Energy arbitrage research"

3. Klik **Register**

4. Check inbox, klik verification link

5. Login: **https://developer.tennet.eu/login/**

6. Ga naar **Dashboard** of **Applications**

7. Klik **Create New Application**
   - Name: "Energy Data Download"
   - Description: "Historical data download"

8. **Copy API Key** (lange string)

---

## 💾 Stap 3: Voeg API Key Toe

```bash
# Copy template
cp .env.example .env

# Edit .env
nano .env
```

Vervang `your_api_key_here` met je echte key:
```
TENNET_API_KEY=abc123xyz789...
```

Save (Ctrl+X, Y, Enter)

---

## ✅ Stap 4: Test API Connection

```bash
python test_api.py
```

**Expected output:**
```
============================================================
🔌 Testing TenneT API Connection
============================================================

API Key: abc123xyz7...89xyz

✅ Settlement Prices: OK (24 records)

✅ Balance Delta: OK (96 records)

✅ Merit Order List: OK (18 records)

✅ FRR Activations: OK (32 records)

✅ Metered Injections: OK (24 records)

✅ Reconciliation Prices: OK (12 records)

============================================================
🎉 Success! All 6 APIs working!

Next step: python download_data.py --year 2025
============================================================
```

**Als errors:**
- `401 Unauthorized` → Check API key in .env
- `429 Rate limit` → Wacht 1 minuut
- `Connection error` → Check internet

---

## 📥 Stap 5: Download Data

### Optie A: Weekly Sampling (Snel, 1 dag)
```bash
python download_data.py --year 2025 --sampling weekly
```
- 52 requests per API
- Lagere resolutie maar snel klaar
- Good enough voor eerste tests

### Optie B: Daily Sampling (Langzaam, 2-15 dagen)
```bash
python download_data.py --year 2025 --sampling daily
```
- 365 requests per API
- Hogere resolutie
- Kan dagen duren door rate limits

**Recommended:** Start met weekly, later upgraden naar daily

---

## 📊 Stap 6: Manual Download (Settlement Prices)

Settlement Prices heeft rate limit van 25/dag = te langzaam.

**Bulk download:**

1. Ga naar: https://www.tennet.eu/nl-en/grids-and-markets/transparency-data-netherlands/download-page-transparency

2. Selecteer **Settlement Prices**

3. Period: **2025-01-01** to **2025-12-31**

4. Format: **CSV**

5. Klik **Download**

6. Save as: `data/settlement_prices_2025.csv`

---

## 📁 Expected Output

Na voltooien heb je in `data/` folder:

```
data/
├── settlement_prices_2025.csv      (manual download)
├── balance_delta_2025.csv          (auto download)
├── merit_order_2025.csv            (auto download)
├── frr_activations_2025.csv        (auto download)
├── metered_injections_2025.csv     (auto download - langzaam!)
└── reconciliation_prices_2025.csv  (auto download)
```

**File sizes (ongeveer):**
- Settlement prices: 5-10 MB
- Balance delta: 2-5 MB
- Merit order: 10-20 MB (veel records)
- FRR activations: 3-8 MB
- Metered injections: 2-4 MB
- Reconciliation: 1-2 MB

**Total: ~30-50 MB**

---

## ⏱️ Timeline Estimate

| Sampling | Rate Limits | Time Needed |
|----------|-------------|-------------|
| Weekly   | 52 × 5 APIs | ~1 dag |
| Daily    | 365 × 5 APIs | 2-15 dagen (afhankelijk van API) |

**Slowest API:** Metered Injections (25/dag) = 15 dagen voor vol jaar!

**Tip:** Start met weekly, later upgraden naar daily als je meer granulariteit wilt.

---

## 🐛 Troubleshooting

### Script stopt na X requests
```
⏸️ Rate limit reached (25 requests)
Sleeping 24 hours...
```
**Normal!** Script pauzeert automatisch. Laat draaien.

### Connection timeout
```
❌ 2025-06-15: Connection timeout
```
**Fix:** Run opnieuw, script pakt op waar het stopte.

### API key invalid
```
❌ Error 401: Unauthorized
```
**Fix:** 
1. Check .env file
2. Regenerate key op TenneT website
3. Update .env

---

## ✅ Checklist

- [ ] Python packages installed
- [ ] TenneT account registered
- [ ] API key in .env
- [ ] Test script succesvol
- [ ] Download script running
- [ ] Settlement prices manually downloaded
- [ ] All CSV files in data/

---

## 🎉 Klaar!

Je hebt nu alle TenneT data!

**Next step:** Analyseer de data of bouw agents (later).

**Check data:**
```bash
ls -lh data/
```

**Quick peek:**
```bash
head -20 data/balance_delta_2025.csv
```
