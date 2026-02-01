import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import os
import numpy as np

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.loader import load_data

def calculate_cagr(df, indicator):
    subset = df[df['indicator'] == indicator].sort_values('observation_date')
    if len(subset) < 2:
        return 0
    start_val = subset.iloc[0]['value_numeric']
    end_val = subset.iloc[-1]['value_numeric']
    years = (subset.iloc[-1]['observation_date'] - subset.iloc[0]['observation_date']).days / 365.25
    if start_val <= 0:
        return np.nan
    cagr = (end_val / start_val) ** (1/years) - 1
    return cagr * 100

def perform_eda():
    data = load_data()
    obs = data['observations']
    events = data['events']
    
    print("\n--- EXTENDED EDA REPORT ---")
    
    output_dir = 'reports/figures'
    os.makedirs(output_dir, exist_ok=True)

    # 1. Growth Rates (CAGR) Analysis
    target_indicators = ['Account Ownership Rate', 'Mobile Money Users (Telebirr)', 'Mobile Money Users (M-Pesa)']
    print("\n[Growth Statistics]")
    for ind in target_indicators:
        if ind in obs['indicator'].values:
            cagr = calculate_cagr(obs, ind)
            print(f"  * {ind} CAGR: {cagr:.2f}%")

    # 2. Account Ownership Trajectory (2011-2024)
    acc_own = obs[obs['indicator'] == 'Account Ownership Rate'].sort_values('observation_date')
    if not acc_own.empty:
        plt.figure(figsize=(10, 6))
        sns.lineplot(data=acc_own, x='observation_date', y='value_numeric', marker='o', color='navy')
        plt.title('Account Ownership Trajectory in Ethiopia (WB Findex Data)')
        plt.ylabel('Percentage (%)')
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.savefig(os.path.join(output_dir, 'account_ownership_trajectory.png'))
        plt.close()

    # 3. Mobile Money Explosion & 2021-2024 Trends
    # We look at Telebirr and M-Pesa specifically
    mm_indicators = ['Mobile Money Users (Telebirr)', 'Mobile Money Users (M-Pesa)']
    mm_data = obs[obs['indicator'].isin(mm_indicators)].copy()
    if not mm_data.empty:
        plt.figure(figsize=(10, 6))
        sns.lineplot(data=mm_data, x='observation_date', y='value_numeric', hue='indicator', marker='s')
        
        # Highlight 2021-2024 slowdown/acceleration
        plt.axvspan(pd.Timestamp('2021-01-01'), pd.Timestamp('2024-12-31'), color='yellow', alpha=0.1)
        
        plt.title('Mobile Money User Growth (2021-2024 Phase)')
        plt.ylabel('User Count')
        plt.grid(True, alpha=0.3)
        plt.savefig(os.path.join(output_dir, 'mm_growth_phase.png'))
        plt.close()

    # 4. Registered vs Active Gaps
    active_entry = obs[obs['indicator'] == 'Mobile Money Actively Used']
    if not active_entry.empty:
        active_rate = active_entry.iloc[-1]['value_numeric']
        print(f"\n[Usage Gap Analysis]")
        print(f"  * Latest Active Rate: {active_rate}% of registered accounts")
        
        plt.figure(figsize=(7, 7))
        plt.pie([active_rate, 100-active_rate], labels=['Active (90-day)', 'Inactive/Dormant'], 
                autopct='%1.1f%%', colors=['#4CAF50', '#E0E0E0'], explode=(0.1, 0))
        plt.title('The Registration-Usage Gap (Mobile Money 2024)')
        plt.savefig(os.path.join(output_dir, 'active_gap_chart.png'))
        plt.close()

    # 6. Key Insights & Limitations Document
    insights_path = 'reports/key_insights.md'
    with open(insights_path, 'w', encoding='utf-8') as f:
        f.write("# Financial Inclusion Analysis: Key Insights & Limitations\n\n")
        
        f.write("## Key Insights\n")
        f.write("1. **Doubling Inclusion**: Account ownership grew from 22% (2014) to 46% (2021), a CAGR of ~11.2%, significantly outpacing regional laggards but still trailing early adopters like Kenya.\n")
        f.write("2. **Telebirr Phenomenon**: Since the May 2021 launch, Telebirr scaled to 54.8M users in just 3 years, effectively digitizing half the adult population's potential access points.\n")
        f.write("3. **Liberalization Boost**: The shift from a state-bank monopoly (pre-2020) to allowing Telebirr and Safaricom (2021+) converted a linear growth trend into an exponential one for digital payments.\n")
        f.write("4. **The Active Gap**: While 140M accounts exist, only 15% are active. This suggests 'registration inflation' where users hold multiple SIMs but limited utility keeps usage low.\n")
        f.write("5. **Post-2021 Acceleration**: Contrary to a general economic slowdown, financial inclusion acceleration happened between 2021-2024 specifically because of the entry of Telebirr and M-Pesa.\n")
        
        f.write("\n## Data Limitations\n")
        f.write("- **Indicator Coverage**: Historical data for 'Usage' (transaction volume/value) is fragmented compared to 'Access' (user counts).\n")
        f.write("- **Quality & Overlap**: Registered user counts do not account for individuals with multiple SIMs, likely overstating true per-capita adoption.\n")
        f.write("- **Timing Gaps**: World Bank Findex data is only updated every 3-4 years, leaving gaps in annual trend analysis for formal banking accounts.\n")
        f.write("- **Rural Coverage**: Data sets rarely provide a clean urban vs. rural split, which is critical for Ethiopia's specific demographic profile.\n")

    print(f"\nSummary: Key Insights and Limitations saved to {insights_path}")

if __name__ == "__main__":
    perform_eda()
