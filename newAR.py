#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 10:40:56 2022

@author: tomasfernandezbouvier
"""

from df import df 
from create_sets import create_sets
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.ar_model import ar_select_order
from scipy.stats import pearsonr
import numpy as np
import matplotlib.pyplot as plt



def fit_AR(y):
    y_flip= np.flip(y, axis=None)
    
    mod = ar_select_order(y, maxlag=13)
    ar_model_past = ARIMA(endog=y, order=(mod.ar_lags,0,0),  trend='n', missing= 'drop').fit()
    mod = ar_select_order(y_flip, maxlag=13)
    ar_model_future = ARIMA(y_flip, order=(mod.ar_lags,0,0),  trend='n',  missing= 'drop').fit()
    

    return ar_model_past, ar_model_future






xs, f= create_sets(6096) # I think that this is a clean station
y= f(xs)

y+=  3.*np.random.randn(len(y)) # Add some noise for robust fit



ar_model_past2, ar_model_fut2= fit_AR(y)





#print(ar_model_past2.model_orders['ar'],ar_model_fut2.model_orders['ar'])

def AR_test(station, plot=True):
    xs, f= create_sets(station)
    ys= f(xs)
   
    mean= np.mean(ys)
    std= np.std(ys)
    
    ord_past= ar_model_past2.model_orders['ar']
    ord_fut= ar_model_fut2.model_orders['ar']
    
    i=0
    while i < len(ys):
        if(abs(ys[i]-mean)>3*std):
            ys[i]=np.NAN
            #y=np.delete(y, i)
            #j=len(y); i=-1;
        i+=1
    def evaluate_point(x, y, thr):
        i_trgt= np.where(x==xs)[0][0]
        ys[i_trgt]=y
        y_flip= np.flip(ys, axis=None)
    
        ar_model_past= ar_model_past2.apply(endog=ys, refit=False)
        ar_model_fut= ar_model_fut2.apply(endog=y_flip, refit=False,  missing= 'drop')
    
        pred_past = ar_model_past.predict(start=i_trgt, end=i_trgt, dynamic=False)
        pred_fut = np.flip(ar_model_fut.predict(start=(len(ys)-i_trgt-1), end=(len(ys)-i_trgt-1), dynamic=False))
        pred_mean= np.mean([pred_past, pred_fut],axis=0)
    
        #u= np.std([pred_past, pred_fut],axis=0)[1:-1]
        #plt.errorbar(np.arange(1, len(y)-1, 1),np.mean([pred_past, pred_fut],axis=0)[1:-1], yerr=None,fmt = 'bx', capsize=0.6, alpha=.6)
    
        # TODO: investigate uncertainty accountance for bad predictions
        
        diff=abs(y - pred_mean)
        if diff>thr:
            return True
        else:
            return False
    return evaluate_point
test=AR_test(4207, plot=False)
xs,f=create_sets(4207)

plt.figure()


mean_y= np.mean(f(xs))
std_y= np.std(f(xs))
for x in xs:
    if ((abs(f(x)-mean_y))>3*std_y):
        plt.plot(x,f(x), 'k.')
    else:
        if(test(x, f(x), 8. )):
            plt.plot(x,f(x), 'r.')
        else:
            plt.plot(x,f(x),'b.')

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