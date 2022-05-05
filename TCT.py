#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  1 14:21:05 2022

@author: tomasfernandezbouvier
"""

from sklearn.cluster import DBSCAN
import numpy as np
from create_sets import create_sets
import matplotlib.pyplot as plt

def time_consistency_test(station):
    """
    Parameters
    ----------
        - station: objective station from which the time-series points will be clustered
    Output
    ------
        - predict: closure functiuon that evaluates wether a given point belongs to a cluster or not
    """
    
    xs, f= create_sets(station)
    ys= f(xs)


    y_steps= [abs(ys[i+1]-ys[i]) for i in range(len(ys)-1)]
    x_steps= [abs(xs[i+1]-xs[i]) for i in range(len(xs)-1)]
    
    
    scale_x= np.mean(x_steps)
    scale_y= np.mean(y_steps)




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
        
        
        i= np.where(x==xs)[0]
        
        ys[i]=y
        
        #print(i)
        sub_xs= [xs[j] for j in range(len(xs)) if xs[j]>xs[i]-100*scale_x and xs[j]<xs[i]+100*scale_x]
        sub_ys= [ys[j] for j in range(len(xs)) if xs[j]>xs[i]-100*scale_x and xs[j]<xs[i]+100*scale_x]
        
        #print(sub_xs, sub_ys)
        
        i= np.where(x==sub_xs)[0]
        
        sub_xs/= scale_x
        sub_ys/= scale_y
        
        X=np.array([sub_xs, sub_ys]).T
        
        labels = DBSCAN(eps=params[0],min_samples=params[1], metric='euclidean').fit_predict(X)

        del(X)
        
        if(labels[i]==-1):
            return True
        else:
            return False
    return predict


model= time_consistency_test(4201)
xs,f= create_sets(4201)

ys=f(xs)



from time import time

start= time()
for i in range(len(xs)):
    if model(xs[i],ys[i], [4., 2]):
        plt.plot(xs[i],ys[i], 'r.')
    else:
        plt.plot(xs[i],ys[i], 'b.')
        
print(time()-start)