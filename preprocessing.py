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


# Load map of australia using postcode data

# In[2]:


aus_map = gpd.read_file('/Users/lindenmp/Dropbox/PersonalProjects/NASA_aus_firedata/aus_map/aus_poas.shp')


# In[3]:


aus_map.head()


# Pull out VIC/NSW

# In[4]:


aus_map['state'].unique()


# The 'state' column only has 'VIC'... that's weird. Let's use the postcodes to stitch together state maps
# 
# Wikipedia to the rescue! https://en.wikipedia.org/wiki/Postcodes_in_Australia
# 
# Victoria spans postcodes 3000 to 3999 inclusive

# In[5]:


vic_map = aus_map.loc[np.logical_and(aus_map['code'] >= 3000, aus_map['code'] <= 3999),:]
ax = vic_map.plot()


# NSW spans postcodes 2000 to 2999, if you include the ACT

# In[6]:


nsw_map = aus_map.loc[np.logical_and(aus_map['code'] >= 2000, aus_map['code'] <= 2999),:]
ax = nsw_map.plot()


# There is some weird spot way out east that shouldn't be there - around 160 longitude

# In[7]:


xmin, ymin, xmax, ymax = nsw_map.total_bounds
print(xmin, ymin, xmax, ymax)


# Cut at 155 longitude

# In[8]:


nsw_map = nsw_map.cx[xmin:155, ymin:ymax]


# In[9]:


ax = nsw_map.plot()


# Better!
# 
# Merge

# In[10]:


my_map = pd.concat((nsw_map, vic_map))
ax = my_map.plot()


# In[11]:


my_map.reset_index(drop = True, inplace = True)
my_map['state'] = 'None'
my_map.head()


# Load in fire data

# In[12]:


# df = gpd.read_file('/Users/lindenmp/Dropbox/PersonalProjects/NASA_aus_firedata/data/DL_FIRE_V1_101558/fire_nrt_V1_101558.shp')
# df = gpd.read_file('/Users/lindenmp/Dropbox/PersonalProjects/NASA_aus_firedata/data/DL_FIRE_M6_101557/fire_nrt_M6_101557.shp')
df = gpd.read_file('/Users/lindenmp/Dropbox/PersonalProjects/NASA_aus_firedata/data/DL_FIRE_M6_101557/fire_archive_M6_101557.shp')
df.shape


# In[13]:


df.head()


# ## Retain only fire data that intersects with my map
# 
# Scrub out postcode boundaries and store in separate variable. We'll use this below to retain fire data inside our map.

# In[14]:


my_map_nopost = my_map.dissolve(by='state')
my_map_nopost.reset_index(drop = True, inplace = True)
my_map_nopost.drop(['POA_NAME','code'], axis = 1, inplace = True)


# In[15]:


ax = my_map_nopost.plot()


# Drop rows outside the general bounds of my map (long,lat)

# In[16]:


xmin, ymin, xmax, ymax = my_map_nopost.total_bounds
print(xmin, ymin, xmax, ymax)


# In[17]:


df = df.cx[xmin:xmax, ymin:ymax]
df.reset_index(drop = True, inplace = True)
df.shape


# In[18]:


df.head()


# In[19]:


fig, ax = plt.subplots(figsize = (5,5))
my_map.plot(ax = ax)
df.plot(ax = ax, color = 'r')


# In[20]:


from IPython.display import clear_output


# In[21]:


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


# In[22]:


mask = my_map_nopost.geometry.unary_union


# In[23]:


my_bool = np.zeros((df.shape[0],), dtype=bool)


# In[24]:


for data in df.iterrows():
    update_progress(data[0]/df.shape[0])
    my_bool[data[0]] = data[1].geometry.within(mask)
update_progress(1)


# In[25]:


fig, ax = plt.subplots(figsize = (5,5))
my_map.plot(ax = ax)
df.loc[my_bool,:].plot(ax = ax, color = 'r')


# In[26]:


df.loc[my_bool,:].shape


# ## Save out

# In[27]:


my_map.to_file('/Users/lindenmp/Dropbox/PersonalProjects/NASA_aus_firedata/data/my_map.shp')
df.loc[my_bool,:].to_file('/Users/lindenmp/Dropbox/PersonalProjects/NASA_aus_firedata/data/df.shp')

