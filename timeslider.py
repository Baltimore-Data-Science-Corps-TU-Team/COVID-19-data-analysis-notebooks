# -*- coding: utf-8 -*-
"""
Created on Fri Sep 25 19:59:49 2020

@author: Arun
"""

import pandas as pd
import folium
import branca.colormap as cm
import geopandas as gpd
import numpy as np
from folium.plugins import TimeSliderChoropleth
import json

df = pd.read_csv('MDCOVID19_MASTER_ZIP_CODE_CASES.csv')

zipsList = [21227,21207,21230,21251,21229,21237,21287,21231,21226,21206,21222,21225,21211,21208,\
            21205,21218,21234,21202,21201,21213,21210,21209,21216,21236,21217,21224,21215,21212,\
                21223,21214,21239,21228]

df = df[df['ZIP_CODE'].isin(zipsList)]

df = df.fillna(0)

df = df.drop('OBJECTID', axis=1)

#print(df.columns)
#print(df)
df = df.transpose()
df.columns = df.iloc[0]
df = df.drop('ZIP_CODE')
df = df.reset_index()
df = df.rename(columns={'index':'Date'})
#df = df.reset_index()

#print(df.columns)

df['Date'] = df['Date'].map(lambda x: x.lstrip('F').lstrip('t').lstrip('o').lstrip('t')\
                            .lstrip('a').lstrip('l'))

dates = pd.DataFrame()
dates = df['Date'].str.split(pat='_', expand=True)
dates[0] = dates[0].map(lambda x: x.lstrip('0'))
dates['fdate'] = dates[2].str.cat(dates[0], sep='-').str.cat(dates[1],sep='-')

dates = dates['fdate']

df = df.drop('Date',axis=1)


df.insert(0,'Date',dates)
#print(df)
df['Date'] = pd.to_datetime(df['Date'])

print(df)

zipcodes = gpd.read_file('geo_export_4d013e8a-7202-4f2a-924a-c706270be6cb.shp')
#print(zipcodes.head())
#print(zipcodes['zipcode1'])
df1 = df.transpose()
df1.columns = df1.iloc[0]
df1 = df1.drop('Date')
df1 = df1.reset_index()
df1 = df1.rename(columns={'ZIP_CODE':'zipcode1'})
df1['zipcode1'] = df1['zipcode1'].astype(int).astype(str)

df1 = pd.melt(df1,id_vars='zipcode1',value_name='cases')
print(df1)
df1 = df1[['zipcode1','Date','cases']]
joined = df1.merge(zipcodes,on='zipcode1')

joined = joined[['zipcode1','Date','cases','geometry']]
joined['Date'] = pd.to_datetime(joined['Date']).values.astype(int)
joined['Date'] = joined['Date'].values.astype(str)
print(joined.head())
baltMap = folium.Map(location=[39.2904,-76.6122], tiles='OpenStreetMap', zoom_start=13)

max_color = max(joined['cases'])
min_color = min(joined['cases'])
cmap = cm.linear.OrRd_09.scale(min_color,max_color)
joined['color'] = joined['cases'].map(cmap)
joined = joined.sort_values(['zipcode1','Date'])

zips_list = joined['zipcode1'].unique().tolist()
zips_idx = range(len(zips_list))


style_dict = {}

for i in zips_idx:
    zipcode = zips_list[i]
    result = joined[joined['zipcode1'] == zipcode]
    inner_dict = {}
    for _, r in result.iterrows():
        inner_dict[r['Date']] = {'color': r['color'],'opacity':0.8}
    style_dict[str(i)] = inner_dict
    
zipcodes_df = joined[['geometry']]
zipcodes_gdf = gpd.GeoDataFrame(zipcodes_df)
zipcodes_gdf = zipcodes_gdf.drop_duplicates().reset_index()


slider_map = folium.Map(location=[39.2904,-76.6122], tiles='OpenStreetMap', zoom_start=13)

_= TimeSliderChoropleth(
    data=zipcodes_gdf.to_json(),
    styledict=style_dict,
    ).add_to(slider_map)

_= cmap.add_to(slider_map)

cmap.caption = 'Baltimore City Reported COVID-19 Cases'
slider_map.save('TimeSliderChoropleth.html')
print(joined[joined['cases'] == 2005])
print(joined.dtypes)