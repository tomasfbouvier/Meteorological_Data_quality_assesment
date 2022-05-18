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
import ast

path_test_properties= '../data/test_properties/'



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
    
    def aux(x, y):
        pos_prob = 0.5 
        print('asdasd',test_properties)
        for i in range(len(test_properties)):
            test_name= test_properties.iloc[i]['test_name']
            if test_name == 'build_pdfs':
                params=  ast.literal_eval(test_properties.iloc[i]['params'])[0]
                test= build_pdfs(station)
                
            elif test_name == 'SCT':
                test= my_SCT(station)
            elif test_name == 'buddy_check':
                test= my_buddy_check(station)
            
            
            llh= np.array([[test_properties.iloc[i]['TPR'],
                            test_properties.iloc[i]['FNR']],
                           [test_properties.iloc[i]['FPR'], 
                            test_properties.iloc[i]['TNR']]])
                 
                
            idx= int(not(test(x,y, params))); print(idx)
            print(llh[idx, 0],(llh[idx, 0]*pos_prob + llh[idx, 1]*(1-pos_prob)) , llh[idx,0], llh[idx,0] )
            pos_prob*= llh[idx, 0]/(llh[idx, 0]*pos_prob  + llh[idx, 1]*(1-pos_prob))
            
            

        
        return pos_prob
    
    
    
    return aux