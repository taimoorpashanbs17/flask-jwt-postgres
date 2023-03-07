drop table if exists users;
-- auto-generated definition
create table users
(
  id         serial                  not null
    constraint users_pkey
    primary key,
  email      text                    not null
    constraint users_email_key
    unique,
  password   varchar(120)            not null,
  first_name varchar(120)            not null,
  last_name  varchar(120)            not null,
  is_admin   boolean default false   not null,
  is_active boolean default true not null,
  created_at timestamp default null
);

alter table users
  owner to postgres;
