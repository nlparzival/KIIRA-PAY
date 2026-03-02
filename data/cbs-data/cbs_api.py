#!/usr/bin/env python3
"""
CBS Open Data API Client for KIIRA-PAY
Complete implementation for accessing all 534 priority datasets

Supports:
- Local cache loading (770+ datasets in data/complete/)
- Live API fallback when local data not available
- Category-based data access
- Search and filtering
"""

import requests
import pandas as pd
from datetime import datetime, timedelta
from typing import Optional, Dict, List, Any
import time
import json
from functools import lru_cache
from pathlib import Path

class CBSDataAPI:
    """
    Professional CBS Open Data API Client
    
    Features:
    - Local-first: checks 770+ cached datasets before hitting API
    - Access to all CBS OData endpoints
    - Automatic caching for performance
    - Rate limiting protection
    - Error handling & retries
    - Category-based data access
    - Multiple output formats (DataFrame, JSON, Dict)
    """
    
    BASE_URL = "https://opendata.cbs.nl/ODataApi/odata"
    CATALOG_URL = f"{BASE_URL}/Catalogs"
    DATA_DIR = Path(__file__).parent / "data" / "complete"
    
    # Available local categories
    CATEGORIES = ['energie', 'hernieuwbaar', 'verbruik', 'productie', 'co2', 'prijzen']
    
    def __init__(self, cache_ttl: int = 3600, rate_limit_delay: float = 0.5):
        """
        Initialize CBS API client
        
        Args:
            cache_ttl: Cache time-to-live in seconds (default: 1 hour)
            rate_limit_delay: Delay between requests in seconds
        """
        self.cache_ttl = cache_ttl
        self.rate_limit_delay = rate_limit_delay
        self.last_request_time = 0
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'KIIRA-PAY/1.0 (Energy Dashboard)',
            'Accept': 'application/json'
        })
        
    def _rate_limit(self):
        """Implement rate limiting between requests"""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.rate_limit_delay:
            time.sleep(self.rate_limit_delay - elapsed)
        self.last_request_time = time.time()
    
    def _make_request(self, url: str, params: Optional[Dict] = None, 
                     retry: int = 3) -> Optional[Dict]:
        """
        Make API request with error handling and retries
        
        Args:
            url: Full URL to request
            params: Query parameters
            retry: Number of retry attempts
            
        Returns:
            JSON response as dict or None on failure
        """
        self._rate_limit()
        
        for attempt in range(retry):
            try:
                response = self.session.get(url, params=params, timeout=30)
                
                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 404:
                    print(f"⚠️  Dataset not found (404): {url}")
                    return None
                elif response.status_code == 429:
                    # Rate limited - wait longer
                    wait_time = 2 ** attempt
                    print(f"⚠️  Rate limited, waiting {wait_time}s...")
                    time.sleep(wait_time)
                    continue
                else:
                    print(f"⚠️  HTTP {response.status_code}: {url}")
                    return None
                    
            except requests.exceptions.Timeout:
                print(f"⚠️  Timeout on attempt {attempt + 1}/{retry}")
                if attempt < retry - 1:
                    time.sleep(1)
                    continue
                return None
                
            except Exception as e:
                print(f"⚠️  Error: {str(e)}")
                return None
        
        return None
    
    def get_dataset_info(self, dataset_id: str) -> Optional[Dict]:
        """
        Get metadata for a specific dataset
        
        Args:
            dataset_id: CBS dataset identifier (e.g., '82610NED')
            
        Returns:
            Dataset metadata as dict
        """
        url = f"{self.BASE_URL}/{dataset_id}"
        return self._make_request(url)
    
    def get_dataset_properties(self, dataset_id: str) -> Optional[List[Dict]]:
        """
        Get all properties/dimensions of a dataset
        
        Args:
            dataset_id: CBS dataset identifier
            
        Returns:
            List of properties with metadata
        """
        url = f"{self.BASE_URL}/{dataset_id}/Properties"
        data = self._make_request(url)
        return data.get('value', []) if data else None
    
    def get_dataset_data(self, dataset_id: str, 
                        filters: Optional[Dict] = None,
                        top: Optional[int] = None,
                        skip: Optional[int] = None,
                        force_api: bool = False) -> Optional[pd.DataFrame]:
        """
        Get actual data from a dataset.
        Strategy: Local cache first → API fallback
        
        Args:
            dataset_id: CBS dataset identifier
            filters: OData filter parameters (e.g., {'Perioden': '2024JJ00'})
            top: Limit number of results
            skip: Skip first N results
            force_api: Skip local cache and fetch from API
            
        Returns:
            Pandas DataFrame with data or None on failure
        """
        # Try local cache first (unless forced to use API or filters applied)
        if not force_api and not filters and not skip:
            local_data = self._load_local(dataset_id)
            if local_data is not None and len(local_data) > 0:
                if top:
                    return local_data.head(top)
                return local_data
        
        url = f"{self.BASE_URL}/{dataset_id}/TypedDataSet"
        
        params = {}
        
        # Build OData filter
        if filters:
            filter_parts = []
            for key, value in filters.items():
                if isinstance(value, str):
                    filter_parts.append(f"{key} eq '{value}'")
                else:
                    filter_parts.append(f"{key} eq {value}")
            params['$filter'] = ' and '.join(filter_parts)
        
        if top:
            params['$top'] = top
        if skip:
            params['$skip'] = skip
        
        data = self._make_request(url, params)
        
        if data and 'value' in data:
            try:
                df = pd.DataFrame(data['value'])
                return df
            except Exception as e:
                print(f"⚠️  Error creating DataFrame: {e}")
                return None
        
        return None
    
    def get_periods(self, dataset_id: str) -> Optional[List[str]]:
        """
        Get available time periods for a dataset
        
        Args:
            dataset_id: CBS dataset identifier
            
        Returns:
            List of period codes
        """
        url = f"{self.BASE_URL}/{dataset_id}/Periods"
        data = self._make_request(url)
        
        if data and 'value' in data:
            return [p.get('Key') for p in data['value']]
        return None
    
    def get_latest_period(self, dataset_id: str) -> Optional[str]:
        """
        Get the most recent period available for a dataset
        
        Args:
            dataset_id: CBS dataset identifier
            
        Returns:
            Latest period code
        """
        periods = self.get_periods(dataset_id)
        return periods[-1] if periods else None
    
    def search_datasets(self, query: str, max_results: int = 50) -> List[Dict]:
        """
        Search for datasets by keyword
        
        Args:
            query: Search term
            max_results: Maximum number of results
            
        Returns:
            List of matching datasets
        """
        url = f"{self.BASE_URL}/Catalogs/CBS/Tables"
        params = {
            '$format': 'json',
            '$filter': f"contains(tolower(Title),'{query.lower()}') or contains(tolower(Summary),'{query.lower()}')",
            '$top': max_results
        }
        
        data = self._make_request(url, params)
        return data.get('value', []) if data else []
    
    # ========================================================================
    # HIGH-LEVEL CONVENIENCE METHODS FOR COMMON DATASETS
    # ========================================================================
    
    def get_renewable_electricity(self, year: Optional[int] = None) -> Optional[pd.DataFrame]:
        """
        Get renewable electricity production and capacity data
        Dataset: 82610NED (Top priority, 108 pts)
        
        Args:
            year: Specific year (None = all years)
            
        Returns:
            DataFrame with renewable electricity data
        """
        dataset_id = '82610NED'
        filters = {'Perioden': f'{year}JJ00'} if year else None
        return self.get_dataset_data(dataset_id, filters)
    
    def get_electricity_netherlands(self, year: Optional[int] = None) -> Optional[pd.DataFrame]:
        """
        Get electricity production and consumption in Netherlands
        Dataset: 70846ned
        
        Args:
            year: Specific year
            
        Returns:
            DataFrame with electricity data
        """
        dataset_id = '70846ned'
        filters = {'Perioden': f'{year}JJ00'} if year else None
        return self.get_dataset_data(dataset_id, filters)
    
    def get_energy_balance(self, year: Optional[int] = None) -> Optional[pd.DataFrame]:
        """
        Get energy balance (supply, transformation, consumption)
        Dataset: 84575NED
        
        Args:
            year: Specific year
            
        Returns:
            DataFrame with energy balance
        """
        dataset_id = '84575NED'
        filters = {'Perioden': f'{year}JJ00'} if year else None
        return self.get_dataset_data(dataset_id, filters)
    
    def get_co2_emissions(self, year: Optional[int] = None) -> Optional[pd.DataFrame]:
        """
        Get CO2 emissions data
        Dataset: 83300NED
        
        Args:
            year: Specific year
            
        Returns:
            DataFrame with CO2 data
        """
        dataset_id = '83300NED'
        filters = {'Perioden': f'{year}JJ00'} if year else None
        return self.get_dataset_data(dataset_id, filters)
    
    def get_energy_prices_cpi(self, start_year: int = 2020) -> Optional[pd.DataFrame]:
        """
        Get consumer price index for energy
        Dataset: 83131NED (Monthly!)
        
        Args:
            start_year: Start year for data
            
        Returns:
            DataFrame with CPI data
        """
        dataset_id = '83131NED'
        # Get all monthly data from start year
        return self.get_dataset_data(dataset_id)
    
    # ========================================================================
    # LOCAL CACHE LOADING
    # ========================================================================
    
    def _load_local(self, dataset_id: str) -> Optional[pd.DataFrame]:
        """Load dataset from local cache (searches all categories)"""
        if not self.DATA_DIR.exists():
            return None
        
        for category_dir in self.DATA_DIR.iterdir():
            if category_dir.is_dir():
                dataset_dir = category_dir / dataset_id
                if dataset_dir.exists():
                    return self._read_dataset_dir(dataset_dir, dataset_id)
        return None
    
    def _read_dataset_dir(self, dataset_dir: Path, dataset_id: str) -> Optional[pd.DataFrame]:
        """Read data from a dataset directory (tries multiple file patterns)"""
        # Try common CSV patterns
        for pattern in [
            f"{dataset_id}_full_data.csv",
            f"{dataset_id}.csv",
            "data.csv",
        ]:
            csv_file = dataset_dir / pattern
            if csv_file.exists():
                try:
                    return pd.read_csv(csv_file)
                except Exception:
                    pass
        
        # Try common JSON patterns
        for pattern in [
            f"{dataset_id}_full_data.json",
            f"{dataset_id}.json",
            "data.json",
        ]:
            json_file = dataset_dir / pattern
            if json_file.exists():
                try:
                    with open(json_file, 'r') as f:
                        data = json.load(f)
                    if isinstance(data, list):
                        return pd.DataFrame(data)
                    elif isinstance(data, dict) and 'value' in data:
                        return pd.DataFrame(data['value'])
                except Exception:
                    pass
        
        return None
    
    def find_dataset_category(self, dataset_id: str) -> Optional[str]:
        """Find which local category a dataset belongs to"""
        if not self.DATA_DIR.exists():
            return None
        for category_dir in self.DATA_DIR.iterdir():
            if category_dir.is_dir() and (category_dir / dataset_id).exists():
                return category_dir.name
        return None
    
    # ========================================================================
    # CATEGORY-BASED ACCESS
    # ========================================================================
    
    def list_local_datasets(self, category: Optional[str] = None) -> Dict[str, List[Dict]]:
        """List all locally available datasets, optionally filtered by category"""
        datasets = {}
        if not self.DATA_DIR.exists():
            return datasets
        
        for category_dir in sorted(self.DATA_DIR.iterdir()):
            if not category_dir.is_dir():
                continue
            cat_name = category_dir.name
            if category and cat_name != category:
                continue
            
            datasets[cat_name] = []
            for dataset_dir in sorted(category_dir.iterdir()):
                if dataset_dir.is_dir():
                    size = sum(f.stat().st_size for f in dataset_dir.rglob('*') if f.is_file())
                    datasets[cat_name].append({
                        'id': dataset_dir.name,
                        'category': cat_name,
                        'size_mb': round(size / 1024 / 1024, 2),
                        'path': str(dataset_dir)
                    })
        return datasets
    
    def get_category_data(self, category: str) -> Dict[str, pd.DataFrame]:
        """Load ALL datasets from a specific category"""
        results = {}
        category_dir = self.DATA_DIR / category
        if not category_dir.exists():
            print(f"Category '{category}' not found")
            return results
        
        for dataset_dir in sorted(category_dir.iterdir()):
            if dataset_dir.is_dir():
                df = self._read_dataset_dir(dataset_dir, dataset_dir.name)
                if df is not None and len(df) > 0:
                    results[dataset_dir.name] = df
        
        print(f"Loaded {len(results)} datasets from '{category}'")
        return results
    
    def get_stats(self) -> Dict[str, Any]:
        """Get overview statistics of all local data"""
        stats = {
            'total_datasets': 0,
            'total_size_mb': 0,
            'categories': {}
        }
        if not self.DATA_DIR.exists():
            return stats
        
        for category_dir in sorted(self.DATA_DIR.iterdir()):
            if not category_dir.is_dir():
                continue
            cat_datasets = 0
            cat_size = 0
            for dataset_dir in category_dir.iterdir():
                if dataset_dir.is_dir():
                    cat_datasets += 1
                    cat_size += sum(f.stat().st_size for f in dataset_dir.rglob('*') if f.is_file())
            
            stats['categories'][category_dir.name] = {
                'datasets': cat_datasets,
                'size_mb': round(cat_size / 1024 / 1024, 2)
            }
            stats['total_datasets'] += cat_datasets
            stats['total_size_mb'] += cat_size
        
        stats['total_size_mb'] = round(stats['total_size_mb'] / 1024 / 1024, 2)
        return stats
    
    def print_overview(self):
        """Print a nice overview of all available local data"""
        stats = self.get_stats()
        print(f"\n{'='*60}")
        print(f"  CBS DATA OVERVIEW - KIIRA-PAY")
        print(f"{'='*60}")
        print(f"  Total datasets:  {stats['total_datasets']}")
        print(f"  Total size:      {stats['total_size_mb']} MB")
        print(f"{'='*60}")
        for cat, info in sorted(stats['categories'].items()):
            bar = '█' * min(int(info['datasets'] / 5), 40)
            print(f"  {cat:<15} {info['datasets']:>4} datasets | {info['size_mb']:>7} MB  {bar}")
        print(f"{'='*60}\n")
    
    # ========================================================================
    # BATCH OPERATIONS
    # ========================================================================
    
    def get_multiple_datasets(self, dataset_ids: List[str], 
                             year: Optional[int] = None) -> Dict[str, pd.DataFrame]:
        """
        Fetch multiple datasets at once
        
        Args:
            dataset_ids: List of CBS dataset IDs
            year: Optional year filter
            
        Returns:
            Dictionary mapping dataset_id to DataFrame
        """
        results = {}
        
        for dataset_id in dataset_ids:
            print(f"📡 Fetching {dataset_id}...")
            filters = {'Perioden': f'{year}JJ00'} if year else None
            df = self.get_dataset_data(dataset_id, filters)
            
            if df is not None:
                results[dataset_id] = df
                print(f"   ✅ {len(df)} records")
            else:
                print(f"   ❌ Failed")
            
            # Small delay between requests
            time.sleep(self.rate_limit_delay)
        
        return results
    
    def get_all_must_haves(self, year: Optional[int] = 2024) -> Dict[str, pd.DataFrame]:
        """
        Fetch all top priority must-have datasets
        
        Args:
            year: Year to fetch (default: 2024)
            
        Returns:
            Dictionary with all must-have datasets
        """
        # Top 10 must-have dataset IDs
        must_have_ids = [
            '82610NED',  # Renewable electricity (108 pts)
            '70846ned',  # Electricity Netherlands
            '84575NED',  # Energy balance
            '83300NED',  # CO2 emissions
            '82380NED',  # Electricity/gas sales
            '83131NED',  # CPI
            '81528NED',  # Household consumption
            '83140NED',  # Consumption by sector
        ]
        
        return self.get_multiple_datasets(must_have_ids, year)


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def format_period_code(year: int, period_type: str = 'JJ') -> str:
    """
    Format CBS period code
    
    Args:
        year: Year (e.g., 2024)
        period_type: JJ (year), KW (quarter), MM (month)
        
    Returns:
        CBS period code (e.g., '2024JJ00')
    """
    return f"{year}{period_type}00"


def parse_period_code(period_code: str) -> Dict[str, Any]:
    """
    Parse CBS period code back to components
    
    Args:
        period_code: CBS period (e.g., '2024JJ00')
        
    Returns:
        Dict with year, type, number
    """
    if len(period_code) >= 6:
        return {
            'year': int(period_code[:4]),
            'type': period_code[4:6],
            'number': period_code[6:] if len(period_code) > 6 else '00'
        }
    return {}


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("🇳🇱 CBS DATA API CLIENT - TEST")
    print("=" * 80)
    
    # Initialize client
    client = CBSDataAPI(rate_limit_delay=0.5)
    
    # Test 1: Local data overview
    print("\n1️⃣  Local data overview...")
    client.print_overview()
    
    # Test 2: Load from local cache
    print("2️⃣  Testing local cache loading...")
    df = client.get_dataset_data('82610NED')
    if df is not None and not df.empty:
        print(f"   ✅ Loaded from local cache: {len(df)} rows, {len(df.columns)} columns")
    else:
        print(f"   ⚠️  Not in local cache, would fall back to API")
    
    # Test 3: List local datasets
    print("\n3️⃣  Local datasets per category...")
    local = client.list_local_datasets()
    for cat, datasets in local.items():
        print(f"   {cat}: {len(datasets)} datasets")
    
    # Test 4: Find dataset category
    print("\n4️⃣  Finding dataset categories...")
    for ds_id in ['82610NED', '83300NED', '70802ned']:
        cat = client.find_dataset_category(ds_id)
        print(f"   {ds_id} → {cat or 'not found locally'}")
    
    print("\n" + "=" * 80)
    print("✅ CBS API CLIENT TEST COMPLETE!")
    print("=" * 80)
