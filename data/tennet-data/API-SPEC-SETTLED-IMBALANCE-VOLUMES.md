# TenneT Settled Imbalance Volumes API - Spec Reference

## API Info
- **Title:** Aether - Settled Imbalance Volumes
- **Version:** 1.5.0
- **Description:** Volumes afgewikkeld door TenneT TSO met programmaverantwoordelijke partijen (BRPs) per tijdseenheid
- **Base URL:** `https://{environment}.tennet.eu` (environment: `api` of `api.acc`)

## Rate Limits

| | Per Second | Per Minute | Per Day |
|---|---|---|---|
| **Production** | 1 | 5 | 25 |
| **Acceptance** | 1 | 60 | 300 |

> ⚠️ **Production rate limits zijn ZEER strikt** (5/min, 25/dag). Gebruik spaarzaam!

## Endpoint

### `GET /publications/v1/settled-imbalance-volumes`

### Parameters
| Param | Type | Required | Example | Notes |
|---|---|---|---|---|
| `date_from` | query string | ✅ | `13-12-2024 11:00:00` | Start datum |
| `date_to` | query string | ✅ | `13-12-2024 12:00:00` | Eind datum |
| `Accept` | header | ✅ | `application/json` | Response format |

**Max range:** 1 uur

**Date format:** `dd-mm-yyyy hh24:mi:ss`

**Resolution:** PT15M (4 ISPs per uur, 96 per dag)

**Unit:** kWh

## Response Structure (JSON)

```json
{
  "Response": {
    "informationType": "SETTLED_IMBALANCE_VOLUMES",
    "period.timeInterval": {
      "start": "2024-12-13T11:00",
      "end": "2024-12-13T12:00"
    },
    "conversation_id": null,
    "TimeSeries": [
      {
        "mRID": 1,
        "quantity_Measurement_Unit_name": "kWh",
        "Period": {
          "timeInterval": { "start": "...", "end": "..." },
          "Points": [ ... ]
        }
      }
    ]
  }
}
```

> ⚠️ **Period is een DICT** (niet een array). Er is 1 Period per TimeSeries.

## Response Fields

### TimeSeries metadata

| Field | Type | Example | Description |
|---|---|---|---|
| `mRID` | int | `1` | TimeSeries identifier |
| `quantity_Measurement_Unit_name` | string | `"kWh"` | Eenheid voor alle volumes |

### Per Point

| Field | Type | Example | Description |
|---|---|---|---|
| `timeInterval_start` | datetime | `2024-12-13T11:00` | Start tijdstip ISP |
| `timeInterval_end` | datetime | `2024-12-13T11:15` | Eind tijdstip ISP |
| `isp` | string | `"45"` | ISP nummer (1-96 per dag) |
| `surplus` | string | `"1630"` | Totaal surplus (lang) volume in kWh |
| `shortage` | string | `"2012733"` | Totaal shortage (kort) volume in kWh |
| `absolute` | string | `"2014363"` | Absoluut totaal volume in kWh |
| `imbalance` | string | `"-2011103"` | Netto imbalance in kWh (kan negatief) |

> ⚠️ **Alle numerieke velden zijn strings** — altijd parsen naar float/int!
>
> ⚠️ **`imbalance` kan negatief zijn** — negatief = shortage (tekort), positief = surplus (overschot)

### Wiskundige relaties

```
absolute  = surplus + shortage
imbalance = surplus - shortage
```

Deze relaties zijn altijd exact geldig.

### CSV Kolommen
```
Timeinterval Start Loc, Timeinterval End Loc, Isp,
Quantity Measurement Unit, Surplus, Shortage, Absolute, Imbalance
```

## Live Data Voorbeeld (13 december 2024, 11:00-12:00)

### Overzicht
```
4 ISPs (45, 46, 47, 48) = 1 uur data
Alle 4 ISPs: richting SHORTAGE (tekort)
Totaal surplus:   2.5 MWh
Totaal shortage:  8,133.7 MWh
Netto imbalance:  -8,131.2 MWh
```

### Per ISP
```
ISP 45  11:00  surplus=    1.630 MWh  shortage= 2,012.733 MWh  imbalance= -2,011.103 MWh  SHORTAGE
ISP 46  11:15  surplus=    0.229 MWh  shortage= 2,012.719 MWh  imbalance= -2,012.490 MWh  SHORTAGE
ISP 47  11:30  surplus=    0.676 MWh  shortage= 2,028.599 MWh  imbalance= -2,027.923 MWh  SHORTAGE
ISP 48  11:45  surplus=    0.000 MWh  shortage= 2,079.642 MWh  imbalance= -2,079.642 MWh  SHORTAGE
```

> In dit uur is het systeem consistent in **shortage** (tekort). Het surplus is verwaarloosbaar (< 2 MWh) tegenover de shortage (~2,000 MWh per ISP).

## Interpretatie & Gebruik

### Wat zijn Settled Imbalance Volumes?
Na afloop van elke ISP (15 minuten) berekent TenneT de totale onbalans van alle Balance Responsible Parties (BRPs):

- **Surplus (lang):** Totale hoeveelheid energie die BRPs meer leverden dan geprogrammeerd (overproductie + onderverbruik)
- **Shortage (kort):** Totale hoeveelheid energie die BRPs minder leverden dan geprogrammeerd (onderproductie + oververbruik)
- **Imbalance (netto):** Het verschil — positief = netto surplus, negatief = netto tekort

### Relatie met Settlement Prices
De imbalance richting bepaalt welke settlement price van toepassing is:

| Systeem richting | Relevante prijs | Consequentie voor BRP |
|---|---|---|
| **Shortage** (imbalance < 0) | Shortage prijs (hoog) | BRPs met tekort betalen hoge prijs |
| **Surplus** (imbalance > 0) | Surplus prijs (laag) | BRPs met overschot ontvangen lage prijs |

### Relatie met andere endpoints

```
Settled Imbalance Volumes (totale onbalans in kWh per ISP)
    ↕ bepaalt welke prijsrichting van toepassing is
Settlement Prices (imbalance prijzen in EUR/MWh per ISP)
    ↕ prijs × volume = kosten
Balance Delta (real-time onbalans in MW per minuut)
    ↕ geaggregeerd resulteert in
FRR Activations (geactiveerde reserves in kWh per ISP)
```

### Volume vs Energie
- Velden zijn in **kWh** (energie per 15-min ISP)
- Voor vermogen in MW: `kWh / 0.25h = kW → / 1000 = MW`
- Voorbeeld: 2,012,733 kWh per 15 min ≈ 8,051 MW gemiddeld vermogen

## Error Handling

| Status | Betekenis | Oplossing |
|---|---|---|
| 200 | OK | — |
| 401 | Ongeldige API key | Controleer `apikey` header |
| 422 | Ongeldige parameters | Check datumformaat `dd-mm-yyyy hh24:mi:ss` en max range (1 uur) |
| 429 | Rate limit overschreden | Wacht en probeer opnieuw (max 5/min production!) |
| 504 | Gateway Timeout | Server overbelast, probeer later |

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

data = api._make_request('/publications/v1/settled-imbalance-volumes', params)

# Processing
for series in data['Response']['TimeSeries']:
    for point in series['Period']['Points']:
        surplus_kwh = float(point['surplus'])
        shortage_kwh = float(point['shortage'])
        imbalance_kwh = float(point['imbalance'])  # negative = shortage
        absolute_kwh = float(point['absolute'])     # = surplus + shortage
```
