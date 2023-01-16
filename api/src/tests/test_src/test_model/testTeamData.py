"""
Test suite for the model representing a team [without the auditing columns] (api/src/model/Team.py)
Author: Andrew Jarombek
Date: 11/29/2020
"""

from tests.TestSuite import TestSuite
from model.TeamData import TeamData
from model.Team import Team


class TestTeamData(TestSuite):
    team1 = TeamData(
        Team(
            {
                "name": "saintsxctf",
                "title": "St. Lawrence Cross Country and Track & Field",
                "picture_name": None,
                "week_start": None,
                "description": None,
                "deleted": "N",
            }
        )
    )

    team2 = TeamData(
        Team(
            {
                "name": "friends",
                "title": "Andy & Friends",
                "picture_name": None,
                "week_start": None,
                "description": None,
                "deleted": "N",
            }
        )
    )

    def test_team_data_str(self) -> None:
        """
        Prove that the human-readable string representation of a TeamData object is as expected.
        """
        team_str = (
            "TeamData: [name: saintsxctf, title: St. Lawrence Cross Country and Track & Field, "
            "picture_name: None, week_start: None, description: None, deleted: N]"
        )

        self.assertEqual(str(self.team1), team_str)

        # pylint: disable=unnecessary-dunder-call
        self.assertEqual(self.team1.__str__(), team_str)

    def test_team_data_repr(self) -> None:
        """
        Prove that the machine-readable string representation of a TeamData object is as expected.
        """
        self.assertEqual(repr(self.team1), "<TeamData 'saintsxctf'>")

        # pylint: disable=unnecessary-dunder-call
        self.assertEqual(self.team1.__repr__(), "<TeamData 'saintsxctf'>")

    def test_team_data_eq(self) -> None:
        """
        Prove that two TeamData objects with the same property values test positive for value equality.
        """
        self.assertTrue(self.team1 == self.team1)

        # pylint: disable=unnecessary-dunder-call
        self.assertTrue(self.team1.__eq__(self.team1))

    def test_team_data_ne(self) -> None:
        """
        Prove that two TeamData objects with different property values test negative for value equality.
        """
        self.assertTrue(self.team1 != self.team2)

        # pylint: disable=unnecessary-dunder-call
        self.assertTrue(self.team1.__ne__(self.team2))
