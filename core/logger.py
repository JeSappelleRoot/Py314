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
    """Define a logger with name and level"""

    # Define a time format
    timeFormat = '%H:%M:%S'

    # If level is logging.INFO, use short formatter
    if level == 20:
        formatter = logging.Formatter(
            '[%(asctime)s]-[%(levelname)s] : %(message)s', 
            datefmt=timeFormat
            )
    # Else, use more verbose formatter by default
    else:
        formatter = logging.Formatter(
            '[%(asctime)s]-[%(levelname)s] (from %(funcName)s in %(module)s) : %(message)s', 
            datefmt=timeFormat
            )

    # Add numeric values of news logging level
    SUCCESS, FAILURE, ASK = 21, 22, 23
    # Define new levels, with headers, and colors ;)
    logging.addLevelName(SUCCESS, colored('+', 'green'))
    logging.addLevelName(FAILURE, colored('!', 'red',attrs=['blink']))
    logging.addLevelName(ASK, colored('?', 'yellow'))

    # Define a logger with given name in argument and set level
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Add attributes to the current logger, tu use new levels
    setattr(logger, 'success', lambda *args: logger.log(SUCCESS, *args))
    setattr(logger, 'failure', lambda *args: logger.log(FAILURE, *args))
    setattr(logger, 'ask', lambda *args: logger.log(ASK, *args))

    # Define a console handler, to write output to the console
    Consolehandler = logging.StreamHandler(sys.stdout)
    # Set the formatter
    Consolehandler.setFormatter(formatter)

    # Finally add handler
    logger.addHandler(Consolehandler)


    return logger



