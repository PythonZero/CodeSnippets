# Exporting (Unloading) files locally:

## Pre-requsite (SnowSQL):
Install `snowsql` to be able to do step 6 below. Steps 1-5 can be done on the UI
  * Change the settings (Default user/pwd/username/schema/..) by doing `vim ~/.snowsql/config`
  
### Parquet
1) Set the DB/Schema (ideally use a DEV db/schema)

```USE DATABASE "<DB_NAME>"; USE SCHEMA "<SCHEMA_NAME>";```

2) Create the file format you will be exporting
```
create or replace file format parquet_unload_format
  type = 'parquet'
  compression = snappy;  // optional
```

3) Create a stage where you will be saving the file format into

```  
create or replace stage parquet_stage
  file_format = parquet_unload_format;
```

4) Prepare the export of the data 

```
copy into @parquet_stage/unload/parquet_ from  "<DB_NAME>"."<SCHEMA_NAME>"."<TABLE)NAME>"
header = true // Only req'd for parquet
overwrite = true; // Only use it if you're overwriting a previous export with the same file name
```

5) Check to make sure parquets are going to be saved
```
list @parquet_stage;
```

6) Download the file locally (This step will fail if you're not using snowsql)

```
get @parquet_stage/unload/parquet_ file:///Users/<local>/Documents/snowsql/<destination>;
```

### CSV

```
USE DATABASE "<DB_NAME>"; USE SCHEMA "<SCHEMA_NAME>";
create or replace file format my_csv_unload_format
  type = 'CSV'
  field_delimiter = '|';
  
create or replace stage my_unload_stage
  file_format = my_csv_unload_format;

copy into @my_unload_stage/unload/ from  "<DB_NAME>"."<SCHEMA_NAME>"."<TABLE_NAME>";

list @my_unload_stage;

get @my_unload_stage/unload/data_0_0_0.csv.gz file:///Users/<user>/Documents/snowsql
```
