#NBA Player Game Log Scraper v1
#Copyright 2018 Rakesh Bhatia

#This scraper demonstrates the use of Python with BeautifulSoup,
#requests, and Pandas. NBA player game log data is scraped from
#www.basketball-reference.com and stored in a Pandas dataframe.

import numpy as np
import pandas as pd
import requests
import scipy
import seaborn as sns
from bs4 import BeautifulSoup
from collections import Counter
from scipy.stats import ttest_ind
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
%matplotlib inline

base_url = 'https://www.basketball-reference.com'

teams = {'BOS':'https://www.basketball-reference.com/teams/BOS/2019.html',
         'BKN':'https://www.basketball-reference.com/teams/BRK/2019.html',
         'NYK':'https://www.basketball-reference.com/teams/NYK/2019.html',
         'PHI':'https://www.basketball-reference.com/teams/PHI/2019.html',
         'TOR':'https://www.basketball-reference.com/teams/TOR/2019.html',

         'CHI':'https://www.basketball-reference.com/teams/CHI/2019.html',
         'CLE':'https://www.basketball-reference.com/teams/CLE/2019.html',
         'DET':'https://www.basketball-reference.com/teams/DET/2019.html',
         'IND':'https://www.basketball-reference.com/teams/IND/2019.html',
         'MIL':'https://www.basketball-reference.com/teams/MIL/2019.html',

         'ATL':'https://www.basketball-reference.com/teams/ATL/2019.html',
         'CHA':'https://www.basketball-reference.com/teams/CHO/2019.html',
         'MIA':'https://www.basketball-reference.com/teams/MIA/2019.html',
         'ORL':'https://www.basketball-reference.com/teams/ORL/2019.html',
         'WAS':'https://www.basketball-reference.com/teams/WAS/2019.html',

         'GSW':'https://www.basketball-reference.com/teams/GSW/2019.html',
         'LAC':'https://www.basketball-reference.com/teams/LAC/2019.html',
         'LAL':'https://www.basketball-reference.com/teams/LAL/2019.html',
         'PHO':'https://www.basketball-reference.com/teams/PHO/2019.html',
         'SAC':'https://www.basketball-reference.com/teams/SAC/2019.html',

         'DAL':'https://www.basketball-reference.com/teams/DAL/2019.html',
         'HOU':'https://www.basketball-reference.com/teams/HOU/2019.html',
         'MEM':'https://www.basketball-reference.com/teams/MEM/2019.html',
         'NOP':'https://www.basketball-reference.com/teams/NOP/2019.html',
         'SAS':'https://www.basketball-reference.com/teams/SAS/2019.html',

         'DEN':'https://www.basketball-reference.com/teams/DEN/2019.html',
         'MIN':'https://www.basketball-reference.com/teams/MIN/2019.html',
         'OKC':'https://www.basketball-reference.com/teams/OKC/2019.html',
         'POR':'https://www.basketball-reference.com/teams/POR/2019.html',
         'UTA':'https://www.basketball-reference.com/teams/UTA/2019.html'}

for team, url in teams.items():
    # only process one team for now (for test purposes)
    if team != 'BOS':
        continue

    res = requests.get(url, timeout=5)
    soup = BeautifulSoup(res.content,'lxml')
    table = soup.find_all('table')[0]
    player_links = []
    player_names = []

    for row in table.find('tbody').find_all('tr'):
        # find player's jersey number
        jersey_number = row.find('th', attrs={'data-stat':'number'})

        # if jersey number field is empty, player is inactive
        if jersey_number.get_text() == '':
            print('player inactive')
            continue

        # get the player names
        name = row.find('td', attrs={'data-stat':'player'})
        print('name: ', name.get_text())
        player_names.append(name.get_text())

        # get the link to each player page
        a = row.find_all('a')[0]
        player_links.append(base_url + a['href'].replace('.html', '/gamelog/2019'))

    #read roster table into pandas dataframe
    roster = pd.read_html(str(table))[0]
    print('read_html output\n')
    print(roster)

    count = 0
    for link in player_links:
        res = requests.get(link, timeout=5)
        soup = BeautifulSoup(res.content,'lxml')
        table = soup.find_all('table', attrs={'class':'row_summable sortable stats_table'})

        if table:
            # load stats table into dataframe
            df = pd.read_html(str(table))[0]

            # set the columns of dataframe
            df.columns = ['Rk', 'G', 'Date', 'Age', 'Tm', 'Location', 'Opp', 'Result', 'GS', 'MP', \
                          'FG', 'FGA', 'FG%', '3P', '3PA', '3P%', 'FT', 'FTA', 'FT%', 'ORB', 'DRB', \
                          'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS', 'GmSc', '+/-']

            # indicate which columns to treat as float
            columns_float = ['FG', 'FGA', 'FG%', '3P', '3PA', '3P%', 'FT', 'FTA', 'FT%', 'ORB', 'DRB', \
                             'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS', 'GmSc', '+/-']

            df[columns_float] = df[columns_float].astype(float)

            # add new column that calculates fanduel points earned for each game
            df['Fanduel Pts'] = 2*df['FG'] + df['FT'] + df['3P'] + 1.2*df['TRB'] + 1.5*df['AST'] + 3*df['STL'] + 3*df['BLK'] - df['TOV']

            df['Name'] = player_names[count]

            print(df)

            df.to_csv(player_names[count].split(' ')[0] + '-' + player_names[count].split(' ')[1] + '-game-log.csv')

            count += 1

        else:
            count += 1
            continue
