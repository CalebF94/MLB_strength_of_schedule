#Author: Caleb Fornshell
#Date Created: 5/3/2025
#Purpose: script to contain a function that gathers season results from baseball-reference

import requests
import re # regular expressions
import pandas as pd
from bs4 import BeautifulSoup

def get_season_results(season):

    url = "https://www.baseball-reference.com/leagues/majors/" + str(season) + "-standings.shtml"
    response = requests.get(url)
    html = response.text

    #Removing html comment that messes with BeutifulSoup
    html = re.sub(r'<!--.*-->', '', html)

    soup = BeautifulSoup(html, features='html.parser')
    season_results = soup.find_all('tbody')


    df = pd.DataFrame(columns=['Season', 'Team', 'Wins', 'Losses', 'Win%', 'GB'])

    for tbl in season_results:
        for row in tbl.find_all('tr'):
            stat_row = [season]
            for stat in row.children:
                stat_row.append(stat.text)
            df.loc[len(df)] = stat_row

    df.rename(columns={'Team': 'Team Name'}, inplace=True)

    return(df)


#print(get_season_results(2022))

