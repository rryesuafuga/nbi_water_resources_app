import folium
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

class NileBasinMapper:
    """Create maps for Nile Basin water resources"""
    
    def __init__(self):
        self.basin_center = [15.0, 30.0]
        self.default_zoom = 5
    
    def create_base_map(self):
        """Create base map of Nile Basin"""
        m = folium.Map(
            location=self.basin_center,
            zoom_start=self.default_zoom,
            tiles='OpenStreetMap'
        )
        
        # Add working tile layers
        folium.TileLayer('OpenStreetMap').add_to(m)
        folium.TileLayer('CartoDB positron').add_to(m)
        folium.TileLayer('CartoDB dark_matter').add_to(m)
        folium.LayerControl().add_to(m)
        
        return m
    
    def add_country_boundaries(self, map_obj):
        """Add NBI country boundaries to map"""
        nbi_countries = {
            'Uganda': [0.3476, 32.5825],
            'Kenya': [-1.2921, 36.8219],
            'Tanzania': [-6.3690, 34.8888],
            'Rwanda': [-1.9441, 29.8739],
            'Burundi': [-3.3731, 29.9189],
            'DR Congo': [-4.0383, 21.7587],
            'Ethiopia': [9.1450, 40.4897],
            'Sudan': [12.8628, 30.2176],
            'South Sudan': [6.8770, 31.3070],
            'Egypt': [26.0975, 31.2357]
        }
        
        for country, coords in nbi_countries.items():
            folium.CircleMarker(
                location=coords,
                radius=10,
                popup=f"<b>{country}</b>",
                color='blue',
                fillColor='lightblue',
                fillOpacity=0.7
            ).add_to(map_obj)
        
        return map_obj
    
    def create_time_series_plot(self, data, title="Water Level Trend"):
        """Create time series plot using Plotly"""
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=data['date'],
            y=data['value'],
            mode='lines+markers',
            name='Water Level',
            line=dict(color='blue', width=2),
            marker=dict(size=6)
        ))
        
        fig.update_layout(
            title=title,
            xaxis_title="Date",
            yaxis_title="Water Level (m)",
            hovermode='x unified',
            template='plotly_white'
        )
        
        return fig
