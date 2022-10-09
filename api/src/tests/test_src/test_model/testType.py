"""
Test suite for the model representing an exercise type (api/src/model/Type.py)
Author: Andrew Jarombek
Date: 11/21/2019
"""

from tests.TestSuite import TestSuite
from model.Type import Type


class TestType(TestSuite):
    type1_dict = {"type": "run"}
    type2_dict = {"type": "bike"}
    type3_dict = {"type": "other"}

    type1 = Type(type1_dict)
    type1copy = Type(type1_dict)

    type2 = Type(type2_dict)
    type3 = Type(type3_dict)

    def test_type_str(self) -> None:
        """
        Prove that the human readable string representation of a Type object is as expected.
        """
        type_str = "Type: [type: run]"

        self.assertEquals(str(self.type1), type_str)
        self.assertEquals(self.type1.__str__(), type_str)

    def test_type_repr(self) -> None:
        """
        Prove that the machine readable string representation of a Type object is as expected.
        """
        self.assertEquals(repr(self.type2), "<Type 'bike'>")
        self.assertEquals(self.type2.__repr__(), "<Type 'bike'>")

    def test_type_eq(self) -> None:
        """
        Prove that two Type objects with the same property values test positive for value equality.
        """
        self.assertTrue(self.type1 == self.type1copy)
        self.assertTrue(self.type1.__eq__(self.type1copy))

    def test_type_ne(self) -> None:
        """
        Prove that two Type objects with different property values test negative for value equality.
        """
        self.assertTrue(self.type1 != self.type3)
        self.assertTrue(self.type1.__ne__(self.type3))
