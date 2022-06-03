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

import numpy as np


from tests.test_base_class import Test

df=  pd.read_pickle("../df_gen/df.pkl")  
class ARTest(Test):
    """
    
    Time consistency test (TCT) based on ARIMA model. 
    
    https://towardsdatascience.com/find-the-order-of-arima-models-b4d99d474e7a
    
    TODO: implement an ensemble forecast trained on noisy data for good 
    stimation of uncertainty values. Needs to be PARALLEL for avoiding 
    long computation times.
    
    TODO: account uncertainty of the estimation in the outlier score.
    
    """
    
    
    pbounds = {'p0': (0., 10.)}
    
    def fit(self, df_name):
        
        """

        Parameters
        ----------
        df_name : The data frame from which the data should be extracted for fitting
        the ARIMA model. 

        Returns
        -------
        None.

        """
        
        xs, f= create_sets(self.station, 'train')
        ys= f(xs) #prepare_points
        
        ys+=  3.*np.random.randn(len(ys)) # Add some noise for robust fit

        y_flip= np.flip(ys, axis=None)
        
        mod = ar_select_order(ys, maxlag=13)
        
        self.ar_past2 = ARIMA(endog=ys, order=(mod.ar_lags,0,0),  trend='n', missing= 'drop').fit(low_memory=True).apply
        self.ar_fut2 = ARIMA(y_flip, order=(mod.ar_lags,0,0),  trend='n',  missing= 'drop').fit(low_memory=True).apply
        # TODO: Tengo que cargarme este mastodonte de memoria
        
        self.mod= int(len(mod.ar_lags)) #unnecesary variable
        
        del(xs,f, ys, y_flip, mod)
        return 
    
    def prepare_points(self, df_name):
        self.xs, self.f = create_sets(self.station , df_name) 
        self.ys= self.f(self.xs)
        return        
    
    def remove_points(self):
        del(self.xs, self.ys, self.f)
        return 
    
    def evaluate(self, x, y, params):
        """
        Parameters
        ----------
            - (x,y): point coordinates in the time series of the station being analyzed
            - thr: score below which a station is labelled as outlier
  
        Returns
        -------
            - Boolean: test result (True/False)
        """
        
        i_trgt= np.where(x==self.xs)[0][0]
        if(i_trgt<self.mod):
            ys2= self.ys[:i_trgt+self.mod].copy() #TRIAL
        elif(i_trgt>len(self.ys)-self.mod):
            ys2= self.ys[i_trgt-self.mod:].copy() #TRIAL
        else:
            ys2= self.ys[i_trgt-self.mod:i_trgt+self.mod].copy()
        
        ys2[self.mod-1]=y
                
        y_flip= np.flip(ys2, axis=None)

        ar_model_past= self.ar_past2(endog=ys2, refit=False, missing='drop')
        ar_model_fut= self.ar_fut2(endog=y_flip, refit=False, missing='drop')

        pred_past = ar_model_past.predict(start=self.mod, end=self.mod, dynamic=False)
        pred_fut = np.flip(ar_model_fut.predict(start=self.mod-1, end=self.mod-1, dynamic=False))
        pred_mean=np.mean([pred_past, pred_fut]) #divide by std?????
    
        # TODO: investigate uncertainty accountance for bad predictions
        diff=abs(y - pred_mean)
        if diff>params['p0']:
            return True
        else:
            return False
    

        
 
#%%


#test=ARTest.init_cached('',6096)
#%%
#test.fit('train')
#test.fit('train')

"""
test.prepare_points('test')


#%%
test.optimize(1.5)
#%%
from tests.test_base_class import Test
test.save_cached('../data_files/test_pkls/AR')
#test.fit('train')
"""
#%%

"""
#%%

test.fit('test')

test.prepare_points('test')


xs,f=create_sets(4201, 'test')

plt.figure()



#%%
mean_y= np.mean(f(xs))
std_y= np.std(f(xs))
for x in xs:
    if(test.evaluate(x, f(x), 1.46755 )):
        plt.plot(x,f(x), 'r.')
    else:
        plt.plot(x,f(x),'b.')
        
"""
"""

from scipy.stats import pearsonr
import matplotlib.pyplot as plt
import time

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