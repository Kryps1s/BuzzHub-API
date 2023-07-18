"""Create a new user in the cognito user pool."""
import os
import re
import boto3
import requests
from botocore.exceptions import ClientError

class TrelloAPIError(Exception):
    """Exception raised for errors in the Trello API"""

def fetch_members():
    """Fetch all members from the organization"""
    #pylint: disable=R0801
    url = "https://api.trello.com/1/organizations/" + os.environ['TRELLO_ORGANIZATION'] + "/members"
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
        raise TrelloAPIError("Trello API error: " + response['error'])
    #filter invalid members from list of invalid members

    invalid_members = ["585a7e82c8a3142c77cfb22e", "placeholder_buzzhub_user"]
    members = [user['id'] for user in response.json() if user['id'] not in invalid_members]
    return members

def validate_user(user):
    """Validate the user"""
    #check input has all fields in the user class
    error = None
    #pylint: disable=R0916
    if "first_name" not in user or "last_name" not in user or "email" not in user \
    or "password" not in user or "trello_id" not in user or "code" not in user:
        error = {"error": "Missing field"}
    #check first and last name are at least 3 characters
    elif len(user["first_name"]) < 3 or len(user["last_name"]) < 3:
        error = {"error": "First and last name must be at least 3 characters"}
    #check email is valid regex
    elif not re.match(r"[^@]+@[^@]+\.[^@]+", user["email"]):
        error = {"error": "Invalid email"}
    #check password is at least 8 characters, and contains at least one number,
    # one uppercase letter, and one lowercase letter, and one special character
    elif not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}",
                     user["password"]):
        #pylint: disable=C0301
        error = {"error": "Password must be at least 8 characters, and contain at least one number, one uppercase letter, and one lowercase letter, and one special character"}
    #check trello id is valid
    elif user["trello_id"] not in fetch_members():
        error = {"error": "Invalid trello id"}
    elif user["code"] != os.environ['BUZZHUB_ACCESS_CODE']:
        error = {"error": "Invalid access code"}
    return error

def create_user(user):
    """Create the user in the cognito user pool"""
    try:
        client = boto3.client('cognito-idp')
        client.sign_up(
            ClientId= os.environ['COGNITO_CLIENT_ID'],
            Username=user["email"],
            Password=user["password"],
            UserAttributes=[
                {
                    'Name': 'name',
                    'Value': user["first_name"] + " " + user["last_name"]
                },
                {
                    'Name': 'custom:trello',
                    'Value': user["trello_id"]
                }
            ]
        )
        #print to cloudwatch logs
        print("user created" + user["email"])
        return user["email"]
    except ClientError as err:
        print(err)
        return {"error": str(err)}

def lambda_handler(event, _):
    """Lambda handler"""
    #get the user from the event
    #validate the user
    user = event["arguments"]
    error = validate_user(user)
    if error:
        print(error)
        return error
    return create_user(user)
