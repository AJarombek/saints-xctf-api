"""
Test suite for the model representing a notification for a user (api/src/model/Notification.py)
Author: Andrew Jarombek
Date: 11/30/2019
"""

from datetime import datetime
from tests.TestSuite import TestSuite
from model.Notification import Notification


class TestNotification(TestSuite):
    notification1_dict = {
        "notification_id": 1,
        "username": "andy",
        "time": datetime.fromisoformat("2019-12-31"),
        "link": None,
        "viewed": "N",
        "description": "Hopefully nobody is being mean to you.  I hope you know + believe that you deserve to be "
        "treated with kindness.",
        "deleted": False,
    }

    notification2_dict = {
        "notification_id": 2,
        "username": "andy",
        "time": datetime.fromisoformat("2019-11-30"),
        "link": None,
        "viewed": "N",
        "description": "Today was the first day selling XMas trees.  We set up the stands yesterday.  Tomorrow might "
        "be rough in the rain/snow.",
        "deleted": False,
    }

    notification1 = Notification(notification1_dict)
    notification1copy = Notification(notification1_dict)

    notification2 = Notification(notification2_dict)

    def test_notification_str(self) -> None:
        """
        Prove that the human-readable string representation of a Notification object is as expected.
        """
        log_str = (
            "Notification: [notification_id: 1, username: andy, time: 2019-12-31 00:00:00, link: None, "
            "viewed: N, description: Hopefully nobody is being mean to you.  I hope you know + believe that you "
            "deserve to be treated with kindness., deleted: False]"
        )

        self.maxDiff = None
        self.assertEqual(str(self.notification1), log_str)

        # pylint: disable=unnecessary-dunder-call
        self.assertEqual(self.notification1.__str__(), log_str)

    def test_notification_repr(self) -> None:
        """
        Prove that the machine-readable string representation of a Notification object is as expected.
        """
        self.assertEqual(repr(self.notification1), "<Notification 1>")

        # pylint: disable=unnecessary-dunder-call
        self.assertEqual(self.notification1.__repr__(), "<Notification 1>")

    def test_notification_eq(self) -> None:
        """
        Prove that two Notification objects with the same property values test positive for value equality.
        """
        self.assertTrue(self.notification1 == self.notification1copy)

        # pylint: disable=unnecessary-dunder-call
        self.assertTrue(self.notification1.__eq__(self.notification1copy))

    def test_notification_ne(self) -> None:
        """
        Prove that two Notification objects with different property values test negative for value equality.
        """
        self.assertTrue(self.notification1 != self.notification2)

        # pylint: disable=unnecessary-dunder-call
        self.assertTrue(self.notification1.__ne__(self.notification2))
