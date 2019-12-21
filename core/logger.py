import sys
import coloredlogs
import logging

class CustomFormatter(logging.Formatter):
    """Logging Formatter to add colors and count warning / errors"""

    timeFormat = '%H:%M:%S'
    defaultFormat = '[%(asctime)s]-[%(levelname)s] : %(message)s'
    debugFormat = '[%(asctime)s]-[%(levelname)s] (from %(funcName)s in %(module)s) : %(message)s'
    

    FORMATS = {
        logging.DEBUG: debugFormat,
        logging.INFO: defaultFormat,
        logging.WARNING: defaultFormat,
        logging.ERROR: defaultFormat,
        logging.CRITICAL: defaultFormat
    }

    def format(self, record):
        logFormat = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(logFormat, datefmt=self.timeFormat)

        return formatter.format(record)

def setup_logger(name):

    level = logging.INFO

    # Add [from %(funcName)s in %(module)s] in debug level (specify a formatter for differents level)

    #formatter = logging.Formatter('[%(asctime)s]-[%(levelname)s] : %(message)s', datefmt='%H:%M:%S')

    logger = logging.getLogger(name)
    logger.setLevel(level)


    Consolehandler = logging.StreamHandler(sys.stdout)
    #Consolehandler.setFormatter(formatter)
    Consolehandler.setFormatter(CustomFormatter())
    logger.addHandler(Consolehandler)


    return logger



