#Author: Caleb Fornshell
#Date Created: 5/4/2025
#Purpose: Scrape season schedules for MLB Teams

import requests
import re # regular expressions
import pandas as pd
from bs4 import BeautifulSoup

def team_names(season):
    url = "https://www.baseball-reference.com/leagues/majors/" + str(season) + "-schedule.shtml"
    team_dict = {}

    response = requests.get(url)

    soup = BeautifulSoup(response.content, features="html.parser")
    team_list = soup.find('form', id = "team_schedule")

    for team in team_list.find_all('option'):
        if(team['value'] != ""):
            team_dict[team.text] = team['value'][7:10]

    return(team_dict)

#teams = team_names(2024)


url = "https://www.baseball-reference.com/teams/ARI/2024-schedule-scores.shtml"

response = requests.get(url)
soup = BeautifulSoup(response.content, features = "html.parser")
schedule = soup.find('table', id = 'team_schedule').find('tbody').find_all('tr')


for rows in schedule:
    print(rows.children) ## struggling to go through hierarchy
