#!/usr/bin/env python3
"""
KIIRA-PAY Energy Dashboard - Professional Edition
Nederlandse Energie & Grid Data Analyse met volledige TenneT integratie
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests
from datetime import datetime, timedelta
import numpy as np
import os
from dotenv import load_dotenv
import warnings
warnings.filterwarnings('ignore')

# Load environment variables
load_dotenv()

# ============================================================================
# PAGE CONFIG
# ============================================================================

st.set_page_config(
    page_title="KIIRA-PAY Energy Dashboard", 
    layout="wide", 
    page_icon="⚡",
    initial_sidebar_state="collapsed"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1f77b4 0%, #2ca02c 100%);
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .main-header h1 {
        color: white;
        margin: 0;
        font-size: 2.5rem;
    }
    .main-header p {
        color: #e0e0e0;
        margin: 0.5rem 0 0 0;
        font-size: 1.1rem;
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #1f77b4;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .status-live {
        color: #2ca02c;
        font-weight: bold;
    }
    .status-demo {
        color: #ff7f0e;
        font-weight: bold;
    }
    .status-error {
        color: #d62728;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# TENNET API CLASS
# ============================================================================

class TennetAPI:
    """TenneT Grid Data API Integration - Complete Implementation"""
    
    def __init__(self, api_key=None, use_acceptance=None):
        # Determine environment
        if use_acceptance is None:
            env = os.getenv('TENNET_ENVIRONMENT', 'acceptance').lower()
            use_acceptance = env == 'acceptance'
        
        # Get appropriate API key
        if api_key:
            self.api_key = api_key
        elif use_acceptance:
            self.api_key = os.getenv('TENNET_API_KEY_ACCEPTANCE') or os.getenv('TENNET_API_KEY')
        else:
            self.api_key = os.getenv('TENNET_API_KEY_PRODUCTION') or os.getenv('TENNET_API_KEY')
        
        self.base_url = 'https://api.acc.tennet.eu' if use_acceptance else 'https://api.tennet.eu'
        self.environment = 'ACCEPTANCE' if use_acceptance else 'PRODUCTION'
        self.is_real_data = False
        self.last_error = None
        
    def _make_request(self, endpoint, params=None):
        """Generic request method with error handling"""
        if not self.api_key or 'your_' in self.api_key.lower():
            return None
        
        try:
            headers = {
                'apikey': self.api_key,
                'Accept': 'application/json'
            }
            
            response = requests.get(
                f'{self.base_url}{endpoint}',
                headers=headers,
                params=params,
                timeout=15
            )
            
            if response.status_code == 200:
                self.is_real_data = True
                self.last_error = None
                return response.json()
            elif response.status_code == 401:
                self.last_error = "Invalid API key (401)"
            elif response.status_code == 422:
                self.last_error = f"Invalid parameters (422): {response.text[:100]}"
            elif response.status_code == 429:
                self.last_error = "Rate limit exceeded (429)"
            else:
                self.last_error = f"Error {response.status_code}: {response.text[:100]}"
                
        except Exception as e:
            self.last_error = f"Exception: {str(e)}"
        
        return None
    
    def get_settlement_prices(self, hours_back=24):
        """Get settlement prices (ISP - 15 min resolution).
        
        API spec v1.5.1: Imbalance prices per balancing time unit.
        Max range = 1 month. Date format: dd-mm-yyyy hh24:mi:ss
        
        Rate limits:
          Production:  1/sec, 5/min,  25/day  ← VERY strict!
          Acceptance:  1/sec, 60/min, 300/day
        
        Fields per point: isp, shortage, surplus, dispatch_up, dispatch_down,
                          regulation_state, regulating_condition,
                          incident_reserve_up/down, timeInterval_start/end
        """
        # Clamp to max ~31 days (1 month) per API spec
        hours_back = min(hours_back, 31 * 24)
        
        # Use December 2024 for ACCEPTANCE environment (known working data)
        end_date = datetime(2024, 12, 13, 12, 0, 0)
        start_date = end_date - timedelta(hours=hours_back)
        
        date_to = end_date.strftime('%d-%m-%Y %H:%M:%S')
        date_from = start_date.strftime('%d-%m-%Y %H:%M:%S')
        
        params = {'date_from': date_from, 'date_to': date_to}
        data = self._make_request('/publications/v1/settlement-prices', params)
        
        if data and not isinstance(data, dict) or data and 'error' not in data:
            self.is_real_data = True
            return self._process_settlement_prices(data)
        
        # NO MOCK DATA - Return None if API fails
        self.is_real_data = False
        return None
    
    def get_reconciliation_prices(self, days_back=30):
        """Get reconciliation prices per ISP (15 min resolution).
        
        API spec v2.2.0: Weighted market price for profile vs actual consumption settlement.
        Uses /reconciliation-prices/isp endpoint.
        Max range = 1 month. Date format: dd-mm-yyyy hh24:mi:ss
        
        Rate limits (same for production & acceptance):
          1/sec, 60/min, 300/day
        
        Fields per point: isp, isp_price, timeInterval_start_loc, timeInterval_end_loc
        Note: Period is an array (1 per day), not a single object.
        """
        # Clamp to max 31 days (1 month) per API spec
        days_back = min(days_back, 31)
        
        # Use December 2024 for ACCEPTANCE environment
        end_date = datetime(2024, 12, 13, 12, 0, 0)
        start_date = end_date - timedelta(days=days_back)
        
        date_to = end_date.strftime('%d-%m-%Y %H:%M:%S')
        date_from = start_date.strftime('%d-%m-%Y %H:%M:%S')
        
        params = {'date_from': date_from, 'date_to': date_to}
        data = self._make_request('/publications/v1/reconciliation-prices/isp', params)
        
        if data and 'error' not in data:
            self.is_real_data = True
            return self._process_reconciliation_prices_isp(data)
        
        # NO MOCK DATA - Return None if API fails
        self.is_real_data = False
        return None
    
    def get_reconciliation_prices_monthly(self, months_back=6):
        """Get monthly reconciliation prices (price, peak_price, off_peak_price).
        
        API spec v2.2.0: Uses /reconciliation-prices endpoint.
        Max range = 1 year. Date format: dd-mm-yyyy hh24:mi:ss
        
        Fields per point: isp, price, peak_price, off_peak_price,
                          timeInterval_start, timeInterval_end
        """
        # Clamp to max 12 months per API spec
        months_back = min(months_back, 12)
        
        end_date = datetime(2024, 12, 13, 12, 0, 0)
        start_date = end_date - timedelta(days=months_back * 31)
        
        date_to = end_date.strftime('%d-%m-%Y %H:%M:%S')
        date_from = start_date.strftime('%d-%m-%Y %H:%M:%S')
        
        params = {'date_from': date_from, 'date_to': date_to}
        data = self._make_request('/publications/v1/reconciliation-prices', params)
        
        if data and 'error' not in data:
            self.is_real_data = True
            return self._process_reconciliation_prices_month(data)
        
        # NO MOCK DATA - Return None if API fails
        self.is_real_data = False
        return None
    
    def get_balance_delta_latest(self):
        """Get latest balance delta by fetching last hour of data.
        
        NOTE: There is no /balance-delta/latest endpoint in the TenneT API (v1.5.1).
        Instead we fetch the most recent 1-hour window and return the last data point.
        Max range = 1 day. Rate limits: 1 req/sec, 60/min (acceptance).
        """
        # Use December 2024 for ACCEPTANCE environment (known working data)
        end_date = datetime(2024, 12, 13, 12, 0, 0)
        start_date = end_date - timedelta(hours=1)
        
        date_to = end_date.strftime('%d-%m-%Y %H:%M:%S')
        date_from = start_date.strftime('%d-%m-%Y %H:%M:%S')
        
        params = {'date_from': date_from, 'date_to': date_to}
        data = self._make_request('/publications/v1/balance-delta', params)
        
        if data and 'error' not in str(data).lower():
            self.is_real_data = True
            return self._process_balance_delta_latest(data)
        
        # NO MOCK DATA - Return None if API fails
        self.is_real_data = False
        return None
    
    def get_balance_delta_highres_latest(self):
        """Get real-time high-resolution balance delta (12-second intervals).
        
        API spec v1.5.0: /publications/v1/balance-delta-high-res/latest
        Returns the most recent 30-minute rolling window (~150 points at 12s).
        No date parameters needed — always returns latest available data.
        JSON only. Timestamps in UTC.
        
        Recommended polling: 5x/min, 1 second after each 12s data-refresh
        (e.g. 00:00:13, 00:00:25, 00:00:37, 00:00:49, 00:01:01).
        
        Rate limits:
          Production:  1/sec, 10/min
          Acceptance:  1/sec, 10/min
        
        Fields per point: power_afrr_in/out, power_igcc_in/out, power_mfrrda_in/out,
                          power_picasso_in/out, power_mari_in/out, mid_price,
                          max_upw_regulation_price, min_downw_regulation_price,
                          timeInterval_start/end, sequence.
        Note: power_mfrrda_in/out and min_downw_regulation_price can be null.
        Period is a list. Points key is lowercase 'points'.
        """
        data = self._make_request('/publications/v1/balance-delta-high-res/latest')
        
        if data and 'error' not in str(data).lower():
            self.is_real_data = True
            return self._process_balance_delta_highres(data)
        
        # NO MOCK DATA - Return None if API fails
        self.is_real_data = False
        return None
    
    def get_balance_delta_highres_historical(self, minutes_back=30):
        """Get historical high-resolution balance delta (12-second intervals).
        
        API spec v1.5.0: /publications/v1/balance-delta-high-res
        Back-up method to retrieve missed data. Max range = 4 hours (240 min).
        Date format: dd-mm-yyyy hh24:mi:ss. Timestamps in UTC.
        
        Rate limits:
          Production:  8/day
          Acceptance:  8/day
        
        ⚠️ VERY strict rate limit — use /latest for real-time, this for backfill only.
        
        Fields per point: same as /latest (see get_balance_delta_highres_latest).
        """
        # Clamp to max 4 hours (240 minutes) per API spec
        minutes_back = min(minutes_back, 240)
        
        # Use current UTC time for real-time data (this endpoint has live data)
        from datetime import timezone
        end_date = datetime.now(timezone.utc)
        start_date = end_date - timedelta(minutes=minutes_back)
        
        date_to = end_date.strftime('%d-%m-%Y %H:%M:%S')
        date_from = start_date.strftime('%d-%m-%Y %H:%M:%S')
        
        params = {'date_from': date_from, 'date_to': date_to}
        data = self._make_request('/publications/v1/balance-delta-high-res', params)
        
        if data and 'error' not in str(data).lower():
            self.is_real_data = True
            return self._process_balance_delta_highres(data)
        
        # NO MOCK DATA - Return None if API fails
        self.is_real_data = False
        return None
    
    def get_balance_delta_historical(self, minutes_back=60):
        """Get historical balance delta (1-minute resolution).
        
        API spec: max range = 1 day (1440 minutes).
        Fields per point: power_afrr_in/out, power_igcc_in/out, power_mfrrda_in/out,
                          power_picasso_in/out, mid_price, max_upw_regulation_price,
                          min_downw_regulation_price, timeInterval_start/end, sequence.
        """
        # Clamp to max 1 day per API spec
        minutes_back = min(minutes_back, 1440)
        
        # Use December 2024 for ACCEPTANCE environment
        end_date = datetime(2024, 12, 13, 12, 0, 0)
        start_date = end_date - timedelta(minutes=minutes_back)
        
        date_to = end_date.strftime('%d-%m-%Y %H:%M:%S')
        date_from = start_date.strftime('%d-%m-%Y %H:%M:%S')
        
        params = {'date_from': date_from, 'date_to': date_to}
        data = self._make_request('/publications/v1/balance-delta', params)
        
        if data and 'error' not in str(data).lower():
            self.is_real_data = True
            return self._process_balance_delta_historical(data)
        
        # NO MOCK DATA - Return None if API fails
        self.is_real_data = False
        return None
    
    def get_merit_order_list(self, hours_back=1):
        """Get merit order list bid prices (ISP - 15 min resolution).
        
        API spec v1.5.0: Prices and volumes of bids for regulating and reserve capacity
        (aFRR and mFRRsa) received by TenneT.
        Max range = 1 HOUR. Date format: dd-mm-yyyy hh24:mi:ss
        
        Rate limits:
          Production:  1/sec, 10/min, 600/day
          Acceptance:  1/sec, 60/min, 600/day
        
        Fields per point: isp, timeInterval_start/end, Thresholds[]
        Per threshold: capacity_threshold (MAW), price_up (EUR/MWh), price_down (EUR/MWh)
        Typically ~70-80 thresholds per ISP (1 MW to ~760 MW).
        price_down can be null at high capacities.
        """
        # Clamp to max 1 hour per API spec
        hours_back = min(hours_back, 1)
        
        # Use December 2024 for ACCEPTANCE environment
        end_date = datetime(2024, 12, 13, 12, 0, 0)
        start_date = end_date - timedelta(hours=hours_back)
        
        date_to = end_date.strftime('%d-%m-%Y %H:%M:%S')
        date_from = start_date.strftime('%d-%m-%Y %H:%M:%S')
        
        params = {'date_from': date_from, 'date_to': date_to}
        data = self._make_request('/publications/v1/merit-order-list', params)
        
        if data and 'error' not in data:
            self.is_real_data = True
            return self._process_merit_order(data)
        
        # NO MOCK DATA - Return None if API fails
        self.is_real_data = False
        return None
    
    def get_control_data(self, hours_back=1):
        """Get control data (IGCCs and PFCs)"""
        # Use December 2024 for ACCEPTANCE environment
        end_date = datetime(2024, 12, 13, 12, 0, 0)
        start_date = end_date - timedelta(hours=hours_back)
        
        date_to = end_date.strftime('%d-%m-%Y %H:%M:%S')
        date_from = start_date.strftime('%d-%m-%Y %H:%M:%S')
        
        params = {'date_from': date_from, 'date_to': date_to}
        data = self._make_request('/publications/v1/control-data/programme', params)
        
        if data and 'error' not in data:
            self.is_real_data = True
            return self._process_control_data(data)
        
        # NO MOCK DATA - Return None if API fails
        self.is_real_data = False
        return None
    
    def get_frr_activations(self, hours_back=24):
        """Get Frequency Restoration Reserve (FRR) activations.
        
        API spec v1.5.0: Volumes of activated balancing energy, settled reserve and emergency energy.
        Endpoint: /publications/v1/frequency-restoration-reserve-activations
        Max range = 1 day. Date format: dd-mm-yyyy hh24:mi:ss
        Resolution: PT15M (96 ISPs per day). Unit: kWh.
        
        Rate limits (same for production & acceptance):
          1/sec, 60/min, 1500/day
        
        Fields per point: isp, aFRR_up, aFRR_down, mfrrda_volume_up, mfrrda_volume_down,
                          total_volume, absolute_total_volume, timeInterval_start/end
        """
        # Clamp to max 24 hours (1 day) per API spec
        hours_back = min(hours_back, 24)
        
        # Use December 2024 for ACCEPTANCE environment
        end_date = datetime(2024, 12, 13, 12, 0, 0)
        start_date = end_date - timedelta(hours=hours_back)
        
        date_to = end_date.strftime('%d-%m-%Y %H:%M:%S')
        date_from = start_date.strftime('%d-%m-%Y %H:%M:%S')
        
        params = {'date_from': date_from, 'date_to': date_to}
        data = self._make_request('/publications/v1/frequency-restoration-reserve-activations', params)
        
        if data and 'error' not in data:
            self.is_real_data = True
            return self._process_frr_activations(data)
        
        # NO MOCK DATA - Return None if API fails
        self.is_real_data = False
        return None
    
    def get_reconciliation_control_data(self, days_back=31):
        """Get reconciliation control data (underlying volumes for reconciliation price calculation).
        
        API spec v1.5.0: Provides market parties with data to calculate reconciliation prices.
        Endpoint: /publications/v1/reconciliation-control-data
        Max range = 1 year. Date format: dd-mm-yyyy hh24:mi:ss
        Resolution: PT15M (96 ISPs per day). Unit: kWh.
        Period is an array (1 per day).
        
        Rate limits (same for production & acceptance):
          1/sec, 12/min, 1500/day
        
        Fields per point: isp, alloc_up, alloc_down, afrr_up, afrr_down,
                          mfrrda_up, mfrrda_down, timeInterval_start, timeInterval_end
        """
        # Clamp to max 365 days (1 year) per API spec
        days_back = min(days_back, 365)
        
        end_date = datetime(2024, 12, 13, 12, 0, 0)
        start_date = end_date - timedelta(days=days_back)
        
        date_to = end_date.strftime('%d-%m-%Y %H:%M:%S')
        date_from = start_date.strftime('%d-%m-%Y %H:%M:%S')
        
        params = {'date_from': date_from, 'date_to': date_to}
        data = self._make_request('/publications/v1/reconciliation-control-data', params)
        
        if data and 'error' not in data:
            self.is_real_data = True
            return self._process_reconciliation_control_data(data)
        
        # NO MOCK DATA - Return None if API fails
        self.is_real_data = False
        return None
    
    def get_settled_imbalance_volumes(self, hours_back=1):
        """Get settled imbalance volumes per ISP.
        
        API spec v1.5.0: Volumes settled by TenneT TSO with programme-responsible
        parties per time unit. Shows surplus (long), shortage (short), absolute,
        and net imbalance per ISP.
        Max range = 1 HOUR. Date format: dd-mm-yyyy hh24:mi:ss
        
        Rate limits:
          Production:  1/sec,  5/min,  25/day  ← VERY strict!
          Acceptance:  1/sec, 60/min, 300/day
        
        Fields per point: isp, surplus, shortage, absolute, imbalance,
                          timeInterval_start, timeInterval_end
        Unit: kWh
        Relationships: absolute = surplus + shortage, imbalance = surplus - shortage
        """
        # Clamp to max 1 hour per API spec
        hours_back = min(hours_back, 1)
        
        # Use December 2024 for ACCEPTANCE environment
        end_date = datetime(2024, 12, 13, 12, 0, 0)
        start_date = end_date - timedelta(hours=hours_back)
        
        date_to = end_date.strftime('%d-%m-%Y %H:%M:%S')
        date_from = start_date.strftime('%d-%m-%Y %H:%M:%S')
        
        params = {'date_from': date_from, 'date_to': date_to}
        data = self._make_request('/publications/v1/settled-imbalance-volumes', params)
        
        if data and 'error' not in data:
            self.is_real_data = True
            return self._process_settled_imbalance_volumes(data)
        
        # NO MOCK DATA - Return None if API fails
        self.is_real_data = False
        return None
    
    def get_metered_injections(self, hours_back=24):
        """Get metered injections and scheduled exchanges per ISP.
        
        API spec v1.5.0: Metered injections representing the load (consumption)
        visible through the Transmission network of the Netherlands per market
        time unit. Load = Feed-in − exports + imports.
        Max range = 1 DAY. Date format: dd-mm-yyyy hh24:mi:ss
        
        Rate limits:
          Production:  1/sec,  5/min,  25/day  ← VERY strict!
          Acceptance:  1/sec, 60/min, 300/day
        
        Fields per point: isp, measured_infeed (MWh), scheduled_import (MWh),
                          scheduled_export (MWh, negative), timeInterval_start/end
        Unit: MWh
        """
        # Clamp to max 24 hours (1 day) per API spec
        hours_back = min(hours_back, 24)
        
        # Use December 2024 for ACCEPTANCE environment
        end_date = datetime(2024, 12, 14, 0, 0, 0)
        start_date = end_date - timedelta(hours=hours_back)
        
        date_to = end_date.strftime('%d-%m-%Y %H:%M:%S')
        date_from = start_date.strftime('%d-%m-%Y %H:%M:%S')
        
        params = {'date_from': date_from, 'date_to': date_to}
        data = self._make_request('/publications/v1/metered-injections', params)
        
        if data and 'error' not in data:
            self.is_real_data = True
            return self._process_metered_injections(data)
        
        # NO MOCK DATA - Return None if API fails
        self.is_real_data = False
        return None
    
    # Processing methods
    def _process_settlement_prices(self, data):
        """Process settlement prices response.
        
        Uses actual API fields from OpenAPI spec v1.5.1:
        isp, shortage, surplus, dispatch_up, dispatch_down,
        regulation_state, regulating_condition,
        incident_reserve_up/down, timeInterval_start/end.
        Currency: EUR, Unit: MWh.
        """
        try:
            response = data.get('Response', {})
            time_series = response.get('TimeSeries', [])
            
            all_prices = []
            for series in time_series:
                period = series.get('Period', {})
                points = period.get('Points', [])
                
                for point in points:
                    try:
                        shortage = point.get('shortage')
                        surplus = point.get('surplus')
                        dispatch_up = point.get('dispatch_up')
                        dispatch_down = point.get('dispatch_down')
                        
                        # Primary price: use shortage for UP, surplus for DOWN, avg for UP_AND_DOWN
                        reg_condition = point.get('regulating_condition', '')
                        if reg_condition == 'UP':
                            price = shortage
                        elif reg_condition == 'DOWN':
                            price = surplus
                        elif reg_condition == 'UP_AND_DOWN':
                            # Both directions active — use shortage as primary
                            price = shortage
                        else:
                            price = shortage or surplus
                        
                        all_prices.append({
                            'timestamp': pd.to_datetime(point.get('timeInterval_start')),
                            'timestamp_end': pd.to_datetime(point.get('timeInterval_end')),
                            'isp': int(point.get('isp', 0)),
                            'price_eur_mwh': float(price) if price else 0,
                            'shortage_price': float(shortage) if shortage else 0,
                            'surplus_price': float(surplus) if surplus else 0,
                            'dispatch_up': float(dispatch_up) if dispatch_up else None,
                            'dispatch_down': float(dispatch_down) if dispatch_down else None,
                            'regulation_state': point.get('regulation_state', 0),
                            'regulating_condition': reg_condition,
                            'incident_reserve_up': point.get('incident_reserve_up', 'NO') == 'YES',
                            'incident_reserve_down': point.get('incident_reserve_down', 'NO') == 'YES',
                        })
                    except (ValueError, TypeError):
                        continue
            
            if all_prices:
                return pd.DataFrame(all_prices).sort_values('timestamp').reset_index(drop=True)
        except Exception as e:
            print(f"Error processing settlement prices: {str(e)}")
        
        return None  # NO MOCK DATA
    
    def _process_reconciliation_prices_isp(self, data):
        """Process reconciliation prices ISP response.
        
        API spec v2.2.0 - /reconciliation-prices/isp
        Note: Period is an ARRAY (1 per day), each with its own Points array.
        Fields: isp, isp_price, timeInterval_start_loc, timeInterval_end_loc
        Resolution: PT15M (96 ISPs per day)
        """
        try:
            response = data.get('Response', {})
            time_series = response.get('TimeSeries', [])
            
            all_prices = []
            for series in time_series:
                periods = series.get('Period', [])
                
                # Period can be a list (multiple days) or a dict (single day)
                if isinstance(periods, dict):
                    periods = [periods]
                
                for period in periods:
                    points = period.get('Points', [])
                    
                    for point in points:
                        try:
                            isp_price = point.get('isp_price')
                            # Use _loc variants (actual field names from live API)
                            ts_start = point.get('timeInterval_start_loc') or point.get('timeInterval_start')
                            ts_end = point.get('timeInterval_end_loc') or point.get('timeInterval_end')
                            
                            all_prices.append({
                                'timestamp': pd.to_datetime(ts_start),
                                'timestamp_end': pd.to_datetime(ts_end),
                                'isp': int(point.get('isp', 0)),
                                'price_eur_mwh': float(isp_price) if isp_price else 0,
                            })
                        except (ValueError, TypeError):
                            continue
            
            if all_prices:
                return pd.DataFrame(all_prices).sort_values('timestamp').reset_index(drop=True)
        except Exception as e:
            print(f"Error processing reconciliation prices ISP: {str(e)}")
        
        return None  # NO MOCK DATA
    
    def _process_reconciliation_prices_month(self, data):
        """Process monthly reconciliation prices response.
        
        API spec v2.2.0 - /reconciliation-prices
        Fields: isp, price, peak_price, off_peak_price,
                timeInterval_start, timeInterval_end
        """
        try:
            response = data.get('Response', {})
            time_series = response.get('TimeSeries', [])
            
            all_prices = []
            for series in time_series:
                period = series.get('Period', {})
                
                # Period can be a list or dict
                if isinstance(period, dict):
                    periods = [period]
                else:
                    periods = period
                
                for p in periods:
                    points = p.get('Points', [])
                    
                    for point in points:
                        try:
                            all_prices.append({
                                'timestamp': pd.to_datetime(point.get('timeInterval_start')),
                                'timestamp_end': pd.to_datetime(point.get('timeInterval_end')),
                                'isp': int(point.get('isp', 0)),
                                'price_eur_mwh': float(point.get('price', 0)) if point.get('price') else 0,
                                'peak_price': float(point.get('peak_price', 0)) if point.get('peak_price') else 0,
                                'off_peak_price': float(point.get('off_peak_price', 0)) if point.get('off_peak_price') else 0,
                            })
                        except (ValueError, TypeError):
                            continue
            
            if all_prices:
                return pd.DataFrame(all_prices).sort_values('timestamp').reset_index(drop=True)
        except Exception as e:
            print(f"Error processing reconciliation prices monthly: {str(e)}")
        
        return None  # NO MOCK DATA
    
    def _process_balance_delta_latest(self, data):
        """Process latest balance delta response - returns last data point.
        
        Uses actual API fields from OpenAPI spec v1.5.1:
        power_afrr_in/out, power_igcc_in/out, power_mfrrda_in/out,
        power_picasso_in/out, mid_price, max_upw_regulation_price,
        min_downw_regulation_price, timeInterval_start/end, sequence.
        """
        try:
            response = data.get('Response', {})
            time_series = response.get('TimeSeries', [])
            
            for series in time_series:
                period = series.get('Period', {})
                points = period.get('Points', [])
                
                if points:
                    point = points[-1]  # Last (most recent) point
                    
                    # Calculate net balance delta from aFRR + IGCC + mFRRda + PICASSO
                    afrr_in = float(point.get('power_afrr_in', 0) or 0)
                    afrr_out = float(point.get('power_afrr_out', 0) or 0)
                    igcc_in = float(point.get('power_igcc_in', 0) or 0)
                    igcc_out = float(point.get('power_igcc_out', 0) or 0)
                    mfrrda_in = float(point.get('power_mfrrda_in', 0) or 0)
                    mfrrda_out = float(point.get('power_mfrrda_out', 0) or 0)
                    picasso_in = float(point.get('power_picasso_in', 0) or 0)
                    picasso_out = float(point.get('power_picasso_out', 0) or 0)
                    
                    # Net balance: positive = upward regulation (shortage), negative = downward (surplus)
                    total_in = afrr_in + igcc_in + mfrrda_in + picasso_in
                    total_out = afrr_out + igcc_out + mfrrda_out + picasso_out
                    balance_delta = total_in - total_out
                    
                    mid_price = float(point.get('mid_price', 0) or 0)
                    
                    return pd.DataFrame([{
                        'timestamp': pd.to_datetime(point.get('timeInterval_start')),
                        'balance_delta_mw': balance_delta,
                        'total_upward_mw': total_in,
                        'total_downward_mw': total_out,
                        'afrr_in': afrr_in,
                        'afrr_out': afrr_out,
                        'igcc_in': igcc_in,
                        'igcc_out': igcc_out,
                        'mfrrda_in': mfrrda_in,
                        'mfrrda_out': mfrrda_out,
                        'picasso_in': picasso_in,
                        'picasso_out': picasso_out,
                        'mid_price': mid_price,
                        'max_upw_regulation_price': float(point.get('max_upw_regulation_price', 0) or 0),
                        'min_downw_regulation_price': float(point.get('min_downw_regulation_price', 0) or 0),
                        'is_imbalance': abs(balance_delta) > 50,
                        'severity': 'HIGH' if abs(balance_delta) > 200 else 'MEDIUM' if abs(balance_delta) > 100 else 'LOW'
                    }])
        except Exception as e:
            print(f"Error processing balance delta latest: {str(e)}")
        
        return None  # NO MOCK DATA
    
    def _process_balance_delta_historical(self, data):
        """Process historical balance delta response.
        
        Uses actual API fields from OpenAPI spec v1.5.1.
        Data is per-minute resolution with balancing power components.
        """
        try:
            response = data.get('Response', {})
            time_series = response.get('TimeSeries', [])
            
            all_points = []
            for series in time_series:
                period = series.get('Period', {})
                points = period.get('Points', [])
                
                for point in points:
                    try:
                        afrr_in = float(point.get('power_afrr_in', 0) or 0)
                        afrr_out = float(point.get('power_afrr_out', 0) or 0)
                        igcc_in = float(point.get('power_igcc_in', 0) or 0)
                        igcc_out = float(point.get('power_igcc_out', 0) or 0)
                        mfrrda_in = float(point.get('power_mfrrda_in', 0) or 0)
                        mfrrda_out = float(point.get('power_mfrrda_out', 0) or 0)
                        picasso_in = float(point.get('power_picasso_in', 0) or 0)
                        picasso_out = float(point.get('power_picasso_out', 0) or 0)
                        
                        total_in = afrr_in + igcc_in + mfrrda_in + picasso_in
                        total_out = afrr_out + igcc_out + mfrrda_out + picasso_out
                        balance_delta = total_in - total_out
                        
                        mid_price = float(point.get('mid_price', 0) or 0)
                        
                        all_points.append({
                            'timestamp': pd.to_datetime(point.get('timeInterval_start')),
                            'sequence': int(point.get('sequence', 0)),
                            'balance_delta_mw': balance_delta,
                            'total_upward_mw': total_in,
                            'total_downward_mw': total_out,
                            'afrr_in': afrr_in,
                            'afrr_out': afrr_out,
                            'igcc_in': igcc_in,
                            'igcc_out': igcc_out,
                            'mfrrda_in': mfrrda_in,
                            'mfrrda_out': mfrrda_out,
                            'picasso_in': picasso_in,
                            'picasso_out': picasso_out,
                            'mid_price': mid_price,
                            'max_upw_regulation_price': float(point.get('max_upw_regulation_price', 0) or 0),
                            'min_downw_regulation_price': float(point.get('min_downw_regulation_price', 0) or 0),
                            'is_imbalance': abs(balance_delta) > 50,
                            'severity': 'HIGH' if abs(balance_delta) > 200 else 'MEDIUM' if abs(balance_delta) > 100 else 'LOW'
                        })
                    except (ValueError, TypeError):
                        continue
            
            if all_points:
                return pd.DataFrame(all_points).sort_values('timestamp').reset_index(drop=True)
        except Exception as e:
            print(f"Error processing balance delta historical: {str(e)}")
        
        return None  # NO MOCK DATA
    
    def _process_balance_delta_highres(self, data):
        """Process high-resolution balance delta response (12-second intervals).
        
        API spec v1.5.0 - /balance-delta-high-res and /balance-delta-high-res/latest
        Period is a LIST (array). Points key is lowercase 'points'.
        Includes power_mari_in/out in addition to standard balance delta fields.
        power_mfrrda_in/out and min_downw_regulation_price can be null.
        Unit: MAW (MW). Currency: EUR.
        """
        try:
            response = data.get('Response', {})
            time_series = response.get('TimeSeries', [])
            
            all_points = []
            for series in time_series:
                # Period is a LIST in high-res endpoints
                periods = series.get('Period', [])
                if isinstance(periods, dict):
                    periods = [periods]
                
                for period in periods:
                    # Points key is lowercase 'points' in high-res
                    points = period.get('points', period.get('Points', []))
                    
                    for point in points:
                        try:
                            afrr_in = float(point.get('power_afrr_in', 0) or 0)
                            afrr_out = float(point.get('power_afrr_out', 0) or 0)
                            igcc_in = float(point.get('power_igcc_in', 0) or 0)
                            igcc_out = float(point.get('power_igcc_out', 0) or 0)
                            mfrrda_in = float(point.get('power_mfrrda_in', 0) or 0)
                            mfrrda_out = float(point.get('power_mfrrda_out', 0) or 0)
                            picasso_in = float(point.get('power_picasso_in', 0) or 0)
                            picasso_out = float(point.get('power_picasso_out', 0) or 0)
                            mari_in = float(point.get('power_mari_in', 0) or 0)
                            mari_out = float(point.get('power_mari_out', 0) or 0)
                            
                            # Net balance: positive = upward regulation (shortage)
                            total_in = afrr_in + igcc_in + mfrrda_in + picasso_in + mari_in
                            total_out = afrr_out + igcc_out + mfrrda_out + picasso_out + mari_out
                            balance_delta = total_in - total_out
                            
                            mid_price = float(point.get('mid_price', 0) or 0)
                            
                            all_points.append({
                                'timestamp': pd.to_datetime(point.get('timeInterval_start')),
                                'timestamp_end': pd.to_datetime(point.get('timeInterval_end')),
                                'sequence': int(point.get('sequence', 0)),
                                'balance_delta_mw': balance_delta,
                                'total_upward_mw': total_in,
                                'total_downward_mw': total_out,
                                'afrr_in': afrr_in,
                                'afrr_out': afrr_out,
                                'igcc_in': igcc_in,
                                'igcc_out': igcc_out,
                                'mfrrda_in': mfrrda_in,
                                'mfrrda_out': mfrrda_out,
                                'picasso_in': picasso_in,
                                'picasso_out': picasso_out,
                                'mari_in': mari_in,
                                'mari_out': mari_out,
                                'mid_price': mid_price,
                                'max_upw_regulation_price': float(point.get('max_upw_regulation_price', 0) or 0),
                                'min_downw_regulation_price': float(point.get('min_downw_regulation_price', 0) or 0),
                                'is_imbalance': abs(balance_delta) > 50,
                                'severity': 'HIGH' if abs(balance_delta) > 200 else 'MEDIUM' if abs(balance_delta) > 100 else 'LOW'
                            })
                        except (ValueError, TypeError):
                            continue
            
            if all_points:
                return pd.DataFrame(all_points).sort_values('timestamp').reset_index(drop=True)
        except Exception as e:
            print(f"Error processing balance delta high-res: {str(e)}")
        
        return None  # NO MOCK DATA
    
    def _process_merit_order(self, data):
        """Process merit order list response.
        
        API spec v1.5.0 - /merit-order-list
        Period is a DICT (single period). Unit: MAW (capacity), EUR/MWh (prices).
        Each Point has: isp, timeInterval_start/end, Thresholds[].
        Each Threshold: capacity_threshold (MAW string), price_up (EUR/MWh string),
                        price_down (EUR/MWh string or null at high capacities).
        Typically 60-230 thresholds per ISP, ranging from 1 to ~2245 MAW.
        """
        try:
            response = data.get('Response', {})
            time_series = response.get('TimeSeries', [])
            
            all_bids = []
            for series in time_series:
                period = series.get('Period', {})
                # Period is a dict (not array) for this endpoint
                points = period.get('Points', [])
                
                for point in points:
                    isp = point.get('isp', '0')
                    time_start = point.get('timeInterval_start')
                    time_end = point.get('timeInterval_end')
                    thresholds = point.get('Thresholds', [])
                    
                    for threshold in thresholds:
                        try:
                            cap_str = threshold.get('capacity_threshold')
                            price_up_str = threshold.get('price_up')
                            price_down_str = threshold.get('price_down')  # can be null
                            
                            all_bids.append({
                                'timestamp': pd.to_datetime(time_start),
                                'timestamp_end': pd.to_datetime(time_end) if time_end else None,
                                'isp': int(isp),
                                'capacity_threshold_mw': float(cap_str) if cap_str is not None else 0.0,
                                'price_up_eur_mwh': float(price_up_str) if price_up_str is not None else None,
                                'price_down_eur_mwh': float(price_down_str) if price_down_str is not None else None
                            })
                        except (ValueError, TypeError):
                            continue
            
            if all_bids:
                df = pd.DataFrame(all_bids)
                df = df.sort_values(['timestamp', 'capacity_threshold_mw']).reset_index(drop=True)
                return df
        except Exception as e:
            print(f"Error processing merit order: {str(e)}")
        
        # NO MOCK DATA - Return None if processing fails
        return None
    
    def _process_reconciliation_control_data(self, data):
        """Process reconciliation control data response.
        
        API spec v1.5.0 - /reconciliation-control-data
        Period is an ARRAY (1 per day). Unit: kWh.
        Fields: isp, alloc_up, alloc_down, afrr_up, afrr_down,
                mfrrda_up, mfrrda_down, timeInterval_start, timeInterval_end
        """
        try:
            response = data.get('Response', {})
            time_series = response.get('TimeSeries', [])
            
            all_points = []
            for series in time_series:
                unit = series.get('measurement_unit_name', 'kWh')
                periods = series.get('Period', [])
                
                # Period can be a list (multiple days) or a dict (single day)
                if isinstance(periods, dict):
                    periods = [periods]
                
                for period in periods:
                    points = period.get('Points', [])
                    
                    for point in points:
                        try:
                            alloc_up = float(point.get('alloc_up', 0) or 0)
                            alloc_down = float(point.get('alloc_down', 0) or 0)
                            afrr_up = float(point.get('afrr_up', 0) or 0)
                            afrr_down = float(point.get('afrr_down', 0) or 0)
                            mfrrda_up = float(point.get('mfrrda_up', 0) or 0)
                            mfrrda_down = float(point.get('mfrrda_down', 0) or 0)
                            
                            # Net allocation = up - down (kWh)
                            net_alloc = alloc_up - alloc_down
                            net_afrr = afrr_up - afrr_down
                            net_mfrrda = mfrrda_up - mfrrda_down
                            
                            all_points.append({
                                'timestamp': pd.to_datetime(point.get('timeInterval_start')),
                                'timestamp_end': pd.to_datetime(point.get('timeInterval_end')),
                                'isp': int(point.get('isp', 0)),
                                'alloc_up_kwh': alloc_up,
                                'alloc_down_kwh': alloc_down,
                                'net_alloc_kwh': net_alloc,
                                'afrr_up_kwh': afrr_up,
                                'afrr_down_kwh': afrr_down,
                                'net_afrr_kwh': net_afrr,
                                'mfrrda_up_kwh': mfrrda_up,
                                'mfrrda_down_kwh': mfrrda_down,
                                'net_mfrrda_kwh': net_mfrrda,
                            })
                        except (ValueError, TypeError):
                            continue
            
            if all_points:
                return pd.DataFrame(all_points).sort_values('timestamp').reset_index(drop=True)
        except Exception as e:
            print(f"Error processing reconciliation control data: {str(e)}")
        
        return None  # NO MOCK DATA
    
    def _process_control_data(self, data):
        """Process control data response"""
        try:
            response = data.get('Response', {})
            time_series = response.get('TimeSeries', [])
            
            all_controls = []
            for series in time_series:
                period = series.get('Period', {})
                points = period.get('Points', [])
                
                for point in points:
                    try:
                        all_controls.append({
                            'timestamp': pd.to_datetime(point.get('timeInterval_start')),
                            'igcc_mw': float(point.get('igcc', 0)),
                            'pfc_mw': float(point.get('pfc', 0))
                        })
                    except (ValueError, TypeError):
                        continue
            
            if all_controls:
                return pd.DataFrame(all_controls).sort_values('timestamp').reset_index(drop=True)
        except Exception as e:
            print(f"Error processing control data: {str(e)}")
        
        return self._get_mock_control_data()
    
    def _process_frr_activations(self, data):
        """Process FRR activations response.
        
        API spec v1.5.0 - /frequency-restoration-reserve-activations
        Fields: isp, aFRR_up, aFRR_down, mfrrda_volume_up, mfrrda_volume_down,
                total_volume, absolute_total_volume, timeInterval_start/end
        Unit: kWh. Period is a single object (max 1 day).
        
        Note: aFRR_down and mfrrda_volume_down are typically negative values.
        total_volume = net (positive=up, negative=down)
        absolute_total_volume = absolute sum of all activations
        """
        try:
            response = data.get('Response', {})
            time_series = response.get('TimeSeries', [])
            
            all_activations = []
            for series in time_series:
                period = series.get('Period', {})
                points = period.get('Points', [])
                
                for point in points:
                    try:
                        afrr_up = float(point.get('aFRR_up', 0) or 0)
                        afrr_down = float(point.get('aFRR_down', 0) or 0)
                        mfrrda_up = float(point.get('mfrrda_volume_up', 0) or 0)
                        mfrrda_down = float(point.get('mfrrda_volume_down', 0) or 0)
                        total_vol = float(point.get('total_volume', 0) or 0)
                        abs_total = float(point.get('absolute_total_volume', 0) or 0)
                        
                        all_activations.append({
                            'timestamp': pd.to_datetime(point.get('timeInterval_start')),
                            'timestamp_end': pd.to_datetime(point.get('timeInterval_end')),
                            'isp': int(point.get('isp', 0)),
                            'afrr_up_kwh': afrr_up,
                            'afrr_down_kwh': afrr_down,
                            'mfrrda_up_kwh': mfrrda_up,
                            'mfrrda_down_kwh': mfrrda_down,
                            'total_volume_kwh': total_vol,
                            'absolute_total_volume_kwh': abs_total,
                            'direction': 'UP' if total_vol > 0 else 'DOWN' if total_vol < 0 else 'NEUTRAL',
                        })
                    except (ValueError, TypeError):
                        continue
            
            if all_activations:
                return pd.DataFrame(all_activations).sort_values('timestamp').reset_index(drop=True)
        except Exception as e:
            print(f"Error processing FRR activations: {str(e)}")
        
        return None  # NO MOCK DATA

    def _process_settled_imbalance_volumes(self, data):
        """Process settled imbalance volumes response.
        
        API spec v1.5.0 - /settled-imbalance-volumes
        Period is a DICT (single period). Unit: kWh.
        Fields per point: isp (str), surplus (str, kWh), shortage (str, kWh),
                          absolute (str, kWh), imbalance (str, kWh, can be negative),
                          timeInterval_start, timeInterval_end.
        Relationships: absolute = surplus + shortage; imbalance = surplus - shortage.
        """
        try:
            response = data.get('Response', {})
            time_series = response.get('TimeSeries', [])
            
            all_rows = []
            for series in time_series:
                period = series.get('Period', {})
                points = period.get('Points', [])
                
                for point in points:
                    try:
                        surplus = float(point.get('surplus', 0))
                        shortage = float(point.get('shortage', 0))
                        absolute = float(point.get('absolute', 0))
                        imbalance = float(point.get('imbalance', 0))
                        
                        all_rows.append({
                            'timestamp': pd.to_datetime(point.get('timeInterval_start')),
                            'timestamp_end': pd.to_datetime(point.get('timeInterval_end')),
                            'isp': int(point.get('isp', 0)),
                            'surplus_kwh': surplus,
                            'shortage_kwh': shortage,
                            'absolute_kwh': absolute,
                            'imbalance_kwh': imbalance,
                            'surplus_mwh': surplus / 1000.0,
                            'shortage_mwh': shortage / 1000.0,
                            'absolute_mwh': absolute / 1000.0,
                            'imbalance_mwh': imbalance / 1000.0,
                            'direction': 'SURPLUS' if imbalance > 0 else 'SHORTAGE' if imbalance < 0 else 'BALANCED',
                        })
                    except (ValueError, TypeError):
                        continue
            
            if all_rows:
                return pd.DataFrame(all_rows).sort_values('timestamp').reset_index(drop=True)
        except Exception as e:
            print(f"Error processing settled imbalance volumes: {str(e)}")
        
        return None  # NO MOCK DATA

    def _process_metered_injections(self, data):
        """Process metered injections and scheduled exchanges response.
        
        API spec v1.5.0 - /metered-injections
        Period is a DICT. Unit: MWh.
        Fields per point: isp (str), measured_infeed (str, MWh),
                          scheduled_import (str, MWh), scheduled_export (str, MWh, ≤ 0),
                          timeInterval_start, timeInterval_end.
        Load = Feed-in − exports + imports (per API description).
        Note: scheduled_export is negative by convention.
        """
        try:
            response = data.get('Response', {})
            time_series = response.get('TimeSeries', [])
            
            all_rows = []
            for series in time_series:
                period = series.get('Period', {})
                points = period.get('Points', [])
                
                for point in points:
                    try:
                        infeed = float(point.get('measured_infeed', 0))
                        sched_import = float(point.get('scheduled_import', 0))
                        sched_export = float(point.get('scheduled_export', 0))
                        # Load = infeed - export + import
                        # Note: export is already negative, so subtracting it adds it
                        net_load = infeed - sched_export + sched_import
                        
                        all_rows.append({
                            'timestamp': pd.to_datetime(point.get('timeInterval_start')),
                            'timestamp_end': pd.to_datetime(point.get('timeInterval_end')),
                            'isp': int(point.get('isp', 0)),
                            'measured_infeed_mwh': infeed,
                            'scheduled_import_mwh': sched_import,
                            'scheduled_export_mwh': sched_export,
                            'net_load_mwh': net_load,
                        })
                    except (ValueError, TypeError):
                        continue
            
            if all_rows:
                return pd.DataFrame(all_rows).sort_values('timestamp').reset_index(drop=True)
        except Exception as e:
            print(f"Error processing metered injections: {str(e)}")
        
        return None  # NO MOCK DATA

# ============================================================================
# CBS API CLASS — LOCAL-FIRST (730 datasets, 911 MB lokale cache)
# ============================================================================

class CBSDataAPI:
    """CBS Open Data — Local-first met API fallback.
    
    Laadt data uit /data/cbs-data/data/complete/ (730 datasets, 8 categorieën).
    Alleen als lokale data niet beschikbaar is, valt terug op CBS OData API.
    """
    
    # Pad naar lokale CBS cache (relatief aan dashboard.py)
    LOCAL_DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                                  '..', 'cbs-data', 'data', 'complete')
    API_BASE = "https://opendata.cbs.nl/ODataApi/odata"
    
    # Dataset registry: id → (categorie-in-cache, beschrijving, groep)
    # Categorie moet matchen met subdir in /data/cbs-data/data/complete/
    DATASETS = {
        # === Kerndata (10 originele dashboard datasets) ===
        '82610ENG': ('energie',     'Renewable electricity production (EN)',      'hernieuwbaar'),
        '80324ned': ('energie',     'Energieprijzen CPI (maandelijks)',           'prijzen'),
        '70802eng': ('productie',   'Wind energy production (EN)',                'hernieuwbaar'),
        '82369ENG': ('energie',     'Industry energy consumption (EN)',           'verbruik'),
        '83109ENG': ('energie',     'CO2 avoided renewable energy (EN)',          'co2'),
        '70789eng': ('energie',     'Renewable import/export (EN)',               'hernieuwbaar'),
        '71457eng': ('energie',     'Renewable energy capacity (EN)',             'hernieuwbaar'),
        '82610NED': ('energie',     'Hernieuwbare elektriciteit (NL)',            'hernieuwbaar'),
        '84917ENG': ('energie',     'Energy consumption by source (EN)',          'verbruik'),
        '70802ned': ('productie',   'Windenergie (NL)',                           'hernieuwbaar'),
        # === Uitgebreide datasets (nieuw) ===
        '83140NED': ('energie',     'Energiebalans NL 1946-2024 (64 kol)',       'balans'),
        '83140ENG': ('energie',     'Energy balance NL (EN)',                     'balans'),
        '85879NED': ('energie',     'Energiebalans recent (210 kol)',             'balans'),
        '82601NED': ('energie',     'Gasbalans NL (213 kol)',                     'balans'),
        '85669NED': ('co2',         'Broeikasgasemissies uitgebreid (9100 rows)', 'co2'),
        '84596NED': ('energie',     'Oliebalans NL maandelijks (54 kol)',         'balans'),
    }
    
    def __init__(self):
        self.local_dir = os.path.normpath(self.LOCAL_DATA_DIR)
        self._session = None  # Lazy init — alleen als API nodig is
        self.source = {}  # Track per dataset: 'local' of 'api'
    
    @property
    def session(self):
        """Lazy session init — alleen aanmaken als we API calls moeten doen."""
        if self._session is None:
            self._session = requests.Session()
            self._session.headers.update({
                'User-Agent': 'KIIRA-PAY-Dashboard/2.0',
                'Accept': 'application/json'
            })
        return self._session
    
    def _load_local(self, dataset_id):
        """Laad dataset uit lokale cache. Retourneert DataFrame of None."""
        # Check registry voor bekende categorie (tuple kan 2 of 3 elementen hebben)
        if dataset_id in self.DATASETS:
            cat = self.DATASETS[dataset_id][0]
            path = os.path.join(self.local_dir, cat, dataset_id)
            df = self._read_dir(path, dataset_id)
            if df is not None:
                return df
        
        # Fallback: zoek in alle categorieën
        if os.path.isdir(self.local_dir):
            for cat in os.listdir(self.local_dir):
                path = os.path.join(self.local_dir, cat, dataset_id)
                if os.path.isdir(path):
                    df = self._read_dir(path, dataset_id)
                    if df is not None:
                        return df
        return None
    
    def _read_dir(self, path, dataset_id):
        """Lees CSV of JSON uit een dataset directory."""
        if not os.path.isdir(path):
            return None
        # Probeer CSV eerst (kleiner, sneller)
        for pattern in [f"{dataset_id}_full_data.csv", f"{dataset_id}.csv", "data.csv"]:
            fpath = os.path.join(path, pattern)
            if os.path.isfile(fpath):
                try:
                    return pd.read_csv(fpath)
                except Exception:
                    pass
        # Dan JSON
        for pattern in [f"{dataset_id}_full_data.json", f"{dataset_id}.json", "data.json"]:
            fpath = os.path.join(path, pattern)
            if os.path.isfile(fpath):
                try:
                    import json as _json
                    with open(fpath) as f:
                        data = _json.load(f)
                    if isinstance(data, list):
                        return pd.DataFrame(data)
                    elif isinstance(data, dict) and 'value' in data:
                        return pd.DataFrame(data['value'])
                except Exception:
                    pass
        return None
    
    def _load_api(self, dataset_id):
        """Fallback: laad via CBS OData API."""
        try:
            url = f"{self.API_BASE}/{dataset_id}/TypedDataSet"
            response = self.session.get(url, timeout=30)
            if response.status_code == 200:
                data = response.json()
                if 'value' in data:
                    return pd.DataFrame(data['value'])
        except Exception as e:
            print(f"CBS API error ({dataset_id}): {e}")
        return None
    
    def get_dataset(self, dataset_id):
        """Universele loader: lokaal eerst, dan API fallback."""
        # 1. Lokale cache
        df = self._load_local(dataset_id)
        if df is not None and not df.empty:
            self.source[dataset_id] = 'local'
            return df
        
        # 2. API fallback
        df = self._load_api(dataset_id)
        if df is not None and not df.empty:
            self.source[dataset_id] = 'api'
            return df
        
        self.source[dataset_id] = 'failed'
        return None
    
    def get_source(self, dataset_id):
        """Retourneert 'local', 'api', of 'failed' voor een dataset."""
        return self.source.get(dataset_id, 'unknown')
    
    # ---- Bestaande convenience methods (nu local-first) ----
    
    def get_renewable_electricity(self):
        return self.get_dataset('82610ENG')
    
    def get_energy_prices(self):
        return self.get_dataset('80324ned')
    
    def get_wind_energy(self):
        return self.get_dataset('70802eng')
    
    def get_energy_consumption_industry(self):
        return self.get_dataset('82369ENG')
    
    def get_co2_emissions(self):
        return self.get_dataset('83109ENG')
    
    def get_renewable_import_export(self):
        return self.get_dataset('70789eng')
    
    def get_renewable_capacity(self):
        return self.get_dataset('71457eng')
    
    def get_renewable_electricity_nl(self):
        return self.get_dataset('82610NED')
    
    def get_renewable_by_source(self):
        return self.get_dataset('84917ENG')
    
    def get_wind_energy_nl(self):
        return self.get_dataset('70802ned')
    
    # ---- Nieuwe datasets ----
    
    def get_energy_balance(self):
        """Energiebalans NL 1946-2024 (83140NED) — 5688 rows, 64 kolommen"""
        return self.get_dataset('83140NED')
    
    def get_energy_balance_en(self):
        """Energy Balance NL EN (83140ENG)"""
        return self.get_dataset('83140ENG')
    
    def get_energy_balance_recent(self):
        """Energiebalans recent (85879NED) — 210 kolommen, meest actueel"""
        return self.get_dataset('85879NED')
    
    def get_gas_balance(self):
        """Gasbalans NL (82601NED)"""
        return self.get_dataset('82601NED')
    
    def get_greenhouse_emissions(self):
        """Broeikasgasemissies uitgebreid (85669NED) — 9100 rows"""
        return self.get_dataset('85669NED')
    
    def get_oil_balance(self):
        """Oliebalans NL maandelijks (84596NED) — 5704 rows"""
        return self.get_dataset('84596NED')
    
    # ---- Statistieken ----
    
    def get_local_stats(self):
        """Geeft overzicht van lokaal beschikbare datasets."""
        stats = {'categories': {}, 'total': 0}
        if not os.path.isdir(self.local_dir):
            return stats
        for cat in sorted(os.listdir(self.local_dir)):
            cat_path = os.path.join(self.local_dir, cat)
            if os.path.isdir(cat_path) and not cat.startswith('.'):
                count = sum(1 for d in os.listdir(cat_path) if os.path.isdir(os.path.join(cat_path, d)))
                if count > 0:
                    stats['categories'][cat] = count
                    stats['total'] += count
        return stats

# ============================================================================
# CACHE & INITIALIZATION
# ============================================================================

@st.cache_resource
def get_tennet_api():
    """Initialize TenneT API (cached) - Auto-detect environment from .env"""
    return TennetAPI()  # Will auto-detect from TENNET_ENVIRONMENT in .env

@st.cache_resource
def get_cbs_api():
    """Initialize CBS API (cached)"""
    return CBSDataAPI()

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def has_data(df):
    """Check if dataframe has data (not None and not empty)"""
    return df is not None and not df.empty

def show_no_data_warning(endpoint_name="deze endpoint"):
    """Show warning when no data is available"""
    st.warning(f"""
    ⚠️ **Geen data beschikbaar voor {endpoint_name}**
    
    De TenneT API heeft momenteel geen data teruggegeven. Dit kan komen door:
    - Tijdelijk geen data beschikbaar voor de gevraagde periode
    - API limiet bereikt
    - Netwerkproblemen
    
    Probeer over een paar minuten opnieuw of gebruik de **Ververs Data** knop in de sidebar.
    """)

# ============================================================================
# MAIN DASHBOARD
# ============================================================================

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>⚡ KIIRA-PAY Energy Dashboard</h1>
        <p>Nederlandse Energie & Grid Data Analyse • Real-time TenneT TSO Integration</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize APIs
    tennet_api = get_tennet_api()
    cbs_api = get_cbs_api()
    cbs_api = get_cbs_api()
    
    # Sidebar for settings
    with st.sidebar:
        st.header("⚙️ Dashboard Instellingen")
        
        # Environment & API Status
        st.subheader("🌍 Environment")
        env_color = "🟢" if tennet_api.environment == "PRODUCTION" else "🟠"
        st.markdown(f"**{env_color} {tennet_api.environment}**")
        st.caption(f"Endpoint: `{tennet_api.base_url}`")
        
        st.subheader("📡 API Status")
        if tennet_api.is_real_data:
            st.markdown('<p class="status-live">🟢 LIVE DATA</p>', unsafe_allow_html=True)
        else:
            st.markdown('<p class="status-demo">🟡 WACHTEN OP DATA</p>', unsafe_allow_html=True)
        
        if tennet_api.last_error:
            st.error(f"⚠️ {tennet_api.last_error}")
        
        st.subheader("📊 CBS Data")
        st.markdown('<p class="status-live">🟢 BESCHIKBAAR</p>', unsafe_allow_html=True)
        st.caption("10 datasets gevalideerd")
        
        # Refresh button
        if st.button("🔄 Ververs Data", use_container_width=True):
            st.cache_data.clear()
            st.cache_resource.clear()
            st.rerun()
        
        # Info
        st.markdown("---")
        st.subheader("ℹ️ Over")
        st.caption("KIIRA-PAY Energy Dashboard v2.0")
        st.caption("TenneT TSO Nederland API Integratie")
        st.caption(f"Laatste update: {datetime.now().strftime('%H:%M:%S')}")
    
    # Tab navigation
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "🔴 Real-Time Grid",
        "💰 Financial Settlement",
        "📊 Market Analysis",
        "⚙️ Grid Operations",
        "⚖️ Balancing",
        "📈 CBS Statistieken"
    ])
    
    # ========================================================================
    # TAB 1: REAL-TIME GRID MONITOR
    # ========================================================================
    with tab1:
        st.header("🔴 Real-Time Grid Monitor")
        st.markdown("**Live Nederlandse hoogspanningsnet status** • TenneT TSO Nederland • 12-seconde resolutie")
        
        # Latest balance delta — prefer high-res /latest, fallback to standard
        col1, col2 = st.columns([2, 1])
        
        # Initialize variables for status panel
        latest = None
        value = None
        source_label = None
        
        with col1:
            st.subheader("⚡ Huidige Grid Balans (12s High-Res)")
            with st.spinner("Loading live high-res balance delta..."):
                balance_latest_hr = tennet_api.get_balance_delta_highres_latest()
            
            # Use the last row from the high-res 30-min window as the "latest"
            if has_data(balance_latest_hr):
                latest = balance_latest_hr.iloc[-1]
                value = latest['balance_delta_mw']
                source_label = "HIGH-RES /latest (12s)"
                
                # Gauge chart
                fig_gauge = go.Figure(go.Indicator(
                    mode="gauge+number+delta",
                    value=value,
                    domain={'x': [0, 1], 'y': [0, 1]},
                    title={'text': "Balance Delta (MW) — 12s Real-Time", 'font': {'size': 22}},
                    delta={'reference': 0, 'increasing': {'color': "red"}, 'decreasing': {'color': "green"}},
                    gauge={
                        'axis': {'range': [-500, 500], 'tickwidth': 1, 'tickcolor': "darkblue"},
                        'bar': {'color': "darkblue"},
                        'bgcolor': "white",
                        'borderwidth': 2,
                        'bordercolor': "gray",
                        'steps': [
                            {'range': [-500, -200], 'color': '#d62728'},
                            {'range': [-200, -50], 'color': '#ff7f0e'},
                            {'range': [-50, 50], 'color': '#2ca02c'},
                            {'range': [50, 200], 'color': '#ff7f0e'},
                            {'range': [200, 500], 'color': '#d62728'}
                        ],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': value
                        }
                    }
                ))
                fig_gauge.update_layout(height=300, font={'size': 18})
                st.plotly_chart(fig_gauge, use_container_width=True)
            else:
                # Fallback to standard 1-min balance delta
                with st.spinner("High-res niet beschikbaar, fallback naar standaard..."):
                    balance_latest = tennet_api.get_balance_delta_latest()
                
                if has_data(balance_latest):
                    latest = balance_latest.iloc[0]
                    value = latest['balance_delta_mw']
                    source_label = "Standaard /balance-delta (1 min)"
                    
                    fig_gauge = go.Figure(go.Indicator(
                        mode="gauge+number+delta",
                        value=value,
                        domain={'x': [0, 1], 'y': [0, 1]},
                        title={'text': "Balance Delta (MW) — 1 min", 'font': {'size': 22}},
                        delta={'reference': 0, 'increasing': {'color': "red"}, 'decreasing': {'color': "green"}},
                        gauge={
                            'axis': {'range': [-500, 500], 'tickwidth': 1, 'tickcolor': "darkblue"},
                            'bar': {'color': "darkblue"},
                            'bgcolor': "white",
                            'borderwidth': 2,
                            'bordercolor': "gray",
                            'steps': [
                                {'range': [-500, -200], 'color': '#d62728'},
                                {'range': [-200, -50], 'color': '#ff7f0e'},
                                {'range': [-50, 50], 'color': '#2ca02c'},
                                {'range': [50, 200], 'color': '#ff7f0e'},
                                {'range': [200, 500], 'color': '#d62728'}
                            ],
                            'threshold': {
                                'line': {'color': "red", 'width': 4},
                                'thickness': 0.75,
                                'value': value
                            }
                        }
                    ))
                    fig_gauge.update_layout(height=300, font={'size': 18})
                    st.plotly_chart(fig_gauge, use_container_width=True)
                else:
                    show_no_data_warning("Balance Delta (High-Res & Standaard)")
        
        with col2:
            if latest is not None and value is not None:
                st.subheader("Status")
                
                is_imbalance = latest['is_imbalance']
                severity = latest['severity']
                
                if is_imbalance:
                    st.error("⚠️ **ONBALANS GEDETECTEERD**")
                else:
                    st.success("✅ **GRID STABIEL**")
                
                st.metric("Afwijking", f"{abs(value):.1f} MW")
                st.metric("Severity", severity)
                st.metric("Laatste Update", latest['timestamp'].strftime("%H:%M:%S UTC"))
                st.caption(f"Bron: `{source_label}`")
                
                if has_data(balance_latest_hr):
                    st.metric("Datapunten (30 min)", f"{len(balance_latest_hr)}")
                    st.metric("Mid Price", f"€{latest['mid_price']:.2f}/MWh")
                
                st.info("""
                **Balance Delta** meet de werkelijke afwijking tussen 
                geprogrammeerd en daadwerkelijk verbruik/productie op het 
                Nederlandse hoogspanningsnet.
                
                - **Groen** (-50 tot +50 MW): Normaal
                - **Oranje** (50-200 MW): Verhoogd
                - **Rood** (>200 MW): Kritiek
                """)
        
        # ---- High-Res 30-minute rolling window from /latest ----
        if has_data(balance_latest_hr):
            st.markdown("---")
            st.subheader("📡 High-Res 30-Minuten Rolling Window (12s)")
            st.caption("Bron: `/balance-delta-high-res/latest` — ~150 datapunten elke 30 min")
            
            # Main time series
            fig_hr = go.Figure()
            fig_hr.add_trace(go.Scatter(
                x=balance_latest_hr['timestamp'],
                y=balance_latest_hr['balance_delta_mw'],
                mode='lines',
                name='Net Balance Delta',
                line=dict(color='#1f77b4', width=1.5),
                fill='tozeroy',
                fillcolor='rgba(31, 119, 180, 0.1)',
                hovertemplate='<b>%{x|%H:%M:%S}</b><br>Net: %{y:.1f} MW<extra></extra>'
            ))
            fig_hr.add_trace(go.Scatter(
                x=balance_latest_hr['timestamp'],
                y=balance_latest_hr['total_upward_mw'],
                mode='lines',
                name='Opwaarts (Shortage)',
                line=dict(color='#d62728', width=1, dash='dot'),
                hovertemplate='Opwaarts: %{y:.1f} MW<extra></extra>'
            ))
            fig_hr.add_trace(go.Scatter(
                x=balance_latest_hr['timestamp'],
                y=-balance_latest_hr['total_downward_mw'],
                mode='lines',
                name='Neerwaarts (Surplus)',
                line=dict(color='#2ca02c', width=1, dash='dot'),
                hovertemplate='Neerwaarts: %{y:.1f} MW<extra></extra>'
            ))
            fig_hr.add_hline(y=50, line_dash="dash", line_color="orange", annotation_text="+ Drempel")
            fig_hr.add_hline(y=-50, line_dash="dash", line_color="orange", annotation_text="- Drempel")
            fig_hr.add_hline(y=0, line_dash="dot", line_color="gray")
            
            fig_hr.update_layout(
                title="Balance Delta — 12s High Resolution (30 min rolling window)",
                xaxis_title="Tijd (UTC)",
                yaxis_title="Balance Delta (MW)",
                hovermode='x unified',
                height=450,
                template='plotly_white',
                showlegend=True,
                legend=dict(orientation="h", yanchor="bottom", y=1.02)
            )
            st.plotly_chart(fig_hr, use_container_width=True)
            
            # Stats row
            sc1, sc2, sc3, sc4, sc5 = st.columns(5)
            with sc1:
                st.metric("Gem. Δ", f"{balance_latest_hr['balance_delta_mw'].mean():.1f} MW")
            with sc2:
                st.metric("σ (Std Dev)", f"{balance_latest_hr['balance_delta_mw'].std():.1f} MW")
            with sc3:
                st.metric("Max", f"{balance_latest_hr['balance_delta_mw'].max():.1f} MW")
            with sc4:
                st.metric("Min", f"{balance_latest_hr['balance_delta_mw'].min():.1f} MW")
            with sc5:
                st.metric("Mid Price (last)", f"€{balance_latest_hr['mid_price'].iloc[-1]:.2f}")
            
            # Component breakdown stacked area
            with st.expander("🔍 Component Breakdown (aFRR, IGCC, PICASSO, MARI, mFRRda)", expanded=False):
                fig_comp = go.Figure()
                for comp, color in [
                    ('afrr_in', '#d62728'), ('afrr_out', '#ff9896'),
                    ('igcc_in', '#1f77b4'), ('igcc_out', '#aec7e8'),
                    ('picasso_in', '#ff7f0e'), ('picasso_out', '#ffbb78'),
                    ('mari_in', '#9467bd'), ('mari_out', '#c5b0d5'),
                    ('mfrrda_in', '#2ca02c'), ('mfrrda_out', '#98df8a'),
                ]:
                    if comp in balance_latest_hr.columns:
                        fig_comp.add_trace(go.Scatter(
                            x=balance_latest_hr['timestamp'],
                            y=balance_latest_hr[comp],
                            mode='lines',
                            name=comp.replace('_', ' ').upper(),
                            line=dict(color=color, width=1),
                        ))
                fig_comp.update_layout(
                    title="Balancing Components — 12s resolutie",
                    xaxis_title="Tijd (UTC)",
                    yaxis_title="Power (MW)",
                    height=400,
                    template='plotly_white',
                    hovermode='x unified',
                    legend=dict(orientation="h", yanchor="bottom", y=1.02)
                )
                st.plotly_chart(fig_comp, use_container_width=True)
            
            # Distribution
            col_d1, col_d2 = st.columns(2)
            with col_d1:
                fig_dist = px.histogram(
                    balance_latest_hr,
                    x='balance_delta_mw',
                    nbins=30,
                    title="Balance Delta Distributie (12s, 30 min)",
                    labels={'balance_delta_mw': 'Balance Delta (MW)', 'count': 'Frequentie'},
                    color_discrete_sequence=['#1f77b4']
                )
                fig_dist.update_layout(height=300, template='plotly_white', showlegend=False)
                st.plotly_chart(fig_dist, use_container_width=True)
            
            with col_d2:
                sev_counts = balance_latest_hr['severity'].value_counts()
                fig_pie = px.pie(
                    values=sev_counts.values,
                    names=sev_counts.index,
                    title="Severity Verdeling (30 min)",
                    color_discrete_map={'LOW': '#2ca02c', 'MEDIUM': '#ff7f0e', 'HIGH': '#d62728'}
                )
                fig_pie.update_layout(height=300, template='plotly_white')
                st.plotly_chart(fig_pie, use_container_width=True)
            
            # Export high-res data
            csv_hr = balance_latest_hr.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download High-Res Balance Delta (CSV)",
                data=csv_hr,
                file_name=f"balance_delta_highres_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
        
        # ---- Historical section: user chooses 12s or 1-min resolution ----
        st.markdown("---")
        st.subheader("📈 Balance Delta Historisch")
        
        col1, col2 = st.columns([3, 1])
        with col2:
            resolution = st.radio(
                "Resolutie",
                ["12 seconden (high-res)", "1 minuut (standaard)"],
                index=0,
                help="High-res: max 4 uur, 12s. Standaard: max 24 uur, 1 min."
            )
            is_highres = "12 seconden" in resolution
            
            if is_highres:
                minutes = st.slider("Periode (minuten)", 5, 240, 30, 
                                    help="Max 240 min (4 uur) voor high-res")
            else:
                minutes = st.slider("Periode (minuten)", 10, 1440, 60,
                                    help="Max 1440 min (24 uur) voor standaard")
        
        with col1:
            with st.spinner(f"Loading {resolution} data..."):
                if is_highres:
                    balance_hist = tennet_api.get_balance_delta_highres_historical(minutes_back=minutes)
                    res_label = "12s"
                else:
                    balance_hist = tennet_api.get_balance_delta_historical(minutes_back=minutes)
                    res_label = "1 min"
            
            if has_data(balance_hist):
                fig = go.Figure()
                
                fig.add_trace(go.Scatter(
                    x=balance_hist['timestamp'],
                    y=balance_hist['balance_delta_mw'],
                    mode='lines',
                    name='Balance Delta',
                    line=dict(color='#1f77b4', width=2 if not is_highres else 1.5),
                    fill='tozeroy',
                    fillcolor='rgba(31, 119, 180, 0.15)',
                    hovertemplate='<b>%{x|%H:%M:%S}</b><br>Balance Delta: %{y:.1f} MW<extra></extra>'
                ))
                
                fig.add_hline(y=50, line_dash="dash", line_color="orange", 
                             annotation_text="+ Drempel", annotation_position="right")
                fig.add_hline(y=-50, line_dash="dash", line_color="orange",
                             annotation_text="- Drempel", annotation_position="right")
                fig.add_hline(y=0, line_dash="dot", line_color="gray")
                
                fig.update_layout(
                    title=f"Balance Delta Tijdlijn ({minutes} min • {res_label} • {len(balance_hist)} punten)",
                    xaxis_title="Tijd (UTC)",
                    yaxis_title="Balance Delta (MW)",
                    hovermode='x unified',
                    height=400,
                    template='plotly_white',
                    showlegend=True
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Statistics
                st1, st2, st3, st4 = st.columns(4)
                with st1:
                    st.metric("Gemiddeld", f"{balance_hist['balance_delta_mw'].mean():.1f} MW")
                with st2:
                    st.metric("Standaard Dev.", f"{balance_hist['balance_delta_mw'].std():.1f} MW")
                with st3:
                    st.metric("Maximum", f"{balance_hist['balance_delta_mw'].max():.1f} MW")
                with st4:
                    st.metric("Minimum", f"{balance_hist['balance_delta_mw'].min():.1f} MW")
                
                # Distribution
                col_h1, col_h2 = st.columns(2)
                with col_h1:
                    fig_hist = px.histogram(
                        balance_hist,
                        x='balance_delta_mw',
                        nbins=40,
                        title=f"Balance Delta Distributie ({res_label})",
                        labels={'balance_delta_mw': 'Balance Delta (MW)', 'count': 'Frequentie'},
                        color_discrete_sequence=['#1f77b4']
                    )
                    fig_hist.update_layout(height=300, template='plotly_white', showlegend=False)
                    st.plotly_chart(fig_hist, use_container_width=True)
                
                with col_h2:
                    imbalance_counts = balance_hist['severity'].value_counts()
                    fig_pie = px.pie(
                        values=imbalance_counts.values,
                        names=imbalance_counts.index,
                        title="Severity Verdeling",
                        color_discrete_map={'LOW': '#2ca02c', 'MEDIUM': '#ff7f0e', 'HIGH': '#d62728'}
                    )
                    fig_pie.update_layout(height=300, template='plotly_white')
                    st.plotly_chart(fig_pie, use_container_width=True)
                
                # Export
                csv = balance_hist.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label=f"📥 Download Balance Delta ({res_label}) Data (CSV)",
                    data=csv,
                    file_name=f"balance_delta_{res_label.replace(' ', '')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
            else:
                show_no_data_warning(f"Balance Delta Historisch ({res_label})")
        
        # Info section
        st.markdown("---")
        with st.expander("ℹ️ Over Balance Delta High-Res", expanded=False):
            st.markdown("""
            **Balance Delta High Resolution** biedt 12-seconde interval data van het Nederlandse
            elektriciteitsnet via TenneT TSO.
            
            | Endpoint | Resolutie | Max Bereik | Rate Limit |
            |---|---|---|---|
            | `/balance-delta-high-res/latest` | 12 sec | 30 min rolling | 1/sec, 10/min |
            | `/balance-delta-high-res` | 12 sec | 4 uur | 8/dag |
            | `/balance-delta` | 1 min | 1 dag | 1/sec, 60/min |
            
            **Components:** aFRR, IGCC, mFRRda, PICASSO, MARI (in/out per component)
            
            **Berekening:** `net_delta = Σ(power_*_in) - Σ(power_*_out)`
            - Positief = opwaartse regulatie (tekort op het net)
            - Negatief = neerwaartse regulatie (overschot op het net)
            
            **Null handling:** `power_mfrrda_in/out` en `min_downw_regulation_price` kunnen `null` zijn;
            deze worden als 0 behandeld.
            """)
    
    # ========================================================================
    # TAB 2: FINANCIAL SETTLEMENT
    # ========================================================================
    with tab2:
        st.header("💰 Financial Settlement")
        st.markdown("**Settlement & Reconciliation Prijzen** • 15-minuut ISP resolutie")
        
        # Controls
        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            price_type = st.selectbox("Prijs Type", ["Settlement", "Reconciliation"])
        with col2:
            if price_type == "Settlement":
                period = st.selectbox("Periode", [24, 48, 72], format_func=lambda x: f"{x} uur")
            else:
                period = st.selectbox("Periode", [7, 14, 30], format_func=lambda x: f"{x} dagen")
        
        # Load data
        with st.spinner(f"Loading {price_type.lower()} prices..."):
            if price_type == "Settlement":
                prices_df = tennet_api.get_settlement_prices(hours_back=period)
            else:
                prices_df = tennet_api.get_reconciliation_prices(days_back=period)
        
        if has_data(prices_df):
            # Key metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                avg_price = prices_df['price_eur_mwh'].mean()
                st.metric("Gemiddelde Prijs", f"€{avg_price:.2f}/MWh")
            with col2:
                max_price = prices_df['price_eur_mwh'].max()
                st.metric("Hoogste Prijs", f"€{max_price:.2f}/MWh")
            with col3:
                min_price = prices_df['price_eur_mwh'].min()
                st.metric("Laagste Prijs", f"€{min_price:.2f}/MWh")
            with col4:
                volatility = prices_df['price_eur_mwh'].std()
                st.metric("Volatiliteit (σ)", f"€{volatility:.2f}")
            
            # Price timeline
            st.subheader("📈 Prijsontwikkeling")
            fig = px.line(
                prices_df,
                x='timestamp',
                y='price_eur_mwh',
                title=f"{price_type} Prijzen Tijdlijn",
                labels={'timestamp': 'Tijd', 'price_eur_mwh': 'Prijs (EUR/MWh)'},
                markers=True
            )
            
            # Add average line
            fig.add_hline(y=avg_price, line_dash="dash", line_color="red",
                         annotation_text=f"Gemiddeld: €{avg_price:.2f}", annotation_position="right")
            
            fig.update_layout(
                height=400,
                template='plotly_white',
                hovermode='x unified',
                showlegend=True
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Detailed analysis
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📊 Prijs Distributie")
                fig_dist = px.histogram(
                    prices_df,
                    x='price_eur_mwh',
                    nbins=30,
                    title="Frequentieverdeling Prijzen",
                    labels={'price_eur_mwh': 'Prijs (EUR/MWh)', 'count': 'Frequentie'},
                    color_discrete_sequence=['#1f77b4']
                )
                fig_dist.update_layout(height=350, template='plotly_white', showlegend=False)
                st.plotly_chart(fig_dist, use_container_width=True)
            
            with col2:
                st.subheader("📦 Box Plot Analyse")
                fig_box = px.box(
                    prices_df,
                    y='price_eur_mwh',
                    title="Prijs Spreiding & Outliers",
                    labels={'price_eur_mwh': 'Prijs (EUR/MWh)'},
                    color_discrete_sequence=['#2ca02c']
                )
                fig_box.update_layout(height=350, template='plotly_white')
                st.plotly_chart(fig_box, use_container_width=True)
            
            # Daily/Hourly patterns
            st.subheader("🕐 Tijd Patronen")
            prices_df_copy = prices_df.copy()
            prices_df_copy['hour'] = prices_df_copy['timestamp'].dt.hour
            prices_df_copy['dayofweek'] = prices_df_copy['timestamp'].dt.day_name()
            
            col1, col2 = st.columns(2)
            
            with col1:
                hourly_avg = prices_df_copy.groupby('hour')['price_eur_mwh'].mean().reset_index()
                fig_hourly = px.bar(
                    hourly_avg,
                    x='hour',
                    y='price_eur_mwh',
                    title="Gemiddelde Prijs per Uur",
                    labels={'hour': 'Uur van de Dag', 'price_eur_mwh': 'Prijs (EUR/MWh)'},
                    color='price_eur_mwh',
                    color_continuous_scale='RdYlGn_r'
                )
                fig_hourly.update_layout(height=300, template='plotly_white')
                st.plotly_chart(fig_hourly, use_container_width=True)
            
            with col2:
                daily_avg = prices_df_copy.groupby('dayofweek')['price_eur_mwh'].mean().reset_index()
                # Sort by weekday
                day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
                daily_avg['dayofweek'] = pd.Categorical(daily_avg['dayofweek'], categories=day_order, ordered=True)
                daily_avg = daily_avg.sort_values('dayofweek')
                
                fig_daily = px.bar(
                    daily_avg,
                    x='dayofweek',
                    y='price_eur_mwh',
                    title="Gemiddelde Prijs per Dag",
                    labels={'dayofweek': 'Dag van de Week', 'price_eur_mwh': 'Prijs (EUR/MWh)'},
                    color='price_eur_mwh',
                    color_continuous_scale='RdYlGn_r'
                )
                fig_daily.update_layout(height=300, template='plotly_white')
                st.plotly_chart(fig_daily, use_container_width=True)
            
            # Data table
            st.subheader("📋 Recente Prijzen (Laatste 50)")
            display_df = prices_df.tail(50).copy()
            display_df['timestamp'] = display_df['timestamp'].dt.strftime('%Y-%m-%d %H:%M')
            display_df['price_eur_mwh'] = display_df['price_eur_mwh'].round(2)
            st.dataframe(display_df, use_container_width=True, height=300)
            
            # Export
            csv = prices_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label=f"📥 Download {price_type} Prices (CSV)",
                data=csv,
                file_name=f"{price_type.lower()}_prices_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
        else:
            st.warning(f"⚠️ Geen {price_type.lower()} price data beschikbaar.")
    
    # ========================================================================
    # TAB 3: MARKET ANALYSIS
    # ========================================================================
    with tab3:
        st.header("📊 Market Analysis")
        st.markdown("**Merit Order List & Bid Ladder** • aFRR & mFRRsa Capacity Pricing")
        
        # Load data
        with st.spinner("Loading merit order data..."):
            merit_df = tennet_api.get_merit_order_list(hours_back=1)
        
        if has_data(merit_df):
            # Key metrics — use skipna for nullable price_down
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                avg_price_up = merit_df['price_up_eur_mwh'].mean(skipna=True)
                st.metric("Gem. Opwaarts Prijs", f"€{avg_price_up:.2f}/MWh")
            with col2:
                avg_price_down = merit_df['price_down_eur_mwh'].mean(skipna=True)
                st.metric("Gem. Neerwaarts Prijs", f"€{avg_price_down:.2f}/MWh" if pd.notna(avg_price_down) else "n/a")
            with col3:
                max_capacity = merit_df['capacity_threshold_mw'].max()
                st.metric("Max Capaciteit", f"{max_capacity:.0f} MW")
            with col4:
                num_isps = merit_df['isp'].nunique()
                st.metric("Aantal ISPs", num_isps)
            
            # Bid ladder visualization
            st.subheader("📈 Bid Ladder - Laatste ISP")
            latest_isp = merit_df['isp'].max()
            latest_bids = merit_df[merit_df['isp'] == latest_isp].copy()
            
            fig = go.Figure()
            
            # Upward regulation (green) — drop rows where price_up is null
            up_bids = latest_bids.dropna(subset=['price_up_eur_mwh'])
            fig.add_trace(go.Scatter(
                x=up_bids['capacity_threshold_mw'],
                y=up_bids['price_up_eur_mwh'],
                mode='lines+markers',
                name='Opwaartse Regulering (↑)',
                line=dict(color='#2ca02c', width=3),
                marker=dict(size=6, symbol='triangle-up'),
                hovertemplate='<b>Capaciteit:</b> %{x:.0f} MW<br><b>Prijs:</b> €%{y:.2f}/MWh<extra></extra>'
            ))
            
            # Downward regulation (red) — drop rows where price_down is null
            down_bids = latest_bids.dropna(subset=['price_down_eur_mwh'])
            fig.add_trace(go.Scatter(
                x=down_bids['capacity_threshold_mw'],
                y=down_bids['price_down_eur_mwh'],
                mode='lines+markers',
                name='Neerwaartse Regulering (↓)',
                line=dict(color='#d62728', width=3),
                marker=dict(size=6, symbol='triangle-down'),
                hovertemplate='<b>Capaciteit:</b> %{x:.0f} MW<br><b>Prijs:</b> €%{y:.2f}/MWh<extra></extra>'
            ))
            
            fig.update_layout(
                title=f"Merit Order Bid Ladder - ISP {latest_isp} (15-min interval)",
                xaxis_title="Capaciteit Drempel (MW)",
                yaxis_title="Prijs (EUR/MWh)",
                hovermode='closest',
                height=450,
                template='plotly_white',
                legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01, bgcolor='rgba(255,255,255,0.8)')
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Price spread analysis (only where both prices are available)
            st.subheader("📊 Prijs Spread Analyse")
            spread_df = merit_df.dropna(subset=['price_up_eur_mwh', 'price_down_eur_mwh']).copy()
            spread_df['price_spread'] = spread_df['price_up_eur_mwh'] - spread_df['price_down_eur_mwh']
            
            col1, col2 = st.columns(2)
            
            with col1:
                if len(spread_df) > 0:
                    fig_spread = px.line(
                        spread_df,
                        x='capacity_threshold_mw',
                        y='price_spread',
                        color='isp',
                        title="Prijs Spread (Up - Down) per ISP",
                        labels={'capacity_threshold_mw': 'Capaciteit (MW)', 'price_spread': 'Spread (EUR/MWh)', 'isp': 'ISP'},
                        markers=True
                    )
                    fig_spread.update_layout(height=350, template='plotly_white')
                    st.plotly_chart(fig_spread, use_container_width=True)
                else:
                    st.info("Geen spread data (price_down ontbreekt bij alle drempels)")
            
            with col2:
                # Average prices per ISP
                isp_summary = merit_df.groupby('isp').agg({
                    'price_up_eur_mwh': 'mean',
                    'price_down_eur_mwh': 'mean',
                    'capacity_threshold_mw': 'max'
                }).reset_index()
                
                fig_isp = go.Figure()
                fig_isp.add_trace(go.Bar(
                    x=isp_summary['isp'],
                    y=isp_summary['price_up_eur_mwh'],
                    name='Opwaarts',
                    marker_color='#2ca02c'
                ))
                fig_isp.add_trace(go.Bar(
                    x=isp_summary['isp'],
                    y=isp_summary['price_down_eur_mwh'],
                    name='Neerwaarts',
                    marker_color='#d62728'
                ))
                
                fig_isp.update_layout(
                    title="Gemiddelde Prijzen per ISP",
                    xaxis_title="ISP",
                    yaxis_title="Prijs (EUR/MWh)",
                    barmode='group',
                    height=350,
                    template='plotly_white'
                )
                st.plotly_chart(fig_isp, use_container_width=True)
            
            # Capacity vs Price correlation
            st.subheader("🔗 Capaciteit vs Prijs Correlatie")
            col1, col2 = st.columns(2)
            
            with col1:
                up_data = merit_df.dropna(subset=['price_up_eur_mwh'])
                fig_scatter_up = px.scatter(
                    up_data,
                    x='capacity_threshold_mw',
                    y='price_up_eur_mwh',
                    color='isp',
                    title="Opwaartse Prijzen vs Capaciteit",
                    labels={'capacity_threshold_mw': 'Capaciteit (MW)', 'price_up_eur_mwh': 'Prijs (EUR/MWh)', 'isp': 'ISP'},
                    trendline="ols"
                )
                fig_scatter_up.update_layout(height=350, template='plotly_white')
                st.plotly_chart(fig_scatter_up, use_container_width=True)
            
            with col2:
                down_data = merit_df.dropna(subset=['price_down_eur_mwh'])
                fig_scatter_down = px.scatter(
                    down_data,
                    x='capacity_threshold_mw',
                    y='price_down_eur_mwh',
                    color='isp',
                    title="Neerwaartse Prijzen vs Capaciteit",
                    labels={'capacity_threshold_mw': 'Capaciteit (MW)', 'price_down_eur_mwh': 'Prijs (EUR/MWh)', 'isp': 'ISP'},
                    trendline="ols"
                )
                fig_scatter_down.update_layout(height=350, template='plotly_white')
                st.plotly_chart(fig_scatter_down, use_container_width=True)
            
            # Data table
            st.subheader("📋 Bid Ladder Details")
            display_df = merit_df.copy()
            display_df['price_spread'] = display_df['price_up_eur_mwh'] - display_df['price_down_eur_mwh']
            display_df['timestamp'] = display_df['timestamp'].dt.strftime('%Y-%m-%d %H:%M')
            display_df = display_df[['timestamp', 'isp', 'capacity_threshold_mw', 'price_up_eur_mwh', 'price_down_eur_mwh', 'price_spread']]
            display_df.columns = ['Tijd', 'ISP', 'Capaciteit (MW)', 'Prijs ↑ (€/MWh)', 'Prijs ↓ (€/MWh)', 'Spread (€/MWh)']
            st.dataframe(display_df, use_container_width=True, height=300)
            
            # Export
            csv = merit_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Merit Order Data (CSV)",
                data=csv,
                file_name=f"merit_order_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
        else:
            st.warning("⚠️ Geen merit order data beschikbaar.")
    
    # ========================================================================
    # TAB 4: GRID OPERATIONS
    # ========================================================================
    with tab4:
        st.header("⚙️ Grid Operations")
        st.markdown("**Control Data & FRR Activations** • Grid Stability Monitoring")
        
        col1, col2 = st.columns(2)
        
        # Control Data
        with col1:
            st.subheader("📊 Control Data (IGCCs & PFCs)")
            with st.spinner("Loading control data..."):
                control_df = tennet_api.get_control_data(hours_back=1)
            
            if has_data(control_df):
                # Plot IGCC and PFC
                fig = make_subplots(
                    rows=2, cols=1,
                    subplot_titles=("IGCC (Interconnected Grid Control Command)", "PFC (Primary Frequency Control)"),
                    vertical_spacing=0.12
                )
                
                fig.add_trace(
                    go.Scatter(x=control_df['timestamp'], y=control_df['igcc_mw'], 
                              name='IGCC', line=dict(color='#1f77b4', width=2)),
                    row=1, col=1
                )
                
                fig.add_trace(
                    go.Scatter(x=control_df['timestamp'], y=control_df['pfc_mw'], 
                              name='PFC', line=dict(color='#ff7f0e', width=2), fill='tozeroy'),
                    row=2, col=1
                )
                
                fig.update_xaxes(title_text="Tijd", row=2, col=1)
                fig.update_yaxes(title_text="MW", row=1, col=1)
                fig.update_yaxes(title_text="MW", row=2, col=1)
                
                fig.update_layout(height=500, template='plotly_white', showlegend=True)
                st.plotly_chart(fig, use_container_width=True)
                
                # Stats
                col_a, col_b = st.columns(2)
                with col_a:
                    st.metric("IGCC Gemiddeld", f"{control_df['igcc_mw'].mean():.0f} MW")
                with col_b:
                    st.metric("PFC Gemiddeld", f"{control_df['pfc_mw'].mean():.1f} MW")
            else:
                st.info("🚧 Control data wordt geladen...")
        
        # FRR Activations
        with col2:
            st.subheader("⚡ FRR Activations")
            with st.spinner("Loading FRR activations..."):
                frr_df = tennet_api.get_frr_activations(hours_back=1)
            
            if has_data(frr_df):
                # Plot by direction
                fig = px.bar(
                    frr_df,
                    x='timestamp',
                    y='total_volume_kwh',
                    color='direction',
                    title="FRR Activated Volumes per ISP",
                    labels={'timestamp': 'Tijd', 'total_volume_kwh': 'Volume (kWh)', 'direction': 'Richting'},
                    color_discrete_map={'UP': '#2ca02c', 'DOWN': '#d62728', 'NEUTRAL': '#7f7f7f'}
                )
                fig.update_layout(height=500, template='plotly_white')
                st.plotly_chart(fig, use_container_width=True)
                
                # Stats
                col_a, col_b = st.columns(2)
                with col_a:
                    total_up = frr_df['afrr_up_kwh'].sum() + frr_df['mfrrda_up_kwh'].sum()
                    st.metric("Totaal Upward", f"{total_up:,.0f} kWh")
                with col_b:
                    total_down = frr_df['afrr_down_kwh'].sum() + frr_df['mfrrda_down_kwh'].sum()
                    st.metric("Totaal Downward", f"{total_down:,.0f} kWh")
            else:
                st.info("🚧 FRR activations data wordt geladen...")
        
        # Info panel
        st.markdown("---")
        st.info("""
        **Grid Operations Overview:**
        - **IGCC** (Interconnected Grid Control Command): Commando signaal voor het regelen van de uitwisseling tussen netgebieden
        - **PFC** (Primary Frequency Control): Primaire frequentieregeling voor snelle reactie op frequentie-afwijkingen  
        - **FRR** (Frequency Restoration Reserve): Reserve voor het herstellen van de frequentie na verstoringen
        """)
    
    # ========================================================================
    # TAB 5: BALANCING MECHANISMS
    # ========================================================================
    with tab5:
        st.header("⚖️ Balancing Mechanisms")
        st.markdown("**Settled Imbalance Volumes** • Afgewikkelde onbalans per ISP (kWh)")
        
        # Load real data
        with st.spinner("Loading settled imbalance volumes..."):
            siv_df = tennet_api.get_settled_imbalance_volumes(hours_back=1)
        
        if has_data(siv_df):
            # Key metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                total_surplus = siv_df['surplus_mwh'].sum()
                st.metric("Totaal Surplus", f"{total_surplus:,.1f} MWh")
            with col2:
                total_shortage = siv_df['shortage_mwh'].sum()
                st.metric("Totaal Shortage", f"{total_shortage:,.1f} MWh")
            with col3:
                total_imbalance = siv_df['imbalance_mwh'].sum()
                direction_label = "↑ Surplus" if total_imbalance > 0 else "↓ Shortage"
                st.metric("Netto Imbalance", f"{total_imbalance:,.1f} MWh", delta=direction_label)
            with col4:
                num_isps = siv_df['isp'].nunique()
                st.metric("Aantal ISPs", num_isps)
            
            # Imbalance bar chart per ISP
            st.subheader("📊 Netto Imbalance per ISP")
            fig_imb = go.Figure()
            
            colors = ['#2ca02c' if v >= 0 else '#d62728' for v in siv_df['imbalance_mwh']]
            fig_imb.add_trace(go.Bar(
                x=siv_df['timestamp'].dt.strftime('%H:%M'),
                y=siv_df['imbalance_mwh'],
                marker_color=colors,
                name='Imbalance',
                hovertemplate='<b>ISP %{customdata}</b><br>Imbalance: %{y:,.1f} MWh<br>%{x}<extra></extra>',
                customdata=siv_df['isp']
            ))
            fig_imb.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5)
            fig_imb.update_layout(
                title="Netto Imbalance per ISP (groen=surplus, rood=shortage)",
                xaxis_title="Tijd",
                yaxis_title="Imbalance (MWh)",
                height=400,
                template='plotly_white'
            )
            st.plotly_chart(fig_imb, use_container_width=True)
            
            # Surplus vs Shortage stacked
            st.subheader("📈 Surplus vs Shortage per ISP")
            col1, col2 = st.columns(2)
            
            with col1:
                fig_stack = go.Figure()
                fig_stack.add_trace(go.Bar(
                    x=siv_df['timestamp'].dt.strftime('%H:%M'),
                    y=siv_df['surplus_mwh'],
                    name='Surplus (lang)',
                    marker_color='#2ca02c',
                    hovertemplate='Surplus: %{y:,.1f} MWh<extra></extra>'
                ))
                fig_stack.add_trace(go.Bar(
                    x=siv_df['timestamp'].dt.strftime('%H:%M'),
                    y=siv_df['shortage_mwh'],
                    name='Shortage (kort)',
                    marker_color='#d62728',
                    hovertemplate='Shortage: %{y:,.1f} MWh<extra></extra>'
                ))
                fig_stack.update_layout(
                    title="Surplus & Shortage Volumes",
                    barmode='group',
                    xaxis_title="Tijd",
                    yaxis_title="Volume (MWh)",
                    height=350,
                    template='plotly_white'
                )
                st.plotly_chart(fig_stack, use_container_width=True)
            
            with col2:
                fig_abs = px.bar(
                    siv_df,
                    x=siv_df['timestamp'].dt.strftime('%H:%M'),
                    y='absolute_mwh',
                    color='direction',
                    title="Absoluut Volume per ISP",
                    labels={'x': 'Tijd', 'absolute_mwh': 'Absoluut Volume (MWh)', 'direction': 'Richting'},
                    color_discrete_map={'SURPLUS': '#2ca02c', 'SHORTAGE': '#d62728', 'BALANCED': '#7f7f7f'}
                )
                fig_abs.update_layout(height=350, template='plotly_white')
                st.plotly_chart(fig_abs, use_container_width=True)
            
            # Data table
            st.subheader("📋 Settled Imbalance Volumes Details")
            display_df = siv_df.copy()
            display_df['timestamp'] = display_df['timestamp'].dt.strftime('%Y-%m-%d %H:%M')
            display_df = display_df[['timestamp', 'isp', 'surplus_mwh', 'shortage_mwh', 'absolute_mwh', 'imbalance_mwh', 'direction']]
            display_df.columns = ['Tijd', 'ISP', 'Surplus (MWh)', 'Shortage (MWh)', 'Absoluut (MWh)', 'Imbalance (MWh)', 'Richting']
            st.dataframe(display_df, use_container_width=True, height=250)
            
            # Export
            csv = siv_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Settled Imbalance Volumes (CSV)",
                data=csv,
                file_name=f"settled_imbalance_volumes_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
        else:
            st.warning("⚠️ Geen settled imbalance volume data beschikbaar.")
        
        st.markdown("---")
        st.info("""
        **Settled Imbalance Volumes — Uitleg:**
        - **Surplus (lang):** Totale overproductie/onderverbruik door alle BRPs (Balance Responsible Parties)
        - **Shortage (kort):** Totale onderproductie/oververbruik door alle BRPs
        - **Absoluut:** Surplus + Shortage = totaal verhandeld volume
        - **Imbalance:** Surplus − Shortage = netto systeemimbalance (negatief = tekort)
        - **Eenheid:** kWh (in tabel omgerekend naar MWh)
        """)
        
        # --- Metered Injections Section ---
        st.markdown("---")
        st.header("� Metered Injections & Scheduled Exchanges")
        st.markdown("**Netbelasting zichtbaar via het transmissienet** • Load = Feed-in − Export + Import")
        
        with st.spinner("Loading metered injections..."):
            mi_df = tennet_api.get_metered_injections(hours_back=24)
        
        if has_data(mi_df):
            # Key metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                avg_infeed = mi_df['measured_infeed_mwh'].mean()
                st.metric("Gem. Infeed", f"{avg_infeed:,.0f} MWh")
            with col2:
                avg_load = mi_df['net_load_mwh'].mean()
                st.metric("Gem. Netbelasting", f"{avg_load:,.0f} MWh")
            with col3:
                total_import = mi_df['scheduled_import_mwh'].sum()
                st.metric("Totaal Import", f"{total_import:,.0f} MWh")
            with col4:
                total_export = mi_df['scheduled_export_mwh'].sum()
                st.metric("Totaal Export", f"{total_export:,.0f} MWh")
            
            # Main load profile chart
            st.subheader("📈 Dagprofiel Netbelasting")
            fig_load = go.Figure()
            
            fig_load.add_trace(go.Scatter(
                x=mi_df['timestamp'],
                y=mi_df['net_load_mwh'],
                mode='lines',
                name='Netbelasting (Load)',
                line=dict(color='#1f77b4', width=3),
                fill='tozeroy',
                fillcolor='rgba(31,119,180,0.15)',
                hovertemplate='<b>ISP %{customdata}</b><br>Load: %{y:,.1f} MWh<br>%{x}<extra></extra>',
                customdata=mi_df['isp']
            ))
            fig_load.add_trace(go.Scatter(
                x=mi_df['timestamp'],
                y=mi_df['measured_infeed_mwh'],
                mode='lines',
                name='Measured Infeed',
                line=dict(color='#2ca02c', width=2, dash='dot'),
                hovertemplate='Infeed: %{y:,.1f} MWh<extra></extra>'
            ))
            
            fig_load.update_layout(
                title="Netbelasting & Infeed over 24 uur (15-min resolutie)",
                xaxis_title="Tijd",
                yaxis_title="Energie (MWh per 15 min)",
                height=450,
                template='plotly_white',
                hovermode='x unified',
                legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01, bgcolor='rgba(255,255,255,0.8)')
            )
            st.plotly_chart(fig_load, use_container_width=True)
            
            # Import/Export chart
            st.subheader("🔄 Geplande Import & Export")
            col1, col2 = st.columns(2)
            
            with col1:
                fig_ie = go.Figure()
                fig_ie.add_trace(go.Bar(
                    x=mi_df['timestamp'],
                    y=mi_df['scheduled_import_mwh'],
                    name='Import',
                    marker_color='#2ca02c',
                    hovertemplate='Import: %{y:,.1f} MWh<extra></extra>'
                ))
                fig_ie.add_trace(go.Bar(
                    x=mi_df['timestamp'],
                    y=mi_df['scheduled_export_mwh'],
                    name='Export (negatief)',
                    marker_color='#d62728',
                    hovertemplate='Export: %{y:,.1f} MWh<extra></extra>'
                ))
                fig_ie.update_layout(
                    title="Geplande Import & Export per ISP",
                    xaxis_title="Tijd",
                    yaxis_title="Volume (MWh)",
                    barmode='relative',
                    height=350,
                    template='plotly_white'
                )
                st.plotly_chart(fig_ie, use_container_width=True)
            
            with col2:
                # Net position = import + export (export is negative)
                mi_df_plot = mi_df.copy()
                mi_df_plot['net_cross_border_mwh'] = mi_df_plot['scheduled_import_mwh'] + mi_df_plot['scheduled_export_mwh']
                colors = ['#2ca02c' if v >= 0 else '#d62728' for v in mi_df_plot['net_cross_border_mwh']]
                fig_net = go.Figure()
                fig_net.add_trace(go.Bar(
                    x=mi_df_plot['timestamp'],
                    y=mi_df_plot['net_cross_border_mwh'],
                    marker_color=colors,
                    hovertemplate='Netto: %{y:,.1f} MWh<extra></extra>'
                ))
                fig_net.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5)
                fig_net.update_layout(
                    title="Netto Cross-Border Positie (Import − |Export|)",
                    xaxis_title="Tijd",
                    yaxis_title="Netto (MWh)",
                    height=350,
                    template='plotly_white'
                )
                st.plotly_chart(fig_net, use_container_width=True)
            
            # Data table
            st.subheader("📋 Metered Injections Details")
            display_mi = mi_df.copy()
            display_mi['timestamp'] = display_mi['timestamp'].dt.strftime('%Y-%m-%d %H:%M')
            display_mi = display_mi[['timestamp', 'isp', 'measured_infeed_mwh', 'scheduled_import_mwh', 'scheduled_export_mwh', 'net_load_mwh']]
            display_mi.columns = ['Tijd', 'ISP', 'Infeed (MWh)', 'Import (MWh)', 'Export (MWh)', 'Netbelasting (MWh)']
            st.dataframe(display_mi, use_container_width=True, height=300)
            
            # Export
            csv_mi = mi_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Metered Injections (CSV)",
                data=csv_mi,
                file_name=f"metered_injections_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
        else:
            st.warning("⚠️ Geen metered injections data beschikbaar.")
        
        st.markdown("---")
        st.info("""
        **Metered Injections — Uitleg:**
        - **Measured Infeed:** Gemeten invoeding op het transmissienet (productie)
        - **Scheduled Import:** Geplande import uit buurlanden (positief)
        - **Scheduled Export:** Geplande export naar buurlanden (negatief)
        - **Netbelasting (Load):** Feed-in − Export + Import = zichtbare consumptie
        - **Eenheid:** MWh per 15-min ISP
        
        🚧 **Nog in ontwikkeling:**
        - Cross-Border Flows (detailanalyse per land)
        - System Imbalance
        """)

    # ========================================================================
    # TAB 6: CBS STATISTIEKEN — LOKALE DATA + UITGEBREIDE ANALYSE
    # ========================================================================
    with tab6:
        st.header("📈 CBS Energie Statistieken")
        st.markdown("**730+ lokale datasets** • CBS Open Data • Local-first engine")
        
        # Initialize CBS API
        cbs_api = get_cbs_api()
        
        # ── Local stats banner ──
        local_stats = cbs_api.get_local_stats()
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("📦 Lokale Datasets", f"{local_stats['total']:,}")
        with col2:
            st.metric("📁 Categorieën", len(local_stats.get('categories', {})))
        with col3:
            st.metric("⚡ Laadmethode", "Local-first")
        with col4:
            total_size_mb = 911  # known from analysis
            st.metric("💾 Cache Grootte", f"{total_size_mb} MB")
        
        # Category breakdown
        if local_stats.get('categories'):
            with st.expander("📂 Lokale dataset categorieën", expanded=False):
                cat_df = pd.DataFrame([
                    {'Categorie': cat.title(), 'Datasets': count}
                    for cat, count in sorted(local_stats['categories'].items(), key=lambda x: -x[1])
                ])
                col_a, col_b = st.columns([1, 2])
                with col_a:
                    st.dataframe(cat_df, use_container_width=True, hide_index=True)
                with col_b:
                    fig_cat = px.bar(cat_df, x='Datasets', y='Categorie', orientation='h',
                                     title='Datasets per categorie',
                                     color='Datasets', color_continuous_scale='Viridis')
                    fig_cat.update_layout(height=300, template='plotly_white', showlegend=False)
                    st.plotly_chart(fig_cat, use_container_width=True)
        
        st.markdown("---")
        
        # ── Sub-tabs voor CBS data ──
        cbs_tab1, cbs_tab2, cbs_tab3, cbs_tab4, cbs_tab5 = st.tabs([
            "⚡ Energiebalans",
            "🌱 Hernieuwbaar",
            "🌍 CO₂ & Emissies",
            "💰 Prijzen & Verbruik",
            "🔍 Dataset Explorer"
        ])
        
        # ================================================================
        # CBS TAB 1: ENERGIEBALANS NL
        # ================================================================
        with cbs_tab1:
            st.subheader("⚡ Energiebalans Nederland")
            st.markdown("*Belangrijkste energiedataset: Totaal aanbod, verbruik en omzetting*")
            
            with st.spinner("Laden energiebalans (83140NED)..."):
                energy_balance = cbs_api.get_energy_balance()
            
            if has_data(energy_balance):
                src = cbs_api.get_source('83140NED')
                st.success(f"✅ Energiebalans geladen: **{len(energy_balance):,}** records × **{energy_balance.shape[1]}** kolommen • Bron: `{src}`")
                
                # Key metrics
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Records", f"{len(energy_balance):,}")
                with col2:
                    st.metric("Kolommen", energy_balance.shape[1])
                with col3:
                    if 'Perioden' in energy_balance.columns:
                        periods = energy_balance['Perioden'].dropna().unique()
                        st.metric("Periodes", f"{len(periods)}")
                    else:
                        st.metric("Periodes", "–")
                with col4:
                    if 'Energiedragers' in energy_balance.columns:
                        st.metric("Energiedragers", energy_balance['Energiedragers'].nunique())
                    else:
                        st.metric("Energiedragers", "–")
                
                # ── Visualisatie: Totaal energieverbruik over tijd ──
                numeric_cols = energy_balance.select_dtypes(include=[np.number]).columns.tolist()
                # Filter out ID column
                numeric_cols = [c for c in numeric_cols if c != 'ID']
                
                if 'Perioden' in energy_balance.columns and numeric_cols:
                    st.subheader("📊 Energiebalans Visualisatie")
                    
                    # Key columns for energy balance
                    key_cols = [c for c in numeric_cols if any(k in c.lower() for k in 
                                ['totaal', 'winning', 'invoer', 'uitvoer', 'verbruik', 'total'])]
                    if not key_cols:
                        key_cols = numeric_cols[:8]
                    
                    col_sel, col_chart = st.columns([1, 3])
                    
                    with col_sel:
                        selected_balance_cols = st.multiselect(
                            "Selecteer indicatoren:",
                            numeric_cols,
                            default=key_cols[:4],
                            key="balance_cols"
                        )
                        
                        # Filter on energiedrager
                        if 'Energiedragers' in energy_balance.columns:
                            dragers = ['Alle'] + sorted(energy_balance['Energiedragers'].dropna().unique().tolist())
                            selected_drager = st.selectbox("Energiedrager:", dragers, key="balance_drager")
                        else:
                            selected_drager = 'Alle'
                    
                    with col_chart:
                        if selected_balance_cols:
                            plot_df = energy_balance.copy()
                            if selected_drager != 'Alle' and 'Energiedragers' in plot_df.columns:
                                plot_df = plot_df[plot_df['Energiedragers'] == selected_drager]
                            
                            if not plot_df.empty:
                                # Melt for multi-line plot
                                melt_df = plot_df.melt(
                                    id_vars=['Perioden'],
                                    value_vars=selected_balance_cols,
                                    var_name='Indicator',
                                    value_name='Waarde'
                                )
                                fig = px.line(melt_df, x='Perioden', y='Waarde', color='Indicator',
                                              title=f"Energiebalans — {selected_drager}",
                                              labels={'Perioden': 'Periode', 'Waarde': 'PJ / eenheid'})
                                fig.update_layout(height=500, template='plotly_white',
                                                  xaxis_tickangle=-45, legend=dict(orientation='h', y=-0.2))
                                st.plotly_chart(fig, use_container_width=True)
                            else:
                                st.info("Geen data voor deze combinatie")
                
                # Raw data
                with st.expander("📋 Ruwe data (83140NED)", expanded=False):
                    st.info(f"{len(energy_balance):,} rows × {energy_balance.shape[1]} kolommen")
                    st.dataframe(energy_balance, use_container_width=True, height=400)
            else:
                show_no_data_warning("Energiebalans (83140NED)")
            
            st.markdown("---")
            
            # ── Oliebalans ──
            st.subheader("🛢️ Oliebalans Nederland (maandelijks)")
            with st.spinner("Laden oliebalans (84596NED)..."):
                oil_balance = cbs_api.get_oil_balance()
            
            if has_data(oil_balance):
                src = cbs_api.get_source('84596NED')
                st.success(f"✅ Oliebalans: **{len(oil_balance):,}** records × **{oil_balance.shape[1]}** kol • `{src}`")
                
                numeric_oil = [c for c in oil_balance.select_dtypes(include=[np.number]).columns if c != 'ID']
                if 'Perioden' in oil_balance.columns and numeric_oil:
                    oil_key = [c for c in numeric_oil if any(k in c.lower() for k in ['totaal', 'winning', 'invoer', 'raffinaderij'])][:4]
                    if not oil_key:
                        oil_key = numeric_oil[:4]
                    
                    oil_melt = oil_balance.melt(id_vars=['Perioden'], value_vars=oil_key,
                                                 var_name='Indicator', value_name='Waarde')
                    fig_oil = px.line(oil_melt, x='Perioden', y='Waarde', color='Indicator',
                                      title="Oliebalans NL — Trends")
                    fig_oil.update_layout(height=400, template='plotly_white',
                                          xaxis_tickangle=-45, legend=dict(orientation='h', y=-0.2))
                    st.plotly_chart(fig_oil, use_container_width=True)
                
                with st.expander("📋 Ruwe data (84596NED)", expanded=False):
                    st.dataframe(oil_balance, use_container_width=True, height=300)
            else:
                st.info("ℹ️ Oliebalans data niet beschikbaar")
            
            st.markdown("---")
            
            # ── Gasbalans ──
            st.subheader("🔥 Gasbalans Nederland")
            with st.spinner("Laden gasbalans (82601NED)..."):
                gas_balance = cbs_api.get_gas_balance()
            
            if has_data(gas_balance):
                src = cbs_api.get_source('82601NED')
                st.success(f"✅ Gasbalans: **{len(gas_balance):,}** records × **{gas_balance.shape[1]}** kol • `{src}`")
                
                with st.expander("📋 Ruwe data (82601NED)", expanded=False):
                    st.dataframe(gas_balance, use_container_width=True, height=300)
            else:
                st.info("ℹ️ Gasbalans data niet beschikbaar")
        
        # ================================================================
        # CBS TAB 2: HERNIEUWBARE ENERGIE
        # ================================================================
        with cbs_tab2:
            st.subheader("🌱 Hernieuwbare Energie")
            
            # ── Renewable Electricity ──
            st.subheader("⚡ Hernieuwbare Elektriciteitsproductie")
            
            with st.spinner("Laden 82610ENG..."):
                renewable_data = cbs_api.get_renewable_electricity()
            
            if has_data(renewable_data):
                src = cbs_api.get_source('82610ENG')
                st.success(f"✅ {len(renewable_data):,} records • `{src}`")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Records", f"{len(renewable_data):,}")
                with col2:
                    st.metric("Kolommen", renewable_data.shape[1])
                with col3:
                    if 'Periods' in renewable_data.columns:
                        st.metric("Periodes", renewable_data['Periods'].nunique())
                
                # Visualization
                period_col = 'Periods' if 'Periods' in renewable_data.columns else 'Perioden'
                numeric_cols = [c for c in renewable_data.select_dtypes(include=[np.number]).columns if c != 'ID']
                
                if period_col in renewable_data.columns and numeric_cols:
                    col_a, col_b = st.columns([1, 3])
                    with col_a:
                        sel_metric = st.selectbox("Metric:", numeric_cols, key="renew_metric")
                        if 'EnergySourcesTechniques' in renewable_data.columns:
                            sources = ['Alle'] + sorted(renewable_data['EnergySourcesTechniques'].dropna().unique().tolist())
                            sel_source = st.selectbox("Bron:", sources, key="renew_source")
                        else:
                            sel_source = 'Alle'
                    
                    with col_b:
                        plot_df = renewable_data.copy()
                        if sel_source != 'Alle' and 'EnergySourcesTechniques' in plot_df.columns:
                            plot_df = plot_df[plot_df['EnergySourcesTechniques'] == sel_source]
                        
                        if not plot_df.empty:
                            fig = px.line(plot_df, x=period_col, y=sel_metric,
                                          title=f"Hernieuwbare Elektriciteit — {sel_metric}",
                                          color='EnergySourcesTechniques' if 'EnergySourcesTechniques' in plot_df.columns and sel_source == 'Alle' else None)
                            fig.update_layout(height=450, template='plotly_white', xaxis_tickangle=-45)
                            st.plotly_chart(fig, use_container_width=True)
                
                with st.expander("📋 Ruwe data (82610ENG)", expanded=False):
                    st.dataframe(renewable_data, use_container_width=True, height=300)
            else:
                show_no_data_warning("Hernieuwbare elektriciteit (82610ENG)")
            
            st.markdown("---")
            
            # ── Wind Energy ──
            st.subheader("💨 Windenergie")
            
            with st.spinner("Laden 70802eng..."):
                wind_data = cbs_api.get_wind_energy()
            
            if has_data(wind_data):
                src = cbs_api.get_source('70802eng')
                st.success(f"✅ Wind data: {len(wind_data):,} records • `{src}`")
                
                period_col = 'Periods' if 'Periods' in wind_data.columns else 'Perioden'
                numeric_wind = [c for c in wind_data.select_dtypes(include=[np.number]).columns if c != 'ID']
                
                if period_col in wind_data.columns and numeric_wind:
                    # Key wind metrics
                    wind_metrics = st.multiselect("Wind metrics:", numeric_wind, 
                                                   default=numeric_wind[:3], key="wind_metrics")
                    if wind_metrics:
                        wind_melt = wind_data.melt(id_vars=[period_col], value_vars=wind_metrics,
                                                    var_name='Metric', value_name='Waarde')
                        fig_wind = px.line(wind_melt, x=period_col, y='Waarde', color='Metric',
                                           title="Windenergie — Trends")
                        fig_wind.update_layout(height=400, template='plotly_white', xaxis_tickangle=-45)
                        st.plotly_chart(fig_wind, use_container_width=True)
                
                with st.expander("📋 Ruwe data (70802eng)", expanded=False):
                    st.dataframe(wind_data, use_container_width=True, height=300)
            else:
                st.info("ℹ️ Wind data niet beschikbaar")
            
            st.markdown("---")
            
            # ── Capacity ──
            st.subheader("⚙️ Hernieuwbare Energie Capaciteit")
            
            with st.spinner("Laden 71457eng..."):
                capacity_data = cbs_api.get_renewable_capacity()
            
            if has_data(capacity_data):
                src = cbs_api.get_source('71457eng')
                st.success(f"✅ Capaciteit: {len(capacity_data):,} records • `{src}`")
                
                period_col = 'Periods' if 'Periods' in capacity_data.columns else 'Perioden'
                numeric_cap = [c for c in capacity_data.select_dtypes(include=[np.number]).columns if c != 'ID']
                
                if period_col in capacity_data.columns and numeric_cap:
                    cap_sel = st.multiselect("Capaciteit metrics:", numeric_cap, 
                                              default=numeric_cap[:3], key="cap_metrics")
                    if cap_sel:
                        cap_melt = capacity_data.melt(id_vars=[period_col], value_vars=cap_sel,
                                                       var_name='Metric', value_name='Waarde')
                        fig_cap = px.area(cap_melt, x=period_col, y='Waarde', color='Metric',
                                           title="Hernieuwbare Capaciteit — Groei")
                        fig_cap.update_layout(height=400, template='plotly_white', xaxis_tickangle=-45)
                        st.plotly_chart(fig_cap, use_container_width=True)
                
                with st.expander("📋 Ruwe data (71457eng)", expanded=False):
                    st.dataframe(capacity_data, use_container_width=True, height=300)
            else:
                st.info("ℹ️ Capaciteit data niet beschikbaar")
            
            st.markdown("---")
            
            # ── Import / Export ──
            st.subheader("🌍 Import & Export Hernieuwbare Elektriciteit")
            
            with st.spinner("Laden 70789eng..."):
                ie_data = cbs_api.get_renewable_import_export()
            
            if has_data(ie_data):
                src = cbs_api.get_source('70789eng')
                st.success(f"✅ Import/Export: {len(ie_data):,} records • `{src}`")
                
                with st.expander("📋 Ruwe data (70789eng)", expanded=False):
                    st.dataframe(ie_data, use_container_width=True, height=300)
            else:
                st.info("ℹ️ Import/Export data niet beschikbaar")
        
        # ================================================================
        # CBS TAB 3: CO₂ & EMISSIES
        # ================================================================
        with cbs_tab3:
            st.subheader("🌍 CO₂ & Broeikasgasemissies")
            
            # ── Broeikasgasemissies (85669NED) — de grootste dataset ──
            st.subheader("🏭 Broeikasgasemissies Nederland (uitgebreid)")
            
            with st.spinner("Laden 85669NED (9.100 records)..."):
                ghg_data = cbs_api.get_greenhouse_emissions()
            
            if has_data(ghg_data):
                src = cbs_api.get_source('85669NED')
                st.success(f"✅ Broeikasgasemissies: **{len(ghg_data):,}** records • `{src}`")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Records", f"{len(ghg_data):,}")
                with col2:
                    if 'Perioden' in ghg_data.columns:
                        st.metric("Periodes", ghg_data['Perioden'].nunique())
                with col3:
                    if 'Klimaatsectoren' in ghg_data.columns:
                        st.metric("Klimaatsectoren", ghg_data['Klimaatsectoren'].nunique())
                
                # Visualization: emissions by sector over time
                if 'Perioden' in ghg_data.columns and 'EmissieBroeikasgassen_1' in ghg_data.columns:
                    col_a, col_b = st.columns([1, 3])
                    
                    with col_a:
                        if 'Klimaatsectoren' in ghg_data.columns:
                            sectors = sorted(ghg_data['Klimaatsectoren'].dropna().unique().tolist())
                            sel_sectors = st.multiselect("Klimaatsectoren:", sectors,
                                                          default=sectors[:5], key="ghg_sectors")
                        else:
                            sel_sectors = []
                        
                        if 'EmissiesNaarLucht' in ghg_data.columns:
                            emissions = sorted(ghg_data['EmissiesNaarLucht'].dropna().unique().tolist())
                            sel_emission = st.selectbox("Type emissie:", emissions, key="ghg_type")
                        else:
                            sel_emission = None
                    
                    with col_b:
                        plot_df = ghg_data.copy()
                        if sel_sectors and 'Klimaatsectoren' in plot_df.columns:
                            plot_df = plot_df[plot_df['Klimaatsectoren'].isin(sel_sectors)]
                        if sel_emission and 'EmissiesNaarLucht' in plot_df.columns:
                            plot_df = plot_df[plot_df['EmissiesNaarLucht'] == sel_emission]
                        
                        if not plot_df.empty:
                            fig_ghg = px.line(plot_df, x='Perioden', y='EmissieBroeikasgassen_1',
                                               color='Klimaatsectoren' if 'Klimaatsectoren' in plot_df.columns else None,
                                               title=f"Broeikasgasemissies per sector",
                                               labels={'EmissieBroeikasgassen_1': 'Emissie (mln kg CO₂-eq)',
                                                       'Perioden': 'Periode'})
                            fig_ghg.update_layout(height=500, template='plotly_white',
                                                   xaxis_tickangle=-45, 
                                                   legend=dict(orientation='h', y=-0.3))
                            st.plotly_chart(fig_ghg, use_container_width=True)
                        else:
                            st.info("Geen data voor deze combinatie")
                
                with st.expander("📋 Ruwe data (85669NED)", expanded=False):
                    st.dataframe(ghg_data, use_container_width=True, height=400)
            else:
                show_no_data_warning("Broeikasgasemissies (85669NED)")
            
            st.markdown("---")
            
            # ── CO2 Avoided (83109ENG) ──
            st.subheader("♻️ CO₂ Vermeden door Hernieuwbare Energie")
            
            with st.spinner("Laden 83109ENG..."):
                co2_data = cbs_api.get_co2_emissions()
            
            if has_data(co2_data):
                src = cbs_api.get_source('83109ENG')
                st.success(f"✅ CO₂ vermeden: {len(co2_data):,} records • `{src}`")
                
                period_col = 'Periods' if 'Periods' in co2_data.columns else 'Perioden'
                numeric_co2 = [c for c in co2_data.select_dtypes(include=[np.number]).columns if c != 'ID']
                
                # Look for avoided emission columns
                avoided_cols = [c for c in numeric_co2 if 'avoided' in c.lower() or 'vermeden' in c.lower()]
                if not avoided_cols:
                    avoided_cols = numeric_co2[:4]
                
                if period_col in co2_data.columns and avoided_cols:
                    co2_melt = co2_data.melt(id_vars=[period_col], value_vars=avoided_cols,
                                              var_name='Indicator', value_name='Waarde')
                    fig_co2 = px.bar(co2_melt, x=period_col, y='Waarde', color='Indicator',
                                      title="Vermeden CO₂ door hernieuwbare energie",
                                      barmode='group')
                    fig_co2.update_layout(height=400, template='plotly_white', xaxis_tickangle=-45)
                    st.plotly_chart(fig_co2, use_container_width=True)
                
                with st.expander("📋 Ruwe data (83109ENG)", expanded=False):
                    st.dataframe(co2_data, use_container_width=True, height=300)
            else:
                st.info("ℹ️ CO₂ vermeden data niet beschikbaar")
        
        # ================================================================
        # CBS TAB 4: PRIJZEN & VERBRUIK
        # ================================================================
        with cbs_tab4:
            st.subheader("💰 Energieprijzen & Verbruik")
            
            # ── Energy Prices ──
            st.subheader("📈 Energieprijzen (CPI, maandelijks)")
            
            with st.spinner("Laden 80324ned..."):
                price_data = cbs_api.get_energy_prices()
            
            if has_data(price_data):
                src = cbs_api.get_source('80324ned')
                st.success(f"✅ Prijsdata: {len(price_data):,} records • `{src}`")
                
                period_col = 'Perioden'
                numeric_price = [c for c in price_data.select_dtypes(include=[np.number]).columns if c != 'ID']
                
                if period_col in price_data.columns and numeric_price:
                    col_a, col_b = st.columns([1, 3])
                    
                    with col_a:
                        price_metric = st.selectbox("Prijs indicator:", numeric_price, key="price_metric")
                        if 'Energiedragers' in price_data.columns:
                            dragers = sorted(price_data['Energiedragers'].dropna().unique().tolist())
                            sel_dragers = st.multiselect("Energiedrager:", dragers,
                                                          default=dragers[:3], key="price_drager")
                        else:
                            sel_dragers = []
                    
                    with col_b:
                        plot_df = price_data.copy()
                        if sel_dragers and 'Energiedragers' in plot_df.columns:
                            plot_df = plot_df[plot_df['Energiedragers'].isin(sel_dragers)]
                        
                        if not plot_df.empty and price_metric:
                            fig_price = px.line(plot_df, x=period_col, y=price_metric,
                                                 color='Energiedragers' if 'Energiedragers' in plot_df.columns else None,
                                                 title=f"Energieprijzen — {price_metric}")
                            fig_price.update_layout(height=450, template='plotly_white', xaxis_tickangle=-45)
                            st.plotly_chart(fig_price, use_container_width=True)
                
                with st.expander("📋 Ruwe data (80324ned)", expanded=False):
                    st.dataframe(price_data, use_container_width=True, height=300)
            else:
                st.info("ℹ️ Prijsdata niet beschikbaar")
            
            st.markdown("---")
            
            # ── Consumption by Source ──
            st.subheader("🔋 Energieverbruik per Bron")
            
            with st.spinner("Laden 84917ENG..."):
                by_source = cbs_api.get_renewable_by_source()
            
            if has_data(by_source):
                src = cbs_api.get_source('84917ENG')
                st.success(f"✅ Verbruik per bron: {len(by_source):,} records • `{src}`")
                
                period_col = 'Periods' if 'Periods' in by_source.columns else 'Perioden'
                
                if 'FinalConsumption_1' in by_source.columns and period_col in by_source.columns:
                    col_a, col_b = st.columns([1, 3])
                    
                    with col_a:
                        if 'EnergySourcesAndTechniques' in by_source.columns:
                            sources = sorted(by_source['EnergySourcesAndTechniques'].dropna().unique().tolist())
                            sel_sources = st.multiselect("Energiebron:", sources, 
                                                          default=sources[:5], key="src_sources")
                        else:
                            sel_sources = []
                    
                    with col_b:
                        plot_df = by_source.copy()
                        if sel_sources and 'EnergySourcesAndTechniques' in plot_df.columns:
                            plot_df = plot_df[plot_df['EnergySourcesAndTechniques'].isin(sel_sources)]
                        
                        if not plot_df.empty:
                            fig_src = px.line(plot_df, x=period_col, y='FinalConsumption_1',
                                               color='EnergySourcesAndTechniques' if 'EnergySourcesAndTechniques' in plot_df.columns else None,
                                               title="Eindverbruik per energiebron")
                            fig_src.update_layout(height=450, template='plotly_white', xaxis_tickangle=-45)
                            st.plotly_chart(fig_src, use_container_width=True)
                
                with st.expander("📋 Ruwe data (84917ENG)", expanded=False):
                    st.dataframe(by_source, use_container_width=True, height=300)
            else:
                st.info("ℹ️ Verbruik per bron niet beschikbaar")
            
            st.markdown("---")
            
            # ── Industry Consumption ──
            st.subheader("🏭 Industrie Energieverbruik")
            
            with st.spinner("Laden 82369ENG..."):
                industry_data = cbs_api.get_energy_consumption_industry()
            
            if has_data(industry_data):
                src = cbs_api.get_source('82369ENG')
                st.success(f"✅ Industrie: {len(industry_data):,} records • `{src}`")
                
                with st.expander("📋 Ruwe data (82369ENG)", expanded=False):
                    st.dataframe(industry_data, use_container_width=True, height=300)
            else:
                st.info("ℹ️ Industrie data niet beschikbaar")
        
        # ================================================================
        # CBS TAB 5: DATASET EXPLORER
        # ================================================================
        with cbs_tab5:
            st.subheader("🔍 Dataset Explorer")
            st.markdown("*Verken elke CBS dataset interactief*")
            
            # Dataset selector
            dataset_options = {f"{did} — {info[1]}": did for did, info in cbs_api.DATASETS.items()}
            selected_label = st.selectbox("Selecteer dataset:", list(dataset_options.keys()), key="explorer_ds")
            selected_id = dataset_options[selected_label]
            
            with st.spinner(f"Laden {selected_id}..."):
                explorer_df = cbs_api.get_dataset(selected_id)
            
            if has_data(explorer_df):
                src = cbs_api.get_source(selected_id)
                st.success(f"✅ **{selected_id}**: {len(explorer_df):,} records × {explorer_df.shape[1]} kolommen • `{src}`")
                
                # Dataset overview
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Records", f"{len(explorer_df):,}")
                with col2:
                    st.metric("Kolommen", explorer_df.shape[1])
                with col3:
                    numeric_count = len(explorer_df.select_dtypes(include=[np.number]).columns)
                    st.metric("Numeriek", numeric_count)
                with col4:
                    mem_mb = explorer_df.memory_usage(deep=True).sum() / 1024 / 1024
                    st.metric("Geheugen", f"{mem_mb:.1f} MB")
                
                # Column info
                with st.expander("📊 Kolom informatie", expanded=True):
                    col_info = pd.DataFrame({
                        'Kolom': explorer_df.columns,
                        'Type': [str(explorer_df[c].dtype) for c in explorer_df.columns],
                        'Non-null': [explorer_df[c].notna().sum() for c in explorer_df.columns],
                        'Uniek': [explorer_df[c].nunique() for c in explorer_df.columns],
                        'Voorbeeld': [str(explorer_df[c].dropna().iloc[0])[:50] if explorer_df[c].notna().any() else '–' for c in explorer_df.columns],
                    })
                    st.dataframe(col_info, use_container_width=True, hide_index=True, height=300)
                
                # Quick chart
                numeric_cols = [c for c in explorer_df.select_dtypes(include=[np.number]).columns if c != 'ID']
                period_candidates = [c for c in explorer_df.columns if c.lower() in ['perioden', 'periods', 'jaar']]
                cat_candidates = [c for c in explorer_df.columns if explorer_df[c].dtype == 'object' and c not in period_candidates and explorer_df[c].nunique() < 50 and c != 'ID']
                
                if numeric_cols:
                    st.subheader("📈 Snelle Visualisatie")
                    
                    col_a, col_b, col_c = st.columns(3)
                    with col_a:
                        x_col = st.selectbox("X-as:", period_candidates + numeric_cols, key="exp_x")
                    with col_b:
                        y_col = st.selectbox("Y-as:", numeric_cols, key="exp_y")
                    with col_c:
                        color_col = st.selectbox("Kleur:", ['Geen'] + cat_candidates, key="exp_color")
                    
                    chart_type = st.radio("Type:", ["Lijn", "Bar", "Scatter", "Area"], horizontal=True, key="exp_chart")
                    
                    color_param = color_col if color_col != 'Geen' else None
                    
                    try:
                        if chart_type == "Lijn":
                            fig_exp = px.line(explorer_df, x=x_col, y=y_col, color=color_param)
                        elif chart_type == "Bar":
                            fig_exp = px.bar(explorer_df, x=x_col, y=y_col, color=color_param)
                        elif chart_type == "Scatter":
                            fig_exp = px.scatter(explorer_df, x=x_col, y=y_col, color=color_param)
                        else:
                            fig_exp = px.area(explorer_df, x=x_col, y=y_col, color=color_param)
                        
                        fig_exp.update_layout(height=450, template='plotly_white', xaxis_tickangle=-45)
                        st.plotly_chart(fig_exp, use_container_width=True)
                    except Exception as e:
                        st.warning(f"Visualisatie niet mogelijk: {e}")
                
                # Full data
                with st.expander("📋 Volledige dataset", expanded=False):
                    st.dataframe(explorer_df, use_container_width=True, height=400)
                
                # Download option
                csv_data = explorer_df.to_csv(index=False)
                st.download_button(
                    label=f"⬇️ Download {selected_id} als CSV",
                    data=csv_data,
                    file_name=f"{selected_id}_export.csv",
                    mime="text/csv",
                    key="explorer_download"
                )
            else:
                show_no_data_warning(f"Dataset {selected_id}")
            
            st.markdown("---")
            
            # Data source summary
            st.subheader("📊 Data Source Overzicht")
            if cbs_api.source:
                source_df = pd.DataFrame([
                    {'Dataset': did, 'Beschrijving': cbs_api.DATASETS.get(did, ('?', '?'))[1][:50], 'Bron': src}
                    for did, src in sorted(cbs_api.source.items())
                ])
                # Color code: local=green, api=orange, failed=red
                st.dataframe(source_df, use_container_width=True, hide_index=True)
                
                local_count = sum(1 for v in cbs_api.source.values() if v == 'local')
                api_count = sum(1 for v in cbs_api.source.values() if v == 'api')
                failed_count = sum(1 for v in cbs_api.source.values() if v == 'failed')
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("🟢 Lokaal", local_count)
                with col2:
                    st.metric("🟡 API", api_count)
                with col3:
                    st.metric("🔴 Gefaald", failed_count)
            else:
                st.info("Nog geen datasets geladen — selecteer een dataset hierboven.")
            
            st.markdown("---")
            
            st.info(f"""
            **CBS Open Data — Local-First Engine:**
            - 📦 **{local_stats['total']:,}** datasets lokaal beschikbaar ({len(local_stats.get('categories', {}))} categorieën)
            - ⚡ Lokale data wordt direct geladen (geen API latency)
            - 🔄 API fallback als lokale data niet beschikbaar is
            - 📊 16 kerndatasets voor energieanalyse geregistreerd
            - 💾 ~911 MB lokale CBS cache
            """)

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 2rem 0;'>
        <p><strong>KIIRA-PAY Energy Dashboard v2.1</strong></p>
        <p>TenneT TSO Nederland API (9 endpoints) • CBS Open Data (730+ datasets, local-first)</p>
        <p style='font-size: 0.9em;'>Real-time Grid Monitoring • Historische Energieanalyse • 45.710+ CBS records</p>
        <p style='font-size: 0.8em; color: #999;'>© 2024 KIIRA-PAY • Streamlit & Plotly</p>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# RUN APP
# ============================================================================

if __name__ == "__main__":
    main()
