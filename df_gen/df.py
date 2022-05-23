#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  1 12:36:14 2022

@author: tomasfernandezbouvier
"""

import os
import numpy as np
import pandas as pd

import sys
sys.path.insert(0, '..')



def aux_df(name, dirname, columns):

    df= pd.read_table(name, dtype=float, header=None, names= columns,sep='\s+').fillna(np.nan)
    df['timestamp'] = pd.to_datetime(df['timestamp'], format='%Y%m%d%H%M')
    #df.describe()
    #df['station'].unique()
    df['file_type']= dirname
    #print(df)

    return df



def Create_df(variable):
    df=pd.DataFrame();
    
    if(variable== 'Press'):
        columns=['station','timestamp','min', 'max']
    if(variable== 't2m'):
        columns=['station','timestamp','min', 'max', 'staturation']
    for dirname, _, filenames in os.walk('../data_files/data'):
        for filename in filenames:
            if str(variable) in filename:
                
                df2=aux_df(str(dirname+'/'+filename), dirname, columns=columns)
                df=df.append(df2, ignore_index=True)
        
    
    
            
    
    
    df_true= df[df['file_type']=='../data_files/data/Carra'] # Corrected data from Bjarne
    
    df=df[df['file_type']=='../data_files/data/data1/combined']
    print(df)
    return df

df=Create_df('Press')
df.to_pickle("df.pkl")  
print(df)