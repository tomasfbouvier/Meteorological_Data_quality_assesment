#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 17 14:23:05 2022

@author: tobou
"""

import sys
sys.path.insert(0, '..')

import os
path_test_properties= '../data_files/test_properties2/'


from tests.AR import ARTest
from tests.SCT import STCT 


def multi_test(station, df_name='deploy'):
    
    path_test_properties= '../data_files/test_pkls_1_5'

    for dirname, _, filenames in os.walk(path_test_properties):
        tests=[]
        for filename in filenames:
            if(str(station) in filename):
                if('ARTest' in dirname):
                    tests.append(ARTest.init_cached(dirname, station))
                    tests[-1].prepare_points(df_name)
                elif('STCT' in dirname):
                    tests.append(STCT.init_cached(dirname, station))
                    tests[-1].prepare_points(df_name)
                
    def evaluate(x,y):
        
        pos_prob= 0.5 #flat prior ---> #TODO: adapt to well informed prior.
        for test in tests:
            idx= int(not(test.evaluate(x, y, test.params)))
            pos_prob = pos_prob*test.llh[idx, 0]/(test.llh[idx, 0]*pos_prob  + test.llh[idx, 1]*(1-pos_prob)) # Bayes update
        return pos_prob
    return evaluate

    
   
"""
import matplotlib.pyplot as plt
from preprocessing.create_sets import create_sets

df= pd.read_pickle("/home/tobou/Desktop/Meteorological_Data_quality_assesment/df_gen/df.pkl")
xs,f= create_sets(4207)
aaa= multi_test(3.5,4207, df)
bbb= AR_test(4207)
"""
"""
for i in range(len(xs)):
    x= xs[i]; y= f(x);
    
    if(aaa(x, y)>0.9 and bbb(x,y, 1.477 )):
        aaa(x,y, printer=True)
        plt.plot(x, y, 'k.')
    elif(aaa(x,y)>0.9):
        #aaa(x,y, printer=True)
        plt.plot(x, y, 'r.')
    else:
        plt.plot(x, y, 'b.')
"""
"""
for i in range(len(xs)):
    x= xs[i]; y= f(x);
    if(aaa(x,y, printer=False)>0.9):
        plt.plot(x, y, 'k.')
    else:
        plt.plot(x, y, 'b.')
"""
