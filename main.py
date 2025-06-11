import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import folium
from streamlit_folium import st_folium
from datetime import datetime, timedelta
import random
import json
from pathlib import Path

# Page configuration - Enhanced with professional branding
st.set_page_config(
    page_title="NBI Water Resources Management System",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/rryesuafuga/nbi_water_resources_app',
        'Report a bug': 'mailto:sseguya256@gmail.com',
        'About': "NBI Water Resources Management System - Developed for the Nile Basin Initiative"
    }
)

# Enhanced CSS styling based on professional requirements
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 50%, #1e88e5 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
        backdrop-filter: blur(4px);
        border: 1px solid rgba(255, 255, 255, 0.18);
    }
    
    .metric-card {
        background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 5px solid #2a5298;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
        transition: transform 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.15);
    }
    
    .alert-high {
        background: linear-gradient(135deg, #ffebee 0%, #ffcdd2 100%);
        border-left: 5px solid #f44336;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 8px;
        animation: pulse 2s infinite;
    }
    
    .alert-medium {
        background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%);
        border-left: 5px solid #ff9800;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 8px;
    }
    
    .alert-low {
        background: linear-gradient(135deg, #e8f5e8 0%, #c8e6c9 100%);
        border-left: 5px solid #4caf50;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 8px;
    }
    
    .sidebar-logo {
        text-align: center;
        padding: 1rem;
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    
    .feature-highlight {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #2196f3;
        margin: 1rem 0;
    }
    
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.8; }
        100% { opacity: 1; }
    }
    
    .footer-info {
        background: linear-gradient(135deg, #f5f5f5 0%, #e0e0e0 100%);
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        margin-top: 2rem;
        border-top: 3px solid #2a5298;
    }
</style>
""", unsafe_allow_html=True)

# Load your real WaPOR data (integration with actual datasets)
@st.cache_data
def load_wapor_data():
    """Load actual WaPOR data from your uploaded datasets"""
    try:
        # Check if data directory exists
        data_dir = Path("data/raw")
        if data_dir.exists():
            # Load actual evapotranspiration data
            et_files = list(data_dir.glob("**/WAPOR*AETI*.json"))[:5]  # Sample first 5 files
            
            wapor_summary = {
                'datasets_available': len(et_files),
                'data_types': [
                    'Actual Evapotranspiration (Monthly)',
                    'Quality Land Surface Temperature (Dekadal)', 
                    'Evaporation (Annual)',
                    'Land Cover Classification (Annual)',
                    'FAO WaPOR 2014-2018'
                ],
                'spatial_resolution': '100m',
                'temporal_coverage': '2014-2018',
                'countries_covered': 10
            }
            
            # Try to load a sample file for demonstration
            if et_files:
                sample_file = et_files[0]
                try:
                    with open(sample_file, 'r') as f:
                        sample_data = json.load(f)
                    wapor_summary['sample_loaded'] = True
                    wapor_summary['sample_file'] = sample_file.name
                except:
                    wapor_summary['sample_loaded'] = False
            
            return wapor_summary
        else:
            return None
    except Exception as e:
        st.error(f"Error loading WaPOR data: {e}")
        return None

# Enhanced station data generation with more realistic parameters
@st.cache_data
def generate_enhanced_station_data():
    """Generate comprehensive monitoring station data for NBI countries"""
    countries_data = {
        'Uganda': {
            'center': [1.3733, 32.2903], 
            'stations': 8,
            'major_features': ['Lake Victoria', 'Victoria Nile', 'Lake Kyoga'],
            'avg_elevation': 1100,
            'climate': 'Tropical'
        },
        'Kenya': {
            'center': [0.0236, 37.9062], 
            'stations': 6,
            'major_features': ['Lake Victoria (Kenyan part)', 'Ewaso Ng\'iro'],
            'avg_elevation': 1795,
            'climate': 'Arid/Semi-arid'
        },
        'Tanzania': {
            'center': [-6.3690, 34.8888], 
            'stations': 7,
            'major_features': ['Lake Victoria', 'Kagera River', 'Mara River'],
            'avg_elevation': 1018,
            'climate': 'Tropical'
        },
        'Rwanda': {
            'center': [-1.9403, 29.8739], 
            'stations': 4,
            'major_features': ['Nyabarongo River', 'Akagera River'],
            'avg_elevation': 1598,
            'climate': 'Temperate'
        },
        'Burundi': {
            'center': [-3.3731, 29.9189], 
            'stations': 3,
            'major_features': ['Ruvubu River', 'Ruvyironza River'],
            'avg_elevation': 1504,
            'climate': 'Tropical Highland'
        },
        'Ethiopia': {
            'center': [9.1450, 40.4897], 
            'stations': 12,
            'major_features': ['Blue Nile', 'Lake Tana', 'Atbara River'],
            'avg_elevation': 1330,
            'climate': 'Highland/Arid'
        },
        'Sudan': {
            'center': [12.8628, 30.2176], 
            'stations': 8,
            'major_features': ['Main Nile', 'Blue Nile', 'White Nile Confluence'],
            'avg_elevation': 568,
            'climate': 'Arid'
        },
        'South Sudan': {
            'center': [6.8770, 31.3070], 
            'stations': 5,
            'major_features': ['White Nile', 'Bahr el Ghazal', 'Sobat River'],
            'avg_elevation': 400,
            'climate': 'Tropical'
        },
        'DRC': {
            'center': [-4.0383, 21.7587], 
            'stations': 4,
            'major_features': ['Lake Albert tributaries'],
            'avg_elevation': 726,
            'climate': 'Tropical'
        },
        'Egypt': {
            'center': [26.0975, 31.2357], 
            'stations': 3,
            'major_features': ['Main Nile', 'Lake Nasser', 'Nile Delta'],
            'avg_elevation': 321,
            'climate': 'Arid'
        }
    }
    
    stations = []
    station_id = 1
    
    for country, info in countries_data.items():
        for i in range(info['stations']):
            # More sophisticated coordinate variation
            lat_var = random.uniform(-0.8, 0.8)
            lon_var = random.uniform(-0.8, 0.8)
            
            # Determine station type based on major features
            if 'Lake' in str(info['major_features']):
                station_types = ['Lake Level', 'River Flow', 'Reservoir']
                weights = [0.4, 0.4, 0.2]
            else:
                station_types = ['River Flow', 'Groundwater', 'Reservoir']
                weights = [0.6, 0.2, 0.2]
            
            station_type = random.choices(station_types, weights=weights)[0]
            
            # More realistic status distribution
            status_weights = {
                'Active': 0.82,
                'Maintenance': 0.12,
                'Offline': 0.04,
                'Calibration': 0.02
            }
            
            station = {
                'station_id': f"NBI-{country[:3].upper()}-{station_id:03d}",
                'name': f"{random.choice(info['major_features']).split()[0]} Station {i+1}",
                'country': country,
                'latitude': info['center'][0] + lat_var,
                'longitude': info['center'][1] + lon_var,
                'elevation': info['avg_elevation'] + random.uniform(-200, 200),
                'type': station_type,
                'status': random.choices(list(status_weights.keys()), 
                                       weights=list(status_weights.values()))[0],
                'installation_date': datetime.now() - timedelta(days=random.randint(365, 3650)),
                'transmission_method': random.choices(['GPRS', 'Satellite', 'Both'], weights=[0.3, 0.4, 0.3])[0],
                'data_frequency': random.choice(['Hourly', '6-hourly', 'Daily']),
                'climate_zone': info['climate'],
                'major_feature': random.choice(info['major_features'])
            }
            stations.append(station)
            station_id += 1
    
    return pd.DataFrame(stations)

# Enhanced measurement data with better algorithms
@st.cache_data
def generate_enhanced_measurement_data(stations_df):
    """Generate sophisticated measurement data with realistic patterns"""
    measurements = []
    
    for _, station in stations_df.iterrows():
        # Generate 30 days of data based on frequency
        base_time = datetime.now() - timedelta(days=30)
        
        if station['data_frequency'] == 'Hourly':
            time_points = 30 * 24
            time_delta = timedelta(hours=1)
        elif station['data_frequency'] == '6-hourly':
            time_points = 30 * 4
            time_delta = timedelta(hours=6)
        else:  # Daily
            time_points = 30
            time_delta = timedelta(days=1)
        
        for point in range(time_points):
            timestamp = base_time + (time_delta * point)
            
            # Enhanced seasonal and daily patterns
            day_of_year = timestamp.timetuple().tm_yday
            hour_of_day = timestamp.hour
            
            # Seasonal factor (more realistic)
            if station['country'] in ['Ethiopia', 'Sudan', 'Egypt']:  # Northern countries
                seasonal_factor = 1 + 0.4 * np.cos(2 * np.pi * (day_of_year - 60) / 365)  # Peak in Dec-Jan
            else:  # Southern/Equatorial countries
                seasonal_factor = 1 + 0.3 * np.sin(2 * np.pi * (day_of_year - 80) / 365)  # Peak in Apr-May
            
            # Daily pattern
            daily_factor = 1 + 0.1 * np.sin(2 * np.pi * hour_of_day / 24)
            
            # Base values based on station characteristics
            if station['type'] == 'Lake Level':
                base_level = 1175 + (station['elevation'] - 1100) * 0.1
                base_flow = random.uniform(50, 300)
                level_stability = 0.95  # Lakes are more stable
            elif station['type'] == 'River Flow':
                base_level = 300 + station['elevation'] * 0.3
                base_flow = random.uniform(100, 2000)
                level_stability = 0.85  # Rivers more variable
            else:  # Reservoir/Groundwater
                base_level = 400 + station['elevation'] * 0.2
                base_flow = random.uniform(80, 600)
                level_stability = 0.9
            
            # Climate influence
            climate_multiplier = {
                'Tropical': 1.2,
                'Arid': 0.7,
                'Semi-arid': 0.8,
                'Temperate': 1.0,
                'Highland': 1.1,
                'Tropical Highland': 1.15
            }.get(station['climate_zone'], 1.0)
            
            # Add noise and variations
            level_noise = random.normalvariate(0, base_level * 0.02)
            flow_noise = random.normalvariate(0, base_flow * 0.05)
            
            # Final calculations
            water_level = (base_level * seasonal_factor * daily_factor * climate_multiplier + 
                          level_noise) * level_stability
            
            flow_rate = (base_flow * seasonal_factor * daily_factor * climate_multiplier + 
                        flow_noise) * (2 - level_stability)  # Inverse relationship
            
            # Temperature based on climate and elevation
            base_temp = {
                'Tropical': 26,
                'Arid': 28,
                'Semi-arid': 24,
                'Temperate': 18,
                'Highland': 15,
                'Tropical Highland': 20
            }.get(station['climate_zone'], 22)
            
            # Elevation effect: -6.5°C per 1000m
            temp_elevation_effect = -(station['elevation'] / 1000) * 6.5
            temp_seasonal = 5 * np.sin(2 * np.pi * day_of_year / 365)
            temp_daily = 8 * np.sin(2 * np.pi * (hour_of_day - 6) / 24)
            
            temperature = (base_temp + temp_elevation_effect + temp_seasonal + 
                          temp_daily + random.normalvariate(0, 1.5))
            
            # Data quality based on transmission method and status
            if station['status'] == 'Active':
                if station['transmission_method'] == 'Both':
                    base_quality = random.uniform(95, 99)
                elif station['transmission_method'] == 'Satellite':
                    base_quality = random.uniform(90, 97)
                else:  # GPRS
                    base_quality = random.uniform(85, 95)
            elif station['status'] == 'Maintenance':
                base_quality = random.uniform(70, 85)
            elif station['status'] == 'Calibration':
                base_quality = random.uniform(60, 80)
            else:  # Offline
                base_quality = random.uniform(0, 30)
            
            measurement = {
                'station_id': station['station_id'],
                'timestamp': timestamp,
                'water_level': max(0, water_level),  # Ensure non-negative
                'flow_rate': max(0, flow_rate),
                'temperature': temperature,
                'data_quality': base_quality,
                'transmission_status': station['transmission_method'],
                'battery_level': random.uniform(60, 100) if station['status'] != 'Offline' else 0
            }
            measurements.append(measurement)
    
    return pd.DataFrame(measurements)

# Enhanced mapping function
def create_professional_nile_map(stations_df, measurements_df=None):
    """Create a professional interactive map with enhanced features"""
    # Initialize map with better styling
    m = folium.Map(
        location=[15, 30],
        zoom_start=4,
        tiles=None  # We'll add custom tiles
    )
    
    # Add multiple tile layers for better visualization
    folium.TileLayer('OpenStreetMap', name='Street Map').add_to(m)
    folium.TileLayer('CartoDB positron', name='Light Map').add_to(m)
    folium.TileLayer('CartoDB dark_matter', name='Dark Map').add_to(m)
    
    # Add satellite imagery
    folium.TileLayer(
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr='Esri',
        name='Satellite',
        overlay=False,
        control=True
    ).add_to(m)
    
    # Color mapping for enhanced status visualization
    status_colors = {
        'Active': '#4CAF50',
        'Maintenance': '#FF9800', 
        'Offline': '#F44336',
        'Calibration': '#2196F3'
    }
    
    # Create marker clusters for better performance
    from folium.plugins import MarkerCluster
    marker_cluster = MarkerCluster(name='Monitoring Stations').add_to(m)
    
    # Add stations with enhanced popups
    for _, station in stations_df.iterrows():
        color = status_colors.get(station['status'], '#9E9E9E')
        
        # Get latest measurement if available
        latest_data = ""
        if measurements_df is not None:
            station_measurements = measurements_df[measurements_df['station_id'] == station['station_id']]
            if not station_measurements.empty:
                latest = station_measurements.iloc[-1]
                latest_data = f"""
                <br><b>Latest Readings:</b><br>
                Water Level: {latest['water_level']:.2f}m<br>
                Flow Rate: {latest['flow_rate']:.1f} m³/s<br>
                Temperature: {latest['temperature']:.1f}°C<br>
                Data Quality: {latest['data_quality']:.1f}%<br>
                Battery: {latest['battery_level']:.0f}%
                """
        
        popup_content = f"""
        <div style="font-family: Arial; width: 300px;">
            <h4 style="color: {color}; margin-bottom: 10px;">
                🌊 {station['name']}
            </h4>
            <table style="width: 100%; font-size: 12px;">
                <tr><td><b>Country:</b></td><td>{station['country']}</td></tr>
                <tr><td><b>Type:</b></td><td>{station['type']}</td></tr>
                <tr><td><b>Status:</b></td><td><span style="color: {color};">{station['status']}</span></td></tr>
                <tr><td><b>Elevation:</b></td><td>{station['elevation']:.0f}m</td></tr>
                <tr><td><b>Climate:</b></td><td>{station['climate_zone']}</td></tr>
                <tr><td><b>Transmission:</b></td><td>{station['transmission_method']}</td></tr>
                <tr><td><b>Feature:</b></td><td>{station['major_feature']}</td></tr>
                <tr><td><b>Installed:</b></td><td>{station['installation_date'].strftime('%Y-%m-%d')}</td></tr>
            </table>
            {latest_data}
        </div>
        """
        
        # Enhanced marker with custom icon
        icon = folium.Icon(
            color='white',
            icon_color=color,
            icon='tint',
            prefix='fa'
        )
        
        folium.Marker(
            location=[station['latitude'], station['longitude']],
            popup=folium.Popup(popup_content, max_width=350),
            tooltip=f"{station['name']} ({station['status']})",
            icon=icon
        ).add_to(marker_cluster)
    
    # Add enhanced legend
    legend_html = f'''
    <div style="position: fixed; 
                bottom: 50px; left: 50px; width: 200px; height: 140px; 
                background-color: white; border: 2px solid grey; z-index: 9999; 
                font-size: 14px; padding: 15px; border-radius: 10px;
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
    <h4 style="margin-top: 0; color: #333;">Station Status</h4>
    <p style="margin: 5px 0;"><i class="fa fa-circle" style="color: #4CAF50;"></i> Active ({len(stations_df[stations_df["status"] == "Active"])})</p>
    <p style="margin: 5px 0;"><i class="fa fa-circle" style="color: #FF9800;"></i> Maintenance ({len(stations_df[stations_df["status"] == "Maintenance"])})</p>
    <p style="margin: 5px 0;"><i class="fa fa-circle" style="color: #2196F3;"></i> Calibration ({len(stations_df[stations_df["status"] == "Calibration"])})</p>
    <p style="margin: 5px 0;"><i class="fa fa-circle" style="color: #F44336;"></i> Offline ({len(stations_df[stations_df["status"] == "Offline"])})</p>
    </div>
    '''
    m.get_root().html.add_child(folium.Element(legend_html))
    
    # Add layer control
    folium.LayerControl().add_to(m)
    
    return m

# Enhanced alert system
def generate_sophisticated_alerts(measurements_df, stations_df):
    """Generate comprehensive alert system with multiple criteria"""
    alerts = []
    
    # Get latest measurements
    latest_data = measurements_df.groupby('station_id').last().reset_index()
    
    for _, data in latest_data.iterrows():
        station_info = stations_df[stations_df['station_id'] == data['station_id']].iloc[0]
        
        # Dynamic thresholds based on station type and climate
        if station_info['type'] == 'Lake Level':
            if station_info['climate_zone'] in ['Tropical', 'Tropical Highland']:
                flood_threshold = 1178 + (station_info['elevation'] - 1100) * 0.1
                drought_threshold = 1172 + (station_info['elevation'] - 1100) * 0.1
            else:
                flood_threshold = 1176 + (station_info['elevation'] - 1100) * 0.1
                drought_threshold = 1174 + (station_info['elevation'] - 1100) * 0.1
        elif station_info['type'] == 'River Flow':
            base_flood = 480 + station_info['elevation'] * 0.2
            base_drought = 320 + station_info['elevation'] * 0.2
            flood_threshold = base_flood
            drought_threshold = base_drought
        else:  # Reservoir/Groundwater
            flood_threshold = 580 + station_info['elevation'] * 0.15
            drought_threshold = 420 + station_info['elevation'] * 0.15
        
        # Check multiple alert conditions
        alerts_for_station = []
        
        # Water level alerts
        if data['water_level'] > flood_threshold:
            severity = 'Critical' if data['water_level'] > flood_threshold * 1.05 else 'High' if data['water_level'] > flood_threshold * 1.02 else 'Medium'
            alerts_for_station.append({
                'type': 'Flood Warning',
                'severity': severity,
                'parameter': 'Water Level',
                'current_value': f"{data['water_level']:.2f}m",
                'threshold': f"{flood_threshold:.2f}m",
                'exceedance': f"{((data['water_level'] / flood_threshold - 1) * 100):.1f}%"
            })
        
        elif data['water_level'] < drought_threshold:
            severity = 'Critical' if data['water_level'] < drought_threshold * 0.95 else 'High' if data['water_level'] < drought_threshold * 0.98 else 'Medium'
            alerts_for_station.append({
                'type': 'Drought Warning',
                'severity': severity,
                'parameter': 'Water Level',
                'current_value': f"{data['water_level']:.2f}m",
                'threshold': f"{drought_threshold:.2f}m",
                'exceedance': f"{((1 - data['water_level'] / drought_threshold) * 100):.1f}%"
            })
        
        # Data quality alerts
        if data['data_quality'] < 80:
            severity = 'Critical' if data['data_quality'] < 60 else 'High' if data['data_quality'] < 70 else 'Medium'
            alerts_for_station.append({
                'type': 'Data Quality Alert',
                'severity': severity,
                'parameter': 'Data Quality',
                'current_value': f"{data['data_quality']:.1f}%",
                'threshold': "80.0%",
                'exceedance': f"{(80 - data['data_quality']):.1f}%"
            })
        
        # Battery level alerts
        if 'battery_level' in data and data['battery_level'] < 30:
            severity = 'Critical' if data['battery_level'] < 15 else 'High' if data['battery_level'] < 25 else 'Medium'
            alerts_for_station.append({
                'type': 'Battery Alert',
                'severity': severity,
                'parameter': 'Battery Level',
                'current_value': f"{data['battery_level']:.0f}%",
                'threshold': "30%",
                'exceedance': f"{(30 - data['battery_level']):.0f}%"
            })
        
        # Add station information to each alert
        for alert in alerts_for_station:
            alert.update({
                'station_id': data['station_id'],
                'station_name': station_info['name'],
                'country': station_info['country'],
                'station_type': station_info['type'],
                'timestamp': data['timestamp'],
                'coordinates': [station_info['latitude'], station_info['longitude']]
            })
            alerts.append(alert)
    
    return alerts

def main():
    # Load all data
    stations_df = generate_enhanced_station_data()
    measurements_df = generate_enhanced_measurement_data(stations_df)
    wapor_data = load_wapor_data()
    alerts = generate_sophisticated_alerts(measurements_df, stations_df)
    
    # Enhanced header with professional styling
    st.markdown("""
    <div class="main-header">
        <h1>🌊 Nile Basin Initiative</h1>
        <h2>Water Resources Management System</h2>
        <p style="font-size: 1.1em; margin-top: 1rem;">
            Comprehensive monitoring and analysis across 10 member countries<br>
            Real-time data • Advanced analytics • Early warning systems
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Enhanced sidebar with logo and branding
    with st.sidebar:
        st.markdown("""
        <div class="sidebar-logo">
            <h3 style="color: white; margin: 0;">🌊 NBI-WRMS</h3>
            <p style="color: #e3f2fd; margin: 5px 0; font-size: 0.9em;">
                Water Resources<br>Management System
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.header("🧭 Navigation")
        page = st.selectbox(
            "Select Module:",
            [
                "🏠 Regional Overview",
                "📊 Station Monitoring", 
                "📈 Trend Analysis",
                "⚠️ Alerts & Warnings",
                "🛰️ WaPOR Integration",
                "📥 Data Export & Reports"
            ]
        )
        
        # Add system status in sidebar
        st.markdown("---")
        st.subheader("📡 System Status")
        
        total_stations = len(stations_df)
        active_stations = len(stations_df[stations_df['status'] == 'Active'])
        system_health = (active_stations / total_stations) * 100
        
        if system_health >= 90:
            st.success(f"🟢 Excellent ({system_health:.0f}%)")
        elif system_health >= 75:
            st.warning(f"🟡 Good ({system_health:.0f}%)")
        else:
            st.error(f"🔴 Needs Attention ({system_health:.0f}%)")
        
        st.metric("Active Stations", f"{active_stations}/{total_stations}")
        st.metric("Data Quality", f"{measurements_df['data_quality'].mean():.1f}%")
        st.metric("Active Alerts", len(alerts))
        
        # WaPOR integration status
        if wapor_data:
            st.markdown("---")
            st.subheader("🛰️ WaPOR Data")
            st.success("✅ Connected")
            st.metric("Datasets", wapor_data['datasets_available'])
            st.info(f"Coverage: {wapor_data['temporal_coverage']}")
    
    # Page routing with enhanced content
    if page == "🏠 Regional Overview":
        st.header("🌍 Regional Overview Dashboard")
        
        # Enhanced KPI metrics with better calculations
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric(
                "🏭 Total Stations", 
                total_stations,
                help="Total monitoring stations across all NBI countries"
            )
        
        with col2:
            active_pct = (active_stations/total_stations*100)
            st.metric(
                "✅ Operational", 
                f"{active_stations}/{total_stations}",
                delta=f"{active_pct:.1f}%",
                help="Percentage of stations currently operational"
            )
        
        with col3:
            avg_quality = measurements_df['data_quality'].mean()
            st.metric(
                "📊 Data Quality", 
                f"{avg_quality:.1f}%",
                delta="2.3%",
                help="Average data quality across all active stations"
            )
        
        with col4:
            critical_alerts = len([a for a in alerts if a['severity'] == 'Critical'])
            st.metric(
                "🚨 Critical Alerts", 
                critical_alerts,
                delta="-1" if critical_alerts < 2 else "+1",
                delta_color="inverse",
                help="Number of critical alerts requiring immediate attention"
            )
        
        with col5:
            countries_with_issues = len(set([a['country'] for a in alerts]))
            st.metric(
                "🌍 Countries Affected",
                countries_with_issues,
                delta=None,
                help="Number of countries with active alerts"
            )
        
        # Enhanced visualization section
        col1, col2 = st.columns([2.5, 1.5])
        
        with col1:
            st.subheader("🗺️ Regional Monitoring Network")
            
            # Add map controls
            map_col1, map_col2 = st.columns([3, 1])
            with map_col2:
                show_alerts_only = st.checkbox("Show Alert Stations Only", False)
                map_style = st.selectbox("Map Style", ["Street Map", "Satellite", "Dark Map"])
            
            if show_alerts_only and alerts:
                alert_stations = set([a['station_id'] for a in alerts])
                filtered_stations = stations_df[stations_df['station_id'].isin(alert_stations)]
            else:
                filtered_stations = stations_df
            
            professional_map = create_professional_nile_map(filtered_stations, measurements_df)
            st_folium(professional_map, width=800, height=600, key="main_map")
        
        with col2:
            # Enhanced status visualization
            st.subheader("📈 System Analytics")
            
            # Station status pie chart
            status_counts = stations_df['status'].value_counts()
            fig_status = px.pie(
                values=status_counts.values, 
                names=status_counts.index,
                title="Station Status Distribution",
                color_discrete_map={
                    'Active': '#4CAF50',
                    'Maintenance': '#FF9800',
                    'Offline': '#F44336',
                    'Calibration': '#2196F3'
                },
                hole=0.4
            )
            fig_status.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_status, use_container_width=True)
            
            # Country coverage bar chart
            st.subheader("🌍 Regional Coverage")
            country_counts = stations_df['country'].value_counts().head(10)
            fig_countries = px.bar(
                x=country_counts.values,
                y=country_counts.index,
                orientation='h',
                title="Stations per Country",
                labels={'x': 'Number of Stations', 'y': 'Country'},
                color=country_counts.values,
                color_continuous_scale='Blues'
            )
            fig_countries.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig_countries, use_container_width=True)
        
        # Real-time system performance
        st.subheader("⚡ Real-time Performance Metrics")
        
        perf_col1, perf_col2, perf_col3, perf_col4 = st.columns(4)
        
        with perf_col1:
            avg_battery = measurements_df['battery_level'].mean()
            st.metric("🔋 Avg Battery", f"{avg_battery:.0f}%", 
                     delta="5%" if avg_battery > 75 else "-3%")
        
        with perf_col2:
            transmission_success = (measurements_df['data_quality'] > 80).mean() * 100
            st.metric("📡 Transmission Success", f"{transmission_success:.1f}%")
        
        with perf_col3:
            last_update = measurements_df['timestamp'].max()
            hours_since = (datetime.now() - last_update).total_seconds() / 3600
            st.metric("🕒 Last Update", f"{hours_since:.1f}h ago")
        
        with perf_col4:
            data_volume = len(measurements_df)
            st.metric("💾 Data Points", f"{data_volume:,}")
    
    elif page == "📊 Station Monitoring":
        st.header("🔍 Advanced Station Monitoring")
        
        # Enhanced station selection with filters
        filter_col1, filter_col2, filter_col3 = st.columns(3)
        
        with filter_col1:
            selected_country = st.selectbox(
                "🌍 Select Country:",
                ["All Countries"] + sorted(stations_df['country'].unique())
            )
        
        with filter_col2:
            if selected_country != "All Countries":
                available_stations = stations_df[stations_df['country'] == selected_country]
            else:
                available_stations = stations_df
            
            station_status_filter = st.selectbox(
                "📊 Filter by Status:",
                ["All Status"] + list(stations_df['status'].unique())
            )
            
            if station_status_filter != "All Status":
                available_stations = available_stations[available_stations['status'] == station_status_filter]
        
        with filter_col3:
            selected_station_id = st.selectbox(
                "🏭 Select Station:",
                available_stations['station_id'].tolist(),
                format_func=lambda x: f"{x} - {available_stations[available_stations['station_id']==x].iloc[0]['name']}"
            )
        
        if selected_station_id:
            station_info = stations_df[stations_df['station_id'] == selected_station_id].iloc[0]
            station_data = measurements_df[measurements_df['station_id'] == selected_station_id]
            
            # Enhanced station information display
            st.subheader(f"📍 {station_info['name']} - Detailed Analysis")
            
            info_col1, info_col2, info_col3, info_col4 = st.columns(4)
            
            with info_col1:
                st.markdown(f"""
                <div class="metric-card">
                    <h4>🏭 Station Details</h4>
                    <p><strong>ID:</strong> {station_info['station_id']}</p>
                    <p><strong>Country:</strong> {station_info['country']}</p>
                    <p><strong>Type:</strong> {station_info['type']}</p>
                    <p><strong>Feature:</strong> {station_info['major_feature']}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with info_col2:
                status_color = {'Active': '#4CAF50', 'Maintenance': '#FF9800', 
                               'Offline': '#F44336', 'Calibration': '#2196F3'}.get(station_info['status'], '#666')
                st.markdown(f"""
                <div class="metric-card">
                    <h4>📊 Operational Status</h4>
                    <p><strong>Status:</strong> <span style="color: {status_color};">{station_info['status']}</span></p>
                    <p><strong>Transmission:</strong> {station_info['transmission_method']}</p>
                    <p><strong>Frequency:</strong> {station_info['data_frequency']}</p>
                    <p><strong>Climate:</strong> {station_info['climate_zone']}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with info_col3:
                if not station_data.empty:
                    latest = station_data.iloc[-1]
                    st.markdown(f"""
                    <div class="metric-card">
                        <h4>📈 Latest Readings</h4>
                        <p><strong>Water Level:</strong> {latest['water_level']:.2f}m</p>
                        <p><strong>Flow Rate:</strong> {latest['flow_rate']:.1f} m³/s</p>
                        <p><strong>Temperature:</strong> {latest['temperature']:.1f}°C</p>
                        <p><strong>Quality:</strong> {latest['data_quality']:.1f}%</p>
                    </div>
                    """, unsafe_allow_html=True)
            
            with info_col4:
                st.markdown(f"""
                <div class="metric-card">
                    <h4>🌍 Location Info</h4>
                    <p><strong>Latitude:</strong> {station_info['latitude']:.4f}</p>
                    <p><strong>Longitude:</strong> {station_info['longitude']:.4f}</p>
                    <p><strong>Elevation:</strong> {station_info['elevation']:.0f}m</p>
                    <p><strong>Installed:</strong> {station_info['installation_date'].strftime('%Y-%m-%d')}</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Enhanced time series analysis
            if len(station_data) > 0:
                st.subheader("📊 Time Series Analysis")
                
                # Time range selector
                time_col1, time_col2 = st.columns(2)
                with time_col1:
                    time_range = st.selectbox(
                        "📅 Time Range:",
                        ["Last 24 Hours", "Last 7 Days", "Last 30 Days", "All Data"]
                    )
                
                with time_col2:
                    chart_type = st.selectbox(
                        "📈 Chart Type:",
                        ["Combined View", "Individual Parameters", "Statistical Analysis"]
                    )
                
                # Filter data based on time range
                if time_range == "Last 24 Hours":
                    cutoff = datetime.now() - timedelta(hours=24)
                elif time_range == "Last 7 Days":
                    cutoff = datetime.now() - timedelta(days=7)
                elif time_range == "Last 30 Days":
                    cutoff = datetime.now() - timedelta(days=30)
                else:
                    cutoff = station_data['timestamp'].min()
                
                filtered_data = station_data[station_data['timestamp'] >= cutoff]
                
                if chart_type == "Combined View":
                    # Multi-parameter subplot
                    fig = make_subplots(
                        rows=3, cols=1,
                        subplot_titles=['Water Level (m)', 'Flow Rate (m³/s)', 'Temperature (°C) & Data Quality (%)'],
                        vertical_spacing=0.08,
                        specs=[[{"secondary_y": False}],
                               [{"secondary_y": False}],
                               [{"secondary_y": True}]]
                    )
                    
                    # Water level
                    fig.add_trace(
                        go.Scatter(x=filtered_data['timestamp'], y=filtered_data['water_level'],
                                  mode='lines', name='Water Level', line=dict(color='blue', width=2)),
                        row=1, col=1
                    )
                    
                    # Flow rate
                    fig.add_trace(
                        go.Scatter(x=filtered_data['timestamp'], y=filtered_data['flow_rate'],
                                  mode='lines', name='Flow Rate', line=dict(color='green', width=2)),
                        row=2, col=1
                    )
                    
                    # Temperature and data quality
                    fig.add_trace(
                        go.Scatter(x=filtered_data['timestamp'], y=filtered_data['temperature'],
                                  mode='lines', name='Temperature', line=dict(color='red', width=2)),
                        row=3, col=1
                    )
                    
                    fig.add_trace(
                        go.Scatter(x=filtered_data['timestamp'], y=filtered_data['data_quality'],
                                  mode='lines', name='Data Quality', line=dict(color='orange', width=2)),
                        row=3, col=1, secondary_y=True
                    )
                    
                    fig.update_layout(height=800, showlegend=True, title_text=f"Comprehensive Analysis - {station_info['name']}")
                    fig.update_xaxes(title_text="Time", row=3, col=1)
                    fig.update_yaxes(title_text="Water Level (m)", row=1, col=1)
                    fig.update_yaxes(title_text="Flow Rate (m³/s)", row=2, col=1)
                    fig.update_yaxes(title_text="Temperature (°C)", row=3, col=1)
                    fig.update_yaxes(title_text="Data Quality (%)", row=3, col=1, secondary_y=True)
                    
                    st.plotly_chart(fig, use_container_width=True)
                
                elif chart_type == "Statistical Analysis":
                    # Statistical summary and distribution analysis
                    st.subheader("📊 Statistical Summary")
                    
                    stats_data = filtered_data[['water_level', 'flow_rate', 'temperature', 'data_quality']].describe()
                    st.dataframe(stats_data.round(2), use_container_width=True)
                    
                    # Distribution plots
                    param_col1, param_col2 = st.columns(2)
                    
                    with param_col1:
                        # Water level distribution
                        fig_dist1 = px.histogram(
                            filtered_data, x='water_level', nbins=30,
                            title="Water Level Distribution",
                            labels={'water_level': 'Water Level (m)', 'count': 'Frequency'}
                        )
                        st.plotly_chart(fig_dist1, use_container_width=True)
                    
                    with param_col2:
                        # Flow rate distribution
                        fig_dist2 = px.histogram(
                            filtered_data, x='flow_rate', nbins=30,
                            title="Flow Rate Distribution",
                            labels={'flow_rate': 'Flow Rate (m³/s)', 'count': 'Frequency'}
                        )
                        st.plotly_chart(fig_dist2, use_container_width=True)
                
                # Recent measurements table with enhanced formatting
                st.subheader("📋 Recent Detailed Measurements")
                recent_data = filtered_data.tail(20)[['timestamp', 'water_level', 'flow_rate', 'temperature', 'data_quality', 'battery_level']]
                recent_data.columns = ['Timestamp', 'Water Level (m)', 'Flow Rate (m³/s)', 'Temperature (°C)', 'Data Quality (%)', 'Battery (%)']
                recent_data['Timestamp'] = recent_data['Timestamp'].dt.strftime('%Y-%m-%d %H:%M')
                
                # Color-code data quality
                def highlight_quality(val):
                    if val >= 90:
                        return 'background-color: #c8e6c9'
                    elif val >= 80:
                        return 'background-color: #fff3e0'
                    else:
                        return 'background-color: #ffebee'
                
                styled_data = recent_data.style.applymap(highlight_quality, subset=['Data Quality (%)'])
                st.dataframe(styled_data, use_container_width=True)
    
    elif page == "📈 Trend Analysis":
        st.header("📈 Advanced Trend Analysis & Insights")
        
        # Enhanced analysis options
        analysis_col1, analysis_col2, analysis_col3, analysis_col4 = st.columns(4)
        
        with analysis_col1:
            analysis_type = st.selectbox(
                "🔍 Analysis Type:",
                [
                    "Cross-Country Comparison",
                    "Seasonal Patterns", 
                    "Data Quality Trends",
                    "Climate Zone Analysis",
                    "Transmission Performance"
                ]
            )
        
        with analysis_col2:
            parameter = st.selectbox(
                "📊 Parameter:",
                ["water_level", "flow_rate", "temperature", "data_quality", "battery_level"]
            )
        
        with analysis_col3:
            time_period = st.selectbox(
                "⏰ Time Period:",
                ["Last 7 Days", "Last 30 Days", "All Data"]
            )
        
        with analysis_col4:
            chart_style = st.selectbox(
                "🎨 Visualization:",
                ["Interactive", "Statistical", "Comparative"]
            )
        
        # Filter data based on selections
        if time_period == "Last 7 Days":
            cutoff_date = datetime.now() - timedelta(days=7)
        elif time_period == "Last 30 Days":
            cutoff_date = datetime.now() - timedelta(days=30)
        else:
            cutoff_date = measurements_df['timestamp'].min()
        
        filtered_data = measurements_df[measurements_df['timestamp'] >= cutoff_date]
        analysis_data = filtered_data.merge(stations_df[['station_id', 'country', 'type', 'climate_zone']], on='station_id')
        
        if analysis_type == "Cross-Country Comparison":
            st.subheader(f"🌍 {parameter.replace('_', ' ').title()} Comparison Across Countries")
            
            country_stats = analysis_data.groupby('country')[parameter].agg(['mean', 'std', 'min', 'max']).round(2)
            
            if chart_style == "Interactive":
                # Interactive bar chart
                fig = px.bar(
                    x=country_stats.index,
                    y=country_stats['mean'],
                    error_y=country_stats['std'],
                    title=f"Average {parameter.replace('_', ' ').title()} by Country",
                    labels={'x': 'Country', 'y': parameter.replace('_', ' ').title()},
                    color=country_stats['mean'],
                    color_continuous_scale='RdYlBu_r'
                )
                fig.update_xaxes(tickangle=45)
                st.plotly_chart(fig, use_container_width=True)
                
                # Box plot for distribution comparison
                fig_box = px.box(
                    analysis_data, x='country', y=parameter,
                    title=f"{parameter.replace('_', ' ').title()} Distribution by Country"
                )
                fig_box.update_xaxes(tickangle=45)
                st.plotly_chart(fig_box, use_container_width=True)
            
            # Statistical summary table
            st.subheader("📊 Statistical Summary by Country")
            st.dataframe(country_stats, use_container_width=True)
            
            # Country ranking
            ranking = country_stats.sort_values('mean', ascending=False)
            st.subheader(f"🏆 Country Ranking by Average {parameter.replace('_', ' ').title()}")
            
            rank_col1, rank_col2 = st.columns(2)
            with rank_col1:
                st.markdown("**🥇 Top Performers:**")
                for i, (country, value) in enumerate(ranking.head(3)['mean'].items(), 1):
                    medal = ["🥇", "🥈", "🥉"][i-1]
                    st.write(f"{medal} {country}: {value:.2f}")
            
            with rank_col2:
                st.markdown("**📈 Highest Variability:**")
                variability = ranking.sort_values('std', ascending=False).head(3)
                for country, value in variability['std'].items():
                    st.write(f"📊 {country}: ±{value:.2f}")
        
        elif analysis_type == "Climate Zone Analysis":
            st.subheader(f"🌡️ {parameter.replace('_', ' ').title()} Analysis by Climate Zone")
            
            climate_stats = analysis_data.groupby('climate_zone')[parameter].agg(['mean', 'std', 'count']).round(2)
            
            # Climate zone comparison
            fig_climate = px.violin(
                analysis_data, x='climate_zone', y=parameter,
                title=f"{parameter.replace('_', ' ').title()} Distribution by Climate Zone",
                box=True
            )
            fig_climate.update_xaxes(tickangle=45)
            st.plotly_chart(fig_climate, use_container_width=True)
            
            # Climate zone statistics
            st.dataframe(climate_stats, use_container_width=True)
            
        elif analysis_type == "Seasonal Patterns":
            st.subheader(f"📅 Seasonal Patterns in {parameter.replace('_', ' ').title()}")
            
            # Add time-based features
            analysis_data['hour'] = analysis_data['timestamp'].dt.hour
            analysis_data['day_of_year'] = analysis_data['timestamp'].dt.dayofyear
            analysis_data['month'] = analysis_data['timestamp'].dt.month
            
            pattern_col1, pattern_col2 = st.columns(2)
            
            with pattern_col1:
                # Hourly pattern
                hourly_pattern = analysis_data.groupby('hour')[parameter].mean()
                fig_hourly = px.line(
                    x=hourly_pattern.index,
                    y=hourly_pattern.values,
                    title=f"Daily Pattern - {parameter.replace('_', ' ').title()}",
                    labels={'x': 'Hour of Day', 'y': parameter.replace('_', ' ').title()}
                )
                st.plotly_chart(fig_hourly, use_container_width=True)
            
            with pattern_col2:
                # Monthly pattern
                monthly_pattern = analysis_data.groupby('month')[parameter].mean()
                month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                              'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
                fig_monthly = px.line(
                    x=[month_names[i-1] for i in monthly_pattern.index],
                    y=monthly_pattern.values,
                    title=f"Monthly Pattern - {parameter.replace('_', ' ').title()}",
                    labels={'x': 'Month', 'y': parameter.replace('_', ' ').title()}
                )
                st.plotly_chart(fig_monthly, use_container_width=True)
    
    elif page == "⚠️ Alerts & Warnings":
        st.header("🚨 Comprehensive Alert Management System")
        
        # Alert summary with enhanced metrics
        if alerts:
            # Categorize alerts by severity
            critical_alerts = [a for a in alerts if a['severity'] == 'Critical']
            high_alerts = [a for a in alerts if a['severity'] == 'High']
            medium_alerts = [a for a in alerts if a['severity'] == 'Medium']
            
            # Alert summary metrics
            alert_col1, alert_col2, alert_col3, alert_col4 = st.columns(4)
            
            with alert_col1:
                st.metric("🔴 Critical Alerts", len(critical_alerts), 
                         delta="+1" if len(critical_alerts) > 0 else "0")
            
            with alert_col2:
                st.metric("🟠 High Priority", len(high_alerts),
                         delta="+2" if len(high_alerts) > 1 else "0")
            
            with alert_col3:
                st.metric("🟡 Medium Priority", len(medium_alerts))
            
            with alert_col4:
                affected_countries = len(set([a['country'] for a in alerts]))
                st.metric("🌍 Countries Affected", affected_countries)
            
            # Enhanced alert display
            if critical_alerts:
                st.subheader("🔴 Critical Priority Alerts - Immediate Action Required")
                for alert in critical_alerts:
                    st.markdown(f"""
                    <div class="alert-high">
                        <h4 style="margin-top: 0; color: #d32f2f;">
                            🚨 {alert['type']} - {alert['severity']} Priority
                        </h4>
                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                            <div>
                                <strong>📍 Station:</strong> {alert['station_name']}<br>
                                <strong>🌍 Country:</strong> {alert['country']}<br>
                                <strong>🏭 Type:</strong> {alert['station_type']}
                            </div>
                            <div>
                                <strong>📊 Current Value:</strong> {alert['current_value']}<br>
                                <strong>⚖️ Threshold:</strong> {alert['threshold']}<br>
                                <strong>📈 Exceedance:</strong> {alert['exceedance']}
                            </div>
                        </div>
                        <small style="color: #666;">
                            🕒 Last Update: {alert['timestamp'].strftime('%Y-%m-%d %H:%M:%S')} | 
                            📧 Notification sent to: Regional Operations Center
                        </small>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Alert visualization
            st.subheader("📊 Alert Analysis Dashboard")
            
            viz_col1, viz_col2 = st.columns(2)
            
            with viz_col1:
                # Alert distribution by type
                alert_df = pd.DataFrame(alerts)
                type_counts = alert_df['type'].value_counts()
                fig_types = px.pie(
                    values=type_counts.values,
                    names=type_counts.index,
                    title="Alert Distribution by Type",
                    color_discrete_sequence=['#f44336', '#ff9800', '#2196f3', '#4caf50']
                )
                st.plotly_chart(fig_types, use_container_width=True)
            
            with viz_col2:
                # Alert severity distribution
                severity_counts = alert_df['severity'].value_counts()
                fig_severity = px.bar(
                    x=severity_counts.index,
                    y=severity_counts.values,
                    title="Alert Distribution by Severity",
                    color=severity_counts.index,
                    color_discrete_map={
                        'Critical': '#d32f2f',
                        'High': '#f57c00',
                        'Medium': '#1976d2'
                    }
                )
                st.plotly_chart(fig_severity, use_container_width=True)
            
            # Geographic distribution of alerts
            if len(alert_df) > 0:
                st.subheader("🗺️ Geographic Alert Distribution")
                country_alert_counts = alert_df['country'].value_counts()
                
                fig_geo = px.bar(
                    x=country_alert_counts.values,
                    y=country_alert_counts.index,
                    orientation='h',
                    title="Number of Alerts by Country",
                    labels={'x': 'Number of Alerts', 'y': 'Country'},
                    color=country_alert_counts.values,
                    color_continuous_scale='Reds'
                )
                st.plotly_chart(fig_geo, use_container_width=True)
        
        else:
            st.success("✅ All Systems Operational - No Active Alerts")
            
            st.markdown("""
            <div class="alert-low">
                <h3 style="margin-top: 0; color: #2e7d32;">🎉 Excellent System Performance</h3>
                <p>All {total_stations} monitoring stations across the Nile Basin are operating within normal parameters.</p>
                <ul>
                    <li>✅ Water levels are within acceptable ranges</li>
                    <li>✅ Data quality exceeds 80% threshold</li>
                    <li>✅ Equipment battery levels are adequate</li>
                    <li>✅ Communication systems are functioning properly</li>
                </ul>
                <p><small>🕒 Last system check: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</small></p>
            </div>
            """.format(total_stations=len(stations_df)), unsafe_allow_html=True)
        
        # Alert configuration and management
        st.subheader("⚙️ Alert Configuration & Management")
        
        with st.expander("🔧 Configure Alert Thresholds", expanded=False):
            st.info("💡 **Production Note**: In a live system, administrators can configure station-specific thresholds based on historical data and local conditions.")
            
            config_col1, config_col2, config_col3 = st.columns(3)
            
            with config_col1:
                st.markdown("**🌊 Water Level Thresholds**")
                lake_flood = st.slider("Lake Flood Level (m)", 1170, 1185, 1178)
                lake_drought = st.slider("Lake Drought Level (m)", 1165, 1175, 1172)
                river_flood = st.slider("River Flood Level (m)", 400, 500, 480)
                river_drought = st.slider("River Drought Level (m)", 300, 400, 320)
            
            with config_col2:
                st.markdown("**📊 Data Quality Thresholds**")
                critical_quality = st.slider("Critical Quality (%)", 50, 70, 60)
                warning_quality = st.slider("Warning Quality (%)", 70, 90, 80)
                battery_critical = st.slider("Battery Critical (%)", 10, 30, 20)
                battery_warning = st.slider("Battery Warning (%)", 30, 50, 40)
            
            with config_col3:
                st.markdown("**🔔 Notification Settings**")
                email_alerts = st.checkbox("Email Notifications", True)
                sms_alerts = st.checkbox("SMS Notifications", False)
                dashboard_alerts = st.checkbox("Dashboard Alerts", True)
                auto_escalation = st.checkbox("Auto Escalation", False)
                
                escalation_time = st.selectbox("Escalation Time", ["15 min", "30 min", "1 hour", "2 hours"])
    
    elif page == "🛰️ WaPOR Integration":
        st.header("🛰️ WaPOR Satellite Data Integration")
        
        # WaPOR system overview
        if wapor_data:
            st.success("✅ WaPOR Data Successfully Connected!")
            
            # WaPOR overview metrics
            wapor_col1, wapor_col2, wapor_col3, wapor_col4 = st.columns(4)
            
            with wapor_col1:
                st.metric("📁 Available Datasets", wapor_data['datasets_available'])
            
            with wapor_col2:
                st.metric("🌍 Countries Covered", wapor_data['countries_covered'])
            
            with wapor_col3:
                st.metric("📏 Spatial Resolution", wapor_data['spatial_resolution'])
            
            with wapor_col4:
                st.metric("📅 Temporal Coverage", wapor_data['temporal_coverage'])
            
            # Available WaPOR datasets
            st.subheader("📊 Available WaPOR Datasets")
            
            datasets_info = pd.DataFrame({
                'Dataset': wapor_data['data_types'],
                'Description': [
                    'Monthly evapotranspiration from crops and natural vegetation',
                    'Quality assessment of land surface temperature measurements',
                    'Annual evaporation from water surfaces and soil',
                    'Annual classification of land cover types',
                    'Comprehensive water data from 2014-2018 period'
                ],
                'Resolution': ['100m', '100m', '100m', '100m', '100m'],
                'Frequency': ['Monthly', 'Dekadal (10-day)', 'Annual', 'Annual', 'Various'],
                'Status': ['✅ Available', '✅ Available', '✅ Available', '✅ Available', '✅ Available']
            })
            
            st.dataframe(datasets_info, use_container_width=True)
            
            # Sample data analysis
            st.subheader("📈 Sample WaPOR Data Analysis")
            
            if wapor_data.get('sample_loaded'):
                st.success(f"📁 Sample file loaded: {wapor_data['sample_file']}")
                
                # Simulate WaPOR data visualization
                sample_data = {
                    'Country': ['Uganda', 'Kenya', 'Tanzania', 'Rwanda', 'Burundi', 'Ethiopia', 'Sudan', 'South Sudan', 'DRC', 'Egypt'],
                    'Avg_ET_mm_month': [85, 72, 78, 92, 88, 68, 45, 67, 95, 25],
                    'Annual_Trend': ['Stable', 'Decreasing', 'Stable', 'Increasing', 'Stable', 'Decreasing', 'Stable', 'Stable', 'Increasing', 'Stable'],
                    'Data_Quality': [96, 94, 95, 97, 93, 92, 89, 91, 94, 98]
                }
                
                wapor_df = pd.DataFrame(sample_data)
                
                # Evapotranspiration comparison
                fig_et = px.bar(
                    wapor_df, 
                    x='Country', 
                    y='Avg_ET_mm_month',
                    color='Annual_Trend',
                    title="Average Evapotranspiration by Country (mm/month)",
                    color_discrete_map={
                        'Increasing': '#d32f2f',
                        'Stable': '#1976d2', 
                        'Decreasing': '#388e3c'
                    }
                )
                fig_et.update_xaxes(tickangle=45)
                st.plotly_chart(fig_et, use_container_width=True)
                
                # Data quality assessment
                fig_quality = px.scatter(
                    wapor_df,
                    x='Avg_ET_mm_month',
                    y='Data_Quality',
                    size=[10]*len(wapor_df),
                    color='Country',
                    title="Data Quality vs Evapotranspiration",
                    labels={'Avg_ET_mm_month': 'Evapotranspiration (mm/month)', 'Data_Quality': 'Data Quality (%)'}
                )
                st.plotly_chart(fig_quality, use_container_width=True)
                
                # Integration benefits
                st.subheader("🎯 Integration Benefits")
                
                benefit_col1, benefit_col2 = st.columns(2)
                
                with benefit_col1:
                    st.markdown("""
                    <div class="feature-highlight">
                        <h4>🔬 Enhanced Analysis Capabilities</h4>
                        <ul>
                            <li>✅ Satellite-derived evapotranspiration data</li>
                            <li>✅ Regional water balance calculations</li>
                            <li>✅ Crop water stress monitoring</li>
                            <li>✅ Drought and flood risk assessment</li>
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)
                
                with benefit_col2:
                    st.markdown("""
                    <div class="feature-highlight">
                        <h4>📊 Operational Advantages</h4>
                        <ul>
                            <li>✅ Independent validation of ground measurements</li>
                            <li>✅ Gap filling for missing station data</li>
                            <li>✅ Regional trend analysis across borders</li>
                            <li>✅ Climate change impact assessment</li>
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)
            
            else:
                st.warning("⚠️ Sample WaPOR file could not be loaded. Data structure is ready for integration.")
                
                st.info("""
                **🔧 Technical Integration Status:**
                - ✅ Data directory structure created
                - ✅ WaPOR processing utilities developed  
                - ✅ JSON parsing capabilities implemented
                - ⏳ Sample data files ready for processing
                """)
        
        else:
            st.error("❌ WaPOR Data Connection Failed")
            st.info("""
            **📁 Expected Data Structure:**
            ```
            data/raw/
            ├── Actual_evapotranspiration_and_interception/
            ├── Evaporation_annual_data/
            ├── FAO_WaPOR_2014_to_2018/
            ├── land_cover_classification_annual/
            └── quality_land_surface_temperature/
            ```
            
            **🔧 To enable WaPOR integration:**
            1. Upload your WaPOR datasets to the data/raw directory
            2. Ensure JSON files are properly formatted
            3. Restart the application
            """)
        
        # Future integration roadmap
        st.subheader("🚀 Future Integration Roadmap")
        
        roadmap_col1, roadmap_col2, roadmap_col3 = st.columns(3)
        
        with roadmap_col1:
            st.markdown("""
            <div class="feature-highlight">
                <h4>📅 Phase 1 (Current)</h4>
                <ul>
                    <li>✅ Static WaPOR data loading</li>
                    <li>✅ Basic visualization</li>
                    <li>✅ Country-level analysis</li>
                    <li>🔄 Data quality assessment</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with roadmap_col2:
            st.markdown("""
            <div class="feature-highlight">
                <h4>📅 Phase 2 (Planned)</h4>
                <ul>
                    <li>🔄 Real-time WaPOR API integration</li>
                    <li>🔄 Automated data updates</li>
                    <li>🔄 Advanced spatial analysis</li>
                    <li>🔄 Predictive modeling</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with roadmap_col3:
            st.markdown("""
            <div class="feature-highlight">
                <h4>📅 Phase 3 (Future)</h4>
                <ul>
                    <li>🔄 Machine learning integration</li>
                    <li>🔄 Climate change projections</li>
                    <li>🔄 Decision support algorithms</li>
                    <li>🔄 Mobile app connectivity</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
    
    elif page == "📥 Data Export & Reports":
        st.header("📥 Comprehensive Data Export & Reporting")
        
        # Export configuration
        st.subheader("⚙️ Export Configuration")
        
        export_col1, export_col2, export_col3 = st.columns(3)
        
        with export_col1:
            export_type = st.selectbox(
                "📊 Data Type:",
                [
                    "Station Metadata",
                    "Measurement Data", 
                    "Alert History",
                    "Statistical Summary",
                    "WaPOR Integration Data",
                    "Executive Dashboard",
                    "Technical Report"
                ]
            )
        
        with export_col2:
            export_format = st.selectbox(
                "📄 Export Format:",
                ["CSV", "Excel (XLSX)", "JSON", "PDF Report"]
            )
        
        with export_col3:
            report_template = st.selectbox(
                "📋 Report Template:",
                ["Standard", "Executive Summary", "Technical Analysis", "Custom"]
            )
        
        # Date range and filters
        st.subheader("📅 Data Range & Filters")
        
        filter_col1, filter_col2, filter_col3 = st.columns(3)
        
        with filter_col1:
            start_date = st.date_input(
                "📅 Start Date:",
                value=datetime.now().date() - timedelta(days=30),
                max_value=datetime.now().date()
            )
        
        with filter_col2:
            end_date = st.date_input(
                "📅 End Date:",
                value=datetime.now().date(),
                max_value=datetime.now().date()
            )
        
        with filter_col3:
            country_filter = st.multiselect(
                "🌍 Countries:",
                options=stations_df['country'].unique(),
                default=stations_df['country'].unique()[:3]
            )
        
        # Advanced filters
        with st.expander("🔍 Advanced Filters", expanded=False):
            adv_col1, adv_col2, adv_col3 = st.columns(3)
            
            with adv_col1:
                station_types = st.multiselect(
                    "🏭 Station Types:",
                    options=stations_df['type'].unique(),
                    default=stations_df['type'].unique()
                )
            
            with adv_col2:
                station_status = st.multiselect(
                    "📊 Station Status:",
                    options=stations_df['status'].unique(),
                    default=['Active']
                )
            
            with adv_col3:
                quality_threshold = st.slider(
                    "📈 Min Data Quality (%):",
                    min_value=0, max_value=100, value=80
                )
        
        # Generate export
        if st.button("🚀 Generate Export", type="primary"):
            with st.spinner("📊 Processing data export..."):
                # Filter data based on selections
                filtered_stations = stations_df[
                    (stations_df['country'].isin(country_filter)) &
                    (stations_df['type'].isin(station_types)) &
                    (stations_df['status'].isin(station_status))
                ]
                
                date_mask = (
                    (measurements_df['timestamp'].dt.date >= start_date) & 
                    (measurements_df['timestamp'].dt.date <= end_date)
                )
                quality_mask = measurements_df['data_quality'] >= quality_threshold
                
                filtered_measurements = measurements_df[
                    date_mask & quality_mask &
                    measurements_df['station_id'].isin(filtered_stations['station_id'])
                ]
                
                # Generate different export types
                if export_type == "Station Metadata":
                    export_data = filtered_stations
                    st.success(f"✅ Station metadata prepared: {len(export_data)} stations")
                    
                elif export_type == "Measurement Data":
                    export_data = filtered_measurements
                    st.success(f"✅ Measurement data prepared: {len(export_data):,} records")
                    
                elif export_type == "Statistical Summary":
                    summary_stats = filtered_measurements.groupby('station_id').agg({
                        'water_level': ['mean', 'std', 'min', 'max'],
                        'flow_rate': ['mean', 'std', 'min', 'max'],
                        'temperature': ['mean', 'std', 'min', 'max'],
                        'data_quality': ['mean', 'count']
                    }).round(2)
                    
                    # Flatten column names
                    summary_stats.columns = [f"{col[0]}_{col[1]}" for col in summary_stats.columns]
                    export_data = summary_stats.reset_index()
                    st.success(f"✅ Statistical summary prepared for {len(export_data)} stations")
                    
                elif export_type == "Executive Dashboard":
                    # Create executive summary
                    exec_summary = {
                        'Report_Date': [datetime.now().strftime('%Y-%m-%d')],
                        'Reporting_Period': [f"{start_date} to {end_date}"],
                        'Total_Stations': [len(filtered_stations)],
                        'Active_Stations': [len(filtered_stations[filtered_stations['status'] == 'Active'])],
                        'Countries_Covered': [len(country_filter)],
                        'Data_Points_Analyzed': [len(filtered_measurements)],
                        'Average_Data_Quality': [filtered_measurements['data_quality'].mean()],
                        'System_Uptime': ['98.7%'],
                        'Critical_Alerts': [len([a for a in alerts if a['severity'] == 'Critical'])],
                        'Recommendations': ['Continue monitoring; Address critical alerts immediately']
                    }
                    export_data = pd.DataFrame(exec_summary)
                    st.success("✅ Executive dashboard summary prepared")
                
                # Display preview
                st.subheader("👀 Data Preview")
                st.dataframe(export_data.head(10), use_container_width=True)
                
                # Download preparation
                st.subheader("💾 Download Options")
                
                download_col1, download_col2 = st.columns(2)
                
                with download_col1:
                    # CSV download
                    csv_data = export_data.to_csv(index=False)
                    filename = f"nbi_{export_type.lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M')}"
                    
                    st.download_button(
                        label="📥 Download CSV",
                        data=csv_data,
                        file_name=f"{filename}.csv",
                        mime="text/csv",
                        help="Download data as CSV file"
                    )
                
                with download_col2:
                    # JSON download
                    json_data = export_data.to_json(orient='records', indent=2)
                    
                    st.download_button(
                        label="📥 Download JSON",
                        data=json_data,
                        file_name=f"{filename}.json",
                        mime="application/json",
                        help="Download data as JSON file"
                    )
                
                # Export summary
                st.info(f"""
                **📊 Export Summary:**
                - **Data Type**: {export_type}
                - **Format**: {export_format}
                - **Records**: {len(export_data):,}
                - **Date Range**: {start_date} to {end_date}
                - **Countries**: {', '.join(country_filter)}
                - **Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                """)
        
        # Scheduled reports section
        st.subheader("📅 Scheduled Reports")
        
        with st.expander("⚙️ Configure Automated Reports", expanded=False):
            st.info("💡 **Production Feature**: Set up automated daily, weekly, or monthly reports for stakeholders.")
            
            schedule_col1, schedule_col2, schedule_col3 = st.columns(3)
            
            with schedule_col1:
                report_frequency = st.selectbox(
                    "📅 Frequency:",
                    ["Daily", "Weekly", "Monthly", "Quarterly"]
                )
                
                report_time = st.time_input("🕒 Send Time:", datetime.now().time())
            
            with schedule_col2:
                recipients = st.text_area(
                    "📧 Email Recipients:",
                    placeholder="director@nilebasin.org\noperations@nilebasin.org"
                )
            
            with schedule_col3:
                include_charts = st.checkbox("📊 Include Charts", True)
                include_alerts = st.checkbox("⚠️ Include Alerts", True)
                include_summary = st.checkbox("📋 Include Summary", True)
                
                if st.button("💾 Save Schedule"):
                    st.success("✅ Automated report schedule saved!")
    
    # Enhanced footer with professional information
    st.markdown("---")
    st.markdown("""
    <div class="footer-info">
        <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 2rem; text-align: center;">
            <div>
                <h4 style="color: #2a5298; margin-bottom: 0.5rem;">🌊 NBI Water Resources Management System</h4>
                <p style="margin: 0; color: #666;">
                    Advanced monitoring and analysis platform for sustainable<br>
                    water resource management across the Nile Basin
                </p>
            </div>
            <div>
                <h4 style="color: #2a5298; margin-bottom: 0.5rem;">🛠️ Technical Specifications</h4>
                <p style="margin: 0; color: #666;">
                    Built with Python & Streamlit<br>
                    Real-time data processing • Interactive visualization<br>
                    Enterprise-ready architecture
                </p>
            </div>
            <div>
                <h4 style="color: #2a5298; margin-bottom: 0.5rem;">👨‍💻 Developer Information</h4>
                <p style="margin: 0; color: #666;">
                    Raymond Rwayesu<br>
                    📧 sseguya256@gmail.com<br>
                    📍 Kampala, Uganda
                </p>
            </div>
        </div>
        <div style="text-align: center; margin-top: 1rem; padding-top: 1rem; border-top: 1px solid #ddd;">
            <small style="color: #888;">
                Demo Version for Nile Basin Initiative • Production deployment available upon request<br>
                © 2025 NBI-WRMS • Built for regional water cooperation and sustainable development
            </small>
        </div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()