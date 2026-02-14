# 📍 NETBEHEERDER COVERAGE MAP - NEDERLAND

```
╔════════════════════════════════════════════════════════════════╗
║                    NEDERLAND - DSO DEKKING                     ║
╚════════════════════════════════════════════════════════════════╝

         FRIESLAND                  GRONINGEN
         [Liander]                  [Enexis]
              ╲                        ╱
               ╲                      ╱
                ╲                    ╱
         NOORD-HOLLAND           DRENTHE
           [Liander]            [Enexis]
                │
                │
         FLEVOLAND              OVERIJSSEL
          [Liander]             [diverse]
                │                   │
                │                   │
         UTRECHT              GELDERLAND
         [Stedin]              [Liander]
            │                      │
            │                      │
      ZUID-HOLLAND           NOORD-BRABANT
        [Stedin]               [Enexis]
            │                      │
            │                      │
         ZEELAND                LIMBURG
        [Stedin]               [Enexis]


╔════════════════════════════════════════════════════════════════╗
║                     COVERAGE STATISTIEKEN                      ║
╚════════════════════════════════════════════════════════════════╝

1️⃣  LIANDER (Alliander)
    ├─ Aansluitingen: 3.1 miljoen (37% van NL)
    ├─ Provincies: Noord-Holland, Gelderland, 
    │               Flevoland, Friesland
    ├─ Open Data: ✅ CSV downloads beschikbaar
    └─ Prioriteit: ⭐⭐⭐⭐⭐ HOOGSTE

2️⃣  ENEXIS
    ├─ Aansluitingen: 2.8 miljoen (33% van NL)
    ├─ Provincies: Noord-Brabant, Limburg, Groningen,
    │               delen van Drenthe/Overijssel
    ├─ Open Data: ✅ CSV downloads via EDSN
    └─ Prioriteit: ⭐⭐⭐⭐⭐ HOOGSTE

3️⃣  STEDIN
    ├─ Aansluitingen: 2.5 miljoen (30% van NL)
    ├─ Provincies: Zuid-Holland, Utrecht, Zeeland
    ├─ Open Data: ✅ Transportvolumes + Capaciteitskaart
    └─ Prioriteit: ⭐⭐⭐⭐⭐ HOOGSTE

TOTAAL: 8.4 miljoen = 100% van Nederlandse huishoudens!


╔════════════════════════════════════════════════════════════════╗
║                  🏆 EDSN = MASTER KEY                          ║
╚════════════════════════════════════════════════════════════════╝

EDSN (Energie Data Services Nederland) aggregeert data van:
✅ Liander    ✅ Enexis     ✅ Stedin
✅ Coteq      ✅ Westland   ✅ Rendo
✅ ALLE andere kleine netbeheerders

→ ÉÉN API = 100% Nederland gedekt!
→ Postcodegebied-niveau
→ Historische + actuele data

Conclusie: Start met EDSN, vul aan met DSO-specifieke data


╔════════════════════════════════════════════════════════════════╗
║              POSTCODE NIVEAU GRANULARITEIT                     ║
╚════════════════════════════════════════════════════════════════╝

CBS Data:           📊 NATIONAAL / PROVINCIAAL
                       ├─ Totaal NL: 123 TWh/jaar
                       ├─ Per provincie trends
                       └─ Macro statistieken

DSO Open Data:      📍 POSTCODEGEBIED (4-cijferig)
                       ├─ 1234: 145 MWh/jaar
                       ├─ 2000: 892 MWh/jaar  
                       └─ ~1000 postcodegebieden

EDSN Data:          📍 POSTCODEGEBIED (4-cijferig)
                       ├─ Kleinverbruik
                       ├─ Grootverbruik
                       ├─ Teruglevering
                       └─ Alle DSO's gecombineerd!

Liander Data:       📍 POSTCODEGEBIED (6-cijferig!)
                       ├─ 1234AB: 23 MWh
                       ├─ 1234CD: 31 MWh
                       └─ Ultra-granular!


╔════════════════════════════════════════════════════════════════╗
║                   DATA COMBINATIE STRATEGIE                    ║
╚════════════════════════════════════════════════════════════════╝

Layer 1: CBS (Foundation)
    └─ Totale productie NL: 50 GW solar, 8 GW wind
       Historische trends, capaciteit groei

Layer 2: EDSN (Regional)
    └─ Postcodegebied 1012: 2.3 MWh/dag verbruik
       Postcodegebied 3011: 4.1 MWh/dag teruglevering
       
Layer 3: DSO Open Data (Detailed)
    └─ Liander 1012AB: 45 zonnepanelen installaties
       Enexis 5611: Netcongestie tijdens zomermaanden

Layer 4: TenneT/ENTSO-E (Prices)
    └─ 13:00 uur: €-0.05/kWh (overproductie solar)
       18:00 uur: €0.25/kWh (avondpiek)

COMBINATIE = ARBITRAGE KANSEN DETECTIE! 🎯


╔════════════════════════════════════════════════════════════════╗
║                    CONCRETE USE CASE                           ║
╚════════════════════════════════════════════════════════════════╝

Scenario: Zonnige zomerdag - 12 juni 2025, 13:00 uur

1️⃣  Weer Data (Open-Meteo)
    → 850 W/m² zonnestraling
    → Weinig bewolking
    → Voorspelling: blijft stabiel 12:00-15:00

2️⃣  CBS Data (84575NED)
    → Nederland heeft 22 GW solar geïnstalleerd
    → Max productie mogelijk: ~18 GW (op dit moment)

3️⃣  EDSN Data (postcode 1012 - Amsterdam centrum)
    → Normaal verbruik: 12 MW
    → Solar teruglevering: 18 MW
    → NET RESULTAAT: +6 MW overproductie

4️⃣  Liander Data (Amsterdam regio)
    → 12.000 zonnepanelen installaties
    → Capaciteitskaart: netcongestie waarschijnlijk

5️⃣  ENTSO-E Prijs Data
    → Day-ahead prijs: €0.02/kWh
    → Imbalance prijs: €-0.08/kWh (NEGATIEF!)

🎯 ARBITRAGE KANS:
   → Koop stroom op €-0.08 (word betaald!)
   → Opslag in batterij
   → Verkoop om 18:00 op €0.25
   → Marge: €0.33/kWh (!!!)

Dit is PRECIES waarvoor je deze data nodig hebt! 💰
```
