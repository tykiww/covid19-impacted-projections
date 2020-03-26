from numpy import *
import pandas as pd
from sklearn import linear_model
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.arima_model import ARIMA
import yaml # pyyaml

# Configuration Parser

def yaml_parser(filename):
  with open(filename,'r') as stream:
    try:
      return yaml.safe_load(stream)
    except yaml.YAMLError as exc:
      print(exc)


# Simple Lagged Yearly Comp Method
def forecast_lag_comp(timeseries,num_used_avg_yearly_diff,num_proj):
  projection = list(timeseries.copy())
  for k in range(len(timeseries),len(timeseries)+num_proj):
    avg_yearly_diff = mean((array(projection[52:])-array(projection[:-52]))[-num_used_avg_yearly_diff:])
    projection.append(projection[-52]+avg_yearly_diff)
  return projection[-52:]


# Signal-Trend Decomposition and Least Squares Penalized Regression
def forecast_decomp_LS(timeseries,power_for_weight_set,num_proj):
  decomp = seasonal_decompose(timeseries, model='additive', freq=52)
  trend = decomp.trend
  seasonal = decomp.seasonal
  res = decomp.resid
  
  x = arange(len(timeseries))[~isnan(trend)]
  y = trend[~isnan(trend)]
  LM = linear_model.LinearRegression()
  weights = (1/((arange(len(x))+1)**power_for_weight_set))[::-1]
  LM.fit(x.reshape(-1,1),y.reshape(-1,1),sample_weight=weights)
  linear_projection = LM.predict(arange(len(timeseries)+num_proj).reshape(-1,1)).reshape(-1)
  seasonal_projection = array([seasonal[i%52] for i in arange(len(timeseries)+num_proj)])
  projection = (linear_projection+seasonal_projection)
  projection[:len(timeseries)] = timeseries.copy()
  return projection[-52:]


# Signal-Trend Decomposition with ARIMA Model
def forecast_decomp_arima(timeseries, num_proj):
  # Since this method does not allow us to weight more recent data
  # we do a hard cutoff at the past two years of data at most.
  timeseries = timeseries[-104:]
  decomp = seasonal_decompose(timeseries, model='additive', freq=52)
  seasonal = decomp.seasonal
  seasonal_projection = array([seasonal[i%52] for i in range(len(timeseries)+num_proj)])
  non_seasonal_timeseries = array(timeseries)-seasonal
  
  try:
    arima_model = ARIMA(non_seasonal_timeseries, order=(2,1,1))
    model_fit = arima_model.fit(order=0, disp=0)
    non_seasonal_projection = list(model_fit.predict(start=1, end=len(timeseries)+num_proj))
    for i in range(1,len(non_seasonal_projection)):
      non_seasonal_projection[i] += non_seasonal_projection[i-1]
    
    non_seasonal_projection = array(non_seasonal_projection)+non_seasonal_timeseries[0]
  
  except:
    print("ARIMA model could not converge, using purely seasonal prediction")
    non_seasonal_projection = zeros(len(seasonal_projection))+mean(non_seasonal_timeseries)
  
  projection = seasonal_projection+non_seasonal_projection
  projection[:len(timeseries)] = timeseries.copy()
  return projection[-52:]


