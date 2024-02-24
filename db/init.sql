CREATE DATABASE gprk_db;
\c gprk_db

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE users (
    id uuid DEFAULT uuid_generate_v4 (),
    username varchar(128) UNIQUE NOT NULL,
    password bytea NOT NULL,

    PRIMARY KEY (id)
);