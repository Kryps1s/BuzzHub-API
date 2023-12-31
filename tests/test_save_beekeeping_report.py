""" Tests for save_beekeeping_report """
from unittest.mock import patch
import pytest
from lambdas.save_beekeeping_report import lambda_handler
from .utils import mock_trello_card

@pytest.fixture(name='event')
def fixture_event():
    """ Generates Appsync GraphQL Event"""
    return {
        "arguments": {
            "eventId": "oBsiLWUX",
            "report": "This is a test report",
            "participants": ["5f1c7b8d0b4a5e7e1a4c1b6d"],
            "nextInspection" : None
        }
    }

#test_save_beekeeping_report.py
@patch('lambdas.save_beekeeping_report.fetch_card')
@patch('lambdas.save_beekeeping_report.update_card')
def test_save_beekeeping_report(mock_update_card,mock_fetch_card, event):
    """ Test fetch_card """
    mock_fetch_card.return_value = mock_trello_card()
    mock_update_card.return_value = mock_trello_card()
    message = lambda_handler(event,{})
    # Check the result
    assert message == {'message': 'successfully saved report'}

#test for missing eventId
@patch('lambdas.save_beekeeping_report.fetch_card')
@patch('lambdas.save_beekeeping_report.update_card')
def test_save_beekeeping_report_fail_no_card_id(mock_update_card,mock_fetch_card, event):
    """ Test fetch_card """
    mock_fetch_card.return_value = mock_trello_card()
    mock_update_card.return_value = mock_trello_card()
    del event['arguments']['eventId']
    with pytest.raises(ValueError) as err:
        lambda_handler(event,{})
    # Check the result contains missing field
    assert str(err.value) == "missing field: 'eventId'"

#test for missing report
@patch('lambdas.save_beekeeping_report.fetch_card')
@patch('lambdas.save_beekeeping_report.update_card')
def test_save_beekeeping_report_fail_no_report(mock_update_card,mock_fetch_card, event):
    """ Test fetch_card """
    mock_fetch_card.return_value = mock_trello_card()
    mock_update_card.return_value = mock_trello_card()
    del event['arguments']['report']
    with pytest.raises(ValueError) as err:
        lambda_handler(event,{})
    # Check the result
    assert str(err.value) == "missing field: 'report'"

#test for missing participants
@patch('lambdas.save_beekeeping_report.fetch_card')
@patch('lambdas.save_beekeeping_report.update_card')
def test_save_beekeeping_report_fail_no_participants(mock_update_card,mock_fetch_card, event):
    """ Test fetch_card """
    mock_fetch_card.return_value = mock_trello_card()
    mock_update_card.return_value = mock_trello_card()
    del event['arguments']['participants']
    with pytest.raises(ValueError) as err:
        lambda_handler(event,{})
    # Check the result
    assert str(err.value) == "missing field: 'participants'"

#test for invalid report
@patch('lambdas.save_beekeeping_report.fetch_card')
@patch('lambdas.save_beekeeping_report.update_card')
def test_save_beekeeping_report_fail_invalid_report(mock_update_card,mock_fetch_card, event):
    """ Test fetch_card """
    mock_fetch_card.return_value = mock_trello_card()
    mock_update_card.return_value = mock_trello_card()
    event['arguments']['report'] = 11
    with pytest.raises(ValueError) as err:
        lambda_handler(event,{})
    # Check the result
    assert str(err.value) == "invalid report"

#test for empty participants
@patch('lambdas.save_beekeeping_report.fetch_card')
@patch('lambdas.save_beekeeping_report.update_card')
def test_save_beekeeping_report_fail_empty_participants(mock_update_card,mock_fetch_card, event):
    """ Test fetch_card """
    mock_fetch_card.return_value = mock_trello_card()
    mock_update_card.return_value = mock_trello_card()
    event['arguments']['participants'] = []
    with pytest.raises(ValueError) as err:
        lambda_handler(event,{})
    # Check the result
    assert str(err.value) == "there must be at least one attendee"

#test for invalid participants (not a list)
@patch('lambdas.save_beekeeping_report.fetch_card')
@patch('lambdas.save_beekeeping_report.update_card')
def test_save_beekeeping_report_fail_invalid_participants(mock_update_card,mock_fetch_card, event):
    """ Test fetch_card """
    mock_fetch_card.return_value = mock_trello_card()
    mock_update_card.return_value = mock_trello_card()
    #participant index are objects
    event['arguments']['participants'] = [{"id": "5f1c7b8d", "name": "John Doe", "email": ""}]
    with pytest.raises(ValueError) as err:
        lambda_handler(event,{})
    # Check the result
    assert str(err.value) == "invalid participants"

#test for invalid eventId
def test_save_beekeeping_report_fail_invalid_card(event):
    """ Test fetch_card """
    event['arguments']['eventId'] = "invalidId"
    with pytest.raises(ValueError) as err:
        lambda_handler(event,{})
    # Check the result value contains Trello API error
    assert "Trello API error" in str(err.value)

#test create next inspection card
@patch('lambdas.save_beekeeping_report.fetch_card')
@patch('lambdas.save_beekeeping_report.update_card')
@patch('lambdas.save_beekeeping_report.create_next_inspection')
def test_save_beekeeping_report_create_next_inspection(
    mock_update_card,mock_fetch_card,mock_create_card, event):
    """ Test fetch_card """
    event["arguments"]["nextInspection"] = "2054-08-01"
    event["arguments"]["goal"] = "This is a test goal"
    event["arguments"]["full"] = True
    mock_fetch_card.return_value = mock_trello_card()
    mock_update_card.return_value = mock_trello_card()
    mock_create_card.return_value = mock_trello_card()
    event['arguments']['report'] = "This is a test report. Next inspection: 2020-08-01"
    message = lambda_handler(event,{})
    # Check the result
    assert message == {'message': 'successfully saved report and created next inspection'}

#test create next inspection card with invalid date
@patch('lambdas.save_beekeeping_report.fetch_card')
@patch('lambdas.save_beekeeping_report.update_card')
@patch('lambdas.save_beekeeping_report.create_next_inspection')
def test_save_beekeeping_report_create_next_inspection_invalid_date(
    mock_update_card,mock_fetch_card,mock_create_card, event):
    """ Test fetch_card """
    event["arguments"]["nextInspection"] = "2020-08-01"
    event["arguments"]["goal"] = "This is a test goal"
    event["arguments"]["full"] = True
    mock_fetch_card.return_value = mock_trello_card()
    mock_update_card.return_value = mock_trello_card()
    mock_create_card.return_value = mock_trello_card()
    event['arguments']['report'] = "This is a test report. Next inspection: 2020-08-01"
    #invalid date
    event['arguments']['nextInspection'] = "2020-08-01"
    with pytest.raises(ValueError) as err:
        lambda_handler(event,{})
    # Check the result
    assert str(err.value) == "next inspection date must be greater than today"
