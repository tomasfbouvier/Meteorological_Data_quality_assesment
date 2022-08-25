#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 10:40:56 2022

@author: tomasfernandezbouvier
"""

import sys
sys.path.insert(0, '..')

from preprocessing.create_sets import create_sets
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.ar_model import ar_select_order
from statsmodels.tsa.seasonal import STL
from statsmodels.tsa.stattools import acf


import numpy as np


from tests.test_base_class import Test

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
    
    to_save = ['confusion_matrix', 'params', 'tuning_status', 'acc', 'acc_train', 'ar_past2', 'ar_fut2', 'mod']

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
        
        thr=int(0.25*len(ys)); 
        #ys+=  3.*np.random.randn(len(ys)) # Add some noise for robust fit

        y_flip= np.flip(ys, axis=None)
        
        mod = ar_select_order(ys[:thr], maxlag=10, glob=True, seasonal=False) 
        #valid for temps
        
        print(mod.ar_lags)
        
        
        self.ar_past2 = ARIMA(endog=ys[thr:], order=(mod.ar_lags,0,0), seasonal_order=(0,0,0,0),
                              trend=None, missing= 'drop').fit(low_memory=True)
        weight_past= 1.001**self.ar_past2.llf #arbitraty
        self.ar_past2= self.ar_past2.apply
        
        self.ar_fut2 =  ARIMA(endog=y_flip[:thr], order=(mod.ar_lags,0,0), seasonal_order=(0,0,0,0),
                              trend=None, missing= 'drop').fit(low_memory=True)
        weight_fut= 1.001**self.ar_fut2.llf #arbitraty
        
        
        self.weights=[]
        if weight_past in [0., 1.]:
            self.weights.append(np.nan)
        else:
            self.weights.append(weight_past)
        if weight_fut in [0., 1.]:
            self.weights.append(np.nan)
        else:
            self.weights.append(weight_fut)
            
        self.ar_fut2= self.ar_fut2.apply
        self.lags= mod.ar_lags
        self.mod= int(len(mod.ar_lags))
        self.time_step = round(np.mean([xs[i]-xs[i-1] for i in range(1, len(xs))]).astype('float')/60)
#df=  pd.read_pickle("../df_gen/df.pkl")  
        del(xs,f, ys, y_flip, mod)
        return 
    
    def prepare_points(self, df_name):
        self.xs, self.f = create_sets(self.station , df_name) 
        #print(self.xs)
        self.ys= self.f(self.xs)
        return        
    
    def remove_points(self):
        del(self.xs, self.ys, self.f)
        return 
        #df=  pd.read_pickle("../df_gen/df.pkl")  
    
    def check_adjacent(self, x, direction):
        for t in self.lags: 
            if(len(np.where(x - t*np.timedelta64(self.time_step,'h')==self.xs)[0])==0):
                return True
        return False
            
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
            ys2= self.ys[:i_trgt+self.mod].copy() #TRIAL#import matplotlib.pyplot as plt # remove
        elif(i_trgt>len(self.ys)-self.mod):
            ys2= self.ys[i_trgt-self.mod:].copy() #TRIAL
        else:
            ys2= self.ys[i_trgt-self.mod:i_trgt+self.mod].copy()
        
        ys2[self.mod-1]=y
        
        if(self.check_adjacent(x, 'left')):
            pred_past= np.nan
        else:    
            ar_model_past= self.ar_past2(endog=ys2, refit=False, missing='drop')
            pred_past = ar_model_past.predict(start=self.mod, end=self.mod, dynamic=False)[0]
           
        if(self.check_adjacent(x, 'right')):
            pred_fut= np.nan
        else:
            y_flip= np.flip(ys2, axis=None)
            ar_model_fut= self.ar_fut2(endog=y_flip, refit=False, missing='drop')
            pred_fut = np.flip(ar_model_fut.predict(start=self.mod-1, end=self.mod-1, dynamic=False))[0]

        pred_mean= np.nansum(np.array([pred_past, pred_fut])*self.weights)/np.nansum(self.weights)
        
        diff=abs(y - pred_mean)
        
        if diff==np.nan:
            raise Exception('test inconclusive')
        elif diff>params['p0']:
            return True
        else:
            return False
    
    def should_pickle(k):
        
        
        removable_attributes= ['xs', 'ys', 'f', 'prepare_points', 'evaluate', 
                               'optimizteste', 'fit']
        if k in removable_attributes:
            print('deleting ' + k)
            return False
        else:
            return True

        
 
#%%



#df=  pd.read_pickle("../df_gen/df.pkl")  
test=ARTest(6193)#import matplotlib.pyplot as plt # remove
test.fit('train')

import time
start_time = time.time()
test.optimize(3.5)
print("--- %s seconds ---" % (time.time() - start_time))

