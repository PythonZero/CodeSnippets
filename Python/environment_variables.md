## Use environs

```python
from environs import Env

env = Env()
env.read_env()    # read .env file, if it exists

# casting variables
S3_BUCKET_NAME = env.str("S3_BUCKET_NAME", "default-bucket-name")  # 2nd arg = default value
MAX_CONNECTIONS = env.int("MAX_CONNECTIONS")  # => 100
SHIP_DATE = env.date("SHIP_DATE")  # => datetime.date(1984, 6, 25)
TTL = env.timedelta("TTL")  # => datetime.timedelta(0, 42)
LOG_LEVEL = env.log_level("LOG_LEVEL")  # => logging.DEBUG

# required variables
GITHUB_USER = env("GITHUB_USER")  # => 'sloria'
SECRET = env("SECRET")  # => raises error if not set

```
