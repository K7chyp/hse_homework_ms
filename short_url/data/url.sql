DROP TABLE IF EXISTS public.short_urls;
CREATE TABLE IF NOT EXISTS public.short_urls (
	id serial4 NOT NULL,
	short_id varchar NULL,
	full_url varchar NULL,
	created_at timestamptz DEFAULT now() NULL,
	CONSTRAINT short_urls_pkey PRIMARY KEY (id)
);
CREATE IF NOT EXISTS UNIQUE INDEX pkey_short_id ON public.short_urls USING btree (short_id);
a