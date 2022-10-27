#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 15 12:51:17 2022

@author: tobou
"""

import sys
sys.path.insert(0, '..')


from settings import variable
from preprocessing.create_sets import create_sets
import matplotlib.pyplot as plt
import pandas as pd

xs, f= create_sets(6096.0, 'train')
xs2,f2= create_sets(6142.0, 'deploy')
ys=f(xs)
ys2=f2(xs2)
#plt.plot(xs,f(xs), 'b.')

from statsmodels.tsa.stattools import acf, kpss, adfuller

def adf_test(timeseries):
    print("Results of Dickey-Fuller Test:")
    dftest = adfuller(timeseries, autolag="AIC")
    dfoutput = pd.Series(
        dftest[0:4],
        index=[
            "Test Statistic",
            "p-value",
            "Lags Used",
            "Number of Observations Used",
        ],
    )
    for key, value in dftest[4].items():
        dfoutput["Critical Value (%s)" % key] = value
    print(dfoutput)
    return 
def kpss_test(timeseries):
    print("Results of KPSS Test:")
    kpsstest = kpss(timeseries, regression="c", nlags="auto")
    kpss_output = pd.Series(
        kpsstest[0:3], index=["Test Statistic", "p-value", "Lags Used"]
    )
    for key, value in kpsstest[3].items():
        kpss_output["Critical Value (%s)" % key] = value
    print(kpss_output)
    return 
    
plt.figure(figsize=(10,5))

plt.plot(acf(f(xs)))

kpss_test(f(xs))

adf_test(f(xs))
plt.xlabel("lags")
plt.ylabel("correlation")
plt.tight_layout()

plt.savefig("../Images/acf_plot_temp")

from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.ar_model import ar_select_order
import numpy as np

mean=np.mean(ys); std=np.std(ys)


#if(variable=='t2m'):
#    ys=[ i for i in ys if (i>(mean-2*std) and i<(mean+2*std))]


mod = ar_select_order(ys, maxlag=6, glob=True, seasonal=True, period=24) 
print(mod.ar_lags)



model = ARIMA(endog=ys, order=(mod.ar_lags,0,0), seasonal_order=(1,0,0,24), missing='drop')#.fit(low_memory=True)
res=model.fit(low_memory=True)

res.plot_diagnostics(figsize=(15, 12))

plt.show()

print(res.summary())



model2=res.apply(ys)
model2.predict(start=0, end=len(ys), dynamic=False)


plt.plot(model2.predict(start=0, end=len(ys), dynamic=False)[1:],ys, 'b.')
plt.plot(np.linspace(min(ys), max(ys), 1000), np.linspace(min(ys), max(ys), 1000), 'r-' )
plt.plot(np.linspace(min(ys), max(ys), 1000), np.linspace(min(ys), max(ys), 1000)-1.5, 'r--', label='$\pm 1.5 K$')
plt.plot(np.linspace(min(ys), max(ys), 1000), np.linspace(min(ys), max(ys), 1000)+1.5, 'r--' )
plt.xlabel("Ground Truth (K)")
plt.ylabel("Prediction (K)")
plt.legend(loc='best', fontsize=12)
plt.tight_layout()
plt.savefig('../Images/yy_plot_temp')


model3= res.apply(ys2)
plt.figure()
plt.plot(xs2,ys2, 'b.' )

plt.plot(xs2,model3.predict(start=0, end=len(ys2), dynamic=False)[1:], 'r.' )
plt.figure()
plt.plot(model3.predict(start=0, end=len(ys2), dynamic=False)[1:],ys2, 'b.')
plt.plot(np.linspace(min(ys2), max(ys2), 1000), np.linspace(min(ys2), max(ys2), 1000), 'r-' )
plt.plot(np.linspace(min(ys2), max(ys2), 1000), np.linspace(min(ys2), max(ys2), 1000)-1.5, 'r--' )
plt.plot(np.linspace(min(ys2), max(ys2), 1000), np.linspace(min(ys2), max(ys2), 1000)+1.5, 'r--' )
