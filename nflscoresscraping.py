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

# get week NFL results

# target URL pro-football-reference
url = "https://www.pro-football-reference.com/boxscores/"

# headers
headers = {
    'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"
    }

# send request to download the data
page = requests.request("GET", url, headers=headers)

# parse the downloaded data
data = BeautifulSoup(page.text, 'html.parser')

# extract week's results
scores = data.find_all("div", {"class": "game_summaries"})

print(scores)

# need to parse scores and create dataframe with date, team names, scores, Final or not
