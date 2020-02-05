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


from IPython.display import clear_output


# In[3]:


def update_progress(progress, my_str = ''):
    bar_length = 20
    if isinstance(progress, int):
        progress = float(progress)
    if not isinstance(progress, float):
        progress = 0
    if progress < 0:
        progress = 0
    if progress >= 1:
        progress = 1

    block = int(round(bar_length * progress))

    clear_output(wait = True)
    text = my_str + " Progress: [{0}] {1:.1f}%".format( "#" * block + "-" * (bar_length - block), progress * 100)
    print(text)


# In[4]:


my_map = gpd.read_file('/Users/lindenmp/Dropbox/PersonalProjects/NASA_aus_firedata/data/my_map.shp')


# In[5]:


df = gpd.read_file('/Users/lindenmp/Dropbox/PersonalProjects/NASA_aus_firedata/data/df.shp')
df.shape


# In[6]:


df.head()


# In[7]:


fig, ax = plt.subplots(figsize = (5,5))
my_map.plot(ax = ax)
df.plot(ax = ax, color = 'r')


# In[8]:


my_map


# In[9]:


df['postcode'] = np.zeros(df.shape[0],).astype(int)


# In[10]:


df.head()


# In[11]:


postcodes = my_map['code'].unique()

for i, postcode in enumerate(postcodes):
    update_progress(i/len(postcodes))
    mask = my_map.loc[my_map['code'] == postcode,'geometry'].unary_union
    my_bool = df.geometry.within(mask)
    df.loc[my_bool,'postcode'] = postcode
update_progress(1)


# ## Save out

# In[12]:


df.to_file('/Users/lindenmp/Dropbox/PersonalProjects/NASA_aus_firedata/data/df_postcode.shp')

