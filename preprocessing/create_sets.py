#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  1 12:33:44 2022

@author: tomasfernandezbouvier
"""
import sys
from settings import variable

sys.path.insert(0, '..')

from scipy.interpolate import interp1d
import pandas as pd
import numpy as np

df_deploy=  pd.read_pickle("/home/tobou/Desktop/Meteorological_Data_quality_assesment/df_gen/df_deploy.pkl")  
df_train=  pd.read_pickle("/home/tobou/Desktop/Meteorological_Data_quality_assesment/df_gen/df_train.pkl")  
df_test=  pd.read_pickle("/home/tobou/Desktop/Meteorological_Data_quality_assesment/df_gen/df_test.pkl")  

if variable == 't2m':
    low_lim  = 184.0
    high_lim = 327.0
elif variable == 'Press':
    low_lim  = 870.0
    high_lim = 1083.8
else:
    raise Exception("The variable is unknow by the program")
def sanity_check(df2):
    
    df2.mask(df2['max'] < low_lim, inplace=True)
    df2.mask(df2['max'] > 327.0, inplace=False)
    return 

def create_sets(station, df_name='train'):
    """
    Parameters
    ----------
        - station: Station ID used for computation
        - df: dataframe from which the data has to be queried
        
    Outputs
    -------
        - x: Time stamps of the station 
        - f: Cubic spline closure to get the y value by interpolation at any given time.  
    """
    
    if (df_name=='train'):
        df= df_train
    elif(df_name=='test'):
        df= df_test
    elif(df_name=='deploy'):
        df= df_deploy
    else:
        print('there was an error with the df name')
        
    df2=df[df['station']==station].copy()
    
    #temp only:
    #df2[df2['max'] < 184] = np.nan
    #df2[df2['max'] > 327] = np.nan
    
    #print(station, ' ','min', np.nanmin(df2['max']), 'max',  np.nanmax(df2['max']))

    sanity_check(df2)
    
    df2.sort_values(by='timestamp', inplace=True)
    
    #mean= np.mean(df2['max'].to_numpy())
    #std= np.std(df2['max'].to_numpy())
    
    #df2.loc[abs(df2['max'].to_numpy()-mean)>3*std, 'max'] = np.nan #TODO: make it local
    
    df2.dropna(subset=['max'],inplace=True)
    
    
    x=df2['timestamp']
    y=df2['max']

    x = x.to_numpy('datetime64[m]')
    y = y.to_numpy()

    f= interp1d(x, y, kind='cubic', fill_value='extrapolate' )

    del(df2)
    return x,f
