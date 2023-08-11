"""Save a job report to a trello card"""
import os
import requests

def lambda_handler(event):
    """Lambda handler"""
    #validate event
    try:
        validate_event(event)
    except KeyError as err:
        raise ValueError("missing field: " + str(err)) from err
    except ValueError as err:
        raise ValueError(str(err)) from err
    #get card id from event
    card_id = event['arguments']['eventId']
    #get report from event
    report = event['arguments']['report']
    #get the participants from event
    participants = event['arguments']['participants']
    #validate report
    if not validate_report(report):
        raise ValueError("invalid report")
    #validate participants
    valid = validate_participants(participants)
    if valid is not True:
        raise ValueError(valid)
    #fetch card
    card = fetch_card(card_id)
    #add report to card
    card['desc'] = report
    #add participants to card
    card['idMembers'] = participants
    #mark card as complete
    card['dueComplete'] = True
    #move card to Completed column
    card['idList'] = os.environ['BEEKEEPING_LIST_COMPLETED']
    #update card
    card = update_card(card)
    return {"message": "successfully saved report"}

def fetch_card(card_id):
    """fetch card from trello"""
    url = "https://api.trello.com/1/cards/" + card_id
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

def update_card(card):
    """update card in trello"""
    url = "https://api.trello.com/1/cards/" + card['shortLink']
    headers = {
    "Accept": "application/json"
    }
    query = {
    'key': os.environ['TRELLO_KEY'],
    'token': os.environ['TRELLO_TOKEN'],
    }
    response = requests.request(
    "PUT",
    url,
    headers=headers,
    params=query,
    json=card,
    timeout=30
    )
    if response.ok is False:
        raise ValueError("Trello API error: " + response.text)
    return response.json()

def validate_report(report):
    """Validate report"""
    #check if report is a string
    if not isinstance(report, str):
        return False
    #check if report is empty
    if not report:
        return False
    return True

def validate_participants(participants):
    """Validate participants"""
    #check if participants is an array
    if not isinstance(participants, list):
        return "invalid participants"
    #check if participants is empty
    if not participants:
        return "there must be at least one attendee"
    #check if participants is an array of strings
    for item in participants:
        if not isinstance(item, str):
            return "invalid participants"
    return True

def validate_event(event):
    """validate event"""
    #check if event is a dict
    if not isinstance(event, dict):
        return False
    #check if arguments is a dict
    if not isinstance(event['arguments'], dict):
        return False
    #check if eventId is a string
    if not isinstance(event['arguments']['eventId'], str):
        return False
    #check if report is a string
    if not isinstance(event['arguments']['report'], str):
        return False
    #check if participants is a list
    if not isinstance(event['arguments']['participants'], list):
        return False
    return True
