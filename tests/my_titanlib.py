#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  6 12:54:23 2022

@author: tobou
"""
import sys

sys.path.insert(0, '..')

from preprocessing.create_sets import create_sets
from helper_functions.helper_functions_titanlib import prepare_test
import titanlib
import numpy as np
from tests.test_base_class import Test




class BuddyCheck(Test):
    pbounds = {'min std': (.5,.6),'threshold': (0.,3.), 'radius': (30000, 100000)}
    to_save=['confusion_matrix', 'params', 'tuning_status', 'acc', 'acc_train']
    
    max_elev_diff = 200
    elev_gradient = -0.0065
    num_iterations = 1
    
    def prepare_points(self, df_name):
        self.xs, _ = create_sets(self.station, df_name)

        self.fs, self.points, self.obs_to_check = prepare_test(self.station, df_name)
        self.i= self.obs_to_check.index(1)
        

    def evaluate(self,x,y,params):

        values=[]
        for f in self.fs:
            value=f(x)
            if(not np.isnan(value)):
                values.append(value.tolist())
            elif(len(values)):
                values.append(np.mean(values)) #DOES THIS MAKE ANY SENSE?????
            else:
                values.append(285)
        values[self.i]=y.tolist()
        
        #print(values)
        
        
        
        
        aux=titanlib.buddy_check(self.points, values, [params['radius']], 
                                 [4], params['threshold'],self.max_elev_diff, 
                                 self.elev_gradient, params['min std'], 
                                 self.num_iterations, self.obs_to_check)[self.i]

        return bool(aux)

class SCT(Test):    
    
    pbounds = {'pos': (0.,6.),'neg': (0.,10.), 'inner radius': (0, 100000), 'outer radius':(0, 200000)}
    to_save=['confusion_matrix', 'params', 'tuning_status', 'acc', 'acc_train']
    
    num_min = 5
    num_max = 100
    num_iterations = 1
    num_min_prof = 20
    min_elev_diff = 200
    min_horizonal_scale=10000
    vertical_scale = 200
    
    
    def prepare_points(self, df_name):
        self.xs, _ = create_sets(self.station, df_name)

        self.fs, self.points, self.obs_to_check = prepare_test(self.station, df_name)
        self.i= self.obs_to_check.index(1)
        

        self.eps2 = np.full(self.points.size(), 0.5)
    


    def evaluate(self, x,y,params):
        pos = np.full(self.points.size(), params['pos'])
        neg = np.full(self.points.size(), params['neg'])
        
        
        values=[]
        for f in self.fs:
            value=f(x)
            if(not np.isnan(value)):
                values.append(value.tolist())
            elif(len(values)):
                values.append(np.mean(values)) #DOES THIS MAKE ANY SENSE?????
            else:
                values.append(300)
        values[self.i]=y.tolist()

        #print(values)
        aux=titanlib.sct(self.points, values, self.num_min, self.num_max,
            params['inner radius'],params['inner radius']+params['outer radius'],
            self.num_iterations, self.num_min_prof, self.min_elev_diff, self.min_horizonal_scale,
            self.vertical_scale,pos, neg, self.eps2)[0][self.i]
        
        # TODO: find why I cannot add obs_to_check
        return bool(aux)
    



#test= SCT.init_cached('/home/tobou/Desktop/Meteorological_Data_quality_assesment/data_files/Press/test_pkls_3_5/BuddyCheck',6096.0)
#test.optimize(3.5)

"""
test.save_cached('../data_files/test_pkls_1_5/SCT')

del(test)
test= SCT.init_cached('../data_files/test_pkls_1_5/SCT',6096)
"""
