# Snowflake Stages

```sql

SHOW STAGES;
DESCRIBE STAGE ZENDESK_USERS_STAGE;

ALTER STAGE ZENDESK_USERS_STAGE SET URL = "s3://bucket/zendesk/users/";
  # ^ However, SET URL can cause external tables to break, and will need to be re-created (DROP TABLE, CREATE TABLE)
ALTER STAGE ZENDESK_USERS_STAGE SET STORAGE_INTEGRATION = AWS_ABC_INTEGRATION;
ALTER EXTERNAL TABLE  "db"."schema"."ZENDESK_USERS" REFRESH;

```

## Get the stages

```sql
SHOW STAGES IN DATABASE "database_name"
# or
SHOW STAGES IN SCHEMA "schema_name"

```

## Identify if table is native snowflake or not

If the table has a `VALUES` column, then it's an external table. Otherwise its an internal table.
Internal tables are stored and managed by snowflake in S3 buckets.
If it's an external table, then it has a stage associated it, and can be discovered by the "Get the stages" section.
