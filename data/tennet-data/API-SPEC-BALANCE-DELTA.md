# TenneT Balance Delta API - OpenAPI Spec Reference

## API Info
- **Title:** Aether - Balance Delta
- **Version:** 1.5.1
- **Base URL:** `https://{environment}.tennet.eu` (environment: `api` of `api.acc`)

## Rate Limits

| | Per Second | Per Minute | Per Day |
|---|---|---|---|
| **Production** | 1 | 24 | 3000 |
| **Acceptance** | 1 | 60 | 3000 |

## Endpoint

### `GET /publications/v1/balance-delta`

**⚠️ Er is GEEN `/latest` endpoint!**

### Parameters
| Param | Type | Required | Example |
|---|---|---|---|
| `date_from` | query string | ✅ | `13-01-2025 00:00:00` |
| `date_to` | query string | ✅ | `14-01-2025 00:00:00` |
| `Accept` | header | ✅ | `application/json` |

**Max range:** 1 dag

**Date format:** `dd-mm-yyyy hh24:mi:ss`

### Response Fields (per Point)

| Field | Type | Example | Description |
|---|---|---|---|
| `timeInterval_start` | datetime | `2025-01-13T00:00` | Start tijdstip |
| `timeInterval_end` | datetime | `2025-01-13T00:15` | Eind tijdstip |
| `sequence` | string | `1` | Volgnummer |
| `power_afrr_in` | string | `29.0` | aFRR opwaarts (MW) |
| `power_afrr_out` | string | `163.0` | aFRR neerwaarts (MW) |
| `power_igcc_in` | string | `0.0` | IGCC opwaarts (MW) |
| `power_igcc_out` | string | `1.0` | IGCC neerwaarts (MW) |
| `power_mfrrda_in` | string | `5.0` | mFRRda opwaarts (MW) |
| `power_mfrrda_out` | string | `2.0` | mFRRda neerwaarts (MW) |
| `power_picasso_in` | string | `2.0` | PICASSO opwaarts (MW) |
| `power_picasso_out` | string | `6.0` | PICASSO neerwaarts (MW) |
| `max_upw_regulation_price` | string | `0.0` | Hoogste opwaartse regulatieprijs (EUR/MWh) |
| `min_downw_regulation_price` | string | `-182.53` | Laagste neerwaartse regulatieprijs (EUR/MWh) |
| `mid_price` | string | `22.69` | Middenprijs (EUR/MWh) |

### Response Formats
- `application/json`
- `application/xml`
- `text/csv`
- `application/xlsx`

### Error Codes
| Code | Description |
|---|---|
| 401 | No valid API key found |
| 405 | Method not allowed |
| 422 | Missing/invalid parameters |
| 429 | Rate limit exceeded |
| 504 | Gateway timeout |
