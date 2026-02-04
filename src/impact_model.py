"""
Event Impact Modeling Module

This module provides functions to analyze and model the impact of events
(policies, product launches, infrastructure investments) on financial inclusion indicators.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, Tuple, List
import warnings
warnings.filterwarnings('ignore')


def build_impact_matrix(events_df: pd.DataFrame, impacts_df: pd.DataFrame) -> pd.DataFrame:
    """
    Build an event-indicator association matrix showing which events affect which indicators.
    
    Args:
        events_df: DataFrame containing event records
        impacts_df: DataFrame containing impact link records
        
    Returns:
        DataFrame with events as rows, indicators as columns, and impact estimates as values
    """
    # Merge events with their impacts
    event_impacts = impacts_df.merge(
        events_df[['record_id', 'indicator', 'observation_date', 'category']], 
        left_on='parent_id', 
        right_on='record_id',
        suffixes=('_impact', '_event')
    )
    
    # Create pivot table: events x indicators
    matrix = event_impacts.pivot_table(
        index='indicator_event',
        columns='indicator_impact',
        values='impact_estimate',
        aggfunc='first'
    )
    
    # Fill NaN with 0 (no impact)
    matrix = matrix.fillna(0)
    
    return matrix


def create_impact_heatmap(impact_matrix: pd.DataFrame, save_path: str = None) -> plt.Figure:
    """
    Create a heatmap visualization of the event-indicator impact matrix.
    
    Args:
        impact_matrix: Event-indicator association matrix
        save_path: Optional path to save the figure
        
    Returns:
        Matplotlib figure object
    """
    fig, ax = plt.subplots(figsize=(12, 8))
    
    sns.heatmap(
        impact_matrix,
        annot=True,
        fmt='.1f',
        cmap='RdYlGn',
        center=0,
        cbar_kws={'label': 'Impact Estimate (percentage points)'},
        linewidths=0.5,
        ax=ax
    )
    
    ax.set_title('Event-Indicator Impact Matrix', fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('Indicator Code', fontsize=12, fontweight='bold')
    ax.set_ylabel('Event', fontsize=12, fontweight='bold')
    
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Heatmap saved to: {save_path}")
    
    return fig


def get_impact_summary(impacts_df: pd.DataFrame, events_df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate a summary table of all impact relationships.
    
    Args:
        impacts_df: DataFrame containing impact link records
        events_df: DataFrame containing event records
        
    Returns:
        DataFrame with detailed impact information
    """
    # Merge impacts with event details
    summary = impacts_df.merge(
        events_df[['record_id', 'indicator', 'observation_date', 'category']], 
        left_on='parent_id', 
        right_on='record_id',
        suffixes=('', '_event')
    )
    
    # Select and rename columns for clarity
    summary = summary[[
        'indicator_event', 'category', 'observation_date',
        'related_indicator', 'impact_direction', 'impact_magnitude',
        'impact_estimate', 'lag_months', 'evidence_basis', 'confidence'
    ]]
    
    summary.columns = [
        'Event', 'Event Type', 'Event Date',
        'Affected Indicator', 'Direction', 'Magnitude',
        'Estimate (pp)', 'Lag (months)', 'Evidence', 'Confidence'
    ]
    
    return summary.sort_values('Event Date')


def estimate_impact_magnitude(
    event_type: str,
    indicator: str,
    comparable_evidence: Dict[str, float] = None
) -> float:
    """
    Estimate the impact magnitude of an event on an indicator.
    
    Args:
        event_type: Type of event (policy, product_launch, infrastructure)
        indicator: Target indicator code
        comparable_evidence: Dictionary of evidence from comparable countries
        
    Returns:
        Estimated impact in percentage points
    """
    # Default impact estimates based on event type and indicator
    default_impacts = {
        'product_launch': {
            'ACC_MM_ACCOUNT': 3.0,
            'USG_DIGITAL_PAYMENT': 4.0,
            'ACC_OWNERSHIP': 1.5
        },
        'policy': {
            'ACC_OWNERSHIP': 2.0,
            'USG_DIGITAL_PAYMENT': 1.5,
            'ACC_MM_ACCOUNT': 1.0
        },
        'infrastructure': {
            'USG_DIGITAL_PAYMENT': 3.5,
            'ACC_MM_ACCOUNT': 2.0,
            'ACC_OWNERSHIP': 1.0
        }
    }
    
    # Use comparable evidence if available, otherwise use defaults
    if comparable_evidence and event_type in comparable_evidence:
        return comparable_evidence[event_type]
    
    return default_impacts.get(event_type, {}).get(indicator, 1.0)


def validate_impact_model(
    observations_df: pd.DataFrame,
    events_df: pd.DataFrame,
    impacts_df: pd.DataFrame,
    indicator_code: str,
    event_id: str
) -> Dict[str, any]:
    """
    Validate impact model by comparing predicted vs. observed outcomes.
    
    Args:
        observations_df: Historical observations
        events_df: Event records
        impacts_df: Impact link records
        indicator_code: Indicator to validate
        event_id: Event to test
        
    Returns:
        Dictionary with validation results
    """
    # Get event details
    event = events_df[events_df['record_id'] == event_id].iloc[0]
    event_date = pd.to_datetime(event['observation_date'])
    
    # Get impact estimate
    impact = impacts_df[
        (impacts_df['parent_id'] == event_id) & 
        (impacts_df['indicator'] == indicator_code)
    ]
    
    if impact.empty:
        return {'error': 'No impact link found for this event-indicator pair'}
    
    impact = impact.iloc[0]
    impact_estimate = impact['impact_estimate']
    lag_months = impact['lag_months']
    
    # Calculate impact start date
    impact_date = event_date + pd.DateOffset(months=int(lag_months))
    
    # Get observations for this indicator
    obs = observations_df[observations_df['indicator_code'] == indicator_code].copy()
    obs['observation_date'] = pd.to_datetime(obs['observation_date'])
    obs = obs.sort_values('observation_date')
    
    # Find observations before and after impact
    before = obs[obs['observation_date'] < impact_date]
    after = obs[obs['observation_date'] >= impact_date]
    
    if before.empty or after.empty:
        return {'error': 'Insufficient data before/after event'}
    
    # Calculate observed change
    value_before = before.iloc[-1]['value_numeric']
    value_after = after.iloc[0]['value_numeric']
    observed_change = value_after - value_before
    
    # Calculate time difference for annualization
    time_diff_years = (after.iloc[0]['observation_date'] - before.iloc[-1]['observation_date']).days / 365.25
    
    # Annualized observed change
    annualized_change = observed_change / time_diff_years if time_diff_years > 0 else observed_change
    
    return {
        'event': event['indicator'],
        'event_date': event_date,
        'impact_date': impact_date,
        'indicator': indicator_code,
        'predicted_impact': impact_estimate,
        'value_before': value_before,
        'value_after': value_after,
        'observed_change': observed_change,
        'time_period_years': time_diff_years,
        'annualized_change': annualized_change,
        'prediction_accuracy': 'Good' if abs(annualized_change - impact_estimate) < 2 else 'Moderate'
    }


def apply_comparable_evidence(
    country: str,
    event_type: str,
    indicator: str
) -> Dict[str, any]:
    """
    Retrieve comparable evidence from similar markets.
    
    Args:
        country: Reference country (e.g., 'Kenya', 'Tanzania', 'Rwanda')
        event_type: Type of event
        indicator: Target indicator
        
    Returns:
        Dictionary with evidence details
    """
    # Comparable country evidence database
    evidence_db = {
        'Kenya': {
            'M-Pesa Launch': {
                'ACC_MM_ACCOUNT': {
                    'impact': 15.0,
                    'timeframe': '3 years',
                    'source': 'Suri & Jack (2016)',
                    'notes': 'M-Pesa reached 70% penetration in 7 years'
                },
                'USG_DIGITAL_PAYMENT': {
                    'impact': 20.0,
                    'timeframe': '5 years',
                    'source': 'Suri & Jack (2016)',
                    'notes': 'Significant usage growth post-launch'
                }
            }
        },
        'Tanzania': {
            'Interoperability': {
                'USG_DIGITAL_PAYMENT': {
                    'impact': 5.0,
                    'timeframe': '1 year',
                    'source': 'GSMA Mobile Money Report',
                    'notes': 'Interoperability increased transaction volumes'
                }
            }
        },
        'Rwanda': {
            'Digital Strategy': {
                'ACC_OWNERSHIP': {
                    'impact': 3.0,
                    'timeframe': '2 years',
                    'source': 'Access to Finance Rwanda',
                    'notes': 'Government strategy supported inclusion growth'
                }
            }
        }
    }
    
    return evidence_db.get(country, {}).get(event_type, {}).get(indicator, {})


def calculate_cumulative_impact(
    impacts_df: pd.DataFrame,
    events_df: pd.DataFrame,
    indicator_code: str,
    reference_date: pd.Timestamp
) -> float:
    """
    Calculate cumulative impact of all events on an indicator up to a reference date.
    
    Args:
        impacts_df: Impact link records
        events_df: Event records
        indicator_code: Target indicator
        reference_date: Date to calculate cumulative impact up to
        
    Returns:
        Total cumulative impact in percentage points
    """
    # Get all impacts for this indicator
    indicator_impacts = impacts_df[impacts_df['indicator'] == indicator_code]
    
    total_impact = 0.0
    
    for _, impact in indicator_impacts.iterrows():
        event_id = impact['parent_id']
        event = events_df[events_df['record_id'] == event_id]
        
        if event.empty:
            continue
            
        event_date = pd.to_datetime(event.iloc[0]['observation_date'])
        lag_months = impact['lag_months']
        impact_start = event_date + pd.DateOffset(months=int(lag_months))
        
        # Only count impacts that have occurred by reference date
        if impact_start <= reference_date:
            total_impact += impact['impact_estimate']
    
    return total_impact
