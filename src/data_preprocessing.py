from pathlib import Path
import pandas as pd

REQUIRED_COLUMNS = {"InvoiceNo", "StockCode", "Description", "Quantity", "InvoiceDate", "UnitPrice", "Country"}


def load_and_clean_data(file_path: str) -> tuple[pd.DataFrame, dict]:
    """Load UCI-style CSV/XLSX data and apply documented cleaning rules."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Dataset not found: {path}. See data/README.md for instructions.")
    data = pd.read_excel(path) if path.suffix.lower() in {".xlsx", ".xls"} else pd.read_csv(path)
    missing_columns = REQUIRED_COLUMNS - set(data.columns)
    if missing_columns:
        raise ValueError(f"Missing required columns: {sorted(missing_columns)}")

    summary = {"original_rows": len(data), "missing_values_before": int(data.isna().sum().sum())}
    data["InvoiceDate"] = pd.to_datetime(data["InvoiceDate"], errors="coerce")
    data["Quantity"] = pd.to_numeric(data["Quantity"], errors="coerce")
    data["UnitPrice"] = pd.to_numeric(data["UnitPrice"], errors="coerce")

    # C-prefixed invoices represent cancellations in the UCI documentation.
    cancellation_mask = data["InvoiceNo"].astype(str).str.startswith("C", na=False)
    invalid_mask = data["InvoiceDate"].isna() | (data["Quantity"] <= 0) | (data["UnitPrice"] <= 0)
    summary["cancelled_rows_removed"] = int(cancellation_mask.sum())
    summary["invalid_rows_removed"] = int((~cancellation_mask & invalid_mask).sum())
    clean = data.loc[~cancellation_mask & ~invalid_mask].copy()
    clean["SalesAmount"] = clean["Quantity"] * clean["UnitPrice"]
    clean = clean.sort_values("InvoiceDate")
    summary["clean_rows"] = len(clean)
    return clean, summary


def create_daily_sales(clean_data: pd.DataFrame) -> pd.DataFrame:
    daily = clean_data.assign(Date=clean_data["InvoiceDate"].dt.normalize()).groupby("Date", as_index=False).agg(
        SalesAmount=("SalesAmount", "sum"), Quantity=("Quantity", "sum"), Transactions=("InvoiceNo", "nunique")
    )
    full_dates = pd.date_range(daily["Date"].min(), daily["Date"].max(), freq="D")
    daily = daily.set_index("Date").reindex(full_dates, fill_value=0).rename_axis("Date").reset_index()
    return daily.sort_values("Date")


def save_processed_data(clean_data: pd.DataFrame, daily_sales: pd.DataFrame, output_dir: str = "outputs") -> None:
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    clean_data.to_csv(output / "cleaned_transactions.csv", index=False)
    daily_sales.to_csv(output / "daily_sales.csv", index=False)
