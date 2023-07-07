"""
This lambda function will return a calendar event by id. 
"""
import os
import boto3
from boto3.dynamodb.types import TypeDeserializer

TABLE_NAME = os.environ['env']+"_calendar"


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
    key = {
        'eventId': {'S': event_id}
    }
    dynamodb = boto3.client('dynamodb', os.environ['region'])
    response = dynamodb.get_item(
        TableName=TABLE_NAME,
        Key=key
    )
    #handle item not found
    if 'Item' not in response:
        return None
    item = response.get('Item')
    deserializer = TypeDeserializer()
    # Convert DynamoDB item to raw JSON
    return {key: deserializer.deserialize(value) for key, value in item.items()}
