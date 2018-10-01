
# coding: utf-8

# In[89]:


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
import openpyxl


# In[2]:


SingleData=xlrd.open_workbook('D:/Data/2409DM.xlsx')
stable=SingleData.sheet_by_name(u'Data')
srows=stable.nrows
sdata=[]
for i in range(srows-1):
    t=stable.row_values(i+1)
    sdata.append(t)


# In[3]:


headname=stable.row_values(0)
sdata=DataFrame(sdata)
sdata.columns=headname


# In[4]:


sdata2=sdata.groupby("System").max()


# In[5]:


sm=sdata2["Used Memory (% max)"]
sm=[i*100 for i in sm]


# In[6]:


sname=sdata2.index


# In[7]:


sname=sname.tolist()


# In[8]:


cData=xlrd.open_workbook('D:/Data/2409cpu.xlsx')
ctable=cData.sheet_by_name(u'Data')
crows=ctable.nrows
cdata=[]
for i in range(crows-1):
    t=ctable.row_values(i+1)
    cdata.append(t)


# In[9]:


cname=ctable.row_values(0)


# In[10]:


cdata2=DataFrame(cdata)
cdata2.columns=cname
cdata2=cdata2.groupby("System").max()
cn=cdata2.index.tolist()
cc=cdata2["CPU Busy (% max)"].values.tolist()


# In[11]:


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


# In[12]:


elements = periodic_table.elements
elements = elements[elements["atomic number"] <= 82]
elements = elements[~pd.isnull(elements["melting point"])]


# In[13]:


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


# In[14]:


Size=Size.drop_duplicates("System")
SizeName=Size["System"].values.tolist()
SV=Size["Host DB Size (GiB)"].values.tolist()


# In[15]:


SPV=[]
for i in range(len(sname)):
    a=0
    for j in range(len(SizeName)):
        if(sname[i]==SizeName[j]):
            SPV.append(SV[j])
            a=1
    if a==0:
        SPV.append(0)
   
        


# In[16]:


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


# In[17]:


html=[]
for i in range(len(sname)):
    t=[]
    t.append(sname[i])
    t.append(sm[i])
    t.append(ct[i])
    t.append(SPV[i])
    html.append(t)
        


# In[18]:


html=DataFrame(html)


# In[19]:


headerName=["SID","Memory Max%","CPU Max%","Size"]


# In[20]:


html.columns=headerName


# In[106]:


html=html.sort_values(by=["Memory Max%"],ascending=False)
pd.set_option("display.width",-1)
html.to_html("list.html")


# In[21]:


html=html.sort_values(by=["Memory Max%"],ascending=False)
pd.set_option("display.width",-1)
html.to_csv("list.csv")


# In[24]:


PreSize=[0.5,1.5,3,4,6]


# In[25]:


PreSize


# In[27]:


Memory=html["Memory Max%"].values.tolist()
SizeH=html["Size"].values.tolist()


# In[51]:


relabel1=[]
relabel2=[]


# In[52]:


for i in range(len(Memory)):
    a=0
    if(Memory[i]>75 and SizeH[i]<6):
        t=Memory[i]
        SizeIndex=PreSize.index(SizeH[i])
        base=t/100*SizeH[i]/PreSize[SizeIndex+1]
        if(base>0.30):
            relabel1.append(SizeH[i])
            relabel2.append(PreSize[SizeIndex+1])
        else:
            relabel1.append(SizeH[i])
            relabel2.append(SizeH[i])
                
        a=1
    if(Memory[i]<30 and SizeH[i]>0.5):
        t=Memory[i]
        SizeIndex=PreSize.index(SizeH[i])
        base=t/100*SizeH[i]/PreSize[SizeIndex-1]
        if(base<0.75):
            relabel1.append(PreSize[SizeIndex-1])
            relabel2.append(PreSize[SizeIndex-1])
        else:
            relabel1.append(SizeH[i])
            relabel2.append(SizeH[i])
        a=1
    if(a==0):
        relabel1.append(SizeH[i])
        relabel2.append(SizeH[i])
        
        
        


# In[53]:


html["relabel1"]=relabel1


# In[54]:


html["relabel2"]=relabel2


# In[58]:


html=html[html["Memory Max%"]>=20]


# In[61]:


html2=html.drop(["relabel1"],axis=1)


# In[68]:


sizet=html2["Size"].values.tolist()
rl2=html2["relabel2"].values.tolist()


# In[69]:


for i in range(len(sizet)):
    if(sizet[i]!=rl2[i]):
        rl2[i]=str(rl2[i])


# In[73]:


html2["relabel2"]=rl2


# In[84]:


def color_negative_red(val):
    """
    Takes a scalar and returns a string with
    the css property `'color: red'` for negative
    strings, black otherwise.
    """
    color = 'red' if type(val)==str  else 'black'
    return 'color: %s' % color


# In[85]:


s = html2.style.applymap(color_negative_red)


# In[90]:


writer=pd.ExcelWriter("output.xlsx")
html2.to_excel(writer,"sheet1")
writer.save()


# In[91]:


s

