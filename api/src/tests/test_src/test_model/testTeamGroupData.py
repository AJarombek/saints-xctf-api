"""
Test suite for the model representing a team/group binding [without the auditing columns]
(api/src/model/TeamGroupData.py)
Author: Andrew Jarombek
Date: 11/29/2020
"""

from tests.TestSuite import TestSuite
from model.TeamGroup import TeamGroup
from model.TeamGroupData import TeamGroupData


class TestTeamGroupData(TestSuite):
    team_group1 = TeamGroupData(
        TeamGroup(
            {
                "team_name": "saintsxctf",
                "group_id": 1,
                "group_name": "alumni",
                "deleted": "Y",
            }
        )
    )

    team_group2 = TeamGroupData(
        TeamGroup(
            {
                "team_name": "saintsxctf_alumni",
                "group_id": 2,
                "group_name": "alumni",
                "deleted": "N",
            }
        )
    )

    def test_team_group_data_str(self) -> None:
        """
        Prove that the human-readable string representation of a TeamGroupData object is as expected.
        """
        team_str = "TeamGroupData: [team_name: saintsxctf, group_id: 1, group_name: alumni, deleted: Y]"

        self.assertEqual(str(self.team_group1), team_str)

        # pylint: disable=unnecessary-dunder-call
        self.assertEqual(self.team_group1.__str__(), team_str)

    def test_team_group_data_repr(self) -> None:
        """
        Prove that the machine-readable string representation of a TeamGroupData object is as expected.
        """
        self.assertEqual(
            repr(self.team_group1), "<TeamGroupData 'saintsxctf', 'alumni'>"
        )

        # pylint: disable=unnecessary-dunder-call
        self.assertEqual(
            self.team_group1.__repr__(), "<TeamGroupData 'saintsxctf', 'alumni'>"
        )

    def test_team_group_data_eq(self) -> None:
        """
        Prove that two TeamGroupData objects with the same property values test positive for value equality.
        """
        self.assertTrue(self.team_group1 == self.team_group1)

        # pylint: disable=unnecessary-dunder-call
        self.assertTrue(self.team_group1.__eq__(self.team_group1))

    def test_team_group_data_ne(self) -> None:
        """
        Prove that two TeamGroupData objects with different property values test negative for value equality.
        """
        self.assertTrue(self.team_group1 != self.team_group2)

        # pylint: disable=unnecessary-dunder-call
        self.assertTrue(self.team_group1.__ne__(self.team_group2))
