#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 17 18:39:11 2022

@author: tomasfernandezbouvier
"""

from create_sets import create_sets
import numpy as np
import pandas as pd
from df import df
import time as timeit

def divide(x):
    return int(x/100)


df3= pd.DataFrame(np.loadtxt('data/SynopFrIngres'),columns=['station', 'init', 'end', 'lat', 'lon', 'height'])
df3['station']= df3['station'].apply(divide)
df3= df3.drop_duplicates(subset='station')


def geostrophic_wind_computation(my_station):
    """
    Computes the gradient of the pressure field at a given time in order to find possible aberrant values for the wind
    
    Parameters
    ----------
        - time: timestamp of the gradient to calculate
    
    Outputs
    --------
        - (gradp_x, gradp_y): 2D gradient in cartesian(?) coordinates
        - x: point grid of the time-stamp
        
    
    TODO: 
        - Improve the wind from the gradient 
        - Compute the subsequent outlier classification based on aberrant values
        
        
        
    Questions:
        - Is height important? 2D or 3D gradient?
        
    """
    
    x=[] ; fs=[]; lats=[]
    station_list=df3['station'].unique()
    r=6.371*1e6 # [m]

    for i in range(len(station_list)):
        station=station_list[i]
        if station in list(df['station'].unique()):
            fs.append(create_sets(station)[1])
            phi, theta= df3[df3['station']==station][['lat', 'lon']].values[0]*np.pi*1./180.
            x.append([r*np.cos(theta)*np.sin(phi),r*np.sin(theta)*np.sin(phi)])
            lats.append(phi)
            if(station==my_station):
                j=len(fs)


    x =np.array(x)
    
    def aux(time, thr):
        #f_param= 1e-4 #[s-1]    7.2921e-5*2*np.sin(x[:,0]) 
        y=[]
        for f in fs:
            y.append(float(f(time))*1e2) # [Pa]
        vx= np.gradient(y, x[:,0])/(1.29*7.2921e-5*2*np.sin(lats[:]))
        vy= np.gradient(y, x[:,1])/(1.29*7.2921e-5*2*np.sin(lats[:]))
        
        v= np.sqrt(vx*vx+vy*vy)
        if(v[j]>thr):
            return True
        else:
            return False

    return aux, x



