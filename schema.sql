CREATE TABLE users(
    id integer primary key unique,
    token text not null
);

CREATE TABLE entries(
  id serial primary key,
  title text not null,
  text text not null,
  user_id integer not null,
  FOREIGN KEY (user_id) REFERENCES USERS(id)
);

CREATE TABLE vk_api(
    id text not null,
    secret text not null,
    url text not null
);