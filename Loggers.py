#Logging
import sys
logging.basicConfig(
    filename=generate_file_name("logs.log"),
    level=logging.DEBUG,
    format="[%(asctime)s] - %(name)s - %(levelname)s - %(message)s",
)
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))  # also output to console.

LOGGER = logging.getLogger('logfilename')
LOGGER.debug('Logger ready')

#Logging2
logger = logging.getLogger() # or getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

#Logging2 with formatter
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
logger.addHandler(handler)
logFormatter = logging.Formatter("[%(asctime)s] - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(logFormatter)

#Logging3 - Get all logs
logger = logging.root # WORKS
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())
logger = logging.getLogger('root') # DOES NOT WORK as you can't access the root logger from getLogger

# Another way to get the root Logger:
logger = logging.getLogger()
logger = logging.getLogger(None) # I think <-- check this then delete this comment

#Silencing Loggers:
logging.getLogger("requests").setLevel(logging.WARNING) # or paramiko, or urllib3 (whatever library).
