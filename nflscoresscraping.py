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

#create teamID column
scores['teamID'] = scores['team']
scores.loc[scores['team'].str.contains('kan', case=False), 'teamID'] = 'KC'
scores.loc[scores['team'].str.contains('rav', case=False), 'teamID'] = 'BAL'
scores.loc[scores['team'].str.contains('tam', case=False), 'teamID'] = 'TB'
scores.loc[scores['team'].str.contains('ten', case=False), 'teamID'] = 'TEN'
scores.loc[scores['team'].str.contains('ari', case=False), 'teamID'] = 'ARI'
scores.loc[scores['team'].str.contains('pit', case=False), 'teamID'] = 'PIT'
scores.loc[scores['team'].str.contains('cle', case=False), 'teamID'] = 'CLE'
scores.loc[scores['team'].str.contains('chic', case=False), 'teamID'] = 'CHI'
scores.loc[scores['team'].str.contains('san', case=False), 'teamID'] = 'SF'
scores.loc[scores['team'].str.contains('orl', case=False), 'teamID'] = 'NO'
scores.loc[scores['team'].str.contains('buf', case=False), 'teamID'] = 'BUF'
scores.loc[scores['team'].str.contains('gre', case=False), 'teamID'] = 'GB'
scores.loc[scores['team'].str.contains('dal', case=False), 'teamID'] = 'DAL'
scores.loc[scores['team'].str.contains('sea', case=False), 'teamID'] = 'SEA'
scores.loc[scores['team'].str.contains('ind', case=False), 'teamID'] = 'IND'
scores.loc[scores['team'].str.contains('phil', case=False), 'teamID'] = 'PHI'
scores.loc[scores['team'].str.contains('ram', case=False), 'teamID'] = 'LAR'
scores.loc[scores['team'].str.contains('min', case=False), 'teamID'] = 'MIN'
scores.loc[scores['team'].str.contains('eng', case=False), 'teamID'] = 'NE'
scores.loc[scores['team'].str.contains('atl', case=False), 'teamID'] = 'ATL'
scores.loc[scores['team'].str.contains('det', case=False), 'teamID'] = 'DET'
scores.loc[scores['team'].str.contains('mia', case=False), 'teamID'] = 'MIA'
scores.loc[scores['team'].str.contains('veg', case=False), 'teamID'] = 'LV'
scores.loc[scores['team'].str.contains('jet', case=False), 'teamID'] = 'NYJ'
scores.loc[scores['team'].str.contains('gian', case=False), 'teamID'] = 'NYG'
scores.loc[scores['team'].str.contains('cin', case=False), 'teamID'] = 'CIN'
scores.loc[scores['team'].str.contains('den', case=False), 'teamID'] = 'DEN'
scores.loc[scores['team'].str.contains('was', case=False), 'teamID'] = 'WAS'
scores.loc[scores['team'].str.contains('jac', case=False), 'teamID'] = 'JAX'
scores.loc[scores['team'].str.contains('caro', case=False), 'teamID'] = 'CAR'
scores.loc[scores['team'].str.contains('hou', case=False), 'teamID'] = 'HOU'
scores.loc[scores['team'].str.contains('char', case=False), 'teamID'] = 'LAC'


#reorder columns
scores = scores[['week', 'teamID', 'team', 'score', 'status']]


# save dataframe for future audit
scores.to_csv('scoresdownload'+ str(datetime.now().strftime('%Y_%m_%d_%H_%M_%S'))+'.csv', index=False)

# add scores to season data

scores = scores[scores['teamID'].isin(['KC','BAL', 'TB','TEN','ARI','PIT','CLE','CHI','SF','NO','BUF','GB','DAL','SEA','IND','PHI',
'LAR','MIN','NE','ATL','DET','MIA','LV','NYJ','NYG','CIN','DEN','WAS','JAX','CAR','HOU','LAC'])]

to_map = scores[scores.week==week_entry].set_index('teamID')['score']

to_update = games.week==week_entry

games.loc[to_update, 'score_0'] = games.loc[to_update,'team_0ID'].map(to_map)
games.loc[to_update, 'score_1'] = games.loc[to_update,'team_1ID'].map(to_map)
