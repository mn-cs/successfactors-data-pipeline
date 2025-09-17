-- Adjust path if needed (this is inside the container)
\set ON_ERROR_STOP 1
\copy staging_billionaires FROM '/import/interim/merged_dataset_2025-09-04.csv' WITH (FORMAT csv, HEADER true)

