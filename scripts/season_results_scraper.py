import requests
import re
import pandas as pd
from bs4 import BeautifulSoup

url = "https://www.baseball-reference.com/leagues/majors/2024-standings.shtml"

response = requests.get(url)
html = response.text

html = re.sub(r'<!--.*-->', '', html)


soup = BeautifulSoup(html, features='html.parser')
season_results = soup.find_all('tbody')


df = pd.DataFrame(columns=['Season', 'Team', 'Wins', 'Losses', 'Win%', 'GB'])

for tbl in season_results:
    for row in tbl.find_all('tr'):
        stat_row = [2024]
        for stat in row.children:
            stat_row.append(stat.text)
        df.loc[len(df)] = stat_row
        
print(df)
