-- Script with DML and DDL commands for updating a PostgreSQL test SaintsXCTF database.
-- Author: Andrew Jarombek
-- Date: 8/15/2022

DELETE FROM weekstart;

INSERT INTO weekstart(week_start) VALUES ('sunday');
INSERT INTO weekstart(week_start) VALUES ('monday');

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
    '$2a$10$5N1gLnRVmm1hZBRTfGx4wO5lnYEMgca6G1GhpOJ9qg1uuNM1ysGUC', -- apitest
    NULL,
    'snow-race-profile-picture.jpg',
    'I sometimes like to run...',
    '2016-12-23',
    2017,
    'New York, NY',
    'Shakeout',
    'aaaaaa',
    'andrew@jarombek.com',
    NOW(),
    'monday',
    'Y',
    0
);

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
    'dotty',
    'Dotty',
    'J',
    'aaa',
    '$2a$10$5N1gLnRVmm1hZBRTfGx4wO5lnYEMgca6G1GhpOJ9qg1uuNM1ysGUC',
    NULL,
    NULL,
    'Napping',
    '2016-12-23',
    2017,
    'New York, NY',
    'Nap',
    'aaaaaa',
    'dotty@horses.com',
    NOW(),
    'monday',
    'Y',
    0
);

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
    'grandma',
    'Mary',
    'Jarombek',
    'aaa',
    '$2a$10$5N1gLnRVmm1hZBRTfGx4wO5lnYEMgca6G1GhpOJ9qg1uuNM1ysGUC',
    NULL,
    NULL,
    'Knitting',
    '2016-12-23',
    2017,
    'Cos Cob, CT',
    'Knitting',
    'aaaaaa',
    'mary@jarombek.com',
    NOW(),
    'monday',
    'Y',
    0
);

DELETE FROM admins;

INSERT INTO admins(user) VALUES ('admin');
INSERT INTO admins(user) VALUES ('user');

DELETE FROM codes;

INSERT INTO codes(
    activation_code, email, group_id, expiration_date, deleted
) VALUES (
    'aaa111', 'andrew@jarombek.com', 1, NOW() + INTERVAL 1 DAY, 0
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

DELETE FROM status;

INSERT INTO status(status) VALUES ('accepted');
INSERT INTO status(status) VALUES ('pending');

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

INSERT INTO groupmembers(
    group_id, group_name, username, status, user, deleted
) VALUES (
    7, 'wmensxc', 'grandma', 'accepted', 'user', 0
);

INSERT INTO groupmembers(
    group_id, group_name, username, status, user, deleted
) VALUES (
    9, 'wmenstf', 'grandma', 'accepted', 'user', 0
);

DELETE FROM metrics;

INSERT INTO metrics(metric) VALUES ('miles');
INSERT INTO metrics(metric) VALUES ('kilometers');
INSERT INTO metrics(metric) VALUES ('meters');

DELETE FROM types;

INSERT INTO types (type) VALUES ('run');
INSERT INTO types (type) VALUES ('bike');
INSERT INTO types (type) VALUES ('swim');
INSERT INTO types (type) VALUES ('other');

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

INSERT INTO logs(
    username, first, last,
    name, location, date,
    type, distance, metric, miles,
    time, pace, feel,
    description, time_created, deleted
) VALUES (
    'andy', 'Andy', 'Jarombek',
    'CP', 'New York, NY', CURRENT_DATE() - INTERVAL 8 DAY,
    'run', 5.12, 'miles', 5.12,
    '00:39:03', '00:07:37', 6,
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
    'Longish', 'New York, NY', CURRENT_DATE() - INTERVAL 9 DAY,
    'run', 8.97, 'miles', 8.97,
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
    'Easy', 'New York, NY', CURRENT_DATE() - INTERVAL 10 DAY,
    'run', 6.55, 'miles', 6.55,
    '00:49:03', '00:07:29', 6,
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
    'Recovery', 'New York, NY', CURRENT_DATE() - INTERVAL 11 DAY,
    'run', 5.3, 'miles', 5.3,
    '00:39:56', '00:07:32', 7,
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
    'CPTC Tempo Workout', 'New York, NY', CURRENT_DATE() - INTERVAL 12 DAY,
    'run', 11.38, 'miles', 11.38,
    '01:17:54', '00:06:50', 7,
    '4mi @ HM, 8x1mi on/off', NOW(), 0
);

INSERT INTO logs(
    username, first, last,
    name, location, date,
    type, distance, metric, miles,
    time, pace, feel,
    description, time_created, deleted
) VALUES (
    'andy', 'Andy', 'Jarombek',
    'Recovery', 'New York, NY', CURRENT_DATE() - INTERVAL 13 DAY,
    'run', 4.31, 'miles', 4.31,
    '00:32:05', '00:07:26', 6,
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
    'CPTC Workout', 'New York, NY', CURRENT_DATE() - INTERVAL 14 DAY,
    'run', 11.15, 'miles', 11.15,
    '00:00:00', '00:00:00', 6,
    '2x400m, 2x1600m, 2x400m', NOW(), 0
);

INSERT INTO logs(
    username, first, last,
    name, location, date,
    type, distance, metric, miles,
    time, pace, feel,
    description, time_created, deleted
) VALUES (
    'andy', 'Andy', 'Jarombek',
    'Dingletown', 'Greenwich, CT', CURRENT_DATE() - INTERVAL 15 DAY,
    'run', 15.25, 'miles', 15.25,
    '01:51:23', '00:07:18', 7,
    'Lots of spontaneous route changes', NOW(), 0
);

INSERT INTO logs(
    username, first, last,
    name, location, date,
    type, distance, metric, miles,
    time, pace, feel,
    description, time_created, deleted
) VALUES (
    'andy', 'Andy', 'Jarombek',
    'Battle Road Twilight 1500m', 'Waltham, MA', CURRENT_DATE() - INTERVAL 16 DAY,
    'run', 7.45, 'miles', 7.45,
    '00:00:00', '00:00:00', 5,
    '4:21.50.  Continuing my string of sub-par performances, but the meet itself was very cool & got to see fellow alumni TC', NOW(), 0
);

INSERT INTO logs(
    username, first, last,
    name, location, date,
    type, distance, metric, miles,
    time, pace, feel,
    description, time_created, deleted
) VALUES (
    'andy', 'Andy', 'Jarombek',
    'Easy + Strides', 'New York, NY', CURRENT_DATE() - INTERVAL 17 DAY,
    'run', 5.34, 'miles', 5.34,
    '00:38:06', '00:07:08', 7,
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
    'Recovery', 'New York, NY', CURRENT_DATE() - INTERVAL 19 DAY,
    'run', 5.18, 'miles', 5.18,
    '00:38:42', '00:07:28', 5,
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
    'CPTC Track Workout', 'New York, NY', CURRENT_DATE() - INTERVAL 20 DAY,
    'run', 10.07, 'miles', 10.07,
    '00:00:00', '00:00:00', 6,
    '4x600m, 3x300m in the heat', NOW(), 0
);

INSERT INTO logs(
    username, first, last,
    name, location, date,
    type, distance, metric, miles,
    time, pace, feel,
    description, time_created, deleted
) VALUES (
    'andy', 'Andy', 'Jarombek',
    'Neighborhood', 'Riverside, CT', CURRENT_DATE() - INTERVAL 21 DAY,
    'run', 5.02, 'miles', 5.02,
    '00:37:53', '00:07:32', 6,
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
    'Tod''s Point', 'Old Greenwich, CT', CURRENT_DATE() - INTERVAL 22 DAY,
    'run', 5.76, 'miles', 5.76,
    '00:41:06', '00:07:08', 8,
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
    'Rockies', 'Sleepy Hollow, NY', CURRENT_DATE() - INTERVAL 23 DAY,
    'run', 15.25, 'miles', 15.25,
    '01:49:36', '00:07:11', 8,
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
    'Bridle Path', 'New York, NY', CURRENT_DATE() - INTERVAL 24 DAY,
    'run', 5.17, 'miles', 5.17,
    '00:38:38', '00:07:28', 6,
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
    'CPTC Workout', 'New York, NY', CURRENT_DATE() - INTERVAL 25 DAY,
    'run', 7.2, 'miles', 7.2,
    '00:00:00', '00:00:00', 9,
    '4x(400m, 200m) at 67-70 & 29-31.  Feeling strong in recent weeks', NOW(), 0
);

INSERT INTO logs(
    username, first, last,
    name, location, date,
    type, distance, metric, miles,
    time, pace, feel,
    description, time_created, deleted
) VALUES (
    'andy', 'Andy', 'Jarombek',
    'Bike', 'New York, NY', CURRENT_DATE() - INTERVAL 26 DAY,
    'bike', 1.75, 'miles', 1.75,
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
    'CPTC Workout', 'New York, NY', CURRENT_DATE() - INTERVAL 26 DAY,
    'run', 12.27, 'miles', 12.27,
    '00:00:00', '00:00:00', 9,
    '8x800m Workout, felt great.  2:27-2:30 for the reps', NOW(), 0
);

INSERT INTO logs(
    username, first, last,
    name, location, date,
    type, distance, metric, miles,
    time, pace, feel,
    description, time_created, deleted
) VALUES (
    'andy', 'Andy', 'Jarombek',
    'CP', 'New York, NY', CURRENT_DATE() - INTERVAL 27 DAY,
    'run', 4.32, 'miles', 4.32,
    '00:31:42', '00:07:20', 7,
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
    'Hot Long Run', 'New York, NY', CURRENT_DATE() - INTERVAL 28 DAY,
    'run', 14.02, 'miles', 14.02,
    '01:43:10', '00:07:21', 6,
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
    'Hot', 'New York, NY', CURRENT_DATE() - INTERVAL 29 DAY,
    'run', 5.61, 'miles', 5.61,
    '00:41:48', '00:07:27', 4,
    'Pushing the long run to tomorrow, that was brutal', NOW(), 0
);

INSERT INTO logs(
    username, first, last,
    name, location, date,
    type, distance, metric, miles,
    time, pace, feel,
    description, time_created, deleted
) VALUES (
    'andy', 'Andy', 'Jarombek',
    'Tracksmith Community Mile', 'New York, NY', CURRENT_DATE() - INTERVAL 30 DAY,
    'run', 14.65, 'miles', 14.65,
    '00:00:00', '00:00:00', 7,
    'Death, taxes, and running 4:40 for the mile. At least tried to make a high mileage day out of it', NOW(), 0
);

INSERT INTO logs(
    username, first, last,
    name, location, date,
    type, distance, metric, miles,
    time, pace, feel,
    description, time_created, deleted
) VALUES (
    'andy', 'Andy', 'Jarombek',
    'Pre Race Day', 'New York, NY', CURRENT_DATE() - INTERVAL 31 DAY,
    'run', 5.26, 'miles', 5.26,
    '00:37:56', '00:07:12', 7,
    NULL, NOW(), 0
);

INSERT INTO logs(
    username, first, last,
    name, location, date,
    type, distance, metric, miles,
    time, pace, feel,
    description, time_created, deleted
) VALUES (
    'dotty', 'Dotty', 'J',
    'Nap', 'New York, NY', CURRENT_DATE() - INTERVAL 31 DAY,
    'run', 0.1, 'meters', 0,
    '00:00:00', '00:00:00', 9,
    NULL, NOW(), 0
);

INSERT INTO logs(
    username, first, last,
    name, location, date,
    type, distance, metric, miles,
    time, pace, feel,
    description, time_created, deleted
) VALUES (
    'grandma', 'Mary', 'Jarombek',
    'Walk', 'Cos Cob, CT', CURRENT_DATE() - INTERVAL 1 DAY,
    'other', 1, 'miles', 1,
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
    'grandma', 'Mary', 'Jarombek',
    'Walk', 'Cos Cob, CT', CURRENT_DATE() - INTERVAL 1 DAY,
    'run', 1, 'miles', 1,
    '00:00:00', '00:00:00', 6,
    NULL, NOW(), 0
);

DELETE FROM comments;

INSERT INTO comments(
    comment_id, username, first, last, log_id, time, content, deleted
) VALUES (
    1, 'andy', 'Andy', 'Jarombek', 1, NOW() - INTERVAL 12 HOUR, 'First Comment', 0
);

INSERT INTO comments(
    comment_id, username, first, last, log_id, time, content, deleted
) VALUES (
    2, 'dotty', 'Dotty', 'J', 1, NOW() - INTERVAL 12 HOUR, 'Second Comment', 0
);

DELETE FROM notifications;

INSERT INTO notifications(
    username, time, link, viewed, description, deleted
) VALUES (
    'andy', NOW(), 'https://www.saintsxctf.com/log.php?logno=1', 'N', 'Dotty J Commented on Your Log', 0
);

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

INSERT INTO teammembers (
    team_name, username, status, user, deleted
) VALUES (
    'saintsxctf', 'grandma', 'accepted', 'user', 0
);
