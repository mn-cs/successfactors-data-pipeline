-- =========================
-- Run this file inside the container to apply indexing:
--   docker exec -it success-db-y \
--     psql -U successuser_username_db_y -d success_db_y \
--     -f /sql/create_indexes.sql

-- After running, you can verify indexes with:
--   docker exec -it success-db-y \
--     psql -U successuser_username_db_y -d success_db_y -c "\di"
-- =========================

-- create_indexes.sql
-- Postgres-safe: uses IF NOT EXISTS.
-- Run AFTER the table is created.

-- =========================
-- Table: public.billionaires
-- Columns:
--   rank_position (PK), name, source, country, gender, age, current_worth,
--   birth_year, birth_month, birth_day,
--   university_1, degree_1, university_2, degree_2, university_3, degree_3,
--   created_at, updated_at
-- =========================

-- === HIGH-VALUE, GENERALLY SAFE TO ENABLE ===

-- Point/equality lookups by name
CREATE INDEX IF NOT EXISTS idx_billionaires_name
ON public.billionaires (name);

-- Common regional filters / GROUP BYs
CREATE INDEX IF NOT EXISTS idx_billionaires_country
ON public.billionaires (country);

-- Useful for ranges and demographics, often paired with country
CREATE INDEX IF NOT EXISTS idx_billionaires_age
ON public.billionaires (age);

-- If you sort/filter by net worth (thresholds, top-N, etc.)
CREATE INDEX IF NOT EXISTS idx_billionaires_current_worth
ON public.billionaires (current_worth);

-- Composite for queries like:
--   WHERE country='USA' AND age BETWEEN ... ORDER BY age;
CREATE INDEX IF NOT EXISTS idx_billionaires_country_age
ON public.billionaires (country, age);

-- Composite for regional “rich list” queries:
--   WHERE country='USA' ORDER BY current_worth DESC;
CREATE INDEX IF NOT EXISTS idx_billionaires_country_current_worth
ON public.billionaires (country, current_worth);

-- Optional composite for equality on full DOB:
--   WHERE birth_year=... AND birth_month=... AND birth_day=...;
-- (See birth_date option below for a cleaner approach.)
CREATE INDEX IF NOT EXISTS idx_billionaires_birth_ymd
ON public.billionaires (birth_year, birth_month, birth_day);



-- === OPTIONAL / COMMENTED: ENABLE ONLY IF NEEDED ===

-- Primary key already creates a unique index. Don’t duplicate.
-- CREATE INDEX IF NOT EXISTS idx_billionaires_rank_position
-- ON public.billionaires (rank_position);

-- If you frequently filter/order by source of wealth
-- CREATE INDEX IF NOT EXISTS idx_billionaires_source
-- ON public.billionaires (source);

-- Very low cardinality; usually NOT helpful alone
-- CREATE INDEX IF NOT EXISTS idx_billionaires_gender
-- ON public.billionaires (gender);

-- If you query by year alone (coarser filters)
-- CREATE INDEX IF NOT EXISTS idx_billionaires_birth_year
-- ON public.billionaires (birth_year);

-- If you query by (year, month) frequently
-- CREATE INDEX IF NOT EXISTS idx_billionaires_birth_year_month
-- ON public.billionaires (birth_year, birth_month);

-- Timestamps: only if you filter by created/updated windows often
-- CREATE INDEX IF NOT EXISTS idx_billionaires_created_at
-- ON public.billionaires (created_at);
-- CREATE INDEX IF NOT EXISTS idx_billionaires_updated_at
-- ON public.billionaires (updated_at);



-- === EDUCATION FIELDS ===
-- If you do exact equality searches per column (rare), enable per-column btree:
-- CREATE INDEX IF NOT EXISTS idx_billionaires_university_1 ON public.billionaires (university_1);
-- CREATE INDEX IF NOT EXISTS idx_billionaires_degree_1     ON public.billionaires (degree_1);
-- CREATE INDEX IF NOT EXISTS idx_billionaires_university_2 ON public.billionaires (university_2);
-- CREATE INDEX IF NOT EXISTS idx_billionaires_degree_2     ON public.billionaires (degree_2);
-- CREATE INDEX IF NOT EXISTS idx_billionaires_university_3 ON public.billionaires (university_3);
-- CREATE INDEX IF NOT EXISTS idx_billionaires_degree_3     ON public.billionaires (degree_3);

-- If you do ILIKE / substring searches across education fields,
-- prefer ONE trigram GIN index instead of many btrees:
-- CREATE EXTENSION IF NOT EXISTS pg_trgm;
-- CREATE INDEX IF NOT EXISTS idx_billionaires_education_trgm
-- ON public.billionaires USING GIN (
--   (concat_ws(' ',
--      coalesce(university_1,''), coalesce(degree_1,''),
--      coalesce(university_2,''), coalesce(degree_2,''),
--      coalesce(university_3,''), coalesce(degree_3,'')
--   )) gin_trgm_ops
-- );



-- === (OPTIONAL) BETTER DATE STRATEGY ===
-- Prefer a single stored generated column and index it for clean equality/range queries:
-- ALTER TABLE public.billionaires
--   ADD COLUMN birth_date date GENERATED ALWAYS AS
--     (make_date(birth_year, birth_month, birth_day)) STORED;
-- CREATE INDEX IF NOT EXISTS idx_billionaires_birth_date
-- ON public.billionaires (birth_date);



-- === HOUSEKEEPING / CHECK USAGE (run manually as needed) ===
-- EXPLAIN ANALYZE SELECT * FROM public.billionaires
--  WHERE country='USA' AND age BETWEEN 40 AND 60
--  ORDER BY current_worth DESC
--  LIMIT 50;
--
-- To drop an index you don’t need:
-- DROP INDEX IF EXISTS idx_billionaires_source;
