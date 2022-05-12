#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  1 12:33:44 2022

@author: tomasfernandezbouvier
"""
import sys

sys.path.insert(0, '..')

from scipy.interpolate import interp1d
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#Esto no deberia estar aquí

df=  pd.read_pickle("/home/tobou/Desktop/Meteorological_Data_quality_assesment/df_gen/df.pkl")  

def create_sets(station, df=df):
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
    df2=df[df['station']==station].copy()
    
    df2.replace(0, np.nan, inplace=True)
    
    mean= np.mean(df2['max'].to_numpy())
    std= np.std(df2['max'].to_numpy())
    
    df2.loc[abs(df2['max'].to_numpy()-mean)>3*std, 'max'] = np.nan
    
    df2.dropna(inplace=True)
    
    
    x=df2['timestamp']
    y=df2['max']

    x = x.to_numpy('float64')
    y = y.to_numpy('float64')

    X = np.array([x,y])
    X= X.T
    
    X=X[X[:, 0].argsort()]
    
    x= X[:,0]
    y= X[:,1]
    


    f= interp1d(x, y, kind='cubic', fill_value='extrapolate' )

    del(df2)
    return x,f