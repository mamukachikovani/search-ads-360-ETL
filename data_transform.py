# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 09:57:09 2020

author: mamuka.chikovani
"""


import pandas as pd

import glob

import os

from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta

import time




pd.set_option('display.max_rows', 50)
pd.set_option('display.max_columns', 50)






def search_ads_data():
    
    mypath = os.getcwd()
          
        
    list_of_files = glob.glob(mypath + '/*.csv')
    
       
    df_total = pd.DataFrame()
# =============================================================================
# loop over .csv files in your working directory 
# =============================================================================
        
    
    for frame in list_of_files:
        df = pd.read_csv(frame)
        print(df)
        df_total = df_total.append(df, ignore_index=True)
        
    df_total = df_total.fillna(0)
    
    df_total = df_total.groupby('account', as_index=False)[['cost', 'key action']].sum()

# =============================================================================
#  create 'month' column as first day of previous month  
# =============================================================================

    df_total['month'] = datetime.today().replace(day=1) - relativedelta(months=1)
    
    
    df_total['month'] = df_total['month'].dt.date
    
        
    df_total = df_total[['account', 'month', 'cost', 'key action']]
      
        
        
    return df_total



if __name__ == '__main__':
  search_ads_data()        
        
        
        
