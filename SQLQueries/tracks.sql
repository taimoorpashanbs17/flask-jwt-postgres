-- auto-generated definition
DROP TABLE if EXISTS tracks;
create table tracks
(
  trackid       serial           not null
    constraint tracks_pkey
    primary key,
  name          varchar(60)      not null,
  albumid       integer          not null
    constraint tracks_album_id_fk
    references album,
  mediatypeid   integer          not null
    constraint tracks_media_types_mediatypeid_fk
    references media_types,
  genreid       integer          not null
    constraint tracks_genre_id_fk
    references genre,
  composer      varchar(70),
  milli_seconds bigint           not null,
  bytes         bigint           not null,
  unitprice     double precision not null,
  created_at    timestamp default now()
);

alter table tracks
  owner to postgres;

create unique index tracks_trackid_uindex
  on tracks (trackid);
