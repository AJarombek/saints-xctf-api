"""
TeamMember data access from the SaintsXCTF MySQL database.  Contains SQL queries related to users
who are members of a team.  Most team data is accessed from a separate TeamDao.
Author: Andrew Jarombek
Date: 11/29/2020
"""

from typing import List, Dict
from datetime import datetime

from sqlalchemy.engine import ResultProxy
from flask import current_app

from database import db
from dao.basicDao import BasicDao
from model.TeamMember import TeamMember


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
            AND (teammembers.deleted IS NULL OR teammembers.deleted <> 'Y')
            AND (teams.deleted IS NULL OR teams.deleted <> 'Y')
            ''',
            {'username': username}
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
            AND (teammembers.deleted IS NULL OR teammembers.deleted <> 'Y')
            AND (teams.deleted IS NULL OR teams.deleted <> 'Y')
            AND (users.deleted IS NULL OR users.deleted <> 'Y')
            ''',
            {'team_name': team_name}
        )

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
            'deleted': 'N',
            'created_date': datetime.now(),
            'created_user': username,
            'created_app': 'saints-xctf-api'
        }) for team_name in teams_joined]

        teams_left_dict = [{'username': username, 'team_name': team_name} for team_name in teams_left]

        groups_joined_dict = [{**group_joined, 'username': username} for group_joined in groups_joined]

        groups_left_dict = [{**group_left, 'username': username} for group_left in groups_left]

        if len(teams_joined_dict) > 0:
            for team_membership in teams_joined_dict:
                db.session.add(team_membership)

        if len(teams_left_dict) > 0:
            db.session.execute(
                '''
                UPDATE teammembers SET 
                    deleted = 'Y',
                    deleted_date=CURRENT_TIMESTAMP(),
                    deleted_user=:username,
                    deleted_app='saints-xctf-api'
                WHERE username=:username
                AND team_name=:team_name
                AND (deleted IS NULL OR deleted <> 'Y')
                ''',
                teams_left_dict
            )

            db.session.execute(
                '''
                UPDATE groupmembers SET
                    deleted = 'Y',
                    deleted_date=CURRENT_TIMESTAMP(),
                    deleted_user=:username,
                    deleted_app='saints-xctf-api'
                WHERE username=:username
                AND group_id IN (
                    SELECT g.id
                    FROM `groups` g
                    INNER JOIN teamgroups tg ON g.id = tg.group_id
                    WHERE tg.team_name = :team_name
                    AND (g.deleted IS NULL OR g.deleted <> 'Y')
                    AND (tg.deleted IS NULL OR tg.deleted <> 'Y')
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
                    AND (gm.deleted IS NULL OR gm.deleted <> 'Y')
                    AND (tg.deleted IS NULL OR tg.deleted <> 'Y')
                    ''',
                    group_joined_dict
                )

                already_team_member: ResultProxy = db.session.execute(
                    '''
                    SELECT * FROM teammembers
                    WHERE username = :username
                    AND team_name = :team_name
                    AND (deleted IS NULL OR deleted <> 'Y')
                    ''',
                    group_joined_dict
                )

                if existing_memberships.rowcount > 0:
                    current_app.logger.warning(
                        f'The user already has a membership to group {group_joined_dict.get("group_name")} '
                        f'in team {group_joined_dict.get("team_name")}.'
                    )
                    continue

                if already_team_member.rowcount == 0 and group_joined_dict.get("team_name") not in teams_joined:
                    current_app.logger.warning(
                        f'The user is not a member of the team {group_joined_dict.get("team_name")}, which the '
                        f'group {group_joined_dict.get("group_name")} is in.'
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
                            AND (g.deleted IS NULL OR g.deleted <> 'Y')
                            AND (tg.deleted IS NULL OR tg.deleted <> 'Y')
                        ), 
                        :group_name,
                        :username, 
                        'pending', 
                        'user', 
                        'N', 
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
                    deleted = 'Y',
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
                    AND (g.deleted IS NULL OR g.deleted <> 'Y')
                    AND (tg.deleted IS NULL OR tg.deleted <> 'Y')
                );
                ''',
                groups_left_dict
            )

        return BasicDao.safe_commit()
