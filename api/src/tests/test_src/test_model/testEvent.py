"""
Test suite for the model representing comments on exercise logs (api/src/model/Comment.py)
Author: Andrew Jarombek
Date: 11/9/2019
"""

from datetime import datetime
from tests.TestSuite import TestSuite
from model.Event import Event


class TestEvent(TestSuite):
    event1 = Event({
        'event_id': 1,
        'name': 'Test Event',
        'group_name': 'wmensxc',
        'start_date': datetime.fromisoformat('2019-11-09').date(),
        'end_date': None,
        'start_time': None,
        'end_time': None,
        'description': 'Test Event',
        'deleted': False
    })

    event2 = Event({
        'event_id': 2,
        'name': 'Another Test Event',
        'group_name': 'wmenstf',
        'start_date': datetime.fromisoformat('2019-11-10').date(),
        'end_date': None,
        'start_time': None,
        'end_time': None,
        'description': 'Another Test Event',
        'deleted': False
    })

    def test_event_str(self) -> None:
        """
        Prove that the human readable string representation of an Comment object is as expected.
        """
        self.assertEquals(
            str(self.event1),
            'Event: [event_id: 1, name: Test Event, group_name: wmensxc, start_date: 2019-11-09, '
            'end_date: None, start_time: None, end_time: None, description: Test Event, deleted: False]'
        )
        self.assertEquals(
            self.event1.__str__(),
            'Event: [event_id: 1, name: Test Event, group_name: wmensxc, start_date: 2019-11-09, '
            'end_date: None, start_time: None, end_time: None, description: Test Event, deleted: False]'
        )

    def test_event_repr(self) -> None:
        """
        Prove that the machine readable string representation of an Event object is as expected.
        """
        self.assertEquals(repr(self.event1), "<Event 'Test Event'>")
        self.assertEquals(self.event1.__repr__(), "<Event 'Test Event'>")

    def test_event_eq(self) -> None:
        """
        Prove that two Event objects with the same property values test positive for value equality.
        """
        self.assertTrue(self.event1 == self.event1)
        self.assertTrue(self.event1.__eq__(self.event1))

    def test_event_ne(self) -> None:
        """
        Prove that two Event objects with different property values test negative for value equality.
        """
        self.assertTrue(self.event1 != self.event2)
        self.assertTrue(self.event1.__ne__(self.event2))
