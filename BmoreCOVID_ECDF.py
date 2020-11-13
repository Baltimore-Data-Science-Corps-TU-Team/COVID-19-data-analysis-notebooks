# -*- coding: utf-8 -*-
"""
Created on Thu Nov 12 21:47:44 2020

@author: Arun
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from pylab import rcParams

df = pd.read_csv('COVID_Cleaned.csv')
df1 = pd.read_csv('Bmore_COVID_NewCasesByDate.csv')

df = df.transpose()
#df.to_csv('test.csv')
df = df.drop('Unnamed: 0')
df = df.reset_index()

df.columns = df.iloc[0]

df = df.rename(columns={'Date':'Zip Code'})
df = df.drop([0,0])

latestCases = pd.DataFrame()

latestCases['Zip Code'] = df['Zip Code']
latestCases['Total Cases'] = df.iloc[:,-1]

latestCases['Zip Code'] = latestCases['Zip Code'].map(lambda x : x.rstrip('0').rstrip('.'))
latestCases['Zip Code'] = latestCases['Zip Code'].astype(int)
latestCases['Total Cases'] = latestCases['Total Cases'].astype(int)

latestCases.to_csv('TotalCOVIDbyZip.csv')

meanList = []
#[rows : columns]
#loop through rows to calculate mean new cases per day per zip code
for x in range(0,len(df1.index)):
    #add values to list
    meanList.append(df1.iloc[x,2:].mean())
    

#add to latest cases
latestCases.insert(2,'meanNewCases',meanList)

#Empirical Cumulative Distribution Function
def ecdf(df):
    n = len(df)
    x = np.sort(df)
    y = np.arange(1, n + 1) /n
    return x, y

#squash and sort data for ECDF plotting
x_totalCases, y_totalCases = ecdf(latestCases['Total Cases'])
x_meanCases, y_meanCases = ecdf(latestCases['meanNewCases'])

#plot ECDF of Mean new cases daily vs total cases
_ = plt.figure(figsize=(8,4.5))
_ = plt.plot(x_totalCases,y_totalCases,marker='.',linestyle='none')
_ = plt.plot(x_meanCases,y_meanCases,marker='.',linestyle='none')
_ = plt.legend(('Total Reported Cases','Mean New Cases/Day'),loc='lower right')

_ = plt.xlabel('Reported COVID-19 Cases')
_ = plt.ylabel('ECDF')
_ = plt.title('ECDF of Baltimore City COVID-19 Cases by Zip Code')
plt.show()