# Debugging 

## Pycharm Docker Debugging
* Place debug statements within `@task` OR `execute` functions
  - Placing them outside can be annoying because refreshing a webpage will
    cause the DAG code to rerun
## Docker Debugging
* Replace the `localhost` URL with `"host.docker.internal"`, and use any port (e.g. `3184`)

# Operators

## Extending an Operator

### BaseOperator
```python
from airflow.models import BaseOperator

class HelloOperator(BaseOperator):
    def __init__(self, name: str, **kwargs) -> None:
        super().__init__(**kwargs)
        self.name = name

    def execute(self, context):
        data = context['task_instance'].xcom_pull("task_1", key="payload")
        message = f"Hello {self.name}"
        print(message)
        return message
```

### Custom Operator
```python
from airflow.providers.amazon.aws.operators.s3 import S3CreateObjectOperator

class S3OpAhmedCustom(S3CreateObjectOperator):
    def execute(self, context):
        self.aws_conn_id = context['task_instance'].xcom_pull()  # does not have this behaviour
        return super(S3OpAhmedCustom, self).execute(context)

```

## Accessing xcom variables in Operators

* `xcom` variables are only available in the `execute` method and not the `__init__`
* To access, extract from the `context`, e.g.
    * ```python
      
      def execute(self, context):
          self.var = context['task_instance'].xcom_pull()
      ```
