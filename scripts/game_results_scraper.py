#Author: Caleb Fornshell
#Date Created: 5/3/2025
#Purpose: script to create a function that gathers game by game results for a specified team and season
#   Functions will be used in driver_data_collection.py

import re # regular expressions
from datetime import datetime
import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup


def get_game_results(team, season):
    """
    Scrapes game level data for a specific team and season

    Keyword arguments:
    team -- team three character abbreviation
    season -- season game results to gather
    """
    url = "https://www.baseball-reference.com/teams/" + str(team) + "/" + str(season) + "-schedule-scores.shtml"

    response = requests.get(url)
    soup = BeautifulSoup(response.content, features = "html.parser")
    schedule = soup.find('table', id = 'team_schedule').find('tbody').find_all('tr')


    stat_names = [stat["data-stat"] for stat in schedule[0].find_all('td')]
    df = pd.DataFrame(columns = stat_names)

    for row in schedule:
        stat_list = [stat.text for stat in row.find_all('td')]
        
        if stat_list:
            if(len(stat_list) != 21):
                    stat_list+[" "]*(21 - len(stat_list))
                    stat_list[5:20] = [""]*16
                
            df.loc[len(df)] = stat_list
        
    df['game_number'] = np.arange(1, len(df)+1)
    df['Year'] = np.repeat(season, len(df))

    #Basic data cleaning and column selection
    df.drop(columns={'boxscore', 'rank', 'games_back', 'winning_pitcher', 'losing_pitcher', 'saving_pitcher', 'cli', 'win_loss_streak', 'reschedule', 'win_loss_record', 'extra_innings'}, inplace=True)
    df.rename(columns = {"date_game": "Date", 'team_ID': 'Team', 'homeORvis': 'H/A', 'opp_ID': 'Opponent', 'R': 'Runs', 'RA': 'Runs Allowed', 'time_of_game': 'Game Time', 'day_or_night': 'Day/Night', 'attendance': 'Attendance', 'game_number': 'Game Number'}, inplace=True)
    df['H/A'] = np.where(df['H/A'] == '@', 'A', 'H')
    df['Date'] = pd.to_datetime(df['Date'].str.replace("\([1-2]\)", "", regex=True) + " " + str(season), format = "%A, %b %d %Y")

    return(df)

#print(get_game_results('ARI', 2024))
