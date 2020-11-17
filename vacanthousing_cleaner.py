# -*- coding: utf-8 -*-
"""
Created on Fri Sep 25 15:08:47 2020

@author: Arun
"""

import pandas as pd

df = pd.read_csv('Vacant_Buildings.csv')

latlong= df['Location'].astype(str)

latlong = latlong.map(lambda x: x.lstrip('(').rstrip(')'))

latlong = latlong.str.split(expand=True)

latlong.iloc[:,0] = latlong.iloc[:,0].map(lambda x: x.rstrip(','))

latlong.iloc[:,:] = latlong.iloc[:,:].astype(float)

latlong.columns = ['latitude','longitude']
print(latlong.head())