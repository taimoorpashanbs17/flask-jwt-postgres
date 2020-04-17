-- auto-generated definition
drop table if exists playlist;
create table playlist
(
  id serial not null
    constraint playlists_pkey
    primary key,
  name       varchar(120),
    created_at timestamp default now() not null
);

alter table playlist
  owner to postgres;

