-- Promote clean rows from staging → prod
INSERT INTO billionaires (
  rank_position, name, source, country, gender, age, current_worth,
  birth_year, birth_month, birth_day,
  university_1, degree_1, university_2, degree_2, university_3, degree_3
)
SELECT
  rank_position::int,
  NULLIF(btrim(name),'')::varchar(100),
  NULLIF(btrim(source),'')::varchar(200),                           -- remains NULL if blank
  NULLIF(btrim(country),'')::varchar(50),                           -- prod requires NOT NULL
  CASE WHEN upper(btrim(gender)) IN ('M','F') THEN upper(btrim(gender)) END,
  CASE WHEN age ~ '^[0-9]+$' AND age::int > 0 AND age::int < 150 THEN age::int END,
  CASE WHEN current_worth ~ '^[0-9]+(\.[0-9]+)?$' THEN current_worth::numeric(10,1) END,
  CASE WHEN birth_year  ~ '^[0-9]+$' AND birth_year::int >= 1472 AND birth_year::int < 2100 THEN birth_year::int END,
  CASE WHEN birth_month ~ '^[0-9]+$' AND birth_month::int BETWEEN 1 AND 12 THEN birth_month::int END,
  CASE WHEN birth_day   ~ '^[0-9]+$' AND birth_day::int BETWEEN 1 AND 31 THEN birth_day::int END,
  NULLIF(btrim(university_1),''),
  NULLIF(btrim(degree_1),''),
  NULLIF(btrim(university_2),''),
  NULLIF(btrim(degree_2),''),
  NULLIF(btrim(university_3),''),
  NULLIF(btrim(degree_3),'')
FROM staging_billionaires
WHERE NULLIF(btrim(country),'') IS NOT NULL                      -- enforce prod NOT NULL
ON CONFLICT (rank_position) DO NOTHING;
