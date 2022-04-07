#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  7 16:10:31 2022

@author: tobou
"""

from df import df
from benchmark import calculate_acc
from optimizer import optimize_test
from create_sets import create_sets
from SCT import build_pdfs
from my_titanlib import my_SCT, my_buddy_check

import pandas as pd

def feed_test_properties_database( stations= df['station'].unique()[-2:], test_names= ['build_pdfs']):
    
    try:
        test_properties= pd.read_csv('test_properties.csv', header=0, names=['station', 'test_name', 'params', 'confusion_matrix'])
    except: 
        return 
    
    
    print(test_properties)
    
    for test_name in test_names:
        for station in stations:
            if( not len(test_properties[test_properties['test_name']==test_name][test_properties['station']==station])):
                xs, f = create_sets(station)
                best=optimize_test(station, test_name, std=1.5, plot=False)
        
                if test_name == 'build_pdfs':
                    test= build_pdfs(station)[0]
                elif test_name == 'SCT':
                    test= my_SCT(station)
                elif test_name == 'buddy_check':
                    test= my_buddy_check(station)
        
                acc= calculate_acc(xs, f, test,list(best['params'].values())
                , std=1.5, n_trials=10000)
                test_properties= test_properties.append({'station': station , 'test_name': test_name, 'params': list(best['params'].values()),'confusion_matrix': acc }, ignore_index=True)
                
    
    test_properties.to_csv('test_properties.csv', index=False)
     
    return 