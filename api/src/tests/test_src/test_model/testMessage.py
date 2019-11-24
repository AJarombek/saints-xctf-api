"""
Test suite for the model representing group/team messages (api/src/model/Message.py)
Author: Andrew Jarombek
Date: 11/24/2019
"""

from datetime import datetime
from tests.TestSuite import TestSuite
from model.Message import Message


class TestMessage(TestSuite):
    message1_dict = {
        'message_id': 1,
        'username': "andy",
        'first': "Andrew",
        'last': "Jarombek",
        'group_name': 'alumni',
        'time': datetime.fromisoformat('2019-12-31'),
        'content': "If you find this, I hope you know that you mean the world to me.",
        'deleted': False
    }

    message2_dict = {
        'message_id': 2,
        'username': "andy",
        'first': "Andrew",
        'last': "Jarombek",
        'group_name': 'alumni',
        'time': datetime.fromisoformat('2019-12-31'),
        'content': "Missing your laugh on rainy days like this.",
        'deleted': False
    }

    message1 = Message(message1_dict)
    message1copy = Message(message1_dict)

    message2 = Message(message2_dict)

    def test_message_str(self) -> None:
        """
        Prove that the human readable string representation of a Message object is as expected.
        """
        log_str = 'Message: [message_id: 1, username: andy, first: Andrew, last: Jarombek, ' \
            "group_name: alumni, time: 2019-12-31 00:00:00, " \
            "content: If you find this, I hope you know that you mean the world to me., deleted: False]"

        self.maxDiff = None
        self.assertEquals(str(self.message1), log_str)
        self.assertEquals(self.message1.__str__(), log_str)

    def test_message_repr(self) -> None:
        """
        Prove that the machine readable string representation of a Message object is as expected.
        """
        self.assertEquals(repr(self.message1), "<Message 1>")
        self.assertEquals(self.message1.__repr__(), "<Message 1>")

    def test_message_eq(self) -> None:
        """
        Prove that two Message objects with the same property values test positive for value equality.
        """
        self.assertTrue(self.message1 == self.message1copy)
        self.assertTrue(self.message1.__eq__(self.message1copy))

    def test_message_ne(self) -> None:
        """
        Prove that two Message objects with different property values test negative for value equality.
        """
        self.assertTrue(self.message1 != self.message2)
        self.assertTrue(self.message1.__ne__(self.message2))
