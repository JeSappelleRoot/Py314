import logging
from random import randint
from pyminifier import compression


def ofuscate_compression(nb, source, dest):

    try:

        logger.debug(f"Source file : {source}")
        logger.debug(f"Destination file : {dest}")

        with open(source, 'r') as fileStream:
            content = fileStream.read()

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

        with open(dest, 'w') as fileStream:
            fileStream.write(result)

    except Exception as error:
        logger.warning(error)


logger = logging.getLogger('main')