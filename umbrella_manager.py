import json
import requests
import os
from dotenv import load_dotenv

load_dotenv()


access_token = os.getenv("WEBEX_TEAMS_ACCESS_TOKEN", "")

BASE_URL = os.getenv("BASE_URL", "")
ORG_ID = os.getenv("ORG_ID", "")
DESTINATION_LIST_ID = os.getenv("DESTINATION_LIST_ID", "")
AUTHORIZATION = os.getenv("AUTHORIZATION", "")

def add_destination_to_list(url_requested):

    url  = BASE_URL + ORG_ID + "/destinationlists/" + DESTINATION_LIST_ID + "/destinations"

    payload = json.dumps([
        {
            "destination": url_requested,
        }
    ])
    auth = "Basic " + AUTHORIZATION
    headers = {
        'Authorization': auth,
        'Content-Type': 'application/json',
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response
