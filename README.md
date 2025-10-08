# Scrape NBA standings

## Local dev
Must have AWS credentials configured on your local machine as per this [documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html#configuration).

```sh
# Done only on initial setup
asdf install
python -m venv .venv

# Install dependencies on virtual env
source .venv/bin/activate
pip install -r requirements.txt

# Run
python .

# Deactivate virtual env
deactivate
```