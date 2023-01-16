"""
Test suite for the model representing groups within a team [without the auditing columns] (api/src/model/Group.py)
Author: Andrew Jarombek
Date: 11/10/2019
"""

from tests.TestSuite import TestSuite
from model.Group import Group
from model.GroupData import GroupData


class TestGroup(TestSuite):
    group1 = GroupData(
        Group(
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
    )

    group2 = GroupData(
        Group(
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
    )

    def test_group_data_str(self) -> None:
        """
        Prove that the human-readable string representation of an Group object is as expected.
        """
        group_str = (
            "GroupData: [id: 2, group_name: mensxc, group_title: Men's Cross Country, grouppic: None, "
            "grouppic_name: None, week_start: monday, description: , deleted: False]"
        )

        self.assertEqual(str(self.group1), group_str)

        # pylint: disable=unnecessary-dunder-call
        self.assertEqual(self.group1.__str__(), group_str)

    def test_group_data_repr(self) -> None:
        """
        Prove that the machine-readable string representation of an GroupData object is as expected.
        """
        self.assertEqual(repr(self.group1), "<GroupData 2, 'mensxc'>")

        # pylint: disable=unnecessary-dunder-call
        self.assertEqual(self.group1.__repr__(), "<GroupData 2, 'mensxc'>")

    def test_group_data_eq(self) -> None:
        """
        Prove that two GroupData objects with the same property values test positive for value equality.
        """
        self.assertTrue(self.group1 == self.group1)

        # pylint: disable=unnecessary-dunder-call
        self.assertTrue(self.group1.__eq__(self.group1))

    def test_group_data_ne(self) -> None:
        """
        Prove that two GroupData objects with different property values test negative for value equality.
        """
        self.assertTrue(self.group1 != self.group2)

        # pylint: disable=unnecessary-dunder-call
        self.assertTrue(self.group1.__ne__(self.group2))
