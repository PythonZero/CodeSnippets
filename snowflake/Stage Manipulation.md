# Snowflake Stages

```sql

SHOW STAGES;
DESCRIBE STAGE ZENDESK_USERS_STAGE;

ALTER STAGE ZENDESK_USERS_STAGE SET URL = "s3://bucket/zendesk/users/";
  // ^ However, SET URL can cause external tables to break, and will need to be re-created (DROP TABLE, CREATE TABLE)
ALTER STAGE ZENDESK_USERS_STAGE SET STORAGE_INTEGRATION = AWS_ABC_INTEGRATION;
ALTER EXTERNAL TABLE  "db"."schema"."ZENDESK_USERS" REFRESH;

```
