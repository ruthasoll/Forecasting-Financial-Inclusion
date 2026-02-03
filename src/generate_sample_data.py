"""
Generate sample data for Financial Inclusion Forecasting project.
This creates synthetic data following the unified schema described in the challenge.
"""

import pandas as pd
import numpy as np
from datetime import datetime
import os

def generate_sample_data():
    """Generate sample unified dataset with observations, events, and impact links."""
    
    # ==================== OBSERVATIONS ====================
    observations = []
    
    # Account Ownership (Access) - Global Findex data
    account_ownership_data = [
        ('2011-06-30', 'Account Ownership Rate', 'ACC_OWNERSHIP', 14.0, 'observation', 'Banking', 
         'World Bank Global Findex', 'https://www.worldbank.org/globalfindex', 'high'),
        ('2014-06-30', 'Account Ownership Rate', 'ACC_OWNERSHIP', 22.0, 'observation', 'Banking',
         'World Bank Global Findex', 'https://www.worldbank.org/globalfindex', 'high'),
        ('2017-06-30', 'Account Ownership Rate', 'ACC_OWNERSHIP', 35.0, 'observation', 'Banking',
         'World Bank Global Findex', 'https://www.worldbank.org/globalfindex', 'high'),
        ('2021-06-30', 'Account Ownership Rate', 'ACC_OWNERSHIP', 46.0, 'observation', 'Banking',
         'World Bank Global Findex', 'https://www.worldbank.org/globalfindex', 'high'),
        ('2024-06-30', 'Account Ownership Rate', 'ACC_OWNERSHIP', 49.0, 'observation', 'Banking',
         'World Bank Global Findex', 'https://www.worldbank.org/globalfindex', 'high'),
    ]
    
    # Mobile Money Account Ownership
    mobile_money_data = [
        ('2014-06-30', 'Mobile Money Account', 'ACC_MM_ACCOUNT', 1.5, 'observation', 'Digital Payments',
         'World Bank Global Findex', 'https://www.worldbank.org/globalfindex', 'high'),
        ('2017-06-30', 'Mobile Money Account', 'ACC_MM_ACCOUNT', 4.7, 'observation', 'Digital Payments',
         'World Bank Global Findex', 'https://www.worldbank.org/globalfindex', 'high'),
        ('2021-06-30', 'Mobile Money Account', 'ACC_MM_ACCOUNT', 4.7, 'observation', 'Digital Payments',
         'World Bank Global Findex', 'https://www.worldbank.org/globalfindex', 'high'),
        ('2024-06-30', 'Mobile Money Account', 'ACC_MM_ACCOUNT', 9.45, 'observation', 'Digital Payments',
         'World Bank Global Findex', 'https://www.worldbank.org/globalfindex', 'high'),
    ]
    
    # Digital Payment Usage
    digital_payment_data = [
        ('2017-06-30', 'Digital Payment Usage', 'USG_DIGITAL_PAYMENT', 15.0, 'observation', 'Digital Payments',
         'World Bank Global Findex', 'https://www.worldbank.org/globalfindex', 'high'),
        ('2021-06-30', 'Digital Payment Usage', 'USG_DIGITAL_PAYMENT', 25.0, 'observation', 'Digital Payments',
         'World Bank Global Findex', 'https://www.worldbank.org/globalfindex', 'high'),
        ('2024-06-30', 'Digital Payment Usage', 'USG_DIGITAL_PAYMENT', 35.0, 'observation', 'Digital Payments',
         'World Bank Global Findex', 'https://www.worldbank.org/globalfindex', 'high'),
    ]
    
    # Telebirr Users (Registered)
    telebirr_data = [
        ('2021-05-15', 'Telebirr Users', 'MM_TELEBIRR_USERS', 0.0, 'observation', 'Digital Payments',
         'Ethio Telecom', 'https://www.ethiotelecom.et', 'high'),
        ('2022-06-30', 'Telebirr Users', 'MM_TELEBIRR_USERS', 20.0, 'observation', 'Digital Payments',
         'Ethio Telecom', 'https://www.ethiotelecom.et', 'high'),
        ('2023-06-30', 'Telebirr Users', 'MM_TELEBIRR_USERS', 34.3, 'observation', 'Digital Payments',
         'Ethio Telecom', 'https://www.ethiotelecom.et', 'high'),
        ('2024-06-30', 'Telebirr Users', 'MM_TELEBIRR_USERS', 54.84, 'observation', 'Digital Payments',
         'Ethio Telecom', 'https://www.ethiotelecom.et', 'high'),
    ]
    
    # M-Pesa Users
    mpesa_data = [
        ('2023-08-10', 'M-Pesa Users', 'MM_MPESA_USERS', 0.0, 'observation', 'Digital Payments',
         'Safaricom Ethiopia', 'https://www.safaricom.et', 'high'),
        ('2024-03-31', 'M-Pesa Users', 'MM_MPESA_USERS', 3.1, 'observation', 'Digital Payments',
         'Safaricom Ethiopia', 'https://www.safaricom.et', 'high'),
        ('2024-06-30', 'M-Pesa Users', 'MM_MPESA_USERS', 4.5, 'observation', 'Digital Payments',
         'Safaricom Ethiopia', 'https://www.safaricom.et', 'high'),
        ('2024-12-31', 'M-Pesa Users', 'MM_MPESA_USERS', 10.8, 'observation', 'Digital Payments',
         'Safaricom Ethiopia', 'https://www.safaricom.et', 'medium'),
    ]
    
    # Infrastructure data
    infrastructure_data = [
        ('2017-12-31', 'Mobile Penetration', 'INF_MOBILE_PEN', 44.0, 'observation', 'Infrastructure',
         'ITU', 'https://www.itu.int', 'high'),
        ('2021-12-31', 'Mobile Penetration', 'INF_MOBILE_PEN', 52.0, 'observation', 'Infrastructure',
         'ITU', 'https://www.itu.int', 'high'),
        ('2024-12-31', 'Mobile Penetration', 'INF_MOBILE_PEN', 58.0, 'observation', 'Infrastructure',
         'ITU', 'https://www.itu.int', 'medium'),
        ('2017-12-31', '4G Coverage', 'INF_4G_COVERAGE', 25.0, 'observation', 'Infrastructure',
         'GSMA', 'https://www.gsma.com', 'medium'),
        ('2021-12-31', '4G Coverage', 'INF_4G_COVERAGE', 45.0, 'observation', 'Infrastructure',
         'GSMA', 'https://www.gsma.com', 'medium'),
        ('2024-12-31', '4G Coverage', 'INF_4G_COVERAGE', 65.0, 'observation', 'Infrastructure',
         'GSMA', 'https://www.gsma.com', 'medium'),
    ]
    
    # Combine all observations
    all_obs = (account_ownership_data + mobile_money_data + digital_payment_data + 
               telebirr_data + mpesa_data + infrastructure_data)
    
    for i, obs in enumerate(all_obs, 1):
        observations.append({
            'record_id': f'OBS_{i:03d}',
            'record_type': obs[4],
            'pillar': obs[5],
            'indicator': obs[1],
            'indicator_code': obs[2],
            'value_numeric': obs[3],
            'observation_date': obs[0],
            'source_type': 'survey' if 'Findex' in obs[6] else 'operator',
            'source_name': obs[6],
            'source_url': obs[7],
            'confidence': obs[8],
            'collected_by': 'Data Team',
            'collection_date': '2026-02-01'
        })
    
    # ==================== EVENTS ====================
    events = [
        {
            'record_id': 'EVT_001',
            'record_type': 'event',
            'pillar': '',  # Events don't have pillars assigned
            'category': 'product_launch',
            'indicator': 'Telebirr Launch',
            'observation_date': '2021-05-15',
            'source_name': 'Ethio Telecom Press Release',
            'source_url': 'https://www.ethiotelecom.et',
            'confidence': 'high',
            'original_text': 'Telebirr mobile money service launched',
            'notes': 'Major mobile money platform launch by state telecom'
        },
        {
            'record_id': 'EVT_002',
            'record_type': 'event',
            'pillar': '',
            'category': 'policy',
            'indicator': 'Telecom Liberalization',
            'observation_date': '2022-08-10',
            'source_name': 'National Bank of Ethiopia',
            'source_url': 'https://nbe.gov.et',
            'confidence': 'high',
            'original_text': 'Safaricom awarded telecom license',
            'notes': 'First private telecom operator license'
        },
        {
            'record_id': 'EVT_003',
            'record_type': 'event',
            'pillar': '',
            'category': 'product_launch',
            'indicator': 'M-Pesa Launch',
            'observation_date': '2023-08-10',
            'source_name': 'Safaricom Ethiopia',
            'source_url': 'https://www.safaricom.et',
            'confidence': 'high',
            'original_text': 'M-Pesa Ethiopia officially launched',
            'notes': 'Second major mobile money platform'
        },
        {
            'record_id': 'EVT_004',
            'record_type': 'event',
            'pillar': '',
            'category': 'infrastructure',
            'indicator': 'EthSwitch Interoperability',
            'observation_date': '2024-01-15',
            'source_name': 'EthSwitch',
            'source_url': 'https://www.ethswitch.com',
            'confidence': 'high',
            'original_text': 'P2P interoperability enabled',
            'notes': 'Cross-platform transfers enabled'
        },
        {
            'record_id': 'EVT_005',
            'record_type': 'event',
            'pillar': '',
            'category': 'policy',
            'indicator': 'NBE Digital Strategy',
            'observation_date': '2023-03-01',
            'source_name': 'National Bank of Ethiopia',
            'source_url': 'https://nbe.gov.et',
            'confidence': 'high',
            'original_text': 'National Digital Financial Services Strategy launched',
            'notes': 'Government commitment to digital finance'
        },
    ]
    
    # ==================== TARGETS ====================
    targets = [
        {
            'record_id': 'TGT_001',
            'record_type': 'target',
            'pillar': 'Banking',
            'indicator': 'Account Ownership Target',
            'indicator_code': 'TGT_ACC_OWNERSHIP',
            'value_numeric': 60.0,
            'observation_date': '2027-12-31',
            'source_name': 'NFIS-II',
            'source_url': 'https://nbe.gov.et',
            'confidence': 'high',
            'notes': 'National Financial Inclusion Strategy II target'
        },
        {
            'record_id': 'TGT_002',
            'record_type': 'target',
            'pillar': 'Digital Payments',
            'indicator': 'Digital Payment Target',
            'indicator_code': 'TGT_DIGITAL_PAYMENT',
            'value_numeric': 50.0,
            'observation_date': '2027-12-31',
            'source_name': 'NFIS-II',
            'source_url': 'https://nbe.gov.et',
            'confidence': 'high',
            'notes': 'Digital payment adoption target'
        },
    ]
    
    # Combine all data records
    all_data = observations + events + targets
    df_data = pd.DataFrame(all_data)
    
    # ==================== IMPACT LINKS ====================
    impact_links = [
        {
            'link_id': 'IMP_001',
            'parent_id': 'EVT_001',  # Telebirr Launch
            'pillar': 'Digital Payments',
            'indicator': 'ACC_MM_ACCOUNT',
            'related_indicator': 'Mobile Money Account',
            'impact_direction': 'positive',
            'impact_magnitude': 'high',
            'impact_estimate': 4.0,  # Estimated +4pp impact
            'lag_months': 6,
            'evidence_basis': 'comparable',
            'evidence_source': 'Kenya M-Pesa launch impact',
            'confidence': 'medium',
            'notes': 'Based on M-Pesa Kenya growth trajectory'
        },
        {
            'link_id': 'IMP_002',
            'parent_id': 'EVT_001',  # Telebirr Launch
            'pillar': 'Digital Payments',
            'indicator': 'USG_DIGITAL_PAYMENT',
            'related_indicator': 'Digital Payment Usage',
            'impact_direction': 'positive',
            'impact_magnitude': 'medium',
            'impact_estimate': 5.0,  # +5pp
            'lag_months': 12,
            'evidence_basis': 'comparable',
            'evidence_source': 'Kenya M-Pesa usage patterns',
            'confidence': 'medium',
            'notes': 'Usage typically lags account opening'
        },
        {
            'link_id': 'IMP_003',
            'parent_id': 'EVT_003',  # M-Pesa Launch
            'pillar': 'Digital Payments',
            'indicator': 'ACC_MM_ACCOUNT',
            'related_indicator': 'Mobile Money Account',
            'impact_direction': 'positive',
            'impact_magnitude': 'medium',
            'impact_estimate': 2.0,  # +2pp
            'lag_months': 6,
            'evidence_basis': 'market',
            'evidence_source': 'Competitive market dynamics',
            'confidence': 'medium',
            'notes': 'Second entrant typically has lower initial impact'
        },
        {
            'link_id': 'IMP_004',
            'parent_id': 'EVT_003',  # M-Pesa Launch
            'pillar': 'Digital Payments',
            'indicator': 'USG_DIGITAL_PAYMENT',
            'related_indicator': 'Digital Payment Usage',
            'impact_direction': 'positive',
            'impact_magnitude': 'medium',
            'impact_estimate': 3.0,  # +3pp
            'lag_months': 12,
            'evidence_basis': 'market',
            'evidence_source': 'Competition drives usage',
            'confidence': 'medium',
            'notes': 'Competition increases overall market activity'
        },
        {
            'link_id': 'IMP_005',
            'parent_id': 'EVT_004',  # Interoperability
            'pillar': 'Digital Payments',
            'indicator': 'USG_DIGITAL_PAYMENT',
            'related_indicator': 'Digital Payment Usage',
            'impact_direction': 'positive',
            'impact_magnitude': 'high',
            'impact_estimate': 4.0,  # +4pp
            'lag_months': 3,
            'evidence_basis': 'comparable',
            'evidence_source': 'Tanzania interoperability impact',
            'confidence': 'high',
            'notes': 'Interoperability significantly increases usage'
        },
        {
            'link_id': 'IMP_006',
            'parent_id': 'EVT_004',  # Interoperability
            'pillar': 'Banking',
            'indicator': 'ACC_OWNERSHIP',
            'related_indicator': 'Account Ownership Rate',
            'impact_direction': 'positive',
            'impact_magnitude': 'low',
            'impact_estimate': 1.5,  # +1.5pp
            'lag_months': 6,
            'evidence_basis': 'comparable',
            'evidence_source': 'Reduced barriers to entry',
            'confidence': 'low',
            'notes': 'Easier switching may encourage new users'
        },
        {
            'link_id': 'IMP_007',
            'parent_id': 'EVT_005',  # NBE Digital Strategy
            'pillar': 'Banking',
            'indicator': 'ACC_OWNERSHIP',
            'related_indicator': 'Account Ownership Rate',
            'impact_direction': 'positive',
            'impact_magnitude': 'medium',
            'impact_estimate': 2.0,  # +2pp
            'lag_months': 18,
            'evidence_basis': 'policy',
            'evidence_source': 'Government commitment signal',
            'confidence': 'low',
            'notes': 'Policy impact is indirect and delayed'
        },
        {
            'link_id': 'IMP_008',
            'parent_id': 'EVT_002',  # Telecom Liberalization
            'pillar': 'Digital Payments',
            'indicator': 'ACC_MM_ACCOUNT',
            'related_indicator': 'Mobile Money Account',
            'impact_direction': 'positive',
            'impact_magnitude': 'low',
            'impact_estimate': 1.0,  # +1pp
            'lag_months': 12,
            'evidence_basis': 'market',
            'evidence_source': 'Market preparation for competition',
            'confidence': 'low',
            'notes': 'License award precedes actual service launch'
        },
    ]
    
    df_impacts = pd.DataFrame(impact_links)
    
    return df_data, df_impacts

def save_to_excel(df_data, df_impacts, output_path):
    """Save dataframes to Excel with multiple sheets."""
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        df_data.to_excel(writer, sheet_name='ethiopia_fi_unified_data', index=False)
        df_impacts.to_excel(writer, sheet_name='impact_links', index=False)
    print(f"Sample data saved to: {output_path}")

if __name__ == "__main__":
    # Generate data
    df_data, df_impacts = generate_sample_data()
    
    # Create output directory
    output_dir = 'data/raw'
    os.makedirs(output_dir, exist_ok=True)
    
    # Save to Excel
    output_path = os.path.join(output_dir, 'ethiopia_fi_unified_data.xlsx')
    save_to_excel(df_data, df_impacts, output_path)
    
    # Print summary
    print(f"\nData Summary:")
    print(f"Total records: {len(df_data)}")
    print(f"  - Observations: {len(df_data[df_data['record_type'] == 'observation'])}")
    print(f"  - Events: {len(df_data[df_data['record_type'] == 'event'])}")
    print(f"  - Targets: {len(df_data[df_data['record_type'] == 'target'])}")
    print(f"Impact links: {len(df_impacts)}")
