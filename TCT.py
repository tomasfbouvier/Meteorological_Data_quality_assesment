#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  1 14:21:05 2022

@author: tomasfernandezbouvier
"""

from sklearn.cluster import DBSCAN
import numpy as np
from create_sets import create_sets


def time_consistency_test(station):
    """
    Parameters
    ----------
        - station: objective station from which the time-series points will be clustered
    Output
    ------
        - predict: closure functiuon that evaluates wether a given point belongs to a cluster or not
    """
    
    x, f= create_sets(station)
    y=f(x)

    X = np.array([x,y])
    X= X.T

    y_steps= [y[i+1]-y[i] for i in range(len(y)-1)]
    x_steps= [x[i+1]-x[i] for i in range(len(x)-1)]

    scaling_factor_y=abs(max(X[:,1])- min(X[:,1]))*10
    scaling_factor_x=max(X[:,0])- min(X[:,0])

   # X[:,0]/=scaling_factor_x
   # X[:,1]/=scaling_factor_y

    def predict(x, y, params):
        """
            Parameters
            ----------
                - (x,y): set of points that define the time-series
            Output
            ------
                - Boolean: test result (True/False)  
            TODO
            ----
                - Turn it into computationally efficient. Remove points for calculation
        """
        
        X_aux=np.array([[x,y]])
        X_aux[:,0]/=scaling_factor_x
        X_aux[:,1]/=scaling_factor_y
        
        X_new=np.append(X,X_aux, axis=0)
        
        labels = DBSCAN(eps=0.01,min_samples=5, metric='euclidean').fit_predict(X_new)
        
        
        del(X_new)
        
        if(labels[-1]==-1):
            return True
        else:
            return False
    return predict

import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA

from statsmodels.tsa.ar_model import ar_select_order
from scipy.stats import gaussian_kde
def AR_model(station):
    
    
    xs, f= create_sets(station)
    y= f(xs)

    #y=  [y[i+1]-y[i] for i in range(len(y)-1)] 
    
    #X = np.array([x[1:],y])
    
    #X= X.T
    
    mod = ar_select_order(y, maxlag=13)
    #print('ORDER:', arma_order_select_ic(y, max_ar=4, max_ma=2))

    ar_model = ARIMA(endog=y, order=(mod.ar_lags,0,0),  trend='n').fit()
    
   # print('lags: %s' % mod.ar_lags)
    #print(print('Coefficients: %s' % ar_model.params))
    
    #plt.plot(xs,y, 'b.')
    
    pred=ar_model.predict(start=0, end=(len(y)-1), dynamic=False)
    

    #plt.plot(xs[1:],pred[1:],'r.')
    

    #print(ar_model.summary())
   # plt.figure()
    
    diffs=pred[1:]-y[1:]
    kde=gaussian_kde(diffs)
   # xss= np.linspace(min(diffs),max(diffs),10000 )
   # plt.plot(xss, kde(xss))
    
    def evaluate_point(x, y, thr):
        
        i= np.where(x==xs)[0][0]
        diff= y-ar_model.predict(start=i, end=i, dynamic=False)
        if (kde(diff)<thr):
            return True
        else:
            return False
    return evaluate_point


    # TODO: Now that I have the way to build a model implement the subsequent test
    # TODO: switch to datetimes
    return 


xs, f= create_sets(4207)
model=AR_model(4207)
"""
for x in xs:
    if model(x, f(x), 0.005):
        plt.plot(x, f(x), 'r.')
    else:
        plt.plot(x, f(x), 'b.')
"""
