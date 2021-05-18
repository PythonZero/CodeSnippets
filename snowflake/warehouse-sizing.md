# Upgrade your warehouse, Create it, and suspend it
This will ensure 0 downtime and no extra costs, just faster execution
as each minute on a large machine is very expensive.
```sql
USE DATABASE ANALYTICS_PROD;
USE ROLE SYSADMIN;
USE WAREHOUSE BALERION_THE_BLACK_DRAGON;
ALTER WAREHOUSE BALERION_THE_BLACK_DRAGON SET WAREHOUSE_SIZE='XXXLARGE';
---------------------------------------
-- Do your actions
INSERT INTO TableName(col1, col2, col3)
SELECT
    col1, col2, col3
FROM old_table;
----------------------------------------
ALTER WAREHOUSE BALERION_THE_BLACK_DRAGON SUSPEND;
ALTER WAREHOUSE BALERION_THE_BLACK_DRAGON SET warehouse_size='LARGE';
USE WAREHOUSE analytics_xsmall;
```
