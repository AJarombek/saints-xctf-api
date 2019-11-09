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
        code = Code({'activation_code': '80UN02', 'deleted': False})
        self.assertEquals(str(code), 'Code: [activation_code: 80UN02, deleted: False]')
        self.assertEquals(code.__str__(), 'Code: [activation_code: 80UN02, deleted: False]')

    def test_code_repr(self) -> None:
        """
        Prove that the machine readable string representation of an Code object is as expected.
        """
        code = Code({'activation_code': '80UN02', 'deleted': False})
        self.assertEquals(repr(code), "<Code '80UN02'>")
        self.assertEquals(code.__repr__(), "<Code '80UN02'>")

    def test_code_eq(self) -> None:
        """
        Prove that two Code objects with the same property values test positive for value equality.
        """
        code1 = Code({'activation_code': 'AJAJAJ', 'deleted': False})
        code2 = Code({'activation_code': 'AJAJAJ', 'deleted': False})
        self.assertTrue(code1 == code2)
        self.assertTrue(code1.__eq__(code2))

    def test_code_ne(self) -> None:
        """
        Prove that two Code objects with different property values test negative for value equality.
        """
        code1 = Code({'activation_code': '80UN02', 'deleted': False})
        code2 = Code({'activation_code': 'AJAJAJ', 'deleted': False})
        self.assertTrue(code1 != code2)
        self.assertTrue(code1.__ne__(code2))
