"""
Test suite for the model representing user activation codes (api/src/model/Code.py)
Author: Andrew Jarombek
Date: 11/9/2019
"""

from datetime import datetime, timedelta
from copy import deepcopy

from tests.TestSuite import TestSuite
from model.Code import Code


class TestCode(TestSuite):
    code1 = Code(
        {
            "activation_code": "AJAJAJ",
            "email": "andrew@jarombek.com",
            "group_id": 2,
            "expiration_date": datetime.now() + timedelta(weeks=2),
            "deleted": False,
        }
    )

    code2 = Code(
        {
            "activation_code": "80UN02",
            "email": "andrew@jarombek.com",
            "group_id": 1,
            "expiration_date": None,
            "deleted": False,
        }
    )

    def test_code_str(self) -> None:
        """
        Prove that the human readable string representation of an Code object is as expected.
        """

        self.assertEquals(
            str(self.code2),
            "Code: [activation_code: 80UN02, email: andrew@jarombek.com, group_id: 1, expiration_date: None, "
            "deleted: False]",
        )
        self.assertEquals(
            self.code2.__str__(),
            "Code: [activation_code: 80UN02, email: andrew@jarombek.com, group_id: 1, expiration_date: None, "
            "deleted: False]",
        )

    def test_code_repr(self) -> None:
        """
        Prove that the machine readable string representation of an Code object is as expected.
        """
        self.assertEquals(repr(self.code2), "<Code '80UN02'>")
        self.assertEquals(self.code2.__repr__(), "<Code '80UN02'>")

    def test_code_eq(self) -> None:
        """
        Prove that two Code objects with the same property values test positive for value equality.
        """
        code3 = deepcopy(self.code1)
        self.assertTrue(self.code1 == code3)
        self.assertTrue(self.code1.__eq__(code3))

    def test_code_ne(self) -> None:
        """
        Prove that two Code objects with different property values test negative for value equality.
        """
        self.assertTrue(self.code1 != self.code2)
        self.assertTrue(self.code1.__ne__(self.code2))
