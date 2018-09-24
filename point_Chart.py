
# coding: utf-8

# In[46]:


import pandas as pd
import numpy as np
from pandas import DataFrame
from operator import itemgetter
import sys 
import xlrd
from bokeh.plotting import figure, show, output_file
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, Range1d, LabelSet, Label
import copy
import urllib
import os
import csv
from bokeh.io import save
import pickle
from bokeh.plotting import figure, show, output_file
from bokeh.sampledata import periodic_table


# In[3]:


SingleData=xlrd.open_workbook('D:/Data/2409DM.xlsx')
stable=SingleData.sheet_by_name(u'Data')
srows=stable.nrows
sdata=[]
for i in range(srows-1):
    t=stable.row_values(i+1)
    sdata.append(t)


# In[4]:


headname=stable.row_values(0)
sdata=DataFrame(sdata)
sdata.columns=headname


# In[8]:


sdata2=sdata.groupby("System").max()


# In[16]:


sm=sdata2["Used Memory (% max)"]
sm=[i*100 for i in sm]


# In[17]:


sname=sdata2.index


# In[19]:


sname=sname.tolist()


# In[33]:


cData=xlrd.open_workbook('D:/Data/2409cpu.xlsx')
ctable=cData.sheet_by_name(u'Data')
crows=ctable.nrows
cdata=[]
for i in range(crows-1):
    t=ctable.row_values(i+1)
    cdata.append(t)


# In[34]:


cname=ctable.row_values(0)


# In[38]:


cdata2=DataFrame(cdata)
cdata2.columns=cname
cdata2=cdata2.groupby("System").max()
cn=cdata2.index.tolist()
cc=cdata2["CPU Busy (% max)"].values.tolist()


# In[95]:


ct=[]
for i in range(len(sname)):
    a=0
    for j in range(len(cn)):
        if(sname[i]==cn[j]):
            ct.append(cc[j])
            a=1
    if a==0:
        ct.append(0)
ctt=[i+0.3 for i in ct]


# In[48]:


elements = periodic_table.elements
elements = elements[elements["atomic number"] <= 82]
elements = elements[~pd.isnull(elements["melting point"])]


# In[53]:


Size=pickle.load(open("SystemSize.txt","rb"))
t=Size["Host DB Size (GiB)"].values.tolist()
t=[i/1000 for i in t]
for i in range(len(t)):
    if(t[i]<0.3):
        t[i]=0.5
    elif(t[i]<0.6):
        t[i]=0.5
    elif(t[i]<1.7):
        t[i]=1.5
    elif(t[i]<3.2):
        t[i]=3
    elif(t[i]<4.5):
        t[i]=4
    else:
        t[i]=6
Size["Host DB Size (GiB)"]=t


# In[80]:


Size=Size.drop_duplicates("System")
SizeName=Size["System"].values.tolist()
SV=Size["Host DB Size (GiB)"].values.tolist()


# In[81]:


SPV=[]
for i in range(len(sname)):
    a=0
    for j in range(len(SizeName)):
        if(sname[i]==SizeName[j]):
            SPV.append(SV[j])
            a=1
    if a==0:
        SPV.append(0)
   
        


# In[96]:


output_file("scatter.html", title="point chart")

p = figure(logo="grey", plot_height=1200,plot_width=1200)

p.circle(sm, ct, size=12,
        line_color="black", fill_alpha=0.8)
p.text(sm, ctt,
    text=sname,text_color="#333333",
    text_align="center", text_font_size="10pt")
p.xaxis.axis_label="memory max %"
p.yaxis.axis_label="CPU max %"
p.grid.grid_line_color="white"
save(p)


# In[97]:


html=[]
for i in range(len(sname)):
    t=[]
    t.append(sname[i])
    t.append(sm[i])
    t.append(ct[i])
    t.append(SPV[i])
    html.append(t)
        


# In[98]:


html=DataFrame(html)


# In[100]:


headerName=["SID","Memory Max%","CPU Max%","Size"]


# In[101]:


html.columns=headerName


# In[106]:


html=html.sort_values(by=["Memory Max%"],ascending=False)
pd.set_option("display.width",-1)
html.to_html("list.html")

