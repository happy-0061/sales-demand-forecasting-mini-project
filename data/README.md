# Dataset instructions

## Recommended real dataset

Use the **Online Retail** dataset from the [UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/352/online+retail). It contains transactions for a UK-based online retailer from 1 December 2010 to 9 December 2011. Cite it as: Chen, D. (2015). *Online Retail* [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5BW33.

The dataset is available under CC BY 4.0. Download `Online Retail.xlsx` from UCI and place it in this `data/` folder, exactly as:

```text
data/Online Retail.xlsx
```

Then run `python main.py --input "data/Online Retail.xlsx"`.

## Included demo data

`sample_sales_data.csv` is **synthetic, reproducible demo data** created by `create_sample_data.py`. It is only included so that the program can be tested without downloading a real dataset. It must not be presented as actual retail results.
