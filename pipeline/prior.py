#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 29 15:23:09 2022

@author: tobou
"""

import numpy as np

y0s=[]

iterations=10000000
for i in range(iterations):
    if np.random.rand()<0.1:
        y0= 9*np.random.rand()-4.5
        if(y0<0.):
            y0-=0.5
        else:
            y0+=0.5
    else:
        y0=0.5*np.random.randn()

    y0s.append(y0)

import matplotlib.pyplot as plt

plt.hist(y0s, bins=1000, density=True)
plt.xlabel('x - x*')
plt.ylabel('P(x - x*)')
plt.tight_layout()
plt.savefig('../Images/prior.png')