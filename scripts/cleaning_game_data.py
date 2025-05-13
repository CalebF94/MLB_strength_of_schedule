#Author: Caleb Fornshell
#Date Created: 5/11/2025
#Purpose: script cleans the raw/scraped data for the game by game data. Clean data is then saved to be used in later analysis

import pandas as pd
import numpy as np


def game_time_to_minutes(game_time):

    if type(game_time) is str: game_time = str(game_time)

    minutes = (float(game_time.split(':')[0]) *60) + float(game_time.split(':')[1])
    return(minutes)


df_game_data = pd.read_csv("./raw_data/raw_game_results.csv")#.drop(['Unnamed: 0'], axis=1)
#df_season_results = pd.read_csv("./raw_data/season_results.csv").drop(['Unnamed: 0'], axis=1)

#removing records that were not completed at time of data scraping
df_game_data = df_game_data[df_game_data['win_loss_result'].notna()]

#some games don't have attendance listed. Will impute using average of non missing
avg_attendance = round(df_game_data.loc[:, 'Attendance'].str.replace(",", "").dropna().astype('int').mean(),0) 

#converting attendance into number and setting nulls to the average
#need regex=True for partial string matches
df_game_data = df_game_data.fillna({'Attendance': str(avg_attendance)}).replace({'Attendance': ',', 'win_loss_result': '-wo'}, '', regex=True)

#2020 had legit zero attendance...setting back to zero
df_game_data.loc[df_game_data['Date']<'2021-01-01', 'Attendance'] = 0

# converting H:MM game lengths to minutes
df_game_data['Length Minutes'] = df_game_data['Game Time'].apply(game_time_to_minutes)

data_types = {
    'Date': 'datetime64[ns]',
    'Team': 'string',
    'H/A': 'string',
    'Opponent':'string',
    'win_loss_result':'string',
    'Runs': 'int',
    'Runs Allowed': 'int',
    'Game Time':'string',
    'Day/Night': 'string',
    'Attendance':'float',
    'Game Number': 'int',
    'Year':'int',
    'Length Minutes': int
}
df_game_data = df_game_data.astype(data_types)

#renaming columns
col_names = {
    'Date': 'date',
    'Team': 'team',
    'H/A': 'H/A',
    'Opponent':'opponent',
    'win_loss_result':'win_loss',
    'Runs': 'runs_scored',
    'Runs Allowed': 'runs_allowed',
    'Game Time':'game_time',
    'Day/Night': 'day_night',
    'Attendance':'attendance',
    'Game Number': 'game_number',
    'Year':'season',
    'Length Minutes': 'game_length'
}
df_game_data.rename(columns=col_names, inplace=True)

df_game_data.to_csv('./clean_data/game_results.csv', index=False)
