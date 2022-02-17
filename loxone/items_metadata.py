import os

import requests
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")

oauthtoken = os.getenv('OAUTH_TOKEN')

url = os.getenv("OPENHAB_ITEMS_URL")

resp = requests.get(url=url)
items = resp.json()

for item in items:
    url = item['link']
    params = {'metadata': 'ga'}
    itemInfo = requests.get(url, params=params)
    tags = item["tags"]
    type_ = item['type']

    # split this -> Kitchen / Intelligent room controller/ Current Temperature
    labelName = item['label']
    labelNameArray = labelName.split('/')
    roomHint = labelNameArray[0]

    if 'CurrentTemperature' in tags and 'Current Temperature' in labelName:
        sensorParams = {
            "value" : "TemperatureSensor",
            "config": {
                "name":"Temperature",
                "roomHint": roomHint
            }
        }

        url = f"{url}/metadata/ga"
        print(f"{roomHint} - {type_.upper()}: {tags} {item['label']} - {url} - {item}")

        response = requests.put(url=url,
                                json=sensorParams,
                                headers={
                                    'content-type':'application/json',
                                    'Authorization' : f"Bearer {oauthtoken}"
                                })

        print(response)



