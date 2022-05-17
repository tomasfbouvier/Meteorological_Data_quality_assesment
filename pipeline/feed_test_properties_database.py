#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  7 16:10:31 2022

@author: tobou
"""
import sys
sys.path.insert(0, '..')

from tuning.benchmark import calculate_acc
from tuning.optimizer import optimize_test
from preprocessing.create_sets import create_sets
from tests.SCT import build_pdfs
from tests.my_titanlib import my_SCT, my_buddy_check

import pandas as pd


df=  pd.read_pickle("/home/tobou/Desktop/Meteorological_Data_quality_assesment/df_gen/df.pkl") 

path_test_properties= '../data/test_properties/'


def feed_test_properties_database(test_names, std, stations=df['station'].unique()):
    
    file_name= path_test_properties+'test_properties_'+str(std).replace('.','_')+ '.csv'
    
    try:
        test_properties= pd.read_csv(file_name, header=0,
                                     names=['station', 'test_name', 'params',
                                            'TPR', 'FNR', 'FPR', 'TNR'])
    except: 
        print('file ' +file_name+ ' does not exist!')
        test_properties= pd.DataFrame()
        test_properties.to_csv(file_name, index=False)
         
        return 
        
    for test_name in test_names:
        for station in stations:
            print('station ', station)
            try:
                if( not len(test_properties[test_properties['test_name']==test_name]
                            [test_properties['station']==station])):
                    xs, f = create_sets(station)
                    best=optimize_test(station, test_name, std, plot=False)
            
                    if test_name == 'build_pdfs':
                        test= build_pdfs(station)[0]
                    elif test_name == 'SCT':
                        test= my_SCT(station)
                    elif test_name == 'buddy_check':
                        test= my_buddy_check(station)
            
                    acc= calculate_acc(xs, f, test,list(best['params'].values())
                    , std=std, n_trials=10000)
                    
                    print(list(best['params'].values()),acc)
                    test_properties= test_properties.append({'station': station , 
                                                             'test_name': test_name,
                                                             'params': list(best['params'].values()),
                                                             'TPR': acc[0,0], 
                                                             'FNR': acc[0,1],
                                                             'FPR': acc[1,0],
                                                             'TNR': acc[1,1] },
                                                            ignore_index=True)
            
            except:
                print('there was an error')
                continue
            test_properties.to_csv(file_name, index=False)
            
     
    return 