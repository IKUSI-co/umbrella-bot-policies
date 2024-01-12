
import requests
import json, os
from jinja2 import Template
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()


CARDS_DIR = os.getenv("CARDS_DIR", "")

def create_response_card(message):


        with open(os.path.join(CARDS_DIR, 'response_card.json.j2')) as json_file:
                j2_template = Template(json_file.read())  

        data = {
                "message": message
        }

        response_card = json.loads(j2_template.render(data))

        attachment = {
                "contentType": "application/vnd.microsoft.card.adaptive",
                "content": response_card
        }

        return attachment


def create_request_url_card():

    with open(os.path.join(CARDS_DIR, 'request_url_card.json.j2')) as json_file:
            j2_template = Template(json_file.read())  

    data = {
    }

    response_card = json.loads(j2_template.render(data))

    attachment = {
        "contentType": "application/vnd.microsoft.card.adaptive",
        "content": response_card
    }

    return attachment