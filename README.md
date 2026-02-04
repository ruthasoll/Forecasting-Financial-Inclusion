# Forecasting Financial Inclusion in Ethiopia

## Project Overview
This project builds a comprehensive forecasting system for Ethiopia's digital financial transformation using time-series analysis and event impact modeling to predict key financial inclusion metrics (Access and Usage) for 2025-2027.

The solution addresses three core questions from the consortium:
1. What drives financial inclusion in Ethiopia?
2. How do events (policies, product launches, infrastructure) affect inclusion outcomes?
3. How will financial inclusion rates change in 2025-2027?

---

## 🚀 Quick Start

### 1. Setup Environment
```bash
# Create virtual environment
python -m venv .venv

# Activate (Windows)
.\.venv\Scripts\activate

# Activate (Mac/Linux)
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Generate Sample Data
```bash
python src/generate_sample_data.py
```

### 3. Run Analysis Notebooks
```bash
# Task 3: Event Impact Modeling
jupyter notebook notebooks/task_3_event_impact_modeling.ipynb

# Task 4: Forecasting
jupyter notebook notebooks/task_4_forecasting.ipynb
```

### 4. Launch Interactive Dashboard
```bash
streamlit run dashboard/app.py
```

---

## 📋 Project Structure

```
ethiopia-fi-forecast/
├── data/
│   ├── raw/                          # Source data (gitignored)
│   │   └── ethiopia_fi_unified_data.xlsx
│   └── processed/                    # Analysis outputs
│       ├── impact_matrix.csv
│       └── task4_forecasts_2025_2027.csv
├── notebooks/
│   ├── task_3_event_impact_modeling.ipynb
│   ├── task_4_forecasting.ipynb
│   └── 01_analysis_walkthrough.ipynb
├── src/
│   ├── loader.py                     # Data loading module
│   ├── impact_model.py               # Event impact modeling
│   ├── scenarios.py                  # Scenario generation
│   ├── forecast.py                   # Forecasting engine
│   └── generate_sample_data.py       # Sample data generator
├── dashboard/
│   ├── app.py                        # Main Streamlit app
│   └── utils.py                      # Dashboard utilities
├── reports/
│   └── figures/                      # Generated visualizations
├── tests/
│   └── __init__.py
├── requirements.txt
└── README.md
```

---

## 📊 Task 3: Event Impact Modeling

### Objective
Model how events (policies, product launches, infrastructure investments) affect financial inclusion indicators.

### Implementation
- **Impact Model Module** (`src/impact_model.py`):
  - `build_impact_matrix()`: Creates event-indicator association matrix
  - `validate_impact_model()`: Compares predicted vs. observed outcomes
  - `apply_comparable_evidence()`: Incorporates Kenya/Tanzania/Rwanda evidence
  - `calculate_cumulative_impact()`: Sums effects of multiple events

- **Analysis Notebook** (`notebooks/task_3_event_impact_modeling.ipynb`):
  - Event-indicator association matrix with heatmap visualization
  - Comparable country evidence (Kenya M-Pesa, Tanzania interoperability)
  - Historical validation against Telebirr and M-Pesa launches
  - Cumulative impact analysis

### Key Findings
- **Telebirr Launch** (May 2021): +4.0pp impact on mobile money accounts
- **M-Pesa Launch** (Aug 2023): +2.0pp competitive effect
- **Interoperability** (Jan 2024): +4.0pp impact on digital payment usage
- **NBE Digital Strategy**: +2.0pp long-term policy impact

### Outputs
- `reports/figures/task3_impact_matrix_heatmap.png`
- `reports/figures/task3_cumulative_impact.png`
- `reports/task3_impact_summary.csv`
- `data/processed/impact_matrix.csv`

---

## 🔮 Task 4: Forecasting Access and Usage

### Objective
Forecast Account Ownership (Access) and Digital Payment Usage for 2025-2027 with scenario analysis and confidence intervals.

### Implementation
- **Scenarios Module** (`src/scenarios.py`):
  - `generate_base_scenario()`: Expected event impacts
  - `generate_optimistic_scenario()`: 30% higher impacts
  - `generate_pessimistic_scenario()`: 30% lower impacts
  - `calculate_confidence_intervals()`: Statistical uncertainty bounds

- **Forecasting Notebook** (`notebooks/task_4_forecasting.ipynb`):
  - Historical trend analysis with CAGR calculations
  - Baseline forecasts using linear regression
  - Three-scenario analysis incorporating event impacts
  - Confidence intervals based on historical variance
  - Key drivers analysis and uncertainty quantification

### Forecasting Approach
1. **Baseline**: Linear trend extrapolation from historical data
2. **Event-Augmented**: Baseline + impact estimates from Task 3
3. **Scenarios**: Optimistic/Base/Pessimistic with varying impact magnitudes
4. **Uncertainty**: 95% confidence intervals using t-distribution

### Key Projections (Base Scenario)
- **Account Ownership**: Forecasted trajectory toward 60% target by 2027
- **Digital Payment Usage**: Growth driven by interoperability and competition
- **Scenario Range**: ±3-5 percentage points between optimistic and pessimistic

### Outputs
- `reports/figures/task4_historical_trends.png`
- `reports/figures/task4_scenario_forecasts.png`
- `reports/task4_forecast_summary.csv`
- `data/processed/task4_forecasts_2025_2027.csv`

---

## 📱 Task 5: Interactive Dashboard

### Objective
Create an interactive Streamlit dashboard for exploring data, trends, forecasts, and projections.

### Features

#### 🏠 Overview Page
- Key metrics summary cards (Account Ownership, Mobile Money, Digital Payments)
- Growth highlights (Telebirr, M-Pesa)
- Interactive event timeline
- Data download functionality

#### 📈 Trends Analysis Page
- Interactive time series charts with event overlays
- Multi-indicator comparison
- Date range filters
- Data table views

#### 🔮 Forecasts Page
- Scenario visualization with confidence intervals
- 2027 scenario comparison (Optimistic/Base/Pessimistic)
- Key projected milestones
- Target gap analysis

#### 🎯 Inclusion Projections Page
- Progress bars toward 2027 targets
- Scenario selector
- Answers to consortium's key questions:
  - What drives financial inclusion?
  - How do events affect outcomes?
  - How will rates change in 2025-2027?

### Running the Dashboard
```bash
streamlit run dashboard/app.py
```

Access at: `http://localhost:8501`

---

## 📈 Data Schema

### Unified Data Structure
All records share the same schema with `record_type` indicating interpretation:

- **observation**: Measured values (Findex surveys, operator reports)
- **event**: Policies, product launches, market entries
- **target**: Official policy goals (NFIS-II targets)

### Impact Links
Separate sheet connecting events to indicators:
- `parent_id`: Links to event record
- `indicator`: Affected indicator code
- `impact_estimate`: Magnitude in percentage points
- `lag_months`: Delay before impact occurs
- `evidence_basis`: Source of estimate (comparable/market/policy)

---

## 🔬 Methodology

### Event Impact Modeling
- **Functional Form**: Step change model (impact persists after lag)
- **Evidence Sources**: Comparable countries (Kenya, Tanzania, Rwanda)
- **Validation**: Historical pre/post analysis where data available
- **Assumptions**: Additive impacts, fixed lags, no decay

### Forecasting
- **Baseline**: Linear regression on historical Findex data
- **Event Adjustment**: Add impact estimates with appropriate lags
- **Scenarios**: Vary impact magnitudes (±30%)
- **Confidence Intervals**: Based on historical variance, t-distribution

### Limitations
- Limited historical data points (Findex every 3 years)
- Recent events lack validation data
- Active vs. registered account gap not fully modeled
- Macroeconomic factors not included
- Comparable evidence may not fully transfer

---

## 📚 Key Data Sources

- **World Bank Global Findex**: Account ownership, digital payment usage
- **Ethio Telecom**: Telebirr user statistics
- **Safaricom Ethiopia**: M-Pesa adoption data
- **National Bank of Ethiopia**: Policy documents, targets
- **GSMA, ITU**: Infrastructure data (4G coverage, mobile penetration)

---

## 🧪 Testing

### Run Unit Tests
```bash
pytest tests/ -v
```

### Validate Notebooks
```bash
pytest --nbmake notebooks/task_3_event_impact_modeling.ipynb
pytest --nbmake notebooks/task_4_forecasting.ipynb
```

---

## 📦 Dependencies

Core libraries:
- `pandas>=2.0.0`: Data manipulation
- `numpy>=1.24.0`: Numerical computing
- `scikit-learn>=1.3.0`: Machine learning (regression)
- `scipy>=1.11.0`: Statistical functions
- `matplotlib>=3.7.0`: Static visualizations
- `seaborn>=0.12.0`: Statistical plotting
- `plotly>=5.17.0`: Interactive charts
- `streamlit>=1.28.0`: Dashboard framework
- `openpyxl>=3.1.0`: Excel file handling

---

## 🌟 Key Insights

1. **Mobile money platforms** (Telebirr, M-Pesa) are the strongest drivers of financial inclusion
2. **Interoperability** significantly boosts digital payment usage
3. **Policy impacts** are delayed (12-18 months) but sustained
4. **Competition** between providers accelerates market growth
5. **Infrastructure** (4G, agents) enables but doesn't guarantee adoption

---

## 👥 Contributors

- **Data Team**: Data collection and enrichment
- **Analytics Team**: Modeling and forecasting
- **Development Team**: Dashboard implementation

---

## 📄 License

This project is part of the 10 Academy AI Mastery Program - Week 10 Challenge.

---

## 🔗 References

- [World Bank Global Findex](https://www.worldbank.org/globalfindex)
- [National Bank of Ethiopia](https://nbe.gov.et)
- [Ethio Telecom](https://www.ethiotelecom.et)
- [Safaricom Ethiopia](https://www.safaricom.et)
- Suri & Jack (2016): "The Long-Run Poverty and Gender Impacts of Mobile Money"
