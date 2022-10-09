"""
Test suite for the model representing a user's forgot password code [without the auditing columns]
(api/src/model/ForgotPasswordData.py)
Author: Andrew Jarombek
Date: 11/9/2019
"""

from datetime import datetime
from tests.TestSuite import TestSuite
from model.ForgotPassword import ForgotPassword
from model.ForgotPasswordData import ForgotPasswordData


class TestForgotPasswordData(TestSuite):
    forgot_password1 = ForgotPasswordData(
        ForgotPassword(
            {
                "forgot_code": "123ABC",
                "username": "andy",
                "expires": datetime.fromisoformat("2019-11-10 00:00:00"),
                "deleted": False,
            }
        )
    )

    forgot_password2 = ForgotPasswordData(
        ForgotPassword(
            {
                "forgot_code": "456DEF",
                "username": "andy",
                "expires": datetime.fromisoformat("2019-11-10 02:00:00"),
                "deleted": False,
            }
        )
    )

    def test_forgot_password_data_str(self) -> None:
        """
        Prove that the human readable string representation of a ForgotPasswordData object is as expected.
        """
        self.assertEquals(
            str(self.forgot_password2),
            "ForgotPasswordData: [forgot_code: 456DEF, username: andy, expires: 2019-11-10 02:00:00, deleted: False]",
        )
        self.assertEquals(
            self.forgot_password2.__str__(),
            "ForgotPasswordData: [forgot_code: 456DEF, username: andy, expires: 2019-11-10 02:00:00, deleted: False]",
        )

    def test_forgot_password_data_repr(self) -> None:
        """
        Prove that the machine readable string representation of a ForgotPasswordData object is as expected.
        """
        self.assertEquals(
            repr(self.forgot_password2), "<ForgotPasswordData '456DEF','andy'>"
        )
        self.assertEquals(
            self.forgot_password2.__repr__(), "<ForgotPasswordData '456DEF','andy'>"
        )

    def test_forgot_password_data_eq(self) -> None:
        """
        Prove that two ForgotPasswordData objects with the same property values test positive for value equality.
        """
        self.assertTrue(self.forgot_password1 == self.forgot_password1)
        self.assertTrue(self.forgot_password1.__eq__(self.forgot_password1))

    def test_forgot_password_data_ne(self) -> None:
        """
        Prove that two ForgotPassword objects with different property values test negative for value equality.
        """
        self.assertTrue(self.forgot_password1 != self.forgot_password2)
        self.assertTrue(self.forgot_password1.__ne__(self.forgot_password2))
