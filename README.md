# Time Series Forecasting


## 1. Code Ussage
### 1.1 File descriptions and order of execution.
### 1.2 File parameters.
There are only a few parameters that need to beadjusted within with each script to get started. 

For run_forecasts.py, the user must set:
```
year_start: the year the user wants to make projections for.
week_start: the week where the projections should start (i.e. a value of 10 means that you wanted to use the first 9 weeks of the year as part of the training data.)
metric_list: This list should contain all the metrics that are present as columns in your data input file (format specified below).
method: selects which of three methods should be used to make the projections. A description of each method is given below.
input_file: file location of the input data.
```

And for plot_all_forecasts.py, the user only needs to set:
```
year_start: same value that was in run_forecasts.py
week_start: "                                     "
plot_metric: the metric to be plotted.
```


## 2. Methodology Review
### 2.1. Simple Lagged Yearly Comp Method
### 2.2. Signal-Trend Decomposition and LS Regression
### 2.3. Signal-Trend Decomposition with ARIMA Model


