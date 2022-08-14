-- Script with DDL commands for a SQLite demo SaintsXCTF database.
-- Author: Andrew Jarombek
-- Date: 8/13/2022

CREATE TABLE IF NOT EXISTS admins(
    user TEXT NOT NULL PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS codes(
    activation_code TEXT NOT NULL PRIMARY KEY,
    email TEXT,
    group_id INTEGER,
    expiration_date NUMERIC,
    deleted INTEGER,
    created_date NUMERIC,
    created_user TEXT,
    created_app TEXT,
    modified_date NUMERIC,
    modified_user TEXT,
    modified_app TEXT,
    deleted_date NUMERIC,
    deleted_user TEXT,
    deleted_app TEXT,
    FOREIGN KEY (group_id) REFERENCES groups(id)
);

CREATE TABLE IF NOT EXISTS comments(
    comment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    first TEXT NOT NULL,
    last TEXT NOT NULL,
    log_id INTEGER NOT NULL,
    time NUMERIC NOT NULL,
    content TEXT,
    deleted INTEGER,
    created_date NUMERIC,
    created_user TEXT,
    created_app TEXT,
    modified_date NUMERIC,
    modified_user TEXT,
    modified_app TEXT,
    deleted_date NUMERIC,
    deleted_user TEXT,
    deleted_app TEXT,
    FOREIGN KEY (log_id) REFERENCES logs(log_id),
    FOREIGN KEY (username) REFERENCES users(username)
);

CREATE TABLE IF NOT EXISTS flair
(
    flair_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    flair TEXT,
    deleted INTEGER,
    created_date NUMERIC,
    created_user TEXT,
    created_app TEXT,
    modified_date NUMERIC,
    modified_user TEXT,
    modified_app TEXT,
    deleted_date NUMERIC,
    deleted_user TEXT,
    deleted_app TEXT,
    FOREIGN KEY (username) REFERENCES users(username)
);
