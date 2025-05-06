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


#for yr in range(2020, 2025)
teams = get_team_names(2024)
#season_results = get_season_results(2024)
#season_results['Team'] = season_results['Team Name'].map(teams)

ind = 0
for team in teams.values():
    time.sleep(5) # needed to avoid 429 error

    ind += 1
    if ind == 1:
        #initialize on first iteration
        game_results = get_game_results(team, 2024)
    else:
        game_results = pd.concat(objs=[game_results, get_game_results(team, 2024)], axis = 0)


print(game_results)
