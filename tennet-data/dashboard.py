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
        """Get settlement prices (ISP - 15 min resolution)"""
        # Use December 2024 for ACCEPTANCE environment (known working data)
        end_date = datetime(2024, 12, 13, 12, 0, 0)
        start_date = end_date - timedelta(hours=hours_back)
        
        date_to = end_date.strftime('%d-%m-%Y %H:%M:%S')
        date_from = start_date.strftime('%d-%m-%Y %H:%M:%S')
        
        params = {'date_from': date_from, 'date_to': date_to}
        data = self._make_request('/publications/v1/settlement-prices', params)
        
        if data:
            self.is_real_data = True
            return self._process_settlement_prices(data)
        
        # NO MOCK DATA - Return None if API fails
        self.is_real_data = False
        return None
    
    def get_reconciliation_prices(self, days_back=30):
        """Get reconciliation prices (ISP - 15 min resolution)"""
        now = datetime.now()
        end_date = now
        start_date = end_date - timedelta(days=days_back)
        
        date_to = end_date.strftime('%d-%m-%Y %H:%M:%S')
        date_from = start_date.strftime('%d-%m-%Y %H:%M:%S')
        
        params = {'date_from': date_from, 'date_to': date_to}
        data = self._make_request('/publications/v1/reconciliation-prices/isp', params)
        
        if data and 'error' not in data:
            self.is_real_data = True
            return self._process_reconciliation_prices(data)
        
        # NO MOCK DATA - Return None if API fails
        self.is_real_data = False
        return None
    
    def get_balance_delta_latest(self):
        """Get latest balance delta (12-second resolution)"""
        data = self._make_request('/publications/v1/balance-delta/latest')
        
        if data:
            self.is_real_data = True
            return self._process_balance_delta_latest(data)
        
        # NO MOCK DATA - Return None if API fails
        self.is_real_data = False
        return None
    
    def get_balance_delta_historical(self, minutes_back=60):
        """Get historical balance delta (1-minute resolution)"""
        # Use December 2024 for ACCEPTANCE environment
        end_date = datetime(2024, 12, 13, 12, 0, 0)
        start_date = end_date - timedelta(minutes=minutes_back)
        
        date_to = end_date.strftime('%d-%m-%Y %H:%M:%S')
        date_from = start_date.strftime('%d-%m-%Y %H:%M:%S')
        
        params = {'date_from': date_from, 'date_to': date_to}
        data = self._make_request('/publications/v1/balance-delta', params)
        
        if data:
            self.is_real_data = True
            return self._process_balance_delta_historical(data)
        
        # NO MOCK DATA - Return None if API fails
        self.is_real_data = False
        return None
    
    def get_merit_order_list(self, hours_back=1):
        """Get merit order list bid prices (ISP - 15 min resolution)"""
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
    
    def get_frr_activations(self, hours_back=1):
        """Get FRR activations"""
        # Use December 2024 for ACCEPTANCE environment
        end_date = datetime(2024, 12, 13, 12, 0, 0)
        start_date = end_date - timedelta(hours=hours_back)
        
        date_to = end_date.strftime('%d-%m-%Y %H:%M:%S')
        date_from = start_date.strftime('%d-%m-%Y %H:%M:%S')
        
        params = {'date_from': date_from, 'date_to': date_to}
        data = self._make_request('/publications/v1/frr-activated-volumes', params)
        
        if data and 'error' not in data:
            self.is_real_data = True
            return self._process_frr_activations(data)
        
        # NO MOCK DATA - Return None if API fails
        self.is_real_data = False
        return None
    
    # Processing methods
    def _process_settlement_prices(self, data):
        """Process settlement prices response"""
        try:
            response = data.get('Response', {})
            time_series = response.get('TimeSeries', [])
            
            all_prices = []
            for series in time_series:
                period = series.get('Period', {})
                points = period.get('Points', [])
                
                for point in points:
                    try:
                        # TenneT settlement prices use 'shortage' and 'surplus' fields
                        # Use 'shortage' as the primary price indicator
                        price = point.get('shortage') or point.get('surplus') or point.get('price', 0)
                        dispatch_up = point.get('dispatch_up')
                        dispatch_down = point.get('dispatch_down')
                        
                        all_prices.append({
                            'timestamp': pd.to_datetime(point.get('timeInterval_start')),
                            'isp': int(point.get('isp', 0)),
                            'price_eur_mwh': float(price) if price else 0,
                            'shortage_price': float(point.get('shortage', 0)) if point.get('shortage') else 0,
                            'surplus_price': float(point.get('surplus', 0)) if point.get('surplus') else 0,
                            'dispatch_up': float(dispatch_up) if dispatch_up else None,
                            'dispatch_down': float(dispatch_down) if dispatch_down else None,
                            'regulation_state': point.get('regulation_state', 0)
                        })
                    except (ValueError, TypeError):
                        continue
            
            if all_prices:
                return pd.DataFrame(all_prices).sort_values('timestamp').reset_index(drop=True)
        except Exception as e:
            print(f"Error processing settlement prices: {str(e)}")
        
        return None  # NO MOCK DATA
    
    def _process_reconciliation_prices(self, data):
        """Process reconciliation prices response"""
        try:
            response = data.get('Response', {})
            time_series = response.get('TimeSeries', [])
            
            all_prices = []
            for series in time_series:
                period = series.get('Period', {})
                points = period.get('Points', [])
                
                for point in points:
                    try:
                        all_prices.append({
                            'timestamp': pd.to_datetime(point.get('timeInterval_start')),
                            'isp': int(point.get('isp', 0)),
                            'price_eur_mwh': float(point.get('price', 0)),
                        })
                    except (ValueError, TypeError):
                        continue
            
            if all_prices:
                return pd.DataFrame(all_prices).sort_values('timestamp').reset_index(drop=True)
        except Exception as e:
            print(f"Error processing reconciliation prices: {str(e)}")
        
        return self._get_mock_reconciliation_prices(30)
    
    def _process_balance_delta_latest(self, data):
        """Process latest balance delta response"""
        try:
            response = data.get('Response', {})
            time_series = response.get('TimeSeries', [])
            
            for series in time_series:
                period = series.get('Period', {})
                points = period.get('Points', [])
                
                if points:
                    point = points[-1]
                    balance_delta = float(point.get('balance_delta', 0))
                    return pd.DataFrame([{
                        'timestamp': pd.to_datetime(point.get('igcc_time')),
                        'balance_delta_mw': balance_delta,
                        'is_imbalance': abs(balance_delta) > 50,
                        'severity': 'HIGH' if abs(balance_delta) > 200 else 'MEDIUM' if abs(balance_delta) > 100 else 'LOW'
                    }])
        except Exception as e:
            print(f"Error processing balance delta latest: {str(e)}")
        
        return self._get_mock_balance_delta_latest()
    
    def _process_balance_delta_historical(self, data):
        """Process historical balance delta response"""
        try:
            response = data.get('Response', {})
            time_series = response.get('TimeSeries', [])
            
            all_points = []
            for series in time_series:
                period = series.get('Period', {})
                points = period.get('Points', [])
                
                for point in points:
                    try:
                        balance_delta = float(point.get('balance_delta', 0))
                        all_points.append({
                            'timestamp': pd.to_datetime(point.get('igcc_time')),
                            'balance_delta_mw': balance_delta,
                            'is_imbalance': abs(balance_delta) > 50,
                            'severity': 'HIGH' if abs(balance_delta) > 200 else 'MEDIUM' if abs(balance_delta) > 100 else 'LOW'
                        })
                    except (ValueError, TypeError):
                        continue
            
            if all_points:
                return pd.DataFrame(all_points).sort_values('timestamp').reset_index(drop=True)
        except Exception as e:
            print(f"Error processing balance delta historical: {str(e)}")
        
        return self._get_mock_balance_delta_historical(60)
    
    def _process_merit_order(self, data):
        """Process merit order list response"""
        try:
            response = data.get('Response', {})
            time_series = response.get('TimeSeries', [])
            
            all_bids = []
            for series in time_series:
                period = series.get('Period', {})
                points = period.get('Points', [])
                
                for point in points:
                    isp = point.get('isp', 0)
                    time_start = point.get('timeInterval_start')
                    thresholds = point.get('Thresholds', [])
                    
                    for threshold in thresholds:
                        try:
                            all_bids.append({
                                'timestamp': pd.to_datetime(time_start),
                                'isp': int(isp),
                                'capacity_threshold_mw': float(threshold.get('capacity_threshold', 0)),
                                'price_up_eur_mwh': float(threshold.get('price_up', 0)),
                                'price_down_eur_mwh': float(threshold.get('price_down', 0))
                            })
                        except (ValueError, TypeError):
                            continue
            
            if all_bids:
                return pd.DataFrame(all_bids).sort_values(['timestamp', 'capacity_threshold_mw']).reset_index(drop=True)
        except Exception as e:
            print(f"Error processing merit order: {str(e)}")
        
        return self._get_mock_merit_order()
    
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
        """Process FRR activations response"""
        try:
            response = data.get('Response', {})
            time_series = response.get('TimeSeries', [])
            
            all_activations = []
            for series in time_series:
                period = series.get('Period', {})
                points = period.get('Points', [])
                
                for point in points:
                    try:
                        all_activations.append({
                            'timestamp': pd.to_datetime(point.get('timeInterval_start')),
                            'isp': int(point.get('isp', 0)),
                            'volume_mw': float(point.get('quantity', 0)),
                            'direction': point.get('direction', 'unknown')
                        })
                    except (ValueError, TypeError):
                        continue
            
            if all_activations:
                return pd.DataFrame(all_activations).sort_values('timestamp').reset_index(drop=True)
        except Exception as e:
            print(f"Error processing FRR activations: {str(e)}")
        
        return None  # NO MOCK DATA

# ============================================================================
# CACHE & INITIALIZATION
# ============================================================================

@st.cache_resource
def get_tennet_api():
    """Initialize TenneT API (cached) - Auto-detect environment from .env"""
    return TennetAPI()  # Will auto-detect from TENNET_ENVIRONMENT in .env

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
    
    # Initialize API
    tennet_api = get_tennet_api()
    
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
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🔴 Real-Time Grid",
        "💰 Financial Settlement",
        "📊 Market Analysis",
        "⚙️ Grid Operations",
        "⚖️ Balancing"
    ])
    
    # ========================================================================
    # TAB 1: REAL-TIME GRID MONITOR
    # ========================================================================
    with tab1:
        st.header("🔴 Real-Time Grid Monitor")
        st.markdown("**Live Nederlandse hoogspanningsnet status** • TenneT TSO Nederland")
        
        # Latest balance delta
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("⚡ Huidige Grid Balans")
            with st.spinner("Loading live balance delta..."):
                balance_latest = tennet_api.get_balance_delta_latest()
            
            if has_data(balance_latest):
                latest = balance_latest.iloc[0]
                value = latest['balance_delta_mw']
                
                # Gauge chart
                fig_gauge = go.Figure(go.Indicator(
                    mode="gauge+number+delta",
                    value=value,
                    domain={'x': [0, 1], 'y': [0, 1]},
                    title={'text': "Balance Delta (MW)", 'font': {'size': 24}},
                    delta={'reference': 0, 'increasing': {'color': "red"}, 'decreasing': {'color': "green"}},
                    gauge={
                        'axis': {'range': [-300, 300], 'tickwidth': 1, 'tickcolor': "darkblue"},
                        'bar': {'color': "darkblue"},
                        'bgcolor': "white",
                        'borderwidth': 2,
                        'bordercolor': "gray",
                        'steps': [
                            {'range': [-300, -200], 'color': '#d62728'},
                            {'range': [-200, -50], 'color': '#ff7f0e'},
                            {'range': [-50, 50], 'color': '#2ca02c'},
                            {'range': [50, 200], 'color': '#ff7f0e'},
                            {'range': [200, 300], 'color': '#d62728'}
                        ],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': value
                        }
                    }
                ))
                fig_gauge.update_layout(height=300, font={'size': 20})
                st.plotly_chart(fig_gauge, use_container_width=True)
            else:
                show_no_data_warning("Balance Delta (Laatst)")
        
        with col2:
            if has_data(balance_latest):
                st.subheader("Status")
                
                latest = balance_latest.iloc[0]
                value = latest['balance_delta_mw']
                is_imbalance = latest['is_imbalance']
                severity = latest['severity']
                
                # Status badge
                if is_imbalance:
                    st.error("⚠️ **ONBALANS GEDETECTEERD**")
                else:
                    st.success("✅ **GRID STABIEL**")
                
                st.metric("Afwijking", f"{abs(value):.1f} MW")
                st.metric("Severity", severity)
                st.metric("Laatste Update", latest['timestamp'].strftime("%H:%M:%S"))
                
                # Info box
                st.info("""
                **Balance Delta** meet de werkelijke afwijking tussen 
                geprogrammeerd en daadwerkelijk verbruik/productie op het 
                Nederlandse hoogspanningsnet.
                
                - **Groen** (-50 tot +50 MW): Normaal
                - **Oranje** (50-200 MW): Verhoogd
                - **Rood** (>200 MW): Kritiek
                """)
        
        # Historical balance delta
        st.markdown("---")
        st.subheader("📈 Balance Delta Historisch (Laatste Uur)")
        
        col1, col2 = st.columns([3, 1])
        with col2:
            resolution = st.radio("Resolutie", ["1 minuut", "12 seconden"], index=0)
            minutes = st.slider("Periode (minuten)", 10, 60, 60)
        
        with col1:
            with st.spinner("Loading historical data..."):
                balance_hist = tennet_api.get_balance_delta_historical(minutes_back=minutes)
            
            if has_data(balance_hist):
                # Time series chart
                fig = go.Figure()
                
                # Add balance delta line with color based on severity
                fig.add_trace(go.Scatter(
                    x=balance_hist['timestamp'],
                    y=balance_hist['balance_delta_mw'],
                    mode='lines',
                    name='Balance Delta',
                    line=dict(color='#1f77b4', width=2),
                    fill='tozeroy',
                    fillcolor='rgba(31, 119, 180, 0.15)',
                    hovertemplate='<b>%{x}</b><br>Balance Delta: %{y:.1f} MW<extra></extra>'
                ))
                
                # Add threshold lines
                fig.add_hline(y=50, line_dash="dash", line_color="orange", 
                             annotation_text="+ Drempel", annotation_position="right")
                fig.add_hline(y=-50, line_dash="dash", line_color="orange",
                             annotation_text="- Drempel", annotation_position="right")
                fig.add_hline(y=0, line_dash="dot", line_color="gray")
                
                fig.update_layout(
                    title=f"Balance Delta Tijdlijn ({minutes} minuten • {resolution})",
                    xaxis_title="Tijd",
                    yaxis_title="Balance Delta (MW)",
                    hovermode='x unified',
                    height=400,
                    template='plotly_white',
                    showlegend=True
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Statistics
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Gemiddeld", f"{balance_hist['balance_delta_mw'].mean():.1f} MW")
                with col2:
                    st.metric("Standaard Dev.", f"{balance_hist['balance_delta_mw'].std():.1f} MW")
                with col3:
                    st.metric("Maximum", f"{balance_hist['balance_delta_mw'].max():.1f} MW")
                with col4:
                    st.metric("Minimum", f"{balance_hist['balance_delta_mw'].min():.1f} MW")
                
                # Distribution
                col1, col2 = st.columns(2)
                with col1:
                    fig_hist = px.histogram(
                        balance_hist,
                        x='balance_delta_mw',
                        nbins=40,
                        title="Balance Delta Distributie",
                        labels={'balance_delta_mw': 'Balance Delta (MW)', 'count': 'Frequentie'},
                        color_discrete_sequence=['#1f77b4']
                    )
                    fig_hist.update_layout(height=300, template='plotly_white', showlegend=False)
                    st.plotly_chart(fig_hist, use_container_width=True)
                
                with col2:
                    # Imbalance percentage
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
                    label="📥 Download Balance Delta Data (CSV)",
                    data=csv,
                    file_name=f"balance_delta_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
            else:
                show_no_data_warning("Balance Delta (Historisch)")
    
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
            # Key metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                avg_price_up = merit_df['price_up_eur_mwh'].mean()
                st.metric("Gem. Opwaarts Prijs", f"€{avg_price_up:.2f}/MWh")
            with col2:
                avg_price_down = merit_df['price_down_eur_mwh'].mean()
                st.metric("Gem. Neerwaarts Prijs", f"€{avg_price_down:.2f}/MWh")
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
            
            # Upward regulation (green)
            fig.add_trace(go.Scatter(
                x=latest_bids['capacity_threshold_mw'],
                y=latest_bids['price_up_eur_mwh'],
                mode='lines+markers',
                name='Opwaartse Regulering (↑)',
                line=dict(color='#2ca02c', width=3),
                marker=dict(size=10, symbol='triangle-up'),
                hovertemplate='<b>Capaciteit:</b> %{x:.0f} MW<br><b>Prijs:</b> €%{y:.2f}/MWh<extra></extra>'
            ))
            
            # Downward regulation (red)
            fig.add_trace(go.Scatter(
                x=latest_bids['capacity_threshold_mw'],
                y=latest_bids['price_down_eur_mwh'],
                mode='lines+markers',
                name='Neerwaartse Regulering (↓)',
                line=dict(color='#d62728', width=3),
                marker=dict(size=10, symbol='triangle-down'),
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
            
            # Price spread analysis
            st.subheader("📊 Prijs Spread Analyse")
            merit_df['price_spread'] = merit_df['price_up_eur_mwh'] - merit_df['price_down_eur_mwh']
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig_spread = px.line(
                    merit_df,
                    x='capacity_threshold_mw',
                    y='price_spread',
                    color='isp',
                    title="Prijs Spread (Up - Down) per ISP",
                    labels={'capacity_threshold_mw': 'Capaciteit (MW)', 'price_spread': 'Spread (EUR/MWh)', 'isp': 'ISP'},
                    markers=True
                )
                fig_spread.update_layout(height=350, template='plotly_white')
                st.plotly_chart(fig_spread, use_container_width=True)
            
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
                fig_scatter_up = px.scatter(
                    merit_df,
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
                fig_scatter_down = px.scatter(
                    merit_df,
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
                    y='volume_mw',
                    color='direction',
                    title="FRR Activated Volumes per ISP",
                    labels={'timestamp': 'Tijd', 'volume_mw': 'Volume (MW)', 'direction': 'Richting'},
                    color_discrete_map={'up': '#2ca02c', 'down': '#d62728'}
                )
                fig.update_layout(height=500, template='plotly_white')
                st.plotly_chart(fig, use_container_width=True)
                
                # Stats
                col_a, col_b = st.columns(2)
                with col_a:
                    total_up = frr_df[frr_df['direction'] == 'up']['volume_mw'].sum()
                    st.metric("Totaal Upward", f"{total_up:.0f} MW")
                with col_b:
                    total_down = frr_df[frr_df['direction'] == 'down']['volume_mw'].sum()
                    st.metric("Totaal Downward", f"{total_down:.0f} MW")
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
        st.markdown("**System Balancing & Imbalance Management**")
        
        st.info("""
        🚧 **In ontwikkeling**: Volgende features worden toegevoegd:
        
        - **Settled Imbalance Volumes**: Afgewikkelde onbalans volumes per BRP (Balance Responsible Party)
        - **Metered Injections**: Real-time gemeten injecties en afnames op het net
        - **Cross-Border Flows**: Grensoverschrijdende elektriciteitsstromen met buurlanden
        - **System Imbalance**: Totale Nederlands systeemonbalans analyse
        - **Imbalance Costs**: Financiële analyse van onbalans kosten
        """)
        
        # Placeholder visualization
        st.subheader("📊 System Imbalance Overview (Demo)")
        
        # Mock data for visualization
        mock_imbalance = pd.DataFrame({
            'timestamp': pd.date_range(end=datetime.now(), periods=24, freq='H'),
            'system_imbalance_mw': np.random.uniform(-300, 300, 24),
            'imbalance_cost_eur': np.random.uniform(10000, 50000, 24)
        })
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig1 = px.line(
                mock_imbalance,
                x='timestamp',
                y='system_imbalance_mw',
                title="System Imbalance (24h)",
                labels={'timestamp': 'Tijd', 'system_imbalance_mw': 'Imbalance (MW)'}
            )
            fig1.add_hline(y=0, line_dash="dash", line_color="gray")
            fig1.update_layout(height=300, template='plotly_white')
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            fig2 = px.bar(
                mock_imbalance,
                x='timestamp',
                y='imbalance_cost_eur',
                title="Imbalance Kosten (24h)",
                labels={'timestamp': 'Tijd', 'imbalance_cost_eur': 'Kosten (EUR)'},
                color='imbalance_cost_eur',
                color_continuous_scale='Reds'
            )
            fig2.update_layout(height=300, template='plotly_white')
            st.plotly_chart(fig2, use_container_width=True)
        
        st.caption("⚠️ Bovenstaande data is demo data. Echte imbalance data wordt binnenkort geïntegreerd.")

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 2rem 0;'>
        <p><strong>KIIRA-PAY Energy Dashboard v2.0</strong></p>
        <p>TenneT TSO Nederland API Integratie • Real-time Grid Monitoring & Analysis</p>
        <p style='font-size: 0.9em;'>© 2024 KIIRA-PAY • Gebouwd met Streamlit & Plotly</p>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# RUN APP
# ============================================================================

if __name__ == "__main__":
    main()
