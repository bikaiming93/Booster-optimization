# -*- coding: utf-8 -*-
"""
Created on Fri Jun  3 12:04:14 2022

@author: kb44774
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df=pd.read_csv('COVID-19_Vaccinations_in_the_United_States_County.csv',usecols=['Date','Recip_County','Recip_State','Booster_Doses_Vax_Pct','Booster_Doses_12Plus_Vax_Pct','Booster_Doses_18Plus_Vax_Pct','Booster_Doses_50Plus_Vax_Pct','Booster_Doses_65Plus_Vax_Pct'])

options=['Travis County']
Austin_df=df[df['Recip_County'].isin(options)]
#Austin_df=Austin_df.dropna(subset=['Booster_Doses_Vax_Pct'])
Austin_df=Austin_df.fillna(0)
Austin_df['Date']=pd.to_datetime(Austin_df['Date'])
Austin_df.sort_values(by='Date', inplace=True)

'''
fig,ax=plt.subplots(dpi=300)
ax.plot(Austin_df["Date"],Austin_df["Booster_Doses_Vax_Pct"],label='Booster%')
ax.plot(Austin_df["Date"],Austin_df["Booster_Doses_12Plus_Vax_Pct"],label='12+ Booster%')
ax.plot(Austin_df["Date"],Austin_df["Booster_Doses_18Plus_Vax_Pct"],label='18+ Booster%')
ax.plot(Austin_df["Date"],Austin_df["Booster_Doses_50Plus_Vax_Pct"],label='50+ Booster%')
ax.plot(Austin_df["Date"],Austin_df["Booster_Doses_65Plus_Vax_Pct"],label='65+ Booster%')
fig.autofmt_xdate()
plt.legend(loc='upper left', prop={'size': 10})
plt.title("Travis county booster% by CDC",fontsize=15)
plt.show()
'''
Austin_df=Austin_df.drop(['Recip_County','Recip_State'],axis=1)
Austin_diff=Austin_df.diff(axis=0)


Austin_diff['Booster_Doses_Vax_Pct'] = Austin_diff['Booster_Doses_Vax_Pct'].mask(Austin_diff['Booster_Doses_Vax_Pct'] > 2, 0)
Austin_diff['Booster_Doses_Vax_Pct'] = Austin_diff['Booster_Doses_Vax_Pct'].mask(Austin_diff['Booster_Doses_Vax_Pct'] < 0, 0)
Austin_diff['Booster_Doses_12Plus_Vax_Pct'] = Austin_diff['Booster_Doses_12Plus_Vax_Pct'].mask(Austin_diff['Booster_Doses_12Plus_Vax_Pct'] > 2, 0)
Austin_diff['Booster_Doses_12Plus_Vax_Pct'] = Austin_diff['Booster_Doses_12Plus_Vax_Pct'].mask(Austin_diff['Booster_Doses_12Plus_Vax_Pct'] < 0, 0)
Austin_diff['Booster_Doses_18Plus_Vax_Pct'] = Austin_diff['Booster_Doses_18Plus_Vax_Pct'].mask(Austin_diff['Booster_Doses_18Plus_Vax_Pct'] > 2, 0)
Austin_diff['Booster_Doses_18Plus_Vax_Pct'] = Austin_diff['Booster_Doses_18Plus_Vax_Pct'].mask(Austin_diff['Booster_Doses_18Plus_Vax_Pct'] < 0, 0)
Austin_diff['Booster_Doses_50Plus_Vax_Pct'] = Austin_diff['Booster_Doses_50Plus_Vax_Pct'].mask(Austin_diff['Booster_Doses_50Plus_Vax_Pct'] > 2, 0)
Austin_diff['Booster_Doses_50Plus_Vax_Pct'] = Austin_diff['Booster_Doses_50Plus_Vax_Pct'].mask(Austin_diff['Booster_Doses_50Plus_Vax_Pct'] < 0, 0)
Austin_diff['Booster_Doses_65Plus_Vax_Pct'] = Austin_diff['Booster_Doses_65Plus_Vax_Pct'].mask(Austin_diff['Booster_Doses_65Plus_Vax_Pct'] > 2, 0)
Austin_diff['Booster_Doses_65Plus_Vax_Pct'] = Austin_diff['Booster_Doses_65Plus_Vax_Pct'].mask(Austin_diff['Booster_Doses_65Plus_Vax_Pct'] < 0, 0)

'''
fig3,ax=plt.subplots(dpi=300)
ax.plot(Austin_df["Date"],Austin_diff["Booster_Doses_Vax_Pct"],label='Booster%')
ax.plot(Austin_df["Date"],Austin_diff["Booster_Doses_12Plus_Vax_Pct"],label='12+ Booster%')
ax.plot(Austin_df["Date"],Austin_diff["Booster_Doses_18Plus_Vax_Pct"],label='18+ Booster%')
ax.plot(Austin_df["Date"],Austin_diff["Booster_Doses_50Plus_Vax_Pct"],label='50+ Booster%')
ax.plot(Austin_df["Date"],Austin_diff["Booster_Doses_65Plus_Vax_Pct"],label='65+ Booster%')
fig3.autofmt_xdate()
plt.legend(loc='upper left', prop={'size': 10})
plt.title("Travis county booster daily new% by CDC",fontsize=15)
plt.show()        
'''        

df2=pd.read_csv('COVID-19_Vaccinations_in_the_United_States_County.csv',usecols=['Date','Recip_County','Series_Complete_Pop_Pct','Series_Complete_5PlusPop_Pct','Series_Complete_5to17Pop_Pct','Series_Complete_12PlusPop_Pct','Series_Complete_18PlusPop_Pct','Series_Complete_65PlusPop_Pct'])
options=['Travis County']
Austin_df2=df2[df2['Recip_County'].isin(options)]
Austin_df2=Austin_df2.dropna(subset=['Series_Complete_Pop_Pct'])
Austin_df2=Austin_df2.fillna(0)
Austin_df2['Date']=pd.to_datetime(Austin_df2['Date'])
Austin_df2.sort_values(by='Date', inplace=True)

'''
fig2,ax2=plt.subplots(dpi=300)
ax2.plot(Austin_df2["Date"],Austin_df2["Series_Complete_Pop_Pct"],label='2-doses%')
ax2.plot(Austin_df2["Date"],Austin_df2["Series_Complete_5PlusPop_Pct"],label='5+ 2-doses%')
#ax2.plot(Austin_df2["Date"],Austin_df2["Series_Complete_5to17Pop_Pct"],label='5-17 2-doses%')
ax2.plot(Austin_df2["Date"],Austin_df2["Series_Complete_12PlusPop_Pct"],label='12+ 2-doses%')
ax2.plot(Austin_df2["Date"],Austin_df2["Series_Complete_18PlusPop_Pct"],label='18+ 2-doses%')
ax2.plot(Austin_df2["Date"],Austin_df2["Series_Complete_65PlusPop_Pct"],label='65+ 2-doses%')
fig2.autofmt_xdate()
plt.legend(loc='upper left', prop={'size': 10})
plt.title("Travis county 2-doses by CDC",fontsize=15)
plt.show()
'''
Austin_df2=Austin_df2.drop(['Recip_County'],axis=1)
Austin_diff2=Austin_df2.diff(axis=0)

Austin_diff2['Series_Complete_Pop_Pct'] = Austin_diff2['Series_Complete_Pop_Pct'].mask(Austin_diff2['Series_Complete_Pop_Pct'] > 2, 0)
Austin_diff2['Series_Complete_Pop_Pct'] = Austin_diff2['Series_Complete_Pop_Pct'].mask(Austin_diff2['Series_Complete_Pop_Pct'] < 0, 0)
Austin_diff2['Series_Complete_5PlusPop_Pct'] = Austin_diff2['Series_Complete_5PlusPop_Pct'].mask(Austin_diff2['Series_Complete_5PlusPop_Pct'] > 2, 0)
Austin_diff2['Series_Complete_5PlusPop_Pct'] = Austin_diff2['Series_Complete_5PlusPop_Pct'].mask(Austin_diff2['Series_Complete_5PlusPop_Pct'] < 0, 0)
Austin_diff2['Series_Complete_12PlusPop_Pct'] = Austin_diff2['Series_Complete_12PlusPop_Pct'].mask(Austin_diff2['Series_Complete_12PlusPop_Pct'] > 2, 0)
Austin_diff2['Series_Complete_12PlusPop_Pct'] = Austin_diff2['Series_Complete_12PlusPop_Pct'].mask(Austin_diff2['Series_Complete_12PlusPop_Pct'] < 0, 0)
Austin_diff2['Series_Complete_18PlusPop_Pct'] = Austin_diff2['Series_Complete_18PlusPop_Pct'].mask(Austin_diff2['Series_Complete_18PlusPop_Pct'] > 2, 0)
Austin_diff2['Series_Complete_18PlusPop_Pct'] = Austin_diff2['Series_Complete_18PlusPop_Pct'].mask(Austin_diff2['Series_Complete_18PlusPop_Pct'] < 0, 0)
Austin_diff2['Series_Complete_65PlusPop_Pct'] = Austin_diff2['Series_Complete_65PlusPop_Pct'].mask(Austin_diff2['Series_Complete_65PlusPop_Pct'] > 2, 0)
Austin_diff2['Series_Complete_65PlusPop_Pct'] = Austin_diff2['Series_Complete_65PlusPop_Pct'].mask(Austin_diff2['Series_Complete_65PlusPop_Pct'] < 0, 0)


'''

fig4,ax=plt.subplots(dpi=300)
ax.plot(Austin_df2["Date"],Austin_diff2["Series_Complete_Pop_Pct"],label='Booster%')
ax.plot(Austin_df2["Date"],Austin_diff2["Series_Complete_5PlusPop_Pct"],label='5+ Booster%')
ax.plot(Austin_df2["Date"],Austin_diff2["Series_Complete_12PlusPop_Pct"],label='12+ Booster%')
ax.plot(Austin_df2["Date"],Austin_diff2["Series_Complete_18PlusPop_Pct"],label='18+ Booster%')
ax.plot(Austin_df2["Date"],Austin_diff2["Series_Complete_65PlusPop_Pct"],label='65+ Booster%')
fig4.autofmt_xdate()
plt.legend(loc='upper left', prop={'size': 10})
plt.title("Travis county 2-dose daily new% by CDC",fontsize=15)
plt.show()  
'''


result=Austin_diff.loc[Austin_diff['Booster_Doses_Vax_Pct'] >0,'Date'].values[0]
result=result.astype('datetime64[D]').tolist()
print(result)