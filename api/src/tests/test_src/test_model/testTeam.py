"""
Test suite for the model representing a team (api/src/model/Team.py)
Author: Andrew Jarombek
Date: 11/29/2020
"""

from tests.TestSuite import TestSuite
from model.Team import Team


class TestTeam(TestSuite):
    team1 = Team(
        {
            "name": "saintsxctf",
            "title": "St. Lawrence Cross Country and Track & Field",
            "picture_name": None,
            "week_start": None,
            "description": None,
            "deleted": "N",
        }
    )

    team2 = Team(
        {
            "name": "friends",
            "title": "Andy & Friends",
            "picture_name": None,
            "week_start": None,
            "description": None,
            "deleted": "N",
        }
    )

    def test_team_str(self) -> None:
        """
        Prove that the human readable string representation of a Team object is as expected.
        """
        team_str = (
            "Team: [name: saintsxctf, title: St. Lawrence Cross Country and Track & Field, "
            "picture_name: None, week_start: None, description: None, deleted: N]"
        )

        self.assertEquals(str(self.team1), team_str)
        self.assertEquals(self.team1.__str__(), team_str)

    def test_team_repr(self) -> None:
        """
        Prove that the machine readable string representation of a Team object is as expected.
        """
        self.assertEquals(repr(self.team1), "<Team 'saintsxctf'>")
        self.assertEquals(self.team1.__repr__(), "<Team 'saintsxctf'>")

    def test_team_eq(self) -> None:
        """
        Prove that two Team objects with the same property values test positive for value equality.
        """
        self.assertTrue(self.team1 == self.team1)
        self.assertTrue(self.team1.__eq__(self.team1))

    def test_team_ne(self) -> None:
        """
        Prove that two Team objects with different property values test negative for value equality.
        """
        self.assertTrue(self.team1 != self.team2)
        self.assertTrue(self.team1.__ne__(self.team2))
