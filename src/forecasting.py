import warnings
import numpy as np
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX
from .evaluation import calculate_metrics


def chronological_split(series: pd.Series, train_fraction: float = 0.85):
    split_index = int(len(series) * train_fraction)
    return series.iloc[:split_index], series.iloc[split_index:]


def naive_forecast(train: pd.Series, test: pd.Series) -> pd.Series:
    return pd.Series(np.repeat(train.iloc[-1], len(test)), index=test.index)


def arima_forecast(train: pd.Series, test: pd.Series, order=(1, 1, 1)) -> pd.Series:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        model = ARIMA(train, order=order).fit()
    return model.forecast(steps=len(test))


def sarima_forecast(train: pd.Series, test: pd.Series, order=(1, 1, 1), seasonal_order=(1, 0, 1, 7)) -> pd.Series:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        model = SARIMAX(train, order=order, seasonal_order=seasonal_order, enforce_stationarity=False, enforce_invertibility=False).fit(disp=False)
    return model.forecast(steps=len(test))


def run_model_comparison(train: pd.Series, test: pd.Series):
    predictions, metrics = {}, {}
    methods = {"Naive": naive_forecast, "ARIMA(1,1,1)": arima_forecast, "SARIMA(1,1,1)(1,0,1,7)": sarima_forecast}
    for name, function in methods.items():
        try:
            prediction = function(train, test)
            prediction.index = test.index
            predictions[name] = prediction
            metrics[name] = calculate_metrics(test, prediction)
        except Exception as error:
            print(f"{name} could not be fitted: {error}")
    if not metrics:
        raise RuntimeError("No forecasting model could be fitted.")
    return predictions, metrics


def future_forecast(full_series: pd.Series, model_name: str, periods: int = 30) -> pd.DataFrame:
    future_dates = pd.date_range(full_series.index.max() + pd.Timedelta(days=1), periods=periods, freq="D")
    if model_name.startswith("SARIMA"):
        model = SARIMAX(full_series, order=(1, 1, 1), seasonal_order=(1, 0, 1, 7), enforce_stationarity=False, enforce_invertibility=False).fit(disp=False)
        result = model.get_forecast(periods)
        confidence = result.conf_int()
        values = result.predicted_mean
        lower, upper = confidence.iloc[:, 0], confidence.iloc[:, 1]
    elif model_name.startswith("ARIMA"):
        model = ARIMA(full_series, order=(1, 1, 1)).fit()
        result = model.get_forecast(periods)
        confidence = result.conf_int()
        values = result.predicted_mean
        lower, upper = confidence.iloc[:, 0], confidence.iloc[:, 1]
    else:
        values = np.repeat(full_series.iloc[-1], periods)
        lower, upper = values, values
    return pd.DataFrame({"Date": future_dates, "Forecast": np.maximum(values, 0), "LowerBound": np.maximum(lower, 0), "UpperBound": np.maximum(upper, 0)})
