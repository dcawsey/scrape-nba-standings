#!/bin/sh

echo
echo "**** START: `date`"

echo "Loading environment variables from .env file..."
set -a; source .env; set +a
echo "Environment variables load status: $?"

echo "Activating virtual environment and scraping NBA standings..."
source .venv/bin/activate
python .
echo "Scraping status: $?"
deactivate

SEASON_START_YEAR=$((SEASON_END_YEAR - 1))

SEASON_PERIOD="$SEASON_START_YEAR-$SEASON_END_YEAR"
FILENAME='standings'

echo "Exporting current standings to nba-skins-draft-results repo..."
cp -nf ".data/${FILENAME}_${SEASON_PERIOD}.json" "../nba-skins-draft-results/src/data/$SEASON_PERIOD/$FILENAME.json"
echo "Copy status: $?"