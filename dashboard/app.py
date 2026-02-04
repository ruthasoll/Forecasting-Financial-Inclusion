"""
Financial Inclusion Forecasting Dashboard

Interactive Streamlit dashboard for exploring Ethiopia's financial inclusion data,
trends, forecasts, and projections.
"""

import streamlit as st
import pandas as pd
import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dashboard.utils import (
    load_all_data,
    calculate_key_metrics,
    create_trend_chart,
    create_forecast_chart,
    create_comparison_chart,
    create_event_timeline,
    format_metric,
    calculate_progress_to_target
)

# Page configuration
st.set_page_config(
    page_title="Ethiopia Financial Inclusion Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #2C3E50;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #F8F9FA;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #3498DB;
    }
    .insight-box {
        background-color: #E8F4F8;
        padding: 1rem;
        border-radius: 5px;
        border-left: 4px solid #3498DB;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def get_data():
    return load_all_data()

data = get_data()

if data is None:
    st.error("Failed to load data. Please check data files.")
    st.stop()

observations = data['observations']
events = data['events']
targets = data['targets']
impacts = data['impacts']
forecasts = data.get('forecasts', pd.DataFrame())

# Sidebar navigation
st.sidebar.title("📊 Navigation")
page = st.sidebar.radio(
    "Select Page",
    ["🏠 Overview", "📈 Trends Analysis", "🔮 Forecasts", "🎯 Inclusion Projections"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### About")
st.sidebar.info(
    """
    This dashboard presents Ethiopia's financial inclusion data,
    trends, and forecasts for 2025-2027.
    
    **Data Sources:**
    - World Bank Global Findex
    - Ethio Telecom
    - Safaricom Ethiopia
    - National Bank of Ethiopia
    """
)

# ==================== PAGE 1: OVERVIEW ====================
if page == "🏠 Overview":
    st.markdown('<p class="main-header">🇪🇹 Ethiopia Financial Inclusion Dashboard</p>', unsafe_allow_html=True)
    
    st.markdown("### 📊 Key Metrics Summary")
    
    metrics = calculate_key_metrics(observations)
    
    # Create three columns for key metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if 'account_ownership' in metrics:
            value = metrics['account_ownership']['value']
            growth = metrics['account_ownership'].get('growth', 0)
            
            st.metric(
                label="📱 Account Ownership Rate",
                value=format_metric(value),
                delta=format_metric(growth, 'change') if growth != 0 else None
            )
            st.caption(f"As of {metrics['account_ownership']['date'].strftime('%B %Y')}")
    
    with col2:
        if 'mobile_money' in metrics:
            value = metrics['mobile_money']['value']
            
            st.metric(
                label="💳 Mobile Money Accounts",
                value=format_metric(value),
            )
            st.caption(f"As of {metrics['mobile_money']['date'].strftime('%B %Y')}")
    
    with col3:
        if 'digital_payment' in metrics:
            value = metrics['digital_payment']['value']
            
            st.metric(
                label="💰 Digital Payment Usage",
                value=format_metric(value),
            )
            st.caption(f"As of {metrics['digital_payment']['date'].strftime('%B %Y')}")
    
    st.markdown("---")
    
    # Growth highlights
    st.markdown("### 📈 Growth Highlights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="insight-box">', unsafe_allow_html=True)
        st.markdown("**🚀 Telebirr Impact**")
        st.markdown("""
        - Launched: May 2021
        - Users: 54.84M (June 2024)
        - Growth: 14.8M users in 1 year
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="insight-box">', unsafe_allow_html=True)
        st.markdown("**🌟 M-Pesa Growth**")
        st.markdown("""
        - Launched: August 2023
        - Users: 10.8M (Dec 2024)
        - Rapid adoption in competitive market
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Event timeline
    st.markdown("### 📅 Key Events Timeline")
    
    if not events.empty:
        timeline_fig = create_event_timeline(events)
        st.plotly_chart(timeline_fig, width='stretch')
    
    st.markdown("---")
    
    # Quick insights
    st.markdown("### 💡 Quick Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**📊 Current State (2024)**")
        st.markdown("""
        - 49% of adults have financial accounts
        - 9.45% have mobile money accounts
        - 35% use digital payments
        - Interoperability enabled (Jan 2024)
        """)
    
    with col2:
        st.markdown("**🎯 2027 Targets**")
        for _, target in targets.iterrows():
            st.markdown(f"- {target['indicator']}: {target['value_numeric']}%")
    
    # Data download
    st.markdown("---")
    st.markdown("### 📥 Download Data")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        csv = observations.to_csv(index=False)
        st.download_button(
            label="Download Observations",
            data=csv,
            file_name="ethiopia_fi_observations.csv",
            mime="text/csv"
        )
    
    with col2:
        csv = events.to_csv(index=False)
        st.download_button(
            label="Download Events",
            data=csv,
            file_name="ethiopia_fi_events.csv",
            mime="text/csv"
        )
    
    with col3:
        if not forecasts.empty:
            csv = forecasts.to_csv(index=False)
            st.download_button(
                label="Download Forecasts",
                data=csv,
                file_name="ethiopia_fi_forecasts.csv",
                mime="text/csv"
            )

# ==================== PAGE 2: TRENDS ANALYSIS ====================
elif page == "📈 Trends Analysis":
    st.markdown('<p class="main-header">📈 Trends Analysis</p>', unsafe_allow_html=True)
    
    st.markdown("### Historical Financial Inclusion Trends")
    
    # Indicator selector
    available_indicators = observations['indicator_code'].unique().tolist()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        selected_indicator = st.selectbox(
            "Select Indicator",
            available_indicators,
            format_func=lambda x: observations[observations['indicator_code'] == x].iloc[0]['indicator']
        )
    
    with col2:
        show_events = st.checkbox("Show Events", value=True)
    
    # Create trend chart
    indicator_name = observations[observations['indicator_code'] == selected_indicator].iloc[0]['indicator']
    
    trend_fig = create_trend_chart(
        observations,
        selected_indicator,
        f"{indicator_name} - Historical Trend",
        show_events=show_events,
        events_df=events if show_events else None
    )
    
    st.plotly_chart(trend_fig, width='stretch')
    
    # Show data table
    with st.expander("📋 View Data Table"):
        indicator_data = observations[observations['indicator_code'] == selected_indicator][
            ['observation_date', 'value_numeric', 'source_name', 'confidence']
        ].sort_values('observation_date', ascending=False)
        
        st.dataframe(indicator_data, width='stretch')
    
    st.markdown("---")
    
    # Multi-indicator comparison
    st.markdown("### 📊 Multi-Indicator Comparison")
    
    comparison_indicators = st.multiselect(
        "Select indicators to compare",
        available_indicators,
        default=['ACC_OWNERSHIP', 'ACC_MM_ACCOUNT', 'USG_DIGITAL_PAYMENT'] if all(
            x in available_indicators for x in ['ACC_OWNERSHIP', 'ACC_MM_ACCOUNT', 'USG_DIGITAL_PAYMENT']
        ) else available_indicators[:3],
        format_func=lambda x: observations[observations['indicator_code'] == x].iloc[0]['indicator']
    )
    
    if comparison_indicators:
        comparison_fig = create_comparison_chart(observations, comparison_indicators)
        st.plotly_chart(comparison_fig, width='stretch')
    
    st.markdown("---")
    
    # Date range filter
    st.markdown("### 📅 Date Range Analysis")
    
    col1, col2 = st.columns(2)
    
    min_date = observations['observation_date'].min()
    max_date = observations['observation_date'].max()
    
    with col1:
        start_date = st.date_input("Start Date", min_date, min_value=min_date, max_value=max_date)
    
    with col2:
        end_date = st.date_input("End Date", max_date, min_value=min_date, max_value=max_date)
    
    # Filter data by date range
    filtered_obs = observations[
        (observations['observation_date'] >= pd.to_datetime(start_date)) &
        (observations['observation_date'] <= pd.to_datetime(end_date))
    ]
    
    st.info(f"Showing {len(filtered_obs)} observations from {start_date} to {end_date}")

# ==================== PAGE 3: FORECASTS ====================
elif page == "🔮 Forecasts":
    st.markdown('<p class="main-header">🔮 Forecasts (2025-2027)</p>', unsafe_allow_html=True)
    
    if forecasts.empty:
        st.warning("No forecast data available. Please run the forecasting notebook first.")
    else:
        st.markdown("### Forecast Scenarios with Confidence Intervals")
        
        # Indicator selector
        forecast_indicators = forecasts['indicator_code'].unique().tolist()
        
        selected_forecast_indicator = st.selectbox(
            "Select Indicator for Forecast",
            forecast_indicators,
            format_func=lambda x: observations[observations['indicator_code'] == x].iloc[0]['indicator'] if not observations[observations['indicator_code'] == x].empty else x
        )
        
        # Create forecast chart
        indicator_name = observations[observations['indicator_code'] == selected_forecast_indicator].iloc[0]['indicator'] if not observations[observations['indicator_code'] == selected_forecast_indicator].empty else selected_forecast_indicator
        
        forecast_fig = create_forecast_chart(
            observations,
            forecasts,
            selected_forecast_indicator,
            f"{indicator_name} - Forecast Scenarios"
        )
        
        st.plotly_chart(forecast_fig, width='stretch')
        
        # Scenario comparison table
        st.markdown("### 📊 Scenario Comparison (2027)")
        
        forecast_2027 = forecasts[
            (forecasts['indicator_code'] == selected_forecast_indicator) &
            (forecasts['observation_date'].dt.year == 2027)
        ]
        
        if not forecast_2027.empty:
            col1, col2, col3 = st.columns(3)
            
            for col, scenario, color in zip(
                [col1, col2, col3],
                ['pessimistic', 'base', 'optimistic'],
                ['🔴', '🔵', '🟢']
            ):
                scenario_data = forecast_2027[forecast_2027['scenario'] == scenario]
                if not scenario_data.empty:
                    value = scenario_data.iloc[0]['value_numeric']
                    with col:
                        st.metric(
                            label=f"{color} {scenario.capitalize()}",
                            value=format_metric(value)
                        )
        
        # Key projected milestones
        st.markdown("---")
        st.markdown("### 🎯 Key Projected Milestones")
        
        base_forecasts = forecasts[forecasts['scenario'] == 'base']
        
        for indicator_code in forecast_indicators:
            indicator_forecast = base_forecasts[base_forecasts['indicator_code'] == indicator_code]
            
            if not indicator_forecast.empty:
                indicator_name = observations[observations['indicator_code'] == indicator_code].iloc[0]['indicator'] if not observations[observations['indicator_code'] == indicator_code].empty else indicator_code
                
                final_value = indicator_forecast.sort_values('observation_date').iloc[-1]['value_numeric']
                
                st.markdown(f"**{indicator_name}**")
                st.markdown(f"- Projected 2027 value: {format_metric(final_value)}")
                
                # Check against target
                target_row = targets[targets['indicator_code'].str.contains(indicator_code.split('_')[1], case=False, na=False)]
                if not target_row.empty:
                    target_value = target_row.iloc[0]['value_numeric']
                    gap = final_value - target_value
                    
                    if gap >= 0:
                        st.success(f"✅ Exceeds 2027 target by {format_metric(abs(gap), 'change')}")
                    else:
                        st.warning(f"⚠️ Falls short of 2027 target by {format_metric(abs(gap), 'change')}")

# ==================== PAGE 4: INCLUSION PROJECTIONS ====================
elif page == "🎯 Inclusion Projections":
    st.markdown('<p class="main-header">🎯 Financial Inclusion Projections</p>', unsafe_allow_html=True)
    
    st.markdown("### Progress Toward National Targets")
    
    if forecasts.empty:
        st.warning("No forecast data available. Please run the forecasting notebook first.")
    else:
        # Scenario selector
        scenario_choice = st.radio(
            "Select Scenario",
            ['pessimistic', 'base', 'optimistic'],
            index=1,
            format_func=lambda x: f"{x.capitalize()} Scenario",
            horizontal=True
        )
        
        scenario_forecasts = forecasts[forecasts['scenario'] == scenario_choice]
        
        # Progress bars for each target
        for _, target in targets.iterrows():
            indicator_code_part = target['indicator_code'].split('_')[-1]
            
            # Find matching forecast
            matching_forecast = None
            for code in scenario_forecasts['indicator_code'].unique():
                if indicator_code_part.lower() in code.lower():
                    matching_forecast = scenario_forecasts[
                        (scenario_forecasts['indicator_code'] == code) &
                        (scenario_forecasts['observation_date'].dt.year == 2027)
                    ]
                    break
            
            if matching_forecast is not None and not matching_forecast.empty:
                current_value = matching_forecast.iloc[0]['value_numeric']
                target_value = target['value_numeric']
                
                progress, status = calculate_progress_to_target(current_value, target_value)
                
                st.markdown(f"**{target['indicator']}**")
                
                col1, col2, col3 = st.columns([2, 1, 1])
                
                with col1:
                    st.progress(min(progress / 100, 1.0))
                
                with col2:
                    st.metric("Projected", format_metric(current_value))
                
                with col3:
                    st.metric("Target", format_metric(target_value))
                
                st.markdown(f"Status: {status}")
                st.markdown("---")
        
        # Consortium questions
        st.markdown("### 📋 Answers to Consortium's Key Questions")
        
        with st.expander("❓ What drives financial inclusion in Ethiopia?"):
            st.markdown("""
            **Key Drivers Identified:**
            
            1. **Mobile Money Platforms** (Telebirr, M-Pesa)
               - Strongest impact on account ownership and usage
               - Telebirr: +4.0pp impact on mobile money accounts
               - M-Pesa: +2.0pp additional competitive effect
            
            2. **Interoperability** (January 2024)
               - High impact on digital payment usage (+4.0pp)
               - Reduces friction and increases utility
            
            3. **Infrastructure Development**
               - 4G coverage expansion
               - Agent network growth
               - Mobile penetration increase
            
            4. **Policy Framework**
               - NBE Digital Strategy: +2.0pp long-term impact
               - Telecom liberalization enabling competition
            """)
        
        with st.expander("❓ How do events affect inclusion outcomes?"):
            st.markdown("""
            **Event Impact Analysis:**
            
            - **Product Launches**: Immediate and substantial impact (3-6 month lag)
            - **Policy Changes**: Delayed but sustained impact (12-18 month lag)
            - **Infrastructure**: Medium-term impact (3-12 month lag)
            
            **Evidence Base:**
            - Kenya M-Pesa: 15pp impact over 3 years
            - Tanzania Interoperability: 5pp impact in 1 year
            - Rwanda Digital Strategy: 3pp impact over 2 years
            """)
        
        with st.expander("❓ How will inclusion rates change in 2025-2027?"):
            st.markdown(f"""
            **Projections ({scenario_choice.capitalize()} Scenario):**
            
            Based on current trends and expected event impacts:
            """)
            
            for indicator_code in ['ACC_OWNERSHIP', 'USG_DIGITAL_PAYMENT']:
                indicator_forecast = scenario_forecasts[scenario_forecasts['indicator_code'] == indicator_code]
                
                if not indicator_forecast.empty:
                    indicator_name = observations[observations['indicator_code'] == indicator_code].iloc[0]['indicator']
                    
                    st.markdown(f"\n**{indicator_name}:**")
                    
                    for year in [2025, 2026, 2027]:
                        year_forecast = indicator_forecast[indicator_forecast['observation_date'].dt.year == year]
                        if not year_forecast.empty:
                            value = year_forecast.iloc[0]['value_numeric']
                            st.markdown(f"- {year}: {format_metric(value)}")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #7F8C8D;'>
        <p>Ethiopia Financial Inclusion Forecasting Dashboard | Data as of 2024</p>
        <p>Built with Streamlit | 10 Academy Week 10 Challenge</p>
    </div>
    """,
    unsafe_allow_html=True
)
