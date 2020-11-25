# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 15:34:41 2020

@author: mamuka.chikovani
"""


import search_ads_data_extract as data_extract

import upload_search_ads_to_s3 as data_load

import time


def full_etl():
    
    

    extract =  data_extract.api_data_pull()
    
    print("data pull completed")
    
    time.sleep(2)
    
    load = data_load.load_to_s3()
    
    print("success")
    
    
    
if __name__ == '__main__':
    full_etl()    

