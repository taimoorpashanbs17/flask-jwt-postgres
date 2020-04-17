-- auto-generated definition
drop table if exists media_types;
create table media_types
(
  mediatypeid serial                  not null
    constraint mediatype_pkey
    primary key,
  name        varchar(50)             not null,
  created_at  timestamp default now() not null
);

alter table media_types
  owner to postgres;

create unique index mediatype_mediatypeid_uindex
  on media_types (mediatypeid);

