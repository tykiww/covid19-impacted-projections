from numpy import *
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import linear_model
from statsmodels.tsa.seasonal import seasonal_decompose
import math, itertools
from utilities.functions import yaml_parser

####################################### Functions of Interest #######################################


# Plotting Function
def plot_timeseries(year_start, week_start, plot_metric, model, real_df, proj_df):
  
  # Setup Axes
  all_hierarchies = list(sort(list(set(proj_df['hierarchy'].values))))
  num_rows = min(len(all_hierarchies),2)
  num_columns = min(math.ceil(len(all_hierarchies)/2),3)
  num_batchs = math.ceil(len(all_hierarchies)/6)
  
  # Create grid output by hierarchy
  for batch in range(num_batchs):
    list_hierarchies = all_hierarchies[(batch*6):((batch+1)*6)]
    fig = plt.figure(figsize=(20*(num_columns/3),10*(num_rows/2)), dpi=200)
    for k in range(len(list_hierarchies)):
      plot_hierarchy = list_hierarchies[k]
      plot_real_df = real_df[real_df['hierarchy'] == plot_hierarchy]
      plot_proj_df = proj_df[proj_df['hierarchy'] == plot_hierarchy]
      
      all_stores = list(set(plot_real_df['store_id'].values))
      proj_stores = list(set(plot_proj_df['store_id'].values))
      plot_real_df = plot_real_df[plot_real_df['store_id'].isin(proj_stores)]
      
      plot_real_df = plot_real_df.groupby(['year','week_num']).sum()[[plot_metric]]
      plot_proj_df = plot_proj_df.groupby(['year','week_num']).sum()[['proj_'+plot_metric]]
      
      plot_real_df.reset_index(inplace=True)
      plot_proj_df.reset_index(inplace=True)
      plot_df = pd.merge(plot_real_df, plot_proj_df, how='outer')
      plot_df.index = [str(x)+'-WK'+('0'*(y<10))+str(y) for (x,y) in zip(plot_df['year'].values,plot_df['week_num'])]
      
      group_vals = real_df.groupby('hierarchy').sum()[plot_metric]
      perc_all = group_vals[plot_hierarchy]/group_vals.sum()
      
      # Match proj with actual on day of split
      for i in range(1,week_start-1):
        ind = plot_df[(plot_df['year']==year_start) & (plot_df['week_num']==i)].index.values[0]
        plot_df.at[ind,'proj_revenue'] = nan
      
      ind = plot_df[(plot_df['year']==year_start) & (plot_df['week_num']==week_start-1)].index.values[0]
      plot_df.at[ind,'proj_'+plot_metric] = plot_df.loc[ind, plot_metric]
      
      ax = fig.add_subplot(num_rows,num_columns,k+1-6*batch)
      ax.plot(arange(6,len(plot_df)),plot_df.iloc[6:,:][plot_metric].values,'-',color='#d45087',label=f'Actual Revenue')
      ax.plot(arange(6,len(plot_df)),plot_df.iloc[6:,:]['proj_revenue'].values,'--',color='#003f5c',label=f'Projected Revenue')
      ax.set_xticks(25*arange(0,len(plot_df)//25+1)-7)
      ax.set_xticklabels([plot_df.index[x] for x in ax.get_xticks()], rotation=30)
      ax.set_yticklabels(['$'+str(int(x/1000))+'K' for x in ax.get_yticks()])
      
      ylim = ax.get_ylim()
      ax.plot([arange(len(plot_df))[plot_df.index==ind][0],arange(len(plot_df))[plot_df.index==ind][0]], ylim,'k--',linewidth=.6)
      ax.axvspan(0,arange(len(plot_df))[plot_df.index==ind][0],color="gray",alpha=.2)
      ax.set_ylim(ylim)
      ax.set_xlim([6,len(plot_df)])
      ax.set_title(plot_hierarchy+f' ({round(100*perc_all,1)}% of Total)')
      ax.legend(loc='upper left')
      
      fig.tight_layout()
      fig.savefig(f'output/{year_start}_projections_{model}_{batch}.png')


####################################### Plot and Save Model #######################################

# Set params
config = yaml_parser("config.yml")
year = config['default']['start']
week = config['default']['week']
metric = config['default']['plot_metric']
method = config['default']['method']

# Read data
actuals = pd.read_csv(f'output/{year_start}_real.csv', header=0)
projected = pd.read_csv(f'output/{year_start}_projected.csv', header=0)

# Execute
plot_timeseries(year, week, metric, 
                method, actuals, projected)
