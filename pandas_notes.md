# Pandas important points

## Pandas Bug with reading in csv

Headers cause pandas to read in the whole thing as a string. Skipping headers fixes this.

```python3
def test_pandas_bad():
    unprocessed_file_contents = """name,clicks,surname,timestamp,impressions,spend_usd
Bob,31,Michael,2018-07-25 22:18:28,32,76
Charlie,20,X,2019-07-01 13:00:00,16,48
Mike,12,X,2020-01-01 14:00:00,,
Joao,1,Y,2021-01-01 14:00,167289225369306298,"""
    pandas_dtypes = {
        "name": "string",
        "clicks": "Int64",
        "surname": "string",
        "timestamp": "string",
        "impressions": "Int64",
        "spend_usd": "float",
    }
    df = pd.read_csv(io.StringIO(unprocessed_file_contents), dtype=pandas_dtypes)  # 1 - broken
    # df = pd.read_csv(io.StringIO(unprocessed_file_contents), header=None, skiprows=1, dtype=pandas_dtypes)  # 2 - still broken
    assert df.iloc[3,4] == 167289225369306298  # 1 - fails, 2 - passes
    assert int(df.iloc[3,4]) == 167289225369306298  # 1 - fails, 2 - fails
    
    # how to make it work
    df = pd.read_csv(io.StringIO(unprocessed_file_contents), dtype=object)  
    df.spend_usd = df.spend_usd.astype("Int64")
    assert int(df.iloc[3,4]) == 167289225369306298  # Passes

    
```
