#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 17 14:23:05 2022

@author: tobou
"""

import sys
sys.path.insert(0, '..')
from settings import variable
import os
from tests.AR import ARTest
from tests.STCT import STCT 
from scipy.stats import norm
from tests.my_titanlib import SCT, BuddyCheck


def multi_test(station, df_name='deploy'):
    
    path_test_properties= '../data_files/'+variable+'/test_pkls_3_5'
    
    tests=[]
    for dirname, _, filenames in os.walk(path_test_properties):
        
        for filename in filenames:
            if(str(station) in filename):
                
                #print(dirname)
                if('ARTest' in dirname):
                    tests.append(ARTest.init_cached(dirname, station))
                    tests[-1].prepare_points(df_name)
                
                elif('STCT' in dirname):
                    tests.append(STCT.init_cached(dirname, station))
                    tests[-1].prepare_points(df_name)
                elif('SCT' in dirname):
                    tests.append(SCT.init_cached(dirname, station))
                    tests[-1].prepare_points(df_name)
                    
                elif('BuddyCheck' in dirname):
                    #print(dirname)
                    tests.append(BuddyCheck.init_cached(dirname, station))
                    tests[-1].prepare_points(df_name)
    
            #tests[-1].optimize(1.5, df_name='test')
    
    log=[test.confusion_matrix for test in tests]
    #print(tests)

    
    #pos_prob= 0.1 #2*(1-norm(scale= 0.9).cdf(1.5))
    def evaluate(x,y):
        if variable=='Press':
            pos_prob=0.1
        elif variable=='t2m':
            pos_prob= 0.21 #flat prior ---> #TODO: adapt to well informed prior and transfer to config
        else:
            raise(Exception("variable not defined"))
        #print(x,y)
        for test in tests:
            try:
                idx= test.evaluate(x, y, test.params)
                #print(test)
                #print(idx)
            
                idx= int(not(idx))
            #print(test.confustationsion_matrix[idx, 0])#(test.confusion_matrix[idx, 0]*pos_prob  + test.confusion_matrix[idx, 1]*(1-pos_prob)))
                pos_prob = pos_prob*test.confusion_matrix[0, idx]/(test.confusion_matrix[0, idx]*pos_prob  + test.confusion_matrix[1, idx]*(1-pos_prob)) # Bayes update
            except:
                pass
        return pos_prob
    return evaluate, log

    


import matplotlib.pyplot as plt
from preprocessing.create_sets import create_sets

#df= pd.read_pickle("/home/tobou/Desktop/Meteorological_Data_quality_assesment/df_gen/df.pkl")
"""
aaa, log= multi_test(6151.0)
#bbb= AR_test(4207)
xs, f= create_sets(6151.0, 'deploy')


for i in range(0,  len(xs)):
    x= xs[i]; y= f(x);
    plt.plot(x,f(x), 'b.')
    
    if (i== len(xs)-50 ):
        #y=y+3.5
        #plt.plot(x, y+3.5, 'k.')
        res= aaa(x,y)
        
    res=aaa(x,y)
    #print(res)



    if(res>0.9):
        print(res)
        plt.plot(x, y, 'r.')
    else:
        plt.plot(x, y, 'b.')
"""
"""
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
