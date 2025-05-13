#Author: Caleb Fornshell
#Date Created: 5/11/2025
#Purpose: script cleans the raw/scraped data for the game by season summary data. Clean data is then saved to be used in later analysis

import pandas as pd
import numpy as np

df_season_results = pd.read_csv("./raw_data/raw_season_results.csv")#.drop(['Unnamed: 0'], axis=1)

#Handling blanks and inconsistencies with franchise changes
df_season_results.loc[:, 'GB'] = df_season_results.loc[: 'GB'].mask(df_season_results.loc[:, 'GB']=='--', '0')
df_season_results.loc[:, 'Team'] = df_season_results.loc[: 'Team'].mask(df_season_results.loc[:, 'Team Name'].str.contains('Athletics'), 'ATH')
df_season_results.loc[:, 'Team'] = df_season_results.loc[: 'Team'].mask(df_season_results.loc[:, 'Team Name'].str.contains('Cleveland'), 'CLE')

# converting data types
data_types = {
    'Season': int,
    'Team Name': str,
    'Wins': int,
    'Losses': int,
    'Win%': float,
    'GB': float,
    'Team': str
}
df_season_results.astype(data_types)

#converting column names
col_names = {
    'Season': 'season',
    'Team Name': 'team_name',
    'Wins': 'wins',
    'Losses': 'losses',
    'Win%': 'win_%',
    'GB': 'GB',
    'Team': 'teams'
}
df_season_results.rename(columns=col_names, inplace=True)

df_season_results.to_csv('./clean_data/season_results.csv', index=False)
