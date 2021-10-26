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


# Write stderr / stdout to log


# Solving problem where StreamHandler causes infinite Recurison
#  (I also posted this on stackoverflow - https://stackoverflow.com/a/69728826/8751871)

class DefaultStreamHandler(logging.StreamHandler):
    def __init__(self, stream=sys.__stdout__):
        # Use the original sys.__stdout__ to write to stdout
        # for this handler, as sys.stdout will write out to logger.
        super().__init__(stream)


class LoggerWriter(io.IOBase):
    """Class to replace the stderr/stdout calls to a logger"""

    def __init__(self, logger_name: str, log_level: int):
        """:param logger_name: Name to give the logger (e.g. 'stderr')
        :param log_level: The log level, e.g. logging.DEBUG / logging.INFO that
                          the MESSAGES should be logged at.
        """
        self.std_logger = logging.getLogger(logger_name)
        # Get the "root" logger as described by the config.py file,
        #  in the config dict, i.e. {"loggers": {"myAppsLogger": {"handlers": ...}}}.
        #  We will use this to create a copy of all its settings, except the name
        app_logger = logging.getLogger("myAppsLogger")
        [self.std_logger.addHandler(handler) for handler in app_logger.handlers]
        self.std_logger.setLevel(app_logger.level)  # the minimum lvl msgs will show at
        self.level = log_level  # the level msgs will be logged at
        self.buffer = []

    def write(self, msg: str):
        """Stdout/stderr logs one line at a time, rather than 1 message at a time.
        Use this function to aggregate multi-line messages into 1 log call."""
        msg = msg.decode() if issubclass(type(msg), bytes) else msg

        if not msg.endswith("\n"):
            return self.buffer.append(msg)

        self.buffer.append(msg.rstrip("\n"))
        message = "".join(self.buffer)
        self.std_logger.log(self.level, message)
        self.buffer = []


def replace_stderr_and_stdout_with_logger():
    """Replaces calls to sys.stderr -> logger.info & sys.stdout -> logger.error"""
    # To access the original stdout/stderr, use sys.__stdout__/sys.__stderr__
    sys.stdout = LoggerWriter("stdout", logging.INFO)
    sys.stderr = LoggerWriter("stderr", logging.ERROR)


if __name__ == __main__():
    # Load the logger & handlers
    logger = logging.getLogger("myAppsLogger")
    logger.setLevel(logging.DEBUG)
    # HANDLER = logging.StreamHandler()  # <--- see line below
    HANDLER = DefaultStreamHandler()  # <--- replace the normal streamhandler with this
    logger.addHandler(HANDLER)
    logFormatter = logging.Formatter("[%(asctime)s] - %(name)s - %(levelname)s - %(message)s")
    HANDLER.setFormatter(logFormatter)

    # Run this AFTER you load the logger
    replace_stderr_and_stdout_with_logger()
