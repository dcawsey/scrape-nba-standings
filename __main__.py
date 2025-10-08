import json
import os

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

from s3 import upload_file

load_dotenv()
season_end_year = int(os.getenv("SEASON_END_YEAR"))

url = (
    f"https://www.basketball-reference.com/leagues/NBA_{season_end_year}_standings.html"
)
response = requests.get(url)

if response.status_code != 200:
    print("Unable to fetch web page:", url)
    exit

parsed_html = BeautifulSoup(response.text, "html.parser")

standings = {}
for conference_id in ["E", "W"]:
    table = parsed_html.find(id=f"confs_standings_{conference_id}")

    table_rows = table.tbody.find_all("tr")
    for team_row in table_rows:
        team_name_element = team_row.find(attrs={"data-stat": "team_name"})
        wins_element = team_row.find(attrs={"data-stat": "wins"})
        losses_element = team_row.find(attrs={"data-stat": "losses"})
        wins = int(wins_element.string)
        losses = int(losses_element.string)
        standings[team_name_element.a.string] = {"wins": wins, "losses": losses}

json_str = json.dumps(standings, indent=4)
file_name = f".data/standings_{season_end_year - 1}-{season_end_year}.json"

with open(file_name, "w") as f:
    f.write(json_str)

bucket_name = os.getenv("S3_BUCKET_NAME")
upload_file(file_name, bucket_name)
