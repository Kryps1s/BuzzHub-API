"""unit tests for get_trello_members.py"""
from unittest.mock import patch
import pytest
from lambdas.get_trello_members import lambda_handler
from .utils import mock_trello_members

@pytest.fixture(name='event')
def fixture_event():
    """ Generates Appsync GraphQL Event"""
    return {
        "arguments": {
        }
    }

#test_get_trello_members.py
@patch('lambdas.get_trello_members.fetch_members')
def test_get_trello_members(mock_fetch_members, event):
    """ Test get_trello_members """
    #mock fetch_users
    mock_fetch_members.return_value = mock_trello_members()
    # Call the function
    result = lambda_handler(event, {})
    # Check the result
    assert result[0]['id'] == '5e6a57617b6a8f865837b846'
