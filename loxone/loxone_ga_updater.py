import getopt
import os

import requests
import sys
from dotenv import load_dotenv

# Quick script to update GA metatags for temperature / lights and dimmers

def main(argv):
    load_dotenv(dotenv_path=".env")
    oauthtoken = os.getenv('OAUTH_TOKEN')
    items_url = os.getenv("OPENHAB_ITEMS_URL")

    try:
        opts, args = getopt.getopt(argv,"htld",["temperature","light","dimmer"])
    except getopt.GetoptError:
        print('loxone.py -t -l -d')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('loxone.py -t --temperature -l --light -d --dimmer')
            sys.exit()
        # TODO set up and define classes specific to the control type
        elif opt in ("-t", "--temperature"):
            print("Setting temperature")
            items = getItems(items_url)
            updateGaItems(oauthtoken, items, "t")
        elif opt in ("-l", "--light"):
            print("Setting lights")
            items = getItems(items_url)
            updateGaItems(oauthtoken, items, "l")
        elif opt in ("-d", "--dimmer"):
            print("Setting lights")
            items = getItems(items_url)
            updateGaItems(oauthtoken, items, "d")

def getItems(items_url):
    resp = requests.get(url=items_url)
    return resp.json()

def updateGaItems(oauthtoken, items, mode):
    for item in items:
        item_url = item['link']
        tags = item["tags"]
        type_ = item['type']

        # split this -> Kitchen / Intelligent room controller/ Current Temperature
        labelName = item['label']
        labelNameArray = labelName.split('/')
        roomHint = labelNameArray[0]

        if mode == "t":
            setTemperature(item, labelName, roomHint, tags, type_, item_url, oauthtoken)
        elif mode == "l":
            setLight(item, labelName, roomHint, tags, type_, item_url, oauthtoken)
        elif mode == "d":
            setDimmer(item, labelName, roomHint, tags, type_, item_url, oauthtoken)



def setTemperature(item, labelName, roomHint, tags, type_, url, oauthtoken):
    if 'CurrentTemperature' in tags and 'Current Temperature' in labelName:
        sensorParams = {
            "value": "TemperatureSensor",
            "config": {
                "name": "Temperature",
                "roomHint": roomHint
            }
        }

        url = f"{url}/metadata/ga"
        print(f"{roomHint} - {type_.upper()}: {tags} {item['label']} - {url} - {item}")

        response = requests.put(url=url,
                                json=sensorParams,
                                headers={
                                    'content-type': 'application/json',
                                    'Authorization': f"Bearer {oauthtoken}"
                                })
        print(response)

def setLight(item, labelName, roomHint, tags, type_, url, oauthtoken):
    label_name_split = labelName.split("/")
    if 'Lighting' in tags \
            and type_ == 'Switch' \
            and len(label_name_split) == 2:
        print(f"{labelName} - {len(label_name_split)} - {label_name_split} - {tags}")
        sensorParams = {
            "value": "Light",
            "config": {
                "name": label_name_split[1],
                "roomHint": roomHint
            }
        }

        url = f"{url}/metadata/ga"
        print(f"{roomHint} - {type_.upper()}: {tags} {item['label']} - {url} - {item}")

        response = requests.put(url=url,
                                json=sensorParams,
                                headers={
                                    'content-type': 'application/json',
                                    'Authorization': f"Bearer {oauthtoken}"
                                })
        print(response)


def setDimmer(item, labelName, roomHint, tags, type_, url, oauthtoken):
    label_name_split = labelName.split("/")
    if 'Lighting' in tags \
            and type_ == 'Dimmer' \
            and len(label_name_split) == 2:
        print(f"{labelName} - {len(label_name_split)} - {label_name_split} - {tags}")
        sensorParams = {
            "value": "Light",
            "config": {
                "name": label_name_split[1],
                "roomHint": roomHint
            }
        }

        url = f"{url}/metadata/ga"
        print(f"{roomHint} - {type_.upper()}: {tags} {item['label']} - {url} - {item}")

        response = requests.put(url=url,
                                json=sensorParams,
                                headers={
                                    'content-type': 'application/json',
                                    'Authorization': f"Bearer {oauthtoken}"
                                })
        print(response)


if __name__ == "__main__":
    main(sys.argv[1:])




