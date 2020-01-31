#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os, sys
import pandas as pd
import numpy as np
import numpy.matlib
import scipy as sp

import geopandas as gpd

# Plotting
import matplotlib.pyplot as plt
import seaborn as sns


# In[2]:


shape_file = gpd.read_file('/Users/lindenmp/Dropbox/PersonalProjects/NASA_aus_firedata/data/DL_FIRE_V1_101558/fire_nrt_V1_101558.shp')
# shape_file = gpd.read_file('/Users/lindenmp/Dropbox/PersonalProjects/NASA_aus_firedata/data/DL_FIRE_V1_101558/fire_archive_V1_101558.shp')


# In[3]:


shape_file.set_index('ACQ_DATE', inplace = True)


# In[4]:


shape_file.tail()


# Plot a couple of dates

# In[5]:


fig, ax = plt.subplots(figsize = (15,15))
shape_file.loc['2019-10-01'].plot(ax = ax)
shape_file.loc['2020-01-29'].plot(ax = ax)


# Plot same date, but color day/night differently

# In[6]:


fig, ax = plt.subplots(figsize = (15,15))
shape_file[shape_file['DAYNIGHT'] == 'D'].loc['2020-01-29'].plot(ax = ax, color = 'blue')
shape_file[shape_file['DAYNIGHT'] == 'N'].loc['2020-01-29'].plot(ax = ax, color = 'red')

