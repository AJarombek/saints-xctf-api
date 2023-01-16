"""
Test suite for the model representing a user's forgot password code (api/src/model/ForgotPassword.py)
Author: Andrew Jarombek
Date: 11/9/2019
"""

from datetime import datetime
from tests.TestSuite import TestSuite
from model.ForgotPassword import ForgotPassword


class TestForgotPassword(TestSuite):
    forgot_password1 = ForgotPassword(
        {
            "forgot_code": "123ABC",
            "username": "andy",
            "expires": datetime.fromisoformat("2019-11-10 00:00:00"),
            "deleted": False,
        }
    )

    forgot_password2 = ForgotPassword(
        {
            "forgot_code": "456DEF",
            "username": "andy",
            "expires": datetime.fromisoformat("2019-11-10 02:00:00"),
            "deleted": False,
        }
    )

    def test_forgot_password_str(self) -> None:
        """
        Prove that the human-readable string representation of a ForgotPassword object is as expected.
        """
        self.assertEqual(
            str(self.forgot_password1),
            "ForgotPassword: [forgot_code: 123ABC, username: andy, expires: 2019-11-10 00:00:00, deleted: False]",
        )

        # pylint: disable=unnecessary-dunder-call
        self.assertEqual(
            self.forgot_password1.__str__(),
            "ForgotPassword: [forgot_code: 123ABC, username: andy, expires: 2019-11-10 00:00:00, deleted: False]",
        )

    def test_forgot_password_repr(self) -> None:
        """
        Prove that the machine-readable string representation of a ForgotPassword object is as expected.
        """
        self.assertEqual(
            repr(self.forgot_password1), "<ForgotPassword '123ABC','andy'>"
        )

        # pylint: disable=unnecessary-dunder-call
        self.assertEqual(
            self.forgot_password1.__repr__(), "<ForgotPassword '123ABC','andy'>"
        )

    def test_forgot_password_eq(self) -> None:
        """
        Prove that two ForgotPassword objects with the same property values test positive for value equality.
        """
        self.assertTrue(self.forgot_password1 == self.forgot_password1)

        # pylint: disable=unnecessary-dunder-call
        self.assertTrue(self.forgot_password1.__eq__(self.forgot_password1))

    def test_forgot_password_ne(self) -> None:
        """
        Prove that two ForgotPassword objects with different property values test negative for value equality.
        """
        self.assertTrue(self.forgot_password1 != self.forgot_password2)

        # pylint: disable=unnecessary-dunder-call
        self.assertTrue(self.forgot_password1.__ne__(self.forgot_password2))
