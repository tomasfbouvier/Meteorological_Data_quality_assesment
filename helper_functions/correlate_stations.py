#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 30 16:05:17 2022

@author: tobou
"""

import sys 

sys.append('..')

import pandas as pd
from preprocessing.create_sets import create_sets
from numpy import np
import scipy.signal as signal

df=  pd.read_pickle("../df_gen/df_train.pkl")  
def correlate_signals(station1, station2, num=100000):  
    """
    Parameters
    ----------
        - (station1,station2): pair of stations for which the correlation score is to be computed
        - num: length of the arrays created by interpolation of the stations time-series. Default=100000 points.    
    Otuputs
    -------
        - lags
    """

    
    x1, f1= create_sets(station1, df= 'train')
    x2, f2= create_sets(station2, df='train')
    #xrange=np.linspace(max(min(x1),min(x2)), min(max(x1),max(x2)), num)
    
    a= f1(x1)
    b= f2(x1)

    a= (a - np.mean(a)) / (np.std(a) * len(x1))
    b= (b - np.mean(b)) / (np.std(b) * len(x1))
    corr = signal.correlate(a,b)
    corr*=len(a) #Does this make sense?
    #lags = signal.correlation_lags(len(a), len(b))
    
    return corr

stations=df['station'].unique()

try:
    stations_correlations= np.loadtxt('../data_files/test_properties/stations_correlations.csv')
except:
    print('recalculating stations_correlations')
    stations= df['station'].unique()
    stations_correlations= np.zeros((len(stations),len(stations)))
    for i in range(len(stations)):
        for j in range(len(stations)):
            try:
                stations_correlations[i,j]= max(correlate_signals(stations[i],stations[j], 10000))
            except:
                pass
    np.savetxt('../data_files/test_properties/stations_correlations.csv', stations_correlations)
