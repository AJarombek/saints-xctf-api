"""
Test suite for the model representing user activation codes [without the auditing columns] (api/src/model/CodeData.py)
Author: Andrew Jarombek
Date: 11/9/2019
"""

from tests.TestSuite import TestSuite
from model.Code import Code
from model.CodeData import CodeData


class TestCodeData(TestSuite):
    def test_code_data_str(self) -> None:
        """
        Prove that the human-readable string representation of an CodeData object is as expected.
        """
        code = CodeData(Code({"activation_code": "80UN02", "deleted": False}))
        self.assertEqual(
            str(code),
            "CodeData: [activation_code: 80UN02, email: None, group_id: None, expiration_date: None, deleted: False]",
        )

        # pylint: disable=unnecessary-dunder-call
        self.assertEqual(
            code.__str__(),
            "CodeData: [activation_code: 80UN02, email: None, group_id: None, expiration_date: None, deleted: False]",
        )

    def test_code_data_repr(self) -> None:
        """
        Prove that the machine-readable string representation of an CodeData object is as expected.
        """
        code = CodeData(Code({"activation_code": "80UN02", "deleted": False}))
        self.assertEqual(repr(code), "<CodeData '80UN02'>")

        # pylint: disable=unnecessary-dunder-call
        self.assertEqual(code.__repr__(), "<CodeData '80UN02'>")

    def test_code_data_eq(self) -> None:
        """
        Prove that two CodeData objects with the same property values test positive for value equality.
        """
        code1 = CodeData(Code({"activation_code": "AJAJAJ", "deleted": False}))
        code2 = CodeData(Code({"activation_code": "AJAJAJ", "deleted": False}))
        self.assertTrue(code1 == code2)

        # pylint: disable=unnecessary-dunder-call
        self.assertTrue(code1.__eq__(code2))

    def test_code_data_ne(self) -> None:
        """
        Prove that two CodeData objects with different property values test negative for value equality.
        """
        code1 = CodeData(Code({"activation_code": "80UN02", "deleted": False}))
        code2 = CodeData(Code({"activation_code": "AJAJAJ", "deleted": False}))
        self.assertTrue(code1 != code2)

        # pylint: disable=unnecessary-dunder-call
        self.assertTrue(code1.__ne__(code2))
