"""
Test suite for the model representing user activation codes (api/src/model/Code.py)
Author: Andrew Jarombek
Date: 11/9/2019
"""

from tests.TestSuite import TestSuite
from model.Code import Code


class TestCode(TestSuite):

    def test_code_str(self) -> None:
        """
        Prove that the human readable string representation of an Code object is as expected.
        """
        admin = Code({'activation_code': '80UN02', 'deleted': False})
        self.assertEquals(str(admin), 'Code: [activation_code: 80UN02, deleted: False]')
        self.assertEquals(admin.__str__(), 'Code: [activation_code: 80UN02, deleted: False]')

    def test_code_repr(self) -> None:
        """
        Prove that the machine readable string representation of an Code object is as expected.
        """
        admin = Code({'activation_code': '80UN02', 'deleted': False})
        self.assertEquals(repr(admin), "<Code '80UN02'>")
        self.assertEquals(admin.__repr__(), "<Code '80UN02'>")

    def test_code_eq(self) -> None:
        """
        Prove that two Code objects with the same property values test positive for value equality.
        """
        admin1 = Code({'activation_code': 'AJAJAJ', 'deleted': False})
        admin2 = Code({'activation_code': 'AJAJAJ', 'deleted': False})
        self.assertTrue(admin1 == admin2)
        self.assertTrue(admin1.__eq__(admin2))

    def test_code_ne(self) -> None:
        """
        Prove that two Code objects with different property values test negative for value equality.
        """
        admin1 = Code({'activation_code': '80UN02', 'deleted': False})
        admin2 = Code({'activation_code': 'AJAJAJ', 'deleted': False})
        self.assertTrue(admin1 != admin2)
        self.assertTrue(admin1.__ne__(admin2))
