# CBS Open Data Integratie voor KIIRA-PAY

## 📁 Structuur

Deze directory bevat alle CBS (Centraal Bureau voor de Statistiek) data integratie voor het KIIRA-PAY Energy Dashboard.

```
cbs-data/
├── README.md                    # Dit bestand
├── CBS_DATASETS.md             # Overzicht van alle relevante datasets
├── cbs_api.py                  # CBS API client class
├── test_cbs_api.py             # Test scripts voor CBS endpoints
├── examples/                   # Voorbeeld queries en outputs
└── data/                       # Cached CBS data (optioneel)
```

## 🎯 Doel

CBS data toevoegen aan KIIRA-PAY dashboard voor:
- Nederlandse energiemix (productie per bron)
- Hernieuwbare energie trends
- Import/export balans
- Prijsontwikkeling elektriciteit en gas
- Historische context voor real-time TenneT data

## 🔗 Links

- **CBS Open Data Portal**: https://opendata.cbs.nl/
- **OData API Docs**: https://www.cbs.nl/nl-nl/onze-diensten/open-data/databank-cbs-statline-als-open-data
- **API Base URL**: https://opendata.cbs.nl/ODataApi/odata/

## 📊 Status

- [ ] Dataset selectie
- [ ] API client implementatie
- [ ] Test scripts
- [ ] Dashboard integratie
- [ ] Visualisaties

## 🚀 Volgende Stappen

1. Documenteer alle relevante CBS datasets in `CBS_DATASETS.md`
2. Bouw CBS API client (`cbs_api.py`)
3. Test alle endpoints (`test_cbs_api.py`)
4. Integreer in hoofddashboard (`/tennet-data/dashboard.py`)
