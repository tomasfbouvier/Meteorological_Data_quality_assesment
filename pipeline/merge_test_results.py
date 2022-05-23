#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 17 14:23:05 2022

@author: tobou
"""

import sys
sys.path.insert(0, '..')

import pandas as pd
import numpy as np
from tests.SCT import build_pdfs
from tests.my_titanlib import my_SCT, my_buddy_check
from tests.newAR import AR_test
import ast

path_test_properties= '../data_files/test_properties/'



def multi_test(std, station):
    
    file_name= path_test_properties+'test_properties_'+str(std).replace('.','_')+ '.csv'    
    
    try:
        test_properties= pd.read_csv(file_name, header=0,
                                     names=['station', 'test_name', 'params',
                                            'TPR', 'FNR', 'FPR', 'TNR'])
        test_properties= test_properties[test_properties['station']==station]
    except: 
        print('file ' +file_name+ ' does not exist!')
        
        return 

    llhs=[]; param_list=[]; tests=[]
    print(test_properties)
    for i in range(len(test_properties)):
        test_name= test_properties.iloc[i]['test_name']
        if test_name == 'build_pdfs':
            params=  ast.literal_eval(test_properties.iloc[i]['params'])[0]
            test= build_pdfs(station)
        elif test_name == 'SCT':
            params=  ast.literal_eval(test_properties.iloc[i]['params'])[0]

            test= my_SCT(station)
        elif test_name == 'buddy_check':
            params=  ast.literal_eval(test_properties.iloc[i]['params'])[0]

            test= my_buddy_check(station)
        if test_name== 'AR':
            params=  ast.literal_eval(test_properties.iloc[i]['params'])[0]

            test= AR_test(station)
        
        llh= np.array([[test_properties.iloc[i]['TPR'],
                        test_properties.iloc[i]['FNR']],
                       [test_properties.iloc[i]['FPR'], 
                        test_properties.iloc[i]['TNR']]])
        llhs.append(llh)
        param_list.append(params)
        tests.append(test)
    
    # Should add del
        
    def aux(x, y,  printer=False):
        pos_prob = 0.5 
        for i in range(len(llhs)):
            
            idx= int(not(tests[i](x,y, param_list[i])))
            
            # TODO: Add a bias value for avoiding exploding probabilities.
            
            if(printer): print(llhs[i], idx, llhs[i][idx, 0]*pos_prob  , llhs[i][idx, 1]*(1-pos_prob))
            pos_prob = pos_prob*llhs[i][idx, 0]/(llhs[i][idx, 0]*pos_prob  + llhs[i][idx, 1]*(1-pos_prob)) # Bayes update
            if(printer): print('pos_prob', pos_prob)
        return pos_prob
    
    
    
    return aux

import matplotlib.pyplot as plt
from preprocessing.create_sets import create_sets
xs,f= create_sets(4207)
aaa= multi_test(3.5,4207)
bbb= AR_test(4207)

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

for i in range(len(xs)):
    x= xs[i]; y= f(x);
    if(aaa(x,y, printer=False)>0.9):
        plt.plot(x, y, 'k.')
    else:
        plt.plot(x, y, 'b.')

