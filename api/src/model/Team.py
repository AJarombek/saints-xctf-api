"""
Team ORM model for the 'teams' table in the SaintsXCTF MySQL database.
Author: Andrew Jarombek
Date: 11/28/2020
"""

from sqlalchemy import Column

from app import db


class Team(db.Model):
    def __init__(self, team: dict):
        """
        Initialize a Team object by passing in a dictionary.
        :param team: A dictionary with fields matching the Team fields
        """
        self.name = team.get("name")
        self.title = team.get("title")
        self.picture_name = team.get("picture_name")
        self.week_start = team.get("week_start")
        self.description = team.get("description")
        self.deleted = team.get("deleted")
        self.created_date = team.get("created_date")
        self.created_user = team.get("created_user")
        self.created_app = team.get("created_app")
        self.modified_date = team.get("modified_date")
        self.modified_user = team.get("modified_user")
        self.modified_app = team.get("modified_app")
        self.deleted_date = team.get("deleted_date")
        self.deleted_user = team.get("deleted_user")
        self.deleted_app = team.get("deleted_app")

    __tablename__ = "teams"

    # Data Columns
    name = Column(db.VARCHAR(31), primary_key=True)
    title = Column(db.VARCHAR(127), index=True)
    picture_name = Column(db.VARCHAR(255))
    week_start = Column(db.VARCHAR(15), db.ForeignKey("weekstart.week_start"))
    description = Column(db.VARCHAR(255))
    deleted = Column(db.BOOLEAN)

    # Audit Columns
    created_date = Column(db.DATETIME)
    created_user = Column(db.VARCHAR(31))
    created_app = Column(db.VARCHAR(31))
    modified_date = Column(db.DATETIME)
    modified_user = Column(db.VARCHAR(31))
    modified_app = Column(db.VARCHAR(31))
    deleted_date = Column(db.DATETIME)
    deleted_user = Column(db.VARCHAR(31))
    deleted_app = Column(db.VARCHAR(31))

    def __str__(self):
        """
        String representation of a team.  This representation is meant to be human-readable.
        :return: The team in string form.
        """
        return (
            f"Team: [name: {self.name}, title: {self.title}, picture_name: {self.picture_name}, "
            f"week_start: {self.week_start}, description: {self.description}, deleted: {self.deleted}]"
        )

    def __repr__(self):
        """
        String representation of a team.  This representation is meant to be machine-readable.
        :return: The team in string form.
        """
        return f"<Team '{self.name}'>"

    def __eq__(self, other):
        """
        Determine value equality between this object and another object.
        :param other: Another object to compare to this team.
        :return: True if the objects are equal, False otherwise.
        """
        return Team.compare(self, other)

    @classmethod
    def compare(cls, team_1, team_2) -> bool:
        """
        Helper function used to determine value equality between two objects that are assumed to be teams.
        :param team_1: The first team object.
        :param team_2: The second team object.
        :return: True if the objects are equal, False otherwise.
        """
        return all(
            [
                team_1.name == team_2.name,
                team_1.title == team_2.title,
                team_1.picture_name == team_2.picture_name,
                team_1.week_start == team_2.week_start,
                team_1.description == team_2.description,
                team_1.deleted == team_2.deleted,
            ]
        )
