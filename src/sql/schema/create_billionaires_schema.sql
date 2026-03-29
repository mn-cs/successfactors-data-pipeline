-- =============================================
-- BILLIONAIRES DATABASE SCHEMA
-- =============================================
-- Purpose:
--   Defines the `billionaires` table for storing information 
--   about the world’s richest individuals.
--
-- Data covered:
--   • Personal details (name, country, gender, age, birthdate)
--   • Source of wealth (companies, industries)
--   • Financial details (net worth in billions USD)
--   • Education (up to 3 universities and degrees)
--   • Metadata (record creation and last update timestamps)
--
-- Notes:
--   • `rank_position` is the primary key (matches the rank in your dataset).
--   • `gender` is restricted to 'M' or 'F'.
--   • Age and birthdate fields have validation checks.
--   • `current_worth` is stored as DECIMAL(10,1) for billions with one decimal place.
--   • `updated_at` defaults to current timestamp; 
--     if auto-update on change is needed, implement with a trigger (PostgreSQL).
--
-- This schema matches your CSV structure of 12 data columns 
-- plus metadata fields for auditing.
-- =============================================

DROP TABLE IF EXISTS billionaires;

CREATE TABLE billionaires (
 rank_position INTEGER PRIMARY KEY,
 name VARCHAR(100) NOT NULL,
 source VARCHAR(200),
 country VARCHAR(50) NOT NULL,
 gender CHAR(1) CHECK (gender IN ('M', 'F') OR gender IS NULL),
 age INTEGER CHECK ((age > 0 AND age < 150) OR age IS NULL),
 current_worth DECIMAL(10, 1) NOT NULL,
 birth_year INTEGER CHECK ((birth_year >= 1472 AND birth_year < 2100) OR birth_year IS NULL),
 birth_month INTEGER CHECK ((birth_month >= 1 AND birth_month <= 12) OR birth_month IS NULL),
 birth_day INTEGER CHECK ((birth_day >= 1 AND birth_day <= 31) OR birth_day IS NULL),
 university_1 VARCHAR(250),
 degree_1 VARCHAR(100),
 university_2 VARCHAR(200),
 degree_2 VARCHAR(100),
 university_3 VARCHAR(200),
 degree_3 VARCHAR(100)
);
