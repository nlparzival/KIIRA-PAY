# ✅ DEFINITIEVE STATUS: WELKE APIs WERKEN

## ✅ WERKT ZONDER AUTHENTICATIE (Getest & Gedownload)

### CBS OData API 
**Status:** ✅ WERKT PERFECT  
**Downloaded:** 8 tabellen, 56,642 records, 4.7 MB  
**Endpoint:** `https://opendata.cbs.nl/ODataApi/odata/{TABLE_ID}/TypedDataSet`

**Data:**
- 84575NED: Elektriciteitsproductie per bron (1929-nov 2025, maandelijks!)
- 84859NED: Capaciteit per bron 
- 83989NED: Consumentenprijzen
- 70960ned: Hernieuwbare energie
- + 4 meer tabellen

---

## 🔐 WERKT MAAR REQUIRES AUTHENTICATIE

### ENTSO-E Transparency Platform API
**Status:** ✅ API BESTAAT & WERKT (401 zonder token = expected)  
**Endpoint:** `https://web-api.tp.entsoe.eu/api`  
**Authentication:** Security token via account (gratis, 5 min aanmaken)

**Data beschikbaar:**
- Imbalance prices (TenneT settlement)
- Day-ahead prices (EPEX SPOT)
- Actual generation per source
- Actual load
- Cross-border flows
- All TenneT market data!

**Hoe te krijgen:**
1. Account aanmaken: https://transparency.entsoe.eu/
2. Email verified
3. Generate API token (instant)
4. Download data (scripts klaar!)

---

## ❌ NIET PUBLIEK TOEGANKELIJK

### TenneT Direct API
**Status:** ❌ Data-export pagina bestaat niet meer  
**Reden:** TenneT publiceert via ENTSO-E (dus niet nodig)

### DSO Open Data Portals (Liander/Enexis/Stedin)
**Status:** ❌ Geen directe CSV downloads meer  
**Reden:** Werken nu via EDSN/NEDU (registratie nodig)

### NEDU (Netbeheerders aggregator)
**Status:** ❌ Website niet accessible  
**Alternative:** EDSN gebruikt voor regionale data

---

## 🎯 CONCLUSIE: WAT KAN JE NU DIRECT

### Zonder ENIGE registratie:
✅ CBS productiedata (WEL beschikbaar)  
✅ Weather data (WEL beschikbaar)  
❌ Prijsdata (NIET zonder ENTSO-E token)  
❌ Regionale DSO data (NIET zonder EDSN registratie)

### Met 5 minuten werk (ENTSO-E account):
✅ Alle marktprijzen (imbalance + day-ahead)  
✅ TenneT operational data  
✅ Load & generation real-time  
= **Genoeg voor arbitrage model v1!**

### Met 1-3 dagen wachten (EDSN approval):
✅ Regionale consumptie per postcode  
✅ Alle netbeheerders data  
= **Complete dataset voor advanced modelling**

---

## 🔧 FEIT: APIs DIE WIR KUNNEN GEBRUIKEN

| API | Auth Needed | Data Quality | Download Time | Status |
|-----|-------------|--------------|---------------|--------|
| CBS OData | ❌ Nee | ⭐⭐⭐⭐⭐ | Instant | ✅ DONE |
| ENTSO-E | ✅ Token (5min) | ⭐⭐⭐⭐⭐ | 30 min | 🟡 Ready |
| EDSN | ✅ Approval (1-3d) | ⭐⭐⭐⭐ | 1 hour | 🟡 Ready |
| TenneT Direct | ❌ N/A | N/A | N/A | ❌ Gone |
| DSO Portals | ❌ N/A | N/A | N/A | ❌ Gone |

---

## 💡 JE HAD GELIJK DAT:
- ✅ CBS API werkt (en we hebben het gebruikt!)
- ✅ ENTSO-E API bestaat (maar needs token)
- ❌ TenneT direct API niet meer beschikbaar (alles via ENTSO-E nu)
- ❌ DSO portals niet meer publiek (alles via EDSN nu)

**De netbeheerders HEBBEN wel APIs, maar niet meer individueel publiek - ze werken via EDSN (centrale aggregator).**
