import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.loader import load_data

def perform_eda():
    data = load_data()
    obs = data['observations']
    events = data['events']
    
    print("\n--- EDA REPORT ---")
    if obs.empty:
        print("No observations found.")
        return

    print(f"Date Range: {obs['observation_date'].min()} to {obs['observation_date'].max()}")
    print("\nUnique Indicators:")
    print(obs['indicator'].unique())
    
    # Pivot to Time Series format to see density
    ts_data = obs.pivot_table(index='observation_date', columns='indicator', values='value_numeric')
    print("\nTime Series Head:")
    print(ts_data.head())
    
    # Basic Plotting
    try:
        plt.figure(figsize=(12, 6))
        sns.lineplot(data=obs, x='observation_date', y='value_numeric', hue='indicator', style='indicator', markers=True)
        
        # Add events as vertical lines
        for _, event in events.iterrows():
            if pd.notnull(event['observation_date']):
                plt.axvline(x=event['observation_date'], color='r', linestyle='--', alpha=0.5)
                # Ideally label them, but might get crowded
        
        plt.title('Financial Inclusion Indicators Over Time (with Events)')
        plt.xlabel('Date')
        plt.ylabel('Value')
        plt.grid(True)
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
        
        output_dir = 'reports/figures'
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, 'eda_timeseries.png')
        plt.savefig(output_path)
        print(f"\nEDA Plot saved to {output_path}")
    except Exception as e:
        print(f"Error plotting: {e}")

if __name__ == "__main__":
    perform_eda()
