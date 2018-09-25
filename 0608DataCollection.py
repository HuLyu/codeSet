
# coding: utf-8

# In[1]:


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


# In[8]:


SizeData=xlrd.open_workbook('D:/data/DBM.xlsx')
SizeTable=SizeData.sheet_by_name(u'Data')
SizeRows=SizeTable.nrows
usedSize=[] 
for i in range(SizeRows-1):                     
    t=[]
    td=SizeTable.row_values(i+1)
    if(len(td[0])!=0 and td[0][0]=="Z"):
        t.append(td[0])
        t.append(td[4])
        t.append(td[3])
        t.append(td[6])
        t.append(td[7])
        #t.append(xlrd.xldate_as_tuple(td[2],0))
        t.append(td[2])
        usedSize.append(t)
#'System',
 #'System Number',
 #'Date',
 #'#OOM Events',
 #'Used Memory (MiB max)',
 #'Used Memory (% max)',
 #'Not yet allocated Memory (MiB max)',
 #'Free Memory Pool (MiB max)',
 #'Memory reserved by OS (MiB max)',
 #'Resident Memory (MiB max)']
 #sid,usedsize,oom,not allocated,free memeory,date  
 #(new column)
SizeTableHeader=SizeTable.row_values(0)
#SizeTableHeader=[i.encode("utf-8") for i in SizeTableHeader]
SizeTableHeader=[SizeTableHeader[0],SizeTableHeader[4],SizeTableHeader[3],SizeTableHeader[6],SizeTableHeader[7],SizeTableHeader[2]]


# In[9]:


#####store cpu data###################
CpuData=xlrd.open_workbook('D:/data/CPU.xlsx')
CpuTable=CpuData.sheet_by_name(u'Data')
Cpu=[]
CpuRows=CpuTable.nrows

for i in range(CpuRows-1):
    t=CpuTable.row_values(i+1)
    if(t[0][0]=="Z"):
        Cpu.append([t[0],t[1],t[5]])
        
Memory=DataFrame(usedSize)
Memory.columns=SizeTableHeader
CpuName=CpuTable.row_values(0)
CpuName=[CpuName[0],CpuName[1],CpuName[5]]
#CpuName=[i.encode("utf-8") for i in CpuName]
Cpu=DataFrame(Cpu)
Cpu.columns=CpuName
Report=pd.merge(Memory,Cpu) 
####merge memory and cpu##########


# In[14]:


###store customer name and merge to "Report"#####
SetSizeData=xlrd.open_workbook('D:/data/T.xlsx')
SetSizeTable=SetSizeData.sheet_by_name(u'Data')
SSRows=SetSizeTable.nrows
SetSize=[]

for i in range(SSRows-1):
    t=SetSizeTable.row_values(i+1)
    if(t[3]=='100'):
        SetSize.append([t[2],t[-1],t[9],t[10],t[5]])
t=SetSizeTable.row_values(0)
t=[t[2],t[-1],t[9],t[10],t[5]]
#t=[i.encode("utf-8") for i in t]
t[0]="System"
SS=DataFrame(SetSize)
SS.columns=t
Report=pd.merge(Report,SS)
ReportSelected=Report.drop(["Not yet allocated Memory (MiB max)","Free Memory Pool (MiB max)","System Business Type","Tenant Role"],axis=1)


# In[15]:


pickle.dump(SS,open("SystemSize.txt","wb"))


# In[16]:


###STORE planningPoints#####
PPData=xlrd.open_workbook('D:/data/ppl.xlsx')
PPTable=PPData.sheet_by_name(u'Data')
PlanningPoints=[]
PlanningPointsRows=PPTable.nrows
for i in range(PlanningPointsRows-1):
    PlanningPoints.append(PPTable.row_values(i+1))
PlanningPoints=DataFrame(PlanningPoints)
t=PPTable.row_values(0)
t[1]="System"
PlanningPoints.columns=t
ReportSelected2=pd.merge(ReportSelected,PlanningPoints,on=['System','Date'])
#######store planningpoint in “ReportSelected2”################################


# In[38]:


rs=ReportSelected2[ReportSelected2["Host DB Size (GiB)"]>500]
rs=rs[rs["Host DB Size (GiB)"]<600]


# In[39]:


rt=rs.groupby("System").max()


# In[42]:


len(rt)


# In[43]:


rt=rt[rt["Planning Points"]>250000000]


# In[59]:


rdd=rdd.drop(["Date"],axis=1)


# In[60]:


rdd=rdd.drop(["Customer Name_x"],axis=1)


# In[54]:


rd=ReportSelected2[ReportSelected2["Planning Points"]>250000000]


# In[55]:


rd=rd[rd["Planning Points"]<300000000]


# In[56]:


rdd=rd.groupby("System").max()


# In[61]:


rdd


# In[58]:


len(rdd)


# In[18]:


ReportSelected2.to_csv("2009.csv")


# In[7]:


####store active user#########################
UserData=xlrd.open_workbook('D:/data/AU1109.xlsx')
UserTable=UserData.sheet_by_name(u'Data')
User=[]
UserRows=UserTable.nrows
for i in range(UserRows-1):
    t=UserTable.row_values(i+1)
    User.append([t[1],t[0],t[-1]])
UN=UserTable.row_values(0)
UN=[UN[1],UN[0],UN[-1]]
UN[0]="System"
User=DataFrame(User)
User.columns=UN
ReportSelected3=pd.merge(ReportSelected,User)
####store all data in ReportSelected3#########


# In[8]:


############store average used memory#######
AM=[]
Audata=xlrd.open_workbook("D:/data/DBA1109.xlsx")
ATable=Audata.sheet_by_name(u"Data")
Arows=ATable.nrows
for i in range(Arows-1):
    t=ATable.row_values(i+1)
    AM.append([t[0],t[2],t[5]])
AN=ATable.row_values(0)
AN=[AN[0],AN[2],AN[5]]
AM=DataFrame(AM)
AM.columns=AN
ReportSelected4=pd.merge(ReportSelected3,AM)


# In[9]:


path="D:/data/"


# In[10]:


Date=ReportSelected4["Date"].values.tolist()
Date=list(set(Date))


# In[11]:


Date2=[xlrd.xldate_as_tuple(i,0) for i in Date]


# In[12]:


Date3=[]
for i in range(len(Date2)):
    if(Date2[i][1]<10):
        t1="0"+str(Date2[i][1])
    else:
        t1=str(Date2[i][1])
    if(Date2[i][2]<10):
        t2="0"+str(Date2[i][2])
    else:
        t2=str(Date2[i][2])
    t3=path+t2+t1+".xlsx"
    Date3.append(t3)


# In[13]:


tread=xlrd.open_workbook("header.xlsx")
treadTable=tread.sheet_by_name(u'fd')
header=treadTable.row_values(0)
header=[i[:-3] for i in header]
header.append(u"Customer Name")


# In[14]:


AData=[]
for i in range(len(Date3)):
    tread=xlrd.open_workbook(Date3[i])
    treadTable=tread.sheet_by_name(u'Data')
    TRows=treadTable.nrows
    th=treadTable.row_values(0)
    for j in range(TRows-1):
        t=treadTable.row_values(j+1)
        tv=[]
        for n in range(len(header)):
            tv.append(t[th.index(header[n])])
        tv.append(Date[i])
            
        AData.append(tv)
    
    
        


# In[15]:


headernew=header
headernew.append(u"Date")
ADF=DataFrame(AData)
ADF.columns=headernew


# In[16]:


FinalReport=pd.merge(ReportSelected4,ADF)
#pickle.dump(FinalReport, open("finalData.txt","wb"))
#getback=pickle.load(open("finalData.txt","rb"))
SID=FinalReport["System"]


# In[17]:


value=FinalReport["Used Memory (MiB max)"].values.tolist()


# In[18]:


max(value)-min(value)


# In[19]:


min(value)


# In[42]:


NormalizedReport=FinalReport.drop(["System","Customer Name","Date"],axis=1)
for i in NormalizedReport.columns.tolist():
    t=NormalizedReport[i]
    t=(t-min(t))/(max(t)-min(t))
    NormalizedReport[i]=t


# In[43]:


NormalizedReport["SID"]=SID


# In[44]:


pickle.dump(NormalizedReport,open("NormalizedData1109.txt","wb"))
    

