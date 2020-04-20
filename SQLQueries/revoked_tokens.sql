DROP TABLE if exists revoked_tokens;

CREATE TABLE revoked_tokens (
	id serial NOT NULL,
	jti varchar(120) NULL,
	CONSTRAINT revoked_tokens_pkey PRIMARY KEY (id)
);
