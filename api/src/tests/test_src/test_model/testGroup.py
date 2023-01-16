"""
Test suite for the model representing groups within a team (api/src/model/Group.py)
Author: Andrew Jarombek
Date: 11/10/2019
"""

from tests.TestSuite import TestSuite
from model.Group import Group


class TestGroup(TestSuite):
    group1 = Group(
        {
            "id": 2,
            "group_name": "mensxc",
            "group_title": "Men's Cross Country",
            "grouppic": None,
            "grouppic_name": None,
            "week_start": "monday",
            "description": "",
            "deleted": False,
        }
    )

    group2 = Group(
        {
            "id": 1,
            "group_name": "wmenstf",
            "group_title": "Women's Track & Field",
            "grouppic": None,
            "grouppic_name": None,
            "week_start": "monday",
            "description": "",
            "deleted": False,
        }
    )

    def test_group_str(self) -> None:
        """
        Prove that the human-readable string representation of an Group object is as expected.
        """
        group_str = (
            "Group: [id: 2, group_name: mensxc, group_title: Men's Cross Country, grouppic: None, "
            "grouppic_name: None, week_start: monday, description: , deleted: False]"
        )

        self.assertEqual(str(self.group1), group_str)

        # pylint: disable=unnecessary-dunder-call
        self.assertEqual(self.group1.__str__(), group_str)

    def test_group_repr(self) -> None:
        """
        Prove that the machine-readable string representation of an Group object is as expected.
        """
        self.assertEqual(repr(self.group1), "<Group 2, 'mensxc'>")

        # pylint: disable=unnecessary-dunder-call
        self.assertEqual(self.group1.__repr__(), "<Group 2, 'mensxc'>")

    def test_group_eq(self) -> None:
        """
        Prove that two Group objects with the same property values test positive for value equality.
        """
        self.assertTrue(self.group1 == self.group1)

        # pylint: disable=unnecessary-dunder-call
        self.assertTrue(self.group1.__eq__(self.group1))

    def test_group_ne(self) -> None:
        """
        Prove that two Group objects with different property values test negative for value equality.
        """
        self.assertTrue(self.group1 != self.group2)

        # pylint: disable=unnecessary-dunder-call
        self.assertTrue(self.group1.__ne__(self.group2))
