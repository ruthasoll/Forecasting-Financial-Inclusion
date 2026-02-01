import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.loader import load_data

def generate_baseline_forecast(df_hist: pd.DataFrame, indicator: str, years_to_forecast: list) -> pd.DataFrame:
    """
    Generates a linear trend forecast for a specific indicator.
    """
    df_ind = df_hist[df_hist['indicator'] == indicator].copy()
    
    if df_ind.empty:
        return pd.DataFrame()

    # Prepare X (Year) and y (Value)
    # Using ordinal date for regression to handle fractional years if necessary, but Year is safer for annual logic
    df_ind['ordinal_date'] = df_ind['observation_date'].map(pd.Timestamp.toordinal)
    
    X = df_ind[['ordinal_date']].values
    y = df_ind['value_numeric'].values
    
    model = LinearRegression()
    model.fit(X, y)
    
    # Create future dates (assuming mid-year or specific timing, let's say Jan 1st for simplicity or matching last obs month)
    # For annual forecasting 2025-2027
    future_dates = [pd.Timestamp(f"{year}-06-30") for year in years_to_forecast]
    future_X = [[d.toordinal()] for d in future_dates]
    
    predictions = model.predict(future_X)
    
    forecast_df = pd.DataFrame({
        'observation_date': future_dates,
        'indicator': indicator,
        'value_numeric': predictions,
        'type': 'baseline_forecast'
    })
    
    return forecast_df

def apply_event_impacts(forecast_df: pd.DataFrame, events_df: pd.DataFrame, impacts_df: pd.DataFrame, start_date: pd.Timestamp):
    """
    Adjusts the forecast based on defined events and their impacts.
    """
    adjusted_forecast = forecast_df.copy()
    adjusted_forecast['type'] = 'adjusted_forecast'
    
    # Filter for future events that might affect the forecast
    future_events = events_df[events_df['observation_date'] >= start_date]
    
    print(f"\nProcessing {len(future_events)} future events...")
    
    for _, event in future_events.iterrows():
        event_id = event['record_id']
        event_date = event['observation_date']
        
        # Find impacts linked to this event
        event_impacts = impacts_df[impacts_df['parent_id'] == event_id]
        
        for _, imp in event_impacts.iterrows():
            target_indicator = imp['indicator']
            # Default to 0 if NaN
            magnitude = imp['impact_estimate'] if pd.notnull(imp['impact_estimate']) else 0
            lag = imp['lag_months'] if pd.notnull(imp['lag_months']) else 0
            
            # Calculate when the impact starts
            impact_start_date = event_date + pd.DateOffset(months=int(lag))
            
            # Apply to all forecast points after the impact start date
            # Note: This is a simplified "step change" model. 
            # If magnitude is percentage points (e.g. 0.05 for 5%), we add it directly if value is ratio, or check units.
            # Assuming value_numeric is in same units (e.g. 0-1 or 0-100).
            
            mask = (adjusted_forecast['indicator'] == target_indicator) & \
                   (adjusted_forecast['observation_date'] >= impact_start_date)
            
            if mask.any():
                print(f"  -> Applying impact of {magnitude} to {target_indicator} starting {impact_start_date.date()} (Event: {event_id})")
                adjusted_forecast.loc[mask, 'value_numeric'] += magnitude

    return adjusted_forecast

def main():
    data = load_data()
    obs = data['observations']
    events = data['events']
    impacts = data['impacts']
    
    forecast_years = [2025, 2026, 2027, 2028]
    indicators = obs['indicator'].unique()
    
    all_forecasts = []
    
    print("Generating baselines...")
    for ind in indicators:
        # Generate baseline
        baseline = generate_baseline_forecast(obs, ind, forecast_years)
        if not baseline.empty:
            all_forecasts.append(baseline)
    
    if not all_forecasts:
        print("No forecasts generated.")
        return

    baseline_df = pd.concat(all_forecasts, ignore_index=True)
    
    # Combine history with baseline to see the full picture for impact calculation context if needed
    # But here we just adjust the future baseline
    
    print("Applying impacts...")
    # We essentially apply impacts to the baseline we just created
    # We use the events dataframe to find future events
    
    # Ensure impacts has numeric estimate
    if 'impact_estimate' in impacts.columns:
        impacts['impact_estimate'] = pd.to_numeric(impacts['impact_estimate'], errors='coerce').fillna(0)
    
    final_forecast = apply_event_impacts(baseline_df, events, impacts, pd.Timestamp('2024-01-01'))
    
    # Output results
    print("\n--- FORECAST RESULTS (Sample) ---")
    print(final_forecast.head())
    
    # Save to CSV for Dashboard
    output_dir = 'data/processed'
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'forecast_results.csv')
    final_forecast.to_csv(output_path, index=False)
    print(f"\nForecast saved to {output_path}")

if __name__ == "__main__":
    main()
