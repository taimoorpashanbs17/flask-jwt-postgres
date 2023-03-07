create table artists
(
  id         serial                  not null
    constraint artist_pkey
    primary key,
  name       varchar(120),
  created_at timestamp default now() not null
);

