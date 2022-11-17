#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 30 16:05:17 2022

@author: tobou
"""

import sys

sys.path.insert(0, '..')


import pandas as pd
from preprocessing.create_sets import create_sets
import numpy as np
import scipy.signal as signal

df=  pd.read_pickle("../df_gen/df_test.pkl")  
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

    
    x1, f1= create_sets(station1, df_name= 'train')
    x2, f2= create_sets(station2, df_name='train')
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
    stations_correlations= pd.read_csv('../data_files/stations_correlations2.csv')
except:
    print('recalculating stations_correlations')
    stations= df['station'].unique()
    
    
    stations_correlations = []

    for i in range(len(stations)):
        print(i, '/', len(stations))
        for j in range(len(stations)):
            
            #stations_correlations[i,j]= max(correlate_signals(stations[i],stations[j], 10000))
            try:
                stations_correlations.append({'station1': stations[i], 
                                              'station2':stations[j],
                                              'r':max(correlate_signals(stations[i],stations[j], 10000))}) 
                #print(stations_correlations[i,j])
            except:
                stations_correlations.append({'station1': stations[i], 
                                              'station2':stations[j],
                                              'r':0.}) 

                pass
            
    #stations_correlations= pd.DataFrame(stations_correlations).to_csv('../data_files/stations_correlations.csv')
    #np.savetxt('../data_files/stations_correlations2.csv', stations_correlations)


import matplotlib.pyplot as plt 
import seaborn as sns;


plt.figure(figsize=(5,5))
mmm=stations_correlations[stations_correlations['station1']<5000][stations_correlations['station2']<5000]
ticklabels=mmm['station1'].unique()
mmm=np.reshape(mmm['r'].values,(36,36))
mmm=np.nan_to_num(mmm)
sns.heatmap(mmm, xticklabels=ticklabels, yticklabels=ticklabels, linewidth=0., 
            cbar_kws={"shrink": 1., "pad": 0.01, "fraction":0.05})
plt.tight_layout()
#plt.savefig('../Images/stations_correlations.png')
