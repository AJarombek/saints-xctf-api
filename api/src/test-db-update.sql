-- Script with DML and DDL commands for updating a PostgreSQL test SaintsXCTF database.
-- Author: Andrew Jarombek
-- Date: 8/15/2022

DELETE FROM admins;

INSERT INTO admins(user) VALUES ('admin');
INSERT INTO admins(user) VALUES ('user');

DELETE FROM codes;

INSERT INTO codes(
    activation_code, email, group_id, expiration_date, deleted
) VALUES (
    'abc123', 'andrew@jarombek.com', 1, NOW() + INTERVAL 1 DAY, 0
);

DELETE FROM comments;

INSERT INTO comments(
    username, first, last, log_id, time, content, deleted
) VALUES (
    'andy', 'Andy', 'Jarombek', 1, NOW() - INTERVAL 12 HOUR, 'First Comment', 0
);

DELETE FROM flair;

INSERT INTO flair(
    username, flair, deleted
) VALUES (
    'andy', 'Site Creator', 0
);

DELETE FROM forgotpassword;

INSERT INTO forgotpassword(
    forgot_code, username, expires, deleted
) VALUES (
    'ABCD1234', 'andy', NOW() + INTERVAL 1 DAY, 0
);

DELETE FROM groups;

INSERT INTO groups(
    id, group_name, group_title, description, week_start, deleted
) VALUES (
    1, 'alumni', 'Alumni', NULL, 'sunday', 0
);

INSERT INTO groups(
    id, group_name, group_title, description, week_start, deleted
) VALUES (
    2, 'friends', 'Andy & Friends', NULL, 'sunday', 0
);

INSERT INTO groups(
    id, group_name, group_title, description, week_start, deleted
) VALUES (
    3, 'jarombek', 'Jarombek Family', NULL, 'sunday', 0
);

INSERT INTO groups(
    id, group_name, group_title, description, week_start, deleted
) VALUES (
    4, 'menstf', 'Men''s Track & Field', 'Go Saints!', 'sunday', 0
);

INSERT INTO groups(
    id, group_name, group_title, description, week_start, deleted
) VALUES (
    5, 'mensxc', 'Men''s Cross Country', 'Joust!', 'sunday', 0
);

INSERT INTO groups(
    id, group_name, group_title, description, week_start, deleted
) VALUES (
    6, 'tf_alumni', 'Track & Field Alumni', NULL, 'sunday', 0
);

INSERT INTO groups(
    id, group_name, group_title, description, week_start, deleted
) VALUES (
    7, 'wmensxc', 'Women''s Cross Country', 'Gung Ho!', 'sunday', 0
);

INSERT INTO groups(
    id, group_name, group_title, description, week_start, deleted
) VALUES (
    8, 'xc_alumni', 'Cross Country Alumni', NULL, 'sunday', 0
);

INSERT INTO groups(
    id, group_name, group_title, description, week_start, deleted
) VALUES (
    9, 'wmenstf', 'Women''s Track & Field', 'Go Saints!', 'sunday', 0
);

DELETE FROM groupmembers;

INSERT INTO groupmembers(
    group_id, group_name, username, status, user, deleted
) VALUES (
    1, 'alumni', 'andy', 'accepted', 'admin', 0
);

INSERT INTO groupmembers(
    group_id, group_name, username, status, user, deleted
) VALUES (
    9, 'xc_alumni', 'andy', 'accepted', 'admin', 0
);

INSERT INTO groupmembers(
    group_id, group_name, username, status, user, deleted
) VALUES (
    6, 'tf_alumni', 'andy', 'accepted', 'admin', 0
);

INSERT INTO groupmembers(
    group_id, group_name, username, status, user, deleted
) VALUES (
    2, 'friends', 'andy', 'accepted', 'admin', 0
);

INSERT INTO groupmembers(
    group_id, group_name, username, status, user, deleted
) VALUES (
    3, 'jarombek', 'andy', 'accepted', 'admin', 0
);

DELETE FROM logs;

INSERT INTO logs(
    username, first, last,
    name, location, date,
    type, distance, metric, miles,
    time, pace, feel,
    description, time_created, deleted
) VALUES (
    'andy', 'Andy', 'Jarombek',
    'Citi Bike', 'New York, NY', CURRENT_DATE(),
    'bike', 7.5, 'miles', 7.5,
    '00:00:00', '00:00:00', 6,
    'Citi biking through Harlem to practice, nice little adventure', NOW(), 0
);

INSERT INTO logs(
    username, first, last,
    name, location, date,
    type, distance, metric, miles,
    time, pace, feel,
    description, time_created, deleted
) VALUES (
    'andy', 'Andy', 'Jarombek',
    'CPTC Track Workout', 'New York, NY', CURRENT_DATE(),
    'run', 6.15, 'miles', 6.15,
    '00:00:00', '00:00:00', 6,
    '4x600m @ mile pace (1:42, 1:44, 1:43, 1:44). Felt difficult', NOW(), 0
);

INSERT INTO logs(
    username, first, last,
    name, location, date,
    type, distance, metric, miles,
    time, pace, feel,
    description, time_created, deleted
) VALUES (
    'andy', 'Andy', 'Jarombek',
    'Central Park', 'New York, NY', CURRENT_DATE() - INTERVAL 1 DAY,
    'run', 5.14, 'miles', 5.14,
    '00:38:52', '00:07:33', 6,
    NULL, NOW(), 0
);

INSERT INTO logs(
    username, first, last,
    name, location, date,
    type, distance, metric, miles,
    time, pace, feel,
    description, time_created, deleted
) VALUES (
    'andy', 'Andy', 'Jarombek',
    'CP Long', 'New York, NY', CURRENT_DATE() - INTERVAL 2 DAY,
    'run', 12.79, 'miles', 12.79,
    '01:36:06', '00:07:30', 6,
    NULL, NOW(), 0
);

INSERT INTO logs(
    username, first, last,
    name, location, date,
    type, distance, metric, miles,
    time, pace, feel,
    description, time_created, deleted
) VALUES (
    'andy', 'Andy', 'Jarombek',
    'Cooldown', 'New York, NY', CURRENT_DATE() - INTERVAL 3 DAY,
    'bike', 5.35, 'miles', 5.35,
    '00:00:00', '00:00:00', 7,
    NULL, NOW(), 0
);

INSERT INTO logs(
    username, first, last,
    name, location, date,
    type, distance, metric, miles,
    time, pace, feel,
    description, time_created, deleted
) VALUES (
    'andy', 'Andy', 'Jarombek',
    'Queens 10K', 'Queens, NY', CURRENT_DATE() - INTERVAL 3 DAY,
    'run', 10.4, 'miles', 10.4,
    '00:00:00', '00:00:00', 3,
    'Mad stomach', NOW(), 0
);

INSERT INTO logs(
    username, first, last,
    name, location, date,
    type, distance, metric, miles,
    time, pace, feel,
    description, time_created, deleted
) VALUES (
    'andy', 'Andy', 'Jarombek',
    'Pre Race', 'New York, NY', CURRENT_DATE() - INTERVAL 4 DAY,
    'run', 5.66, 'miles', 5.66,
    '00:41:39', '00:07:21', 7,
    NULL, NOW(), 0
);

INSERT INTO logs(
    username, first, last,
    name, location, date,
    type, distance, metric, miles,
    time, pace, feel,
    description, time_created, deleted
) VALUES (
    'andy', 'Andy', 'Jarombek',
    'Citi Bike', 'New York, NY', CURRENT_DATE() - INTERVAL 5 DAY,
    'bike', 8.19, 'miles', 8.19,
    '00:00:00', '00:00:00', 6,
    NULL, NOW(), 0
);

INSERT INTO logs(
    username, first, last,
    name, location, date,
    type, distance, metric, miles,
    time, pace, feel,
    description, time_created, deleted
) VALUES (
    'andy', 'Andy', 'Jarombek',
    'CP', 'New York, NY', CURRENT_DATE() - INTERVAL 6 DAY,
    'run', 5.03, 'miles', 5.03,
    '00:38:21', '00:07:37', 7,
    NULL, NOW(), 0
);

INSERT INTO logs(
    username, first, last,
    name, location, date,
    type, distance, metric, miles,
    time, pace, feel,
    description, time_created, deleted
) VALUES (
    'andy', 'Andy', 'Jarombek',
    'To Practice', 'New York, NY', CURRENT_DATE() - INTERVAL 7 DAY,
    'bike', 1.54, 'miles', 1.54,
    '00:00:00', '00:00:00', 6,
    NULL, NOW(), 0
);

INSERT INTO logs(
    username, first, last,
    name, location, date,
    type, distance, metric, miles,
    time, pace, feel,
    description, time_created, deleted
) VALUES (
    'andy', 'Andy', 'Jarombek',
    'CPTC Workout', 'New York, NY', CURRENT_DATE() - INTERVAL 7 DAY,
    'run', 11.52, 'miles', 11.52,
    '00:00:00', '00:00:00', 7,
    '2x400m, 2x1600m, 2x400m', NOW(), 0
);

DELETE FROM metrics;

INSERT INTO metrics(metric) VALUES ('miles');
INSERT INTO metrics(metric) VALUES ('kilometers');
INSERT INTO metrics(metric) VALUES ('meters');

DELETE FROM notifications;

DELETE FROM status;

INSERT INTO status(status) VALUES ('accepted');
INSERT INTO status(status) VALUES ('pending');

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

INSERT INTO teamgroups (
    team_name, group_id, group_name, deleted
) VALUES (
    'saintsxctf', 1, 'alumni', 0
);

INSERT INTO teamgroups (
    team_name, group_id, group_name, deleted
) VALUES (
    'saintsxctf', 4, 'menstf', 0
);

INSERT INTO teamgroups (
    team_name, group_id, group_name, deleted
) VALUES (
    'saintsxctf', 5, 'mensxc', 0
);

INSERT INTO teamgroups (
    team_name, group_id, group_name, deleted
) VALUES (
    'saintsxctf', 7, 'wmenstf', 0
);

INSERT INTO teamgroups (
    team_name, group_id, group_name, deleted
) VALUES (
    'saintsxctf', 8, 'wmensxc', 0
);

INSERT INTO teamgroups (
    team_name, group_id, group_name, deleted
) VALUES (
    'saintsxctf_alumni', 9, 'xc_alumni', 0
);

INSERT INTO teamgroups (
    team_name, group_id, group_name, deleted
) VALUES (
    'saintsxctf_alumni', 6, 'tf_alumni', 0
);

INSERT INTO teamgroups (
    team_name, group_id, group_name, deleted
) VALUES (
    'friends', 2, 'friends', 0
);

INSERT INTO teamgroups (
    team_name, group_id, group_name, deleted
) VALUES (
    'jarombek', 3, 'jarombek', 0
);

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

DELETE FROM types;

INSERT INTO types (type) VALUES ('run');
INSERT INTO types (type) VALUES ('bike');
INSERT INTO types (type) VALUES ('swim');
INSERT INTO types (type) VALUES ('other');

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

DELETE FROM weekstart;

INSERT INTO weekstart(week_start) VALUES ('sunday');
INSERT INTO weekstart(week_start) VALUES ('monday');
