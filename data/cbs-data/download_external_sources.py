#!/usr/bin/env python3
"""
Download priority external data sources for KIIRA-PAY.
Focuses on real-time and historical energy market data.
"""

import requests
import pandas as pd
from pathlib import Path
import json
from datetime import datetime, timedelta
import time

class DataSourceDownloader:
    """Download and cache data from multiple sources."""
    
    def __init__(self, base_dir="data"):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(exist_ok=True)
    
    def download_tennet_data(self):
        """
        Download TenneT data (Dutch TSO).
        Note: TenneT has various data endpoints. This is a template.
        """
        print("\n" + "="*80)
        print("📡 DOWNLOADING TENNET DATA")
        print("="*80 + "\n")
        
        tennet_dir = self.base_dir / "tennet"
        tennet_dir.mkdir(exist_ok=True)
        
        # TenneT data endpoints (examples - verify current URLs)
        endpoints = {
            'generation': 'https://www.tennet.org/bedrijfsvoering/ExporteerData.aspx?exportType=actuele_generatie',
            'consumption': 'https://www.tennet.org/bedrijfsvoering/ExporteerData.aspx?exportType=actueel_verbruik',
            'balance': 'https://www.tennet.org/bedrijfsvoering/ExporteerData.aspx?exportType=balans_delta',
        }
        
        print("⚠️  Note: TenneT URLs may have changed. Please verify at:")
        print("   https://www.tennet.eu/nl/elektriciteitsmarkt/")
        print()
        
        for data_type, url in endpoints.items():
            try:
                print(f"Downloading {data_type}...")
                # Add headers to mimic browser
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'
                }
                response = requests.get(url, headers=headers, timeout=30)
                
                if response.status_code == 200:
                    output_file = tennet_dir / f"{data_type}_{datetime.now().strftime('%Y%m%d')}.csv"
                    output_file.write_bytes(response.content)
                    print(f"  ✅ Saved to {output_file}")
                else:
                    print(f"  ⚠️  HTTP {response.status_code} - {url}")
                    
            except Exception as e:
                print(f"  ❌ Error: {e}")
        
        print("\n✅ TenneT download complete")
        return tennet_dir
    
    def download_entsoe_data(self, api_key=None):
        """
        Download ENTSO-E transparency platform data.
        Requires API key from: https://transparency.entsoe.eu/
        """
        print("\n" + "="*80)
        print("📡 DOWNLOADING ENTSO-E DATA")
        print("="*80 + "\n")
        
        if not api_key:
            print("⚠️  ENTSO-E requires API key!")
            print("   Get one at: https://transparency.entsoe.eu/")
            print("   Then set ENTSOE_API_KEY environment variable")
            return None
        
        entsoe_dir = self.base_dir / "entsoe"
        entsoe_dir.mkdir(exist_ok=True)
        
        # ENTSO-E API endpoint
        base_url = "https://web-api.tp.entsoe.eu/api"
        
        # Netherlands EIC code
        domain = "10YNL----------L"
        
        # Date range (last 7 days)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)
        
        # Format dates for API
        period_start = start_date.strftime('%Y%m%d0000')
        period_end = end_date.strftime('%Y%m%d0000')
        
        # Data types to download
        doc_types = {
            'A44': 'day_ahead_prices',  # Day-ahead prices
            'A75': 'actual_generation',  # Actual generation
            'A69': 'load_forecast',      # Load forecast
            'A71': 'generation_forecast', # Generation forecast
        }
        
        for doc_type, name in doc_types.items():
            try:
                print(f"Downloading {name}...")
                
                params = {
                    'securityToken': api_key,
                    'documentType': doc_type,
                    'in_Domain': domain,
                    'out_Domain': domain,
                    'periodStart': period_start,
                    'periodEnd': period_end,
                }
                
                response = requests.get(base_url, params=params, timeout=30)
                
                if response.status_code == 200:
                    output_file = entsoe_dir / f"{name}_{datetime.now().strftime('%Y%m%d')}.xml"
                    output_file.write_bytes(response.content)
                    print(f"  ✅ Saved to {output_file}")
                else:
                    print(f"  ⚠️  HTTP {response.status_code}")
                    
                time.sleep(1)  # Rate limiting
                
            except Exception as e:
                print(f"  ❌ Error: {e}")
        
        print("\n✅ ENTSO-E download complete")
        return entsoe_dir
    
    def download_knmi_data(self):
        """
        Download KNMI weather data.
        Historical and forecast data for renewable energy predictions.
        """
        print("\n" + "="*80)
        print("📡 DOWNLOADING KNMI DATA")
        print("="*80 + "\n")
        
        knmi_dir = self.base_dir / "knmi"
        knmi_dir.mkdir(exist_ok=True)
        
        # KNMI data API
        # Historical data
        knmi_url = "https://www.daggegevens.knmi.nl/klimatologie/daggegevens"
        
        # Get last year of data
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365)
        
        # Station De Bilt (260) - central Netherlands
        station = "260"
        
        try:
            print("Downloading historical weather data...")
            
            params = {
                'stns': station,
                'start': start_date.strftime('%Y%m%d'),
                'end': end_date.strftime('%Y%m%d'),
            }
            
            response = requests.get(knmi_url, params=params, timeout=30)
            
            if response.status_code == 200:
                output_file = knmi_dir / f"daily_weather_{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}.txt"
                output_file.write_text(response.text)
                print(f"  ✅ Saved to {output_file}")
                
                # Parse and convert to CSV
                lines = response.text.split('\n')
                data_lines = [l for l in lines if l and not l.startswith('#')]
                
                if data_lines:
                    csv_file = knmi_dir / f"daily_weather_{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}.csv"
                    with open(csv_file, 'w') as f:
                        f.write('\n'.join(data_lines))
                    print(f"  ✅ Converted to {csv_file}")
            else:
                print(f"  ⚠️  HTTP {response.status_code}")
                
        except Exception as e:
            print(f"  ❌ Error: {e}")
        
        print("\n✅ KNMI download complete")
        return knmi_dir
    
    def download_rdw_data(self):
        """
        Download RDW open data (vehicle registrations, charging stations).
        """
        print("\n" + "="*80)
        print("📡 DOWNLOADING RDW DATA")
        print("="*80 + "\n")
        
        rdw_dir = self.base_dir / "rdw"
        rdw_dir.mkdir(exist_ok=True)
        
        # RDW Open Data API
        datasets = {
            'electric_vehicles': 'https://opendata.rdw.nl/resource/w4rt-e856.json',
            'charging_stations': 'https://opendata.rdw.nl/resource/b3us-f26s.json',
            'fuel_consumption': 'https://opendata.rdw.nl/resource/8ys7-d773.json',
        }
        
        for name, url in datasets.items():
            try:
                print(f"Downloading {name}...")
                
                # Limit to 10000 records for initial download
                params = {'$limit': 10000}
                response = requests.get(url, params=params, timeout=30)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Save as JSON
                    json_file = rdw_dir / f"{name}_{datetime.now().strftime('%Y%m%d')}.json"
                    with open(json_file, 'w') as f:
                        json.dump(data, f, indent=2)
                    print(f"  ✅ Saved {len(data)} records to {json_file}")
                    
                    # Convert to CSV
                    if data:
                        df = pd.DataFrame(data)
                        csv_file = rdw_dir / f"{name}_{datetime.now().strftime('%Y%m%d')}.csv"
                        df.to_csv(csv_file, index=False)
                        print(f"  ✅ Converted to {csv_file}")
                else:
                    print(f"  ⚠️  HTTP {response.status_code}")
                    
                time.sleep(1)
                
            except Exception as e:
                print(f"  ❌ Error: {e}")
        
        print("\n✅ RDW download complete")
        return rdw_dir
    
    def generate_summary(self):
        """Generate summary of downloaded data."""
        print("\n" + "="*80)
        print("📊 DOWNLOAD SUMMARY")
        print("="*80 + "\n")
        
        summary = {}
        
        for source_dir in self.base_dir.iterdir():
            if source_dir.is_dir() and not source_dir.name.startswith('.'):
                files = list(source_dir.glob('*'))
                total_size = sum(f.stat().st_size for f in files if f.is_file())
                
                summary[source_dir.name] = {
                    'files': len(files),
                    'size_mb': round(total_size / (1024 * 1024), 2),
                    'last_updated': datetime.now().isoformat()
                }
                
                print(f"📁 {source_dir.name}")
                print(f"   Files: {len(files)}")
                print(f"   Size:  {summary[source_dir.name]['size_mb']} MB")
                print()
        
        # Save summary
        summary_file = self.base_dir / "download_summary.json"
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"✅ Summary saved to {summary_file}")

def main():
    """Main download routine."""
    import os
    
    print("\n" + "="*80)
    print("🚀 KIIRA-PAY DATA DOWNLOADER")
    print("="*80)
    print("\nDownloading priority external data sources...")
    print()
    
    downloader = DataSourceDownloader()
    
    # Download from each source
    sources_attempted = []
    
    # 1. KNMI (no API key required)
    print("\n1. KNMI Weather Data")
    try:
        downloader.download_knmi_data()
        sources_attempted.append('KNMI')
    except Exception as e:
        print(f"❌ KNMI download failed: {e}")
    
    # 2. RDW (no API key required)
    print("\n2. RDW Vehicle Data")
    try:
        downloader.download_rdw_data()
        sources_attempted.append('RDW')
    except Exception as e:
        print(f"❌ RDW download failed: {e}")
    
    # 3. TenneT (may require verification)
    print("\n3. TenneT TSO Data")
    try:
        downloader.download_tennet_data()
        sources_attempted.append('TenneT')
    except Exception as e:
        print(f"❌ TenneT download failed: {e}")
    
    # 4. ENTSO-E (requires API key)
    print("\n4. ENTSO-E Transparency Platform")
    entsoe_key = os.getenv('ENTSOE_API_KEY')
    if entsoe_key:
        try:
            downloader.download_entsoe_data(entsoe_key)
            sources_attempted.append('ENTSO-E')
        except Exception as e:
            print(f"❌ ENTSO-E download failed: {e}")
    else:
        print("⚠️  Skipping ENTSO-E (no API key)")
        print("   Set ENTSOE_API_KEY environment variable to enable")
    
    # Generate summary
    downloader.generate_summary()
    
    print("\n" + "="*80)
    print("✅ DOWNLOAD COMPLETE")
    print("="*80)
    print(f"\nSources downloaded: {', '.join(sources_attempted)}")
    print()

if __name__ == "__main__":
    main()
