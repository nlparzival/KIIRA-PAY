# CBS Open Data Integratie voor KIIRA-PAY

## 📁 Structuur

```
cbs-data/
├── README.md                          # Dit bestand
├── CBS_DATASETS.md                    # Overzicht van alle relevante datasets
├── ADDITIONAL_DATA_SOURCES.md         # Extra databronnen
├── cbs_api.py                         # CBS API client class
├── download_missing.py                # Script om ontbrekende datasets te downloaden
├── download_all_data.py               # Bulk download script
└── data/
    └── complete/                      # Alle gedownloade CBS datasets
        ├── energie/                   # Energieproductie & verbruik
        ├── hernieuwbaar/              # Hernieuwbare energie
        ├── co2/                       # CO2 uitstoot
        ├── verbruik/                  # Energieverbruik
        ├── prijzen/                   # Energieprijzen
        ├── warmte/                    # Warmte
        ├── bouw/                      # Bouwsector
        ├── economie/                  # Economische data
        └── ...                        # Overige categorieën
```

## 📊 Status (maart 2026)

- [x] Dataset selectie & prioritering
- [x] CBS API client (`cbs_api.py`)
- [x] Alle must-have datasets gedownload
- [x] Alle should-have datasets gedownload
- [x] Bulk download (~807 datasets, ~4GB lokaal)
- [ ] Dashboard integratie
- [ ] Visualisaties

## ⚠️ Grote bestanden (niet op GitHub)

**16 datasets zijn te groot voor GitHub** (>50MB) en staan in `.gitignore`.
Deze bestanden staan wél lokaal maar worden NIET mee-gepusht naar GitHub.

Ze kunnen altijd opnieuw gedownload worden via de CBS API (zie hieronder).

### Overzicht grote bestanden

| Dataset | Categorie | Grootte | Bestand |
|---------|-----------|---------|---------|
| 85140NED | energie | 450 MB | `85140NED_full_data.json` |
| 85698NED | hernieuwbaar | 163 MB | `85698NED_full_data.csv` |
| 83989ENG | energie | 121 MB | `83989ENG_full_data.json` |
| 83989NED | energie | 119 MB | `83989NED_full_data.json` |
| 82059NED | energie | 113 MB | `82059NED_full_data.json` |
| 85534NED | hernieuwbaar | 94 MB | `85534NED_full_data.json` |
| 82061NED | energie | 64 MB | `82061NED_full_data.json` |
| 86159NED | verbruik | 62 MB | `86159NED_full_data.json` |
| 85999NED | energie | 61 MB | `85999NED_full_data.json` |
| 85697NED | energie | 61 MB | `85697NED_full_data.json` |
| 85359NED | energie | 60 MB | `85359NED_full_data.json` |
| 85677NED | energie | 52 MB | `85677NED_full_data.json` |
| 85337NED | energie | 51 MB | `85337NED_full_data.json` |
| 85126NED | energie | 51 MB | `85126NED_full_data.json` |
| 84837NED | energie | 51 MB | `84837NED_full_data.json` |
| 82505NED | co2 | 51 MB | `82505NED_full_data.json` |

**Totaal: ~1.6 GB** aan lokale data die niet op GitHub staat.

### Hoe deze bestanden opnieuw downloaden

```bash
cd data/cbs-data
python3 download_missing.py
```

Of handmatig per dataset:

```python
from cbs_api import CBS_API
api = CBS_API()
data = api.get_dataset_data("85140NED")  # Vervang met dataset ID
```

## 🔗 Links

- **CBS Open Data Portal**: https://opendata.cbs.nl/
- **OData API Docs**: https://www.cbs.nl/nl-nl/onze-diensten/open-data/databank-cbs-statline-als-open-data
- **API Base URL**: https://opendata.cbs.nl/ODataApi/odata/

## 🎯 Doel

CBS data toevoegen aan KIIRA-PAY dashboard voor:
- Nederlandse energiemix (productie per bron)
- Hernieuwbare energie trends
- Import/export balans
- Prijsontwikkeling elektriciteit en gas
- CO2-uitstoot data
- Historische context voor real-time TenneT data
