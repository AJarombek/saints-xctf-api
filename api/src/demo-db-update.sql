-- Script with DML and DDL commands for updating a SQLite demo SaintsXCTF database.
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
DELETE FROM teamgroups;
DELETE FROM teammembers;

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
