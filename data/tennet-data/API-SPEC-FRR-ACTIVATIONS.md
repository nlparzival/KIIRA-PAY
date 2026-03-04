# TenneT Frequency Restoration Reserve Activations API - Spec Reference

## API Info
- **Title:** Aether - Frequency Restoration Reserve Activations
- **Version:** 1.5.0
- **Description:** Volumes van geactiveerde balanceringsenergie, settled reserve en noodenergie
- **Base URL:** `https://{environment}.tennet.eu` (environment: `api` of `api.acc`)

## Rate Limits (zelfde voor Production & Acceptance)

| | Per Second | Per Minute | Per Day |
|---|---|---|---|
| **Alle omgevingen** | 1 | 60 | 1500 |

## Endpoint

### `GET /publications/v1/frequency-restoration-reserve-activations`

> ⚠️ **NIET** `/frr-activated-volumes` — dat endpoint bestaat niet (404)!

### Parameters
| Param | Type | Required | Example | Notes |
|---|---|---|---|---|
| `date_from` | query string | ✅ | `13-01-2025 00:00:00` | Start datum |
| `date_to` | query string | ✅ | `14-01-2025 00:00:00` | Eind datum |
| `Accept` | header | ✅ | `application/json` | Response format |

**Max range:** 1 dag

**Date format:** `dd-mm-yyyy hh24:mi:ss`

**Resolution:** PT15M (96 ISPs per dag)

**Unit:** kWh

## Response Fields (per Point)

| Field | Type | Example | Description |
|---|---|---|---|
| `timeInterval_start` | datetime | `2025-01-13T00:00` | Start tijdstip ISP |
| `timeInterval_end` | datetime | `2025-01-13T00:15` | Eind tijdstip ISP |
| `isp` | string | `1` | ISP nummer (1-96 per dag) |
| `aFRR_up` | string | `77` | aFRR opwaarts geactiveerd (kWh) |
| `aFRR_down` | string | `161` | aFRR neerwaarts geactiveerd (kWh, typisch negatief) |
| `mfrrda_volume_up` | string | `190` | mFRRda opwaarts geactiveerd (kWh) |
| `mfrrda_volume_down` | string | `165` | mFRRda neerwaarts geactiveerd (kWh, typisch negatief) |
| `total_volume` | string | `424` | Netto totaal volume (kWh, positief=up, negatief=down) |
| `absolute_total_volume` | string | `253` | Absoluut totaal volume (kWh) |

> ⚠️ **Let op:** `aFRR_down` en `mfrrda_volume_down` zijn typisch **negatieve** waarden!
> ⚠️ **Let op:** Veldnamen gebruiken `aFRR_up` (met hoofdletter F, R, R) — niet `afrr_up`!

### CSV Kolommen
```
Timeinterval Start Loc, Timeinterval End Loc, Isp, 
Quantity Measurement Unit Name, Afrr Down, Afrr Up, 
Incident Reserve Down, Incident Reserve Up, 
Absolute Total Volume, Total Volume
```

> CSV bevat ook `Incident Reserve Up/Down` — niet in JSON response fields!

## Live Data Voorbeeld (3 maart 2026)

```
ISP  1  00:00  aFRR_up=234     aFRR_down=-12,068  mfrrda=0/0    total=-11,834  abs=12,302
ISP  2  00:15  aFRR_up=0       aFRR_down=-10,936  mfrrda=0/0    total=-10,936  abs=10,936
ISP  3  00:30  aFRR_up=0       aFRR_down=-34,922  mfrrda=0/0    total=-34,922  abs=34,922
```

> 3 maart 2026 nacht: consistent neerwaartse regulatie (overschot aan energie)

## Relatie met andere endpoints

```
FRR Activations (volumes in kWh per ISP)
    ↕ gerelateerd aan
Balance Delta (real-time MW per minuut)
    ↕ bepaalt
Settlement Prices (imbalance prijzen per ISP in EUR/MWh)
```

- **FRR Activations** = hoeveel reserve-energie per ISP geactiveerd is
- **Balance Delta** = real-time grid balans (aFRR/IGCC/mFRRda per minuut)
- **Settlement Prices** = de afgerekende onbalansprijzen

## Error Codes

| Code | Description |
|---|---|
| 401 | No valid API key found |
| 405 | Method not allowed |
| 422 | Missing/invalid parameters |
| 429 | Rate limit exceeded |
| 504 | Gateway timeout |
