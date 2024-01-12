from webexteamssdk import WebexTeamsAPI, Webhook
from webhooks_manager import webex_teams_webhook_events
from urllib.parse import urljoin

import os
from dotenv import load_dotenv
from http import HTTPStatus


from aiohttp import web
from aiohttp.web import Request, Response
from threading import Thread
import asyncio

load_dotenv()

WEBHOOK_NAME = "Bot Umbrella Test"
WEBHOOK_URL_SUFFIX = "/events"
MESSAGE_WEBHOOK_RESOURCE = "messages"
MESSAGE_WEBHOOK_EVENT = "created"
CARDS_WEBHOOK_RESOURCE = "attachmentActions"
CARDS_WEBHOOK_EVENT = "created"

ngrok_url = os.getenv("NGROK_URL", "")
access_token = os.getenv("WEBEX_TEAMS_ACCESS_TOKEN", "")
PORT = os.getenv("PORT", "")
# Create the Webex Teams API connection object
api = WebexTeamsAPI(access_token = access_token)
# Get the details for the account who's access token we are using
me = api.people.me()

# ---------------------------- Create webhooks ----------------------------

# Helper functions
def delete_webhooks_with_name():

    """List all webhooks and delete webhooks created by this script."""

    for webhook in api.webhooks.list():
        if webhook.name == WEBHOOK_NAME:
            print("Deleting Webhook:", webhook.name, webhook.targetUrl)
            api.webhooks.delete(webhook.id)

def create_webhooks(ngrok_url):

    """Create the Webex Teams webhooks we need for our bot."""

    print("Creating Message Created Webhook...")
    targetUrl=urljoin(ngrok_url, WEBHOOK_URL_SUFFIX)
    webhook = api.webhooks.create(
        resource=MESSAGE_WEBHOOK_RESOURCE,
        event=MESSAGE_WEBHOOK_EVENT,
        name=WEBHOOK_NAME,
        targetUrl=targetUrl
    )
    print(webhook)
    print("Webhook successfully created.")

    print("Creating Attachment Actions Webhook...")
    webhook = api.webhooks.create(
        resource=CARDS_WEBHOOK_RESOURCE,
        event=CARDS_WEBHOOK_EVENT,
        name=WEBHOOK_NAME,
        targetUrl=urljoin(ngrok_url, WEBHOOK_URL_SUFFIX)
    )
    print(webhook)
    print("Webhook successfully created.")

async def events(request: Request) -> Response:
    if request.method == 'POST':
        # print('request.body:', request.body)
        body = await request.json()
        webex_teams_webhook_events(body)
        return Response(status=HTTPStatus.OK)
    return Response(status=HTTPStatus.OK)

def create_application ( ):
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.create_task(web.run_app(APP, host="localhost", port=int (PORT)))
        Thread(target=loop.run_forever).start()
    except Exception as error:
        raise error

APP = web.Application()
APP.router.add_post("/events", events)
delete_webhooks_with_name (  )
create_webhooks ( ngrok_url )
create_application ( )
