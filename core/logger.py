import sys
import coloredlogs
import logging



def setup_logger(name):

    level = logging.INFO

    # Add [from %(funcName)s in %(module)s] in debug level (specify a formatter for differents level)

    formatter = logging.Formatter('[%(asctime)s]-[%(levelname)s] : %(message)s', datefmt='%H:%M:%S')

    logger = logging.getLogger(name)
    logger.setLevel(level)


    Consolehandler = logging.StreamHandler(sys.stdout)
    Consolehandler.setFormatter(formatter)
    logger.addHandler(Consolehandler)


    return logger



