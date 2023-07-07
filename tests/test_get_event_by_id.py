""" Tests for get_event_by_id """
import pytest
from moto import mock_dynamodb
from lambdas.get_event_by_id import lambda_handler
from .utils import create_mock_table

@pytest.fixture(name='event')
def fixture_event():
    """ Generates Appsync GraphQL Event"""
    return {
        "arguments": {
            "eventId": "event1"
        }
    }

#test_get_event_by_id.py
@mock_dynamodb
def test_get_event_by_id(event):
    """ Test get_event_by_id """
    create_mock_table()
    # Call the function
    result = lambda_handler(event, {})
    # Check the result
    assert result['eventId'] == 'event1'
    assert result['type'] == 'BEEKEEPING'
    assert result['roles'] == [
        {
            'roleName': 'Role 1',
            'userName': 'User 1'
        },
        {
            'roleName': 'Role 2',
            'userName': 'User 2'
        }
    ]

#test fail scenario
@mock_dynamodb
def test_get_event_by_id_fail_event_not_found(event):
    """ Test get_event_by_id fails when event is not found """
    # Create the table
    create_mock_table()
    # Call the function
    event['arguments']['eventId'] = 'nonexistent'
    result = lambda_handler(event, {})
    # Check the result
    assert result is None

#test fail scenario no event id provided
@mock_dynamodb
def test_get_event_by_id_fail_no_event_id(event):
    """ Test get_event_by_id fails when no event id is provided """
    # Create the table
    create_mock_table()
    # Call the function
    del event['arguments']['eventId']
    result = lambda_handler(event, {})
    # Check the result is error message
    assert result['error'] == 'eventId must be a string and not empty'

#test fail scenario event id is not a string
@mock_dynamodb
def test_get_event_by_id_fail_event_id_not_string(event):
    """Test get_event_by_id fails when event id is not a string"""
    # Create the table
    create_mock_table()
    # Call the function
    event['arguments']['eventId'] = 1
    result = lambda_handler(event, {})
    # Check the result is error message
    assert result['error'] == 'eventId must be a string and not empty'
