# Postgres Docker Workflow

This project uses a Postgres container (`success-db-y`) to manage the **billionaires** dataset.  
The commands below show the full workflow:

1. **Create production schema and indexes** (build the clean table with constraints + indexes).
2. **ETL with staging** (load raw CSV → staging, clean → production, verify row counts, drop staging).

All commands use `$POSTGRES_USER` and `$POSTGRES_DB`, which should be set from your `.env` file.  
No usernames or passwords are exposed here.

# 1) Create prod schema and indexes

```bash
docker exec -it success-db-y psql -U $POSTGRES_USER -d $POSTGRES_DB -f /sql/create_billionaires_schema.sql
docker exec -it success-db-y psql -U $POSTGRES_USER -d $POSTGRES_DB -f /sql/create_indexes.sql
docker exec -it success-db-y psql -U $POSTGRES_USER -d $POSTGRES_DB -c "\di"
```

# 2) Staging: create, load, promote, check, drop

```bash
docker exec -it success-db-y psql -U $POSTGRES_USER -d $POSTGRES_DB -f /sql/create_staging.sql
docker exec -it success-db-y psql -U $POSTGRES_USER -d $POSTGRES_DB -f /sql/load_staging.sql
docker exec -it success-db-y psql -U $POSTGRES_USER -d $POSTGRES_DB -f /sql/promote_to_prod.sql
docker exec -it success-db-y psql -U $POSTGRES_USER -d $POSTGRES_DB -f /sql/counts.sql
docker exec -it success-db-y psql -U $POSTGRES_USER -d $POSTGRES_DB -f /sql/drop_staging.sql
```
