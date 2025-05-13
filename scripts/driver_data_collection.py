#Author: Caleb Fornshell
#Date Created: 5/3/2025
#Purpose: driver script to  run and gather data
#   Will use the functions from game_results_scraper, season_results_scraper, team_name_scraper
#   Will save data to local drive

from team_name_scraper import *
from game_results_scraper import *
from season_results_scraper import *
import pandas as pd
import time


#indexes to identify first loop through
game_ind = 1
season_ind = 1
for yr in range(2015, 2026):
    print(f'Scraping Year: {yr}')
    
    teams = get_team_names(yr)

    # Gathering season results
    if season_ind == 1:
        season_ind += 1
        season_results = get_season_results(yr)
    else:
        season_results = pd.concat(objs = [season_results, get_season_results(yr)], axis=0)

    
    #Gathering game by game results
    for team in teams.values():
        time.sleep(2) # needed to avoid 429 error. No more than 30 requests per minute
        
        if game_ind == 1:
            game_ind += 1
            #initialize on first iteration
            game_results = get_game_results(team, yr)
        else:
            game_results = pd.concat(objs=[game_results, get_game_results(team, yr)], axis = 0)


season_results['Team'] = season_results['Team Name'].map(teams)
game_results.to_csv("./raw_data/raw_game_results.csv", index=False)
season_results.to_csv("./raw_data/raw_season_results.csv", index=False)
#print(season_results)

#clean data
exec(open("./scripts/cleaning_season_data.py").read())
exec(open("./scripts/cleaning_game_data.py").read())