create table genre
(
  id         serial                  not null
    constraint genre_pkey
    primary key,
  name       varchar(40),
  created_at timestamp default now() not null
);


