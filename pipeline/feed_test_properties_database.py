#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  7 16:10:31 2022

@author: tobou
"""
import sys
sys.path.insert(0, '..')
import os

from tests.AR import ARTest
from tests.SCT import STCT     # TODO: see how to make it dynamical for new tests without reinstalling the full package
import pandas as pd

df_train=  pd.read_pickle("/home/tobou/Desktop/Meteorological_Data_quality_assesment/df_gen/df_train.pkl")  

path_test_properties= '../data_files/test_pkls'


def feed_db(test_names, std, stations):

    for test_name in test_names:
        for station in stations:
            print(test_name, station)
            
            try:
                dirname= os.path.join(path_test_properties, test_name)
                print(dirname)
                #TODO: consider remove test creation from function.
                if(test_name=='ARTest'):
                    
                    test=ARTest.init_cached(dirname, station)
                    if(test.tuning_status):
                        print(test.tuning_status)
                        continue
                    #test.prepare_points('train')
                elif(test_name=='STCT'):
                    test=STCT.init_cached(dirname, station)
                else:
                    print(f'test {test_name} not defined')
                
                test.fit('train')
                test.optimize(std)
                test.tuning_status=True
                test.save_cached(dirname) #TODO make sort that if dir doesnt exist it creates it
                
    
            
            except:
                print('there was an error')
                continue
            
            
        
    return 

feed_db(['STCT','ARTest'], 2.5,df_train['station'].unique())