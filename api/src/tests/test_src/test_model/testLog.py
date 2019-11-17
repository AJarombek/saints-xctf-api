"""
Test suite for the model representing exercise logs (api/src/model/Log.py)
Author: Andrew Jarombek
Date: 11/17/2019
"""

from datetime import datetime
from tests.TestSuite import TestSuite
from model.Log import Log


class TestLog(TestSuite):
    log1_dict = {
        'log_id': 1,
        'username': "andy",
        'first': "Andrew",
        'last': "Jarombek",
        'name': 'Van Cortlandt NYRR XC 5K',
        'location': 'Bronx, NY',
        'date': datetime.fromisoformat('2019-11-17'),
        'type': 'run',
        'distance': 5,
        'metric': 'kilometers',
        'miles': 3.11,
        'time': '17:35',
        'pace': '5:40',
        'feel': 5,
        'description': "Didn't run very fast and felt tired, but it was nice to run a cross country race again.",
        'time_created': datetime.fromisoformat('2019-11-17'),
    }

    log1 = Log(log1_dict)
    log1copy = Log(log1_dict)

    log2 = Log({
        'log_id': 2,
        'username': "andy",
        'first': "Andrew",
        'last': "Jarombek",
        'name': 'Cooldown',
        'location': 'Bronx, NY',
        'date': datetime.fromisoformat('2019-11-17'),
        'type': 'run',
        'distance': 1.75,
        'metric': 'miles',
        'miles': 1.75,
        'time': '12:31',
        'pace': '7:09',
        'feel': 5,
        'description': "I hope you are doing well and had a fun weekend.",
        'time_created': datetime.now(),
    })

    def test_log_str(self) -> None:
        """
        Prove that the human readable string representation of a Log object is as expected.
        """
        group_str = 'Log: [log_id: 1, username: andy, first: Andrew, last: Jarombek, ' \
            'name: Van Cortlandt NYRR XC 5K, location: Bronx, NY, date: 2019-11-17 00:00:00, type: run ' \
            'distance: 5, metric: kilometers, miles: 3.11, time: 12:31, ' \
            "pace: 7:09, feel: 5, " \
            "description: Didn't run very fast and felt tired, but it was nice to run a cross country race again., " \
            "time_created: , deleted: 2019-11-17 00:00:00]"

        self.assertEquals(str(self.log1), group_str)
        self.assertEquals(self.log1.__str__(), group_str)

    def test_log_repr(self) -> None:
        """
        Prove that the machine readable string representation of a Log object is as expected.
        """
        self.assertEquals(repr(self.log1), "<Log 1>")
        self.assertEquals(self.log1.__repr__(), "<Log 1>")

    def test_log_eq(self) -> None:
        """
        Prove that two Log objects with the same property values test positive for value equality.
        """
        self.assertTrue(self.log1 == self.log1)
        self.assertTrue(self.log1.__eq__(self.log1))

    def test_log_ne(self) -> None:
        """
        Prove that two Log objects with different property values test negative for value equality.
        """
        self.assertTrue(self.log1 != self.log2)
        self.assertTrue(self.log1.__ne__(self.log2))
