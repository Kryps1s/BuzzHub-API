"""Test get_meeting_agenda function in lambda_handler.py"""
import os
from unittest.mock import patch
import pytest
from lambdas.get_meeting_agenda import lambda_handler
from .utils import mock_beekeeping_board, mock_collective_board

@pytest.fixture(name='event')
def fixture_event():
    """ Generates Appsync GraphQL Event"""
    return {
        "arguments": {}
    }

#test gets meeting agenda
@patch('lambdas.get_meeting_agenda.get_trello_board')
def test_get_meeting_agenda(mock_get_trello_board, event):
    """get meeting agenda"""
    #mock get_meeting_agenda
    def side_effect(board_id):
        if board_id == os.environ['TRELLO_BOARD_BEEKEEPING']:
            return mock_beekeeping_board()
        if board_id == os.environ['TRELLO_BOARD_COLLECTIVE']:
            return mock_collective_board()
        raise ValueError("Board must be BEEKEEPING or COLLECTIVE")
    mock_get_trello_board.side_effect = side_effect
    #call lambda_handler
    test = lambda_handler(event, {})
    #assert length of all values in test is equal to length of mock boards
    testlengeth = len(test['BEEKEEPING']['unassigned']) +\
                  len(test['BEEKEEPING']['inProgress']) +\
                  len(test['BEEKEEPING']['completed']) +\
                  len(test['COLLECTIVE']['unassigned']) +\
                  len(test['COLLECTIVE']['inProgress']) +\
                  len(test['COLLECTIVE']['completed'])
    assert testlengeth == len(mock_beekeeping_board()) + len(mock_collective_board())

#test get_meeting_agenda raises error if trello api call fails
@patch('lambdas.get_meeting_agenda.get_trello_board')
def test_get_meeting_agenda_error(mock_get_board, event):
    """get meeting agenda raises error if trello api call fails"""
    #mock get_trello_board
    mock_get_board.side_effect = ValueError("Trello API error")
    #assert get_meeting_agenda raises error
    with pytest.raises(ValueError) as error:
        lambda_handler(event, {})
    #assert error message is correct
    assert str(error.value) == "Trello API error"

#test get_meeting_agenda raises error if board is not BEEKEEPING or COLLECTIVE
@patch('lambdas.get_meeting_agenda.get_trello_board')
def test_get_meeting_agenda_error_board(mock_get_board, event):
    """get meeting agenda raises error if board is not BEEKEEPING or COLLECTIVE"""
    #mock get_trello_board
    mock_get_board.side_effect = ValueError("Board must be BEEKEEPING or COLLECTIVE")
    #assert get_meeting_agenda raises error
    with pytest.raises(ValueError) as error:
        lambda_handler(event, {})
    #assert error message is correct
    assert str(error.value) == "Board must be BEEKEEPING or COLLECTIVE"

#test get_meeting_agenda runs when event list is empty
@patch('lambdas.get_meeting_agenda.get_trello_board')
def test_get_meeting_agenda_empty_event(mock_get_board, event):
    """get meeting agenda runs when event list is empty"""
    #mock get_trello_board
    def side_effect(board_id):
        if board_id == os.environ['TRELLO_BOARD_BEEKEEPING']:
            return []
        elif board_id == os.environ['TRELLO_BOARD_COLLECTIVE']:
            return []
    mock_get_board.side_effect = side_effect
    #call lambda_handler
    test = lambda_handler(event, {})
    #assert length of all values is equal to 0
    testlengeth = len(test['BEEKEEPING']['unassigned']) +\
                  len(test['BEEKEEPING']['inProgress']) +\
                  len(test['BEEKEEPING']['completed']) +\
                  len(test['COLLECTIVE']['unassigned']) +\
                  len(test['COLLECTIVE']['inProgress']) +\
                  len(test['COLLECTIVE']['completed'])
    assert testlengeth == 0
