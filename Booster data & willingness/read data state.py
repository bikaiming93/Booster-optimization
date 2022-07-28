# -*- coding: utf-8 -*-
"""
Created on Mon Jun  6 11:21:51 2022

@author: kb44774
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import matplotlib.dates as mdates

df=pd.read_csv('COVID-19_Vaccinations_in_the_United_States_Jurisdiction.csv',usecols=['Date','Location','Additional_Doses_Vax_Pct','Additional_Doses_5Plus_Vax_Pct','Additional_Doses_12Plus_Vax_Pct','Additional_Doses_18Plus_Vax_Pct','Additional_Doses_50Plus_Vax_Pct','Additional_Doses_65Plus_Vax_Pct','Administered_Dose1_Recip_5PlusPop_Pct'])

options=['TX']
TX_df=df[df['Location'].isin(options)]
TX_df=TX_df.dropna(subset=['Additional_Doses_Vax_Pct'])
TX_df=TX_df.fillna(0)
TX_df['Date']=pd.to_datetime(TX_df['Date'])
TX_df.sort_values(by='Date', inplace=True)
#TX_df.to_csv('TX.csv', encoding='utf-8') 

fig,ax=plt.subplots(dpi=300)
ax.plot(TX_df["Date"],TX_df["Additional_Doses_Vax_Pct"],label='Booster%')
#ax.plot(TX_df["Date"],TX_df["Administered_Dose1_Recip_5PlusPop_Pct"],label='5+ Booster%')
ax.plot(TX_df["Date"],TX_df["Additional_Doses_12Plus_Vax_Pct"],label='12+ Booster%')
ax.plot(TX_df["Date"],TX_df["Additional_Doses_18Plus_Vax_Pct"],label='18+ Booster%')
ax.plot(TX_df["Date"],TX_df["Additional_Doses_50Plus_Vax_Pct"],label='50+ Booster%')
ax.plot(TX_df["Date"],TX_df["Additional_Doses_65Plus_Vax_Pct"],label='65+ Booster%')
fig.autofmt_xdate()
plt.legend(loc='upper left', prop={'size': 10})
plt.title("Texas state booster% by CDC",fontsize=15)
plt.show()

TX_df=TX_df.drop(['Location'],axis=1)
TX_diff=TX_df.diff(axis=0)

TX_diff['Additional_Doses_Vax_Pct'] = TX_diff['Additional_Doses_Vax_Pct'].mask(TX_diff['Additional_Doses_Vax_Pct'] > 2, 0)
TX_diff['Additional_Doses_Vax_Pct'] = TX_diff['Additional_Doses_Vax_Pct'].mask(TX_diff['Additional_Doses_Vax_Pct'] < 0, 0)
TX_diff['Additional_Doses_12Plus_Vax_Pct'] = TX_diff['Additional_Doses_12Plus_Vax_Pct'].mask(TX_diff['Additional_Doses_12Plus_Vax_Pct'] > 2, 0)
TX_diff['Additional_Doses_12Plus_Vax_Pct'] = TX_diff['Additional_Doses_12Plus_Vax_Pct'].mask(TX_diff['Additional_Doses_12Plus_Vax_Pct'] < 0, 0)
TX_diff['Additional_Doses_18Plus_Vax_Pct'] = TX_diff['Additional_Doses_18Plus_Vax_Pct'].mask(TX_diff['Additional_Doses_18Plus_Vax_Pct'] > 2, 0)
TX_diff['Additional_Doses_18Plus_Vax_Pct'] = TX_diff['Additional_Doses_18Plus_Vax_Pct'].mask(TX_diff['Additional_Doses_18Plus_Vax_Pct'] < 0, 0)
TX_diff['Additional_Doses_50Plus_Vax_Pct'] = TX_diff['Additional_Doses_50Plus_Vax_Pct'].mask(TX_diff['Additional_Doses_50Plus_Vax_Pct'] > 2, 0)
TX_diff['Additional_Doses_50Plus_Vax_Pct'] = TX_diff['Additional_Doses_50Plus_Vax_Pct'].mask(TX_diff['Additional_Doses_50Plus_Vax_Pct'] < 0, 0)
TX_diff['Additional_Doses_65Plus_Vax_Pct'] = TX_diff['Additional_Doses_65Plus_Vax_Pct'].mask(TX_diff['Additional_Doses_65Plus_Vax_Pct'] > 2, 0)
TX_diff['Additional_Doses_65Plus_Vax_Pct'] = TX_diff['Additional_Doses_65Plus_Vax_Pct'].mask(TX_diff['Additional_Doses_65Plus_Vax_Pct'] < 0, 0)

fig3,ax=plt.subplots(dpi=300)
ax.plot(TX_df["Date"],TX_diff["Additional_Doses_Vax_Pct"],label='Booster%')
ax.plot(TX_df["Date"],TX_diff["Additional_Doses_12Plus_Vax_Pct"],label='12+ Booster%')
ax.plot(TX_df["Date"],TX_diff["Additional_Doses_18Plus_Vax_Pct"],label='18+ Booster%')
ax.plot(TX_df["Date"],TX_diff["Additional_Doses_50Plus_Vax_Pct"],label='50+ Booster%')
ax.plot(TX_df["Date"],TX_diff["Additional_Doses_65Plus_Vax_Pct"],label='65+ Booster%')
fig3.autofmt_xdate()
plt.legend(loc='upper left', prop={'size': 10})
plt.title("Texas state booster daily new% by CDC",fontsize=15)
plt.show()        
        
    


df2=pd.read_csv('COVID-19_Vaccinations_in_the_United_States_Jurisdiction.csv',usecols=['Date','Location','Series_Complete_Pop_Pct','Series_Complete_5PlusPop_Pct','Series_Complete_12PlusPop_Pct','Series_Complete_18PlusPop_Pct','Series_Complete_65PlusPop_Pct'])

options=['TX']
TX_df2=df2[df2['Location'].isin(options)]
TX_df2=TX_df2.dropna(subset=['Series_Complete_Pop_Pct'])
TX_df2=TX_df2.fillna(0)
TX_df2['Date']=pd.to_datetime(TX_df2['Date'])
TX_df2.sort_values(by='Date', inplace=True)

fig2,ax=plt.subplots(dpi=300)
ax.plot(TX_df2["Date"],TX_df2["Series_Complete_Pop_Pct"],label='2-doses%')
ax.plot(TX_df2["Date"],TX_df2["Series_Complete_12PlusPop_Pct"],label='12+ 2-doses%')
ax.plot(TX_df2["Date"],TX_df2["Series_Complete_18PlusPop_Pct"],label='18+ 2-doses%')
ax.plot(TX_df2["Date"],TX_df2["Series_Complete_65PlusPop_Pct"],label='65+ 2-doses%')
fig2.autofmt_xdate()
plt.legend(loc='upper left', prop={'size': 10})
plt.title("Texas state 2-doses by CDC",fontsize=15)
plt.show()

TX_df2=TX_df2.drop(['Location'],axis=1)
TX_diff2=TX_df2.diff(axis=0)

#TX_df2.to_csv('TX2.csv', encoding='utf-8') 

TX_diff2['Series_Complete_Pop_Pct'] = TX_diff2['Series_Complete_Pop_Pct'].mask(TX_diff2['Series_Complete_Pop_Pct'] > 2, 0)
TX_diff2['Series_Complete_Pop_Pct'] = TX_diff2['Series_Complete_Pop_Pct'].mask(TX_diff2['Series_Complete_Pop_Pct'] < 0, 0)
TX_diff2['Series_Complete_12PlusPop_Pct'] = TX_diff2['Series_Complete_12PlusPop_Pct'].mask(TX_diff2['Series_Complete_12PlusPop_Pct'] > 2, 0)
TX_diff2['Series_Complete_12PlusPop_Pct'] = TX_diff2['Series_Complete_12PlusPop_Pct'].mask(TX_diff2['Series_Complete_12PlusPop_Pct'] < 0, 0)
TX_diff2['Series_Complete_18PlusPop_Pct'] = TX_diff2['Series_Complete_18PlusPop_Pct'].mask(TX_diff2['Series_Complete_18PlusPop_Pct'] > 2, 0)
TX_diff2['Series_Complete_18PlusPop_Pct'] = TX_diff2['Series_Complete_18PlusPop_Pct'].mask(TX_diff2['Series_Complete_18PlusPop_Pct'] < 0, 0)
TX_diff2['Series_Complete_65PlusPop_Pct'] = TX_diff2['Series_Complete_65PlusPop_Pct'].mask(TX_diff2['Series_Complete_65PlusPop_Pct'] > 2, 0)
TX_diff2['Series_Complete_65PlusPop_Pct'] = TX_diff2['Series_Complete_65PlusPop_Pct'].mask(TX_diff2['Series_Complete_65PlusPop_Pct'] < 0, 0)


fig4,ax=plt.subplots(dpi=300)
ax.plot(TX_df2["Date"],TX_diff2["Series_Complete_Pop_Pct"],label='Booster%')
#ax.plot(TX_df["Date"],TX_df["Administered_Dose1_Recip_5PlusPop_Pct"],label='5+ Booster%')
ax.plot(TX_df2["Date"],TX_diff2["Series_Complete_12PlusPop_Pct"],label='12+ Booster%')
ax.plot(TX_df2["Date"],TX_diff2["Series_Complete_18PlusPop_Pct"],label='18+ Booster%')
ax.plot(TX_df2["Date"],TX_diff2["Series_Complete_65PlusPop_Pct"],label='65+ Booster%')
fig4.autofmt_xdate()
plt.legend(loc='upper right', prop={'size': 10})
plt.title("Texas state 2-dose daily new% by CDC",fontsize=15)
plt.show()    

df3=pd.read_csv('COVID-19_Vaccinations_in_the_United_States_Jurisdiction.csv',usecols=['Date','Location','Second_Booster','Second_Booster_50Plus_Vax_Pct','Second_Booster_65Plus_Vax_Pct'])

options=['TX']
TX_df3=df3[df3['Location'].isin(options)]
TX_df3=TX_df3.dropna(subset=['Second_Booster_50Plus_Vax_Pct'])
TX_df3=TX_df3.fillna(0)
TX_df3['Date']=pd.to_datetime(TX_df3['Date'])
TX_df3.sort_values(by='Date', inplace=True) 

fig5,ax=plt.subplots(dpi=300)
#ax.plot(TX_df3["Date"],TX_df3["Second_Booster"],label='2nd booster%')
ax.plot(TX_df3["Date"],TX_df3["Second_Booster_50Plus_Vax_Pct"],label='50+ 2nd booster%')
ax.plot(TX_df3["Date"],TX_df3["Second_Booster_65Plus_Vax_Pct"],label='65+ 2nd booster%')
fig5.autofmt_xdate()
plt.legend(loc='upper left', prop={'size': 10})
plt.title("Texas state 2nd booster by CDC",fontsize=15)
plt.show()

TX_df3=TX_df3.drop(['Location'],axis=1)
TX_diff3=TX_df3.diff(axis=0)

TX_diff3['Second_Booster_50Plus_Vax_Pct'] = TX_diff3['Second_Booster_50Plus_Vax_Pct'].mask(TX_diff3['Second_Booster_50Plus_Vax_Pct'] > 2, 0)
TX_diff3['Second_Booster_50Plus_Vax_Pct'] = TX_diff3['Second_Booster_50Plus_Vax_Pct'].mask(TX_diff3['Second_Booster_50Plus_Vax_Pct'] < 0, 0)
TX_diff3['Second_Booster_65Plus_Vax_Pct'] = TX_diff3['Second_Booster_65Plus_Vax_Pct'].mask(TX_diff3['Second_Booster_65Plus_Vax_Pct'] > 2, 0)
TX_diff3['Second_Booster_65Plus_Vax_Pct'] = TX_diff3['Second_Booster_65Plus_Vax_Pct'].mask(TX_diff3['Second_Booster_65Plus_Vax_Pct'] < 0, 0)

fig6,ax=plt.subplots(dpi=300)
ax.plot(TX_df3["Date"],TX_diff3["Second_Booster_50Plus_Vax_Pct"],label='50+ 2nd Booster%')
ax.plot(TX_df3["Date"],TX_diff3["Second_Booster_65Plus_Vax_Pct"],label='65+ 2nd Booster%')
fig6.autofmt_xdate()
plt.legend(loc='upper right', prop={'size': 10})
plt.title("Texas state 2nd booster daily new% by CDC",fontsize=15)
plt.show() 


#willingness for 18+, 50+ ,65+
TX_df=TX_df.set_index(['Date'])
Select_df_18=TX_df.loc['2021-10-20':'2022-06-16']
#240*7-->booster coverage data


TX_df2=TX_df2.set_index(['Date'])
Select_df2_18=TX_df2.loc['2021-4-23':'2021-12-17']
#239*5-->2 dose coverage data

#print(Select_df_18.iloc[0,5])

willing_booster_65=np.zeros(239)
willing_booster_50=np.zeros(239)
willing_booster_18=np.zeros(239)

age_65=12.9
age_50=17.1
age_18=41.8
age_12=10.7

for i in range(239):
    vac_65=Select_df2_18.iloc[i,4]
    booster_65=Select_df_18.iloc[i,6]
    willing_booster_65[i]=min(max(float((Select_df_18.iloc[i+1,6]-booster_65)/(vac_65-booster_65)),0),0.05)
    vac_18=Select_df2_18.iloc[i,3]
    vac_50=vac_18+(vac_65-vac_18)*0.6
    booster_50=Select_df_18.iloc[i,5]
    willing_50plus=float((Select_df_18.iloc[i+1,5]-booster_50)/(vac_50-booster_50))
    willing_booster_50[i]=min(max(float((willing_50plus*(age_65+age_50)-willing_booster_65[i]*age_65)/age_50),0),0.05)
    booster_18=Select_df_18.iloc[i,4]
    willing_18plus=float((Select_df_18.iloc[i+1,4]-booster_18)/(vac_18-booster_18))
    willing_booster_18[i]=min(max(float((willing_18plus*(age_65+age_50+age_18)-willing_booster_65[i]*age_65-willing_booster_50[i]*age_50)/age_18),0),0.05)
    
now = dt.datetime.strptime('10/21/21', "%m/%d/%y")
then = now + dt.timedelta(days=239)
days = mdates.drange(now,then,dt.timedelta(days=1))

fig7,ax=plt.subplots(dpi=300)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
ax.plot(days,willing_booster_65,color='r',label='65+ 1st Booster willingness%')
plt.legend(loc='upper left', prop={'size': 10})
plt.show()

willing_booster_65_no0=willing_booster_65[75:]
willing_booster_65_no0=[(x*100) for x in willing_booster_65_no0 if (x > 0.0001)&(x<0.03)]
fig8=plt.subplots(dpi=300)
plt.hist(willing_booster_65_no0, bins = np.arange(0,5,0.2), color='red')
plt.xlabel('Willingness in %')
plt.ylabel('Percentage')
plt.title('65+ 1st booster willingness (workday) after Feb 1 2022')

fig9,ax=plt.subplots(dpi=300)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
ax.plot(days,willing_booster_50,color='g',label='50-64 1st Booster willingness%')
plt.legend(loc='upper left', prop={'size': 10})
plt.show()

willing_booster_50_no0=willing_booster_50[75:]
willing_booster_50_no0=[(x*100) for x in willing_booster_50_no0 if (x > 0.0001)&(x<0.03)]
fig10=plt.subplots(dpi=300)
plt.hist(willing_booster_50_no0,bins = np.arange(0,5,0.2), color='green')
plt.xlabel('Willingness in %')
plt.ylabel('Percentage')
plt.title('50-64 1st booster willingness (workday) after Feb 1 2022')

fig11,ax=plt.subplots(dpi=300)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
ax.plot(days,willing_booster_18,color='black',label='18-49 1st Booster willingness%')
plt.legend(loc='upper left', prop={'size': 10})
plt.show()

willing_booster_18_no0=willing_booster_18[75:]
willing_booster_18_no0=[(x*100) for x in willing_booster_18_no0 if (x > 0.0001)&(x<0.03)]
fig12=plt.subplots(dpi=300)
plt.hist(willing_booster_18_no0, bins = np.arange(0,5,0.2), color='black')
plt.xlabel('Willingness in %')
plt.ylabel('Percentage')
plt.title('18-49 1st booster willingness (workday) after Feb 1 2022')

#willingness for 12+
Select_df_12=TX_df.loc['2022-01-27':'2022-06-16']
Select_df2_12=TX_df2.loc['2021-07-31':'2021-12-17']

willing_booster_12=np.zeros(140)

for i in range(140):
    vac_12=Select_df2_12.iloc[i,2]
    booster_12=Select_df_12.iloc[i,3]
    willing_12plus=float((Select_df_12.iloc[i+1,3]-booster_12)/(vac_12-booster_12))
    willing_booster_12[i]=min(max(float((willing_12plus*(age_65+age_50+age_18+age_12)-willing_booster_65[i+98]*age_65-willing_booster_50[i+98]*age_50-willing_booster_18[i+98]*age_18)/age_12),0),0.05)

now = dt.datetime.strptime('01/27/22', "%m/%d/%y")
then = now + dt.timedelta(days=140)
days = mdates.drange(now,then,dt.timedelta(days=1))

fig13,ax=plt.subplots(dpi=300)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
ax.plot(days,willing_booster_12,color='blue',label='12-17 1st Booster willingness%')
plt.legend(loc='upper left', prop={'size': 10})
plt.show()

willing_booster_12_no0=[(x*100) for x in willing_booster_12 if (x > 0.0001)&(x<0.06)]
fig14=plt.subplots(dpi=300)
plt.hist(willing_booster_12_no0,bins = np.arange(0,5,0.2), color='blue')
plt.xlabel('Willingness in %')
plt.ylabel('Percentage')
plt.title('12-17 1st booster willingness (workday) after Feb 1 2022')


TX_df3=TX_df3.set_index(['Date'])
Select_df3_50=TX_df3.loc['2022-04-22':'2022-06-16']
#56rows
#Select_df3_50.to_csv('TX3.csv')

Select_df_50=TX_df.loc['2021-12-24':'2022-02-16']
#55rows
#Select_df_50.to_csv('TX4.csv')

#print(Select_df_50)
#print(Select_df_50.iloc[0,6])

willing_booster2_65=np.zeros(55)
willing_booster2_50=np.zeros(55)


for i in range(55):
    booster2_65=Select_df3_50.iloc[i,2]
    booster_65=Select_df_50.iloc[i,6]
    willing_booster2_65[i]=min(max(float((Select_df3_50.iloc[i+1,2]-booster2_65)/(booster_65-booster2_65)),0),0.05)
    booster2_50=Select_df3_50.iloc[i,1]
    booster_50=Select_df_50.iloc[i,5]
    willing_50plus2=float((Select_df3_50.iloc[i+1,1]-booster2_50)/(booster_50-booster2_50))
    willing_booster2_50[i]=min(max(float((willing_50plus2*(age_65+age_50)-willing_booster2_65[i]*age_65)/age_50),0),0.05)
    
now = dt.datetime.strptime('04/22/22', "%m/%d/%y")
then = now + dt.timedelta(days=55)
days = mdates.drange(now,then,dt.timedelta(days=1))

fig15,ax=plt.subplots(dpi=300)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
ax.plot(days,willing_booster2_65,color='r',label='65+ 2nd Booster willingness%')
plt.legend(loc='upper left', prop={'size': 10})
plt.show()

willing_booster2_65_no0=[(x*100) for x in willing_booster2_65 if (x > 0.0001)&(x<0.2)]
fig16=plt.subplots(dpi=300)
plt.hist(willing_booster2_65_no0,bins = np.arange(0,3,0.2), color='red')
plt.xlabel('Willingness in %')
plt.ylabel('Percentage')
plt.title('65+ 2nd booster willingness (workday) after April 22 2022')

fig17,ax=plt.subplots(dpi=300)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
ax.plot(days,willing_booster2_50,color='green',label='50-64 2nd Booster willingness%')
plt.legend(loc='upper left', prop={'size': 10})
plt.show()

willing_booster2_50_no0=[(x*100) for x in willing_booster2_50 if (x > 0.0001)&(x<0.2)]
fig16=plt.subplots(dpi=300)
plt.hist(willing_booster2_50_no0,bins = np.arange(0,3,0.2), color='green')
plt.xlabel('Willingness in %')
plt.ylabel('Percentage')
plt.title('50-64 2nd booster willingness (workday) after April 22 2022')