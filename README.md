# Forecasting Financial Inclusion in Ethiopia

## Project Overview
This project aims to build a forecasting system for Ethiopia's digital financial transformation. It utilizes time-series analysis and event impact modeling to predict key financial inclusion metrics (Access and Usage) for the years 2025-2027.

The solution is divided into modular tasks, focusing on robust data pipelines, exploratory analysis, and scenario-based forecasting.

---

## 🚀 Task 1: Data Understanding & Exploratory Data Analysis (EDA)

### Objective
To load, clean, and understand the historical financial inclusion data and identifying key trends and data quality issues.

### Implementation
- **Data Loader (`src/loader.py`)**: A reusable module created to ingest the raw Excel data `ethiopia_fi_unified_data.xlsx`. It splits the data into logical components:
    - `observations`: Historical time-series data (e.g., Account Ownership, Digital Payments).
    - `events`: Policy/Market events (e.g., "M-Pesa License", "NBE Directive").
    - `impacts`: Definitions of how events affect specific indicators.
- **EDA Script (`src/eda.py`)**: An automated analysis script that:
    - Summarizes dataset statistics (time range, missing values).
    - Generates time-series plots overlaying historical data points.
    - Saves visual outputs to `reports/figures/`.
- **Inspection (`src/inspect_data.py`)**: A utility to inspect the raw Excel structure and sheet names to ensure robust loading.

### Key Outputs
- Validated dataset with separated event and observation streams.
- Visualization of historical trends (`reports/figures/eda_timeseries.png`).

---

## 📈 Task 2: Modeling & Forecasting (Event Impact Model)

### Objective
To forecast financial inclusion indicators for 2025-2028, incorporating both historical trends and the expected impact of future simulated events (policy changes, market entry).

### Implementation
- **Forecasting Engine (`src/forecast.py`)**:
    1.  **Baseline Forecast**: Uses Linear Regression on historical data to project a "Business as Usual" trend for 2025-2028.
    2.  **Event Impact Adjustment**: Applies specific adjustments to the baseline based on defined events.
        - *Logic*: If an event (e.g., "New Interoperability Law") occurs in 2025, the model looks up its "Impact Estimate" (e.g., +5%) and applies this magnitude to the forecast for all subsequent periods.
    3.  **Output**: Saves the combined forecast (Baseline + Adjusted) to `data/processed/forecast_results.csv`.

- **Interactive Dashboard (`dashboard/app.py`)**:
    - Built with **Streamlit** and **Plotly**.
    - Allows users to select an indicator (e.g., "Account Ownership Rate").
    - Visualizes the Historical Data vs. Baseline Forecast vs. Adjusted Forecast.
    - Displays Event markers on the timeline to correlate policy changes with projections.

---

## 📂 Unified Data Schema

To maintain consistency across diverse data sources (World Bank, NBE, Ethio Telecom), we utilize a **Unified Schema**.

### Record Types
- **`observation`**: A specific data point measured at a point in time (e.g., Account Ownership %).
- **`event`**: A significant milestone or policy launch (e.g., "M-Pesa License Awarded").
- **`target`**: Official government or organizational goals (e.g., "NBE 2025 Goal of 70% Inclusion").
- **`impact_link`**: (Defined in sheets) Connects an **Event** to an **Indicator** with an `impact_magnitude` and `lag_months`.

### Data Pillars
- **Banking**: Formal accounts and traditional financial services.
- **Digital Payments**: Mobile money, wallet adoption, and digital transaction rates.
- **Regulation**: Policy shifts, directives, and licensing events.

---

## 💻 How to Run

### 1. Setup Environment
Ensure you have Python 3.10+ installed.
```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .\.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Run Analysis & Forecasting Pipeline
```bash
# Step 1: Run EDA to generate plots
python src/eda.py

# Step 2: Generate Forecasts (saves to data/processed/)
python src/forecast.py
```

### 3. Launch Dashboard
To interactively explore the results:
```bash
streamlit run dashboard/app.py
```

### 4. Notebook Walkthrough
For a step-by-step code walkthrough, open the notebook:
```bash
jupyter notebook notebooks/01_analysis_walkthrough.ipynb
```