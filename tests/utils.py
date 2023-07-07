""" This file contains setup functions that are used by multiple tests."""
import datetime
import pytest
import boto3
from moto import mock_dynamodb

def create_mock_table():
    """ Generates DynamoDB Table with mock data"""
    events = []
    # Get the current date and time
    now = datetime.datetime.now()

    # Generate events in the past
    for i in range(2):
        event = {
            'eventId': f'event{i}',
            'start': (now - datetime.timedelta(days=7 * (i + 1))).strftime("%Y-%m-%dT%H:%M:%S"),
            'end': (now - datetime.timedelta(days=7 * (i + 1))).strftime("%Y-%m-%dT%H:%M:%S"),
            'type': 'BEEKEEPING',
            'roles': [
                {
                    'roleName': 'Role 1',
                    'userName': 'User 1'
                },
                {
                    'roleName': 'Role 2',
                    'userName': 'User 2'
                }
            ]
        }
        events.append(event)

    # Generate events in the future
    for i in range(3):
        event = {
            'eventId': f'event{i + 2}',
            'start': (now + datetime.timedelta(days=7 * (i + 1))).strftime("%Y-%m-%dT%H:%M:%S"),
            'end': (now + datetime.timedelta(days=7 * (i + 1))).strftime("%Y-%m-%dT%H:%M:%S"),
            'type': 'MEETING',
            'roles': [
                {
                    'roleName': 'Role 1',
                    'userName': 'User 1'
                },
                {
                    'roleName': 'Role 2',
                    'userName': 'User 2'
                }
            ]
        }
        events.append(event)



    dynamodb_table = boto3.resource('dynamodb', region_name='ca-central-1')
    table = dynamodb_table.create_table(
        TableName='test_calendar',
        KeySchema=[
            {
                'AttributeName': 'eventId',
                'KeyType': 'HASH'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'eventId',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'type',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'start',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        },
        GlobalSecondaryIndexes=[
            {
                'IndexName': 'upcomingEvent',
                'KeySchema': [
                    {
                        'AttributeName': 'type',
                        'KeyType': 'HASH'
                    },
                    {
                        'AttributeName': 'start',
                        'KeyType': 'RANGE'
                    }
                ],
                'Projection': {
                    'ProjectionType': 'ALL'
                },
                'ProvisionedThroughput': {
                    'ReadCapacityUnits': 5,
                    'WriteCapacityUnits': 5
                }
            }
        ]
    )
    # Add multiple items to the table
    with table.batch_writer() as batch:
        for event in events:
            batch.put_item(Item=event)
