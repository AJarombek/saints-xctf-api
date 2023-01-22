"""
GroupMember data access from the SaintsXCTF MySQL database.  Contains SQL queries related to users
who are members of a group.  Most group data is accessed from a separate GroupDao.
Author: Andrew Jarombek
Date: 7/2/2019
"""

from datetime import datetime

from sqlalchemy.engine.cursor import ResultProxy
from sqlalchemy import and_

from database import db
from model.GroupMember import GroupMember
from model.TeamGroup import TeamGroup
from dao.basicDao import BasicDao


class GroupMemberDao:
    @staticmethod
    def get_group_member(group_id: int, username: str) -> GroupMember:
        """
        Get a group membership based on the group id and username of the user.
        :param group_id: Unique id of a group.
        :param username: Unique identifier for the user
        :return: A group membership object.
        """
        return (
            GroupMember.query.filter(
                and_(GroupMember.group_id == group_id, GroupMember.username == username)
            )
            .filter(GroupMember.deleted.is_(False))
            .first()
        )

    @staticmethod
    def get_group_member_by_group_name(
        team_name: str, group_name: str, username: str
    ) -> GroupMember:
        """
        Get a group membership based on a team name, group name, and username of a user.
        :param team_name: Unique name for a team.
        :param group_name: Unique name of a group within a team.
        :param username: Unique identifier for the user.
        :return: A group membership object.
        """
        return (
            GroupMember.query.filter(GroupMember.group_name == TeamGroup.group_name)
            .filter(
                and_(
                    TeamGroup.group_name == group_name, TeamGroup.team_name == team_name
                )
            )
            .filter(
                and_(
                    GroupMember.group_name == group_name,
                    GroupMember.username == username,
                )
            )
            .filter(GroupMember.deleted.is_(False))
            .first()
        )

    @staticmethod
    def get_user_groups(username: str) -> ResultProxy:
        """
        Get information about all the groups a user is a member of
        :param username: Unique identifier for the user
        :return: A list of groups
        """
        # pylint: disable=no-member
        return db.session.execute(
            """
            SELECT `groups`.id, groupmembers.group_name, group_title, status, user
            FROM groupmembers 
            INNER JOIN `groups` ON `groups`.group_name=groupmembers.group_name 
            WHERE username=:username
            AND groupmembers.deleted IS FALSE 
            AND `groups`.deleted IS FALSE 
            """,
            {"username": username},
        )

    @staticmethod
    def get_user_groups_in_team(username: str, team_name: str) -> ResultProxy:
        """
        Get information about all the groups a user is a member of within a team
        :param username: Unique identifier for the user
        :param team_name: Unique name for a team
        :return: A list of groups
        """
        # pylint: disable=no-member
        return db.session.execute(
            """
            SELECT groupmembers.group_name,groupmembers.group_id,group_title,status,user 
            FROM groupmembers 
            INNER JOIN `groups` ON `groups`.group_name=groupmembers.group_name 
            INNER JOIN teamgroups ON teamgroups.group_id=`groups`.id
            INNER JOIN teams ON teams.name=teamgroups.team_name 
            WHERE username=:username
            AND teams.name=:team_name
            AND groupmembers.deleted IS FALSE 
            AND `groups`.deleted IS FALSE 
            AND teamgroups.deleted IS FALSE 
            AND teams.deleted IS FALSE 
            """,
            {"username": username, "team_name": team_name},
        )

    @staticmethod
    def get_group_members(group_name: str, team_name: str) -> ResultProxy:
        """
        Get the users who are members of a group.
        :param group_name: Unique name of a group within a team.
        :param team_name: Unique name for a team.
        :return: A list of group members.
        """
        # pylint: disable=no-member
        return db.session.execute(
            """
            SELECT users.username,first,last,member_since,user,status 
            FROM groupmembers 
            INNER JOIN `groups` ON `groups`.group_name=groupmembers.group_name 
            INNER JOIN teamgroups ON teamgroups.group_id=`groups`.id
            INNER JOIN users ON groupmembers.username=users.username 
            WHERE groupmembers.group_name=:group_name
            AND teamgroups.team_name=:team_name
            AND groupmembers.deleted IS FALSE 
            AND `groups`.deleted IS FALSE 
            AND teamgroups.deleted IS FALSE 
            AND users.deleted IS FALSE 
            """,
            {"group_name": group_name, "team_name": team_name},
        )

    @staticmethod
    def get_group_members_by_id(group_id: str) -> ResultProxy:
        """
        Get the users who are members of a group.
        :param group_id: Unique id of a group.
        :return: A list of group members.
        """
        # pylint: disable=no-member
        return db.session.execute(
            """
            SELECT users.username,first,last,member_since,user,status 
            FROM groupmembers 
            INNER JOIN users ON groupmembers.username=users.username 
            WHERE groupmembers.group_id=:group_id
            AND groupmembers.deleted IS FALSE 
            AND users.deleted IS FALSE 
            """,
            {"group_id": group_id},
        )

    @staticmethod
    def update_group_member(
        group_id: int, username: str, status: str, user: str
    ) -> bool:
        """
        Update a group membership for a user.
        :param group_id: Unique id of a group.
        :param username: Unique name for a user.
        :param status: Status of a group membership - whether it is accepted or pending.
        :param user: User type of a group membership - whether the user is an admin or a regular user.
        :return: True if the group membership was updated, False otherwise.
        """
        # pylint: disable=no-member
        db.session.execute(
            """
            UPDATE groupmembers SET 
                status=:status, 
                user=:user,
                modified_date=:modified_date,
                modified_app=:modified_app
            WHERE group_id=:group_id 
            AND username=:username
            AND deleted IS FALSE
            """,
            {
                "group_id": group_id,
                "username": username,
                "modified_date": datetime.now(),
                "modified_app": "saints-xctf-api",
                "status": status,
                "user": user,
            },
        )
        return BasicDao.safe_commit()

    @staticmethod
    def soft_delete_group_member(group_id: int, username: str) -> bool:
        """
        Soft delete a group membership record.
        :param group_id: Unique id of a group.
        :param username: Unique name for a user.
        :return: True if the group membership was soft deleted, False otherwise.
        """
        # pylint: disable=no-member
        db.session.execute(
            """
            UPDATE groupmembers SET 
                deleted=:deleted,
                deleted_date=:deleted_date,
                deleted_app=:deleted_app
            WHERE group_id=:group_id 
            AND username=:username
            AND deleted IS FALSE
            """,
            {
                "group_id": group_id,
                "username": username,
                "deleted": True,
                "deleted_date": datetime.now(),
                "deleted_app": "saints-xctf-api",
            },
        )
        return BasicDao.safe_commit()
