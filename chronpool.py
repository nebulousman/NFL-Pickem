#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 3 10:21:50 2020

@author: dariush
"""

import json
import requests

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