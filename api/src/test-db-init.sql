-- Script with DDL commands for a PostgreSQL test SaintsXCTF database.
-- Author: Andrew Jarombek
-- Date: 11/8/2022

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

ALTER TABLE comments
ADD CONSTRAINT comments_log_id_fk
FOREIGN KEY (log_id) REFERENCES logs(log_id);

ALTER TABLE comments
ADD CONSTRAINT comments_username_fk
FOREIGN KEY (username) REFERENCES logs(username);

ALTER TABLE events
ADD CONSTRAINT events_group_name_fk
FOREIGN KEY (group_name) REFERENCES `groups` (group_name);

ALTER TABLE flair
ADD CONSTRAINT flair_username_fk
FOREIGN KEY (username) REFERENCES users (username);

ALTER TABLE forgotpassword
ADD CONSTRAINT forgotpassword_username_fk
FOREIGN KEY (username) REFERENCES users (username);
