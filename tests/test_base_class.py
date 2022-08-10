#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 30 13:24:40 2022

@author: tobou
"""

import sys

sys.path.insert(0, '..')

from bayes_opt import BayesianOptimization
from bayes_opt import SequentialDomainReductionTransformer

from preprocessing.create_sets import create_sets
import os
import _pickle as cPickle
import numpy as np


class Test():
    
    pbounds = None
    confusion_matrix = None 
    params= None
    tuning_status=False
    
    
    to_save=[]
    
    @classmethod
    def init_cached(cls, filepath, station):
        filename=os.path.join(filepath, str(station)+'.pkl' )
        #print(filename)
        if not os.path.exists(filename):  # create new
            #print('Constructor called, test for station ' + str(station) + ' created.')
            test = cls(station)
            
            return test
        else:
            #print('loaded file')
            with open(filename, 'rb') as fp:
                initial_data= cPickle.load(fp)
                test=cls(station)
                for key in initial_data:
                    setattr(test, key, initial_data[key])
                del(initial_data)
                return test
    
    def __init__(self, station):
        self.station= station
        self.tuning_status=False
        
        
        
        return 
    
    def save_cached(self, filepath):
        
        """
        TODO: consider saving to another format. E.g hdf5.
        
        """
        
        
        """
        
        removable_attributes= ['xs', 'ys', 'f', 'prepare_points', 'evaluate', 
                               'optimize', 'fit'] #Maybe move this to daughters
        
        
        for attribute in dir(self):
            if(attribute in removable_attributes):
                delattr(self,attribute)
        
        """
        aux={}
        for key in self.to_save:
            
            aux[key]=getattr(self, key)
        print(aux)
        filename=os.path.join(filepath, str(self.station)+'.pkl')
        output_file= open(filename, "wb+")
        cPickle.dump(aux, output_file)
        print('saved file')
    
    def calculate_acc(self, xs, ys, params, std, n_trials):
        
        """
        Parameters
        ----------
            - x and f: time series stamp and interpolator corresponding to the station to be evaluated
            - test: the test function to be benchmarked
            - params: the hyperparameters of the test
            - n_trials: number of synthetic anomalies to be generated for testing 
        
        Returns:
        --------
            - Confusion matrix: [[True Postivies, False Negatives][False Positives, True Negatives]]
            
            
        TODO: Implement a version which is robust to initially corruped data
            
        """
        
        if not hasattr(self, 'evaluate') and callable(getattr(self, 'evaluate')):
            return
        
        rho_pos=0.011; rho_neg=0.1
        T= np.array([[0.94371228 ,0.06422073],
         [0.05628772, 0.93577927]])#noise labels
        mult=T.T
        #mult=np.linalg.inv(T.T)#np.linalg.pinv(np.diag(np.array([0.296514, 0.703486])))@np.linalg.pinv(T)
        def create_outlier(ys):
            
            """
            Parameters
            ----------
                - y: nominal value to be inputed
                - previous_status: previous inputation process (True or False)
                
            Returns:
            --------
                - Confusion matrix: [[True Postivies, False Negatives][False Positives, True Negatives]]
                
            TODO
            ----
            Implement multiple sources of error for a better benchmark.
            """
            
            i= np.random.randint(0, len(ys))
            
            # Explored ranges: >4.5, >3.5, >2.5, >1.5
            
            out= 0#2.*np.random.rand()-1. #2*std*np.random.rand()-std
            
            if(np.random.rand()<0.5):
                out-=std
            else:
                out=+std 
            return i, out
        
        
        TP=1; FP=1; TN=1; FN=1; #Trying to smooth confusion matrix
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
                TP+=1; 
            elif(test_result==True and outlier_status==False):
                FP+=1; 
            elif(test_result==False and outlier_status==False):
                TN+=1;
            elif(test_result==False and outlier_status==True):
                FN+=1; 
            ys[idx_out]-= out
                
        TPR= TP/(TP+FN); TNR= TN/(TN+FP); FNR= FN/(TP+FN); FPR=FP/(TN+FP)
        confusion_matrix= np.array([[TPR, FNR],[FPR, TNR]])
        
        #print(confusion_matrix)
        
        confusion_matrix= mult@confusion_matrix
        
        #print(confusion_matrix)
        #print(confusion_matrix)
        #confusion_matrix2= np.array([[TP, FN],[FP, TN]])/(n_trials+4)

        #confusion_matrix=(mult@confusion_matrix2)
        #print(confusion_matrix)

        return confusion_matrix


    def optimize(self, std):
        
        if(not(self.pbounds) or not(self.prepare_points)):
            return 

        
        bounds_transformer = SequentialDomainReductionTransformer()
        xs, f = create_sets(self.station, 'train' ) # 'train' ????
        ys= f(xs)
        
        self.prepare_points('train')

        del(f)
        
        def calculate_J(xs=xs,ys=ys,**kwargs ):
            confusion_matrix= self.calculate_acc(xs, ys,params=kwargs,std=std, n_trials= 100)
            
            
            #J=(confusion_matrix[0,0]+confusion_matrix[1,1])/2.
            
            if np.any(confusion_matrix<0):
                J=-10
            else:
                J=-((confusion_matrix[0,0]+confusion_matrix[1,1])*0.5759394198788437+
                (confusion_matrix[0,1]+confusion_matrix[1,0])*0.8259394198788436)
                
                
            #J= 1 - confusion_matrix[0,0] + confusion_matrix[1,0]*1.9
            del(confusion_matrix, xs, ys)
            return J
        
        optimizer = BayesianOptimization(
            f=calculate_J,
            pbounds=self.pbounds,
            random_state=1,
            bounds_transformer=SequentialDomainReductionTransformer()
        )

        optimizer.maximize(
            init_points=20,
            n_iter=40,
        )
        # TODO: consider add different number of trials for random exploration depending on number of hyperparams 
            #print(calculate_acc(x,f,test, [optimizer.max['params']['p0'],optimizer.max['params']['p1'],optimizer.max['params']['p2']],1000, stds[i]))
        
        del(xs,ys)
        xs, f = create_sets(self.station, df_name='test') # 'train' ????
        ys= f(xs)
        
        self.prepare_points('test')
        
        self.params= optimizer.max['params']
        self.acc_train= optimizer.max['target']
        self.confusion_matrix= self.calculate_acc(xs, ys,params=self.params,std=std, n_trials= 1000)
        self.acc= (self.confusion_matrix[0,0]+self.confusion_matrix[1,1])/(sum(sum(self.confusion_matrix)))
        print(self.confusion_matrix)
        
        del(xs, ys, f)
        return 

 