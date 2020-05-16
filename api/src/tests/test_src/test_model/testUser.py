"""
Test suite for the model representing a user (api/src/model/User.py)
Author: Andrew Jarombek
Date: 12/9/2019
"""

from datetime import datetime
from tests.TestSuite import TestSuite
from model.User import User


class TestUser(TestSuite):
    user1_dict = {
        'username': "andy",
        'first': 'Andy',
        'last': 'Jarombek',
        'salt': None,
        'password': 'hashed_and_salted_password',
        'profilepic': None,
        'profilepic_name': None,
        'description': "Andy's Profile",
        'member_since': datetime.fromisoformat('2016-12-23'),
        'class_year': 2017,
        'location': 'Riverside, CT',
        'favorite_event': '8K, 5000m',
        'activation_code': 'ABC123',
        'email': 'andrew@jarombek.com',
        'subscribed': 1,
        'last_signin': datetime.fromisoformat('2019-12-10'),
        'week_start': 'monday',
        'deleted': False
    }

    user2_dict = {
        'username': "andy2",
        'first': 'Andrew',
        'last': 'Jarombek',
        'salt': None,
        'password': 'hashed_and_salted_password',
        'profilepic': None,
        'profilepic_name': None,
        'description': None,
        'member_since': datetime.fromisoformat('2019-12-10'),
        'class_year': 2017,
        'location': None,
        'favorite_event': None,
        'activation_code': 'DEF456',
        'email': 'andrew@jarombek.com',
        'subscribed': None,
        'last_signin': datetime.now(),
        'week_start': None,
        'deleted': False
    }

    user1 = User(user1_dict)
    user1copy = User(user1_dict)
    user2 = User(user2_dict)

    def test_user_str(self) -> None:
        """
        Prove that the human readable string representation of a User object is as expected.
        """
        log_str = 'User: [username: andy, first: Andy, last: Jarombek, salt: None, ' \
                  'password: hashed_and_salted_password, ' \
                  "description: Andy's Profile, member_since: 2016-12-23 00:00:00, class_year: 2017, " \
                  'location: Riverside, CT, favorite_event: 8K, 5000m, activation_code: ABC123, ' \
                  'email: andrew@jarombek.com, subscribed: 1, last_signin: 2019-12-10 00:00:00, week_start: monday, ' \
                  'deleted: None]'

        self.maxDiff = None
        self.assertEquals(str(self.user1), log_str)
        self.assertEquals(self.user1.__str__(), log_str)

    def test_user_repr(self) -> None:
        """
        Prove that the machine readable string representation of a User object is as expected.
        """
        self.assertEquals(repr(self.user1), "<User 'andy'>")
        self.assertEquals(self.user1.__repr__(), "<User 'andy'>")

    def test_user_eq(self) -> None:
        """
        Prove that two User objects with the same property values test positive for value equality.
        """
        self.assertTrue(self.user1 == self.user1copy)
        self.assertTrue(self.user1.__eq__(self.user1copy))

    def test_user_ne(self) -> None:
        """
        Prove that two User objects with different property values test negative for value equality.
        """
        self.assertTrue(self.user1 != self.user2)
        self.assertTrue(self.user1.__ne__(self.user2))
