# Login to psql instance

```bash
psql -h 192.168.0.1 -p 5423 -d database_name -U username -W   # -W creates password prompt

# if you don't want to type your password each time
export PGPASSWORD=yourpassword
psql -h 192.168.0.1 -p 5423 -d database_name -U username  # no -W
```

## Commands

- `\l` - list available databases
- `\dt` - list all relational tables 
    * `no relations found` -> no relational tables
- `\dt+ *` - list ALL tables
- `\c <db_name>` - changes to that database
