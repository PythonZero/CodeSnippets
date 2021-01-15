# Using Pyspark with pycharm

### Test locally (Terminal)

1) Check `pyspark` works in bash terminal
2) `USE <database_name>`
3) `spark.sql("SHOW TABLES").collect()`

### Test in PyCharm script
1) Add `SPARK_HOME`
- Should point to spark installation, e.g. `os.environ["SPARK_HOME"] = "/usr/lib/spark"`

2) Add `PYTHONPATH§
- Should contain `$SPARK_HOME/python` and `$SPARK_HOME/python/lib/py4j-<version>.src.zip`
  * e.g. `/usr/lib/spark/python/lib/py4j-0.10.7-src.zip:/usr/lib/spark/python/:`

3) Create the spark session
```python
from pyspark import SparkContext
from pyspark import SparkConf
from pyspark.sql.session import SparkSession

os.environ["SPARK_HOME"] = "/usr/lib/spark"
os.environ["PYTHONPATH"] += ':/usr/lib/spark/python/lib/py4j-0.10.7-src.zip:/usr/lib/spark/python/:'

def init_spark_session():
    conf = SparkConf()
    conf.set("hive.metastore.client.factory.class",
             "com.amazonaws.glue.catalog.metastore.AWSGlueDataCatalogHiveClientFactory")
    spark_context = SparkContext(conf=conf)
    spark_session = SparkSession.builder \
        .appName("<Give it a name>") \
        .config(conf=conf) \
        .enableHiveSupport() \
        .getOrCreate()
    spark_session.sparkContext.setLogLevel('WARN')
    spark_session.sql(f"use db_name")
    return spark_session, spark_context


if __name__ == '__main__':
    spark, sc = init_spark_session()
```
4) Test with `spark.sql("SHOW tables").toPandas()`

### Adding python modules
* i.e. if you need to use a function from a module inside a UDF
```python
def _zip_module(name="module_name") -> None:
    """Creates a zip of the module, allowing the functions to
    be importable within the pyspark worker modules.

    :param name: Path to folder inside the root folder
    """
    path_to_folder = os.path.join(ROOT_DIR, name)
    shutil.make_archive(path_to_folder, "zip", ROOT_DIR, name)

# After creating the spark_context and spark_session
_zip_module("my_py_module")
spark_context.addPyFile(os.path.join(ROOT_DIR, "module_name.zip"))
spark_context.addPyFile(PATH_TO_DAYS_IN_MP_PY_FILE)
```

## Debugging pyspark (spark-submit) in pycharm

## For a remote machine
1) Port Forward a port from the ssh machine to yours (e.g. port 12345)
```ssh -R 12345:localhost:12345 user@192.168.0.1```

2) In PyCharm -> top right -> click the python runner, e.g. -> Edit Configurations 
3) Click the "+" icon -> Python Debug Server
4) Set the IDE host name to `localhost`, and the port to the port assigned in step 1 (e.g. 12345).
   Give it a nice name, e.g. `debug-port-12345`
5) On the running machine, run `pip install pydevd-pycharm`
6) At the top of your code, add these two lines
```python
import pydevd_pycharm
pydevd_pycharm.settrace('localhost', port=$SERVER_PORT, stdoutToServer=True, stderrToServer=True)
```
7) Run your code on the remote machine, e.g. through spark-submit or whatever
8) **THEN** start the python debug server you made in step 4 by pressing the bug button
   * Note: if you run the debug server before starting your code, it may not connect
9) You will get a prompt, click auto-detect the code. If that fails, click download from source
10) Happy debugging!
