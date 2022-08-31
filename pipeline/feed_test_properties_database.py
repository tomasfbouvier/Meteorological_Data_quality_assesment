#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  7 16:10:31 2022

@author: tobou
"""
import sys
sys.path.insert(0, '..')
import os
from settings import variable
from tests.AR import ARTest
from tests.STCT import STCT     # TODO: see how to make it dynamical for new tests without reinstalling the full package
import pandas as pd
from tests.my_titanlib import BuddyCheck, SCT

df_train=  pd.read_pickle("/home/tobou/Desktop/Meteorological_Data_quality_assesment/df_gen/df_train.pkl")  

path_test_properties= '../data_files/'+ variable +'/test_pkls_3_5'


def feed_db(test_names, std, stations):

    for test_name in test_names:
        for station in stations:
            #test=BuddyCheck.init_cached(dirname, station)
            try:
                print('test name: ', test_name)
                print('station ', station)
                
                dirname= os.path.join(path_test_properties, test_name)
                #TODO: consider remove test creation from function.
                if(test_name=='ARTest'):
                    test=ARTest.init_cached(dirname, station)
                    if(test.mod<2):
                        test.tuning_status=False
                    test.fit('train')
                elif(test_name=='STCT'):
                    test=STCT.init_cached(dirname, station)
                    test.fit('train')
                elif(test_name=='BuddyCheck'):
                    test=BuddyCheck.init_cached(dirname, station)
                elif(test_name=='SCT'):
                    test=SCT.init_cached(dirname, station)
                    
                else:
                    print(f'test {test_name} not defined')
                if(test.tuning_status):
                    print('tuning status: ',test.tuning_status)
                    print(test.acc_train, test.acc)
                    continue
                
                test.optimize(std)
                test.tuning_status=True

            
            except:
            
                print(f'An error ocurred while feeding the database for station {station}')
                continue
            test.save_cached(dirname) #TODO make sort that if dir doesnt exist it creates it
                
            
            
        
    return 


feed_db(['ARTest'], 3.5,df_train['station'].unique()[:])
