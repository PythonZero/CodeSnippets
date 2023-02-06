# EMR and python / pyspark

## Converting Python code → Pyspark

1. Write the python program normally
2. Refactor the code to contain the code that can be parallelised into a function / functions
   * Make sure no picklable stuff are passed into args (recreate them)
   * ```python
     import os, boto3
     
     def load_and_parse_file(args):
         file_name, date, something_else = args  # you can only pass 1 arg, so unpack it
         # You can't pass non-picklable stuff (like GCP client), so recreate it
         s3_client = boto3.client(
              "s3",
              aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
              aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"])
         # NOTE: if you are passing environment variables in EMR AWS,
         # ensure you pass as a --conf (see below)
         file_contents = s3_client.get_object(file_name)["Body"]
         parsed_contents = do_something(file_contents)
         save_to_s3(parsed_contents)
         return parsed_contents
       ```
3. Add this to your code
   * ```python
      from pyspark.sql import SparkSession
      if __name__ == "__main__:
          spark_session = SparkSession.builder.appName("Parse Files on S3").getOrCreate()
     ```
4. The magic part ... 
   1. Get the iterable that you will be iterating over, i.e. file_names
   * ```python
        s3_files = list_all_files(s3_client, AWS_BUCKET_NAME)
        x = 10
        date = "2022-01-01"
        file_name_date__sth_else = [(f, date, x) for f in s3_files] 
     ```
   2. Convert it into an RDD (resilient Distributed Dataset):
   *   ```python
        s3_files_rdd = spark_session.sparkContext.parallelize(file_name_date__sth_else)
       ```
   3. Run it parallelised!
   * ```python
      all_parsed_files = s3_files_rdd.map(load_and_parse_file).collect()
      # you can then use  the `all_parsed_files` variable if you wish
      # as normal in python
      ```

## How to run it?

### Easy: Locally
   * `python filename.py` - it will automatically use pyspark


### Medium: Locally with `spark-submit`
#### Quickstart:
   * `spark-submit --master local[*] question1_pysparked.py`
     * The `[*]` mentions how many workers to use (i.e. [8] )
#### How does it work?
   * It auto-detects that the python code is actually spark / pyspark code
   * It submits the job to the cluster (local)
   * Waits for it to complete, then brings back the values to python

#### Tips:
   * Environment Variables
     * Set them in your **command prompt**
       * e.g. `set AWS_ACCESS_KEY_ID=XXXXXXXXXXX` (on windows) or `export AWS_ACCESS_KEY_ID=XXXXXXXXXXX` (linux)
       * repeat for all the variables in the .env file
     * pass as args **does not work** if you need to access in master node 
       * `--conf "spark.executorEnv.ENV_VAR=value"` 
   * Ensure you have installed the requirements using `pip install requirements.txt`
   * Ensure you are using the correct python with pyspark  by setting `PYSPARK_PYTHON`
     * This should be the python that you `pip installed` the requirements

### Difficult: EMR in AWS


#### Quickstart:
* Create a `bootstrap.sh` to `pip install ` dependencies, and any other 
  * Upload it to a bucket in S3
* Zip up custom modules (ensure it has `__init__.py`) 
  * Upload it to a bucket in S3
* Environment Variables must be passed using `--conf "spark.executorEnv.ENV_VAR=value"`
  * passing it in via ` --configurations file://C:/path/to/spark_config.json` will only provide
    it to the master node and not slaves
* ```bash
  aws emr create-cluster \
    --name "My Cluster Name" \
    --release-label emr-6.9.0 \
    --applications Name=Hadoop Name=Spark \
    --instance-type c4.xlarge \
    --instance-count 3 \
    --bootstrap-actions Path=s3://my_bucket/my_pkg/bootstrap.sh \
    --use-default-roles \
    --log-uri s3://aws-logs-177153431722-us-east-1/logs \
    --steps Type=CUSTOM_JAR,Name="Run spark-submit using command-runner.jar",ActionOnFailure=CONTINUE,Jar=command-runner.jar,Args=[spark-submit,--py-files,s3://my-bucket/my_pkg/my_pkg.zip,--conf,spark.executorEnv.Key1=Value1,--conf,spark.executorEnv.Key2=Value2,s3://my-bucket/my_pkg/main.py] \
    --ec2-attributes '{"KeyName":"myKeyPair"}'  \  # Optional: if you want to remote in
    --auto-terminate
  ```

#### Background:
* `command-runner.jar` is a pre-built jar that allows you to use `spark-submit` by passing args in EMR
* A `step` is just a `spark-submit` that you want to run. You can run multiple.

#### Setup & SSH into Master EMR machine:
* In EMR / EC2 - `Security` -> Create an inbound rule to allow `SSH` for all ipv4 AND ipv6 addresses 
  *  (or tighten it to only include your IPs)
  * `::/0` will only work for ipv6 (and not ipv4) and `0.0.0.0/0` only for IPv4 (and not ipv6) 
* In EC2 Key Pairs - Create a security key (i.e. `myKeyPair.ppk` for PuTTy) and assign it to the master machine in EMR
  1. On PuTTY `Connection -> Auth -> Credentials` browse for that `Private Key file` (`myKeyPair.ppk`)
  2. On PuTTY `Session -> HostName = hadoop@internal-ip-address.com`, e.g. `hadoop@ec2-3-239-49-216.compute-1.amazonaws.com`
  3. Press save before connecting to save you time (Give it a session name)

#### Running code in Master EMR machine
* **If you are remoted into the machine**
  * ```bash
    spark-submit  --py-files s3://my-bucket/my_pkg/my_pkg.zip  --conf "spark.executorEnv.ENV_VAR=value"  --conf "spark.executorEnv.ENV_VAR2=value2" s3://my-bucket/my_pkg/main.py
    ``` 
    * NOTE: order matters (`main.py` must be at the end)
    * Env Variables: `--conf "spark.executorEnv.ENV_VAR=value"` - add as many as you want in order
      * This will also pass env variables to the slave nodes
* **If you want to replicate a "step"**
  * ```bash
      aws emr add-steps \
         --cluster-id j-ABCD123456 \
         --steps Type=CUSTOM_JAR,Name="Run spark-submit using command-runner.jar",ActionOnFailure=CONTINUE,Jar=command-runner.jar,Args=[spark-submit,--py-files,s3://my-bucket/my_pkg/my_pkg.zip,--conf,spark.executorEnv.Key1=Value1,--conf,spark.executorEnv.Key2=Value2,s3://my-bucket/my_pkg/main.py]
    ```

#### Things that worked:
* `bootstrap.sh` only needed to `pip install` the requirements
* You must read env variables **BEFORE** creating the spark context -> otherwise not added.

#### Stuff I tried that didn't work:

* **Problem** - EMR was not recognising my custom module.
* **What I tried** - Fixing it using `bootstrap.sh`
  * Creating a zip locally
  * ```bash
      aws s3 cp --recursive s3://my-emr-bucket/ ~
      zip ~/my_pkg/my_pkg.zip ~/my_pkg/my_pkg/
      ```
      * Didn't work - the slave nodes wouldn't recognise `--py-files  /my_pkg/my_pkg.zip`
        * ONLY recognised when passed via `s3://`
  * Adding the package to the PYTHONPATH   
     * `export PYTHONPATH="${PYTHONPATH}:~/my_pkg"`
  * Changing the directory to the package 
    * `cd ~/my_pkg`
  * **CAVEAT** - some of these might have worked, I also had a bug in my code when moving to EMR.
* **How I fixed it?** - pass the `--py-files s3://bucket/my_pkg.zip`
