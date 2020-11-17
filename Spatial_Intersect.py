# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 23:51:04 2020

@author: Arun
"""

import geopandas as gpd
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

zipcodes = gpd.read_file('zipcode.geojson')
neighs = gpd.read_file('Maryland_Baltimore_City_Neighborhoods.geojson')
mhinc = pd.read_csv('MASTER_MERGED.csv')
covid = pd.read_csv('COVID_Cleaned_Transposed.csv')

joined = gpd.sjoin(neighs, zipcodes, how='inner',op='intersects')


joined.to_csv('spatialJoin.csv')

joined = joined[['LABEL','zipcode1']]
joined = joined.rename(columns={'LABEL':'Neigh','zipcode1':'Zip Code'})
mhinc = mhinc[['Neigh','CSA','MHINC']]

merged = pd.merge_ordered(mhinc, joined, fill_method='none')
merged['Zip Code'] = merged['Zip Code'].astype(int)
merged = merged.sort_values(by=['Zip Code'])


meanlist = []
zipsList = [21227,21207,21230,21251,21229,21237,21287,21231,21226,21206,21222,21225,21211,21208,\
            21205,21218,21234,21202,21201,21213,21210,21209,21216,21236,21217,21224,21215,21212,\
                21223,21214,21239,21228]

zipsList.sort()

for zipcode in zipsList: 
    df1 = merged[merged['Zip Code'] == zipcode]
    mean = df1['MHINC'].mean()
    meanlist.append(mean)

latestCases = pd.DataFrame()

covid = covid.sort_values(by=['Zip Code'])
latestCases['Zip Code'] = covid['Zip Code'].astype(int)
latestCases['MHINC'] = meanlist
latestCases['TotalCases'] = covid.iloc[:,-1].astype(int)

_ = plt.figure(figsize=(12,6.75))
_ = plt.style.use('ggplot')
_ = sns.scatterplot(x='MHINC',y='TotalCases',data=latestCases,legend=False)
_ = plt.xlabel('Median Household Income')
_ = plt.ylabel('Total Reported COVID-19 Cases')
_ = plt.title('Baltimore City Reported COVID-19 Cases vs. Median Household Income')
plt.show()

corr = np.corrcoef(latestCases['MHINC'],latestCases['TotalCases'])
print(corr)