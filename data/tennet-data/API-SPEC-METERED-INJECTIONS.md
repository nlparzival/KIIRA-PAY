# TenneT Metered Injections & Scheduled Exchanges API - Spec Reference

## API Info
- **Title:** Aether - Metered Injections and Scheduled Exchanges
- **Version:** 1.5.0
- **Description:** Gemeten invoeding als zichtbare belasting (consumptie) op het transmissienet van Nederland per markt-tijdseenheid, gebaseerd op meetberichten. Load = Feed-in − Export + Import.
- **Base URL:** `https://{environment}.tennet.eu` (environment: `api` of `api.acc`)

## Rate Limits

| | Per Second | Per Minute | Per Day |
|---|---|---|---|
| **Production** | 1 | 5 | 25 |
| **Acceptance** | 1 | 60 | 300 |

> ⚠️ **Production rate limits zijn ZEER strikt** (5/min, 25/dag). Gebruik spaarzaam!

## Endpoint

### `GET /publications/v1/metered-injections`

### Parameters
| Param | Type | Required | Example | Notes |
|---|---|---|---|---|
| `date_from` | query string | ✅ | `13-12-2024 00:00:00` | Start datum |
| `date_to` | query string | ✅ | `14-12-2024 00:00:00` | Eind datum |
| `Accept` | header | ✅ | `application/json` | Response format |

**Max range:** 1 dag

**Date format:** `dd-mm-yyyy hh24:mi:ss`

**Resolution:** PT15M (96 ISPs per dag)

**Unit:** MWh

## Response Structure (JSON)

```json
{
  "Response": {
    "informationType": "METERED_INJECTIONS",
    "period.timeInterval": {
      "start": "2024-12-13T00:00",
      "end": "2024-12-14T00:00"
    },
    "conversation_id": null,
    "TimeSeries": [
      {
        "mRID": 1,
        "quantity_Measurement_Unit_name": "MWh",
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
| `quantity_Measurement_Unit_name` | string | `"MWh"` | Eenheid voor alle velden |

### Per Point

| Field | Type | Example | Description |
|---|---|---|---|
| `timeInterval_start` | datetime | `2024-12-13T00:00` | Start tijdstip ISP |
| `timeInterval_end` | datetime | `2024-12-13T00:15` | Eind tijdstip ISP |
| `isp` | string | `"1"` | ISP nummer (1-96 per dag) |
| `measured_infeed` | string | `"2025.200"` | Gemeten invoeding (MWh, altijd ≥ 0) |
| `scheduled_import` | string | `"329.875"` | Geplande import vanuit buurlanden (MWh, ≥ 0) |
| `scheduled_export` | string | `"-175.000"` | Geplande export naar buurlanden (MWh, ≤ 0) |

> ⚠️ **Alle numerieke velden zijn strings** — altijd parsen naar float!
>
> ⚠️ **`scheduled_export` is negatief** (conventie) — export = uitstroom
>
> ⚠️ **`scheduled_import` is positief** — import = instroom

### Afgeleide waarde: Netbelasting (Load)

```
Load = measured_infeed − scheduled_export + scheduled_import
```

Omdat `scheduled_export` negatief is, wordt dit in de praktijk:
```
Load = infeed + |export| + import
```

### CSV Kolommen
```
Timeinterval Start Loc, Timeinterval End Loc, Isp,
Quantity Measurement Unit Name, Measured Infeed, Scheduled Import, Scheduled Export
```

## Live Data Voorbeeld (13 december 2024, volledig dag)

### Overzicht
```
96 ISPs (ISP 1-96) = 24 uur data
Gem. Infeed:       2,466 MWh per ISP
Gem. Netbelasting: 2,653 MWh per ISP
Totaal Import:     8,362 MWh (dag)
Totaal Export:    -9,623 MWh (dag)
Netto: Nederland was netto exporteur deze dag
```

### Bereik per veld
```
measured_infeed:  1,813 - 3,014 MWh  (dagprofiel met piek overdag)
scheduled_import:     0 - 330 MWh    (56 van 96 ISPs met import)
scheduled_export: -255 - 0 MWh       (68 van 96 ISPs met export)
net_load:         1,816 - 3,265 MWh
```

### Voorbeeld: Ochtend, middag, avond
```
ISP  1  00:00  infeed=2,025  import= 330  export=   0  load=2,355 MWh  ← nacht, import
ISP 48  11:45  infeed=2,878  import=   0  export=-175  load=3,053 MWh  ← piek, export
ISP 96  23:45  infeed=2,074  import=   0  export=-175  load=2,249 MWh  ← avond, export
```

### Typisch dagpatroon
- **Nacht (ISP 1-24):** Lage infeed (~2,000 MWh), voornamelijk import
- **Dag (ISP 25-72):** Hoge infeed (~2,800-3,000 MWh), voornamelijk export
- **Avond (ISP 73-96):** Dalende infeed, export/import wisselend

## Interpretatie & Gebruik

### Wat zijn Metered Injections?
De **measured infeed** representeert de totale gemeten invoeding op het Nederlandse transmissienet. Dit is de basisbelasting (productie) zichtbaar op het hoogspanningsnet.

- **Measured Infeed:** Totale productie die het transmissienet binnenkomt
- **Scheduled Import:** Geplande elektriciteitsimport vanuit buurlanden (Duitsland, België, Noorwegen, UK)
- **Scheduled Export:** Geplande elektriciteitsexport naar buurlanden (negatief)

### Cross-Border Positie
De netto cross-border positie wordt berekend als:
```
Netto cross-border = scheduled_import + scheduled_export
```
- **Positief:** Nederland importeert netto
- **Negatief:** Nederland exporteert netto

### Relatie met andere endpoints

```
Metered Injections (productie & cross-border flows in MWh per ISP)
    ↕ productie bepaalt aanbod
Balance Delta (real-time onbalans in MW per minuut)
    ↕ afwijking van planning
FRR Activations (geactiveerde reserves in kWh per ISP)
    ↕ correctie op onbalans
Settlement Prices (imbalance prijzen in EUR/MWh per ISP)
```

### Vermogensberekening
- Velden zijn in **MWh per 15-min ISP**
- Voor gemiddeld vermogen in MW: `MWh / 0.25h = MW × 4`
- Voorbeeld: 2,466 MWh per 15 min ≈ 9,864 MW gemiddeld vermogen

## Error Handling

| Status | Betekenis | Oplossing |
|---|---|---|
| 200 | OK | — |
| 401 | Ongeldige API key | Controleer `apikey` header |
| 422 | Ongeldige parameters | Check datumformaat `dd-mm-yyyy hh24:mi:ss` en max range (1 dag) |
| 429 | Rate limit overschreden | Wacht en probeer opnieuw (max 5/min production!) |
| 504 | Gateway Timeout | Server overbelast, probeer later |

## Code Voorbeeld

```python
from datetime import datetime, timedelta

# Max 1 dag range
end = datetime(2024, 12, 14, 0, 0, 0)
start = end - timedelta(days=1)

params = {
    'date_from': start.strftime('%d-%m-%Y %H:%M:%S'),
    'date_to': end.strftime('%d-%m-%Y %H:%M:%S')
}

data = api._make_request('/publications/v1/metered-injections', params)

# Processing
for series in data['Response']['TimeSeries']:
    for point in series['Period']['Points']:
        infeed = float(point['measured_infeed'])
        sched_import = float(point['scheduled_import'])
        sched_export = float(point['scheduled_export'])  # negative
        net_load = infeed - sched_export + sched_import
```
