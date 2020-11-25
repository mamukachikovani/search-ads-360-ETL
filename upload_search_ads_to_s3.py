# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 10:17:50 2020

@author: mamuka.chikovani
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 23:04:35 2020

@author: mamuka.chikovani
"""


import boto3
import pandas as pd
from io import StringIO
import re
import time

#import data_cleaning as data
import date_range_checker as data




params = {
    'region': 'us-east-1',
    'database': 'grd_merck',
    'bucket': 'mbww-gr2-custom-initiative',
    'path': 'merck/LenvimaSearch/',
}

session = boto3.Session(profile_name='default')

def s3_to_pandas(session, params):    
    s3client = session.client('s3')
   

# =============================================================================
# export search dataframe for load 
# =============================================================================
    df = data.query_to_df()
    
   
        
    if isinstance(df, pd.DataFrame):
        
        df['month'] = pd.to_datetime(df['month'])  
               
        print(df.info())
        
# =============================================================================
# create file name                
# =============================================================================
    
        filename = str(max(df['month']).strftime('%Y%m%d')) + '.csv'

        
# =============================================================================
# save df in csv format
# =============================================================================
            
        csv_buffer = StringIO()
    
        df.to_csv(csv_buffer, index=False)
    
    
# =============================================================================
# load data into s3 bucket     
# =============================================================================
       
        print("data is being loaded..")
        
        s3client.put_object(Bucket=params['bucket'], Key=params['path'] + filename, Body=csv_buffer.getvalue())

       
    else:
        
         pass
        
        
def load_to_s3():
    s3_to_pandas(session, params)
        
   
if __name__ == '__main__':
    load_to_s3()

       