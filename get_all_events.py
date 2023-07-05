"""
This lambda function will return all events in the calendar, with optional modifiers. 
"""
import os
import boto3
from boto3.dynamodb.types import TypeDeserializer

TABLE_NAME = os.environ['env']+"_calendar"
SORT_NAME = "upcomingEvent"


def lambda_handler(event, context):
    """
    wrapper aroud the DynamoDB scan function. 
    event : the event object from the GraphQL query
    arguments : the arguments object from the GraphQL query
        type : string, from the GraphQL type enum
        limit : int, the number of items to return
    """
    dynamodb = boto3.client('dynamodb', region_name=os.environ['region'])
    response = dynamodb.scan(TableName=TABLE_NAME, IndexName=SORT_NAME)
    items = response.get('Items', [])
    deserializer = TypeDeserializer()
    items = [
        {
            key: deserializer.deserialize(value)
            for key, value in item.items()
        } for item in items]
    if 'arguments' in event:
        arguments = event['arguments']
        if 'type' in arguments:
            items = [item for item in items if item.get('type') == arguments['type']]
        if 'limit' in arguments:
            limit = arguments.get('limit')
            items = items[:limit]
    return items
