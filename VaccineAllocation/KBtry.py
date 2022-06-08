# -*- coding: utf-8 -*-
"""
Created on Fri Apr 29 12:07:31 2022

@author: kb44774
"""


import numpy as np
import pandas as pd
import datetime as dt
from datetime import timedelta, date
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import random

from SEIYAHRD import discrete_approx 

df_delta = pd.read_csv (r'C:\Users\kb44774\Desktop\python codes\COVID19-vaccine-main\VaccineAllocation\instances\austin\delta_prevelance.csv')
#print (df_delta)
predelta_start= date(2020, 3, 1)
delta_start = date(2021, 4, 20)
#print (delta_start)
df_omicron=pd.read_csv (r'C:\Users\kb44774\Desktop\python codes\COVID19-vaccine-main\VaccineAllocation\instances\austin\omicron_prevelance.csv')
omicron_start = date(2021, 12, 13)
potentialnew_start = date(2023, 1, 1)



Simulation_start=date(2021, 3, 1)
Simulation_end=date(2022, 9, 30)
count_day=(Simulation_end-Simulation_start).days
#print (count_day)

number_variants=np.zeros(count_day)
predelta_prev=np.zeros(count_day)
delta_prev=np.zeros(count_day)
omicron_prev=np.zeros(count_day)
potentialnew_prev=np.zeros(count_day)
beta=np.zeros(count_day)
YHRr=np.zeros(count_day)

beta0=0.06901061034207119
predelta_beta=beta0
delta_beta=predelta_beta*1.65
omicron_beta=delta_beta*1.55
potentialnew_beta=omicron_beta*random.uniform(1.2, 1.8)

potentialnew_YHR=random.uniform(0.5,2)
omicron_YHR=0.9
delta_YHR=1.8
predelta_YHR=1

for t in range(count_day):
    current_date=Simulation_start+timedelta(t)
    #print(current_date)
    
    if number_variants[t-1]==3:
        if random.uniform(0,1)>0.995:
            potentialnew_start =current_date
    
    if current_date>potentialnew_start:
        number_variants[t]=4
        t1=(current_date-potentialnew_start).days
        potentialnew_prev[t]=max(random.uniform(df_delta['delta_prev'][t1], df_omicron['prev'][t1]),potentialnew_prev[t-1])
        omicron_prev[t]=1-potentialnew_prev[t]
        beta[t]=potentialnew_prev[t]*potentialnew_beta+omicron_prev[t]*omicron_beta
        YHRr[t]=potentialnew_prev[t]*potentialnew_YHR+omicron_prev[t]*omicron_YHR
    elif current_date>omicron_start:
        number_variants[t]=3
        t1=(current_date-omicron_start).days
        omicron_prev[t]=df_omicron['prev'][t1]
        delta_prev[t]=1-omicron_prev[t]
        beta[t]=omicron_prev[t]*omicron_beta+delta_prev[t]*delta_beta
        YHRr[t]=omicron_prev[t]*omicron_YHR+delta_prev[t]*delta_YHR
    elif current_date>delta_start:
        number_variants[t]=2
        t1=(current_date-delta_start).days
        delta_prev[t]=df_delta['delta_prev'][t1]
        predelta_prev[t]=1-delta_prev[t]
        beta[t]=delta_prev[t]*delta_beta+predelta_prev[t]*predelta_beta
        YHRr[t]=delta_prev[t]*delta_YHR+predelta_prev[t]*predelta_YHR
    else:
        number_variants[t]=1
        predelta_prev[t]=1
        beta[t]=predelta_prev[t]*predelta_beta
        YHRr[t]=predelta_prev[t]*predelta_YHR


immune_evasion= 0.002848550057
step_size=9
rate_immune = discrete_approx(immune_evasion, step_size)

potentialnew_immuneescape=random.uniform(0.1,0.3)
omicron_immuneescape=0.22
delta_immuneescape=0
predelta_immuneescape=0
        
X_days = mdates.drange(Simulation_start,Simulation_end,dt.timedelta(days=1))

fig1 = plt.figure(dpi=300)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=60))
plt.plot(X_days,number_variants)
plt.gcf().autofmt_xdate()
plt.ylabel("number of variants")
plt.show()

fig2 = plt.figure(dpi=300)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=60))
plt.plot(X_days,predelta_prev,'r',label='pre delta')
plt.plot(X_days,delta_prev,'b',label='delta')
plt.plot(X_days,omicron_prev,'g',label='omicron')
plt.plot(X_days,potentialnew_prev,'k',label='potentialnew')
plt.gcf().autofmt_xdate()
plt.ylabel("Prev%")
plt.legend()
plt.show()

fig3 = plt.figure(dpi=300)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=60))
plt.plot(X_days,beta,'k')
plt.gcf().autofmt_xdate()
plt.ylabel("beta")
plt.show()

fig4 = plt.figure(dpi=300)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=60))
plt.plot(X_days,YHRr,'k')
plt.gcf().autofmt_xdate()
plt.ylabel("current YHR/ standard YHR")
plt.show()

print("predelta start date:" + str(predelta_start))
print("predelta beta:" + str(predelta_beta))
print("predelta immune escape:" + str(predelta_immuneescape))
print("predelta YHR / standard YHR:" + str(predelta_YHR))
print("-----------")
print("delta start date:"+ str(delta_start))
print("delta beta:" + str(delta_beta))
print("delta immune escape:" + str(delta_immuneescape))
print("delta YHR / standard YHR:" + str(delta_YHR))
print("-----------")
print("omicron start date:"+str(omicron_start))
print("omicron beta:"+str(omicron_beta))
print("omicron immune escape:" + str(omicron_immuneescape))
print("omicron YHR / standard YHR:" + str(omicron_YHR))
print("-----------")
print("new varint start date:"+str(potentialnew_start))
print("new varint beta:"+str(potentialnew_beta))
print("new varint immune escape:" + str(potentialnew_immuneescape))
print("new varint YHR / standard YHR:" + str(potentialnew_YHR))