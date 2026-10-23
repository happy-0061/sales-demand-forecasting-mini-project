"""Run preprocessing, EDA, model evaluation, and a 30-day forecast."""
import argparse
import json
from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller
from src.data_preprocessing import load_and_clean_data, create_daily_sales, save_processed_data
from src.eda import create_eda_outputs
from src.forecasting import chronological_split, run_model_comparison, future_forecast
from src.evaluation import comparison_table


def run_pipeline(input_path: str) -> None:
    Path("outputs/figures").mkdir(parents=True, exist_ok=True)
    Path("outputs/forecasts").mkdir(parents=True, exist_ok=True)
    Path("outputs/metrics").mkdir(parents=True, exist_ok=True)
    clean, cleaning_summary = load_and_clean_data(input_path)
    daily = create_daily_sales(clean)
    save_processed_data(clean, daily)
    eda_summary = create_eda_outputs(clean, daily)
    with open("outputs/metrics/data_summary.json", "w", encoding="utf-8") as file:
        json.dump({**cleaning_summary, **eda_summary}, file, indent=2)

    series = daily.set_index("Date")["SalesAmount"].asfreq("D")
    # ADF is reported, not used blindly: p < 0.05 suggests stationarity.
    adf_stat, adf_pvalue, *_ = adfuller(series)
    pd.DataFrame([{"ADF statistic": adf_stat, "p-value": adf_pvalue, "Interpretation": "Likely stationary" if adf_pvalue < .05 else "Likely non-stationary; differencing is used by ARIMA"}]).to_csv("outputs/metrics/adf_result.csv", index=False)
    if len(series) >= 21:
        decomposition = seasonal_decompose(series, model="additive", period=7)
        figure = decomposition.plot(); figure.set_size_inches(10, 8); figure.tight_layout(); figure.savefig("outputs/figures/weekly_decomposition.png", dpi=150); plt.close(figure)

    train, test = chronological_split(series)
    predictions, model_metrics = run_model_comparison(train, test)
    comparison = comparison_table(model_metrics)
    comparison.to_csv("outputs/metrics/model_comparison.csv", index=False)
    best_model = comparison.iloc[0]["Model"]
    future = future_forecast(series, best_model, periods=30)
    future.to_csv("outputs/forecasts/future_forecast.csv", index=False)
    predicted = predictions[best_model]
    plt.figure(figsize=(11, 5)); plt.plot(train.index, train, label="Training sales", alpha=.65); plt.plot(test.index, test, label="Actual test sales", color="#111111"); plt.plot(predicted.index, predicted, label=f"{best_model} prediction", linestyle="--"); plt.plot(future.Date, future.Forecast, label="30-day future forecast", color="#D1495B")
    plt.legend(); plt.title("Sales Forecast: Actual, Predicted, and Future"); plt.ylabel("Sales Amount (£)"); plt.tight_layout(); plt.savefig("outputs/figures/forecast_result.png", dpi=150); plt.close()
    print(f"Pipeline complete. Best model by MAE: {best_model}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="data/sample_sales_data.csv", help="Path to CSV or XLSX source data")
    args = parser.parse_args()
    try:
        run_pipeline(args.input)
    except Exception as error:
        print(f"Pipeline failed: {error}")
        raise



#python main.py
#python -m streamlit run app.py