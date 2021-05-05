# Casting types

```sql
# Rather than
SELECT CAST(timestamp AS date),
       CAST(colA as NUMBER), 
       CAST(colB AS FLOAT)
FROM table1

# Do
SELECT timestamp::date, 
       colA::NUMBER,
       colB::FLOAT
FROM table1

```
