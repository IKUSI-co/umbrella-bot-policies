import os
import sys
import requests
import json
from urllib.parse import urljoin
from webexteamssdk import WebexTeamsAPI, Webhook
from webexteamssdk.exceptions import ApiError
from dotenv import load_dotenv

from webhooks_card import create_request_url_card,create_response_card
from umbrella_manager import add_destination_to_list

load_dotenv()


MESSAGE_WEBHOOK_RESOURCE = "messages"
MESSAGE_WEBHOOK_EVENT = "created"
CARDS_WEBHOOK_RESOURCE = "attachmentActions"
CARDS_WEBHOOK_EVENT = "created"
access_token = os.getenv("WEBEX_TEAMS_ACCESS_TOKEN", "")
api = WebexTeamsAPI(access_token = access_token)
def webex_teams_webhook_events(request_json):

    """Respond to inbound webhook JSON HTTP POST from Webex Teams."""

    # Create a Webhook object from the JSON data
    webhook_obj = Webhook(request_json)
    # print(f"WEBHOOK:\n{webhook_obj}")
    message_id = str(webhook_obj.data.id)

    # Handle a new message event
    if (webhook_obj.resource == MESSAGE_WEBHOOK_RESOURCE
            and webhook_obj.event == MESSAGE_WEBHOOK_EVENT):
        handle_message_response(webhook_obj)
    # Handle an Action.Submit button press event
    elif (webhook_obj.resource == CARDS_WEBHOOK_RESOURCE
        and webhook_obj.event == CARDS_WEBHOOK_EVENT):
        handle_card_response(webhook_obj)

    return "OK"

def handle_card_response (webhook):
    
    attachment_action = api.attachment_actions.get(webhook.data.id)
    person = api.people.get(attachment_action.personId)
    user = False 

    with open("users/users.txt") as archivo:
        for linea in archivo:
            if linea == person.emails[0]:
                user = True 
                
    if ( user == False ):
        message = "Acceso no autorizado! ❌ "
        send_response_card(person.emails[0], message)
    else:
        url =  list((attachment_action.inputs).items())[0][1] 
        response = add_destination_to_list ( url )

        if response.status_code == 200:
            message = " La solicitud fue completada! ✅"
            send_response_card(person.emails[0], message)
        else:
            message = "La solicitud no pudo ser completada! ❌ "
            send_response_card(person.emails[0], message)
    

def send_response_card(person, message):

    attachment = create_response_card(message)
    markdown = message
    send_message(person, attachment, markdown) 


def handle_message_response(webhook_obj):

    """Respond to incoming message - Responds with card to request URL"""

    user = False 

    with open("users/users.txt") as archivo:
        for linea in archivo:
            if linea == webhook_obj.data.personEmail:
                user = True 

    if ( user == True ):
        send_request_url_card(webhook_obj.data.personEmail)
    else:
        print ( "HELLO")
        message = "Acceso no autorizado! ❌ "
        send_response_card(webhook_obj.data.personEmail, message)

def send_request_url_card(person_email):
    
    attachment = create_request_url_card()
    markdown = 'Tarjetas no soportadas 😕.'
    send_message(person_email, attachment, markdown)  

def send_message(email, attachment, markdown):

    print('SEND MESSAGE')

    apiUrl = 'https://webexapis.com/v1/messages'
    access_token = os.environ.get("WEBEX_TEAMS_ACCESS_TOKEN", "")
    httpHeaders = { 'Content-type': 'application/json', 'Authorization': 'Bearer ' + access_token }
    
    body = {
        "toPersonEmail": email,
        "markdown":  markdown,
        "attachments" : [attachment]
    }

    response = requests.post( url = apiUrl, json = body, headers = httpHeaders )