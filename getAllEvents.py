import boto3
from boto3.dynamodb.types import TypeDeserializer
TABLE_NAME = "Events-dev"


def lambda_handler():
    # Create a DynamoDB client for the specified region
    dynamodb = boto3.client('dynamodb', region_name='ca-central-1')

    response = dynamodb.scan(TableName=TABLE_NAME)
    items = response.get('Items', [])
    deserializer = TypeDeserializer()
    items = [{key: deserializer.deserialize(value) for key, value in item.items()} for item in items]
    return [items]
