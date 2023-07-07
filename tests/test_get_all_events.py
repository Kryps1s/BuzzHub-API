"""Test get_all_events function in lambda_handler.py"""
import datetime
import pytest
from moto import mock_dynamodb
from lambdas.get_all_events import lambda_handler
from .utils import create_mock_table

@pytest.fixture(name='event')
def fixture_event():
    """ Generates Appsync GraphQL Event"""
    return {
        "arguments": {}
    }

#test_get_all_events.py
@mock_dynamodb
def test_get_all_events(event):
    """Test get_all_events function"""
    create_mock_table()
    # Call the function
    result = lambda_handler(event, {})
    # Check the result length is 5
    assert len(result) == 5

#test_get_all_events returns the limited number of events
@mock_dynamodb
def test_get_all_events_limit(event):
    """Test get_all_events function"""
    create_mock_table()
    # Add limit to the event
    event['arguments']['limit'] = 2
    # Call the function
    result = lambda_handler(event, {})
    # Check the result length is 2
    assert len(result) == 2

#test_get_all_events returns the events in the future
@mock_dynamodb
def test_get_all_events_future(event):
    """Test get_all_events function"""
    create_mock_table()
    # Add limit to the event
    event['arguments']['future'] = True
    # Call the function
    result = lambda_handler(event, {})
    # Check all events end properties are in the future
    for item in result:
        assert datetime.datetime.now() < datetime.datetime.fromisoformat(item['end'])

#test_get_all_events returns the events of selected type
@mock_dynamodb
def test_get_all_events_type(event):
    """Test get_all_events function"""
    create_mock_table()
    # Add limit to the event
    event['arguments']['type'] = 'MEETING'
    # Call the function
    result = lambda_handler(event, {})
    # Check all events are of type MEETING
    for item in result:
        assert item['type'] == 'MEETING'
