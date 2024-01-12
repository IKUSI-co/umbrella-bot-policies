# Webex-Umbrella integration for managing destination lists

The objective of this project is to interact with a Webex bot, which can request a URL and this URL can be put in an Umbrella destination list

## Requirements

1. Access to [Umbrella](https://login.umbrella.com)
2. Access to [Webex Developer](https://developer.webex.com/)
3. [Python 3.7](https://www.python.org/) or above
4. ngrok

## Getting Started

1. Clone repo

`git clone https://github.com/IKUSI-co/umbrella-bot-policies.git`

2. Install the required libraries

`pip install -r requirements.txt`

**Webex Bot Configuration**

3. Create a Bot in Webex and update `.env` with your your Webex Access Token.

**Umbrella Configuration**

4. Update `.env` with your Umbrella API access token. For more information on creating your Access Token, please refer to the following link: [Develops Cisco](https://developer.cisco.com/docs/cloud-security/#!authentication/generate-an-api-access-token)

5. Update `.env` with the ID of Organization and Destination List

**Ngrok Configuration**

6. Update `.env` with the port you are going to use

7. Run the following command in Ngrok and update `.env` with your Forwarding under `NGROK_URL`

`ngrok http http://localhost:PORT`

**Users Configuration**

8. Update the `users/users.txt` file with the email addresses of individuals who have write access to the bot. List each email address on a separate line

**Run Project**

9. Run code

`python3 manage.py`

## SUCCESS

From now on, you can send any message to the bot. If you are authorized, it will respond with a card asking for the URL you want to add to the Umbrella destination list. Upon sending the URL, the bot will reply with a message confirming the successful request. If an error occurs, it will also notify you accordingly. If your email is not on the list of authorized emails for requests, the bot will send a message informing you that you do not have permission to submit requests.

![image](https://github.com/IKUSI-co/umbrella-bot-policies/assets/135241749/b799a47b-dbf2-4018-aa1a-c5dbd9ab29d9)
