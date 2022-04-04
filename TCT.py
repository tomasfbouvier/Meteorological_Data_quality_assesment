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

    X[:,0]/=scaling_factor_x
    X[:,1]/=scaling_factor_y

    def predict(x, y):
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

