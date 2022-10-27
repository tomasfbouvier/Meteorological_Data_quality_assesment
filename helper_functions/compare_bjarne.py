#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 14 13:49:36 2022

@author: tobou
"""
import sys

sys.path.insert(0, "..")


import os
import numpy as np
import pandas as pd


from df_gen.df import Create_df
import matplotlib.pyplot as plt

pd.options.mode.chained_assignment = None  # default='warn'



from settings import (
    variable,
    train_start_date,
    train_end_date,
    test_start_date,
    test_end_date,
    output_start_date,
    output_end_date,
)


df_deploy = Create_df(
    start=np.datetime64(output_start_date), end=np.datetime64(output_end_date)
)

df_bjarne = Create_df(
    start=np.datetime64(output_start_date),
    end=np.datetime64(output_end_date),
    data_source="Carra",
)  # .to_pickle('/home/tobou/Desktop/Meteorological_Data_quality_assesment/df_gen/df_corrected.pkl')

df_corrected = Create_df(
    start=np.datetime64(output_start_date),
    end=np.datetime64(output_end_date),
    data_source="corrected",
)

station = 4207.0

fig, axs = plt.subplots(nrows=2, sharex=True, sharey=True, figsize=(10, 4))
plt.tight_layout()

#df_deploy = df_deploy[df_deploy["timestamp"] > np.datetime64("1997-05-22")][
#    df_deploy["timestamp"] < np.datetime64("1997-05-30")
#]

axs[0].plot(
    df_deploy[df_deploy["station"] == station]["timestamp"],
    df_deploy[df_deploy["station"] == station]["max"],
    "b.",The reason why no observation is flagged is because being in Greenland, there is a big chance that only the TCT was performing well. However the accuracy is still not 100%. Therefore, even if the output of the test is correct, the information contribution is not enough to raise the prior probability (15%) to the posterior over which I determine that the observation is an outlier (90%). In other words, what Bayes says is that the TCT by itself is not enough to trigger the alarm. The test should be supplied with other independent pieces of evidence such as SCT, but unfortunately in Greenland it is rather hard to obtain good results for it.
)
axs[1].plot(
    df_deploy[df_deploy["station"] == station]["timestamp"],
    df_deploy[df_deploy["station"] == station]["max"],
    "b.",
)

axs[0].plot(
    df_deploy[df_deploy["station"] == station][df_bjarne["max"] < 0.0]["timestamp"],
    df_deploy[df_deploy["station"] == station][df_bjarne["max"] < 0.0]["max"],
    "r.",
)
axs[1].plot(
    df_deploy[df_deploy["station"] == station][df_corrected["max"] < 0.0]["timestamp"],
    df_deploy[df_deploy["station"] == station][df_corrected["max"] < 0.0]["max"],
    "r.",
)

# axs[0].set_title('Bjarne\'s detection', pad=-14, loc=None)
# axs[1].set_title('Algorithm detection', pad= -50)
axs[0].text(
    0.15,
    0.85,
    "Expert hand-work",
    horizontalalignment="center",
    transform=axs[0].transAxes,
    fontsize="x-large",
)
axs[1].text(
    0.15,
    0.85,
    "Automatic detection",
    horizontalalignment="center",
    transform=axs[1].transAxes,
    fontsize="x-large",
)


# for i in range(2):
#    axs[i].set_ylim(270.0,295.0)
# plt.suptitle(s='station: '+ str(station), y=1.1)
plt.savefig("../Images/" + str(station) + "_" + variable + ".png")

"""
for station in df_bjarne[df_bjarne['max']<0.][df_bjarne['station']>6000]['station'].unique():
    plt.figure()
    plt.title(str(station))
    plt.plot(df_deploy[df_deploy['station']==station]['timestamp'], df_deploy[df_deploy['station']==station]['max'], 'b.')
    plt.plot(df_deploy[df_deploy['station']==station][df_bjarne['max']<0.]['timestamp'], df_deploy[df_deploy['station']==station][df_bjarne['max']<0.]['max'], 'r.')
    

"""