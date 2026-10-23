# Viva Questions and Short Answers

1. **What is a time series?** Data observations arranged in time order, such as daily sales.
2. **What is forecasting?** Estimating future values using historical data.
3. **Why is demand forecasting useful?** It supports inventory, staffing, and purchase planning.
4. **What is trend?** The long-term upward or downward movement in a series.
5. **What is seasonality?** A pattern that repeats at fixed intervals, such as weekly sales behaviour.
6. **What is noise?** Random variation that is not explained by trend or seasonality.
7. **What is stationarity?** A series whose statistical properties are reasonably stable over time.
8. **Why does stationarity matter?** ARIMA models work more reliably with stable series.
9. **What is the ADF test?** A statistical test that gives evidence about whether a series has a unit root/non-stationarity.
10. **What does a small ADF p-value suggest?** Evidence against a unit root; the series may be stationary.
11. **What is ARIMA?** AutoRegressive Integrated Moving Average, a statistical forecasting model.
12. **What does p mean in ARIMA?** The autoregressive order: how many previous values are used.
13. **What does d mean in ARIMA?** The number of differencing steps.
14. **What does q mean in ARIMA?** The moving-average order for past errors.
15. **What is SARIMA?** Seasonal ARIMA, which extends ARIMA with repeating seasonal terms.
16. **What are P, D, Q, and s?** Seasonal AR, differencing, MA terms, and seasonal period.
17. **Why was s=7 used?** The data is daily, so a seven-day weekly pattern is practical to examine.
18. **What is a baseline model?** A simple reference forecast used to judge advanced models.
19. **Which baseline is used here?** A Naive model that repeats the last training value.
20. **Why not randomly split time-series data?** It would mix future information into training and cause leakage.
21. **What is chronological splitting?** Training on earlier dates and testing on later dates.
22. **What is MAE?** Mean Absolute Error; average absolute difference between actual and predicted values.
23. **What is RMSE?** Root Mean Squared Error; it penalises large errors more heavily.
24. **What is MAPE?** Mean Absolute Percentage Error, a percentage-based error measure.
25. **How is zero handled in MAPE?** Zero actual values are excluded to avoid division by zero.
26. **Why might SARIMA outperform ARIMA?** It can model repeating seasonal patterns.
27. **Why might SARIMA not be best?** The data may not have strong stable seasonality or the configuration may not fit well.
28. **What is SalesAmount?** Quantity multiplied by UnitPrice.
29. **Why remove cancelled invoices?** They do not represent completed positive sales; UCI marks them with C-prefixed InvoiceNo.
30. **Why remove non-positive quantity or price?** They are not valid positive-sale records for this analysis.
31. **Why fill missing dates with zero?** It preserves a continuous daily time axis and represents days without recorded sales.
32. **What is decomposition?** Separating a series into trend, seasonal, and residual components.
33. **Why use Streamlit?** It quickly turns Python analysis into an interactive dashboard.
34. **Prediction versus forecasting?** Forecasting is prediction specifically for future time points.
35. **What is overfitting in time series?** A model learns historical noise and performs poorly on new future data.
36. **What are project limitations?** No promotions, holidays, inventory, or product-level forecasting are included.
