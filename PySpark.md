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
    spark_session.sql(f"use ads_poststage")
    return spark_session, spark_context


if __name__ == '__main__':
    spark, sc = init_spark_session()
```
4) Test with `spark.sql("SHOW tables").toPandas()`
