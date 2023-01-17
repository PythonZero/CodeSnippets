## Quickstart
```python
from environs import Env

env = Env()
env.read_env()    # read .env file, if it exists

# default value (& casting)
S3_BUCKET_NAME = env.str("S3_BUCKET_NAME", "default-bucket-name") 

```

## Using it in Code (v1 - see v2)
```python
from environs import Env

class EnvVariables:
    s3_bucket_name: str

    def __init__(self):
        self.env = Env()
        self.env.read_env()  # read .env file, if it exists
        self.s3_bucket_name = self.env.str("S3_BUCKET_NAME")  # no default => will error if env var not exists
```


## More examples

https://pypi.org/project/environs/
```cmd
pip install environs
```

```python
from environs import Env

env = Env()
env.read_env()    # read .env file, if it exists

# default value (& casting)
S3_BUCKET_NAME = env.str("S3_BUCKET_NAME", "default-bucket-name") 

# casting variables
MAX_CONNECTIONS = env.int("MAX_CONNECTIONS")  # => 100
SHIP_DATE = env.date("SHIP_DATE")  # => datetime.date(1984, 6, 25)
TTL = env.timedelta("TTL")  # => datetime.timedelta(0, 42)
LOG_LEVEL = env.log_level("LOG_LEVEL")  # => logging.DEBUG

# required variables
GITHUB_USER = env("GITHUB_USER")  # => 'sloria'
SECRET = env("SECRET")  # => raises error if not set

```

## Using it in Code with tests (v2)

```python

from environs import Env


class EnvVarMeta(type):
    def __init__(cls, *args, path=None):
        # Use environs to force type checks
        super().__init__(cls)
        cls.env = Env()
        cls.env.read_env()  # read .env file, if it exists
        cls.vars = {}

    def clear(cls):
        for var in cls.vars.keys():
            delattr(cls, var)
        cls.vars = {}

    def path(cls, path, override=False, *args, **kwargs):
        """Reads env from a path.

        :param path: path/to/the/.env file (e.g. `file1.env` or `.env`)
        :param override - if True, then it overrides any existing env variables.
                          Otherwise, any existing env variables take precedent."""
        cls.env.read_env(path=path, override=override, *args, **kwargs)

    def __getattr__(cls, name):
        if hasattr(cls.env, name):
            # Allows usage of e.g. EnvVariables.str("x") -> loads the env variable and saves it as EnvVariables.x
            return lambda env_name, *a, **kw: cls.save_using_env(name, env_name, *a, **kw)
        raise KeyError(
            f"'{name}' not found. Ensure you've loaded the EnvVar by doing "
            f"'{cls.__name__}.str({name})'  or"
            f" '{cls.__name__}.env({name})' (if not specifying the type)."
            f"\n      See https://pypi.org/project/environs/#:~:text=2%2C%20%27konch%27%3A%203%7D-,Supported,-types "
            f"for all Supported types "
        )

    def save_using_env(cls, func, env_name, *args, **kwargs):
        env_value = getattr(cls.env, func)(env_name, *args, **kwargs)
        setattr(cls, env_name, env_value)
        cls.vars[env_value] = env_value
        return env_value


class EnvVariables(metaclass=EnvVarMeta):
    """Usage: (NOTE: Do not need to create an instance, can use as a class)

    Access the env variable using dot notation, e.g. EnvVariables.AWS_S3_BUCKET

    Works exactly like Env(), but also stores the variables as class attributes,
      # access all the Env methods by doing EnvVariables.method_name
      # if a method name is not passed, then looks for the variable instead (auto-type detect)

    Usage:

    ```
    # define all the types of the env variables
    def setup_env_vars():
        EnvVariables.path("path/to/file.env")  # optional
        EnvVariables.str("var1")
        EnvVariables.int("var2")

    setup_env_vars()

    # Use them in the code
    my_func(EnvVariables.var1)
    my_func2(EnvVariables.var2)
    my_func3(EnvVariables.str("var3"))  # can also pass it directly in
    ```

    See https://pypi.org/project/environs/ for all env.<method> methods.
    """

    def __getattr__(self, name):
        """Overrides the __getattr__ if being access from an instance"""
        return getattr(type(self), name)
```

### .env file
```env
X=1
Y=hello_world
Z=whatsup_bro!
```

### tests
```python
import os.path

import pytest

from dags.helpers.env_vars import EnvVariables

ROOT_DIR = os.path.abspath(os.path.join(__file__, "..", ".env"))


def test_env_vars__reassigning_type():
    EnvVariables.path(ROOT_DIR, override=True)
    EnvVariables.str("X")
    assert EnvVariables.X == "1"
    EnvVariables.int("X")
    assert EnvVariables.X == 1
    assert EnvVariables.X == 1


def test_env_vars__env_functions():
    EnvVariables.path(ROOT_DIR)
    assert EnvVariables.str("Y") == "hello_world"
    assert EnvVariables.str("Z") == "whatsup_bro!"


def test_env_vars__with_default():
    assert EnvVariables.bool("SOMETHING_THAT_DOESNT_EXIST2", False) is False
    assert (
        EnvVariables.str("ANOTHER_THING_I_MADE_UP", "default_value") == "default_value"
    )
    assert EnvVariables.str("X", "do_not_use_default") == "1"


def test_env_vars_error_if_not_loaded():
    with pytest.raises(
        KeyError, match="'SOMETHING_THAT_DOESNT_EXIST' not found. Ensure .*"
    ):
        EnvVariables.SOMETHING_THAT_DOESNT_EXIST
```
