-- auto-generated definition
drop table if exists user_session;
create table user_session
(
  session_id       serial    not null
    constraint user_session_pkey
    primary key,
  user_id          integer   not null
    constraint user_session_users_id_fk
    references users,
  session_time_in  timestamp not null,
  session_time_out timestamp
);

alter table user_session
  owner to postgres;

create unique index user_session_session_id_uindex
  on user_session (session_id);

