# NBI Water Resources Management Demo App

A comprehensive water resources monitoring and management system for the Nile Basin Initiative, built with Streamlit and real FAO WaPOR satellite data.

## Features

- **Real-time Monitoring**: Live station data across 10 NBI member countries
- **Satellite Analysis**: Integration with FAO WaPOR evapotranspiration data
- **Interactive Mapping**: Dynamic maps with station status and alerts
- **Statistical Analysis**: Trend analysis and anomaly detection
- **Alert System**: Automated flood/drought warnings

## Data Sources

This demo uses actual FAO WaPOR datasets:
- Actual Evapotranspiration and Interception (Monthly)
- Quality Land Surface Temperature (Dekadal)
- Evaporation (Annual)
- Land Cover Classification (Annual)

## Installation

```bash
# Clone the repository
git clone https://github.com/rryesuafuga/nbi_water_resources_app.git
cd nbi_water_resources_app

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run streamlit_app.py
```

## Project Structure

```
nbi_water_resources_app/
├── streamlit_app.py          # Main application
├── data/
│   ├── raw/                  # Raw WaPOR JSON files
│   └── processed/            # Processed data
├── src/
│   ├── data_processing/      # Data processing utilities
│   └── visualization/        # Visualization functions
├── pages/                    # Additional app pages
└── requirements.txt          # Dependencies
```

## Technical Highlights

- **Framework**: Streamlit for rapid prototyping
- **Data Processing**: Real WaPOR satellite data integration
- **Visualization**: Interactive maps and charts
- **Architecture**: Modular design for scalability
- **Performance**: Efficient caching and data loading

## Demo for NBI

This application demonstrates:
1. Technical capability with real satellite data
2. Understanding of NBI operational needs
3. Scalable architecture for production deployment
4. Regional expertise in East African water management

## Contact

Raymond Rwayesu - sseguya256@gmail.com
GitHub: https://github.com/rryesuafuga/nbi_water_resources_app
