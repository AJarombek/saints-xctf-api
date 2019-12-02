"""
Test suite for the model representing a notification for a user [without the auditing columns]
(api/src/model/NotificationData.py)
Author: Andrew Jarombek
Date: 12/1/2019
"""

from datetime import datetime
from tests.TestSuite import TestSuite
from model.Notification import Notification
from model.NotificationData import NotificationData


class TestNotificationData(TestSuite):
    notification1_dict = {
        'notification_id': 3,
        'username': "andy",
        'time': datetime.fromisoformat('2019-12-01'),
        'link': None,
        'viewed': "N",
        'description': "Wet and cold but good day selling Christmas trees.",
        'deleted': False
    }

    notification2_dict = {
        'notification_id': 4,
        'username': "andy",
        'time': datetime.fromisoformat('2019-12-01'),
        'link': None,
        'viewed': "N",
        'description': "Now need sleep and Dotty the horse snuggle time :).",
        'deleted': False
    }

    notification1 = NotificationData(Notification(notification1_dict))
    notification1copy = NotificationData(Notification(notification1_dict))

    notification2 = NotificationData(Notification(notification2_dict))

    def test_notification_data_str(self) -> None:
        """
        Prove that the human readable string representation of a NotificationData object is as expected.
        """
        log_str = 'NotificationData: [notification_id: 3, username: andy, time: 2019-12-01 00:00:00, link: None, ' \
            'viewed: N, description: Wet and cold but good day selling Christmas trees., deleted: False]'

        self.maxDiff = None
        self.assertEquals(str(self.notification1), log_str)
        self.assertEquals(self.notification1.__str__(), log_str)

    def test_notification_data_repr(self) -> None:
        """
        Prove that the machine readable string representation of a NotificationData object is as expected.
        """
        self.assertEquals(repr(self.notification1), "<NotificationData 3>")
        self.assertEquals(self.notification1.__repr__(), "<NotificationData 3>")

    def test_notification_data_eq(self) -> None:
        """
        Prove that two NotificationData objects with the same property values test positive for value equality.
        """
        self.assertTrue(self.notification1 == self.notification1copy)
        self.assertTrue(self.notification1.__eq__(self.notification1copy))

    def test_notification_data_ne(self) -> None:
        """
        Prove that two NotificationData objects with different property values test negative for value equality.
        """
        self.assertTrue(self.notification1 != self.notification2)
        self.assertTrue(self.notification1.__ne__(self.notification2))
