CREATE DATABASE gprk_db;
\c gprk_db

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE roles (
    role_id int PRIMARY KEY,
    description varchar(32) UNIQUE NOT NULL
);

INSERT INTO roles VALUES (0, 'admin'), (1, 'teacher'), (2, 'student');

CREATE TABLE users (
    id uuid DEFAULT uuid_generate_v4(),
    username varchar(128) UNIQUE NOT NULL,
    password bytea NOT NULL,
    surname varchar(128) NOT NULL,
    name varchar(128) NOT NULL,
    patronymic varchar(128) NOT NULL,
    role_id int NOT NULL REFERENCES roles(role_id),
    PRIMARY KEY (id)
);

CREATE TABLE course (
    id uuid NOT NULL PRIMARY KEY,
    name varchar(128) UNIQUE NOT NULL,
    description varchar(512)
);

CREATE TABLE task (
    id uuid DEFAULT uuid_generate_v4(),
    creater_id uuid NOT NULL REFERENCES users(id),
    topic varchar(128) NOT NULL,
    description varchar(512) NOT NULL,
    deadline timestamp NOT NULL,
    created timestamp NOT NULL,
    course_id uuid NOT NULL REFERENCES course(id)
);

CREATE TABLE groups (
    id uuid NOT NULL PRIMARY KEY,
    name varchar(128) UNIQUE NOT NULL,
    course_id uuid NOT NULL REFERENCES course(id)
);

CREATE TABLE users_courses (
    id uuid DEFAULT uuid_generate_v4(),
    user_id uuid NOT NULL REFERENCES users(id),
    course_id uuid NOT NULL REFERENCES course(id),
    url_repo varchar(128) UNIQUE NOT NULL
);

CREATE TABLE changed_files (
    id uuid NOT NULL PRIMARY KEY,
    submission_id uuid NOT NULL REFERENCES submission(id),
    file_path varchar(512) NOT NULL,
    change_type varchar(20) NOT NULL, 
    content text, 
    uploaded timestamp NOT NULL,
    FOREIGN KEY (submission_id) REFERENCES submission(id)
);

CREATE TABLE submission (
    id uuid NOT NULL PRIMARY KEY,
    user_id uuid NOT NULL REFERENCES users(id),
    task_id uuid NOT NULL REFERENCES task(id),
    uploaded timestamp NOT NULL,
    status_id int,
    count int, 
    score int
);