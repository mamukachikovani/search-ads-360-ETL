# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 22:02:10 2020

@author: mamuka.chikovani
"""

import boto3
import pandas as pd
import csv
import os
import time
import numpy as np
import data_transform as transform
import re
from retrying import retry

        

params = {
    'region': 'us-east-1',
    'database': 'database_name',
    'bucket': 'your_s3_bucket',
    'path': 'path_to_your_project_folder',
    'query': """select month from database_table
                group by month
                order by month"""
}

session = boto3.Session(profile_name='default')


def query_results(session, params):
    ## Creating the Client for Athena
    client = boto3.client('athena')
    
    ## This function executes the query and returns the query execution ID
    response_query_execution_id = client.start_query_execution(
        QueryString = params['query'],
        QueryExecutionContext = {
            'Database' : params['database']
        },
        ResultConfiguration = {
            'OutputLocation': 's3://' + params['bucket'] + '/' + params['path'] + 'temp'
        }
    )

    ## This function takes query execution id as input and returns the details of the query executed
    response_get_query_details = client.get_query_execution(
        QueryExecutionId = response_query_execution_id['QueryExecutionId']
    )

        
    RETRY_COUNT = 10    
    status = 'QUEUED'

   # while status == 'QUEUED' or status == 'RUNNING' or status is None:
    for i in range(1, 1 + RETRY_COUNT):
        #(iterations>0):
        #iterations = iterations - 1
        response_get_query_details = client.get_query_execution(
        QueryExecutionId = response_query_execution_id['QueryExecutionId']
        )
        status = response_get_query_details['QueryExecution']['Status']['State']
        print(status)
        if (status == 'FAILED') or (status == 'CANCELLED') :
            return False, False
        
       # elif status == 'QUEUED':
            
            
        elif status == 'SUCCEEDED':
            location = response_get_query_details['QueryExecution']['ResultConfiguration']['OutputLocation']

            ## Function to get output results
            response_query_result = client.get_query_results(
                QueryExecutionId = response_query_execution_id['QueryExecutionId']
            )
            result_data = response_query_result['ResultSet']
            
            filename = re.findall('.*\/(.*)', location)[0]
            
            #print(filename)
            
            #print(os.listdir(location))
                        
            #print("location: ", location)
            #print("data: ", result_data)
            return location, result_data
        else:
            time.sleep(1)
        
    return False


#@retry(wait_fixed=2000)
    


@retry(stop_max_attempt_number = 30,
    wait_exponential_multiplier = 3000,
    wait_exponential_max = 10 * 1000)

def query_to_df():
    
    query = query_results(session, params)
    
    data = query[1]
    
    
    
       
        
    df_query = pd.DataFrame(columns = ['month'])

    print(data)

    for val in data['Rows']:
        data1 = val.get('Data')
        for date_range in data1:
            date = date_range.get('VarCharValue')
            df_query = df_query.append({ 'month' : date}, ignore_index = True)
            
     
    
        
    df_query['month'] = df_query['month'].astype(str) 
    
    df_query['month'] = pd.to_datetime(df_query['month'], errors='coerce')

    df_query = df_query.dropna()
    
    df_query['month'] = df_query['month'].dt.date
    
    df_data = transform.search_ads_data()
    
# =============================================================================
# validate date range against existing dataset in s3 bucket
# =============================================================================

       
    date_checker = np.isin(df_data['month'], df_query['month']) 

    print(date_checker)        
    
    if False in date_checker:
        
        df_data['month'] = pd.to_datetime(df_data['month'], format='%Y-%m-%d')

        print('ready for load')
        
            
        print(df_data.info())
                              
        return df_data 
    else:
        print('The date range already exist in the s3 folder')
        return False
        
    
     
    
if __name__ == '__main__':
    
   query_to_df()
