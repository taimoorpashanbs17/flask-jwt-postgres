-- Drop table

-- DROP TABLE public.album;

CREATE TABLE public.album (
	id serial NOT NULL,
	title varchar(120) NULL,
	artist_id int4 NULL,
	created_at timestamp NOT NULL DEFAULT now(),
	CONSTRAINT album_pkey PRIMARY KEY (id),
	CONSTRAINT album_artist_id_fkey FOREIGN KEY (artist_id) REFERENCES artists(id)
);

-- Permissions

ALTER TABLE public.album OWNER TO postgres;
GRANT ALL ON TABLE public.album TO postgres;
