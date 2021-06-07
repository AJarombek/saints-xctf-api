"""
TeamMember data access from the SaintsXCTF MySQL database.  Contains SQL queries related to users
who are members of a team.  Most team data is accessed from a separate TeamDao.
Author: Andrew Jarombek
Date: 11/29/2020
"""

from typing import List, Dict
from datetime import datetime

from sqlalchemy.engine.cursor import ResultProxy
from flask import current_app

from database import db
from dao.basicDao import BasicDao
from model.TeamMember import TeamMember
from model.GroupMember import GroupMember


class TeamMemberDao:

    @staticmethod
    def get_user_teams(username: str) -> ResultProxy:
        """
        Get information about all the teams a user is a member of
        :param username: Unique identifier for the user
        :return: A list of teams
        """
        return db.session.execute(
            '''
            SELECT team_name,title,status,user 
            FROM teammembers 
            INNER JOIN teams ON teams.name=teammembers.team_name 
            WHERE username=:username
            AND teammembers.deleted IS FALSE
            AND teams.deleted IS FALSE
            ''',
            {'username': username}
        )

    @staticmethod
    def get_user_team_membership(username: str, team_name: str) -> ResultProxy:
        """
        Get information about a specific team that a user is a member of.
        :param username: Unique identifier for the user.
        :param team_name: Unique name of a team.
        :return: Details about a team membership.
        """
        return db.session.execute(
            '''
            SELECT team_name,title,status,user 
            FROM teammembers 
            INNER JOIN teams ON teams.name=teammembers.team_name 
            WHERE username=:username
            AND teams.name=:team_name
            AND teammembers.deleted IS FALSE
            AND teams.deleted IS FALSE
            ''',
            {'username': username, 'team_name': team_name}
        )

    @staticmethod
    def get_team_members(team_name: str) -> ResultProxy:
        """
        Get the users who are members of a team.
        :param team_name: Unique name of a team.
        :return: A list of team members.
        """
        return db.session.execute(
            '''
            SELECT users.username,first,last,member_since,user,status,teammembers.deleted 
            FROM teammembers 
            INNER JOIN teams ON teams.name=teammembers.team_name 
            INNER JOIN users ON teammembers.username=users.username 
            WHERE teammembers.team_name=:team_name
            AND teammembers.deleted IS FALSE 
            AND teams.deleted IS FALSE 
            AND users.deleted IS FALSE 
            ''',
            {'team_name': team_name}
        )

    @staticmethod
    def set_initial_membership(username: str, team_name: str, group_id: int, group_name: str) -> bool:
        """
        Set the team and group memberships for a new user when they join SaintsXCTF.
        :param username: Unique identifier for the new user.
        :param team_name: Unique name of a team.
        :param group_id: Unique id of a group.
        :param group_name: Unique name of a group within a team.
        :return: Whether or not the team and group memberships were successfully created.
        """
        team_membership = TeamMember({
            'team_name': team_name,
            'username': username,
            'status': 'accepted',
            'user': 'user',
            'deleted': False,
            'created_date': datetime.now(),
            'created_user': username,
            'created_app': 'saints-xctf-api'
        })

        db.session.add(team_membership)

        group_membership = GroupMember({
            'group_name': group_name,
            'group_id': group_id,
            'username': username,
            'status': 'accepted',
            'user': 'user',
            'deleted': False,
            'created_date': datetime.now(),
            'created_user': username,
            'created_app': 'saints-xctf-api'
        })

        db.session.add(group_membership)

        return BasicDao.safe_commit()

    @staticmethod
    def accept_user_team_membership(username: str, team_name: str, updating_username: str) -> bool:
        """
        Change the status of a users team membership to 'accepted'.
        :param username: Unique identifier for the user who team membership is getting updated.
        :param team_name: Unique name of a team.
        :param updating_username: Unique identifier for the user who is updating a team membership.
        :return: Whether or not the team membership was successfully updated.
        """
        db.session.execute(
            '''
            UPDATE teammembers SET 
                status = 'accepted',
                modified_date=CURRENT_TIMESTAMP(),
                modified_user=:updating_username,
                modified_app='saints-xctf-api'
            WHERE username=:username
            AND team_name=:team_name
            AND deleted IS FALSE
            ''',
            {'username': username, 'team_name': team_name, 'updating_username': updating_username}
        )
        return BasicDao.safe_commit()

    @staticmethod
    def update_user_memberships(username: str, teams_joined: List[str], teams_left: List[str],
                                groups_joined: List[Dict[str, str]], groups_left: List[Dict[str, str]]) -> bool:
        """
        Update the team and group memberships of a user.
        :param username: The username of the user who is updating their team memberships.
        :param teams_joined: A list of team names that the user is requesting to join.
        :param teams_left: A list of team names that the user is requesting to leave.
        :param groups_joined: A list dictionaries containing a team name and a group name.  Each tuple represents a
        group that the user is requesting to join.
        :param groups_left: A list dictionaries containing a team name and a group name.  Each tuple represents a group
        that the user is requesting to leave.
        :return: True if the transaction is completed successfully, False otherwise.
        """
        teams_joined_dict = [TeamMember({
            'team_name': team_name,
            'username': username,
            'status': 'pending',
            'user': 'user',
            'deleted': False,
            'created_date': datetime.now(),
            'created_user': username,
            'created_app': 'saints-xctf-api'
        }) for team_name in teams_joined]

        teams_left_dict = [{'username': username, 'team_name': team_name} for team_name in teams_left]

        groups_joined_dict = [{**group_joined, 'username': username} for group_joined in groups_joined]

        groups_left_dict = [{**group_left, 'username': username} for group_left in groups_left]

        if len(teams_joined_dict) > 0:
            for team_membership in teams_joined_dict:
                existing_team_memberships = db.session.execute(
                    '''
                    SELECT team_name
                    FROM teammembers 
                    INNER JOIN teams ON teams.name=teammembers.team_name 
                    WHERE username=:username
                    AND teams.name=:team_name
                    AND teammembers.deleted IS FALSE
                    AND teams.deleted IS FALSE
                    ''',
                    {'username': username, 'team_name': team_membership.team_name}
                )

                if existing_team_memberships.rowcount > 0:
                    current_app.logger.warning(
                        f'The user {username} already has a membership to team {team_membership.team_name}.'
                    )
                else:
                    db.session.add(team_membership)

        if len(teams_left_dict) > 0:
            db.session.execute(
                '''
                UPDATE teammembers SET 
                    deleted = True,
                    deleted_date=CURRENT_TIMESTAMP(),
                    deleted_user=:username,
                    deleted_app='saints-xctf-api'
                WHERE username=:username
                AND team_name=:team_name
                AND deleted IS FALSE
                ''',
                teams_left_dict
            )

            db.session.execute(
                '''
                UPDATE groupmembers SET
                    deleted = TRUE,
                    deleted_date=CURRENT_TIMESTAMP(),
                    deleted_user=:username,
                    deleted_app='saints-xctf-api'
                WHERE username=:username
                AND group_id IN (
                    SELECT g.id
                    FROM `groups` g
                    INNER JOIN teamgroups tg ON g.id = tg.group_id
                    WHERE tg.team_name = :team_name
                    AND g.deleted IS FALSE
                    AND tg.deleted IS FALSE 
                );
                ''',
                teams_left_dict
            )

        if len(groups_joined_dict) > 0:
            for group_joined_dict in groups_joined_dict:
                existing_memberships: ResultProxy = db.session.execute(
                    '''
                    SELECT gm.* FROM groupmembers gm
                    INNER JOIN teamgroups tg on gm.group_id = tg.group_id
                    WHERE username = :username
                    AND gm.group_name = :group_name
                    AND tg.team_name = :team_name
                    AND gm.deleted IS FALSE
                    AND tg.deleted IS FALSE
                    ''',
                    group_joined_dict
                )

                already_team_member: ResultProxy = db.session.execute(
                    '''
                    SELECT * FROM teammembers
                    WHERE username = :username
                    AND team_name = :team_name
                    AND deleted IS FALSE
                    ''',
                    group_joined_dict
                )

                if existing_memberships.rowcount > 0:
                    current_app.logger.warning(
                        f'The user {username} already has a membership to group {group_joined_dict.get("group_name")} '
                        f'in team {group_joined_dict.get("team_name")}.'
                    )
                    continue

                if already_team_member.rowcount == 0 and group_joined_dict.get("team_name") not in teams_joined:
                    current_app.logger.warning(
                        f'The user {username} is not a member of the team {group_joined_dict.get("team_name")}, which '
                        f'the group {group_joined_dict.get("group_name")} is in.'
                    )
                    continue

                db.session.execute(
                    '''
                    INSERT INTO groupmembers (
                        group_id, 
                        group_name, 
                        username, 
                        status, 
                        user, 
                        deleted, 
                        created_date, 
                        created_user, 
                        created_app
                    ) VALUES (
                        (
                            SELECT g.id
                            FROM `groups` g
                            INNER JOIN teamgroups tg ON g.id = tg.group_id
                            WHERE tg.team_name = :team_name
                            AND tg.group_name = :group_name
                            AND g.deleted IS FALSE
                            AND tg.deleted IS FALSE
                        ), 
                        :group_name,
                        :username, 
                        'pending', 
                        'user', 
                        FALSE, 
                        CURRENT_TIMESTAMP(), 
                        :username, 
                        'saints-xctf-api'
                    )
                    ''',
                    group_joined_dict
                )

        if len(groups_left_dict) > 0:
            db.session.execute(
                '''
                UPDATE groupmembers SET
                    deleted = TRUE,
                    deleted_date=CURRENT_TIMESTAMP(),
                    deleted_user=:username,
                    deleted_app='saints-xctf-api'
                WHERE username=:username
                AND group_id = (
                    SELECT g.id
                    FROM `groups` g
                    INNER JOIN teamgroups tg ON g.id = tg.group_id
                    WHERE tg.team_name = :team_name
                    AND tg.group_name = :group_name
                    AND g.deleted IS FALSE
                    AND tg.deleted IS FALSE
                );
                ''',
                groups_left_dict
            )

        return BasicDao.safe_commit()
