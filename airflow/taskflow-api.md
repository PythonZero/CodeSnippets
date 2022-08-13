# Taskflow API
## TOC
1. Using dag decorator (auto includes JSON config params)
2. Not using the dag decorator (no JSON config params)
3. Not using the dag decorator - but adding params manually

# 1. Using DAG decorator

```python
from airflow.decorators import dag, task
from airflow.providers.amazon.aws.operators.s3 import S3CreateObjectOperator
from airflow.utils.dates import days_ago

default_args = {
    "owner": "airflow",
}


@dag(default_args=default_args, schedule_interval="@daily", start_date=days_ago(2))
def s3_file_generator_example(name):
    """
    # My custom Airflow DAG
    This is a simple ETL pipeline which demonstrates usage

    ## Custom parameters
    ```python
    {
      "name": "<put your name>",
    }
    ```
    """
    
    # NOTE: you can also put the entire `create_file` function outside as a global function (& not a nested function)
    @task(multiple_outputs=True)
    def create_file(name):
        """
        # Task 1
        Prints the name
        """
        import pandas as pd
        import tempfile
        import os

        df = pd.DataFrame({"a": [1,2,3, 4], "b": [4, 5, 6, 7]})
        file_name = os.path.join(tempfile.gettempdir(), f"{name}.csv")
        df.to_parquet(file_name)
        csv_data = df.to_csv()
        return {"file_name": file_name, "csv_data": csv_data}

    output_dict = create_file(name)
    S3CreateObjectOperator(
        s3_bucket="my-example-bucket",
        s3_key=output_dict["file_name"],
        data=output_dict["csv_data"],
        task_id="s3-create-object",
        replace=False,
        encrypt=False
    )

DAG = s3_file_generator_example("example_pandas_df")


# Notes
#  1. Using the @dag decorator automatically creates the params
```

# 2. Not Using DAG decorator

```python
from datetime import timedelta

from airflow import DAG
from airflow.decorators import task
from airflow.providers.amazon.aws.operators.s3 import S3CreateObjectOperator
from airflow.utils.dates import days_ago

default_args = {
    "owner": "airflow",
}

dag = DAG(
    dag_id="my-dag-with-some-s3-magic",
    default_args=default_args,
    description="A simple tutorial DAG",
    schedule_interval=timedelta(days=1),
    start_date=days_ago(2),
    tags=["example"],
)


@task(multiple_outputs=True)
def create_file(name):
    """
    # Task 1
    Prints the name
    """
    import pandas as pd
    import tempfile
    import os

    df = pd.DataFrame({"a": [1, 2, 3, 4], "b": [4, 5, 6, 7]})
    file_name = os.path.join(tempfile.gettempdir(), f"{name}.csv")
    df.to_parquet(file_name)
    csv_data = df.to_csv()
    return {"file_name": os.path.basename(file_name), "csv_data": csv_data}


output_dict = create_file("a-custom-file")
S3CreateObjectOperator(
    s3_bucket="my-example-bucket",
    s3_key=output_dict["file_name"],
    data=output_dict["csv_data"],
    task_id="s3-create-object",
    replace=False,
    encrypt=False,
    dag=dag,
)
```

# 3. Not using DAG decorator - BUT adding params manually
```python
from datetime import timedelta

from airflow import XComArg, DAG
from airflow.decorators import dag, task
from airflow.providers.amazon.aws.operators.s3 import S3CreateObjectOperator
from airflow.utils.dates import days_ago

default_args = {
    "owner": "airflow",
}

dag = DAG(
    dag_id="my-dag-with-some-s3-magic-v3",
    default_args=default_args,
    description="A simple tutorial DAG",
    schedule_interval=timedelta(days=1),
    start_date=days_ago(2),
    tags=["example"],
    params={"name": "a-custom-file-v3"},  # makes the params for the configuration JSON
)


@task(multiple_outputs=True)
def create_file(name):
    """"""
    import pandas as pd
    import tempfile
    import os

    df = pd.DataFrame({"a": [1, 2, 3, 4], "b": [4, 5, 6, 7]})
    file_name = os.path.join(tempfile.gettempdir(), f"{name}.csv")
    df.to_parquet(file_name)
    csv_data = df.to_csv()
    return {"file_name": os.path.basename(file_name), "csv_data": csv_data}


output_dict = create_file("{{ params.name }}")
# {{ params.name }} only works if you put it here, not as a kwarg

file_name = output_dict["file_name"]
csv_data = output_dict["csv_data"]

S3CreateObjectOperator(
    s3_bucket="my-example-bucket",
    s3_key=file_name,
    data=csv_data,
    task_id="s3-create-object",
    replace=False,
    encrypt=False,
    dag=dag,
)

# If you don't use dag decorator, then the configuration JSON won't auto-fill the arguments.
```
