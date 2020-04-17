create table artists
(
  id         serial                  not null
    constraint artist_pkey
    primary key,
  name       varchar(120),
  created_at timestamp default now() not null
);

--CREATE A Function

CREATE OR REPLACE FUNCTION artist_booelans()
  RETURNS trigger AS
$$
BEGIN
         UPDATE artists
         SET is_updated = TRUE
  WHERE is_updated is not null ;
    RETURN NEW;
END;
$$
LANGUAGE 'plpgsql';

-- CREATE A TRIGGER
CREATE TRIGGER updating_artist AFTER UPDATE ON artists
  FOR EACH ROW EXECUTE PROCEDURE artist_booelans();

alter table artist
  owner to postgres;
