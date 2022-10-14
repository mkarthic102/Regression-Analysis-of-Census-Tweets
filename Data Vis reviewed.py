#!/usr/bin/env python
# coding: utf-8

# In[8]:


import os
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
import matplotlib.patches as mp
get_ipython().run_line_magic('matplotlib', 'inline')

df = pd.read_csv('Construction Spending 20-22.csv')
df = df[df['Type']!='Total']
palette = sns.xkcd_palette(["turquoise", "bluey purple"])
sns.barplot(data=df, x='Date', y='Spending (Millions of Dollars)', hue='Type', palette = palette, dodge=False)
plt.xticks(rotation=90)
sns.set(rc = {"figure.figsize":(20,10)}) #setting the size of plot
plt.title("Construction Spending from June 2020 to June 2022: Seasonally Adjusted Annual Rate", fontsize = 25, pad = 20, weight = "bold")
plt.xlabel("", fontsize = 23, labelpad = 20)
plt.ylabel("Spending (Millions of Dollars)", fontsize = 23, labelpad = 20)
plt.xticks(rotation = 45, fontsize = 14)
plt.yticks(fontsize = 20)
plt.subplots_adjust(left=5, right=6)


# In[6]:


data = pd.read_csv("New Manufacturing Data.csv")
palette = sns.xkcd_palette(["turquoise", "dark lavender", "cerulean", "deep rose"])
sns.set(rc = {"figure.figsize":(20,10)}) #setting the size of plot
sns.set_style("darkgrid")
axis = sns.scatterplot(x = "Month", y = "Value", data = data, hue = "Year", palette = palette, s = 175)
axis = sns.lineplot(x = "Month", y = "Value", data = data, hue = "Year", palette = palette, sort = False, lw = 5)
plt.xticks(rotation = 90, fontsize = 18)

plt.yticks(fontsize = 20)
plt.xticks(fontsize = 20, rotation = 45)
plt.ylabel("Value of Shipments (Millions of Dollars)", fontsize = 23, labelpad = 20)
plt.xlabel("")
plt.title("Seasonally Adjusted Values of Manufacturers' Shipments from 2018 to 2021", fontsize = 25, pad = 20, weight = "bold")
plt.legend(labels=["2018","2019", "2020", "2021"], title = "Legend", fontsize = "19", title_fontsize = "21")
plt.subplots_adjust(left=5, right=6)


# In[ ]:




