import boto3
from boto3.dynamodb.types import TypeDeserializer
TABLE_NAME = "dev_calendar"
SORT_NAME = "upcomingEvent"


def lambda_handler(event, context):
    dynamodb = boto3.client('dynamodb', region_name='ca-central-1')
    response = dynamodb.scan(TableName=TABLE_NAME, IndexName=SORT_NAME)
    items = response.get('Items', [])
    deserializer = TypeDeserializer()
    items = [{key: deserializer.deserialize(value) for key, value in item.items()} for item in items]
    if 'arguments' in event[0]:
        arguments = event[0]['arguments']
        if 'type' in arguments:
            items = [item for item in items if item.get('type') == arguments['type']]
        if 'limit' in arguments:
            limit = arguments.get('limit')
            items = items[:limit]
    return items
