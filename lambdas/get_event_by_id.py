"""
This lambda function will return a calendar event by id. 
"""
    # pylint: disable=R0801

import os
import json
import requests


TABLE_NAME = os.environ['env']+"_calendar"

def is_valid_json(json_str):
    """Check if string is valid json"""
    try:
        #convert string to json
        json.loads(json_str)
        return True
    except json.JSONDecodeError:
        return False

def map_card_to_event(event_type, card):
    """Map trello card to event object"""
    event = {}
    event['eventId'] = card['shortLink']
    event['type'] = event_type
    event['start'] = card['due']
    #map specific event fields
    if event_type == "BEEKEEPING":
        event['jobs'] = []
        event['hives'] = []
        event['roles'] = []
        #try parsing {} enclosure in desc into json if first character is {
        if card['desc'].startswith("{") and is_valid_json(card['desc'].split("}")[0] + "}"):
            roles = json.loads(card['desc'].split("}")[0] + "}")
            #add roles to event
            event['roles'].append(roles)
        event['type'] = event_type
        #loop through labels
        for label in card['labels']:
            #if label name starts with job or hive, add to event array
            if label['name'].startswith("job"):
                event['jobs'].append(label['name'].split("job:")[1])
            elif label['name'].startswith("hive"):
                event['hives'].append(label['name'].split("hive:")[1])
    elif event_type == "MEETING":
        #check if label starting with MONTHLY is present
        for label in card['labels']:
            if label['name'].startswith("MONTHLY"):
                event['isMonthly'] = True
            if label['name'] == "ONLINE":
                event['location'] = "ONLINE"
            if label['name'] == "IN-PERSON":
                event['location'] = "IN-PERSON"
    return event

def fetch_event(event_id):
    """Fetch trello card by id"""
    url = "https://api.trello.com/1/cards/" + event_id
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
        return None
    #remove cards with no due date
    if 'due' not in response.json():
        return None
    return response.json()

def lambda_handler(event, _):
    """
    A simple wrapper around the DynamoDB get_item function.
    id is a string
    event : the event object from the GraphQL query
    """
    #check arguments has event id, event_id is a string, and not empty
    if 'eventId' not in event['arguments']:
        return {'error': 'eventId must be a string and not empty'}
    if not isinstance(event['arguments']['eventId'], str):
        return {'error': 'eventId must be a string and not empty'}
    if not event['arguments']['eventId']:
        return {'error': 'eventId must be a string and not empty'}
    event_id = event['arguments']['eventId']
    trello_card = fetch_event(event_id)
    if trello_card is None:
        return {'error': 'event not found'}
    #find which env variable BOARD_ID matches with idBoard
    board_id = trello_card['idBoard']
    if board_id == os.environ['BEEKEEPING_BOARD_ID']:
        event_type = "BEEKEEPING"
    elif board_id == os.environ['MEETING_BOARD_ID']:
        event_type = "MEETING"
    elif board_id == os.environ['COLLECTIVE_BOARD_ID']:
        event_type = "COLLECTIVE"
    else:
        return {'error': 'board id not found'}
    #map trello card to event
    event = map_card_to_event(event_type, trello_card)
    return event
