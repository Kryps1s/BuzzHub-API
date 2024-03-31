"""update a trello card with the new event information"""
import os
import requests

#an enum of supported update keys
UPDATE_KEYS = ['subject', 'description', 'assigned_users', 'due_date', 'status']
class Auth:
    """Auth class for storing token"""
    def __init__(self, token):
        self.token = token

    def set_token(self, token):
        """Set token"""
        self.token = token

auth = Auth("")

def lambda_handler(event, _):
    """update a trello card with the new event information"""
    headers = {
    "Accept": "application/json"
    }
    login = requests.request(
    "post",
    "https://api.taiga.io/api/v1/auth",
    headers=headers,
    json={
    'username': os.environ['TAIGA_USER'],
    'password': os.environ['TAIGA_PASSWORD'],
    'type': "normal"
    },
    timeout=30
    )
    auth.set_token(login.json()['auth_token'])
    #get the trello  client
    #get the card id, name, and description from the event
    card_id = event['arguments']['eventId']
    updates = event['arguments']['updates']
    #check that updates is a dict, and that it only contains valid keys
    if not isinstance(updates, dict):
        raise TypeError("updates must be a dict")
    for key in updates:
        if key not in UPDATE_KEYS:
            raise ValueError("invalid key: " + key)
    #pylint: disable=R0801
    url = "https://api.taiga.io/v1/userstories/" + card_id
    headers = {
    "Accept": "application/json",
    "Authorization": "Bearer " + auth.token,
    }
    response = requests.request(
    "PATCH",
    url,
    headers=headers,
    json=updates,
    timeout=30
    )
    if response.ok is False:
        raise ValueError("Trello API error: " + response.text)
    return response.json()
