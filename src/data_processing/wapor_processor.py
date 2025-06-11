import json
import pandas as pd
import numpy as np
from pathlib import Path

class WaPORProcessor:
    """Process WaPOR JSON data files"""
    
    def __init__(self, data_dir="data/raw"):
        self.data_dir = Path(data_dir)
    
    def load_json_file(self, filename):
        """Load a single WaPOR JSON file"""
        try:
            with open(self.data_dir / filename, 'r') as f:
                data = json.load(f)
            return data
        except Exception as e:
            print(f"Error loading {filename}: {e}")
            return None
    
    def process_evapotranspiration_data(self):
        """Process evapotranspiration JSON files"""
        et_files = list(self.data_dir.glob("**/WAPOR*AETI*.json"))
        
        processed_data = []
        for file_path in et_files:
            data = self.load_json_file(file_path)
            if data:
                # Extract metadata from filename
                parts = file_path.stem.split('.')
                if len(parts) > 3:
                    year_month = parts[-1]  # e.g., "2014-01"
                    processed_data.append({
                        'date': year_month,
                        'filename': file_path.name,
                        'data': data
                    })
        
        return processed_data
