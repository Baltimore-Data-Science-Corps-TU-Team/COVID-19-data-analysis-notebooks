# -*- coding: utf-8 -*-
"""
Created on Thu Nov 12 21:47:44 2020

@author: Arun
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

#np.corrcoef(x,y)

df = pd.read_csv('COVID_Cleaned.csv')
df1 = pd.read_csv('Bmore_COVID_NewCasesByDate.csv')

df = df.transpose()
#df.to_csv('test.csv')
df = df.drop('Unnamed: 0')
df = df.reset_index()

df.columns = df.iloc[0]

df = df.rename(columns={'Date':'Zip Code'})
df = df.drop([0,0])
df.to_csv('COVID_Cleaned_Transposed.csv')
latestCases = pd.DataFrame()

latestCases['Zip Code'] = df['Zip Code']
latestCases['Total Cases'] = df.iloc[:,-1]

latestCases['Zip Code'] = latestCases['Zip Code'].map(lambda x : x.rstrip('0').rstrip('.'))
latestCases['Zip Code'] = latestCases['Zip Code'].astype(int)
latestCases['Total Cases'] = latestCases['Total Cases'].astype(int)

meanList = []
medianList = []
#[rows : columns]
#loop through rows to calculate mean/median new cases per day per zip code
for x in range(0,len(df1.index)):
    #add values to list
    meanList.append(df1.iloc[x,2:].mean())
    medianList.append(df1.iloc[x,2:].median())

#add to latest cases
latestCases.insert(2,'meanNewCases',meanList)
latestCases.insert(3,'medianNewCases',medianList)

latestCases.to_csv('TotalMeanMedianCOVIDbyZip.csv')
#Empirical Cumulative Distribution Function
def ecdf(df):
    n = len(df)
    x = np.sort(df)
    y = np.arange(1, n + 1) /n
    return x, y

#squash and sort data for ECDF plotting
x_totalCases, y_totalCases = ecdf(latestCases['Total Cases'])
x_meanCases, y_meanCases = ecdf(latestCases['meanNewCases'])
x_medianCases, y_medianCases = ecdf(latestCases['medianNewCases'])

#plot ECDF of Mean new cases daily vs total cases
_ = plt.figure(figsize=(12,6.75))
_ = plt.plot(x_totalCases,y_totalCases,marker='.',linestyle='-')
_ = plt.plot(x_meanCases,y_meanCases,marker='.',linestyle='-')
_ = plt.plot(x_medianCases,y_medianCases,marker='.',linestyle='-')
_ = plt.legend(('Total Reported Cases','Mean New Cases/Day','Median New Cases/Day'),loc='lower right')
_ = plt.xlabel('Reported COVID-19 Cases')
_ = plt.ylabel('ECDF')
_ = plt.title('ECDF of Baltimore City (Reported) COVID-19 Cases by Zip Code')
plt.show()

#boxplot of total cases by zip
_ = plt.figure(figsize=(6,8))
_ = sns.boxplot(y='Total Cases',data=latestCases[['Zip Code','Total Cases']])
_ = plt.xlabel('Baltimore City')
_ = plt.ylabel('Total Reported COVID-19 Cases')
_ = plt.title('Baltimore COVID-19 Total (Reported) Cases by Zip Code')
plt.show()

#swarmplot of total cases by zip
_ = plt.figure(figsize=(6,8))
_ = sns.swarmplot(y='Total Cases',data=latestCases[['Zip Code','Total Cases']])
_ = plt.xlabel('Baltimore City')
_ = plt.title('Baltimore COVID-19 Total (Reported) Cases by Zip Code')
plt.show()