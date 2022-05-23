#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 10:40:56 2022

@author: tomasfernandezbouvier
"""

import sys
sys.path.insert(0, '..')


import pandas as pd
from preprocessing.create_sets import create_sets
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.ar_model import ar_select_order
from scipy.stats import pearsonr
import numpy as np
import matplotlib.pyplot as plt
import time


df=  pd.read_pickle("../df_gen/df.pkl")  
def fit_AR(ys):
    y= ys.copy()
    y+=  3.*np.random.randn(len(y)) # Add some noise for robust fit

    y_flip= np.flip(y, axis=None)
    
    mod = ar_select_order(y, maxlag=13)
    ar_model_past = ARIMA(endog=y, order=(mod.ar_lags,0,0),  trend='n', missing= 'drop').fit()
    mod = ar_select_order(y_flip, maxlag=13)
    ar_model_future = ARIMA(y_flip, order=(mod.ar_lags,0,0),  trend='n',  missing= 'drop').fit()
    
    del(y); del(y_flip);

    return ar_model_past, ar_model_future, mod

def AR_test(station):
    xs, f= create_sets(station)
    ys= f(xs)
    
    ar_model_past2, ar_model_fut2, mod= fit_AR(ys)
    
    def evaluate_point(x, y, thr):
        i_trgt= np.where(x==xs)[0][0]
        if(i_trgt<int(len(mod.ar_lags))):
            ys2= ys[:i_trgt+int(len(mod.ar_lags))].copy() #TRIAL
        elif(i_trgt>len(ys)-int(len(mod.ar_lags))):
            ys2= ys[i_trgt-int(len(mod.ar_lags)):].copy() #TRIAL
        else:
            ys2= ys[i_trgt-int(len(mod.ar_lags)):i_trgt+int(len(mod.ar_lags))].copy()
        
        ys2[int(len(mod.ar_lags))-1]=y
                
        y_flip= np.flip(ys2, axis=None)
        # start= time.time()
        
        ar_model_past= ar_model_past2.apply(endog=ys2, refit=False, missing='drop')
        ar_model_fut= ar_model_fut2.apply(endog=y_flip, refit=False, missing='drop')
        # p1= time.time()
        pred_past = ar_model_past.predict(start=int(len(mod.ar_lags)), end=int(len(mod.ar_lags)), dynamic=False)
        pred_fut = np.flip(ar_model_fut.predict(start=int(len(mod.ar_lags))-1, end=int(len(mod.ar_lags))-1, dynamic=False))
        #pred_past = ar_model_past.predict(start=i_trgt, end=i_trgt, dynamic=False)
        #pred_fut = np.flip(ar_model_fut.predict(start=(len(ys)-i_trgt-1), end=(len(ys)-i_trgt-1), dynamic=False))
        #pred_mean= np.mean([pred_past, pred_fut],axis=0)
        #end=time.time()
        pred_mean=np.mean([pred_past, pred_fut])
        
        #u= np.std([pred_past, pred_fut],axis=0)[1:-1]
        #plt.errorbar(np.arange(1, len(y)-1, 1),np.mean([pred_past, pred_fut],axis=0)[1:-1], yerr=None,fmt = 'bx', capsize=0.6, alpha=.6)
    
        # TODO: investigate uncertainty accountance for bad predictions
        #print(end-p1,p1-start,end-start)
        diff=abs(y - pred_mean)
        if diff>thr:
            return True
        else:
            return False
    return evaluate_point

"""
test=AR_test(6096)
xs,f=create_sets(6096)

plt.figure()


mean_y= np.mean(f(xs))
std_y= np.std(f(xs))
for x in xs:
    if ((abs(f(x)-mean_y))>3*std_y):
        plt.plot(x,f(x), 'k.')
    else:
        if(test(x, f(x), 1.46755 )):
            plt.plot(x,f(x), 'r.')
        else:
            plt.plot(x,f(x),'b.')

"""
"""
print('r_past: ', pearsonr(y[1:], pred_past[1:]) )
print('r_fut: ', pearsonr(y[:-1], pred_fut[:-1]) )
print('r: ', pearsonr(y[1:-1], pred_mean[1:-1] ))

if plot:
    
    plt.figure()
    plt.plot(y[1:-1], 'b.')
    
    
    plt.plot(pred_mean[1:-1], 'r.')
    
    plt.figure()
    plt.title('mean')
    plt.scatter(y[1:-1], pred_mean[1:-1], c='b', s=2)
    plt.plot(np.linspace(min(y), max(y),10000), np.linspace(min(y), max(y),10000), 'r-')
    plt.plot(np.linspace(min(y), max(y),10000), np.linspace(min(y), max(y),10000)+3., 'r--')
    plt.plot(np.linspace(min(y), max(y),10000), np.linspace(min(y), max(y),10000)-3., 'r--')
    
    
    plt.figure()
    plt.scatter(y[1:], pred_past[1:], c='b', s=2)
    plt.plot(np.linspace(min(y), max(y),10000), np.linspace(min(y), max(y),10000), 'r-')
    plt.plot(np.linspace(min(y), max(y),10000), np.linspace(min(y), max(y),10000)+1.5, 'r--')
    plt.plot(np.linspace(min(y), max(y),10000), np.linspace(min(y), max(y),10000)-1.5, 'r--')
    
    
    plt.figure()
    plt.scatter(y[:-1], pred_fut[:-1], c='b', s=2)
    plt.plot(np.linspace(min(y), max(y),10000), np.linspace(min(y), max(y),10000), 'r-')
    plt.plot(np.linspace(min(y), max(y),10000), np.linspace(min(y), max(y),10000)+1.5, 'r--')
    plt.plot(np.linspace(min(y), max(y),10000), np.linspace(min(y), max(y),10000)-1.5, 'r--')
    
"""
"""
pred_past= pred_past[~np.isnan(y)]
pred_fut= pred_fut[~np.isxnan(y)]
pred_mean= pred_mean[~np.isnan(y)]
y= y[~np.isnan(y)]
print(len(y), len(pred_past))
"""