#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  6 12:18:01 2022

@author: tobou
"""
import sys

sys.path.insert(0, '..')

import numpy as np
import pandas as pd
from preprocessing.create_sets import create_sets
import titanlib

def divide(x):
    return int(x/100)


df3= pd.DataFrame(np.loadtxt('../data_files/data/SynopFrIngres'),columns=['station', 'init', 'end', 'lat', 'lon', 'height'])

df3['station']= df3['station'].apply(divide)
df3= df3.drop_duplicates(subset='station')
#positions= df3[['lat', 'lon']].values

# TODO: remove drop duplicates and find a solution for updating the position of the stations dynamically

def get_stations(station, radius):
        
    lon= df3[df3['station']==station]['lon'].to_numpy()[0]
    lat= df3[df3['station']==station]['lat'].to_numpy()[0]    
    stations_in_range = df3 #df3[df3['lat'] > lat-radius ][df3['lat'] < lat+radius][df3['lon'] < lon+radius][df3['lon'] > lon-radius]
    return stations_in_range
    
    
#print(get_stations(6096, 1))
      
def prepare_test(station):
    surrounds= df3 #get_stations(station, 1000)
    #values= []
    points= []
    fs=[]
    obs_to_check=[]
    for station1 in surrounds['station']:
        try:
            x,f= create_sets(station1)
            #values.append(f(time_stamp).tolist())
            fs.append(f)
            points.append(df3[df3['station']==station1].to_numpy()[0,3:].tolist())
            if station1==station:
                obs_to_check.append(1)
            else:
                obs_to_check.append(0)
        except:
            pass
        
    points=np.array(points).T.tolist()
    points=titanlib.Points(points[0],points[1],points[2])
    return fs, points, obs_to_check
