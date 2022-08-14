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

CREATE TABLE IF NOT EXISTS forgotpassword(
    forgot_code TEXT NOT NULL PRIMARY KEY,
    username TEXT NOT NULL,
    expires NUMERIC NOT NULL,
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

CREATE TABLE IF NOT EXISTS groups(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    group_name TEXT,
    group_title TEXT,
    grouppic BLOB,
    grouppic_name TEXT,
    description TEXT,
    week_start TEXT,
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
    FOREIGN KEY (week_start) REFERENCES weekstart(week_start)
);

CREATE TABLE IF NOT EXISTS groupmembers(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    group_id INTEGER,
    group_name TEXT,
    username TEXT,
    status TEXT,
    user TEXT,
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
    FOREIGN KEY (group_name) REFERENCES groups(group_name),
    FOREIGN KEY (status) REFERENCES status(status),
    FOREIGN KEY (user) REFERENCES admins(user),
    FOREIGN KEY (group_id) REFERENCES groups(id)
);

CREATE TABLE IF NOT EXISTS logs(
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    first TEXT NOT NULL,
    last TEXT NOT NULL,
    name TEXT NOT NULL,
    location TEXT NOT NULL,
    date NUMERIC NOT NULL,
    type TEXT NOT NULL,
    distance NUMERIC,
    metric TEXT,
    miles NUMERIC,
    time NUMERIC,
    pace NUMERIC,
    feel INTEGER NOT NULL,
    description TEXT,
    time_created NUMERIC NOT NULL,
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
    FOREIGN KEY (metric) REFERENCES metrics(metric),
    FOREIGN KEY (type) REFERENCES types(type),
    FOREIGN KEY (username) REFERENCES users(username)
);

CREATE TABLE IF NOT EXISTS metrics(
    metric TEXT PRIMARY KEY NOT NULL
);

CREATE TABLE IF NOT EXISTS notifications(
    notification_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    time NUMERIC NOT NULL,
    link TEXT,
    viewed TEXT NOT NULL,
    description TEXT,
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