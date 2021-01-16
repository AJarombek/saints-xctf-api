"""
GroupMember data access from the SaintsXCTF MySQL database.  Contains SQL queries related to users
who are members of a group.  Most group data is accessed from a separate GroupDao.
Author: Andrew Jarombek
Date: 7/2/2019
"""

from sqlalchemy.engine import ResultProxy

from database import db


class GroupMemberDao:

    @staticmethod
    def get_user_groups(username: str) -> ResultProxy:
        """
        Get information about all the groups a user is a member of
        :param username: Unique identifier for the user
        :return: A list of groups
        """
        return db.session.execute(
            '''
            SELECT groupmembers.group_name,group_title,status,user 
            FROM groupmembers 
            INNER JOIN `groups` ON `groups`.group_name=groupmembers.group_name 
            WHERE username=:username
            AND (groupmembers.deleted IS NULL OR groupmembers.deleted <> 'Y')
            AND (`groups`.deleted IS NULL OR `groups`.deleted <> 'Y')
            ''',
            {'username': username}
        )

    @staticmethod
    def get_user_groups_in_team(username: str, team_name: str) -> ResultProxy:
        """
        Get information about all the groups a user is a member of within a team
        :param username: Unique identifier for the user
        :param team_name: Unique name for a team
        :return: A list of groups
        """
        return db.session.execute(
            '''
            SELECT groupmembers.group_name,groupmembers.group_id,group_title,status,user 
            FROM groupmembers 
            INNER JOIN `groups` ON `groups`.group_name=groupmembers.group_name 
            INNER JOIN teamgroups ON teamgroups.group_id=`groups`.id
            INNER JOIN teams ON teams.name=teamgroups.team_name 
            WHERE username=:username
            AND teams.name=:team_name
            AND (groupmembers.deleted IS NULL OR groupmembers.deleted <> 'Y')
            AND (`groups`.deleted IS NULL OR `groups`.deleted <> 'Y')
            AND (teamgroups.deleted IS NULL OR teamgroups.deleted <> 'Y')
            AND (teams.deleted IS NULL OR teams.deleted <> 'Y')
            ''',
            {'username': username, 'team_name': team_name}
        )

    @staticmethod
    def get_group_members(group_name: str, team_name: str) -> ResultProxy:
        """
        Get the users who are members of a group.
        :param group_name: Unique name of a group.
        :param team_name: Unique name for a team.
        :return: A list of group members.
        """
        return db.session.execute(
            '''
            SELECT users.username,first,last,member_since,user,status 
            FROM groupmembers 
            INNER JOIN `groups` ON `groups`.group_name=groupmembers.group_name 
            INNER JOIN teamgroups ON teamgroups.group_id=`groups`.id
            INNER JOIN users ON groupmembers.username=users.username 
            WHERE groupmembers.group_name=:group_name
            AND teamgroups.team_name=:team_name
            AND (groupmembers.deleted IS NULL OR groupmembers.deleted <> 'Y')
            AND (`groups`.deleted IS NULL OR `groups`.deleted <> 'Y')
            AND (teamgroups.deleted IS NULL OR teamgroups.deleted <> 'Y')
            AND (users.deleted IS NULL OR users.deleted <> 'Y')
            ''',
            {'group_name': group_name, 'team_name': team_name}
        )

    @staticmethod
    def get_group_members_by_id(group_id: str) -> ResultProxy:
        """
        Get the users who are members of a group.
        :param group_id: Unique id of a group.
        :return: A list of group members.
        """
        return db.session.execute(
            '''
            SELECT users.username,first,last,member_since,user,status 
            FROM groupmembers 
            INNER JOIN users ON groupmembers.username=users.username 
            WHERE groupmembers.group_id=:group_id
            AND (groupmembers.deleted IS NULL OR groupmembers.deleted <> 'Y')
            AND (users.deleted IS NULL OR users.deleted <> 'Y')
            ''',
            {'group_id': group_id}
        )
