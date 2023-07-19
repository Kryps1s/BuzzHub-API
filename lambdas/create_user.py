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
    #pylint: disable=R1720 disable=R0916
    if "firstName" not in user or "lastName" not in user or "email" not in user \
    or "password" not in user or "trello" not in user or "code" not in user:
        raise ValueError("Missing field")
    if len(user["firstName"]) < 3 or len(user["lastName"]) < 3:
        raise ValueError("First and last name must be at least 3 characters")
    if not re.match(r"[^@]+@[^@]+\.[^@]+", user["email"]):
        raise ValueError("Invalid email")
    if not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}",
                     user["password"]):
        #pylint: disable=C0301
        raise ValueError("Password must be at least 8 characters, and contain at least one number, one uppercase letter, and one lowercase letter, and one special character")
    if user["trello"] not in fetch_members():
        raise ValueError("Invalid trello id")
    if user["code"] != os.environ['BUZZHUB_ACCESS_CODE']:
        raise ValueError("Invalid access code")

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
                    'Value': user["firstName"] + " " + user["lastName"]
                },
                {
                    'Name': 'custom:trello',
                    'Value': user["trello"]
                }
            ]
        )
        #print to cloudwatch logs
        print("user created" + user["email"])
        return user["email"]

    except ClientError as err:
        print(err.response["message"])
        raise ValueError(err.response["message"]) from err

def lambda_handler(event, _):
    """Lambda handler"""
    #validate the user
    #ensure input exists
    if "arguments" not in event or "input" not in event["arguments"]:
        raise ValueError("Missing field")
    user = event["arguments"]["input"]
    print(user)
    try:
        validate_user(user)
    except ValueError as exc:
        # If any validation error occurs, raise the specific exception with the error message
        raise exc
    try:
        created = create_user(user)
        return created
    except ValueError as exc:
        # If any validation error occurs, raise the specific exception with the error message
        raise exc
