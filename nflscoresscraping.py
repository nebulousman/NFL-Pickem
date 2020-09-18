#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 1 14:02:05 2020

@author: dariush
"""

# imports
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from datetime import datetime

# get week NFL results

# target URL pro-football-reference
url = "https://www.pro-football-reference.com/boxscores/"

data = pd.read_html(url)
scores = pd.DataFrame(np.concatenate(data))

# remove stat rows
statrows = ['PassYds','RushYds','RecYds']
scores = scores[~scores[0].isin(statrows)]


#rename columns
scores = scores.rename(columns={scores.columns[0]:"team"})
scores = scores.rename(columns={scores.columns[1]:"score"})
scores = scores.rename(columns={scores.columns[2]:"status"})

# request the NFL week number and add column with value
week_entry = input('enter NFL week number - format must be a number: ')
scores['week']= week_entry

# save dataframe for future audit
scores.to_csv('scoresdownload.csv'+ str(datetime.now().strftime('%Y_%m_%d_%H_%M_%S')), index=False)


# introduce ID 
for i in scores['team']:
#add IDs


# add scores to season data
to_map = scores[scores.week==week_entry].set_index('teamID')['score']

to_update = games.week==week_entry

games.loc[to_update, 'score_0'] = games.loc[to_update,'team_0'].map(to_map)
games.loc[to_update, 'score_1'] = games.loc[to_update,'team_1'].map(to_map)
