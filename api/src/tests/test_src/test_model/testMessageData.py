"""
Test suite for the model representing group/team messages [without the auditing columns] (api/src/model/MessageData.py)
Author: Andrew Jarombek
Date: 11/25/2019
"""

from datetime import datetime
from tests.TestSuite import TestSuite
from model.Message import Message
from model.MessageData import MessageData


class TestMessageData(TestSuite):
    message1_dict = {
        'message_id': 3,
        'username': "andy",
        'first': "Andrew",
        'last': "Jarombek",
        'group_name': 'alumni',
        'time': datetime.fromisoformat('2019-11-25'),
        'content': "Test Message 1",
        'deleted': None
    }

    message2_dict = {
        'message_id': 4,
        'username': "andy",
        'first': "Andrew",
        'last': "Jarombek",
        'group_name': 'alumni',
        'time': datetime.fromisoformat('2019-11-25'),
        'content': "Test Message 2",
        'deleted': True
    }

    message1 = MessageData(Message(message1_dict))
    message1copy = MessageData(Message(message1_dict))

    message2 = MessageData(Message(message2_dict))

    def test_message_data_str(self) -> None:
        """
        Prove that the human readable string representation of a MessageData object is as expected.
        """
        log_str = 'MessageData: [message_id: 3, username: andy, first: Andrew, last: Jarombek, ' \
            "group_name: alumni, time: 2019-11-25 00:00:00, content: Test Message 1, deleted: None]"

        self.maxDiff = None
        self.assertEquals(str(self.message1), log_str)
        self.assertEquals(self.message1.__str__(), log_str)

    def test_message_data_repr(self) -> None:
        """
        Prove that the machine readable string representation of a MessageData object is as expected.
        """
        self.assertEquals(repr(self.message1), "<MessageData 3>")
        self.assertEquals(self.message1.__repr__(), "<MessageData 3>")

    def test_message_data_eq(self) -> None:
        """
        Prove that two MessageData objects with the same property values test positive for value equality.
        """
        self.assertTrue(self.message1 == self.message1copy)
        self.assertTrue(self.message1.__eq__(self.message1copy))

    def test_message_data_ne(self) -> None:
        """
        Prove that two MessageData objects with different property values test negative for value equality.
        """
        self.assertTrue(self.message1 != self.message2)
        self.assertTrue(self.message1.__ne__(self.message2))
