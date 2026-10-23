# Project Plan

## Objective
Analyse historical retail transactions, construct a daily sales time series, compare forecasting models, and predict the next 30 days of sales through a Streamlit dashboard.

## Planned workflow

1. **Dataset:** use UCI Online Retail where available; otherwise use the included clearly labelled synthetic dataset for testing.
2. **Preprocessing:** validate required columns, convert invoice date, exclude cancellations and non-positive quantity/price, create `SalesAmount`, aggregate daily sales, and fill dates without sales with zero.
3. **EDA:** inspect shape, data types, missing values, totals, products, customers, countries, monthly sales, and daily sales.
4. **Time series:** plot trend, rolling average, weekly decomposition, and run an explained ADF stationarity check.
5. **Split:** keep chronological order; use the first 85% of days for training and the latest 15% for testing.
6. **Models:** Naive baseline, ARIMA(1,1,1), and SARIMAX(1,1,1)x(1,0,1,7). Weekly seasonality is used because the series is daily and its weekly pattern is visible in the demo data.
7. **Evaluation:** compare MAE, RMSE, and MAPE. MAPE excludes zero actual values to avoid division by zero.
8. **Forecast:** select the model with the lowest MAE and forecast the next 30 days with confidence intervals when available.
9. **Dashboard:** provide overview, sales analysis, time-series analysis, forecasting, performance, and downloadable processed data.
10. **Documentation/testing:** create report, synopsis, viva preparation, run the pipeline, confirm generated artefacts, and compile source files.
