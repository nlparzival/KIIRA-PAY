# TenneT Balance Delta High Resolution API - OpenAPI Spec Reference

## API Info
- **Title:** Aether - Balance Delta High Resolution
- **Version:** 1.5.0
- **Base URL:** `https://{environment}.tennet.eu` (environment: `api` of `api.acc`)
- **Resolutie:** 12 seconden (PT12S)
- **Timestamps:** UTC

## Rate Limits

### `/balance-delta-high-res/latest` (Standaard methode)

| | Per Second | Per Minute |
|---|---|---|
| **Production** | 1 | 10 |
| **Acceptance** | 1 | 10 |

### `/balance-delta-high-res` (Back-up methode)

| | Per Day |
|---|---|
| **Production** | 8 |
| **Acceptance** | 8 |

> ⚠️ **Let op:** De back-up endpoint heeft een zeer strikte rate limit (8/dag).
> Gebruik `/latest` voor real-time monitoring en `/balance-delta-high-res` alleen
> voor het ophalen van gemiste data.

---

## Endpoints

### 1. `GET /publications/v1/balance-delta-high-res/latest`

**Aanbevolen methode.** Retourneert de meest recente 30 minuten (~150 datapunten à 12s).

#### Parameters
| Param | In | Type | Required | Description |
|---|---|---|---|---|
| `Accept` | header | string | ✅ | Alleen `application/json` |

> **Geen date parameters nodig** — altijd de laatste 30 minuten.

#### Aanbevolen polling
Poll 5x per minuut, 1 seconde na elke data-refresh op de 12e seconde:
```
00:00:13, 00:00:25, 00:00:37, 00:00:49, 00:01:01
```

---

### 2. `GET /publications/v1/balance-delta-high-res`

**Back-up methode.** Voor het ophalen van gemiste data. Max bereik = **4 uur**.

#### Parameters
| Param | In | Type | Required | Example |
|---|---|---|---|---|
| `date_from` | query | string | ✅ | `13-01-2025 00:00:00` |
| `date_to` | query | string | ✅ | `13-01-2025 04:00:00` |
| `Accept` | header | string | ✅ | `application/json` |

**Max range:** 4 uur (240 minuten)

**Date format:** `dd-mm-yyyy hh24:mi:ss` (met Z suffix voor UTC)

**Response formats:** JSON, CSV, XML, XLSX

#### Aanbevolen backfill strategie
Om 24 uur aan data te compileren, roep max 8x per dag aan:
```
00:00 – 04:00, 04:00 – 08:00, 08:00 – 12:00,
12:00 – 16:00, 16:00 – 20:00, 20:00 – 00:00
```

---

## Response Structuur (JSON)

```json
{
  "Response": {
    "informationType": "BALANCE_DELTA_HIGH_RES",
    "period.timeInterval": {
      "start": "2026-03-04T14:26:36Z",
      "end": "2026-03-04T14:56:36Z"
    },
    "TimeSeries": [
      {
        "mRID": 1,
        "quantity_Measurement_Unit_name": "MAW",
        "currency_Unit_name": "EUR",
        "Period": [          ← ARRAY (lijst), niet een enkel object!
          {
            "timeInterval": {
              "start": "2026-03-04T14:26:36Z",
              "end": "2026-03-04T14:56:36Z"
            },
            "points": [      ← lowercase 'points' (niet 'Points')
              { ... },
              { ... }
            ]
          }
        ]
      }
    ]
  }
}
```

> **Let op:** `Period` is een **array** (lijst) en `points` is **lowercase**.
> Dit verschilt van sommige andere TenneT endpoints waar Period een dict is
> en Points met hoofdletter P.

---

## Response Fields (per Point)

| Field | Type | Example | Null? | Description |
|---|---|---|---|---|
| `timeInterval_start` | datetime (UTC) | `2026-03-04T14:26:36Z` | ❌ | Start van het 12s interval |
| `timeInterval_end` | datetime (UTC) | `2026-03-04T14:26:48Z` | ❌ | Eind van het 12s interval |
| `sequence` | string | `4634` | ❌ | Volgnummer (doorlopend) |
| `power_afrr_in` | string | `89.0` | ❌ | aFRR opwaarts vermogen (MW) |
| `power_afrr_out` | string | `0.0` | ❌ | aFRR neerwaarts vermogen (MW) |
| `power_igcc_in` | string | `0.0` | ❌ | IGCC opwaarts vermogen (MW) |
| `power_igcc_out` | string | `0.0` | ❌ | IGCC neerwaarts vermogen (MW) |
| `power_mfrrda_in` | string | `5.0` | ✅ null | mFRRda opwaarts vermogen (MW) |
| `power_mfrrda_out` | string | `2.0` | ✅ null | mFRRda neerwaarts vermogen (MW) |
| `power_picasso_in` | string | `2.0` | ❌ | PICASSO opwaarts vermogen (MW) |
| `power_picasso_out` | string | `6.0` | ❌ | PICASSO neerwaarts vermogen (MW) |
| `power_mari_in` | string | `1.0` | ❌ | MARI opwaarts vermogen (MW) |
| `power_mari_out` | string | `4.0` | ❌ | MARI neerwaarts vermogen (MW) |
| `max_upw_regulation_price` | string | `85.43` | ❌ | Hoogste opwaartse regulatieprijs (EUR/MWh) |
| `min_downw_regulation_price` | string | `-182.53` | ✅ null | Laagste neerwaartse regulatieprijs (EUR/MWh) |
| `mid_price` | string | `2250.00` | ❌ | Middenprijs (EUR/MWh) |

### Verschil met standaard Balance Delta (`/balance-delta`)
- **Extra velden:** `power_mari_in`, `power_mari_out` (MARI platform)
- **Resolutie:** 12 seconden i.p.v. 1 minuut
- **Period:** Array i.p.v. dict
- **Points key:** lowercase `points` i.p.v. uppercase `Points`
- **Null patronen:** `power_mfrrda_in/out` en `min_downw_regulation_price` zijn vaak `null`

---

## Null Handling

Geobserveerde null-patronen (live data 2026-03-04):

| Veld | Null ratio | Toelichting |
|---|---|---|
| `power_mfrrda_in` | 150/150 (100%) | Geen mFRRda activaties in dit interval |
| `power_mfrrda_out` | 150/150 (100%) | Geen mFRRda activaties in dit interval |
| `min_downw_regulation_price` | 150/150 (100%) | Geen neerwaartse regulatie in dit interval |

> **Implementatie:** Null waarden worden als `0` behandeld bij berekening van
> de net balance delta.

---

## Berekening Net Balance Delta

```python
# Per 12s data punt:
total_in  = afrr_in + igcc_in + mfrrda_in + picasso_in + mari_in
total_out = afrr_out + igcc_out + mfrrda_out + picasso_out + mari_out
net_delta = total_in - total_out
```

- **Positief** = opwaartse regulatie (tekort → meer productie nodig)
- **Negatief** = neerwaartse regulatie (overschot → minder productie nodig)

---

## Live Data Voorbeeld (2026-03-04)

### `/latest` response (150 punten, 30 min rolling window)

```
Tijdsbereik:  14:30:48 UTC → 15:00:36 UTC
Punten:       150
Resolutie:    12 seconden

Net Balance Δ:   95.0 – 96.0 MW (constant opwaarts)
Dominante bron:  aFRR IN (89-96 MW)
IGCC/PICASSO:    0.0 MW (inactief)
MARI:            0.0 MW (inactief)
mFRRda:          null (geen activaties)
Mid price:       €2250.00/MWh
Max upw price:   €85.43/MWh
```

### `/balance-delta-high-res` response (4 uur, 1200 punten)

```
Tijdsbereik:  11:03:00 UTC → 15:02:36 UTC
Punten:       1199
Resolutie:    12 seconden

Gemiddelde Δ:  -2.0 MW (licht neerwaarts)
```

---

## Error Codes

| Code | Description |
|---|---|
| 401 | No valid API key found in request |
| 405 | Wrong HTTP Method used |
| 422 | Missing/invalid parameters (bijv. "Period out of bounds") |
| 429 | Rate limit exceeded |
| 503 | Service temporarily unavailable (maintenance) |

### Voorbeeld 422 Error (bereik te groot)
```json
{
  "error_date_time": "2026-03-04T14:59:25+0000",
  "error_id": "9124bf4c-7c81-47e9-8ac5-098bbd9d97f6",
  "error_message": "Period out of bounds, check documentation"
}
```

---

## Security

| Scheme | Type | Header |
|---|---|---|
| `apikey` | API Key | `apikey` header |

---

## Vergelijking Balance Delta Endpoints

| Eigenschap | `/balance-delta` | `/balance-delta-high-res/latest` | `/balance-delta-high-res` |
|---|---|---|---|
| Resolutie | 1 minuut | 12 seconden | 12 seconden |
| Max bereik | 1 dag | 30 min (vast) | 4 uur |
| Rate limit | 1/sec, 60/min | 1/sec, 10/min | 8/dag |
| MARI velden | ❌ | ✅ | ✅ |
| Period type | Dict | Array | Array |
| Points key | `Points` | `points` | `points` |
| Use case | Historisch | Real-time monitoring | Backfill |
| Formats | JSON/CSV/XML/XLSX | JSON only | JSON/CSV/XML/XLSX |

---

## Backfilling (Grote datasets)

Voor het downloaden van grote historische datasets (tot 100 MB) is een optie
beschikbaar op:
[TenneT Download Pagina](https://www.tennet.eu/nl-en/grids-and-markets/transparency-data-netherlands/download-page-transparency)

---

*Laatste update: 2026-03-04 — Gevalideerd met live API calls (acceptance environment)*
