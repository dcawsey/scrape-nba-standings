import json
import os
import sys

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

print("Running python script...")
load_dotenv()
env_variable_name = "SEASON_END_YEAR"
season_end_year = os.getenv(env_variable_name)
if season_end_year == None:
    print("No value in .env file for ", env_variable_name)
    sys.exit(1)

season_end_year = int(season_end_year)
print("Loaded env vars, SEASON_END_YEAR:", season_end_year)

url = (
    f"https://www.basketball-reference.com/leagues/NBA_{season_end_year}_standings.html"
)
response = requests.get(url)
print("Fetch standings HTML response:", response.status_code)

if response.status_code != 200:
    print("Unable to fetch web page:", url)
    sys.exit(1)

parsed_html = BeautifulSoup(response.text, "html.parser")


def get_data_stat_element(attr_id: str):
    element = team_row.select_one(f"[data-stat='{attr_id}']")
    if element is None:
        raise ValueError(f"No HTML element found for data-stat attr: {attr_id}")
    return element


standings = {}
for conference_id in ["E", "W"]:
    try:
        table_id = f"confs_standings_{conference_id}"
        table = parsed_html.select_one(f"#{table_id}")
        if table is None:
            raise ValueError(f"No <table> tag found for id={table_id}")

        table_rows = table.select("tbody tr")
        if not table_rows:
            raise ValueError(f"No rows found in tbody for id={table_id}")

        for team_row in table_rows:
            wins_element = get_data_stat_element("wins")
            wins = int(wins_element.get_text(strip=True))

            losses_element = get_data_stat_element("losses")
            losses = int(losses_element.get_text(strip=True))

            team_name_element = get_data_stat_element("team_name")
            if not team_name_element.a:
                raise ValueError(
                    "Could not find anchor child element for team_name attribute Tag"
                )
            team_name_string = team_name_element.a.get_text(strip=True)

            standings[team_name_string] = {"wins": wins, "losses": losses}
    except ValueError as e:
        print("Table HTML contract broken for conference: ", conference_id)
        print(e)
        sys.exit(1)


json_str = json.dumps(standings, indent=4)
file_name = f".data/standings_{season_end_year - 1}-{season_end_year}.json"

with open(file_name, "w") as f:
    f.write(json_str)
