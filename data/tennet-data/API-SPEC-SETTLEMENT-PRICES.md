# TenneT Settlement Prices API - OpenAPI Spec Reference

## API Info
- **Title:** Aether - Settlement Prices
- **Version:** 1.5.1
- **Description:** Imbalance prices per balancing time unit
- **Base URL:** `https://{environment}.tennet.eu` (environment: `api` of `api.acc`)

## ⚠️ Rate Limits (ZEER STRENG op Production!)

| | Per Second | Per Minute | Per Day |
|---|---|---|---|
| **Production** | 1 | **5** | **25** |
| **Acceptance** | 1 | 60 | 300 |

> **LET OP:** Production heeft maar 25 requests per dag! Plan je downloads zorgvuldig.

## Endpoint

### `GET /publications/v1/settlement-prices`

### Parameters
| Param | Type | Required | Example | Notes |
|---|---|---|---|---|
| `date_from` | query string | ✅ | `01-01-2025 00:00:00` | Start datum |
| `date_to` | query string | ✅ | `01-02-2025 00:00:00` | Eind datum |
| `Accept` | header | ✅ | `application/json` | Response format |

**Max range:** 1 maand

**Date format:** `dd-mm-yyyy hh24:mi:ss`

**Response formats:** `application/json`, `application/xml`, `text/csv`, `application/xlsx`

### Response Fields (per Point)

| Field | Type | Example | Description |
|---|---|---|---|
| `timeInterval_start` | datetime | `2025-06-20T00:00` | Start tijdstip ISP |
| `timeInterval_end` | datetime | `2025-06-20T00:15` | Eind tijdstip ISP |
| `isp` | string | `1` | Imbalance Settlement Period nummer (1-96 per dag) |
| `shortage` | string | `55.00` | Shortage prijs (EUR/MWh) — prijs bij tekort |
| `surplus` | string | `66.00` | Surplus prijs (EUR/MWh) — prijs bij overschot |
| `dispatch_up` | string | `33.00` | Dispatch prijs opwaarts (EUR/MWh) |
| `dispatch_down` | string | `36.00` | Dispatch prijs neerwaarts (EUR/MWh) |
| `regulation_state` | integer | `1` | Regulatiestaat (1 = UP, -1 = DOWN) |
| `regulating_condition` | string | `DOWN` | Richting: `UP`, `DOWN`, of `UP_AND_DOWN` |
| `incident_reserve_up` | string | `YES` | Incident reserve opwaarts geactiveerd |
| `incident_reserve_down` | string | `NO` | Incident reserve neerwaarts geactiveerd |

### Regulating Conditions (uit live data)
- **`UP`** — Opwaartse regulatie (tekort aan energie, prijs stijgt)
- **`DOWN`** — Neerwaartse regulatie (overschot aan energie, prijs daalt)
- **`UP_AND_DOWN`** — Beide richtingen tegelijk actief

### Prijslogica voor Arbitrage
- Bij `UP`: gebruik `shortage` prijs (je wordt betaald om te leveren)
- Bij `DOWN`: gebruik `surplus` prijs (je betaalt om af te nemen)  
- Bij `UP_AND_DOWN`: `shortage` ≠ `surplus` — groot verschil = kans!
- `dispatch_up`/`dispatch_down` zijn de daadwerkelijk afgerekende dispatch prijzen

### CSV Kolommen
```
Timeinterval Start Loc, Timeinterval End Loc, Isp, Currency Unit Name, 
Price Measurement Unit Name, Incident Reserve Up, Incident Reserve Down, 
Price Dispatch Up, Price Dispatch Down, Price Shortage, Price Surplus, 
Regulation State, Regulating Condition
```

### Error Codes
| Code | Description |
|---|---|
| 401 | No valid API key found |
| 405 | Method not allowed |
| 422 | Missing/invalid parameters (check date format!) |
| 429 | Rate limit exceeded |
| 503 | Service temporarily unavailable (maintenance) |

### Live Data Voorbeeld (3 maart 2026)
```
ISP  1 | 00:00 | UP_AND_DOWN | short €63.00  | surp €53.07  | d_up €55.72 | d_dn €53.07
ISP  4 | 00:45 | DOWN        | short €-4.00  | surp €-4.00  | d_up -      | d_dn €-4.00
ISP  5 | 01:00 | UP_AND_DOWN | short €109.00 | surp €-7.70  | d_up €109   | d_dn €-7.70
ISP 91 | 22:30 | UP          | short €137.00 | surp €137.00 | d_up €137   | d_dn -
```
> ISP 5 is een goed arbitrage-voorbeeld: shortage €109 vs surplus €-7.70 = spread van €116.70/MWh!
