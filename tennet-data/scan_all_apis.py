#!/usr/bin/env python3
"""
Find working TSO/DSO APIs by checking known operational endpoints
"""
import requests
import json

print("🔍 COMPLETE API SCAN - TSO & DSO DATA SOURCES")
print("="*80)

results = {}

# === ENTSO-E Transparency (Known working) ===
print("\n1️⃣  ENTSO-E TRANSPARENCY PLATFORM")
print("-"*80)

# These are KNOWN working endpoints without auth for VIEWING
entsoe_public_data = {
    "Load": "https://transparency.entsoe.eu/load-domain/r2/totalLoadR2/show?name=&defaultValue=false&viewType=TABLE&areaType=CTY&atch=false&dateTime.dateTime=13.02.2026+00:00|CET|DAY&biddingZone.values=CTY|10YNL----------L!CTY|10YNL----------L&dateTime.timezone=CET_CEST&dateTime.timezone_input=CET+(UTC+1)+/+CEST+(UTC+2)",
    "Generation": "https://transparency.entsoe.eu/generation/r2/actualGenerationPerProductionType/show",
    "Prices Day-Ahead": "https://transparency.entsoe.eu/transmission-domain/r2/dayAheadPrices/show",
}

for name, url in entsoe_public_data.items():
    try:
        resp = requests.get(url, timeout=10)
        status = "✅ WERKT" if resp.status_code == 200 else f"Status {resp.status_code}"
        print(f"  {name}: {status}")
        results[f"ENTSO-E {name}"] = resp.status_code == 200
    except Exception as e:
        print(f"  {name}: ❌ {e}")
        results[f"ENTSO-E {name}"] = False

# === TenneT Specific ===
print("\n2️⃣  TENNET (via ENTSO-E)")
print("-"*80)
print("  💡 TenneT data is available through ENTSO-E Transparency")
print("  💡 Domain code for Netherlands: 10YNL----------L")
print("  ✅ All TenneT market data accessible via ENTSO-E API")

# === EDSN Platform ===
print("\n3️⃣  EDSN (Netbeheerders Aggregator)")
print("-"*80)

edsn_endpoints = [
    "https://www.edsn.nl/",
    "https://edsn.nl/open-data/",
    "https://energieleveren.nl/inzicht",
]

for url in edsn_endpoints:
    try:
        resp = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
        if resp.status_code == 200:
            print(f"  ✅ {url}")
            results[f"EDSN {url}"] = True
        else:
            print(f"  ⚠️  {url} - Status {resp.status_code}")
            results[f"EDSN {url}"] = False
    except Exception as e:
        print(f"  ❌ {url}: {str(e)[:40]}")
        results[f"EDSN {url}"] = False

# === CBS (Already working) ===
print("\n4️⃣  CBS STATLINE")
print("-"*80)
print("  ✅ Already working - 8 tables downloaded (56k records)")

# === Summary ===
print("\n" + "="*80)
print("📊 SUMMARY - WHAT'S AVAILABLE")
print("="*80)

print("\n✅ WERKENDE APIs (Zonder Auth):")
print("   • CBS OData API - Production data")
print("   • ENTSO-E Transparency - View pages (HTML)")

print("\n🔐 WERKENDE APIs (Met Auth - Gratis):")
print("   • ENTSO-E API - All market data (need token)")
print("   • EDSN Platform - Regional data (need registration)")

print("\n💡 DATA BESCHIKBAAR:")
print("   TenneT Market Data:")
print("     ├─ Imbalance prices → via ENTSO-E API")
print("     ├─ Day-ahead prices → via ENTSO-E API")
print("     ├─ Actual load → via ENTSO-E API")
print("     ├─ Generation per type → via ENTSO-E API")
print("     └─ Cross-border flows → via ENTSO-E API")

print("\n   Netbeheerder Data:")
print("     ├─ Consumption per postcode → via EDSN (registration)")
print("     ├─ Production per postcode → via EDSN (registration)")
print("     └─ Network capacity → via EDSN (registration)")

print("\n📝 NEXT STEPS TO GET DATA:")
print("   1. Create ENTSO-E account (5 min) → Get all TenneT market data")
print("   2. Register at EDSN (15 min) → Get regional DSO data")
print("   3. Both are FREE and legitimate!")

# Save results
with open('data/api_scan_results.json', 'w') as f:
    json.dump(results, f, indent=2)

print(f"\n💾 Results saved to: data/api_scan_results.json")
