import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys
import os

# Add project root to path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.loader import load_data

st.set_page_config(page_title="Ethiopia Financial Inclusion Forecast", layout="wide")

@st.cache_data
def get_data():
    # Load Historical
    raw_data = load_data()
    obs = raw_data['observations']
    events = raw_data['events']
    
    # Load Forecast
    forecast_path = 'data/processed/forecast_results.csv'
    if os.path.exists(forecast_path):
        forecast = pd.read_csv(forecast_path)
        forecast['observation_date'] = pd.to_datetime(forecast['observation_date'])
    else:
        forecast = pd.DataFrame()
        
    return obs, events, forecast

try:
    obs, events, forecast = get_data()
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

st.title("🇪🇹 Ethiopia Financial Inclusion Forecasting (2025-2028)")

st.markdown("""
This dashboard enables the exploration of historical trends and future scenarios for financial inclusion in Ethiopia.
It incorporates **Event Impact Modeling** to adjust baseline trends based on known policy interventions and market shifts.
""")

# Sidebar controls
st.sidebar.header("Configuration")
selected_indicator = st.sidebar.selectbox(
    "Select Indicator",
    options=obs['indicator'].unique(),
    index=0
)

# Filter Data
hist_data = obs[obs['indicator'] == selected_indicator].sort_values('observation_date')
fore_data = forecast[forecast['indicator'] == selected_indicator].sort_values('observation_date')

if hist_data.empty:
    st.warning(f"No historical data found for {selected_indicator}")
else:
    # --- Visualization ---
    st.subheader(f"Trend Analysis: {selected_indicator}")
    
    fig = go.Figure()
    
    # Historical Line
    fig.add_trace(go.Scatter(
        x=hist_data['observation_date'], 
        y=hist_data['value_numeric'],
        mode='lines+markers',
        name='Historical Data',
        line=dict(color='blue', width=2)
    ))
    
    # Forecast Lines
    if not fore_data.empty:
        # Baseline
        baseline = fore_data[fore_data['type'] == 'baseline_forecast']
        fig.add_trace(go.Scatter(
            x=baseline['observation_date'], 
            y=baseline['value_numeric'],
            mode='lines+markers',
            name='Baseline Forecast (Trend)',
            line=dict(color='gray', dash='dash')
        ))
        
        # Adjusted
        adjusted = fore_data[fore_data['type'] == 'adjusted_forecast']
        fig.add_trace(go.Scatter(
            x=adjusted['observation_date'], 
            y=adjusted['value_numeric'],
            mode='lines+markers',
            name='Adjusted Forecast (With Events)',
            line=dict(color='green', width=3)
        ))
        
    # Add Events
    # Filter events that are relevant ?? Or just show all major ones?
    # Showing all might be cluttered, let's just show top 5 or just markers
    for _, event in events.iterrows():
        if pd.notnull(event['observation_date']):
             fig.add_vline(
                 x=event['observation_date'].timestamp() * 1000, 
                 line_width=1, 
                 line_dash="dot", 
                 line_color="red",
                 annotation_text=event['record_id'], 
                 annotation_position="top right"
             )

    fig.update_layout(
        title=f"Forecast: {selected_indicator}",
        xaxis_title="Year",
        yaxis_title="Value",
        hovermode='x unified',
        height=600
    )
    
    st.plotly_chart(fig, use_container_width=True)

    # --- Data Tables ---
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("### Historical Data")
        st.dataframe(hist_data[['observation_date', 'value_numeric', 'source_name']].reset_index(drop=True))
        
    with col2:
        st.write("### Adjusted Forecast Data")
        if not fore_data.empty:
            st.dataframe(fore_data[fore_data['type'] == 'adjusted_forecast'][['observation_date', 'value_numeric']].reset_index(drop=True))
        else:
            st.write("No forecast available.")

# --- Event Impact Explorer ---
st.markdown("---")
st.subheader("Event Impact Reference")
st.dataframe(events[['record_id', 'observation_date', 'description']].merge(
    pd.DataFrame(columns=['impact']), how='cross' # Placeholder, better to merge impacts
))

# Just raw tables for debug/view
with st.expander("View Raw Event Data"):
    st.dataframe(events)
