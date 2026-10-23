from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd


def create_eda_outputs(clean_data: pd.DataFrame, daily_sales: pd.DataFrame, output_dir: str = "outputs") -> dict:
    figures = Path(output_dir) / "figures"
    figures.mkdir(parents=True, exist_ok=True)
    plt.style.use("seaborn-v0_8-whitegrid")
    daily = daily_sales.copy()
    daily["RollingAverage"] = daily["SalesAmount"].rolling(30, min_periods=1).mean()

    def save_plot(filename, title, x, y, kind="line", rotation=0):
        plt.figure(figsize=(10, 4.5))
        if kind == "bar": plt.bar(x, y, color="#4C78A8")
        else: plt.plot(x, y, color="#2A6F97", linewidth=1.4)
        plt.title(title); plt.xlabel(""); plt.ylabel("Sales Amount (£)")
        plt.xticks(rotation=rotation); plt.tight_layout(); plt.savefig(figures / filename, dpi=150); plt.close()

    save_plot("daily_sales_trend.png", "Daily Sales Trend", daily.Date, daily.SalesAmount)
    monthly = clean_data.set_index("InvoiceDate").resample("MS")["SalesAmount"].sum()
    save_plot("monthly_sales_trend.png", "Monthly Sales Trend", monthly.index, monthly.values)
    save_plot("monthly_sales_bar.png", "Monthly Sales", monthly.index.strftime("%b %Y"), monthly.values, "bar", 45)
    top_products = clean_data.groupby("Description")["SalesAmount"].sum().nlargest(10).sort_values()
    save_plot("top_products.png", "Top 10 Products by Sales", top_products.index, top_products.values, "bar", 55)
    country_sales = clean_data.groupby("Country")["SalesAmount"].sum().nlargest(10).sort_values()
    save_plot("country_sales.png", "Top Countries by Sales", country_sales.index, country_sales.values, "bar", 55)
    plt.figure(figsize=(10, 4.5)); plt.plot(daily.Date, daily.SalesAmount, alpha=.35, label="Daily sales"); plt.plot(daily.Date, daily.RollingAverage, linewidth=2, label="30-day rolling average")
    plt.title("Daily Sales and 30-Day Rolling Average"); plt.ylabel("Sales Amount (£)"); plt.legend(); plt.tight_layout(); plt.savefig(figures / "rolling_average.png", dpi=150); plt.close()
    return {"total_sales": float(clean_data.SalesAmount.sum()), "total_quantity": int(clean_data.Quantity.sum()), "unique_products": int(clean_data.StockCode.nunique()), "unique_customers": int(clean_data.CustomerID.nunique()) if "CustomerID" in clean_data else None, "transactions": int(clean_data.InvoiceNo.nunique())}
