# Data Engineering via BQ and Parquet Files

* Option 1 - BigQuery reads/writes directly to Native BQ Table
* **Option 2** - Bigquery reads from Externally Partitioned Parquet Table
  * PRO - Will always contain the latest data
  * PRO - Can be cheaper than continuously rewriting the bigquery table.
  * CON - Slightly Slower to read file vs native bigquery table during query


# Option 2
## Save to Parquet

```python3

GCP_FILE_NAME = f"gs://{GCP_BUCKET_NAME}/folder1/folder2/folder3/filename.parquet"

def _gcp_file_exists(
    storage_client: storage.Client,
    gcp_full_file_path=GCP_FILE_NAME,
) -> bool:
    """Checks if a file exists

    :param storage_client: The storage client
    :param gcp_full_file_path:  e.g. "gs://bucket/path/to/file.extension
    :return: True if file exists else False
    """
    bucket = Path(gcp_full_file_path).parts[1]
    file_prefix = "/".join(Path(gcp_full_file_path).parts[2:])  # Removes gs://bucket/
    return bool(
        list(storage_client.list_blobs(bucket, prefix=file_prefix, max_results=1))
    )
    
df.to_parquet(
    GCP_FILE_NAME,
    partition_cols=["date"],
    engine="fastparquet",  # Must set this for the append option to be available
    append=_gcp_file_exists(storage_client, GCP_FILE_NAME),  # If True and doesn't exist -> errors
)


```
Files get saved as the following format (depending on partition): 
```
gs://BUCKET/folder1/file.parquet/date=2022-05-26/part0.parquet
gs://BUCKET/folder1/file.parquet/date=2022-05-26/part1.parquet
gs://BUCKET/folder1/file.parquet/date=2022-05-26/partX.parquet
gs://BUCKET/folder1/file.parquet/date=2022-05-26/name=bob/part0.parquet
gs://BUCKET/folder1/file.parquet/date=2022-05-26/key=value/part0.parquet
```


## Create External Table in BigQuery

1. Create Table From -> Google Cloud Storage
2. File path, e.g. `BUCKET/folder1/file.parquet/*.parquet  # as there's metadata etc files`
3. **Enable** Source Data Partitioning
4. Select source URI prefix - `BUCKET/folder1/file.parquet/`  _# this will automatically get the key=values and partition based on them_`
    * **OR add** `/bigstore/` to the prefix -> `/bigstore/BUCKET/folder1/file.parquet/`
       * If you get the error: "Failed to create table: Directory URI `/bigstore/BUCKET/folder1/file.parquet/ds=2022-05-26/` does not contain path to table (`BUCKET/folder1/file.parquet`) as a prefix, which is a requirement." 
6. **Disable** Require partition filter
7. Partition inference mode - **Automtically infer types**
8. Destination
  a. Project, Dataset, Table
  b. **Table Type** - External Table
9. Schema -> Autodetect
