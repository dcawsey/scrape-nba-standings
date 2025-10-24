# Get all env variables from .env file
set -a; source .env; set +a

source .venv/bin/activate
python .
deactivate

SEASON_START_YEAR=$((SEASON_END_YEAR - 1))

SEASON_PERIOD="$SEASON_START_YEAR-$SEASON_END_YEAR"
FILENAME='standings'
cp -nf ".data/${FILENAME}_${SEASON_PERIOD}.json" "../nba-skins-draft-results/src/data/$SEASON_PERIOD/$FILENAME.json"