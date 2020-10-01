#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 3 10:21:50 2020

@author: dariush
"""
import pandas as pd
import json
import requests
import re
import time
from datetime import datetime
import os

path = '[insertpath]'

# the-odd-api API key - free acct allows up to 500 calls per month
api_key = '[insertkey]'


# get NFL game odds
sport_key = 'americanfootball_nfl'

odds_response = requests.get('https://api.the-odds-api.com/v3/odds', params={
    'api_key' : api_key,
    'sport' : sport_key,
    'region' : 'us',
    'mkt' : 'spreads' # h2h spreads totals
    })

odds_json = json.loads(odds_response.text)
if not odds_json['success']:
    print('there was a problem with the request:', odds_json['msg'])
    
else:
    print()
    print(
        'Successfully got {} odds'.format(len(odds_json['data'])),
        'view the first one')
    print(odds_json['data'][0])
    
# check usage
print('Remaining requests', odds_response.headers['x-requests-remaining'])
print('used requests', odds_response.headers['x-requests-used'])

# create flatten function
def flatten_json(y):
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[name[:-1]] = x

    flatten(y)
    return out

# flatten file
odds_json_flat = flatten_json(odds_json)


# create dataframe
current_odds = pd.DataFrame()
special_cols = []

columns_list = list(odds_json_flat.keys())
for item in columns_list:
    try:
        row_idx = re.findall(r'\_(\d+)\_', item )[0]
    except:
        special_cols.append(item)
        continue
    column = re.findall(r'\_\d+\_(.*)', item )[0]
    

    row_idx = int(row_idx)
    value = odds_json_flat[item]

    current_odds.loc[row_idx, column] = value

for item in special_cols:
    current_odds[item] = odds_json_flat[item]
    
# select cols using wildcards
current_odds = current_odds.filter(regex='team|time|site_nice|update|odds_spreads_points|count')

# rename columns
new_cols = ['date',
            'site1','site1updated','site1_pointspread_0','site1_pointspread_1',
            'site2','site2updated','site2_pointspread_0','site2_pointspread_1',
            'site3','site3updated','site3_pointspread_0','site3_pointspread_1',
            'site4','site4updated','site4_pointspread_0','site4_pointspread_1',
            'site5','site5updated','site5_pointspread_0','site5_pointspread_1',
            'site6','site6updated','site6_pointspread_0','site6_pointspread_1',
            'site7','site7updated','site7_pointspread_0','site7_pointspread_1',
            'site8','site8updated','site8_pointspread_0','site8_pointspread_1',
            'site9','site9updated','site9_pointspread_0','site9_pointspread_1']

current_odds.rename(columns=dict(zip(current_odds.columns[[2,4,5,6,7,8,9,10,
                                                           11,12,13,14,15,16,
                                                           17,18,19,20,21,22,
                                                           23,24,25,26,27,28,
                                                           29,30,31,32,33,34,
                                                           35,36,37,38,39]], 
                                     new_cols)),inplace=True)

# save copy for possible audit
current_odds.to_csv(path + 'audit/odds/oddsdownload' + str(datetime.now().strftime('%Y_%m_%d_%H_%M_%S'))+'.csv', index=False)

# select needed columns
current_odds = current_odds.iloc[:, : 28]

# select the most common point spread from sources in new cols
current_odds['pointspread_0'] = current_odds.filter(regex='pointspread_0').mode(axis=1).iloc[:,0]
current_odds['pointspread_1'] = current_odds.filter(regex='pointspread_1').mode(axis=1).iloc[:,0]


# drop pointspread source cols
current_odds.drop(['site1','site1updated','site1_pointspread_0','site1_pointspread_1',
        'site2','site2updated','site2_pointspread_0','site2_pointspread_1',
        'site3','site3updated','site3_pointspread_0','site3_pointspread_1',
        'site4','site4updated','site4_pointspread_0','site4_pointspread_1',
        'site5','site5updated','site5_pointspread_0','site5_pointspread_1',
        'site6','site6updated','site6_pointspread_0','site6_pointspread_1'], 
        axis=1, inplace=True)



#convert commence_time from epoch and insert in 2 new columns day hour
current_odds['date'] = pd.to_datetime(current_odds['date'], unit='s', utc=True).dt.tz_convert(tz="US/Eastern")
current_odds['day'] = pd.to_datetime(current_odds['date'], dayfirst=True).dt.strftime('%A %B %d')
current_odds['hour'] = pd.to_datetime(current_odds['date'], dayfirst=True).dt.strftime('%I:%M %p')
current_odds['date'] = pd.to_datetime(current_odds['date'].dt.strftime('%Y-%m-%d'))

# save copy for possible audit
current_odds.to_csv('oddsdownload.csv', index=False)

# select needed columns
current_odds = current_odds.iloc[:, : 40]

# select the most common point spread from sources in new cols
current_odds['pointspread_0'] = current_odds.filter(regex='pointspread_0').mode(axis=1).iloc[:,0]
current_odds['pointspread_1'] = current_odds.filter(regex='pointspread_1').mode(axis=1).iloc[:,0]


# drop pointspread source cols
current_odds.drop(['site1','site1updated','site1_pointspread_0','site1_pointspread_1',
        'site2','site2updated','site2_pointspread_0','site2_pointspread_1',
        'site3','site3updated','site3_pointspread_0','site3_pointspread_1',
        'site4','site4updated','site4_pointspread_0','site4_pointspread_1',
        'site5','site5updated','site5_pointspread_0','site5_pointspread_1',
        'site6','site6updated','site6_pointspread_0','site6_pointspread_1'], 
        axis=1, inplace=True)

#convert commence_time from epoch and insert in 2 new columns day hour
current_odds['date'] = pd.to_datetime(current_odds['date'], unit='s', utc=True).dt.tz_convert(tz="US/Eastern")
current_odds['day'] = pd.to_datetime(current_odds['date'], dayfirst=True).dt.strftime('%A %B %d')
current_odds['hour'] = pd.to_datetime(current_odds['date'], dayfirst=True).dt.strftime('%I:%M %p')
current_odds['date'] = pd.to_datetime(current_odds['date'].dt.strftime('%Y-%m-%d'))

# request the NFL week number for input
week_entry = input('enter NFL week number - format must be a number: ')
current_odds['Week']= week_entry

# request date range for that week
date_entry_start = input('enter start of NFL week - format must be YYYY-MM-DD: ')
start_date = pd.Timestamp(date_entry_start)

date_entry_end = input('enter end of NFL week - format must be YYYY-MM-DD: ')
end_date = pd.Timestamp(date_entry_end)

# mask for the week
thisweek = (current_odds['date'] >= start_date) & (current_odds['date'] <= end_date)
# apply mask to filter the date range
current_odds = current_odds.loc[thisweek]


# export to csv for viewing
current_odds.to_csv('current_odds.csv', index=False)

