"""
Test suite for the model representing information about a user that is part of a group [without the auditing columns]
(api/src/model/GroupMember.py)
Author: Andrew Jarombek
Date: 11/10/2019
"""

from tests.TestSuite import TestSuite
from model.GroupMember import GroupMember
from model.GroupMemberData import GroupMemberData


class TestGroupMemberData(TestSuite):
    group_member1 = GroupMemberData(
        GroupMember(
            {
                "id": 1,
                "group_name": "mensxc",
                "group_id": 3,
                "username": "andy",
                "status": "accepted",
                "user": "user",
                "deleted": False,
            }
        )
    )

    group_member2 = GroupMemberData(
        GroupMember(
            {
                "id": 2,
                "group_name": "alumni",
                "group_id": 1,
                "username": "andy",
                "status": "accepted",
                "user": "admin",
                "deleted": False,
            }
        )
    )

    def test_group_member_data_str(self) -> None:
        """
        Prove that the human-readable string representation of an GroupMember object is as expected.
        """
        group_member_str = (
            "GroupMemberData: [id: 2, group_name: alumni, group_id: 1, username: andy, "
            "status: accepted, user: admin, deleted: False]"
        )

        self.assertEqual(str(self.group_member2), group_member_str)

        # pylint: disable=unnecessary-dunder-call
        self.assertEqual(self.group_member2.__str__(), group_member_str)

    def test_group_member_data_repr(self) -> None:
        """
        Prove that the machine-readable string representation of an GroupMember object is as expected.
        """
        self.assertEqual(repr(self.group_member2), "<GroupMemberData 'alumni','andy'>")

        # pylint: disable=unnecessary-dunder-call
        self.assertEqual(
            self.group_member2.__repr__(), "<GroupMemberData 'alumni','andy'>"
        )

    def test_group_member_data_eq(self) -> None:
        """
        Prove that two GroupMember objects with the same property values test positive for value equality.
        """
        self.assertTrue(self.group_member1 == self.group_member1)

        # pylint: disable=unnecessary-dunder-call
        self.assertTrue(self.group_member1.__eq__(self.group_member1))

    def test_group_member_data_ne(self) -> None:
        """
        Prove that two GroupMember objects with different property values test negative for value equality.
        """
        self.assertTrue(self.group_member1 != self.group_member2)

        # pylint: disable=unnecessary-dunder-call
        self.assertTrue(self.group_member1.__ne__(self.group_member2))
