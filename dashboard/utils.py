"""
Dashboard Utility Functions

Helper functions for the Streamlit dashboard including data loading,
caching, chart generation, and metric calculations.
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import streamlit as st
from typing import Dict, List, Tuple
import os


@st.cache_data
def load_all_data():
    """Load all data files with caching."""
    from src.loader import load_data
    
    data_path = 'data/raw/ethiopia_fi_unified_data.xlsx'
    
    if not os.path.exists(data_path):
        st.error(f"Data file not found: {data_path}")
        return None
    
    data = load_data(data_path)
    
    # Load forecasts if available
    forecast_path = 'data/processed/task4_forecasts_2025_2027.csv'
    if os.path.exists(forecast_path):
        data['forecasts'] = pd.read_csv(forecast_path)
        data['forecasts']['observation_date'] = pd.to_datetime(data['forecasts']['observation_date'])
    else:
        data['forecasts'] = pd.DataFrame()
    
    return data


def calculate_key_metrics(observations: pd.DataFrame) -> Dict:
    """Calculate key metrics for the overview page."""
    metrics = {}
    
    # Latest Account Ownership
    acc_ownership = observations[observations['indicator_code'] == 'ACC_OWNERSHIP']
    if not acc_ownership.empty:
        latest = acc_ownership.sort_values('observation_date').iloc[-1]
        metrics['account_ownership'] = {
            'value': latest['value_numeric'],
            'date': latest['observation_date']
        }
    
    # Latest Mobile Money Accounts
    mm_accounts = observations[observations['indicator_code'] == 'ACC_MM_ACCOUNT']
    if not mm_accounts.empty:
        latest = mm_accounts.sort_values('observation_date').iloc[-1]
        metrics['mobile_money'] = {
            'value': latest['value_numeric'],
            'date': latest['observation_date']
        }
    
    # Latest Digital Payment Usage
    digital_payment = observations[observations['indicator_code'] == 'USG_DIGITAL_PAYMENT']
    if not digital_payment.empty:
        latest = digital_payment.sort_values('observation_date').iloc[-1]
        metrics['digital_payment'] = {
            'value': latest['value_numeric'],
            'date': latest['observation_date']
        }
    
    # Growth rates
    if not acc_ownership.empty and len(acc_ownership) >= 2:
        acc_ownership = acc_ownership.sort_values('observation_date')
        prev = acc_ownership.iloc[-2]['value_numeric']
        curr = acc_ownership.iloc[-1]['value_numeric']
        metrics['account_ownership']['growth'] = curr - prev
    
    return metrics


def create_trend_chart(
    observations: pd.DataFrame,
    indicator_code: str,
    title: str,
    show_events: bool = False,
    events_df: pd.DataFrame = None
) -> go.Figure:
    """Create an interactive trend chart using Plotly."""
    
    data = observations[observations['indicator_code'] == indicator_code].copy()
    data = data.sort_values('observation_date')
    
    fig = go.Figure()
    
    # Add main trend line
    fig.add_trace(go.Scatter(
        x=data['observation_date'],
        y=data['value_numeric'],
        mode='lines+markers',
        name='Historical Data',
        line=dict(color='#3498DB', width=3),
        marker=dict(size=10)
    ))
    
    # Add events if requested
    if show_events and events_df is not None:
        for _, event in events_df.iterrows():
            event_date = pd.to_datetime(event['observation_date'])
            fig.add_vline(
                x=event_date,
                line_dash="dash",
                line_color="red",
                opacity=0.5,
                annotation_text=event['indicator'][:20],
                annotation_position="top"
            )
    
    fig.update_layout(
        title=title,
        xaxis_title="Year",
        yaxis_title="Percentage (%)",
        hovermode='x unified',
        template='plotly_white',
        height=500
    )
    
    return fig


def create_forecast_chart(
    observations: pd.DataFrame,
    forecasts: pd.DataFrame,
    indicator_code: str,
    title: str
) -> go.Figure:
    """Create forecast visualization with scenarios and confidence intervals."""
    
    fig = go.Figure()
    
    # Historical data
    hist_data = observations[observations['indicator_code'] == indicator_code].copy()
    hist_data = hist_data.sort_values('observation_date')
    
    fig.add_trace(go.Scatter(
        x=hist_data['observation_date'],
        y=hist_data['value_numeric'],
        mode='lines+markers',
        name='Historical',
        line=dict(color='#34495E', width=3),
        marker=dict(size=10)
    ))
    
    # Forecast scenarios
    if not forecasts.empty:
        forecast_data = forecasts[forecasts['indicator_code'] == indicator_code]
        
        colors = {
            'optimistic': '#27AE60',
            'base': '#3498DB',
            'pessimistic': '#E74C3C'
        }
        
        for scenario in ['pessimistic', 'base', 'optimistic']:
            scenario_data = forecast_data[forecast_data['scenario'] == scenario].sort_values('observation_date')
            
            if not scenario_data.empty:
                linestyle = 'solid' if scenario == 'base' else 'dash'
                
                fig.add_trace(go.Scatter(
                    x=scenario_data['observation_date'],
                    y=scenario_data['value_numeric'],
                    mode='lines+markers',
                    name=f'{scenario.capitalize()} Scenario',
                    line=dict(color=colors[scenario], width=2.5, dash=linestyle),
                    marker=dict(size=8)
                ))
        
        # Add confidence interval for base scenario
        base_data = forecast_data[forecast_data['scenario'] == 'base'].sort_values('observation_date')
        if not base_data.empty and 'ci_lower' in base_data.columns:
            fig.add_trace(go.Scatter(
                x=base_data['observation_date'],
                y=base_data['ci_upper'],
                mode='lines',
                line=dict(width=0),
                showlegend=False,
                hoverinfo='skip'
            ))
            
            fig.add_trace(go.Scatter(
                x=base_data['observation_date'],
                y=base_data['ci_lower'],
                mode='lines',
                line=dict(width=0),
                fillcolor='rgba(52, 152, 219, 0.2)',
                fill='tonexty',
                name='95% Confidence Interval',
                hoverinfo='skip'
            ))
    
    fig.update_layout(
        title=title,
        xaxis_title="Year",
        yaxis_title="Percentage (%)",
        hovermode='x unified',
        template='plotly_white',
        height=600,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    return fig


def create_comparison_chart(observations: pd.DataFrame, indicators: List[str]) -> go.Figure:
    """Create a comparison chart for multiple indicators."""
    
    fig = go.Figure()
    
    colors = ['#3498DB', '#E74C3C', '#27AE60', '#F39C12', '#9B59B6']
    
    for idx, indicator_code in enumerate(indicators):
        data = observations[observations['indicator_code'] == indicator_code].copy()
        data = data.sort_values('observation_date')
        
        if not data.empty:
            indicator_name = data.iloc[0]['indicator']
            
            fig.add_trace(go.Scatter(
                x=data['observation_date'],
                y=data['value_numeric'],
                mode='lines+markers',
                name=indicator_name,
                line=dict(color=colors[idx % len(colors)], width=2.5),
                marker=dict(size=8)
            ))
    
    fig.update_layout(
        title="Indicator Comparison",
        xaxis_title="Year",
        yaxis_title="Percentage (%)",
        hovermode='x unified',
        template='plotly_white',
        height=500,
        legend=dict(
            orientation="v",
            yanchor="top",
            y=1,
            xanchor="left",
            x=1.02
        )
    )
    
    return fig


def create_event_timeline(events: pd.DataFrame) -> go.Figure:
    """Create an interactive event timeline."""
    
    events = events.copy()
    events['observation_date'] = pd.to_datetime(events['observation_date'])
    events = events.sort_values('observation_date')
    
    # Create color mapping for event categories
    category_colors = {
        'product_launch': '#27AE60',
        'policy': '#3498DB',
        'infrastructure': '#F39C12',
        'market': '#E74C3C'
    }
    
    fig = go.Figure()
    
    for category in events['category'].unique():
        category_events = events[events['category'] == category]
        
        fig.add_trace(go.Scatter(
            x=category_events['observation_date'],
            y=[category] * len(category_events),
            mode='markers+text',
            name=category.replace('_', ' ').title(),
            marker=dict(
                size=15,
                color=category_colors.get(category, '#95A5A6'),
                symbol='diamond'
            ),
            text=category_events['indicator'],
            textposition='top center',
            hovertemplate='<b>%{text}</b><br>Date: %{x}<extra></extra>'
        ))
    
    fig.update_layout(
        title="Event Timeline",
        xaxis_title="Date",
        yaxis_title="Event Category",
        hovermode='closest',
        template='plotly_white',
        height=400,
        showlegend=True
    )
    
    return fig


def format_metric(value: float, format_type: str = 'percentage') -> str:
    """Format metric values for display."""
    if format_type == 'percentage':
        return f"{value:.1f}%"
    elif format_type == 'millions':
        return f"{value:.1f}M"
    elif format_type == 'change':
        sign = '+' if value >= 0 else ''
        return f"{sign}{value:.1f}pp"
    else:
        return f"{value:.1f}"


def calculate_progress_to_target(current: float, target: float) -> Tuple[float, str]:
    """Calculate progress towards a target."""
    progress = (current / target) * 100
    
    if progress >= 100:
        status = "✅ Target Achieved"
    elif progress >= 80:
        status = "🟢 On Track"
    elif progress >= 60:
        status = "🟡 Moderate Progress"
    else:
        status = "🔴 Behind Target"
    
    return progress, status
