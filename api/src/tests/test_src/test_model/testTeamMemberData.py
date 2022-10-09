"""
Test suite for the model representing a team membership [without the auditing columns] (api/src/model/TeamMemberData.py)
Author: Andrew Jarombek
Date: 11/29/2020
"""

from tests.TestSuite import TestSuite
from model.TeamMemberData import TeamMemberData
from model.TeamMember import TeamMember


class TestTeamMemberData(TestSuite):
    team_member1 = TeamMemberData(
        TeamMember(
            {
                "team_name": "saintsxctf",
                "username": "andy",
                "status": "accepted",
                "user": "admin",
                "deleted": "N",
            }
        )
    )

    team_member2 = TeamMemberData(
        TeamMember(
            {
                "team_name": "saintsxctf_alumni",
                "username": "andy",
                "status": "accepted",
                "user": "user",
                "deleted": None,
            }
        )
    )

    def test_team_member_data_str(self) -> None:
        """
        Prove that the human readable string representation of a TeamMemberData object is as expected.
        """
        team_str = "TeamMemberData: [team_name: saintsxctf, username: andy, status: accepted, user: admin, deleted: N]"

        self.assertEquals(str(self.team_member1), team_str)
        self.assertEquals(self.team_member1.__str__(), team_str)

    def test_team_member_data_repr(self) -> None:
        """
        Prove that the machine readable string representation of a TeamMemberData object is as expected.
        """
        self.assertEquals(
            repr(self.team_member1), "<TeamMemberData 'saintsxctf', 'andy'>"
        )
        self.assertEquals(
            self.team_member1.__repr__(), "<TeamMemberData 'saintsxctf', 'andy'>"
        )

    def test_team_member_data_eq(self) -> None:
        """
        Prove that two TeamMemberData objects with the same property values test positive for value equality.
        """
        self.assertTrue(self.team_member1 == self.team_member1)
        self.assertTrue(self.team_member1.__eq__(self.team_member1))

    def test_team_member_data_ne(self) -> None:
        """
        Prove that two TeamMemberData objects with different property values test negative for value equality.
        """
        self.assertTrue(self.team_member1 != self.team_member2)
        self.assertTrue(self.team_member1.__ne__(self.team_member2))
