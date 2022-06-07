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


class buddy_check(Test):
    
    pbounds = {'radius': (0., 10000.), 'num_min':(0.,  5000), 'min_std': 1}
    
    def prepare_points(self,df_name=None):    

        self.xs, _ = create_sets(self.station , df_name) 
        
        self.fs, self.points, self.obs_to_check = prepare_test(self.station, df_name)
        self.i= self.obs_to_check.index(1)

    def evaluate(self,x,y,params):

        values=[]
        for f in self.fs:
            values.append(f(x).tolist())
        values[self.i]=y.tolist()
        aux=titanlib.buddy_check(self.points, values,  radius= params['radius'] , 
                                 num_min= params['num_min'], threshold= params['threshold'], 
                                 max_elev_diff = -1, 
                                 elev_gradient = -0.0065, min_std= params['min std'],
                                 num_iterations = 1,obs_to_check=self.obs_to_check)[self.i]
        return aux

def my_SCT(station, df_name=None):    
    num_min = 5
    num_max = 100
    num_iterations = 1
    num_min_prof = 20
    min_elev_diff = 200
    min_horizonal_scale=10000
    vertical_scale = 200

    xs, _ = create_sets(station,df_name)

    fs, points, obs_to_check = prepare_test(station,df_name)
    

    eps2 = np.full(points.size(), 0.5)
    
    i= obs_to_check.index(1)

    def aux_SCT(x,y,params):
        pos = np.full(points.size(), params[0])
        neg = np.full(points.size(), params[1])
        inner_radius = params[2]
        outer_radius = params[2]+params[3]
        
        
        values=[]
        for f in fs:
            values.append(f(x).tolist())
        values[i]=y.tolist()
        aux=titanlib.sct(points, values, num_min, num_max, inner_radius, outer_radius,
            num_iterations, num_min_prof, min_elev_diff, min_horizonal_scale, vertical_scale,
            pos, neg, eps2)[0][i]
        # TODO: find why I cannot add obs_to_check
        return aux
    return aux_SCT