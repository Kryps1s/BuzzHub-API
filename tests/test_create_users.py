"""Tests for create_users"""
from unittest.mock import patch
import pytest
from lambdas.create_user import lambda_handler


@pytest.fixture(name='event')
def fixture_event():
    """ Generates Appsync GraphQL Event"""
    return {
        "arguments": {
            "email": "elliot@test.com",
            "password": "Password!2",
            "code" : "test",
            "trello": "elliot",
            "first_name": "Elliot",
            "last_name": "Alderson"

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
    result = lambda_handler(event, {})
    # Check the result
    assert result['error'] == 'Missing field'

#test for invalid password
@patch('lambdas.create_user.fetch_members')
@patch('lambdas.create_user.create_user')
def test_create_users_fail_invalid_password(mock_create_user,mock_fetch_members, event):
    """ Test create_users fails when invalid password is provided """
    mock_create_user.return_value = "user created"
    mock_fetch_members.return_value = ["elliot"]
    event['arguments']['password'] = "Password"
    result = lambda_handler(event, {})
    # Check the result
    #pylint: disable=line-too-long
    assert result['error'] == 'Password must be at least 8 characters, and contain at least one number, one uppercase letter, and one lowercase letter, and one special character'

#test for invalid code
@patch('lambdas.create_user.fetch_members')
@patch('lambdas.create_user.create_user')
def test_create_users_fail_invalid_code(mock_create_user,mock_fetch_members, event):
    """ Test create_users fails when invalid code is provided """
    mock_create_user.return_value = "user created"
    mock_fetch_members.return_value = ["elliot"]
    event['arguments']['code'] = "test1"
    result = lambda_handler(event, {})
    # Check the result
    assert result['error'] == 'Invalid access code'

#test for invalid trello id
@patch('lambdas.create_user.fetch_members')
@patch('lambdas.create_user.create_user')
def test_create_users_fail_invalid_trello(mock_create_user,mock_fetch_members, event):
    """ Test create_users fails when invalid trello id is provided """
    mock_create_user.return_value = "user created"
    mock_fetch_members.return_value = ["elliot"]
    event['arguments']['trello'] = "elliot1"
    result = lambda_handler(event, {})
    # Check the result
    assert result['error'] == 'Invalid trello id'

#test for invalid first name
@patch('lambdas.create_user.fetch_members')
@patch('lambdas.create_user.create_user')
def test_create_users_fail_invalid_first_name(mock_create_user,mock_fetch_members, event):
    """ Test create_users fails when invalid first name is provided """
    mock_create_user.return_value = "user created"
    mock_fetch_members.return_value = ["elliot"]
    event['arguments']['first_name'] = "El"
    result = lambda_handler(event, {})
    # Check the result
    assert result['error'] == 'First and last name must be at least 3 characters'

#test for invalid last name
@patch('lambdas.create_user.fetch_members')
@patch('lambdas.create_user.create_user')
def test_create_users_fail_invalid_last_name(mock_create_user,mock_fetch_members, event):
    """ Test create_users fails when invalid last name is provided """
    mock_create_user.return_value = "user created"
    mock_fetch_members.return_value = ["elliot"]
    event['arguments']['last_name'] = "Al"
    result = lambda_handler(event, {})
    # Check the result
    assert result['error'] == 'First and last name must be at least 3 characters'

#test for invalid email
@patch('lambdas.create_user.fetch_members')
@patch('lambdas.create_user.create_user')
def test_create_users_fail_invalid_email(mock_create_user,mock_fetch_members, event):
    """ Test create_users fails when invalid email is provided """
    mock_create_user.return_value = "user created"
    mock_fetch_members.return_value = ["elliot"]
    event['arguments']['email'] = "elliot@test"
    result = lambda_handler(event, {})
    # Check the result
    assert result['error'] == 'Invalid email'
