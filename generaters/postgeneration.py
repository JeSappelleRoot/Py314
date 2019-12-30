import logging
from random import randint
from pyminifier import compression
import compilation

def ofuscate_compression(nb, src, dst):

    try:

        logger.debug(f"Source file : {src}")
        logger.debug(f"Destination file : {dst}")

        
        with open(src, 'r') as fileStream:
            content = fileStream.read()
        
        logger.info(f'Source file {src} successfully read')

        temp = content
        methods = ['bz2', 'gz2', 'lzma']


        for i in range(nb):

            random = randint(0, 2)
            method = methods[random]
            logger.debug(f"Choosen method for iteration {i} : {method}")

            if method == 'bz2':
                result = compression.bz2_pack(temp)
            elif method == 'gz2':
                result = compression.gz_pack(temp)
            elif method == 'lzma':
                result = compression.lzma_pack(temp)

            temp = result


        with open(dst, 'w') as fileStream:
            fileStream.write(result)
        
        logger.info(f"Destination file {dst} successfully written")

    except Exception as error:
        logger.warning(error)





# Define a logger for functions
logger = logging.getLogger('main')