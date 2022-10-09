"""
Test suite for the model representing a team/group binding (api/src/model/TeamGroup.py)
Author: Andrew Jarombek
Date: 11/29/2020
"""

from tests.TestSuite import TestSuite
from model.TeamGroup import TeamGroup


class TestTeamGroup(TestSuite):
    team_group1 = TeamGroup(
        {
            "team_name": "saintsxctf",
            "group_id": 1,
            "group_name": "alumni",
            "deleted": "Y",
        }
    )

    team_group2 = TeamGroup(
        {
            "team_name": "saintsxctf_alumni",
            "group_id": 2,
            "group_name": "alumni",
            "deleted": "N",
        }
    )

    def test_team_group_str(self) -> None:
        """
        Prove that the human readable string representation of a TeamGroup object is as expected.
        """
        team_str = "TeamGroup: [team_name: saintsxctf, group_id: 1, group_name: alumni, deleted: Y]"

        self.assertEquals(str(self.team_group1), team_str)
        self.assertEquals(self.team_group1.__str__(), team_str)

    def test_team_group_repr(self) -> None:
        """
        Prove that the machine readable string representation of a TeamGroup object is as expected.
        """
        self.assertEquals(repr(self.team_group1), "<TeamGroup 'saintsxctf', 'alumni'>")
        self.assertEquals(
            self.team_group1.__repr__(), "<TeamGroup 'saintsxctf', 'alumni'>"
        )

    def test_team_group_eq(self) -> None:
        """
        Prove that two TeamGroup objects with the same property values test positive for value equality.
        """
        self.assertTrue(self.team_group1 == self.team_group1)
        self.assertTrue(self.team_group1.__eq__(self.team_group1))

    def test_team_group_ne(self) -> None:
        """
        Prove that two TeamGroup objects with different property values test negative for value equality.
        """
        self.assertTrue(self.team_group1 != self.team_group2)
        self.assertTrue(self.team_group1.__ne__(self.team_group2))
