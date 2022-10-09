"""
Test suite for the model representing information about a user that is part of a group (api/src/model/GroupMember.py)
Author: Andrew Jarombek
Date: 11/10/2019
"""

from tests.TestSuite import TestSuite
from model.GroupMember import GroupMember


class TestGroupMember(TestSuite):
    group_member1 = GroupMember(
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

    group_member2 = GroupMember(
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

    def test_group_member_str(self) -> None:
        """
        Prove that the human readable string representation of an GroupMember object is as expected.
        """
        group_member_str = (
            "GroupMember: [id: 1, group_name: mensxc, group_id: 3, username: andy, "
            "status: accepted, user: user, deleted: False]"
        )

        self.assertEquals(str(self.group_member1), group_member_str)
        self.assertEquals(self.group_member1.__str__(), group_member_str)

    def test_group_member_repr(self) -> None:
        """
        Prove that the machine readable string representation of an GroupMember object is as expected.
        """
        self.assertEquals(repr(self.group_member1), "<GroupMember 'mensxc','andy'>")
        self.assertEquals(
            self.group_member1.__repr__(), "<GroupMember 'mensxc','andy'>"
        )

    def test_group_member_eq(self) -> None:
        """
        Prove that two GroupMember objects with the same property values test positive for value equality.
        """
        self.assertTrue(self.group_member1 == self.group_member1)
        self.assertTrue(self.group_member1.__eq__(self.group_member1))

    def test_group_member_ne(self) -> None:
        """
        Prove that two GroupMember objects with different property values test negative for value equality.
        """
        self.assertTrue(self.group_member1 != self.group_member2)
        self.assertTrue(self.group_member1.__ne__(self.group_member2))
