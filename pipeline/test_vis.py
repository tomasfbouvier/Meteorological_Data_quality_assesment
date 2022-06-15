#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  9 13:39:42 2022

@author: tobou
"""
import sys
sys.path.insert(0, '..')

import os
import pandas as pd
import _pickle as cPickle
import numpy as np
import matplotlib.pyplot as plt

df=pd.DataFrame(columns=['test', 'station', 'acc_train', 'acc'])

parent_dir_name= '../data_files/test_pkls_1_5'

for dirname, _, filenames in os.walk(parent_dir_name):
    for filename in filenames:
        
        print(dirname)
        with open(os.path.join(dirname,filename), 'rb') as fp:
            data= cPickle.load(fp)
            df=df.append(pd.DataFrame({'test': dirname.replace(parent_dir_name + '/', '')
                                , 'station': int( filename.replace('.0.pkl', '')), 
                                'acc_train': data['acc_train'], 'acc': data['acc']}, index=[0]))
        #print(dirname.replace('../data_files/test_pkls_2_5' + '/', ''),filename)
        
        
def divide(x):
    return int(x/100)


df3= pd.DataFrame(np.loadtxt('../data_files/data/SynopFrIngres'),columns=['station', 'init', 'end', 'lat', 'lon', 'height'])

df3['station']= df3['station'].apply(divide)
df3= df3.drop_duplicates(subset='station')

fig, ax = plt.subplots(nrows=1, ncols=3, sharex=True, sharey =True, figsize=(6,6))
for i, name in enumerate(df['test'].unique()):

    df2=df[df['test']==name]
    
    
    xs=[]; ys=[]; zs=[]
    for station in df['station'].unique():
        z= np.mean( df2[df2['station']==station ]['acc'].tolist())
    
        x=float(df3[df3['station']==int(station)]['lon'])
        y=float(df3[df3['station']==int(station)]['lat'])
        xs.append(x); ys.append(y); zs.append(z)
    
    
    
    import matplotlib.pyplot as plt
    import numpy as np
    import os
    import gc
    
    
    #Graph Limit
    graphlim = 41
    
    #Plot
    
    im=ax[i].scatter(xs, ys,
                edgecolors = 'none',
                c = zs,
                s = 20,
                cmap=plt.cm.get_cmap('jet'))
    ax[i].set_title(name)

fig.colorbar(im)
"""
plt.xlim(0, graphlim)
plt.ylim(0, graphlim)
plt.xticks(range(0, graphlim, int(graphlim/10)))
plt.yticks(range(0, graphlim, int(graphlim/10)))
plt.colorbar()
plt.grid(zorder = 0, alpha = 0.3)
ax.set_xlabel('p / mV')
ax.set_ylabel('p_nach / mV')
plt.show()
"""