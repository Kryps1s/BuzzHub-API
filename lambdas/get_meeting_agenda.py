""" get the current agenda for the weekly meeting """
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

def get_trello_board(board):
    """get taiga board"""
    url = "https://api.taiga.io/api/v1/userstories?project="+ board
    headers = {
        "Authorization": "Bearer " + auth.token
    }
    response = requests.request(
        "GET",
        url,
        headers=headers,
        timeout=30
    )
    return response.json()

def sort_cards(cards,board):
    """sort cards into unassigned, in progress, and completed"""
    #if board is BEEKEEPING get the list ids for the unassigned, in progress, and completed lists
    if board == 'BEEKEEPING':
        unassigned_id = os.environ['BEEKEEPING_LIST_UNASSIGNED']
        in_progress_id = os.environ['BEEKEEPING_LIST_IN_PROGRESS']
        completed_id = os.environ['BEEKEEPING_LIST_COMPLETED']
    #if board is COLLECTIVE get the list ids for the unassigned, in progress, and completed lists
    elif board == 'COLLECTIVE':
        unassigned_id = os.environ['COLLECTIVE_LIST_UNASSIGNED']
        in_progress_id = os.environ['COLLECTIVE_LIST_IN_PROGRESS']
        completed_id = os.environ['COLLECTIVE_LIST_COMPLETED']
        #else raise an error
    else:
        raise ValueError("Board must be BEEKEEPING or COLLECTIVE")
    #get the unassigned, in progress, and completed cards
    unassigned_cards = []
    in_progress_cards = []
    completed_cards = []
    for card in cards:
        #remove every in card but its name, and list id, idMembers, labels, due, and short link
        card = {'name': card['subject'],
                'status': card['status_extra_info']['name'].lower(), 
                'participants': card['assigned_users'],
                'labels': [{"name": tag[0]} for tag in card['tags']] if card['tags'] is not None else [],
                'start': card['due_date'],
                'eventId': card['ref']}
        #convert the labels to a list of string names of the labels
        card['labels'] = [label['name'] for label in card['labels']]
        if card['status'] == "unassigned":
            unassigned_cards.append(card)
        elif card['status'] == "in_progress":
            in_progress_cards.append(card)
        elif card['status'] == "completed":
            completed_cards.append(card)
    #sort the unassigned, in progress, and completed cards by due date,
    # then name. put cards with no due date at the end.
    unassigned_cards = sorted(unassigned_cards,\
                              key=lambda card: (card['start'] is None, card['start'], card['name']))
    in_progress_cards = sorted(in_progress_cards,\
                              key=lambda card: (card['start'] is None, card['start'], card['name']))
    completed_cards = sorted(completed_cards,\
                              key=lambda card: (card['start'] is None, card['start'], card['name']))
    #return the unassigned, in progress, and completed cards as one dict of lists
    return {'unassigned': unassigned_cards,\
            'inProgress': in_progress_cards,\
            'completed': completed_cards}

def lambda_handler(event, _):
    """get the current agenda for the weekly meeting"""
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


    #get the unassigned, in progress, and completed cards
    #get the beekeeping and collective boards
    print(event)
    beekeeping_cards= get_trello_board(os.environ['TAIGA_PROJECT_BEEKEEPING'])
    collective_cards = get_trello_board(os.environ['TAIGA_PROJECT_COLLECTIVE'])
    #get the unassigned, in progress, and completed cards for each board
    beekeeping_cards = sort_cards(beekeeping_cards, 'BEEKEEPING')
    collective_cards = sort_cards(collective_cards, 'COLLECTIVE')
    #return the unassigned, in progress, and completed cards for each board
    print({'BEEKEEPING': beekeeping_cards, 'COLLECTIVE': collective_cards})
    return {'BEEKEEPING': beekeeping_cards, 'COLLECTIVE': collective_cards}

lambda_handler({}, {})