# Sales & Demand Forecasting using Time-Series Analysis

## Overview and problem statement

This BTech mini project transforms retail invoices into a daily sales series, studies historical patterns, evaluates forecasting models, and predicts the next 30 days. Transaction-level data is difficult to inspect manually; the dashboard provides charts and a simple forecast to support demand-planning discussion.

## Features

- Documented cleaning of UCI-style retail transactions
- Daily and monthly sales analysis, top products, country sales, rolling average, and decomposition
- Chronological train/test split
- Naive baseline, ARIMA, and weekly SARIMA comparison using MAE, RMSE, and MAPE
- 30-day future forecast and Streamlit dashboard
- Clear error messages for missing or invalid datasets

## Dataset

Use the UCI Online Retail dataset; download and placement instructions are in [data/README.md](data/README.md). The included `sample_sales_data.csv` is synthetic testing data and must not be described as real retail data.

## Technologies

Python, Pandas, NumPy, Matplotlib, Plotly, statsmodels, scikit-learn, Streamlit, and openpyxl.

## Structure

```text
sales-demand-forecasting/
├── data/                 # UCI instructions and synthetic demo data
├── src/                  # preprocessing, EDA, forecasting, evaluation
├── outputs/              # generated data, figures, metrics, forecasts
├── app.py                # Streamlit dashboard
├── main.py               # complete analysis pipeline
├── PROJECT_PLAN.md       # implementation plan
├── SYNOPSIS.md           # submission synopsis
├── PROJECT_REPORT.md     # report draft
└── VIVA_QUESTIONS.md     # viva preparation
```

## Installation

```powershell
cd sales-demand-forecasting
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Run with included testing data

```powershell
python data/create_sample_data.py
python main.py
streamlit run app.py
```

## Run with UCI data

Place `Online Retail.xlsx` inside `data/`, then run:

```powershell
python main.py --input "data/Online Retail.xlsx"
streamlit run app.py
```

## Model explanation and evaluation

The Naive baseline repeats the final training value. ARIMA(1,1,1) models recent observations after one differencing step. SARIMA adds weekly seasonality (`s=7`) for daily data. The program chooses the lowest MAE only after evaluating on the newest chronological test period. MAE is average absolute error, RMSE gives greater weight to large errors, and MAPE is percentage error (with zero actual values excluded).

## Expected output

After `main.py`, look in `outputs/` for cleaned data, daily sales, six figures, ADF results, `model_comparison.csv`, and `future_forecast.csv`.

## Limitations and future scope

The analysis forecasts total daily sales and does not account for promotions, holidays, price changes, or stock availability. Extensions can add product-level models, external variables, and more advanced model selection.
