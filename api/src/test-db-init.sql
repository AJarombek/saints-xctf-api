-- Script with DDL commands for a PostgreSQL test SaintsXCTF database.
-- Author: Andrew Jarombek
-- Date: 11/8/2022

SET foreign_key_checks = 0;

DROP TABLE IF EXISTS messages;
DROP TABLE IF EXISTS comments;
DROP TABLE IF EXISTS logs;
DROP TABLE IF EXISTS teammembers;
DROP TABLE IF EXISTS notifications;
DROP TABLE IF EXISTS events;
DROP TABLE IF EXISTS flair;
DROP TABLE IF EXISTS forgotpassword;
DROP TABLE IF EXISTS groupmembers;
DROP TABLE IF EXISTS teamgroups;
DROP TABLE IF EXISTS teams;
DROP TABLE IF EXISTS admins;
DROP TABLE IF EXISTS status;
DROP TABLE IF EXISTS codes;
DROP TABLE IF EXISTS metrics;
DROP TABLE IF EXISTS types;
DROP TABLE IF EXISTS `groups`;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS weekstart;

CREATE TABLE IF NOT EXISTS admins(
    user VARCHAR(10) NOT NULL PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS codes(
    activation_code VARCHAR(8)  NOT NULL PRIMARY KEY,
    email           VARCHAR(50) NULL,
    group_id        INT         NULL,
    expiration_date DATETIME    NULL,
    deleted         TINYINT(1)  NULL,
    created_date    DATETIME    NULL,
    created_user    VARCHAR(31) NULL,
    created_app     VARCHAR(31) NULL,
    modified_date   DATETIME    NULL,
    modified_user   VARCHAR(31) NULL,
    modified_app    VARCHAR(31) NULL,
    deleted_date    DATETIME    NULL,
    deleted_user    VARCHAR(31) NULL,
    deleted_app     VARCHAR(31) NULL
);

CREATE TABLE IF NOT EXISTS comments(
    comment_id    INT AUTO_INCREMENT PRIMARY KEY,
    username      VARCHAR(20)   NOT NULL,
    first         VARCHAR(30)   NOT NULL,
    last          VARCHAR(30)   NOT NULL,
    log_id        INT           NOT NULL,
    time          DATETIME      NOT NULL,
    content       VARCHAR(1000) NULL,
    deleted       TINYINT(1)    NULL,
    created_date  DATETIME      NULL,
    created_user  VARCHAR(31)   NULL,
    created_app   VARCHAR(31)   NULL,
    modified_date DATETIME      NULL,
    modified_user VARCHAR(31)   NULL,
    modified_app  VARCHAR(31)   NULL,
    deleted_date  DATETIME      NULL,
    deleted_user  VARCHAR(31)   NULL,
    deleted_app   VARCHAR(31)   NULL
);

CREATE TABLE IF NOT EXISTS events(
    event_id      INT AUTO_INCREMENT PRIMARY KEY,
    name          VARCHAR(20) NOT NULL,
    group_name    VARCHAR(50) NOT NULL,
    start_date    VARCHAR(50) NOT NULL,
    end_date      VARCHAR(50) NULL,
    start_time    VARCHAR(50) NULL,
    end_time      VARCHAR(50) NULL,
    description   VARCHAR(50) NULL,
    deleted       TINYINT(1)  NULL,
    created_date  DATETIME    NULL,
    created_user  VARCHAR(31) NULL,
    created_app   VARCHAR(31) NULL,
    modified_date DATETIME    NULL,
    modified_user VARCHAR(31) NULL,
    modified_app  VARCHAR(31) NULL,
    deleted_date  DATETIME    NULL,
    deleted_user  VARCHAR(31) NULL,
    deleted_app   VARCHAR(31) NULL
);

CREATE TABLE IF NOT EXISTS flair(
    flair_id      INT AUTO_INCREMENT PRIMARY KEY,
    username      VARCHAR(20) NULL,
    flair         VARCHAR(50) NULL,
    deleted       TINYINT(1)  NULL,
    created_date  DATETIME    NULL,
    created_user  VARCHAR(31) NULL,
    created_app   VARCHAR(31) NULL,
    modified_date DATETIME    NULL,
    modified_user VARCHAR(31) NULL,
    modified_app  VARCHAR(31) NULL,
    deleted_date  DATETIME    NULL,
    deleted_user  VARCHAR(31) NULL,
    deleted_app   VARCHAR(31) NULL
);

CREATE TABLE IF NOT EXISTS forgotpassword(
    forgot_code   VARCHAR(8)  NOT NULL PRIMARY KEY,
    username      VARCHAR(20) NOT NULL,
    expires       DATETIME    NOT NULL,
    deleted       TINYINT(1)  NULL,
    created_date  DATETIME    NULL,
    created_user  VARCHAR(31) NULL,
    created_app   VARCHAR(31) NULL,
    modified_date DATETIME    NULL,
    modified_user VARCHAR(31) NULL,
    modified_app  VARCHAR(31) NULL,
    deleted_date  DATETIME    NULL,
    deleted_user  VARCHAR(31) NULL,
    deleted_app   VARCHAR(31) NULL
);

CREATE TABLE IF NOT EXISTS groupmembers(
    id            INT AUTO_INCREMENT PRIMARY KEY,
    group_id      INT                  NULL,
    group_name    VARCHAR(20)          NULL,
    username      VARCHAR(20)          NULL,
    status        VARCHAR(10)          NULL,
    user          VARCHAR(10)          NULL,
    deleted       TINYINT(1) DEFAULT 0 NULL,
    created_date  DATETIME             NULL,
    created_user  VARCHAR(31)          NULL,
    created_app   VARCHAR(31)          NULL,
    modified_date DATETIME             NULL,
    modified_user VARCHAR(31)          NULL,
    modified_app  VARCHAR(31)          NULL,
    deleted_date  DATETIME             NULL,
    deleted_user  VARCHAR(31)          NULL,
    deleted_app   VARCHAR(31)          NULL
);

CREATE TABLE IF NOT EXISTS `groups`(
    id            INT AUTO_INCREMENT PRIMARY KEY,
    group_name    VARCHAR(20)  NOT NULL,
    group_title   VARCHAR(50)  NULL,
    grouppic      LONGBLOB     NULL,
    grouppic_name VARCHAR(50)  NULL,
    description   VARCHAR(255) NULL,
    week_start    VARCHAR(15)  NULL,
    deleted       TINYINT(1)   NULL,
    created_date  DATETIME     NULL,
    created_user  VARCHAR(31)  NULL,
    created_app   VARCHAR(31)  NULL,
    modified_date DATETIME     NULL,
    modified_user VARCHAR(31)  NULL,
    modified_app  VARCHAR(31)  NULL,
    deleted_date  DATETIME     NULL,
    deleted_user  VARCHAR(31)  NULL,
    deleted_app   VARCHAR(31)  NULL
);

CREATE TABLE IF NOT EXISTS logs(
    log_id        INT AUTO_INCREMENT PRIMARY KEY,
    username      VARCHAR(20)          NOT NULL,
    first         VARCHAR(30)          NOT NULL,
    last          VARCHAR(30)          NOT NULL,
    name          VARCHAR(40)          NULL,
    location      VARCHAR(50)          NULL,
    date          DATE                 NOT NULL,
    type          VARCHAR(40)          NOT NULL,
    distance      FLOAT                NULL,
    metric        VARCHAR(15)          NULL,
    miles         FLOAT                NULL,
    time          TIME                 NULL,
    pace          TIME                 NULL,
    feel          INT(2)               NOT NULL,
    description   VARCHAR(1000)        NULL,
    time_created  DATETIME             NOT NULL,
    deleted       TINYINT(1) DEFAULT 0 NULL,
    created_date  DATETIME             NULL,
    created_user  VARCHAR(31)          NULL,
    created_app   VARCHAR(31)          NULL,
    modified_date DATETIME             NULL,
    modified_user VARCHAR(31)          NULL,
    modified_app  VARCHAR(31)          NULL,
    deleted_date  DATETIME             NULL,
    deleted_user  VARCHAR(31)          NULL,
    deleted_app   VARCHAR(31)          NULL
);

CREATE TABLE IF NOT EXISTS metrics(
    metric VARCHAR(15) NOT NULL PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS notifications(
    notification_id INT AUTO_INCREMENT PRIMARY KEY,
    username        VARCHAR(20)          NOT NULL,
    time            DATETIME             NOT NULL,
    link            VARCHAR(127)         NULL,
    viewed          CHAR                 NOT NULL,
    description     VARCHAR(1000)        NULL,
    deleted         TINYINT(1) DEFAULT 0 NULL,
    created_date    DATETIME             NULL,
    created_user    VARCHAR(31)          NULL,
    created_app     VARCHAR(31)          NULL,
    modified_date   DATETIME             NULL,
    modified_user   VARCHAR(31)          NULL,
    modified_app    VARCHAR(31)          NULL,
    deleted_date    DATETIME             NULL,
    deleted_user    VARCHAR(31)          NULL,
    deleted_app     VARCHAR(31)          NULL
);

CREATE TABLE IF NOT EXISTS status(
    status VARCHAR(10) NOT NULL PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS teamgroups(
    team_name     VARCHAR(31) CHARSET UTF8 NOT NULL,
    group_id      INT                      NOT NULL,
    group_name    VARCHAR(20)              NOT NULL,
    deleted       TINYINT(1) DEFAULT 0     NULL,
    created_date  DATETIME                 NULL,
    created_user  VARCHAR(31)              NULL,
    created_app   VARCHAR(31)              NULL,
    modified_date DATETIME                 NULL,
    modified_user VARCHAR(31)              NULL,
    modified_app  VARCHAR(31)              NULL,
    deleted_date  DATETIME                 NULL,
    deleted_user  VARCHAR(31)              NULL,
    deleted_app   VARCHAR(31)              NULL
);

CREATE TABLE IF NOT EXISTS teammembers(
    team_name     VARCHAR(31) CHARSET UTF8 NOT NULL,
    username      VARCHAR(20)              NOT NULL,
    status        VARCHAR(10)              NOT NULL,
    user          VARCHAR(10)              NOT NULL,
    deleted       TINYINT(1) DEFAULT 0     NULL,
    created_date  DATETIME                 NULL,
    created_user  VARCHAR(31)              NULL,
    created_app   VARCHAR(31)              NULL,
    modified_date DATETIME                 NULL,
    modified_user VARCHAR(31)              NULL,
    modified_app  VARCHAR(31)              NULL,
    deleted_date  DATETIME                 NULL,
    deleted_user  VARCHAR(31)              NULL,
    deleted_app   VARCHAR(31)              NULL
);

CREATE TABLE IF NOT EXISTS teams(
    name          VARCHAR(31) CHARSET UTF8  NOT NULL PRIMARY KEY,
    title         VARCHAR(127) CHARSET UTF8 NOT NULL,
    picture_name  VARCHAR(255)              NULL,
    description   VARCHAR(255)              NULL,
    week_start    VARCHAR(15)               NULL,
    deleted       TINYINT(1) DEFAULT 0      NULL,
    created_date  DATETIME                  NULL,
    created_user  VARCHAR(31)               NULL,
    created_app   VARCHAR(31)               NULL,
    modified_date DATETIME                  NULL,
    modified_user VARCHAR(31)               NULL,
    modified_app  VARCHAR(31)               NULL,
    deleted_date  DATETIME                  NULL,
    deleted_user  VARCHAR(31)               NULL,
    deleted_app   VARCHAR(31)               NULL
);

CREATE TABLE IF NOT EXISTS types(
    type VARCHAR(15) NOT NULL PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS users(
    username        VARCHAR(20)          NOT NULL PRIMARY KEY,
    first           VARCHAR(30)          NOT NULL,
    last            VARCHAR(30)          NOT NULL,
    salt            VARCHAR(255)         NULL,
    password        VARCHAR(255)         NOT NULL,
    profilepic      LONGBLOB             NULL,
    profilepic_name VARCHAR(50)          NULL,
    description     VARCHAR(255)         NULL,
    member_since    DATE                 NOT NULL,
    class_year      INT(4)               NULL,
    location        VARCHAR(50)          NULL,
    favorite_event  VARCHAR(20)          NULL,
    activation_code VARCHAR(8)           NOT NULL,
    email           VARCHAR(50)          NULL,
    last_signin     DATETIME             NOT NULL,
    week_start      VARCHAR(15)          NULL,
    subscribed      CHAR                 NULL,
    deleted         TINYINT(1) DEFAULT 0 NULL,
    created_date    DATETIME             NULL,
    created_user    VARCHAR(31)          NULL,
    created_app     VARCHAR(31)          NULL,
    modified_date   DATETIME             NULL,
    modified_user   VARCHAR(31)          NULL,
    modified_app    VARCHAR(31)          NULL,
    deleted_date    DATETIME             NULL,
    deleted_user    VARCHAR(31)          NULL,
    deleted_app     VARCHAR(31)          NULL
);

CREATE TABLE IF NOT EXISTS weekstart(
    week_start VARCHAR(15) NOT NULL PRIMARY KEY
);

ALTER TABLE `groups` ADD INDEX (group_name);

ALTER TABLE comments
ADD CONSTRAINT comments_log_id_fk
FOREIGN KEY (log_id) REFERENCES logs(log_id);

ALTER TABLE comments
ADD CONSTRAINT comments_username_fk
FOREIGN KEY (username) REFERENCES users(username);

ALTER TABLE events
ADD CONSTRAINT events_group_name_fk
FOREIGN KEY (group_name) REFERENCES `groups`(group_name);

ALTER TABLE flair
ADD CONSTRAINT flair_username_fk
FOREIGN KEY (username) REFERENCES users(username);

ALTER TABLE forgotpassword
ADD CONSTRAINT forgotpassword_username_fk
FOREIGN KEY (username) REFERENCES users(username);

ALTER TABLE groupmembers
ADD CONSTRAINT groupmembers_group_name_fk
FOREIGN KEY (group_name) REFERENCES `groups`(group_name);

ALTER TABLE groupmembers
ADD CONSTRAINT groupmembers_status_fk
FOREIGN KEY (status) REFERENCES status(status);

ALTER TABLE groupmembers
ADD CONSTRAINT groupmembers_user_fk
FOREIGN KEY (user) REFERENCES admins(user);

ALTER TABLE groupmembers
ADD CONSTRAINT groupmembers_group_id_fk
FOREIGN KEY (group_id) REFERENCES `groups`(id);

ALTER TABLE `groups`
ADD CONSTRAINT groups_week_start_fk
FOREIGN KEY (week_start) REFERENCES weekstart(week_start);

ALTER TABLE logs
ADD CONSTRAINT logs_metric_fk
FOREIGN KEY (metric) REFERENCES metrics(metric);

ALTER TABLE logs
ADD CONSTRAINT logs_type_fk
FOREIGN KEY (type) REFERENCES types(type);

ALTER TABLE logs
ADD CONSTRAINT logs_username_fk
FOREIGN KEY (username) REFERENCES users(username);

ALTER TABLE notifications
ADD CONSTRAINT notifications_username_fk
FOREIGN KEY (username) REFERENCES users(username);

ALTER TABLE teamgroups
ADD CONSTRAINT teamgroups_team_name_fk
FOREIGN KEY (team_name) REFERENCES teams(name);

ALTER TABLE teamgroups
ADD CONSTRAINT teamgroups_group_id_fk
FOREIGN KEY (group_id) REFERENCES `groups`(id);

ALTER TABLE teamgroups
ADD CONSTRAINT teamgroups_username_fk
FOREIGN KEY (group_name) REFERENCES `groups`(group_name);

ALTER TABLE teammembers
ADD CONSTRAINT teammembers_team_name_fk
FOREIGN KEY (team_name) references teams(name);

ALTER TABLE teammembers
ADD CONSTRAINT teammembers_username_fk
FOREIGN KEY (username) references users(username);

ALTER TABLE users
ADD CONSTRAINT users_week_start_fk
FOREIGN KEY (week_start) references weekstart(week_start);
