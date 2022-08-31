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


from settings import variable

df=pd.DataFrame(columns=['test', 'station', 'acc_train', 'acc'])

parent_dir_name_base= '../data_files/'+variable+'/test_pkls_'

parent_dir_names=['1_5', '2_5', '3_5']

fig, axs= plt.subplots(nrows=1, ncols= 3, figsize=(10,15), sharey=False)
fig.tight_layout()
plt.subplots_adjust(wspace=0.2, hspace=0)

for i, name in enumerate(parent_dir_names):
    parent_dir_name= parent_dir_name_base+ name
    for dirname, _, filenames in os.walk(parent_dir_name):
        for filename in filenames:
            
            print(dirname)
            with open(os.path.join(dirname,filename), 'rb') as fp:
                data= cPickle.load(fp)

                df=df.append(pd.DataFrame({'test': dirname.replace(parent_dir_name + '/', '')
                                    , 'station': int( filename.replace('.0.pkl', '')), 
                                    'acc_train': data['acc_train'], 'acc': data['acc']}, index=[0]))

            #print(dirname.replace('../data_files/test_pkls_2_5' + '/', ''),filename)
    l=df['station'].tolist()
    d = dict([(y,x+1) for x,y in enumerate(sorted(l))])
    
    print(df[df['station']==6096.0])#[df['test']=='STCT'])
    im=axs[i].scatter(df['test'].tolist(), [d[x] for x in l], c=df['acc'].tolist())
    axs[i].set_yticks( list(d.values()))
    axs[i].set_yticklabels([str(x) for x in list(d.keys())])
    axs[i].tick_params(direction='in')
    axs[i].text(.5,0.98,str(name).replace('_','.'), horizontalalignment='center',transform=axs[i].transAxes)
    
    del(d, l)
axs[1].set_yticklabels([]) 
#axs[2].set_yticklabels([])         
def divide(x):
    return int(x/100)





fig.colorbar(im)

plt.savefig('../Images/test_acc_vis_press.png')


df3= pd.DataFrame(np.loadtxt('../data_files/data/SynopFrIngres'),columns=['station', 'init', 'end', 'lat', 'lon', 'height'])

df3['station']= df3['station'].apply(divide)
df3.drop_duplicates(subset='station', inplace=True)
df3= df3[df3['station']<10000]
df3= df3[df3['lon']>-100]

for i in range(len(df3)):
    try:
        df3.iloc[i,1]= np.datetime64(str(int(df3.iloc[i,1]))[:4]+'-'+str(int(df3.iloc[i,1]))[4:6]+'-'+str(int(df3.iloc[i,1]))[6:], 'D')
    except:
        df3.iloc[i,1]=np.NAN
    try:
        df3.iloc[i,2]= np.datetime64(str(int(df3.iloc[i,2]))[:4]+'-'+str(int(df3.iloc[i,2]))[4:6]+'-'+str(int(df3.iloc[i,2]))[6:], 'D')
    except:
        df3.iloc[i,2]=np.NAN
        
"""

fig, ax = plt.subplots(nrows=1, ncols=4, sharex=True, sharey =True, figsize=(10,4))
for i, name in enumerate(df['test'].unique()):

    df2=df[df['test']==name]
    
    
    xs=[]; ys=[]; zs=[]
    for station in df['station'].unique():
        z= np.mean( df2[df2['station']==station ]['acc'].tolist())
    
        x=float(df3[df3['station']==int(station)]['lon'])
        y=float(df3[df3['station']==int(station)]['lat'])
        xs.append(x); ys.append(y); zs.append(z)
    
    
    #Graph Limit
    graphlim = 41
    
    #Plot
    
    im=ax[i].scatter(xs, ys,
                edgecolors = 'none',
                c = zs,
                s = 20,
                cmap=plt.cm.get_cmap('jet'))
    ax[i].set_title(name)
    ax[i].set_xlabel('lon (¤)')
    ax[i].tick_params(axis="x",direction="in")
    ax[i].tick_params(axis="y",direction="in")
ax[0].set_ylabel('lat (¤)')
fig.colorbar(im)
fig.tight_layout()
"""
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