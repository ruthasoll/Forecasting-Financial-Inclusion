import pandas as pd
import os
from typing import Dict, Tuple

def load_data(data_path: str = 'data/raw/ethiopia_fi_unified_data.xlsx') -> Dict[str, pd.DataFrame]:
    """
    Loads the unified data file and splits it into logical components.
    
    Args:
        data_path: Path to the Excel file.
        
    Returns:
        A dictionary containing:
        - 'observations': Time series data
        - 'events': Policy and market events
        - 'targets': Policy targets
        - 'impacts': Impact link definitions
        - 'raw_data': The full raw data sheet
    """
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Data file not found at {data_path}")

    print(f"Loading data from {data_path}...")
    
    # Load Data Sheet
    try:
        df_data = pd.read_excel(data_path, sheet_name='ethiopia_fi_unified_data', engine='openpyxl')
    except ValueError:
        # Fallback if sheet name is different (e.g. 'data')
        df_data = pd.read_excel(data_path, sheet_name=0, engine='openpyxl')

    # Load Impact Sheet
    try:
        df_impact = pd.read_excel(data_path, sheet_name='Impact_sheet', engine='openpyxl')
    except ValueError:
         try:
            df_impact = pd.read_excel(data_path, sheet_name='impact_links', engine='openpyxl')
         except ValueError:
            df_impact = pd.DataFrame() # Return empty if not found

    # Process Data Sheet
    # Ensure dates are datetime
    if 'observation_date' in df_data.columns:
        df_data['observation_date'] = pd.to_datetime(df_data['observation_date'])

    # --- ENRICHMENT STEP ---
    # Load supplementary data if exists
    supp_path = os.path.join(os.path.dirname(data_path), 'supplementary_data.csv')
    if os.path.exists(supp_path):
        print(f"Loading supplementary data from {supp_path}...")
        try:
            df_supp = pd.read_csv(supp_path)
            if 'observation_date' in df_supp.columns:
                df_supp['observation_date'] = pd.to_datetime(df_supp['observation_date'])
            # Align columns (fill missing with NaN)
            df_data = pd.concat([df_data, df_supp], axis=0, ignore_index=True)
        except Exception as e:
            print(f"Warning: Failed to load supplementary data: {e}")
    # -----------------------
    
    # Split by record_type
    observations = df_data[df_data['record_type'] == 'observation'].copy()
    events = df_data[df_data['record_type'] == 'event'].copy()
    targets = df_data[df_data['record_type'] == 'target'].copy()

    # Sort observations by date
    if not observations.empty:
        observations = observations.sort_values('observation_date')

    # Process Impact Sheet
    # (Optional: Add processing if needed)

    return {
        'observations': observations,
        'events': events,
        'targets': targets,
        'impacts': df_impact,
        'raw_data': df_data
    }

if __name__ == "__main__":
    # Test the loader
    try:
        data = load_data()
        print("Data loaded successfully.")
        print(f"Observations: {len(data['observations'])}")
        print(f"Events: {len(data['events'])}")
        print(f"Targets: {len(data['targets'])}")
        print(f"Impacts: {len(data['impacts'])}")
        
        print("\nSample Observations:")
        print(data['observations'][['observation_date', 'indicator', 'value_numeric']].head())
    except Exception as e:
        print(f"Error loading data: {e}")
