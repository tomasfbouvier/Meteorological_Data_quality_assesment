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
from df_gen.df import Create_df
from pipeline.feed_test_properties_database import feed_test_properties_database
from pipeline.merge_test_results import multi_test

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