""" Tests for get_event_by_id """
from unittest.mock import patch
import pytest
from lambdas.get_event_by_id import lambda_handler
from .utils import mock_trello_card

@pytest.fixture(name='event')
def fixture_event():
    """ Generates Appsync GraphQL Event"""
    return {
        "arguments": {
            "eventId": "oBsiLWUX"
        }
    }

#test_get_event_by_id.py
@patch('lambdas.get_event_by_id.fetch_event')
def test_get_event_by_id(mock_fetch_event, event):
    """ Test get_event_by_id """
    #mock fetch_event
    mock_fetch_event.return_value = mock_trello_card()
    # Call the function
    result = lambda_handler(event, {})
    # Check the result
    assert result['eventId'] == 'oBsiLWUX'

#test fail scenario
@patch('lambdas.get_event_by_id.fetch_event')
def test_get_event_by_id_fail_event_not_found(mock_fetch_event, event):
    """ Test get_event_by_id fails when event is not found """
    mock_fetch_event.return_value = None
    # Call the function
    event['arguments']['eventId'] = 'nonexistent'
    result = lambda_handler(event, {})
    # Check the result
    assert result['error'] == 'event not found'

#test fail scenario no event id provided
@patch('lambdas.get_event_by_id.fetch_event')
def test_get_event_by_id_fail_no_event_id(mock_fetch_event, event):
    """ Test get_event_by_id fails when no event id is provided """
    # Create the table
    mock_fetch_event.return_value = mock_trello_card()
    # Call the function
    del event['arguments']['eventId']
    result = lambda_handler(event, {})
    # Check the result is error message
    assert result['error'] == 'eventId must be a string and not empty'

#test fail scenario event id is not a string
@patch('lambdas.get_event_by_id.fetch_event')
def test_get_event_by_id_fail_event_id_not_string(mock_fetch_event, event):
    """Test get_event_by_id fails when event id is not a string"""
    # Create the table
    mock_fetch_event.return_value = mock_trello_card()
    # Call the function
    event['arguments']['eventId'] = 1
    result = lambda_handler(event, {})
    # Check the result is error message
    assert result['error'] == 'eventId must be a string and not empty'
