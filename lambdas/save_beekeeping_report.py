"""Save a job report to a trello card"""
import datetime
import os
import requests
class Auth:
    """Auth class for storing token"""
    def __init__(self, token):
        self.token = token

    def set_token(self, token):
        """Set token"""
        self.token = token

auth = Auth("")
def lambda_handler(event, _):
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
    #get next inspection details and validate, if any
    headers = {
    "Accept": "application/json"
    }
    query = {
    'username': os.environ['TAIGA_USER'],
    'password': os.environ['TAIGA_PASSWORD'],
    'type': "normal"
    }
    login = requests.request(
    "post",
    "https://api.taiga.io/api/v1/auth",
    headers=headers,
    json=query,
    timeout=30
    )
    auth.set_token(login.json()['auth_token'])

    if event['arguments']['nextInspection'] is not None:
        #validate inspection
        valid = validate_inspection(event['arguments']['nextInspection'])
        if valid is not True:
            raise ValueError(valid)
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
    card['description'] = requests.utils.unquote(report)
    #add participants to card
    card['assigned_users'] = participants
    #mark card as complete
    card['status'] = os.environ['BEEKEEPING_LIST_COMPLETED']
    #update card
    card = update_card(card)
    #create next event
    if event['arguments']['nextInspection'] is not None:
        if event['arguments']['goal'] is not None:
            card['description'] = event['arguments']['goal']
        card['due_date'] = event['arguments']['nextInspection']
        #get the label with the hive name and add it to the card
        hive = 'UNKNOWN HIVE'
        for label in [{"name": tag[0]} for tag in card['tags']] :
            #if label name contains hive:
            if label.find('hive:') != -1:
                hive = label.replace('hive:', '')
                break
        #get card name, full or partial based on inspection full, then display hive name
        if event['arguments']['full']:
            card_name = 'Full Inspection: ' + hive
        else:
            card_name = 'Partial Inspection: ' + hive
        card['subject'] = card_name
        create_next_inspection(card)
        return {"message": "successfully saved report and created next inspection"}
    return {"message": "successfully saved report"}

def fetch_card(card_id):
    """fetch card from trello"""
    url = f"https://api.taiga.io/api/v1/userstories/by_ref?ref={card_id}&project={os.environ['TAIGA_PROJECT_BEEKEEPING']}"
    headers = {
    "Accept": "application/json",
    "Authorization": "Bearer " + auth.token,
    }
    response = requests.request(
    "GET",
    url,
    headers=headers,
    timeout=30
    )
    if response.ok is False:
        raise ValueError("Trello API error: " + response.text)
    card = response.json()
    card['desc'] = card['description'] if card['description'] is not None else ""
    card['shortLink'] = card['ref'] if card['ref'] is not None else ""
    card['name'] = card['subject'] if card['subject'] is not None else ""
    card['due'] = card['due_date'] if card['due_date'] is not None else ""
    card['labels'] = [{"name": tag[0]} for tag in card['tags']] if card['tags'] is not None else []
    return response.json()

def update_card(card):
    """update card in trello"""
    url = "https://api.taiga.io/v1/userstories/" + card['id']
    headers = {
    "Accept": "application/json",
    "Authorization": "Bearer " + auth.token,
    }
    response = requests.request(
    "PATCH",
    url,
    headers=headers,
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

def validate_inspection(inspection):
    """validate inspection"""
    valid = True
    #check if date is a string
    if not isinstance(inspection, str):
        valid = False
    #check if date is empty
    if not inspection:
        valid = "date for next inspection cannot be empty"
    #check if date is not in the past
    today = datetime.date.today()
    year = int(inspection[0:4])
    month = int(inspection[5:7])
    day = int(inspection[8:10])
    date = datetime.date(year, month, day)
    if date < today:
        valid = "next inspection date must be greater than today"
    #check if date is in the format YYYY-MM-DD
    if len(inspection) != 10:
        valid = False
    if inspection[4] != '-' or inspection[7] != '-':
        valid = False
    return valid

def create_next_inspection(inspection):
    """create card in trello"""
    url = "https://api.taiga.io/v1/userstories"
    headers = {
    "Accept": "application/json",
    "Authorization": "Bearer " + auth.token,
    }
    query = {
    'status': os.environ['BEEKEEPING_LIST_UNASSIGNED'],
    'tags': inspection['tags'],
    'due_date': inspection['due_date'],
    'description': inspection['description'],
    'subject': inspection['subject'],
    'assigned_users': [],
    'project': os.environ['TAIGA_PROJECT_BEEKEEPING'],
    }
    response = requests.request(
    "POST",
    url,
    headers=headers,
    params=query,
    timeout=30
    )
    if response.ok is False:
        raise ValueError("Trello API error: " + response.text)
    return response.json()
