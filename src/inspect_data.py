import pandas as pd
import os

data_path = 'data/raw/ethiopia_fi_unified_data.xlsx'
ref_path = 'data/raw/reference_codes.xlsx'

print(f"Loading data from {data_path}...")
try:
    xl = pd.ExcelFile(data_path)
    print(f"Sheet names found: {xl.sheet_names}")
    
    # Read both sheets
    if 'data' in xl.sheet_names:
        df_data = pd.read_excel(data_path, sheet_name='data')
    elif 'Data' in xl.sheet_names:
        df_data = pd.read_excel(data_path, sheet_name='Data')
    else:
        df_data = pd.read_excel(data_path, sheet_name=0)
        print("Warning: 'data' sheet not found, reading first sheet.")

    if 'impact_links' in xl.sheet_names:
        df_impact = pd.read_excel(data_path, sheet_name='impact_links')
    elif 'Impact' in xl.sheet_names:
        df_impact = pd.read_excel(data_path, sheet_name='Impact')
    elif len(xl.sheet_names) > 1:
        df_impact = pd.read_excel(data_path, sheet_name=1)
        print("Warning: 'impact_links' sheet not found, reading second sheet.")
    else:
        df_impact = pd.DataFrame() # Empty if not found
    
    print("\n--- INFO: DATA SHEET ---")
    print(df_data.info())
    print("\n--- HEAD: DATA SHEET ---")
    print(df_data.head())
    print("\n--- COLUMNS: DATA SHEET ---")
    print(df_data.columns.tolist())
    
    print("\n--- INFO: IMPACT_LINKS SHEET ---")
    print(df_impact.info())
    print("\n--- HEAD: IMPACT_LINKS SHEET ---")
    print(df_impact.head())

    print("\n--- UNIQUE RECORD TYPES ---")
    print(df_data['record_type'].value_counts())

except Exception as e:
    print(f"Error loading data: {e}")

print(f"\nLoading references from {ref_path}...")
try:
    df_ref = pd.read_excel(ref_path)
    print("\n--- INFO: REFERENCE CODES ---")
    print(df_ref.info())
    print(df_ref.head())
except Exception as e:
    print(f"Error loading references: {e}")
