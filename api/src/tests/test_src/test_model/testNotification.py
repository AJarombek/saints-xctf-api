"""
Test suite for the model representing a notification for a user (api/src/model/Notification.py)
Author: Andrew Jarombek
Date: 11/30/2019
"""

from datetime import datetime
from tests.TestSuite import TestSuite
from model.Message import Message


class TestNotification(TestSuite):
    notification1_dict = {
        'notification_id': 1,
        'username': "andy",
        'time': datetime.fromisoformat('2019-12-31'),
        'link': None,
        'viewed': "N",
        'content': "Hopefully nobody is being mean to you.  I hope you know + believe that you deserve to be treated "
                   "with kindness.",
        'deleted': False
    }

    notification2_dict = {
        'notification_id': 2,
        'username': "andy",
        'time': datetime.fromisoformat('2019-11-30'),
        'link': None,
        'viewed': "N",
        'content': "Today was the first day selling XMas trees.  We set up the stands yesterday.  Tomorrow might be "
                   "rough in the rain/snow.",
        'deleted': False
    }

    message1 = Message(notification1_dict)
    message1copy = Message(notification1_dict)

    message2 = Message(notification2_dict)