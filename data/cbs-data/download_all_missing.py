#!/usr/bin/env python3
"""
CBS Bulk Download — Download ALLE missende datasets uit de catalogus.
780 datasets in ~50 minuten met paginering en hervatting.

Features:
- Paginated downloads ($top/$skip) — voorkomt CBS HTTP 500 errors
- Hervatbaar: slaat voortgang op, skipt al gedownloade datasets
- Rate limiting: 0.3s tussen pagina's, 0.5s tussen datasets
- Robuuste error handling met retry
- Live voortgangsrapportage
"""

import requests
import pandas as pd
import json
import os
import time
import sys
from pathlib import Path
from datetime import datetime

# ============================================================================
# CONFIGURATIE
# ============================================================================

DATA_DIR = Path(__file__).parent / "data" / "complete"
CATALOG_FILE = Path(__file__).parent / "cbs_datasets_categorized.json"
PROGRESS_FILE = DATA_DIR / "download_progress_bulk.json"
SUMMARY_FILE = DATA_DIR / "download_summary_bulk.json"

API_BASE = "https://opendata.cbs.nl/ODataApi/odata"
PAGE_SIZE = 5000          # Max rows per API call (CBS limit)
RATE_LIMIT_PAGE = 0.3     # Seconds between pages
RATE_LIMIT_DATASET = 0.5  # Seconds between datasets
REQUEST_TIMEOUT = 60      # Seconds per request
MAX_RETRIES = 3           # Retries per failed request

# Categorie mapping voor opslaglocatie
CATEGORY_MAP = {
    'energie': 'energie',
    'hernieuwbaar': 'hernieuwbaar',
    'prijzen': 'prijzen',
    'co2': 'co2',
    'verbruik': 'verbruik',
    'productie': 'productie',
    'economie': 'arbeid',    # Economie → arbeid map (bestaande dir)
    'woningen': 'woningen',
}

# ============================================================================
# SESSION
# ============================================================================

session = requests.Session()
session.headers.update({
    'User-Agent': 'KIIRA-PAY-BulkDownload/2.1',
    'Accept': 'application/json'
})

# ============================================================================
# HELPERS
# ============================================================================

def get_local_datasets():
    """Scan welke datasets al lokaal staan."""
    local = set()
    if DATA_DIR.is_dir():
        for cat_dir in DATA_DIR.iterdir():
            if cat_dir.is_dir() and not cat_dir.name.startswith('.'):
                for ds_dir in cat_dir.iterdir():
                    if ds_dir.is_dir():
                        csv = ds_dir / f"{ds_dir.name}_full_data.csv"
                        if csv.exists() and csv.stat().st_size > 100:
                            local.add(ds_dir.name)
    return local


def load_progress():
    """Laad voortgang van eerder gestopte run."""
    if PROGRESS_FILE.exists():
        with open(PROGRESS_FILE) as f:
            return json.load(f)
    return {'completed': [], 'failed': [], 'skipped': []}


def save_progress(progress):
    """Sla voortgang op."""
    with open(PROGRESS_FILE, 'w') as f:
        json.dump(progress, f, indent=2)


def get_missing_datasets():
    """Bouw lijst van alle missende datasets uit catalogus."""
    with open(CATALOG_FILE) as f:
        catalog = json.load(f)
    
    local = get_local_datasets()
    
    missing = []
    seen = set()
    
    # Prioriteit: energie/co2 eerst, dan hernieuwbaar/productie, dan rest
    priority_order = ['energie', 'co2', 'hernieuwbaar', 'productie', 'verbruik', 'prijzen', 'economie']
    
    for category in priority_order:
        if category not in catalog:
            continue
        for ds in catalog[category]:
            ds_id = ds.get('Identifier', ds.get('id', ''))
            if ds_id and ds_id not in local and ds_id not in seen:
                seen.add(ds_id)
                missing.append({
                    'id': ds_id,
                    'category': category,
                    'title': ds.get('Title', ds.get('title', ''))[:100],
                    'storage_cat': CATEGORY_MAP.get(category, category),
                })
    
    return missing


def download_dataset(ds_id, storage_cat, title):
    """Download een CBS dataset met paginering."""
    ds_dir = DATA_DIR / storage_cat / ds_id
    
    # Skip als al bestaat
    csv_path = ds_dir / f"{ds_id}_full_data.csv"
    if csv_path.exists() and csv_path.stat().st_size > 100:
        return {'id': ds_id, 'status': 'skipped', 'reason': 'already_exists'}
    
    ds_dir.mkdir(parents=True, exist_ok=True)
    
    # Download data met paginering
    all_rows = []
    base_url = f"{API_BASE}/{ds_id}/TypedDataSet"
    skip = 0
    
    while True:
        for attempt in range(MAX_RETRIES):
            try:
                r = session.get(base_url, params={'$top': PAGE_SIZE, '$skip': skip}, timeout=REQUEST_TIMEOUT)
                
                if r.status_code == 200:
                    break
                elif r.status_code == 403:
                    return {'id': ds_id, 'status': 'forbidden', 'error': 'HTTP 403 — dataset ingetrokken'}
                elif r.status_code == 404:
                    return {'id': ds_id, 'status': 'not_found', 'error': 'HTTP 404'}
                elif r.status_code == 500 and skip == 0 and attempt < MAX_RETRIES - 1:
                    # Soms helpt een retry bij 500
                    time.sleep(2 ** attempt)
                    continue
                elif r.status_code == 429:
                    time.sleep(5)
                    continue
                else:
                    if attempt == MAX_RETRIES - 1:
                        return {'id': ds_id, 'status': 'error', 'error': f'HTTP {r.status_code}'}
                    time.sleep(1)
                    continue
                    
            except requests.exceptions.Timeout:
                if attempt < MAX_RETRIES - 1:
                    time.sleep(2)
                    continue
                return {'id': ds_id, 'status': 'timeout'}
            except Exception as e:
                if attempt < MAX_RETRIES - 1:
                    time.sleep(1)
                    continue
                return {'id': ds_id, 'status': 'error', 'error': str(e)[:100]}
        else:
            if not all_rows:
                return {'id': ds_id, 'status': 'error', 'error': 'Max retries exceeded'}
            break
        
        data = r.json()
        rows = data.get('value', [])
        if not rows:
            break
        
        all_rows.extend(rows)
        skip += len(rows)
        
        if len(rows) < PAGE_SIZE:
            break  # Last page
        
        time.sleep(RATE_LIMIT_PAGE)
    
    if not all_rows:
        return {'id': ds_id, 'status': 'empty'}
    
    # Save CSV + JSON
    df = pd.DataFrame(all_rows)
    df.to_csv(csv_path, index=False)
    df.to_json(ds_dir / f"{ds_id}_full_data.json", orient='records', indent=2)
    
    # Metadata (best effort)
    try:
        r = session.get(f"{API_BASE}/{ds_id}/TableInfos", timeout=15)
        if r.status_code == 200:
            meta = r.json().get('value', [{}])
            with open(ds_dir / f"{ds_id}_metadata.json", 'w') as f:
                json.dump(meta[0] if meta else {}, f, indent=2)
    except:
        pass
    
    return {
        'id': ds_id,
        'status': 'success',
        'rows': len(df),
        'cols': df.shape[1],
        'size_kb': csv_path.stat().st_size // 1024
    }


# ============================================================================
# MAIN
# ============================================================================

def main():
    start_time = datetime.now()
    
    print("=" * 70)
    print("  CBS BULK DOWNLOAD — Alle missende datasets")
    print(f"  Datum: {start_time.strftime('%Y-%m-%d %H:%M')}")
    print("=" * 70)
    
    # Get missing datasets
    missing = get_missing_datasets()
    print(f"\n📊 Missende datasets: {len(missing)}")
    
    # Load progress from previous run
    progress = load_progress()
    already_done = set(progress['completed'] + progress['failed'] + progress['skipped'])
    
    # Filter out already processed
    todo = [m for m in missing if m['id'] not in already_done]
    print(f"📋 Nog te doen: {len(todo)} (al verwerkt: {len(already_done)})")
    
    if not todo:
        print("\n✅ Alles al gedownload!")
        return
    
    # Category breakdown
    from collections import Counter
    cat_count = Counter(m['storage_cat'] for m in todo)
    for cat, count in cat_count.most_common():
        print(f"   {cat:15s}: {count}")
    
    print(f"\n🚀 Start download... (geschat ~{len(todo) * 4 // 60} min)")
    print("-" * 70)
    
    # Stats
    stats = {'success': 0, 'empty': 0, 'error': 0, 'forbidden': 0, 'not_found': 0, 'timeout': 0, 'skipped': 0}
    total_rows = 0
    total_kb = 0
    
    for i, ds in enumerate(todo, 1):
        ds_id = ds['id']
        cat = ds['storage_cat']
        title = ds['title']
        
        # Progress indicator
        pct = i / len(todo) * 100
        elapsed = (datetime.now() - start_time).total_seconds()
        rate = i / elapsed if elapsed > 0 else 0
        eta_min = (len(todo) - i) / rate / 60 if rate > 0 else 0
        
        print(f"[{i:>4}/{len(todo)}] {pct:5.1f}% | ETA {eta_min:>4.0f}m | {ds_id:12s} [{cat:12s}] ", end='', flush=True)
        
        result = download_dataset(ds_id, cat, title)
        status = result['status']
        stats[status] = stats.get(status, 0) + 1
        
        if status == 'success':
            rows = result.get('rows', 0)
            kb = result.get('size_kb', 0)
            total_rows += rows
            total_kb += kb
            print(f"✅ {rows:>8,} rows ({kb:,} KB)")
            progress['completed'].append(ds_id)
        elif status == 'skipped':
            print(f"⏭️  al aanwezig")
            progress['skipped'].append(ds_id)
        elif status == 'empty':
            print(f"📭 leeg")
            progress['completed'].append(ds_id)  # Don't retry empty
        elif status == 'forbidden':
            print(f"🚫 ingetrokken (403)")
            progress['failed'].append(ds_id)
        elif status == 'not_found':
            print(f"❓ niet gevonden (404)")
            progress['failed'].append(ds_id)
        else:
            error = result.get('error', status)
            print(f"❌ {error[:50]}")
            progress['failed'].append(ds_id)
        
        # Save progress every 10 datasets
        if i % 10 == 0:
            save_progress(progress)
        
        time.sleep(RATE_LIMIT_DATASET)
    
    # Final save
    save_progress(progress)
    
    # ========================================================================
    # SAMENVATTING
    # ========================================================================
    elapsed_total = (datetime.now() - start_time).total_seconds()
    
    print("\n" + "=" * 70)
    print("  RESULTAAT")
    print("=" * 70)
    print(f"  ✅ Gedownload:  {stats['success']:>5}")
    print(f"  📭 Leeg:        {stats['empty']:>5}")
    print(f"  ⏭️  Overgeslagen: {stats['skipped']:>5}")
    print(f"  🚫 Ingetrokken: {stats['forbidden']:>5}")
    print(f"  ❓ Niet gevonden: {stats['not_found']:>5}")
    print(f"  ❌ Fouten:       {stats.get('error', 0) + stats.get('timeout', 0):>5}")
    print(f"  📊 Totaal rows:  {total_rows:>12,}")
    print(f"  💾 Totaal grootte: {total_kb:>8,} KB ({total_kb // 1024:,} MB)")
    print(f"  ⏱️  Tijd:         {elapsed_total / 60:.1f} minuten")
    
    # Count final local total
    local = get_local_datasets()
    print(f"\n  📦 Lokale datasets nu: {len(local)}")
    
    # Save summary
    summary = {
        'date': datetime.now().isoformat(),
        'duration_seconds': round(elapsed_total),
        'stats': stats,
        'total_rows_downloaded': total_rows,
        'total_kb': total_kb,
        'local_datasets_total': len(local),
    }
    with open(SUMMARY_FILE, 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"\n✅ Klaar!")


if __name__ == '__main__':
    main()
