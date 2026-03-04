# TenneT Merit Order List API - Spec Reference

## API Info
- **Title:** Aether - Merit Order List
- **Version:** 1.5.0
- **Description:** Prijzen en volumes van biedingen voor reguleer- en reservecapaciteit (aFRR en mFRRsa) ontvangen door TenneT
- **Base URL:** `https://{environment}.tennet.eu` (environment: `api` of `api.acc`)

## Rate Limits

| | Per Second | Per Minute | Per Day |
|---|---|---|---|
| **Production** | 1 | 10 | 600 |
| **Acceptance** | 1 | 60 | 600 |

## Endpoint

### `GET /publications/v1/merit-order-list`

### Parameters
| Param | Type | Required | Example | Notes |
|---|---|---|---|---|
| `date_from` | query string | ✅ | `13-12-2024 11:00:00` | Start datum |
| `date_to` | query string | ✅ | `13-12-2024 12:00:00` | Eind datum |
| `Accept` | header | ✅ | `application/json` | Response format |

**Max range:** 1 uur

**Date format:** `dd-mm-yyyy hh24:mi:ss`

**Resolution:** PT15M (4 ISPs per uur)

**Units:** MAW (capacity), EUR/MWh (prices)

## Response Structure (JSON)

```json
{
  "Response": {
    "informationType": "MERIT_ORDER_LIST",
    "period.timeInterval": {
      "start": "2024-12-13T11:00",
      "end": "2024-12-13T12:00"
    },
    "conversation_id": null,
    "TimeSeries": [
      {
        "mRID": 1,
        "quantity_Measurement_Unit_name": "MAW",
        "price_Measurement_Unit_name": "MWh",
        "currency_Unit_name": "EUR",
        "Period": {
          "timeInterval": { "start": "...", "end": "..." },
          "Points": [ ... ]
        }
      }
    ]
  }
}
```

> ⚠️ **Period is een DICT** (niet een array zoals bij sommige andere endpoints). Er is 1 Period per TimeSeries.

## Response Fields

### TimeSeries metadata

| Field | Type | Example | Description |
|---|---|---|---|
| `mRID` | int | `1` | TimeSeries identifier |
| `quantity_Measurement_Unit_name` | string | `"MAW"` | Eenheid capaciteit |
| `price_Measurement_Unit_name` | string | `"MWh"` | Eenheid prijs |
| `currency_Unit_name` | string | `"EUR"` | Valuta |

### Per Point

| Field | Type | Example | Description |
|---|---|---|---|
| `timeInterval_start` | datetime | `2024-12-13T11:00` | Start tijdstip ISP |
| `timeInterval_end` | datetime | `2024-12-13T11:15` | Eind tijdstip ISP |
| `isp` | string | `"45"` | ISP nummer (1-96 per dag) |
| `Thresholds` | array | `[...]` | Array van bid drempels |

### Per Threshold

| Field | Type | Example | Description |
|---|---|---|---|
| `capacity_threshold` | string | `"100"` | Capaciteitsdrempel in MAW (≈ MW) |
| `price_up` | string | `"13.130"` | Opwaartse reguleerprijs (EUR/MWh) |
| `price_down` | string \| null | `"1.000"` of `null` | Neerwaartse reguleerprijs (EUR/MWh) |

> ⚠️ **`price_down` kan `null` zijn** bij hoge capaciteitsdrempels! Dit betekent dat er geen neerwaartse biedingen beschikbaar zijn boven die drempel.
>
> ⚠️ **`price_up` kan negatief zijn** (bijv. `-1.000`), wat duidt op biedingen die betalen om opwaarts te reguleren.
>
> ⚠️ **Alle numerieke velden zijn strings** — altijd parsen naar float!

### CSV Kolommen
```
Timeinterval Start Loc, Timeinterval End Loc, Isp,
Quantity Measurement Unit Name, Price Measurement Unit Name, Currency Unit Name,
Capacity Threshold, Price Down, Price Up
```

## Live Data Voorbeeld (13 december 2024, 11:00-12:00)

### Overzicht
```
4 ISPs (45, 46, 47, 48) = 1 uur data
580 totaal bid-drempels
Capaciteit: 1 - 2245 MW
Price up:   -1.000 tot 812.130 EUR/MWh
Price down: -413.130 tot 234.670 EUR/MWh (37% null)
```

### Per ISP
```
ISP 45:  226 drempels, capaciteit 1-2245 MW, 54 null price_down
ISP 46:   64 drempels, capaciteit 1-625 MW,  54 null price_down
ISP 47:  226 drempels, capaciteit 1-2245 MW, 54 null price_down
ISP 48:   64 drempels, capaciteit 1-625 MW,  54 null price_down
```

> Aantal drempels varieert sterk per ISP (64-226). Dit reflecteert het werkelijke aantal unieke capaciteitsniveaus waarvoor biedingen zijn ingediend.

### Voorbeeld: ISP 45 (eerste 5 drempels)
```
Capacity  Price_Up    Price_Down
1 MW      -1.000      234.670     ← negatieve up-prijs, hoge down-prijs
10 MW     -1.000       13.230
20 MW     -1.000        1.000
30 MW     -1.000        1.000
40 MW     -1.000        1.000
```

### Voorbeeld: ISP 48 (laatste 5 drempels)
```
Capacity  Price_Up    Price_Down
590 MW    712.230     null        ← geen neerwaartse biedingen
600 MW    712.230     null
610 MW    712.230     null
620 MW    712.230     null
625 MW    812.130     null        ← hoogste prijs bij max capaciteit
```

### Typisch patroon
- **Lage capaciteit:** lage/negatieve `price_up`, hoge `price_down`
- **Hoge capaciteit:** hoge `price_up`, `price_down` wordt `null`
- **Spread (up - down):** negatief bij lage capaciteit, niet te berekenen bij hoge capaciteit

## Interpretatie & Gebruik

### Wat is de Merit Order List?
De Merit Order List bevat alle ingediende biedingen voor balanceringsenergie (aFRR en mFRRsa). TenneT selecteert de goedkoopste biedingen eerst (merit order principe):

- **Opwaartse regulering (price_up):** kosten om productie te verhogen / verbruik te verlagen
- **Neerwaartse regulering (price_down):** kosten om productie te verlagen / verbruik te verhogen

### Capacity Threshold
Het veld `capacity_threshold` geeft de cumulatieve capaciteit in MW. Bij elke drempel hoort een marginale prijs. Dit vormt de "bid ladder" (biedladder):

```
Prijs (EUR/MWh)
    │
812 ┤                                          ╱ price_up
    │                                    ╱─────╱
712 ┤                              ╱─────╱
    │                        ╱─────╱
    │                  ╱─────╱
    │            ╱─────╱
  0 ┤──────────╱
    │
 -1 ┤────╱
    └──────────────────────────────────────────── Capaciteit (MW)
    0    100   200   300   500   700   1000  2245
```

### Relatie met andere endpoints

```
Merit Order List (biedingen per ISP in EUR/MWh)
    ↕ bepaalt beschikbare reguleerenergie
FRR Activations (geactiveerde volumes in kWh per ISP)
    ↕ gerelateerd aan
Balance Delta (real-time MW per minuut)
    ↕ bepaalt
Settlement Prices (imbalance prijzen per ISP in EUR/MWh)
```

## Error Handling

| Status | Betekenis | Oplossing |
|---|---|---|
| 200 | OK | — |
| 401 | Ongeldige API key | Controleer `apikey` header |
| 422 | Ongeldige parameters | Check datumformaat en max range |
| 429 | Rate limit overschreden | Wacht en probeer opnieuw |

## Code Voorbeeld

```python
from datetime import datetime, timedelta

# Max 1 uur range
end = datetime(2024, 12, 13, 12, 0, 0)
start = end - timedelta(hours=1)

params = {
    'date_from': start.strftime('%d-%m-%Y %H:%M:%S'),
    'date_to': end.strftime('%d-%m-%Y %H:%M:%S')
}

data = api._make_request('/publications/v1/merit-order-list', params)

# Processing
for series in data['Response']['TimeSeries']:
    for point in series['Period']['Points']:
        for t in point['Thresholds']:
            cap = float(t['capacity_threshold'])
            price_up = float(t['price_up']) if t['price_up'] is not None else None
            price_down = float(t['price_down']) if t['price_down'] is not None else None
```
