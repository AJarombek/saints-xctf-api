"""
Test suite for the model representing a team membership (api/src/model/TeamMember.py)
Author: Andrew Jarombek
Date: 11/29/2020
"""

from tests.TestSuite import TestSuite
from model.TeamMember import TeamMember


class TestTeamMember(TestSuite):
    team_member1 = TeamMember(
        {
            "team_name": "saintsxctf",
            "username": "andy",
            "status": "accepted",
            "user": "admin",
            "deleted": "N",
        }
    )

    team_member2 = TeamMember(
        {
            "team_name": "saintsxctf_alumni",
            "username": "andy",
            "status": "accepted",
            "user": "user",
            "deleted": None,
        }
    )

    def test_team_member_str(self) -> None:
        """
        Prove that the human-readable string representation of a TeamMember object is as expected.
        """
        team_str = "TeamMember: [team_name: saintsxctf, username: andy, status: accepted, user: admin, deleted: N]"

        self.assertEqual(str(self.team_member1), team_str)

        # pylint: disable=unnecessary-dunder-call
        self.assertEqual(self.team_member1.__str__(), team_str)

    def test_team_member_repr(self) -> None:
        """
        Prove that the machine-readable string representation of a TeamMember object is as expected.
        """
        self.assertEqual(repr(self.team_member1), "<TeamMember 'saintsxctf', 'andy'>")

        # pylint: disable=unnecessary-dunder-call
        self.assertEqual(
            self.team_member1.__repr__(), "<TeamMember 'saintsxctf', 'andy'>"
        )

    def test_team_member_eq(self) -> None:
        """
        Prove that two TeamMember objects with the same property values test positive for value equality.
        """
        self.assertTrue(self.team_member1 == self.team_member1)

        # pylint: disable=unnecessary-dunder-call
        self.assertTrue(self.team_member1.__eq__(self.team_member1))

    def test_team_member_ne(self) -> None:
        """
        Prove that two TeamMember objects with different property values test negative for value equality.
        """
        self.assertTrue(self.team_member1 != self.team_member2)

        # pylint: disable=unnecessary-dunder-call
        self.assertTrue(self.team_member1.__ne__(self.team_member2))
