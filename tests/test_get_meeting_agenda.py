"""get the agenda for the weekly meeting"""
import os
import requests
import json
from unittest.mock import patch
import pytest 
from lambdas.get_meeting_agenda import lambda_handler

@pytest.fixture
def event():
    """generate event"""
    return {
        "arguments": {}
    }

#test get agenda
