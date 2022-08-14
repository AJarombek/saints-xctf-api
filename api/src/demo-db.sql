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

CREATE TABLE IF NOT EXISTS status(
    status TEXT PRIMARY KEY NOT NULL
);

CREATE TABLE IF NOT EXISTS teams(
    name TEXT PRIMARY KEY NOT NULL,
    title TEXT NOT NULL,
    picture_name TEXT,
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
    deleted_app TEXT
);

CREATE TABLE IF NOT EXISTS teamgroups(
    team_name TEXT NOT NULL,
    group_id INTEGER NOT NULL,
    group_name TEXT NOT NULL,
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
    FOREIGN KEY (team_name) REFERENCES teams (name),
    FOREIGN KEY (group_id) REFERENCES `groups` (id),
    FOREIGN KEY (group_name) REFERENCES `groups` (group_name)
);

CREATE TABLE IF NOT EXISTS teammembers(
    team_name TEXT NOT NULL,
    username TEXT NOT NULL,
    status TEXT NOT NULL,
    user TEXT NOT NULL,
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
    FOREIGN KEY (team_name) REFERENCES teams(name),
    FOREIGN KEY (username) REFERENCES users(username)
);

CREATE TABLE IF NOT EXISTS types(
    type TEXT PRIMARY KEY NOT NULL
);

CREATE TABLE IF NOT EXISTS users
(
    username TEXT PRIMARY KEY NOT NULL,
    first TEXT NOT NULL,
    last TEXT NOT NULL,
    salt TEXT,
    password TEXT NOT NULL,
    profilepic BLOB,
    profilepic_name TEXT,
    description TEXT,
    member_since NUMERIC,
    class_year INTEGER,
    location TEXT,
    favorite_event TEXT,
    activation_code TEXT NOT NULL,
    email TEXT,
    last_signin NUMERIC,
    week_start TEXT,
    subscribed TEXT,
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

create table weekstart(
    week_start TEXT PRIMARY KEY NOT NULL
);