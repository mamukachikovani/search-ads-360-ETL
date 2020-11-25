# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 11:39:28 2020

@author: mamuka.chikovani
"""


import time

import lenvima_dtc_patient 

import lenvima_hcc_patient 

import keytruda_lenvima_consumer

import keytruda_lenvima_hcp 

import lenvima_rcc_patient 

import lenvima_pan_tumor_patient


def api_data_pull():
    
    

    lenvima_dtc_patient.main() 
    
           
    time.sleep(2)
    
    lenvima_hcc_patient.main()
    
    time.sleep(2)
    
    keytruda_lenvima_consumer.main()
    
    time.sleep(2)
    
    keytruda_lenvima_hcp.main()
    
    time.sleep(2)
    
    lenvima_rcc_patient.main()
    
    time.sleep(2)
    
    lenvima_pan_tumor_patient.main()
    


if __name__ == '__main__':
    api_data_pull()    
    











