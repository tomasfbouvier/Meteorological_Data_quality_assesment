#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 24 12:00:43 2022

@author: tobou
"""

import sys
sys.path.insert(0, '..')

import numpy as np
import pandas as pd
#from pipeline.feed_test_properties_database import feed_db
from pipeline.merge_test_results import multi_test
import os
from datetime import datetime 

"""
def pipeline(mode='w', variable='Press'):
    if(mode=='w'):
        def aux(std, test_names, split= np.datetime64('1997-06-15' )):
            
            df=Create_df(variable, start= None, end=split)
            df.to_pickle("/home/tobou/Desktop/Meteorological_Data_quality_assesment/df_gen/df_train.pkl")  
            del(df)
            df=Create_df(variable, start= split + np.timedelta64(1,'D') , end= None)
            df.to_pickle("/home/tobou/Desktop/Meteorological_Data_quality_assesment/df_gen/df_test.pkl")    
            del(df)
            stations=  pd.read_pickle("/home/tobou/Desktop/Meteorological_Data_quality_assesment/df_gen/df_train.pkl")['station'].unique()
            feed_test_properties_database(test_names, std, stations)
            
            return
    elif(mode=='d'):
        df=Create_df(variable)
        df.to_pickle("df.pkl")  
        del(df)
        def aux(std, station):
            return multi_test(std, station)
    return aux

"""


df_deploy=  pd.read_pickle("/home/tobou/Desktop/Meteorological_Data_quality_assesment/df_gen/df_deploy.pkl") 
stations= df_deploy['station'].unique()



#ATTEMPTING TO CORRECT 1 MONTH DATA. HORRIBLE I/O. TO BE TRANSFERRED TO R + BASH 
dirname='../data_files/data_output'
variable='t2m'

if(variable== 'Press'):
    columns=['station','timestamp','min', 'max']
if(variable== 't2m'):
    columns=['station','timestamp','min', 'max', 'staturation']


for _,_, filenames in os.walk(dirname):
    for filename in filenames:
        if variable in filename:
            df_output=pd.read_table(os.path.join(dirname,filename), names=columns, sep='\s+')
# Replace the target string

for station in stations[0:5]:
    test_ensemble = multi_test(station)
    for row in df_output[df_output['station'] == station].iterrows():
        x = np.datetime64(datetime.strptime(str(int(row[1][1])), '%Y%m%d%H%M'), '[m]')
        y = np.array(row[1][3])
        print(test_ensemble(x,y))
    
    


