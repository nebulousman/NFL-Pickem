#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 13 17:36:58 2020

@author: dariush
"""

import pandas as pd
import numpy as np
import spacy
from spacy.matcher import PhraseMatcher
sp = spacy.load('en_core_web_sm')
matcher = PhraseMatcher(sp.vocab, attr='LOWER')

picks = open("picks.txt", "r") #use picks.read()
all_teams = ['Punish The Monkey', 'flea flicker', 'ermatiger']

email = sp(picks.read())
team_name=[sp(term) for term in all_teams]

matcher.add('team_name_matcher', None, *team_name)

team_matches = matcher(email)

for match_id,start,end in team_matches:
    span=email[start:end]
    team=span.text

picks = pd.DataFrame([token for token in email if not token.is_stop and not token.is_punct])

picks['team']= team
picks = picks.rename(columns={picks.columns[0]:'selection',picks.columns[1]:'team'})
picks['selection']=picks['selection'].astype(str)
picks['selection']=picks['selection'].str.lower()

#picks['selectID']=picks['selection'].astype(str)
#df["fruit"] = df["fruit"].astype(str)
#.str.lower()
#picks['selectID']=picks['selectID'].str.lower()

#create selectID column
picks['selectID']=np.nan

#populate selectID column
#picks['selectID'].str.contains('dal', case=False), ('DAL')
#picks.loc[picks['selection'].astype(str).str.contains('dal', case=False), 'selectID'] = 'DAL'


picks.loc[picks['selection'].str.contains('kan', case=False), 'selectID'] = 'KC'
picks.loc[picks['selection'].str.contains('rav', case=False), 'selectID'] = 'BAL'
picks.loc[picks['selection'].str.contains('tam', case=False), 'selectID'] = 'TB'
picks.loc[picks['selection'].str.contains('ten', case=False), 'selectID'] = 'TEN'
picks.loc[picks['selection'].str.contains('ari', case=False), 'selectID'] = 'ARI'
picks.loc[picks['selection'].str.contains('pit', case=False), 'selectID'] = 'PIT'
picks.loc[picks['selection'].str.contains('cle', case=False), 'selectID'] = 'CLE'
picks.loc[picks['selection'].str.contains('chic', case=False), 'selectID'] = 'CHI'
picks.loc[picks['selection'].str.contains('san', case=False), 'selectID'] = 'SF'
picks.loc[picks['selection'].str.contains('orl', case=False), 'selectID'] = 'NO'
picks.loc[picks['selection'].str.contains('buf', case=False), 'selectID'] = 'BUF'
picks.loc[picks['selection'].str.contains('gre', case=False), 'selectID'] = 'GB'
picks.loc[picks['selection'].str.contains('dal', case=False), 'selectID'] = 'DAL'
picks.loc[picks['selection'].str.contains('cowboy', case=False), 'selectID'] = 'DAL'
picks.loc[picks['selection'].str.contains('sea', case=False), 'selectID'] = 'SEA'
picks.loc[picks['selection'].str.contains('ind', case=False), 'selectID'] = 'IND'
picks.loc[picks['selection'].str.contains('phil', case=False), 'selectID'] = 'PHI'
picks.loc[picks['selection'].str.contains('ram', case=False), 'selectID'] = 'LAR'
picks.loc[picks['selection'].str.contains('min', case=False), 'selectID'] = 'MIN'
picks.loc[picks['selection'].str.contains('eng', case=False), 'selectID'] = 'NE'
picks.loc[picks['selection'].str.contains('atl', case=False), 'selectID'] = 'ATL'
picks.loc[picks['selection'].str.contains('det', case=False), 'selectID'] = 'DET'
picks.loc[picks['selection'].str.contains('mia', case=False), 'selectID'] = 'MIA'
picks.loc[picks['selection'].str.contains('veg', case=False), 'selectID'] = 'LV'
picks.loc[picks['selection'].str.contains('jet', case=False), 'selectID'] = 'NYJ'
picks.loc[picks['selection'].str.contains('gian', case=False), 'selectID'] = 'NYG'
picks.loc[picks['selection'].str.contains('cin', case=False), 'selectID'] = 'CIN'
picks.loc[picks['selection'].str.contains('den', case=False), 'selectID'] = 'DEN'
picks.loc[picks['selection'].str.contains('was', case=False), 'selectID'] = 'WAS'
picks.loc[picks['selection'].str.contains('jac', case=False), 'selectID'] = 'JAX'
picks.loc[picks['selection'].str.contains('caro', case=False), 'selectID'] = 'CAR'
picks.loc[picks['selection'].str.contains('hou', case=False), 'selectID'] = 'HOU'
picks.loc[picks['selection'].str.contains('char', case=False), 'selectID'] = 'LAC'

#remove nan rows
picks=picks[picks['selectID'].notna()]
picks=picks.drop_duplicates(subset='selectID',keep='first')

#add week column
picks['week']=

#append to main dataframe

