import sys
import coloredlogs
import logging



def setup_logger(name):

    level = logging.INFO

    formatter = logging.Formatter('[%(asctime)s]-[%(levelname)s] : %(message)s', datefmt='%H:%M:%S')

    logger = logging.getLogger(name)
    logger.setLevel(level)


    Consolehandler = logging.StreamHandler(sys.stdout)
    Consolehandler.setFormatter(formatter)
    logger.addHandler(Consolehandler)


    return logger



