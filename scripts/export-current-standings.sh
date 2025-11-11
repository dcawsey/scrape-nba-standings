#!/bin/sh

echo
echo "**** START: `date`"

echo "Change directory to scrape project..."
cd /home/dcawsey/dev/repo/scrape-nba-standings
pwd
. ./.env
echo "Loaded env variables status: $?"

echo "Scraping NBA standings..."
. .venv/bin/activate
python .
echo "Scraping status: $?"
deactivate

SEASON_START_YEAR=$((SEASON_END_YEAR - 1))

SEASON_PERIOD="$SEASON_START_YEAR-$SEASON_END_YEAR"
echo $SEASON_PERIOD
FILENAME='standings'

echo "Exporting current standings to nba-skins-draft-results repo..."
cp -f ".data/${FILENAME}_${SEASON_PERIOD}.json" "../nba-skins-draft-results/src/data/$SEASON_PERIOD/$FILENAME.json"
echo "Copy status: $?"
