
#BY:GERARD AGADA

import sqlite3
from turtle import color
import pandas as pd
import requests as r
import os
import json
import pprint as pp
import matplotlib.pyplot as plt 
from sqlalchemy import create_engine

#Import keys from OS environment.
foursquare_api = os.environ["FOURSQUARE_API_KEY"]
yelp_api = os.environ["YELP_KEY"]


#Create database for SQLite
engine = create_engine('sqlite:///mini_project_2.db', echo=True)
sqlite_connection = engine.connect()

#Authenticate Foursquare API
four_square_url = "https://api.foursquare.com/v3/places/search?ll=45.4206%2C-75.7007&radius=5000&categories=10000%2C%2013000%2C%2016000&fields=fsq_id%2Cname%2Cgeocodes%2Clocation%2Ccategories%2Ctimezone%2Cdistance%2Cpopularity%2Crating&sort=RATING&limit=20"
headers = {
    "Accept":"application/json",
    "Authorization": foursquare_api,
}
#Perform GET request for Foursquare
response_four = r.request("GET", four_square_url, headers=headers)
response_four_json = json.loads(response_four.text)
#Convert to DataFrame for FourSquare
foursquare_df = pd.json_normalize(response_four_json['results'])
foursquare_df['categories']= foursquare_df['categories'].astype('str')
foursquare_df['location.neighborhood']= foursquare_df['location.neighborhood'].astype('str') 
foursquare_df.to_csv('foursquare_data.csv')
foursquare_df.plot(kind='bar',x='name',y='distance')
plt.show()

print('*******************SEPERATOR**********************/n')



#Authenticate Yelp API
yelp_url = "https://api.yelp.com/v3/businesses/search?latitude=45.4206&longitude=-75.7007&radius=5000&categories=bars,restaurants,Landmarks %26 Historical Buildings,Diners,Arts %26 Entertainment"
headers = {
    #"Accept":"application/json",
    "Authorization": 'Bearer ' + yelp_api,
}
#Perform GET request for YELP
response_yelp = r.request("GET", yelp_url, headers=headers)
response_yelp_json = json.loads(response_yelp.text)
#Convert to DataFrame for YELP
yelp_df = pd.json_normalize(response_yelp_json['businesses'])
yelp_df['categories']= yelp_df['categories'].astype('str')
yelp_df.drop(columns=['transactions'], axis=1, inplace=True)
yelp_df['location.display_address']= yelp_df['location.display_address'].astype('str') 
yelp_df.to_csv('yelp_data.csv')
yelp_df.plot(kind='bar',x='name',y='review_count', color='#483D8B')
plt.show()


#Create Foursquare Table
foursquare_sqlite = "foursquare_table"
foursquare_df.to_sql(foursquare_sqlite, sqlite_connection, if_exists='fail')

#Create Yelp Table
yelp_sqlite = "yelp_table"
yelp_df.to_sql(yelp_sqlite, sqlite_connection, if_exists='fail')
sqlite_connection.close()