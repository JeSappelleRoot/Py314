import sys
import coloredlogs
import logging
from termcolor import colored

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


def setup_logger(name, level):

    #level = logging.INFO

    timeFormat = '%H:%M:%S'

    if level == 20:
        formatter = logging.Formatter(
            '[%(asctime)s]-[%(levelname)s] : %(message)s', 
            datefmt=timeFormat
            )
    else:
        formatter = logging.Formatter(
            '[%(asctime)s]-[%(levelname)s] (from %(funcName)s in %(module)s) : %(message)s', 
            datefmt=timeFormat
            )

    SUCCESS, FAILURE, ASK = 21, 22, 23
    logging.addLevelName(SUCCESS, colored('+', 'green'))
    logging.addLevelName(FAILURE, colored('!', 'red',attrs=['blink']))
    logging.addLevelName(ASK, colored('?', 'yellow'))

    logger = logging.getLogger(name)
    logger.setLevel(level)

    setattr(logger, 'success', lambda *args: logger.log(SUCCESS, *args))
    setattr(logger, 'failure', lambda *args: logger.log(FAILURE, *args))
    setattr(logger, 'ask', lambda *args: logger.log(ASK, *args))

    Consolehandler = logging.StreamHandler(sys.stdout)

    
    Consolehandler.setFormatter(formatter)

    logger.addHandler(Consolehandler)


    return logger



