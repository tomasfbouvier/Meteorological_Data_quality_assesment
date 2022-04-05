#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  1 12:36:14 2022

@author: tomasfernandezbouvier
"""

import os
import numpy as np
import pandas as pd



df=pd.DataFrame();
def Create_df(name):
    
    
    df= pd.DataFrame(np.loadtxt(name), columns=['station','timestamp','min', 'max'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], format='%Y%m%d%H%M')
    #df.describe()
    #df['station'].unique()
    df['file_type']= dirname

    #print(df)

    return df

for dirname, _, filenames in os.walk('data'):
    for filename in filenames:
        if 'Press' in filename:
            #print(dirname+filename)
            df2=Create_df(str(dirname+'/'+filename))
            df=df.append(df2, ignore_index=True)

        
df['min']=df['min'].replace(0, np.nan)        
df['max']=df['max'].replace(0, np.nan) 

df_true= df[df['file_type']=='data/Carra']

df=df[df['file_type']=='data/data1/combined']