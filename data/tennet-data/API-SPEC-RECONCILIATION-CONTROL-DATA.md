# TenneT Reconciliation Control Data API - OpenAPI Spec Reference

## API Info
- **Title:** Aether - Reconciliation Control Data
- **Version:** 1.5.0
- **Description:** Voorziet marktpartijen van data om zelf reconciliation prices te berekenen
- **Base URL:** `https://{environment}.tennet.eu` (environment: `api` of `api.acc`)

## Rate Limits (zelfde voor Production & Acceptance)

| | Per Second | Per Minute | Per Day |
|---|---|---|---|
| **Alle omgevingen** | 1 | 12 | 1500 |

## Endpoint

### `GET /publications/v1/reconciliation-control-data`

### Parameters
| Param | Type | Required | Example | Notes |
|---|---|---|---|---|
| `date_from` | query string | ✅ | `13-01-2024 00:00:00` | Start datum |
| `date_to` | query string | ✅ | `13-01-2025 00:00:00` | Eind datum |
| `Accept` | header | ✅ | `application/json` | Response format |

**Max range:** 1 jaar

**Date format:** `dd-mm-yyyy hh24:mi:ss`

**Resolution:** PT15M (96 ISPs per dag)

**Unit:** kWh

## Response Fields (per Point)

| Field | Type | Example | Description |
|---|---|---|---|
| `timeInterval_start` | datetime | `2024-01-13T00:00` | Start tijdstip ISP |
| `timeInterval_end` | datetime | `2024-01-13T00:15` | Eind tijdstip ISP |
| `isp` | integer | `1` | ISP nummer (1-96 per dag) |
| `alloc_up` | string | `5409769` | Allocatie opwaarts (kWh) |
| `alloc_down` | string | `3988725` | Allocatie neerwaarts (kWh) |
| `afrr_up` | string | `678332` | aFRR opwaarts (kWh) |
| `afrr_down` | string | `5409769` | aFRR neerwaarts (kWh) |
| `mfrrda_up` | string | `45678` | mFRRda opwaarts (kWh) |
| `mfrrda_down` | string | `570098` | mFRRda neerwaarts (kWh) |

> ⚠️ **Let op:** `Period` is een **array** (1 per dag)
> ⚠️ **Let op:** Eenheid is **kWh** (niet MW of MWh zoals andere endpoints)
> ⚠️ **Let op:** `isp` is een **integer** (niet string zoals bij andere endpoints)

## Relatie met andere endpoints

Dit endpoint levert de **volumes** waarmee de reconciliation **prices** berekend worden:

```
Reconciliation Control Data (volumes in kWh)
    ↓ berekening
Reconciliation Prices ISP (prijs per ISP in EUR/MWh)
    ↓ aggregatie
Reconciliation Prices Month (maandprijs in EUR/MWh)
```

### Hoe het werkt:
- `alloc_up/down` = totale allocatie volumes (wat BRP's inkopen/verkopen)
- `afrr_up/down` = aFRR activaties die in de reconciliation meegenomen worden
- `mfrrda_up/down` = mFRRda activaties die in de reconciliation meegenomen worden
- De reconciliation prijs is het gewogen gemiddelde van deze volumes × marktprijzen

## Live Data Voorbeeld (1 jan 2025)

```
ISP 1  00:00  alloc_up=3,006,997  alloc_down=2,656,515  afrr_up=0      afrr_down=71,539  mfrrda=0/0
ISP 2  00:15  alloc_up=2,976,210  alloc_down=2,647,506  afrr_up=9,253  afrr_down=7,462   mfrrda=0/0
ISP 3  00:30  alloc_up=2,927,585  alloc_down=2,659,819  afrr_up=62     afrr_down=48,738  mfrrda=0/0
```

alloc_up range jan 2025: 2,118,703 - 4,403,450 kWh per ISP

## Error Codes

| Code | Description |
|---|---|
| 401 | No valid API key found |
| 405 | Method not allowed |
| 422 | Missing/invalid parameters |
| 429 | Rate limit exceeded |
| 504 | Gateway timeout |

## Response Formats
- `application/json`
- `application/xml`
- `text/csv`
- `application/xlsx`

### CSV Kolommen
```
Timeinterval Start Loc, Timeinterval End Loc, Isp, 
Alloc Down, Alloc Up, Afrr Up, Afrr Down, Mfrrda Up, Mfrrda Down
```
