# Time Series Forecasting
We built this repository to help retailers prepare for, and evaluate the impact of, the COVID-19 epidemic. This repository can be used to forecast future timeseries values, and compare these forecasts against observed values to measure the impact-to-date of fleet-wide influences. For more detail on the motivation behind this project, please see https://marketdial.com/covid-19-model/.

The repository consists of python scripts which utilize various methods of forecasting, and a generic excel model that can be used to track and estimate effects at the store, department, and state level.

## 1. Code Usage

### 1.1 File descriptions and order of execution.
### 1.2 File parameters.
There are only a few parameters that need to be adjusted within with each script to get started. 

For run_forecasts.py, the user must set:
```
year_start: the year the user wants to make projections for.
week_start: the week where the projections should start (i.e. a value of 10 means that you want to use the first 9 weeks of the year as part of the training data.)
metric_list: This list should contain all the metrics that are present as columns in your data input file (format specified below).
method: selects which of three methods should be used to make the projections. A description of each method is given below.
input_file: file location of the input data.
```

And for plot_all_forecasts.py, the user only needs to set:
```
year_start: same value that was used in run_forecasts.py
week_start: "                                          "
plot_metric: the metric to be plotted.
```


## 2. Methodology Review
### 2.1. Signal-Trend Decomposition and LS Regression
![alt text](MethodologyExamples/decompose_LS_method.png "")

### 2.2. Signal-Trend Decomposition with ARIMA Model
![alt text](MethodologyExamples/decompose_ARIMA_method.png "")

### 2.3. Simple Lagged Yearly Comp Method
![alt text](MethodologyExamples/lag_comp_method.png "")




## 3. Spreadsheet Scenario Planning
This spreadsheet tabs are colored by their purpose: (1) outputs = green (2) scenario-planning adjustable fields = orange (3) input data = blue.
### 3.1. Add Data
To use this spreadsheet, you will need prediction and actual data on the store-category-week level as produced above. The current spreadsheet is built around revenue and units sold metrics. Data can be copy and pasted into the "Raw Predictions" and "Actual Values" tabs. Columns for store, week, category and one or two metrics should retain the same ordering as the example spreadsheet.

Store-region information can be added to the "Store State Lookup" tab.

Once the raw data has been updated, the pivot tables in the last 3 tabs should be refreshed.
### 3.2. Adjust Other Fields as Necessary
There are a few fields which will need to be hand-adjusted based on your data. For instance, the number of category columns will need to be adjusted one most of the output and adjustable-value tabs. In addition, one with other metrics may wish to adjust the revenue/units toggle or the tab and column names. Such changes may require adjustments to dependent pivot tables, formulas, etc.

### 3.3. Scenario Planning
The "Adjust Impact by State" tab allows a user to suppose that certain regional effects will be greater than others. The values represent the hypothesized percent increase or decrease from predicted values based on the state alone.

The "Adjust Category Effects" tab allows the user to adjust hypothesized percent increase or decrease from predicted values at the category-week level.
### 3.4. Outputs
These tabs summarize projected effects and effects observed so far using the raw input data and the user-adjusted scenario planning fields. The projected impact can be viewed at an overall or individual store level. The "Impact To-Date" tab summarizes impact observed by comparing predicted vs. actual for available data.
