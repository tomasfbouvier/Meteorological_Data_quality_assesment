#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  6 12:54:23 2022

@author: tobou
"""

from create_sets import create_sets
from helper_functions_titanlib import prepare_test
import titanlib
import numpy as np

def my_buddy_check(station):    
    max_elev_diff = -1 #200
    elev_gradient = -0.0065
    num_iterations = 50
    xs, _ = create_sets(station)

    fs, points, obs_to_check = prepare_test(station)
    i= obs_to_check.index(1)

    def aux_buddy_check(x,y,params):
        
        min_std = params[0]# 1 TO BE OPTIMIZED
        threshold = params[1]#2  TO BE OPTIMIZED
        radius= [params[2]]# [90000] TO BE OPTIMIZED
        num_min=[4] # TO BE OPTIMIZED ?
        
        values=[]
        for f in fs:
            values.append(f(x).tolist())
        values[i]=y.tolist()
        aux=titanlib.buddy_check(points, values,  radius ,num_min,threshold, max_elev_diff, elev_gradient, min_std, num_iterations,obs_to_check)[i]
        return aux
    return aux_buddy_check

def my_SCT(station):    
    num_min = 5
    num_max = 100
    num_iterations = 1
    num_min_prof = 20
    min_elev_diff = 200
    min_horizonal_scale=10000
    vertical_scale = 200

    xs, _ = create_sets(station)

    fs, points, obs_to_check = prepare_test(station)
    

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