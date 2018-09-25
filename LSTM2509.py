
# coding: utf-8

# In[68]:


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
import tensorflow as tf
from sklearn.metrics import mean_absolute_error,mean_squared_error
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import warnings 
warnings.filterwarnings('ignore')
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
import math

import matplotlib.pyplot as plt
import pandas as pd
import datetime as dt
import urllib.request, json
import os
import numpy as np
import tensorflow as tf # This code has been tested with TensorFlow 1.6
from sklearn.preprocessing import MinMaxScaler
from matplotlib import pyplot
from matplotlib.pyplot import figure
from keras.models import load_model
from keras.layers import Dropout
from keras.layers.core import Dense, Activation, Dropout
from keras.layers.recurrent import LSTM
from keras import optimizers

from keras.callbacks import ModelCheckpoint
###add checkpoint and tensorboard version


# In[3]:


###load normalized data and store data for every system in "Systems"############
Data=pickle.load(open("NormalizedData.txt","rb"))
SID=Data["SID"].values.tolist()
SID2=list(set(SID))
Systems=[Data[Data["SID"]==SID2[i]] for i in range(len(SID2)) ]


# In[4]:


###load normalized data and store data for every system in "Systems"############
Data2=pickle.load(open("NormalizedData1109.txt","rb"))
SID3=Data2["SID"].values.tolist()
SID4=list(set(SID3))
Systems2=[Data2[Data2["SID"]==SID2[i]] for i in range(len(SID4)) ]


# In[5]:


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


# In[6]:


SizeT={SID2[i]:Size[Size["System"]==SID2[i]]["Host DB Size (GiB)"].values[0] for i in range(len(SID2))}


# In[7]:


l=[len(i) for i in Systems]


# In[8]:


datanew=[Systems[i].drop(["SID"],axis=1) for i in range(len(Systems))]


# In[9]:


datanew2=[Systems2[i].drop(["SID"],axis=1) for i in range(len(Systems2))]


# In[71]:


dl=[i.values.tolist() for i in datanew]
dataall=[]
label=[]
dt=[]
lt=[]
for i in range(len(dl)):
    t2=[]
    l2=[]
    step=7
    t=[dl[i][j:j+step] for j in range(0,len(dl[i])) if len(dl[i][j:j+step])==step]
    l=[list(map(itemgetter(0),i)) for i in t]
    for h in range(len(t)-step):
        dataall.append([m for m in t[h]])
        label.append(max(l[h+step]))
        t2.append([m for m in t[h]])
        l2.append(max(l[h+step]))
    dt.append(t2)
    lt.append(l2)
        
    
    


# In[72]:


dl2=[i.values.tolist() for i in datanew2]
dataall2=[]
label2=[]
dt2=[]
lt2=[]
for i in range(len(dl2)):
    t2=[]
    l2=[]
    step=7
    t=[dl2[i][j:j+step] for j in range(0,len(dl2[i])) if len(dl2[i][j:j+step])==step]
    l=[list(map(itemgetter(0),i)) for i in t]
    for h in range(len(t)-step):
        dataall2.append([m for m in t[h]])
        label2.append(max(l[h+step]))
        t2.append([m for m in t[h]])
        l2.append(max(l[h+step]))
    dt2.append(t2)
    lt2.append(l2)
        
    
    


# In[44]:


for i in range(len(dataall)):
    dataall[i].append(label[i])
np.random.shuffle(dataall)


# In[48]:


label=[]
for i in range(len(dataall)):
    label.append(dataall[i].pop())


# In[51]:


train_X=dataall
train_Y=label
test_X=dataall2
test_Y=label2


# In[52]:


train_X=np.array(train_X)
train_Y=np.array(train_Y)
test_X=np.array(test_X)
test_Y=np.array(test_Y)


# In[53]:


from keras.datasets import mnist
from keras.layers import Dense, LSTM
from keras.utils import to_categorical
from keras.models import Sequential


# In[69]:


model = Sequential()
model.add(LSTM(
            200,
            input_shape=(train_X.shape[1], train_X.shape[2]),return_sequences=True
            ))
model.add(Dropout(0.2))
model.add(LSTM(
            300,
            return_sequences=False))
model.add(Dropout(0.2))
model.add(Dense(1))
model.add(Activation("sigmoid"))
sgd = optimizers.SGD(lr=0.001, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss="mse", optimizer=sgd)
model.fit(train_X, train_Y, epochs=150, batch_size=30, validation_data=(test_X, test_Y), verbose=2, shuffle=True)


# In[28]:


model = Sequential()
model.add(LSTM(300, activation='relu',input_shape=(train_X.shape[1], train_X.shape[2])))
model.add(Dropout(0.2, name='dropout_1'))
model.add(Dense(8, activation='relu', name='second_hidden'))
model.add(Dense(1, activation='sigmoid', name='output_layer'))
model.compile(loss='mean_squared_error', optimizer='adam')
# fit network
model.fit(train_X, train_Y, epochs=100, batch_size=30, validation_data=(test_X, test_Y), verbose=2, shuffle=True)


# In[46]:


model.save("model1909allfinal.ht")


# In[16]:


model=load_model("model1209allfinal.ht")


# In[65]:


for i in range(len(dt2)):
    x=dt2[i]
    y=lt2[i]
    if(SID4[i] in SizeT):
        s=str(SizeT[SID4[i]])+" "+"TB"
        sname=SID4[i]
        x=np.array(x)
        if(x.shape!=(0,)):
            yhat = model.predict(x)
            ty=[(i*4150764+33708)/1000 for i in np.array(y)]
            y=[(i[0]*4150764+33708)/1000 for i in yhat]
            
           
            pyplot.yscale("linear")
            pyplot.title(sname+s)
            pyplot.plot(y, label='prediction')
            pyplot.plot(ty, label='true')
            pyplot.legend()
#pyplot.savefig("14days.pdf")
            pyplot.show()

