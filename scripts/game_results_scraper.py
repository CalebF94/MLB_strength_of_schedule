import requests
import re # regular expressions
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup

def get_game_results(team, season):
    url = "https://www.baseball-reference.com/teams/" + str(team) + "/" + str(season) + "-schedule-scores.shtml"

    response = requests.get(url)
    soup = BeautifulSoup(response.content, features = "html.parser")
    schedule = soup.find('table', id = 'team_schedule').find('tbody').find_all('tr')


    stat_names = [stat["data-stat"] for stat in schedule[0].find_all('td')]
    df = pd.DataFrame(columns = stat_names)

    for row in schedule:
        stat_list = [stat.text for stat in row.find_all('td')]
        
        if stat_list:
            df.loc[len(df)] = stat_list
        
    df['game_number'] = np.arange(1, len(df)+1)
    return(df)

print(get_game_results('ARI', 2024))
