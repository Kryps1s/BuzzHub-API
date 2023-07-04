import boto3
from boto3.dynamodb.types import TypeDeserializer
TABLE_NAME = "dev_calendar"


def lambda_handler(event, context):
    event_id = event['arguments']['eventId']
    key = {
        'eventId': {'S': event_id}
    }
    dynamodb = boto3.client('dynamodb', region_name="ca-central-1")
    response = dynamodb.get_item(
        TableName=TABLE_NAME,
        Key=key
    )
    item = response.get('Item')
    deserializer = TypeDeserializer()
    # Convert DynamoDB item to raw JSON
    return {key: deserializer.deserialize(value) for key, value in item.items()}
