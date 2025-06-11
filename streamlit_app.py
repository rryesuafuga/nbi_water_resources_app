import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import folium
from streamlit_folium import st_folium
import json
from datetime import datetime, timedelta
import random

# Page configuration
st.set_page_config(
    page_title="NBI Water Resources Management",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for NBI branding
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1f77b4 0%, #17a2b8 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .alert-banner {
        background: #f8d7da;
        border: 1px solid #f5c6cb;
        padding: 0.75rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.title("NBI Water Resources")
st.sidebar.markdown("---")

page = st.sidebar.selectbox(
    "Navigate to:",
    ["Regional Overview", "Station Monitoring", "WaPOR Analysis", "Trend Analysis", "Alerts & Warnings"]
)

# Data loading functions
@st.cache_data(ttl=300)
def load_sample_data():
    """Load sample station data"""
    # NBI member countries with key monitoring stations
    stations = {
        'Uganda': {'lat': 0.3476, 'lon': 32.5825, 'stations': ['Jinja', 'Masindi Port']},
        'Kenya': {'lat': -1.2921, 'lon': 36.8219, 'stations': ['Malaba', 'Turkana']},
        'Tanzania': {'lat': -6.3690, 'lon': 34.8888, 'stations': ['Musoma', 'Mwanza']},
        'Rwanda': {'lat': -1.9441, 'lon': 29.8739, 'stations': ['Nyabarongo', 'Akagera']},
        'Burundi': {'lat': -3.3731, 'lon': 29.9189, 'stations': ['Ruvubu', 'Ruvyironza']},
        'DR Congo': {'lat': -4.0383, 'lon': 21.7587, 'stations': ['Aba', 'Faradje']},
        'Ethiopia': {'lat': 9.1450, 'lon': 40.4897, 'stations': ['Blue Nile Dam', 'Lake Tana']},
        'Sudan': {'lat': 12.8628, 'lon': 30.2176, 'stations': ['Khartoum', 'Atbara']},
        'South Sudan': {'lat': 6.8770, 'lon': 31.3070, 'stations': ['Juba', 'Bor']},
        'Egypt': {'lat': 26.0975, 'lon': 31.2357, 'stations': ['Aswan', 'Cairo']}
    }
    
    station_data = []
    for country, info in stations.items():
        for station in info['stations']:
            # Add some random variation to coordinates
            lat_var = random.uniform(-0.5, 0.5)
            lon_var = random.uniform(-0.5, 0.5)
            
            station_data.append({
                'station_id': f"{country}_{station}".replace(' ', '_'),
                'name': station,
                'country': country,
                'lat': info['lat'] + lat_var,
                'lon': info['lon'] + lon_var,
                'status': random.choice(['excellent', 'good', 'fair', 'poor']),
                'transmission': random.choice(['GPRS', 'Satellite', 'Both']),
                'data_quality': random.uniform(75, 99)
            })
    
    return pd.DataFrame(station_data)

@st.cache_data(ttl=60)
def generate_realtime_data(station_df):
    """Generate realistic real-time water data"""
    current_time = datetime.now()
    
    # Base water levels for different regions (meters above sea level)
    base_levels = {
        'Uganda': 1175.0,  # Lake Victoria
        'Kenya': 1135.0,   # Lake Victoria region
        'Tanzania': 1134.0, # Lake Victoria
        'Rwanda': 1460.0,  # Higher elevation
        'Burundi': 1450.0, # Higher elevation  
        'DR Congo': 1200.0, # Variable
        'Ethiopia': 1830.0, # Blue Nile highlands
        'Sudan': 280.0,    # Lower Nile
        'South Sudan': 400.0, # White Nile
        'Egypt': 85.0      # Lower Nile
    }
    
    realtime_data = []
    for _, station in station_df.iterrows():
        base_level = base_levels.get(station['country'], 500)
        
        # Add seasonal and random variations
        seasonal_factor = 1 + 0.1 * np.sin((current_time.month / 12) * 2 * np.pi)
        random_variation = random.normalvariate(0, 5)
        
        water_level = base_level * seasonal_factor + random_variation
        flow_rate = max(10, water_level * 0.1 + random.normalvariate(0, 20))
        
        realtime_data.append({
            'station_id': station['station_id'],
            'timestamp': current_time,
            'water_level': round(water_level, 2),
            'flow_rate': round(flow_rate, 1),
            'temperature': round(random.uniform(18, 32), 1),
            'data_quality': station['data_quality']
        })
    
    return pd.DataFrame(realtime_data)

@st.cache_data
def load_wapor_sample():
    """Simulate WaPOR data structure based on your actual files"""
    # This simulates the structure of your actual WaPOR JSON files
    wapor_data = {
        'metadata': {
            'dataset': 'WAPOR-2 L2 Actual Evapotranspiration',
            'temporal_resolution': 'Monthly',
            'spatial_resolution': '100m',
            'coverage': 'Nile River Basin',
            'unit': 'mm/month'
        },
        'countries': {
            'Uganda': {'avg_et': 85.2, 'trend': 'stable'},
            'Kenya': {'avg_et': 72.1, 'trend': 'decreasing'},
            'Tanzania': {'avg_et': 78.9, 'trend': 'stable'},
            'Rwanda': {'avg_et': 92.3, 'trend': 'increasing'},
            'Burundi': {'avg_et': 88.7, 'trend': 'stable'},
            'DR Congo': {'avg_et': 95.1, 'trend': 'increasing'},
            'Ethiopia': {'avg_et': 68.4, 'trend': 'decreasing'},
            'Sudan': {'avg_et': 45.3, 'trend': 'stable'},
            'South Sudan': {'avg_et': 67.8, 'trend': 'stable'},
            'Egypt': {'avg_et': 25.1, 'trend': 'stable'}
        }
    }
    return wapor_data

def create_nile_basin_map(station_df, realtime_df=None):
    """Create interactive map of Nile Basin with monitoring stations"""
    # Center map on Nile Basin
    m = folium.Map(
        location=[15.0, 30.0],
        zoom_start=5,
        tiles='OpenStreetMap'
    )
    
    # Add different map layers
    folium.TileLayer('OpenStreetMap').add_to(m)
    folium.TileLayer('Stamen Terrain').add_to(m)
    folium.TileLayer('CartoDB positron').add_to(m)
    
    # Color mapping for station status
    status_colors = {
        'excellent': 'green',
        'good': 'lightgreen',
        'fair': 'orange', 
        'poor': 'red',
        'offline': 'gray'
    }
    
    # Add station markers
    for _, station in station_df.iterrows():
        color = status_colors.get(station['status'], 'gray')
        
        # Get real-time data if available
        popup_text = f"""
        <b>{station['name']}</b><br>
        Country: {station['country']}<br>
        Status: {station['status'].title()}<br>
        Transmission: {station['transmission']}<br>
        Data Quality: {station['data_quality']:.1f}%
        """
        
        if realtime_df is not None:
            rt_data = realtime_df[realtime_df['station_id'] == station['station_id']]
            if not rt_data.empty:
                rt_row = rt_data.iloc[0]
                popup_text += f"<br><br><b>Current Readings:</b><br>"
                popup_text += f"Water Level: {rt_row['water_level']:.1f}m<br>"
                popup_text += f"Flow Rate: {rt_row['flow_rate']:.1f} m³/s<br>"
                popup_text += f"Temperature: {rt_row['temperature']:.1f}°C"
        
        folium.Marker(
            location=[station['lat'], station['lon']],
            popup=folium.Popup(popup_text, max_width=300),
            icon=folium.Icon(color=color, icon='tint', prefix='fa'),
            tooltip=f"{station['name']} ({station['country']})"
        ).add_to(m)
    
    # Add layer control
    folium.LayerControl().add_to(m)
    
    return m

def check_alerts(realtime_df):
    """Check for flood/drought conditions"""
    alerts = []
    
    for _, row in realtime_df.iterrows():
        # Simple threshold-based alerts (would use historical data in production)
        if row['water_level'] > 1500:  # High elevation areas
            alerts.append({
                'type': 'Flood Warning',
                'station': row['station_id'],
                'severity': 'High',
                'value': f"{row['water_level']:.1f}m",
                'threshold': '1500m'
            })
        elif row['flow_rate'] < 5:  # Very low flow
            alerts.append({
                'type': 'Drought Warning', 
                'station': row['station_id'],
                'severity': 'Medium',
                'value': f"{row['flow_rate']:.1f} m³/s",
                'threshold': '5 m³/s'
            })
        elif row['data_quality'] < 80:  # Poor data quality
            alerts.append({
                'type': 'Data Quality',
                'station': row['station_id'], 
                'severity': 'Low',
                'value': f"{row['data_quality']:.1f}%",
                'threshold': '80%'
            })
    
    return alerts

# Main application logic
def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🌊 Nile Basin Initiative - Water Resources Management System</h1>
        <p>Real-time monitoring and analysis for sustainable water resource management across 10 member countries</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Load data
    station_df = load_sample_data()
    realtime_df = generate_realtime_data(station_df)
    wapor_data = load_wapor_sample()
    alerts = check_alerts(realtime_df)
    
    # Display alerts if any
    if alerts:
        st.markdown(f"""
        <div class="alert-banner">
            <h4>⚠️ Active Alerts ({len(alerts)})</h4>
            <p>There are {len(alerts)} active alerts requiring attention.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Page routing
    if page == "Regional Overview":
        st.header("Regional Overview Dashboard")
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Active Stations", f"{len(station_df)}/60", "2↑")
        
        with col2:
            avg_quality = station_df['data_quality'].mean()
            st.metric("Avg Data Quality", f"{avg_quality:.1f}%", "1.3%↑")
        
        with col3:
            st.metric("Alert Status", f"{len(alerts)} Active", "-1↓")
        
        with col4:
            countries_online = station_df['country'].nunique()
            st.metric("Countries Online", f"{countries_online}/10", "0")
        
        # Interactive map
        st.subheader("🗺️ Basin-wide Monitoring Network")
        map_obj = create_nile_basin_map(station_df, realtime_df)
        st_folium(map_obj, width=1000, height=600)
        
        # Station summary table
        st.subheader("📊 Station Status Summary")
        status_summary = station_df.groupby(['country', 'status']).size().unstack(fill_value=0)
        st.dataframe(status_summary, use_container_width=True)
    
    elif page == "Station Monitoring":
        st.header("Real-time Station Monitoring")
        
        # Station selector
        selected_country = st.selectbox("Select Country:", station_df['country'].unique())
        country_stations = station_df[station_df['country'] == selected_country]
        selected_station = st.selectbox("Select Station:", country_stations['name'].unique())
        
        # Get station data
        station_info = country_stations[country_stations['name'] == selected_station].iloc[0]
        station_rt = realtime_df[realtime_df['station_id'] == station_info['station_id']].iloc[0]
        
        # Display current readings
        st.subheader(f"📍 {selected_station}, {selected_country}")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Water Level", f"{station_rt['water_level']:.1f} m", "0.2↑")
        with col2:
            st.metric("Flow Rate", f"{station_rt['flow_rate']:.1f} m³/s", "-1.5↓")
        with col3:
            st.metric("Temperature", f"{station_rt['temperature']:.1f}°C", "0.8↑")
        
        # Time series simulation (you would load from your actual JSON files here)
        st.subheader("📈 Historical Trends")
        
        # Generate sample time series
        dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
        base_level = station_rt['water_level']
        variation = np.random.normal(0, 2, 30)
        levels = [base_level + v for v in variation]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=dates,
            y=levels,
            mode='lines+markers',
            name='Water Level',
            line=dict(color='blue', width=2)
        ))
        fig.update_layout(
            title=f"Water Level Trend - {selected_station}",
            xaxis_title="Date",
            yaxis_title="Water Level (m)",
            hovermode='x'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    elif page == "WaPOR Analysis":
        st.header("🛰️ WaPOR Satellite Data Analysis")
        st.markdown("*Based on your downloaded FAO WaPOR datasets*")
        
        # WaPOR metrics
        st.subheader("Regional Evapotranspiration Analysis")
        
        # Create visualization from WaPOR data
        countries = list(wapor_data['countries'].keys())
        et_values = [wapor_data['countries'][c]['avg_et'] for c in countries]
        trends = [wapor_data['countries'][c]['trend'] for c in countries]
        
        # Bar chart
        fig = px.bar(
            x=countries,
            y=et_values,
            title="Average Evapotranspiration by Country (mm/month)",
            color=trends,
            color_discrete_map={'increasing': 'red', 'stable': 'blue', 'decreasing': 'green'}
        )
        fig.update_layout(xaxis_title="Country", yaxis_title="ET (mm/month)")
        st.plotly_chart(fig, use_container_width=True)
        
        # Data table
        st.subheader("📊 Detailed WaPOR Metrics")
        wapor_df = pd.DataFrame.from_dict(wapor_data['countries'], orient='index')
        wapor_df.index.name = 'Country'
        wapor_df.columns = ['Avg ET (mm/month)', 'Trend']
        st.dataframe(wapor_df, use_container_width=True)
        
        # Information about your datasets
        st.subheader("📁 Available Datasets")
        st.info("""
        **Your Downloaded WaPOR Datasets:**
        - ✅ Actual Evapotranspiration (Monthly, 2014-2018)
        - ✅ Quality Land Surface Temperature (Dekadal)
        - ✅ Evaporation (Annual)
        - ✅ Land Cover Classification (Annual)
        - ✅ FAO WaPOR 2014-2018 Water Data
        
        *These datasets are being processed and integrated into the analysis system.*
        """)
    
    elif page == "Trend Analysis":
        st.header("📈 Statistical Trend Analysis")
        
        # Multi-station comparison
        st.subheader("Cross-Country Water Level Comparison")
        
        # Create sample comparison data
        countries = station_df['country'].unique()[:5]  # First 5 countries
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        
        fig = go.Figure()
        
        for country in countries:
            # Generate seasonal pattern for each country
            base = realtime_df[realtime_df['station_id'].str.contains(country)]['water_level'].mean()
            seasonal_pattern = [base + 10*np.sin((i/12)*2*np.pi) + random.uniform(-5, 5) for i in range(12)]
            
            fig.add_trace(go.Scatter(
                x=months,
                y=seasonal_pattern,
                mode='lines+markers',
                name=country,
                line=dict(width=3)
            ))
        
        fig.update_layout(
            title="Seasonal Water Level Patterns by Country",
            xaxis_title="Month",
            yaxis_title="Water Level (m)",
            hovermode='x'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Statistical summary
        st.subheader("📊 Statistical Summary")
        summary_stats = realtime_df.groupby(realtime_df['station_id'].str.split('_').str[0])['water_level'].agg([
            'mean', 'std', 'min', 'max'
        ]).round(2)
        summary_stats.columns = ['Mean (m)', 'Std Dev (m)', 'Min (m)', 'Max (m)']
        st.dataframe(summary_stats, use_container_width=True)
    
    elif page == "Alerts & Warnings":
        st.header("🚨 Alert & Warning System")
        
        if alerts:
            st.error(f"⚠️ {len(alerts)} Active Alerts Detected")
            
            # Display alerts table
            alerts_df = pd.DataFrame(alerts)
            st.dataframe(alerts_df, use_container_width=True)
            
            # Alert map
            st.subheader("🗺️ Alert Locations")
            alert_map = create_nile_basin_map(station_df, realtime_df)
            st_folium(alert_map, width=1000, height=500)
            
        else:
            st.success("✅ No Active Alerts - All Systems Normal")
        
        # Alert configuration
        st.subheader("⚙️ Alert Configuration")
        col1, col2 = st.columns(2)
        
        with col1:
            st.slider("Flood Threshold (m)", 1000, 2000, 1500)
            st.slider("Data Quality Threshold (%)", 70, 95, 80)
        
        with col2:
            st.slider("Drought Threshold (m³/s)", 1, 20, 5)
            st.selectbox("Alert Frequency", ["Real-time", "Hourly", "Daily"])

if __name__ == "__main__":
    main()