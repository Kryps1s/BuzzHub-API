import os
import boto3
from boto3.dynamodb.types import TypeDeserializer

TABLE_NAME = os.environ['env']+"_calendar"
SORT_NAME = "upcomingEvent"


def lambda_handler(event, context):
    dynamodb = boto3.client('dynamodb', region_name=os.environ['region'])
    response = dynamodb.scan(TableName=TABLE_NAME, IndexName=SORT_NAME)
    items = response.get('Items', [])
    deserializer = TypeDeserializer()
    items = [{key: deserializer.deserialize(value) for key, value in item.items()} for item in items]
    if 'arguments' in event:
        arguments = event['arguments']
        if 'type' in arguments:
            items = [item for item in items if item.get('type') == arguments['type']]
        if 'limit' in arguments:
            limit = arguments.get('limit')
            items = items[:limit]
    return items
