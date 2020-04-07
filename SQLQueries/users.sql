create table users
(
  id         SERIAL      not null
    primary key,
  username   VARCHAR(120) not null
    unique,
  password   VARCHAR(120) not null,
  created_at timestamp without time zone NOT NULL DEFAULT now()
);
