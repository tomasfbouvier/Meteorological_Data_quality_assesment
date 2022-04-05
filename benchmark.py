#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  4 21:07:11 2022

@author: tomasfernandezbouvier
"""

import numpy as np

def calculate_acc(x, f, test, params, n_trials= 100, std=1.5):
    
    """
    Parameters
    ----------
        - x and f: time series stamp and interpolator corresponding to the station to be evaluated
        - test: the test function to be benchmarked
        - params: the hyperparameters of the test
        - n_trials: number of synthetic anomalies to be generated for testing 
    
    Outputs:
    --------
        - Confusion matrix: [[True Postivies, False Negatives][False Positives, True Negatives]]
        
        
    TODO: Implement a version which is robust to initially corrupe
        
    """
    
    def create_outlier(y):
        
        """
        Parameters
        ----------
            - y: nominal value to be inputed
            - previous_status: previous inputation process (True or False)
        Outputs:
        --------
            - Confusion matrix: [[True Postivies, False Negatives][False Positives, True Negatives]]
            
        TODO
        ----
        Implement multiple sources of error for a better benchmark.
        """
        i= np.random.randint(0, len(y))
        
        out= 0. #2*std*np.random.rand()-std
        
        if(out<0.):
            out-=std
        else:
            out+=std 
        return i, out
    
    
    TP=0; FP=0; TN=0; FN=0;
    outlier_status=False
    
    y=f(x)
    for trial in range(n_trials):
        if(trial%2==0):
            idx_out, out = create_outlier(y)
            outlier_status=True
            
        else:
            idx_out, out, outlier_status= (np.random.randint(0, len(y)), 0., False)
        
        y[idx_out]+= out
    
        test_result= test(x[idx_out], y[idx_out], params)

        if(test_result==True and outlier_status==True):
            TP+=1
        elif(test_result==True and outlier_status==False):
            FP+=1
        elif(test_result==False and outlier_status==False):
            TN+=1
        elif(test_result==False and outlier_status==True):
            FN+=1
        
        y[idx_out]-= out
            
    TPR= TP/(TP+FN); TNR= TN/(TN+FP); FNR= FN/(TP+FN); FPR=FP/(TN+FP)
    confusion_matrix= np.array([[TPR, FNR],[FPR, TNR]])
    return confusion_matrix
