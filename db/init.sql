CREATE DATABASE gprk_db;
\c gprk_db

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE roles (
    role_id tinyint PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    description varchar(32) UNIQUE NOT NULL,
)

INSERT INTO roles VALUES ('admin'), ('teacher'), ('student');

CREATE TABLE users (
    id uuid DEFAULT uuid_generate_v4 (),
    username varchar(128) UNIQUE NOT NULL,
    password bytea NOT NULL,
    surname varchar(128) NOT NULL,
    name varchar(128) NOT NULL,
    patronymic varchar(128) NOT NULL,
    role role_id NOT NULL REFERENCES roles(role_id),
    PRIMARY KEY (id)
);