"""This lambda function will return all members of the trello 
organization that are valid options for user to link to their account."""

import os
import json
import requests

class TrelloAPIError(Exception):
    """Exception raised for errors in the Trello API"""

#the root trello user, and te buzzhub user are invalid members
invalid_members = ["585a7e82c8a3142c77cfb22e"]

def fetch_members():
    """Fetch all members from the organization"""
    #pylint: disable=R0801
    headers = {
    "Accept": "application/json"
    }
    query = {
    'username': os.environ['TAIGA_USER'],
    'password': os.environ['TAIGA_PASSWORD'],
    'type': "normal"
    }
    response = requests.request(
    "post",
    "https://api.taiga.io/api/v1/auth",
    headers=headers,
    json=query,
    timeout=30
    )
    if response.ok is False:
        raise TrelloAPIError("Trello API error: " + response['error'])
    #filter invalid members from list of invalid members
    auth = response.json()['auth_token']
    headers = {
    "Accept": "application/json",
    "Authorization": "Bearer " + auth
    }
    url = "https://api.taiga.io/api/v1/memberships?project=" + os.environ['TAIGA_PROJECT_MEETING']
    response = requests.request(
    "get",
    url,
    headers=headers,
    timeout=30
    )
    
    members = list(response.json())
    members = [{ "id": member["id"], "fullName": member["full_name"],\
                 "username": member["user_email"] } for member in members]
    return members
# pylint: disable=W0613
def lambda_handler(event, _):
    """Lambda handler"""
    try:
        members = fetch_members()
        #add __typename to each member
        for member in members:
            member['__typename'] = "TrelloMember"
        #print to cloudwatch logs
        print("members fetched: " + str(len(members)))
        print(members)
        return members
    except TrelloAPIError as err:
        return {
            'statusCode': 500,
            'body': json.dumps({"error": str(err)})
        }

lambda_handler({}, {})