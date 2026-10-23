"""Create a clearly labelled synthetic transaction dataset for project testing."""
from pathlib import Path
import numpy as np
import pandas as pd


def create_sample_data(output_path: str = "data/sample_sales_data.csv") -> None:
    rng = np.random.default_rng(42)
    dates = pd.date_range("2022-01-01", "2024-12-31", freq="D")
    products = [
        ("P100", "Wireless Headphones", 22.0), ("P101", "USB Cable", 4.5),
        ("P102", "Notebook Set", 8.0), ("P103", "Desk Lamp", 18.0),
        ("P104", "Water Bottle", 10.0), ("P105", "Phone Stand", 7.5),
    ]
    countries = ["United Kingdom", "France", "Germany", "Netherlands", "Spain"]
    rows, invoice_number = [], 100000
    for day_index, date in enumerate(dates):
        weekly_factor = 1.25 if date.dayofweek in [4, 5] else 0.85
        yearly_factor = 1.45 if date.month in [11, 12] else 1.0
        trend = 1 + (day_index / len(dates)) * 0.25
        transactions = rng.integers(8, 17)
        for _ in range(transactions):
            stock_code, description, price = products[rng.integers(len(products))]
            quantity = max(1, int(rng.poisson(3 * weekly_factor * yearly_factor * trend)))
            unit_price = round(price * rng.uniform(0.92, 1.08), 2)
            rows.append({
                "InvoiceNo": str(invoice_number), "StockCode": stock_code,
                "Description": description, "Quantity": quantity,
                "InvoiceDate": date + pd.Timedelta(hours=int(rng.integers(8, 20))),
                "UnitPrice": unit_price, "CustomerID": int(rng.integers(12000, 12501)),
                "Country": countries[rng.choice(len(countries), p=[.55, .12, .12, .11, .10])],
            })
            invoice_number += 1
    destination = Path(output_path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(destination, index=False)
    print(f"Created synthetic demo data: {destination} ({len(rows):,} transactions)")


if __name__ == "__main__":
    create_sample_data()
