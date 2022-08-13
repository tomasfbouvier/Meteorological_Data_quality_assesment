#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 24 12:00:43 2022

@author: tobou
"""


import sys
sys.path.insert(0, '..')
from settings import variable, output_start_date, output_end_date

import numpy as np
import pandas as pd
#from pipeline.feed_test_properties_database import feed_db
from pipeline.merge_test_results import multi_test
#import os
#from datetime import datetime 
from preprocessing.create_sets import sanity_check
from df_gen.df import Create_df

#CONFIG
pd.options.mode.chained_assignment = None  # default='warn'

#TODO: be able to pass the desired variable to avoid bugs

"""
def pipeline(mode='w', variable='Press'):
    if(mode=='w'):
        def aux(std, test_names, split= np.datetime64('1997-06-15' )):
            
            df=Create_df(variable, start= None, end=split)
            df.to_pickle("/home/tobou/Desktop/Meteorological_Data_quality_assesment/df_gen/df_train.pkl")  
            del(df)
            df=Create_df(variable, start= split + np.timedelta64(1,'D') , end= None)
            df.to_pickle("/home/tobou/Desktop/Meteorological_Data_quality_assesment/df_gen/df_test.pkl")    
            del(df)
            stations=  pd.read_pickle("/home/tobou/Desktop/Meteor    df2[df2['max'] <= 0] = np.nanological_Data_quality_assesment/df_gen/df_train.pkl")['station'].unique()
            feed_test_properties_database(test_names, std, stations)
            
            return
    elif(mode=='d'):
        df=Create_df(variable)
        df.to_pickle("df.pkl")  
        del(d2001-01-31'f)
        def aux(std, station):temp
            return multi_test(std, station)
    return aux                print(self.correlated_stations[target_station])

"""

Create_df(variable, start=np.datetime64(output_start_date),
          end=np.datetime64(output_end_date)).to_pickle(
              '/home/tobou/Desktop/Meteorological_Data_quality_assesment/df_gen/df_deploy.pkl')

df_output = pd.read_pickle("/home/tobou/Desktop/Meteorological_Data_quality_assesment/df_gen/df_deploy.pkl") 
stations = df_output['station'].unique()

print(stations)
#ATTEMPTING TO CORRECT 1 MONTH DATA. HORRIBLE I/O. TO BE TRANSFERRED TO R + BASH 

#df_output= df_deploy.copy()

#sanity_check(df_output)

if variable == 't2m':
    low_lim  = 184.0
    high_lim = 327.0
elif variable == 'Press':
    low_lim  = 870.0
    high_lim = 1083.8
def preprocessing(x):
    
    if(x == np.nan):
        return False
    elif(x < low_lim):
        return False
    elif(x > high_lim):
        return False
    else:
        return True
    
"""
dirname='../data_files/data_output'
variable='t2m'

if(variable== 'Press'):
    columns=['station','timestamp','min', 'max']
if(variable== 't2m'):
    columns=['station','timestamp','min', 'max', 'staturation']


for _,_, filenames in os.walk(dirname):2001-01-31'
    for filename in filenames:
        if variable in filename:a.tr
            df_output=pd.read_table(os.path.join(dirname,filename), names=columns, sep='\s+')
# Replace the target stringvariablea.tr
"""

### CORRECTION


correction_info = []


for station in stations[:4]:
    print(f'station: {station}')
    try:
        test_ensemble, log = multi_test(station)
        n = 0; c = 0;b = 0
        for (idx,row) in df_output[df_output['station'] == station].iterrows():
            n += 1
            #idx(row[0])
            x = row[1].to_numpy('datetime64[h]')
            y = np.array(row[3])
            
            if(preprocessing(y)):
                
                
                if(test_ensemble(x,y)>0.5):
                    df_output.iloc[idx]['max'] = -1
                    c+=1
            else:
                b+=1                
                
                df_output.iloc[idx]['max'] = -1
            
        correction_info.append({'station':station, 'points':n, 'bad':b, 'corrected':c, 'acc':
                                [np.trace(a)/2. for a in log]})
    

    except: 
        correction_info.append({'station':station, 'points':-1, 'corrected':-1, 'acc':
                                -1})
        print('problem with station ', station)
        continue 
    





### WRITE


correction_info=pd.DataFrame(correction_info)

def convert_dt_str(dt):
    
    dt_str = str(dt)
    dt_str = dt_str.replace(':', '')
    dt_str = dt_str.replace('-', '')
    dt_str = dt_str.replace(' ', '')
    #dt_str = dt_str[:-2]    
    
    return dt_str

df_output.dropna(subset=['timestamp'], inplace=True)
df_output.sort_values(by=['timestamp'])
days= np.sort(df_output.dropna(subset=['timestamp'], 
                                 inplace=False)['timestamp'].dt.date.unique())

df_output['timestamp']= df_output['timestamp'].apply(lambda x: convert_dt_str(x)[:-2])


if variable=='Press':
    fmt = ['%d', '%d', '%f', '%f']
if variable == 't2m':
    fm = ['%d', '%d', '%f', '%f', '%f']

for day in days:
    df_to_write= df_output[df_output['timestamp'].apply(lambda x: convert_dt_str(day) in x)]
    df_to_write['timestamp']=df_to_write['timestamp'].apply(lambda x: int(x))
    
    df_to_write.fillna(-1, inplace=True)
    
    np.savetxt( '../data_files/data_output/'+convert_dt_str(day)[2:]+'.'+variable ,
               df_to_write.drop(columns=['file_type']).values, fmt= fmt)
    