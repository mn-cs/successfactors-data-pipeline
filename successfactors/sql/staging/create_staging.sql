-- Raw landing table: all TEXT, no constraints
DROP TABLE IF EXISTS staging_billionaires;
CREATE UNLOGGED TABLE staging_billionaires (
  rank_position  text,
  name           text,
  source         text,
  country        text,
  gender         text,
  age            text,
  current_worth  text,
  birth_year     text,
  birth_month    text,
  birth_day      text,
  university_1   text,
  degree_1       text,
  university_2   text,
  degree_2       text,
  university_3   text,
  degree_3       text
);
