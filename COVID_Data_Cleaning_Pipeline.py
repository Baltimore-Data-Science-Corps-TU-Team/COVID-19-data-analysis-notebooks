# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 20:54:43 2020

@author: Arun
"""
import pandas as pd

c2n = pd.read_excel('CSA-to-NSA-2010.xlsx')
hinc = pd.read_excel('Vital Signs Indicator Median Household Income.xlsx')
z2c = pd.read_excel('Zip-to-CSA-2010.xls')
df = pd.read_csv('MDCOVID19_MASTER_ZIP_CODE_CASES.csv')

#pipeline raw data -> cleaned rows:dates, columns:zips------------------------
zipsList = [21227,21207,21230,21251,21229,21237,21287,21231,21226,21206,21222,21225,21211,21208,\
            21205,21218,21234,21202,21201,21213,21210,21209,21216,21236,21217,21224,21215,21212,\
                21223,21214,21239,21228]

df = df[df['ZIP_CODE'].isin(zipsList)]

df = df.fillna(0)
df = df.drop('OBJECTID', axis=1)

df = df.transpose()

df.columns = df.iloc[0]
df = df.drop('ZIP_CODE')
df = df.reset_index()
df = df.rename(columns={'index':'Date'})

df['Date'] = df['Date'].map(lambda x: x.lstrip('F').lstrip('t').lstrip('o').lstrip('t')\
                            .lstrip('a').lstrip('l'))

dates = pd.DataFrame()
dates = df['Date'].str.split(pat='_', expand=True)
dates[0] = dates[0].map(lambda x: x.lstrip('0'))
dates['fdate'] = dates[2].str.cat(dates[0], sep='-').str.cat(dates[1],sep='-')

dates = dates['fdate']

df = df.drop('Date',axis=1)

df.insert(0,'Date',dates)

df['Date'] = pd.to_datetime(df['Date'])

#print(df)
df.to_csv('COVID_Cleaned.csv')


#pipeline rows:dates, columns:zips -> rows:zips, columns:zips-----------------
df = df.transpose()
#df.to_csv('test.csv')
#df = df.drop('Unnamed: 0')
df = df.reset_index()

df.columns = df.iloc[0]

df = df.rename(columns={'Date':'Zip Code'})
df1 = df.drop([0,0])

#print(df1)
df1.to_csv('COVID_Cleaned_Transposed.csv')


#pipeline zips, CSAs, NSAs, MHINC, total COVID cases -> one file--------------
zipsLatest = pd.DataFrame()

zipsLatest['Zip'] = df1['Zip Code'].astype(int)
zipsLatest['TotalCOVIDCases'] = df1.iloc[:,-1]

#rename columns appropriately
z2c = z2c.rename(columns={'Zip2010':'Zip','CSA2010':'CSA'})
c2n = c2n.rename(columns={'CSA2010':'Community'})

#merge, rename Household income and CSAs-to-Neighborhoods
df = pd.merge_ordered(hinc, c2n, fill_method='ffill')
df = df.rename(columns={'2018 Data':'MHINC','NSA2010':'Neigh','Community':'CSA'})
df = df[['Neigh','CSA','MHINC']]

#merge with Zip Codes
df = pd.merge_ordered(z2c,df,fill_method='ffill')

#drop commas from household income numbers, convert to float
df['MHINC'] = df['MHINC'].replace(',','',regex=True)
df['MHINC'] = df['MHINC'].astype(float)

#convert zips to ints
df['Zip'] = df['Zip'].astype(int)

#merge with latest covid cases
df = pd.merge_ordered(zipsLatest,df,fill_method='ffill')
df = df[['Neigh','CSA','Zip','MHINC','TotalCOVIDCases']]

#export as CSV
df.to_csv('MASTER_MERGED.csv',index=False)
#print(df)


#pipeline COVID_Cleaned_Transposed -> Daily Increase--------------------------
cc = pd.read_csv('COVID_Cleaned.csv')

cc = cc.transpose()
cc = cc.drop('Unnamed: 0')
cc = cc.reset_index()

cc.columns = cc.iloc[0]

cc = cc.rename(columns={'Date':'Zip Code'})
cc = cc.drop([0,0]) 

cc1 = cc.loc[:,'2020-04-11':]\
        .diff(axis=1)\
        .drop(columns='2020-04-11')\
  

dates = cc['Zip Code']
cc1.insert(0,'Zip Code',dates)    

#cc1['Zip Code'] = cc1['Zip Code'].astype(float).astype(int) 
cc.to_csv('Bmore_COVID_NewCasesByDate.csv')
#print(cc)

#pipeline -> Mean, median new cases, total cases
latestCases = pd.DataFrame()

latestCases['Zip Code'] = df1['Zip Code']
latestCases['Total Cases'] = df1.iloc[:,-1]

#latestCases['Zip Code'] = latestCases['Zip Code'].map(lambda x : x.rstrip('0').rstrip('.'))
latestCases['Zip Code'] = latestCases['Zip Code'].astype(int)
latestCases['Total Cases'] = latestCases['Total Cases'].astype(int)

meanList = []
medianList = []
#[rows : columns]
#loop through rows to calculate mean/median new cases per day per zip code
for x in range(0,len(cc.index)):
    #add values to list
    meanList.append(cc.iloc[x,2:].mean())
    medianList.append(cc.iloc[x,2:].median())

#add to latest cases
latestCases.insert(2,'meanNewCasesPerDay',meanList)
latestCases.insert(3,'medianNewCasesPerDay',medianList)

latestCases.to_csv('TotalMeanMedianCOVIDbyZip.csv')
print(latestCases)