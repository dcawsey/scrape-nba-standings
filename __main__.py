import requests
from bs4 import BeautifulSoup
import json

season_end_year = 2025
response = requests.get(f"https://www.basketball-reference.com/leagues/NBA_{season_end_year}_standings.html")

if response.status_code != 200:
    print("Unable to fetch web page...")
    exit

soup = BeautifulSoup(response.text, 'html.parser')
standings = {}
conference_ids = ['E', 'W']

for conference in conference_ids:
    table = soup.find(id=f"confs_standings_{conference}")

    table_rows = table.tbody.find_all('tr')
    for team_row in table_rows:
        team_name_element = team_row.find(attrs={'data-stat': 'team_name'})
        wins_element = team_row.find(attrs={'data-stat': 'wins'})
        losses_element = team_row.find(attrs={'data-stat': 'losses'})
        wins = int(wins_element.string)
        losses = int(losses_element.string)
        standings[team_name_element.a.string] = { 'wins': wins, 'losses': losses }
    
json_str = json.dumps(standings, indent=4)
with open(f"standings_{season_end_year-1}-{season_end_year}.json", "w") as f:
    f.write(json_str)