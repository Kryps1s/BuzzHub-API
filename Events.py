import json
import boto3
from boto3.dynamodb.types import TypeDeserializer
TABLE_NAME = "Events-dev"
def handler(event, context):
    switch = {
        'getEvent': handle_get_event,
    }
    # Get the appropriate function based on the field name
    func = switch.get(event['info']['fieldName'])
    if func:
        # Call the function
        result = func(event)
        # Process the result further if needed
        return result

def handle_get_event(event):
    # Logic for handling 'getEvent' field
    event_id = event['arguments']['eventId']
    dynamodb_client = boto3.client('dynamodb', region_name="ca-central-1")
    # event_id = parsed_payload['variables']['eventId']
    key = {
        'eventId': {'S': event_id}
    }
    response = dynamodb_client.get_item(
        TableName=TABLE_NAME,
        Key=key
    )
    item = response.get('Item')
    deserializer = TypeDeserializer()
    # Convert DynamoDB item to raw JSON
    raw_json = {key: deserializer.deserialize(value) for key, value in item.items()}
    return raw_json