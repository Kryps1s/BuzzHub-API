import os
import requests
import json

def get_trello_board(board):
    """get trello board"""
    url = "https://api.trello.com/1/boards/" + board
    headers = {
    "Accept": "application/json"
    }
    query = {
    'key': os.environ['TRELLO_KEY'],
    'token': os.environ['TRELLO_TOKEN']
    }
    response = requests.request(
    "GET",
    url,
    headers=headers,
    params=query,
    timeout=30
    )
    if response.ok is False:
        raise ValueError("Trello API error: " + response.text)
    return response.json()


def lambda_handler(event, context):
    """get the agenda for the weekly meeting"""
    