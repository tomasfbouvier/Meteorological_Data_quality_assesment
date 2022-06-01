#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 30 13:24:40 2022

@author: tobou
"""

import sys
import matplotlib.pyplot as plt
from numba import jit

sys.path.insert(0, '..')

from bayes_opt import BayesianOptimization
from bayes_opt import SequentialDomainReductionTransformer

from preprocessing.create_sets import create_sets
import os
import _pickle as cPickle
import numpy as np



class Test():
    
    
    
    pbounds=None
    
    
    
    
    @classmethod
    def init_cached(cls, filepath, station):
        filename=os.path.join(filepath, str(station)+'.pkl' )
        if not os.path.exists(filename):  # create new

            result = cls(station)
            
            return result
        else:
            print('loaded file')
            with open(filename, 'rb') as fp:
                return cPickle.load(fp)
    
    def __init__(self, station):
        self.station= station
        print('Constructor called, test for station ' + str(self.station) + ' created.')
        
        
        return 
    
 
    def save_cached(self, filepath):
        
        removable_attributes= ['xs', 'ys', 'f'] #Maybe move this to daughters

        for attribute in dir(self):
            if(attribute in removable_attributes):
                delattr(self,attribute)
    
        filename=os.path.join(filepath, str(self.station)+'.pkl')
        output_file= open(filename, "wb")
        cPickle.dump(self, output_file)
    
    
    def calculate_acc(self, xs, ys, params, std, n_trials):
        
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
            
            
        TODO: Implement a version which is robust to initially corruped data
            
        """
        
        if not hasattr(self, 'evaluate') and callable(getattr(self, 'evaluate')):
            return
        
        
        
        def create_outlier(ys):
            
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
            i= np.random.randint(0, len(ys))
            
            # Explored ranges: >4.5, >3.5, >2.5, >1.5
            
            out= 2.*np.random.rand()-1. #2*std*np.random.rand()-std
            
            if(out<0.):
                out-=std
            else:
                out=+std 
            return i, out
        
        
        TP=0; FP=0; TN=0; FN=0;
        outlier_status=False
        
        for trial in range(n_trials):
            if(trial%2==0):
                idx_out, out = create_outlier(ys)
                outlier_status=True
                
            else:
                idx_out, out, outlier_status= (np.random.randint(0, len(ys)), 0., False)
            
            ys[idx_out]+= out
        
            test_result= self.evaluate(xs[idx_out], ys[idx_out], params)

            if(test_result==True and outlier_status==True):
                TP+=1
            elif(test_result==True and outlier_status==False):
                FP+=1
            elif(test_result==False and outlier_status==False):
                TN+=1
            elif(test_result==False and outlier_status==True):
                FN+=1
            
            ys[idx_out]-= out
                
        TPR= TP/(TP+FN); TNR= TN/(TN+FP); FNR= FN/(TP+FN); FPR=FP/(TN+FP)
        confusion_matrix= np.array([[TPR, FNR],[FPR, TNR]])
        return confusion_matrix


    def optimize_test(self, std):
        
        if(not(self.pbounds)):
            return 
        
        bounds_transformer = SequentialDomainReductionTransformer()
        xs, f = create_sets(self.station, df='test')
        ys= f(xs)
        del(f)
        
        def calculate_J(**kwargs ):
            confusion_matrix= self.calculate_acc(xs, ys,params=kwargs,std=std, n_trials= 100)
            J=(confusion_matrix[0,0]+confusion_matrix[1,1])/(sum(sum(confusion_matrix)))
            #J= 1 - confusion_matrix[0,0] + confusion_matrix[1,0]*1.9
            del(confusion_matrix)
            return J
        
        optimizer = BayesianOptimization(
            f=calculate_J,
            pbounds=self.pbounds,
            random_state=1,
            bounds_transformer=bounds_transformer 
        )

        optimizer.maximize(
            init_points=10,
            n_iter=20,
        )
        # TODO: consider add different number of trials for random exploration depending on number of hyperparams 
            #print(calculate_acc(x,f,test, [optimizer.max['params']['p0'],optimizer.max['params']['p1'],optimizer.max['params']['p2']],1000, stds[i]))
        
        del(xs, ys)
        return optimizer.max

 