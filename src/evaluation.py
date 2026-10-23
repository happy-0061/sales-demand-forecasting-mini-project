import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error


def calculate_metrics(actual, predicted) -> dict:
    actual = np.asarray(actual, dtype=float)
    predicted = np.asarray(predicted, dtype=float)
    non_zero = actual != 0
    mape = np.mean(np.abs((actual[non_zero] - predicted[non_zero]) / actual[non_zero])) * 100 if non_zero.any() else np.nan
    return {"MAE": round(mean_absolute_error(actual, predicted), 2), "RMSE": round(np.sqrt(mean_squared_error(actual, predicted)), 2), "MAPE": round(float(mape), 2)}


def comparison_table(results: dict) -> pd.DataFrame:
    return pd.DataFrame([{"Model": name, **metrics} for name, metrics in results.items()]).sort_values("MAE").reset_index(drop=True)
