#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  6 15:13:59 2022

@author: tobou
"""

import sys

sys.path.insert(0, '..')

from bayes_opt import BayesianOptimization
from bayes_opt import SequentialDomainReductionTransformer

from preprocessing.create_sets import create_sets
from tuning.benchmark import calculate_acc
from tests.TCT import time_consistency_test
from tests.SCT import build_pdfs
from tests.my_titanlib import my_buddy_check, my_SCT
from tests.newAR import AR_test
import matplotlib.pyplot as plt


def optimize_test(station, name, std, plot=True):
    
    if(name=='buddy_check'):
        pbounds = {'p0': (.5,.6),'p1': (0.,3.), 'p2': (30000, 100000)}
        test= my_buddy_check(station, df='train')
    elif(name=='SCT'):
        pbounds = {'p0': (0.,6.),'p1': (0.,6.), 'p2': (0, 100000), 'p3':(0, 200000)}
        test= my_SCT(station, df='train')
    elif(name=='build_pdfs'):
        pbounds = {'p0': (0., 1.)}
        test = build_pdfs(station, df='train')
    
    elif(name=='DBSCAN'):
        pbounds = {'p0': (0.0001, 2.), 'p1':  (0.0001, 2.)}
        test= time_consistency_test(station, df='train')
    elif(name=='AR'):
        pbounds = {'p0': (0., 10.)}
        test= AR_test(station, 'train')
        
    else:
        print('wrong name 1')
    
    
    
    bounds_transformer = SequentialDomainReductionTransformer()

    x, f = create_sets(station, df='train')
    
    def calculate_J(std, c='b.',label=None):
        if(name=='buddy_check'):
            def aux(p0,p1,p2):
                params=[p0,p0+p1,p2] # p1 cannot be lower than p0
                confusion_matrix= calculate_acc(x,f,test, params,1000, std)
                #J= 1 - confusion_matrix[0,0] + confusion_matrix[1,0]*1.98 
                J=(confusion_matrix[0,0]+confusion_matrix[1,1])/(sum(sum(confusion_matrix)))
                if plot==True:
                    plt.plot(confusion_matrix[1,0], confusion_matrix[0,0], c, label=label)
                return J
        elif(name=='SCT'):
            def aux(p0,p1,p2,p3):
                params=[p0,p1,p2, p3]
                confusion_matrix= calculate_acc(x,f,test, params,1000, std)
                #J= 1 - confusion_matrix[0,0] + confusion_matrix[1,0]*1.98 
                J=(confusion_matrix[0,0]+confusion_matrix[1,1])/(sum(sum(confusion_matrix)))
                if plot==True:
                    plt.plot(confusion_matrix[1,0], confusion_matrix[0,0], c, label=label)
                return J
        elif(name=='build_pdfs' or name== 'AR'):
            def aux(p0):
                params=[p0] 
                confusion_matrix= calculate_acc(x,f,test, params,200, std)
                #J= 1 - confusion_matrix[0,0] + confusion_matrix[1,0]*1.98 
                J=(confusion_matrix[0,0]+confusion_matrix[1,1])/(sum(sum(confusion_matrix)))
                if plot==True:
                    plt.plot(confusion_matrix[1,0], confusion_matrix[0,0], c, label=label)
                return J
        elif 'DBSCAN´':
            def aux(p0,p1):
                params=[p0,p1] 
                confusion_matrix= calculate_acc(x,f,test, params,1000, std)
                #J= 1 - confusion_matrix[0,0] + confusion_matrix[1,0]*1.98 
                J=(confusion_matrix[0,0]+confusion_matrix[1,1])/(sum(sum(confusion_matrix)))
                if plot==True:
                    plt.plot(confusion_matrix[1,0], confusion_matrix[0,0], c, label=label)
                return J
            
            
        else:
            print('wrong name 2')
            return 
        return aux


    optimizer = BayesianOptimization(
        f=calculate_J(std=std, label='$\sigma = $'+str(std)),
        pbounds=pbounds,
        random_state=1,
        bounds_transformer=bounds_transformer 
    )

    optimizer.maximize(
        init_points=15,
        n_iter=20,
    )
    # TODO: consider add different number of trials for random exploration depending on number of hyperparams 
        #print(calculate_acc(x,f,test, [optimizer.max['params']['p0'],optimizer.max['params']['p1'],optimizer.max['params']['p2']],1000, stds[i]))

    return optimizer.max
