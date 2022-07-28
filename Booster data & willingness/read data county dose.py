# -*- coding: utf-8 -*-
"""
Created on Fri Jun 10 14:32:54 2022

@author: kb44774
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df=pd.read_csv('COVID-19_Vaccinations_in_the_United_States_County.csv',usecols=['Date','Recip_County','Booster_Doses','Booster_Doses_12Plus','Booster_Doses_18Plus','Booster_Doses_50Plus','Booster_Doses_65Plus'])

Travis_total=int(1300503)
Travis_0to4=int(76226)
Travis_5to17=int(193250)
Travis_18to50=int(647206)
Travis_50to64=int(212703)
Travis_65plus=int(136406)

Travis_50plus=Travis_65plus+Travis_50to64
Travis_18plus=Travis_50plus+Travis_18to50
Travis_12plus=int(1091726)
Travis_5plus=Travis_total-Travis_0to4

options=['Travis County']
Austin_df=df[df['Recip_County'].isin(options)]
Austin_df=Austin_df.dropna(subset=['Booster_Doses'])
Austin_df=Austin_df.fillna(0)
Austin_df['Date']=pd.to_datetime(Austin_df['Date'])
Austin_df.sort_values(by='Date', inplace=True)

Austin_df['Booster_Doses']=Austin_df['Booster_Doses'].str.replace(',', '').astype(float)
Austin_df['Booster_Doses_12Plus']=Austin_df['Booster_Doses_12Plus'].str.replace(',', '').astype(float)
Austin_df['Booster_Doses_18Plus']=Austin_df['Booster_Doses_18Plus'].str.replace(',', '').astype(float)
Austin_df['Booster_Doses_50Plus']=Austin_df['Booster_Doses_50Plus'].str.replace(',', '').astype(float)
Austin_df['Booster_Doses_65Plus']=Austin_df['Booster_Doses_65Plus'].str.replace(',', '').astype(float)

fig,ax=plt.subplots(dpi=300)
ax.plot(Austin_df["Date"],Austin_df["Booster_Doses"]/Travis_total,label='Booster%')
ax.plot(Austin_df["Date"],Austin_df["Booster_Doses_12Plus"]/Travis_12plus,label='12+ Booster%')
ax.plot(Austin_df["Date"],Austin_df["Booster_Doses_18Plus"]/Travis_18plus,label='18+ Booster%')
ax.plot(Austin_df["Date"],Austin_df["Booster_Doses_50Plus"]/Travis_50plus,label='50+ Booster%')
ax.plot(Austin_df["Date"],Austin_df["Booster_Doses_65Plus"]/Travis_65plus,label='65+ Booster%')
fig.autofmt_xdate()
plt.legend(loc='upper left', prop={'size': 10})
plt.title("Travis county booster% by CDC",fontsize=15)
plt.show()

Austin_df=Austin_df.drop(['Recip_County'],axis=1)
Austin_diff=Austin_df.diff(axis=0)
Austin_diff["Booster_Doses"]=Austin_diff["Booster_Doses"]/Travis_total
Austin_diff["Booster_Doses_12Plus"]=Austin_diff["Booster_Doses_12Plus"]/Travis_12plus
Austin_diff["Booster_Doses_18Plus"]=Austin_diff["Booster_Doses_18Plus"]/Travis_18plus
Austin_diff['Booster_Doses_50Plus']=Austin_diff['Booster_Doses_50Plus']/Travis_50plus
Austin_diff["Booster_Doses_65Plus"]=Austin_diff["Booster_Doses_65Plus"]/Travis_65plus


Austin_diff['Booster_Doses'] = Austin_diff['Booster_Doses'].mask(Austin_diff['Booster_Doses'] > 0.05, 0)
Austin_diff['Booster_Doses_12Plus'] = Austin_diff['Booster_Doses_12Plus'].mask(Austin_diff['Booster_Doses_12Plus'] > 0.05, 0)
Austin_diff['Booster_Doses_18Plus'] = Austin_diff['Booster_Doses_18Plus'].mask(Austin_diff['Booster_Doses_18Plus'] > 0.05, 0)
Austin_diff['Booster_Doses_50Plus'] = Austin_diff['Booster_Doses_50Plus'].mask(Austin_diff['Booster_Doses_50Plus'] > 0.05, 0)
Austin_diff['Booster_Doses_65Plus'] = Austin_diff['Booster_Doses_65Plus'].mask(Austin_diff['Booster_Doses_65Plus'] > 0.05, 0)

fig2,ax2=plt.subplots(dpi=300)
ax2.plot(Austin_df["Date"],Austin_diff["Booster_Doses"],label='Booster%')
ax2.plot(Austin_df["Date"],Austin_diff["Booster_Doses_12Plus"],label='12+ Booster%')
ax2.plot(Austin_df["Date"],Austin_diff["Booster_Doses_18Plus"],label='18+ Booster%')
ax2.plot(Austin_df["Date"],Austin_diff["Booster_Doses_50Plus"],label='50+ Booster%')
ax2.plot(Austin_df["Date"],Austin_diff["Booster_Doses_65Plus"],label='65+ Booster%')
fig2.autofmt_xdate()
plt.legend(loc='upper right', prop={'size': 10})
plt.title("Travis county new booster% by CDC",fontsize=15)
plt.show()

output_df=pd.DataFrame()
output_df['vaccine_time']=Austin_df["Date"]
output_df['vaccine_time'] = output_df['vaccine_time'].dt.strftime('%m/%d/%Y')
output_df['vaccine_amount']=Austin_diff["Booster_Doses"]
output_df['A1-R1']=0
output_df['A1-R2']=0

output_df['A5-R1']=Austin_diff['Booster_Doses_65Plus']*Travis_65plus * 0.56
output_df['A5-R2']=Austin_diff['Booster_Doses_65Plus']*Travis_65plus * 0.44
output_df['A4-R1']=((Austin_diff['Booster_Doses_50Plus']*Travis_50plus)-(Austin_diff['Booster_Doses_65Plus']*Travis_65plus))*0.7
output_df['A4-R2']=((Austin_diff['Booster_Doses_50Plus']*Travis_50plus)-(Austin_diff['Booster_Doses_65Plus']*Travis_65plus))*0.3
output_df['A3-R1']=((Austin_diff['Booster_Doses_18Plus']*Travis_18plus)-(Austin_diff['Booster_Doses_50Plus']*Travis_50plus)-(Austin_diff['Booster_Doses_65Plus']*Travis_65plus))*0.85
output_df['A3-R2']=((Austin_diff['Booster_Doses_18Plus']*Travis_18plus)-(Austin_diff['Booster_Doses_50Plus']*Travis_50plus)-(Austin_diff['Booster_Doses_65Plus']*Travis_65plus))*0.15
output_df['A2-R1']=(Austin_diff['Booster_Doses']*Travis_total-(Austin_diff['Booster_Doses_18Plus']*Travis_18plus)-(Austin_diff['Booster_Doses_50Plus']*Travis_50plus)-(Austin_diff['Booster_Doses_65Plus']*Travis_65plus))*0.9
output_df['A2-R2']=(Austin_diff['Booster_Doses']*Travis_total-(Austin_diff['Booster_Doses_18Plus']*Travis_18plus)-(Austin_diff['Booster_Doses_50Plus']*Travis_50plus)-(Austin_diff['Booster_Doses_65Plus']*Travis_65plus))*0.1

output_df['A2-R2']=output_df['A2-R2'].mask(output_df['A2-R2']<0,0)
output_df['A2-R1']=output_df['A2-R1'].mask(output_df['A2-R1']<0,0)


output_df.to_csv('booster_allocation.csv', index=False)


