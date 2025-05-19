#Author: Caleb Fornshell
#Date Created: 5/4/2025
#Purpose: Scrapes team abbreviations for the specified season

import requests
from bs4 import BeautifulSoup


def get_team_names(season):
    """
    Collects three character team abbreviations for the specified season

    Keyword Arguments:
    season - season to gather
    """
    url = "https://www.baseball-reference.com/leagues/majors/" + str(season) + "-schedule.shtml"
    team_dict = {}

    response = requests.get(url, verify=False)

    soup = BeautifulSoup(response.content, features="html.parser")
    team_list = soup.find('form', id = "team_schedule")

    for team in team_list.find_all('option'):
        if(team['value'] != ""):
            team_dict[team.text] = team['value'][7:10]

    return(team_dict)

#teams = get_team_names(2024)
#print(teams)