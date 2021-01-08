# Spark SQL

## Running commands in the SQL query:

```python
QUERY = f"""
WITH mpsub2 as (
SELECT 'Sultan' AS mp_user, 3 AS day
UNION ALL SELECT 'Sultan', 4
UNION ALL SELECT 'Sultan', 5
UNION ALL SELECT 'Bob', 6)
SELECT * FROM (
FROM  mpsub2
map mp_user, day
--using 'python {PATH_TO_DAYS_IN_MP_PY_FILE}'  -- <- e.g. mapping using a file
-- as mp_user bigint, x int, days_in_mp int. -- <- the output
using 'ls' -- <- Runs ls
as mp_user string <- Returns one row per ls item found
)

"""
df = spark.sql(QUERY).show()
```
Example of the `PATH_TO_DAYS_IN_MP_PY_FILE.py`

```python
import sys
from itertools import groupby

for u, lines in groupby(sys.stdin, lambda x : x.strip().split('\t')[0]):
  days = set()
  for line in lines:
    u, day = line.strip().split('\t')
    day = int(day)

    days.add(day)
    days &= set(range(day-90,day+1))

    print('\t'.join(map(str, [u, day, len(days)])))
```

Remember to:

```python
  spark_context.addPyFile(PATH_TO_DAYS_IN_MP_PY_FILE)
```
