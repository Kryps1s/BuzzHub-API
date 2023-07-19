"""Tests for create_users"""
from unittest.mock import patch
import pytest
from lambdas.create_user import lambda_handler

class TrelloAPIError(Exception):
    """Exception raised for errors in the Trello API"""

@pytest.fixture(name='event')
def fixture_event():
    """ Generates Appsync GraphQL Event"""
    return {
        "arguments": {
            "email": "elliot@test.com",
            "password": "Password!2",
            "code" : "test",
            "trello": "elliot",
            "firstName": "Elliot",
            "lastName": "Alderson"

        }
    }

@patch('lambdas.create_user.fetch_members')
@patch('lambdas.create_user.create_user')
def test_create_users(mock_create_user,mock_fetch_members, event):
    """ Test create_users """
    mock_create_user.return_value = "user created"
    mock_fetch_members.return_value = ["elliot"]
    result = lambda_handler(event, {})
    # Check the result
    assert result == 'user created'

#test for missing email
@patch('lambdas.create_user.fetch_members')
@patch('lambdas.create_user.create_user')
def test_create_users_fail_no_email(mock_create_user,mock_fetch_members, event):
    """ Test create_users fails when no email is provided """
    mock_create_user.return_value = "user created"
    mock_fetch_members.return_value = ["elliot"]
    del event['arguments']['email']
    with pytest.raises(ValueError) as err:
        lambda_handler(event, {})
    # Check the result
    assert str(err.value) == "Missing field"

    # Check the result

#test for invalid password
@patch('lambdas.create_user.fetch_members')
@patch('lambdas.create_user.create_user')
def test_create_users_fail_invalid_password(mock_create_user,mock_fetch_members, event):
    """ Test create_users fails when invalid password is provided """
    mock_create_user.return_value = "user created"
    mock_fetch_members.return_value = ["elliot"]
    event['arguments']['password'] = "Password"
    with pytest.raises(ValueError) as err:
        lambda_handler(event, {})
    # Check the result
    #pylint: disable=C0301
    assert str(err.value) == "Password must be at least 8 characters, and contain at least one number, one uppercase letter, and one lowercase letter, and one special character"

#test for invalid code
@patch('lambdas.create_user.fetch_members')
@patch('lambdas.create_user.create_user')
def test_create_users_fail_invalid_code(mock_create_user,mock_fetch_members, event):
    """ Test create_users fails when invalid code is provided """
    mock_create_user.return_value = "user created"
    mock_fetch_members.return_value = ["elliot"]
    event['arguments']['code'] = "test1"
    with pytest.raises(ValueError) as err:
        lambda_handler(event, {})
    # Check the result
    assert str(err.value) == "Invalid access code"

#test for invalid trello id
@patch('lambdas.create_user.fetch_members')
@patch('lambdas.create_user.create_user')
def test_create_users_fail_invalid_trello(mock_create_user,mock_fetch_members, event):
    """ Test create_users fails when invalid trello id is provided """
    mock_create_user.return_value = "user created"
    mock_fetch_members.return_value = ["elliot"]
    event['arguments']['trello'] = "elliot1"
    with pytest.raises(ValueError) as err:
        lambda_handler(event, {})
    # Check the result
    assert str(err.value) == "Invalid trello id"

#test for invalid first name
@patch('lambdas.create_user.fetch_members')
@patch('lambdas.create_user.create_user')
def test_create_users_fail_invalid_first_name(mock_create_user,mock_fetch_members, event):
    """ Test create_users fails when invalid first name is provided """
    mock_create_user.return_value = "user created"
    mock_fetch_members.return_value = ["elliot"]
    event['arguments']['firstName'] = "El"
    with pytest.raises(ValueError) as err:
        lambda_handler(event, {})
    # Check the result
    assert str(err.value) == "First and last name must be at least 3 characters"

#test for invalid last name
@patch('lambdas.create_user.fetch_members')
@patch('lambdas.create_user.create_user')
def test_create_users_fail_invalid_last_name(mock_create_user,mock_fetch_members, event):
    """ Test create_users fails when invalid last name is provided """
    mock_create_user.return_value = "user created"
    mock_fetch_members.return_value = ["elliot"]
    event['arguments']['lastName'] = "Al"
    with pytest.raises(ValueError) as err:
        lambda_handler(event, {})
    # Check the result
    assert str(err.value) == "First and last name must be at least 3 characters"

#test for invalid email
@patch('lambdas.create_user.fetch_members')
@patch('lambdas.create_user.create_user')
def test_create_users_fail_invalid_email(mock_create_user,mock_fetch_members, event):
    """ Test create_users fails when invalid email is provided """
    mock_create_user.return_value = "user created"
    mock_fetch_members.return_value = ["elliot"]
    event['arguments']['email'] = "elliot@test"
    with pytest.raises(ValueError) as err:
        lambda_handler(event, {})
    # Check the result
    assert str(err.value) == "Invalid email"
