# Time Series Forecasting Rebuilt 

This repository is an adaptation of MarketDial's pro-bono forecasting models provided for retailers amidst the current COVID-19 pandemic. "This repository can be used to forecast future timeseries values, and compare these forecasts against observed values to measure the impact-to-date of fleet-wide influences" [(source)](https://github.com/gkropf/timeseries-impacted-projections).

The purpose of this rebuild was twofold:
  1) For a more non-technical audience: Create a friendlier and more streamlined approach to generating plots
  2) For parameter tuning abilities: Allow performance adjustment for enhanced accuraccy.

*Instead of having to directly open any python files, a user only needs to edit the contents of the `config.yml` files and run a single line of code to generate forecasts of interest.* Soon, a friendlier interface such as a dashboard with a csv upload may be considered.

So far, none of the model parameters have been changed aside from an added flexibility of the ARIMA parameters. Future updates may include a gridsearch/adapted-weight options or updates on likelihood estimates (still deciding).

Other minor changes may be tracked through the commit history.


## Code Usage

The forecast algorithm uses a CSV to be input under the `dataset/` folder. Please refer to the `sample_input_data.csv` or any instructions in [MarketDial's repository](https://github.com/gkropf/timeseries-impacted-projections) as a reference guide for a minimum viable output.

- Columns must at least have the columns: (hierarchy_id, store_id, date_day)
- Columns should also include a metric of interest: (revenue, units)
- Date_day must have a specific format: YYYY-MM-DD

### Modifying the `config.yml` File


- A year for the expected projections will be specified in the `config.yml` file: (e.g. 2020)
- A week parameter will specify how many weeks of data should train the model: (e.g. 10)
- The tracked metric of interest should be included in the `config.yml` file: (revenue, units)
- For plotting, only 1 specific metric can be chosen: ('revenue')
- The method/model of interest should be set: ('deccomp_LS')
- The filepath to the dataset should also be included as a csv: 'dataset/sample_input_data.csv'

Here is an example of a useful configuration.

```
default:
  start: 2020                                           # Year to start prediction from
  week: 15                                              # use the first n-1 weeks of the year as part of the training data.
  metrics: ['revenue', 'units', 'profit']               # Name of prediction aggregates to collect
  plot_metric: 'revenue'                                # The metric you want plotted
  method: 'decomp_arima'                                # can be 'lag_comp', 'decomp_LS', or 'decomp_arima'
  input_file: 'dataset/sample_input_data.csv'           # Path to raw input file.
```


### The single line of code

```

```
