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
    
#convert start date time DOES NOT WORK
current_odds['commence_time'] = pd.to_datetime(current_odds['commence_time'], unit='s')

# export to csv for viewing
current_odds.to_csv('current_odds.csv', index=False)

