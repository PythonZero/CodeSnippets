# Login to psql instance

```bash
psql -h 192.168.0.1 -p 5423 -d database_name -U username -W   # -W creates password prompt
# if you don't want to type your password eachtime
export PGPASSWORD=yourpassword
```

## Commands

- `\l` - list available databases
- `\dt` - list available tables 
    * `no relations found` -> no tables
- `\c <db_name>` - changes to that database
