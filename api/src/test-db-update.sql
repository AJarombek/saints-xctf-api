-- Script with DML and DDL commands for updating a PostgreSQL test SaintsXCTF database.
-- Author: Andrew Jarombek
-- Date: 8/15/2022

DELETE FROM codes;
DELETE FROM comments;
DELETE FROM flair;
DELETE FROM forgotpassword;
DELETE FROM groups;
DELETE FROM groupmembers;
DELETE FROM logs;
DELETE FROM notifications;
DELETE FROM teams;
INSERT INTO teams (
    name,
    title,
    picture_name,
    description,
    week_start,
    deleted
) VALUES (
    'friends',
    'Andy & Friends',
    NULL,
    NULL,
    'monday',
    0
);

INSERT INTO teams (
    name,
    title,
    picture_name,
    description,
    week_start,
    deleted
) VALUES (
    'jarombek',
    'Jarombek Family',
    NULL,
    NULL,
    'monday',
    0
);

INSERT INTO teams (
    name,
    title,
    picture_name,
    description,
    week_start,
    deleted
) VALUES (
    'saintsxctf',
    'St. Lawrence Cross Country and Track & Field',
    NULL,
    NULL,
    'monday',
    0
);

INSERT INTO teams (
    name,
    title,
    picture_name,
    description,
    week_start,
    deleted
) VALUES (
    'saintsxctf_alumni',
    'SaintsXCTF Alumni',
    NULL,
    NULL,
    'monday',
    0
);

DELETE FROM teamgroups;
DELETE FROM teammembers;
INSERT INTO teammembers (
    team_name, username, status, user, deleted
) VALUES (
    'saintsxctf', 'andy', 'accepted', 'admin', 0
);

INSERT INTO teammembers (
    team_name, username, status, user, deleted
) VALUES (
    'saintsxctf_alumni', 'andy', 'accepted', 'admin', 0
);

INSERT INTO teammembers (
    team_name, username, status, user, deleted
) VALUES (
    'friends', 'andy', 'accepted', 'admin', 0
);

INSERT INTO teammembers (
    team_name, username, status, user, deleted
) VALUES (
    'jarombek', 'andy', 'accepted', 'admin', 0
);

DELETE FROM users;
INSERT INTO users (
    username,
    first,
    last,
    salt,
    password,
    profilepic,
    profilepic_name,
    description,
    member_since,
    class_year,
    location,
    favorite_event,
    activation_code,
    email,
    last_signin,
    week_start,
    subscribed,
    deleted
) VALUES (
    'andy',
    'Andy',
    'Jarombek',
    'aaa',
    'aaa',
    NULL,
    'snow-race-profile-picture.jpg',
    'I sometimes like to run...',
    '2016-12-23',
    2017,
    'New York, NY',
    'Shakeout',
    'aaaaaa',
    'andrew@jarombek.com',
    NULL,
    'monday',
    'subscribed',
    0
);