DROP SCHEMA public CASCADE;
CREATE SCHEMA public;

DROP TABLE IF EXISTS users;
CREATE TABLE users(
    id integer primary key unique,
    token text not null
);

DROP TABLE IF EXISTS polls;
CREATE TABLE polls(
    id serial primary key,
    url text not null,
    user_id integer not null,
    question text not null,
    time_of_creation TIMESTAMPTZ DEFAULT Now(),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

DROP TABLE IF EXISTS possible_choice;
CREATE TABLE possible_choice (
    id serial primary key,
    poll_id integer not null,
    text text not null,
    FOREIGN KEY (poll_id) REFERENCES polls(id)
);

DROP TABLE IF EXISTS user_choice;
CREATE TABLE user_choice (
    user_id integer not null,
    poll_id integer not null,
    choice_id integer not null,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (poll_id) REFERENCES polls(id),
    FOREIGN KEY (choice_id) REFERENCES possible_choice(id)
);