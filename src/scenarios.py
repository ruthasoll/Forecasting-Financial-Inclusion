"""
Scenario Generation Module for Financial Inclusion Forecasting

This module provides functions to generate different forecast scenarios
(optimistic, base, pessimistic) and calculate confidence intervals.
"""

import pandas as pd
import numpy as np
from scipy import stats
from typing import Dict, Tuple, List
import warnings
warnings.filterwarnings('ignore')


def generate_base_scenario(
    baseline_forecast: pd.DataFrame,
    impacts_df: pd.DataFrame,
    events_df: pd.DataFrame,
    indicator_code: str
) -> pd.DataFrame:
    """
    Generate base case scenario using expected event impacts.
    
    Args:
        baseline_forecast: Baseline trend forecast
        impacts_df: Impact link records
        events_df: Event records
        indicator_code: Target indicator
        
    Returns:
        DataFrame with base scenario forecast
    """
    scenario = baseline_forecast.copy()
    scenario['scenario'] = 'base'
    
    # Apply expected impacts
    for _, impact in impacts_df[impacts_df['indicator'] == indicator_code].iterrows():
        event_id = impact['parent_id']
        event = events_df[events_df['record_id'] == event_id]
        
        if event.empty:
            continue
            
        event_date = pd.to_datetime(event.iloc[0]['observation_date'])
        lag_months = impact['lag_months']
        impact_start = event_date + pd.DateOffset(months=int(lag_months))
        
        # Apply impact to forecast periods after impact start
        mask = scenario['observation_date'] >= impact_start
        scenario.loc[mask, 'value_numeric'] += impact['impact_estimate']
    
    return scenario


def generate_optimistic_scenario(
    baseline_forecast: pd.DataFrame,
    impacts_df: pd.DataFrame,
    events_df: pd.DataFrame,
    indicator_code: str,
    multiplier: float = 1.3
) -> pd.DataFrame:
    """
    Generate optimistic scenario with higher impact estimates.
    
    Args:
        baseline_forecast: Baseline trend forecast
        impacts_df: Impact link records
        events_df: Event records
        indicator_code: Target indicator
        multiplier: Factor to increase impact estimates (default 1.3 = 30% higher)
        
    Returns:
        DataFrame with optimistic scenario forecast
    """
    # Create modified impacts with higher estimates
    impacts_optimistic = impacts_df.copy()
    impacts_optimistic['impact_estimate'] = impacts_optimistic['impact_estimate'] * multiplier
    
    scenario = baseline_forecast.copy()
    scenario['scenario'] = 'optimistic'
    
    # Apply amplified impacts
    for _, impact in impacts_optimistic[impacts_optimistic['indicator'] == indicator_code].iterrows():
        event_id = impact['parent_id']
        event = events_df[events_df['record_id'] == event_id]
        
        if event.empty:
            continue
            
        event_date = pd.to_datetime(event.iloc[0]['observation_date'])
        lag_months = impact['lag_months']
        impact_start = event_date + pd.DateOffset(months=int(lag_months))
        
        mask = scenario['observation_date'] >= impact_start
        scenario.loc[mask, 'value_numeric'] += impact['impact_estimate']
    
    return scenario


def generate_pessimistic_scenario(
    baseline_forecast: pd.DataFrame,
    impacts_df: pd.DataFrame,
    events_df: pd.DataFrame,
    indicator_code: str,
    multiplier: float = 0.7
) -> pd.DataFrame:
    """
    Generate pessimistic scenario with lower impact estimates.
    
    Args:
        baseline_forecast: Baseline trend forecast
        impacts_df: Impact link records
        events_df: Event records
        indicator_code: Target indicator
        multiplier: Factor to decrease impact estimates (default 0.7 = 30% lower)
        
    Returns:
        DataFrame with pessimistic scenario forecast
    """
    # Create modified impacts with lower estimates
    impacts_pessimistic = impacts_df.copy()
    impacts_pessimistic['impact_estimate'] = impacts_pessimistic['impact_estimate'] * multiplier
    
    scenario = baseline_forecast.copy()
    scenario['scenario'] = 'pessimistic'
    
    # Apply reduced impacts
    for _, impact in impacts_pessimistic[impacts_pessimistic['indicator'] == indicator_code].iterrows():
        event_id = impact['parent_id']
        event = events_df[events_df['record_id'] == event_id]
        
        if event.empty:
            continue
            
        event_date = pd.to_datetime(event.iloc[0]['observation_date'])
        lag_months = impact['lag_months']
        impact_start = event_date + pd.DateOffset(months=int(lag_months))
        
        mask = scenario['observation_date'] >= impact_start
        scenario.loc[mask, 'value_numeric'] += impact['impact_estimate']
    
    return scenario


def calculate_confidence_intervals(
    observations_df: pd.DataFrame,
    forecast_df: pd.DataFrame,
    indicator_code: str,
    confidence_level: float = 0.95
) -> pd.DataFrame:
    """
    Calculate confidence intervals for forecasts based on historical variance.
    
    Args:
        observations_df: Historical observations
        forecast_df: Forecast dataframe
        indicator_code: Target indicator
        confidence_level: Confidence level (default 0.95 for 95% CI)
        
    Returns:
        Forecast dataframe with confidence interval columns added
    """
    # Get historical observations for this indicator
    hist_obs = observations_df[observations_df['indicator_code'] == indicator_code].copy()
    
    if len(hist_obs) < 3:
        # Not enough data for meaningful CI, use fixed percentage
        forecast_df['ci_lower'] = forecast_df['value_numeric'] * 0.90
        forecast_df['ci_upper'] = forecast_df['value_numeric'] * 1.10
        return forecast_df
    
    # Calculate historical growth rates
    hist_obs = hist_obs.sort_values('observation_date')
    hist_obs['growth_rate'] = hist_obs['value_numeric'].pct_change()
    
    # Calculate standard deviation of growth rates
    growth_std = hist_obs['growth_rate'].std()
    
    # Use t-distribution for small samples
    n = len(hist_obs)
    t_value = stats.t.ppf((1 + confidence_level) / 2, n - 1)
    
    # Calculate margin of error as percentage of forecast value
    # Margin increases with forecast horizon
    forecast_df = forecast_df.copy()
    forecast_df['forecast_year'] = forecast_df['observation_date'].dt.year
    min_year = forecast_df['forecast_year'].min()
    
    for idx, row in forecast_df.iterrows():
        years_ahead = row['forecast_year'] - min_year + 1
        # Uncertainty grows with time
        margin = row['value_numeric'] * growth_std * t_value * np.sqrt(years_ahead)
        
        forecast_df.loc[idx, 'ci_lower'] = max(0, row['value_numeric'] - margin)
        forecast_df.loc[idx, 'ci_upper'] = min(100, row['value_numeric'] + margin)
    
    return forecast_df


def generate_all_scenarios(
    baseline_forecast: pd.DataFrame,
    observations_df: pd.DataFrame,
    impacts_df: pd.DataFrame,
    events_df: pd.DataFrame,
    indicator_code: str
) -> pd.DataFrame:
    """
    Generate all three scenarios (optimistic, base, pessimistic) with confidence intervals.
    
    Args:
        baseline_forecast: Baseline trend forecast
        observations_df: Historical observations
        impacts_df: Impact link records
        events_df: Event records
        indicator_code: Target indicator
        
    Returns:
        Combined dataframe with all scenarios
    """
    # Generate scenarios
    base = generate_base_scenario(baseline_forecast, impacts_df, events_df, indicator_code)
    optimistic = generate_optimistic_scenario(baseline_forecast, impacts_df, events_df, indicator_code)
    pessimistic = generate_pessimistic_scenario(baseline_forecast, impacts_df, events_df, indicator_code)
    
    # Add confidence intervals to base scenario
    base = calculate_confidence_intervals(observations_df, base, indicator_code)
    
    # Combine all scenarios
    all_scenarios = pd.concat([base, optimistic, pessimistic], ignore_index=True)
    
    return all_scenarios


def calculate_forecast_metrics(forecast_df: pd.DataFrame, target_value: float = None) -> Dict:
    """
    Calculate key metrics from forecast results.
    
    Args:
        forecast_df: Forecast dataframe
        target_value: Optional target value to compare against
        
    Returns:
        Dictionary of forecast metrics
    """
    metrics = {}
    
    # Get base scenario
    base = forecast_df[forecast_df['scenario'] == 'base']
    
    if not base.empty:
        metrics['final_forecast'] = base.iloc[-1]['value_numeric']
        metrics['forecast_years'] = base['observation_date'].dt.year.tolist()
        
        # Calculate growth
        if len(base) > 1:
            initial = base.iloc[0]['value_numeric']
            final = base.iloc[-1]['value_numeric']
            metrics['total_growth'] = final - initial
            metrics['avg_annual_growth'] = metrics['total_growth'] / len(base)
        
        # Target comparison
        if target_value:
            metrics['target_value'] = target_value
            metrics['gap_to_target'] = target_value - metrics['final_forecast']
            metrics['on_track'] = metrics['gap_to_target'] <= 0
    
    # Scenario range
    optimistic = forecast_df[forecast_df['scenario'] == 'optimistic']
    pessimistic = forecast_df[forecast_df['scenario'] == 'pessimistic']
    
    if not optimistic.empty and not pessimistic.empty:
        metrics['best_case'] = optimistic.iloc[-1]['value_numeric']
        metrics['worst_case'] = pessimistic.iloc[-1]['value_numeric']
        metrics['scenario_range'] = metrics['best_case'] - metrics['worst_case']
    
    return metrics


def create_future_events(start_year: int = 2025, end_year: int = 2027) -> pd.DataFrame:
    """
    Create hypothetical future events for scenario planning.
    
    Args:
        start_year: Start year for future events
        end_year: End year for future events
        
    Returns:
        DataFrame with future event scenarios
    """
    future_events = [
        {
            'record_id': 'EVT_FUT_001',
            'record_type': 'event',
            'category': 'infrastructure',
            'indicator': 'Agent Network Expansion',
            'observation_date': f'{start_year}-06-01',
            'confidence': 'medium',
            'notes': 'Projected agent network doubling'
        },
        {
            'record_id': 'EVT_FUT_002',
            'record_type': 'event',
            'category': 'policy',
            'indicator': 'Credit Scoring Framework',
            'observation_date': f'{start_year + 1}-01-01',
            'confidence': 'low',
            'notes': 'Potential digital credit regulation'
        },
        {
            'record_id': 'EVT_FUT_003',
            'record_type': 'event',
            'category': 'infrastructure',
            'indicator': '5G Rollout',
            'observation_date': f'{start_year + 2}-01-01',
            'confidence': 'low',
            'notes': 'Potential 5G network deployment'
        }
    ]
    
    return pd.DataFrame(future_events)
