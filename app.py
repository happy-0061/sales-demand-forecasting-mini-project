from pathlib import Path
import json
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Sales & Demand Forecasting", page_icon="📈", layout="wide")
ROOT = Path(__file__).parent

@st.cache_data
def load_csv(relative_path, parse_dates=None):
    path = ROOT / relative_path
    if not path.exists(): return None
    return pd.read_csv(path, parse_dates=parse_dates)

st.title("📈 Sales & Demand Forecasting using Time-Series Analysis")
st.caption("Academic mini project • Results depend on the dataset selected")
daily = load_csv("outputs/daily_sales.csv", ["Date"])
transactions = load_csv("outputs/cleaned_transactions.csv", ["InvoiceDate"])
comparison = load_csv("outputs/metrics/model_comparison.csv")
forecast = load_csv("outputs/forecasts/future_forecast.csv", ["Date"])

if daily is None or transactions is None:
    st.error("Processed data is not available. Run `python main.py` first. See README.md for help.")
    st.stop()

overview, sales, time_series, forecasting, performance, data_tab = st.tabs(["Overview", "Sales Analysis", "Time-Series Analysis", "Forecasting", "Model Performance", "Data"])
with overview:
    cols = st.columns(4)
    cols[0].metric("Total Sales", f"£{transactions.SalesAmount.sum():,.0f}")
    cols[1].metric("Total Quantity Sold", f"{transactions.Quantity.sum():,}")
    cols[2].metric("Number of Products", f"{transactions.StockCode.nunique():,}")
    cols[3].metric("Number of Transactions", f"{transactions.InvoiceNo.nunique():,}")
    st.plotly_chart(px.line(daily, x="Date", y="SalesAmount", title="Daily Sales Trend"), use_container_width=True)
with sales:
    monthly = transactions.set_index("InvoiceDate").resample("MS")["SalesAmount"].sum().reset_index()
    left, right = st.columns(2)
    left.plotly_chart(px.bar(monthly, x="InvoiceDate", y="SalesAmount", title="Monthly Sales"), use_container_width=True)
    top = transactions.groupby("Description", as_index=False).SalesAmount.sum().nlargest(10, "SalesAmount").sort_values("SalesAmount")
    right.plotly_chart(px.bar(top, x="SalesAmount", y="Description", orientation="h", title="Top Products"), use_container_width=True)
    country = transactions.groupby("Country", as_index=False).SalesAmount.sum().sort_values("SalesAmount", ascending=False)
    st.plotly_chart(px.bar(country, x="Country", y="SalesAmount", title="Country-wise Sales"), use_container_width=True)
with time_series:
    chart = daily.copy(); chart["30-day rolling average"] = chart.SalesAmount.rolling(30, min_periods=1).mean()
    st.plotly_chart(px.line(chart, x="Date", y=["SalesAmount", "30-day rolling average"], title="Trend and Rolling Average"), use_container_width=True)
    st.info("Trend shows the long-term direction. Weekly seasonality is examined because this is daily data. ARIMA-type models use differencing when the series is non-stationary.")
with forecasting:
    if forecast is None or comparison is None: st.warning("Forecast artefacts not found. Run `python main.py`.")
    else:
        st.plotly_chart(px.line(forecast, x="Date", y=["Forecast", "LowerBound", "UpperBound"], title="Next 30-Day Sales Forecast"), use_container_width=True)
        st.dataframe(forecast.round(2), use_container_width=True, hide_index=True)
with performance:
    if comparison is not None: st.dataframe(comparison, use_container_width=True, hide_index=True)
    else: st.warning("Run the pipeline to generate model evaluation metrics.")
with data_tab:
    st.dataframe(daily, use_container_width=True, hide_index=True)
    st.download_button("Download daily sales data", daily.to_csv(index=False).encode(), "daily_sales.csv", "text/csv")
