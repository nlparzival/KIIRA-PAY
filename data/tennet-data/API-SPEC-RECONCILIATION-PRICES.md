# TenneT Reconciliation Prices API - OpenAPI Spec Reference

## API Info
- **Title:** Aether - Reconciliation Prices
- **Version:** 2.2.0
- **Description:** Gewogen marktprijs voor het verrekenen van verschil tussen profiel-berekend en daadwerkelijk verbruik
- **Base URL:** `https://{environment}.tennet.eu` (environment: `api` of `api.acc`)

## Rate Limits (zelfde voor Production & Acceptance!)

| | Per Second | Per Minute | Per Day |
|---|---|---|---|
| **Alle omgevingen** | 1 | 60 | 300 |

> Rate limits gelden **per pad** (elk sub-endpoint apart)

---

## 3 Sub-endpoints

### 1️⃣ `GET /publications/v1/reconciliation-prices` (Maandelijks)

**Max range:** 1 jaar

| Param | Required | Example |
|---|---|---|
| `date_from` | ✅ | `13-01-2024 00:00:00` |
| `date_to` | ✅ | `13-01-2025 00:00:00` |
| `Accept` | ✅ | `application/json` |

**Response Fields per Point:**

| Field | Type | Example | Description |
|---|---|---|---|
| `timeInterval_start` | datetime | `2025-01-01T00:00` | Start maand |
| `timeInterval_end` | datetime | `2025-02-01T00:00` | Eind maand |
| `isp` | string | `1` | Volgnummer maand |
| `price` | string | `114.32` | Gemiddelde prijs (EUR/MWh) |
| `peak_price` | string | `125.42` | Piekprijs (EUR/MWh) |
| `off_peak_price` | string | `101.36` | Dalprijs (EUR/MWh) |

**Live Data 2024:**
```
jan-24  €83.17  peak €94.62   off-peak €68.80
apr-24  €53.71  peak €68.70   off-peak €34.57  ← goedkoopste maand
dec-24  €117.92 peak €153.03  off-peak €84.64  ← duurste maand
```

---

### 2️⃣ `GET /publications/v1/reconciliation-prices/isp` (Per ISP, 15 min)

**Max range:** 1 maand

| Param | Required | Example |
|---|---|---|
| `date_from` | ✅ | `13-01-2025 00:00:00` |
| `date_to` | ✅ | `13-02-2025 00:00:00` |
| `Accept` | ✅ | `application/json` |

**Response Fields per Point:**

| Field | Type | Example | Description |
|---|---|---|---|
| `timeInterval_start_loc` | datetime | `2025-01-01T00:00` | Start ISP (lokale tijd!) |
| `timeInterval_end_loc` | datetime | `2025-01-01T00:15` | Eind ISP (lokale tijd!) |
| `isp` | string | `1` | ISP nummer (1-96 per dag) |
| `isp_price` | string | `3421525.67` | ISP prijs (EUR/MWh) |

> ⚠️ **Let op:** Veldnamen gebruiken `_loc` suffix! (`timeInterval_start_loc` niet `timeInterval_start`)
> ⚠️ **Let op:** `isp_price` niet `price`!
> ⚠️ **Let op:** `Period` is een **array** (1 per dag), niet een enkel object!

**Resolution:** PT15M (96 ISPs per dag)

**Live Data (1 jan 2025):**
```
ISP 1  00:00  €-105.00  ← negatieve prijs!
ISP 2  00:15  €20.68
ISP 3  00:30  €84.90
ISP 4  00:45  €85.12
```

---

### 3️⃣ `GET /publications/v1/reconciliation-prices/mffbas` (MFFBAS)

**Max range:** 1 maand

**⚠️ Ander parameterschema dan andere endpoints!**

| Param | Required | Example | Notes |
|---|---|---|---|
| `bidding-zone` | ✅ | `10YNL----------L` | NL bidding zone |
| `start-date` | ✅ | `2025-01-13` | **yyyy-mm-dd** (anders dan rest!) |
| `end-date` | ✅ | `2025-02-13` | **yyyy-mm-dd** |
| `product` | ✅ | `023` | Product code |
| `Accept` | ✅ | `application/json` | **Alleen JSON!** |

**Response structuur (compleet anders!):**
```json
{
  "mrid": "...",
  "product": "023",
  "biddingDomain": { "mrid": "10YNL----------L" },
  "priceMonthSeries": [
    {
      "quantity": { "timeframeType": "E10" },
      "product": { "identification": "8716867000030", "measureUnit": "MWH" },
      "price": { "amount": "24.84" }
    }
  ],
  "pricePointSeries": {
    "product": { "resolution": "PT15M", "measureUnit": "MWH" },
    "point": [
      { "pos": 1, "price": { "amount": "77.11" } },
      { "pos": 2, "price": { "amount": "73.66" } }
    ]
  }
}
```

**Timeframe types:** `E10`, `E29`, `E11`

---

## Error Codes (alle endpoints)

| Code | Description |
|---|---|
| 401 | No valid API key found |
| 405 | Method not allowed |
| 422 | Missing/invalid parameters |
| 429 | Rate limit exceeded |
| 504 | Gateway timeout |

**Date format (endpoints 1 & 2):** `dd-mm-yyyy hh24:mi:ss`
**Date format (MFFBAS):** `yyyy-mm-dd`
