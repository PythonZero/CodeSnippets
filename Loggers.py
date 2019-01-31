#Logging
logging.basicConfig(filename=r"path/to/logfile.log",
                    level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
LOGGER = logging.getLogger('logfilename')
LOGGER.debug('Logger ready')

#Logging2
logger = logging.getLogger() # or getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

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
