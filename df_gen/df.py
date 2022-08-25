#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  1 12:36:14 2022

@author: tomasfernandezbouvier
"""

import os
import numpy as np
import pandas as pd
import sys
sys.path.insert(0, '..')

from settings import variable


def aux_df(name, dirname, columns, start=None, end=None):

    df= pd.read_table(name, dtype=float, header=None, names= columns,sep='\s+').fillna(np.nan)
    df['timestamp'] = pd.to_datetime(df['timestamp'], format='%Y%m%d%H%M')
    if(start):
        df= df[df['timestamp']>=start]
    elif(end):
        df= df[df['timestamp']<=end]
    df['file_type']= dirname
    return df



def Create_df(start=None, end=None):
    df=pd.DataFrame();
    
    if(variable== 'Press'):
        columns=['station','timestamp','min', 'max']
    if(variable== 't2m'):
        columns=['station','timestamp','min', 'max', 'staturation']
    for dirname, _, filenames in os.walk('/home/tobou/data/combined'):
        for filename in filenames:
            
            try:
                datetime_str= filename.split('.', 1)[0]
                if(int(datetime_str[0:2])<23):
                    date=np.datetime64('20'+datetime_str[0:2]+'-'+datetime_str[2:4]+'-'+datetime_str[4:])
                else:
                    date=np.datetime64('19'+datetime_str[0:2]+'-'+datetime_str[2:4]+'-'+datetime_str[4:])

                if(str(variable) in filename):
                    if(start and date<start):
                        continue
                    elif(end and date>end):
                        continue
                    #print(filename)
                    df2=aux_df(str(dirname+'/'+filename), dirname, columns, start, end)
                    df=df.append(df2, ignore_index=True)
            except:
                print(f"error reading {filename}")
                pass                       
            



    return df



Create_df(start=np.datetime64('1997-01-01'), end=np.datetime64('1997-12-31')).to_pickle('/home/tobou/Desktop/Meteorological_Data_quality_assesment/df_gen/df_train.pkl')