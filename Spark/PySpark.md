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
