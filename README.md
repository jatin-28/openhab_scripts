#Using POETRY

Create .env file under root with:
OAUTH_TOKEN=<API Token from OPENHAB - Found by clicking your Profile>
OPENHAB_ITEMS_URL=http://<OPENHAB_SERVER>:<OPENHAB_PORT>/rest/items?recursive=false

Commands to run to setup / update poetry
poetry lock
poetry install
poetry run pytest tests
poetry run python loxone/loxone_ga_updater.py

Troubleshooting
- when updating python
- run:
`rm -rf .venv && poetry env remove --all`