"""
Test suite for the model representing a user [without the auditing columns] (api/src/model/UserData.py)
Author: Andrew Jarombek
Date: 12/10/2019
"""

from datetime import datetime
from tests.TestSuite import TestSuite
from tests.test_src.test_model.testUser import TestUser
from model.User import User
from model.UserData import UserData


class TestUserData(TestSuite):
    user1 = UserData(TestUser.user1)
    user1copy = UserData(TestUser.user1copy)
    user2 = UserData(TestUser.user2)

    def test_user_str(self) -> None:
        """
        Prove that the human readable string representation of a UserData object is as expected.
        """
        log_str = 'UserData: [username: andy, first: Andy, last: Jarombek, salt: None, ' \
                  'password: hashed_and_salted_password, profilepic_name: None, ' \
                  "description: Andy's Profile, member_since: 2016-12-23 00:00:00, class_year: 2017, " \
                  'location: Riverside, CT, favorite_event: 8K, 5000m, activation_code: ABC123, ' \
                  'email: andrew@jarombek.com, subscribed: 1, last_signin: 2019-12-10 00:00:00, week_start: monday, ' \
                  'deleted: None]'

        self.maxDiff = None
        self.assertEquals(str(self.user1), log_str)
        self.assertEquals(self.user1.__str__(), log_str)

    def test_user_repr(self) -> None:
        """
        Prove that the machine readable string representation of a UserData object is as expected.
        """
        self.assertEquals(repr(self.user1), "<UserData 'andy'>")
        self.assertEquals(self.user1.__repr__(), "<UserData 'andy'>")

    def test_user_eq(self) -> None:
        """
        Prove that two UserData objects with the same property values test positive for value equality.
        """
        self.assertTrue(self.user1 == self.user1copy)
        self.assertTrue(self.user1.__eq__(self.user1copy))

    def test_user_ne(self) -> None:
        """
        Prove that two UserData objects with different property values test negative for value equality.
        """
        self.assertTrue(self.user1 != self.user2)
        self.assertTrue(self.user1.__ne__(self.user2))
