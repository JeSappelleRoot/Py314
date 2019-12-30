import logging
from random import randint
from pyminifier import compression


def ofuscate_compression(nb, src, dst):

    try:
        # Some debug
        logger.debug(f"Iterations : {nb}")
        logger.debug(f"Source file : {src}")
        logger.debug(f"Destination file : {dst}")

        # Open source file and get the content
        with open(src, 'r') as fileStream:
            content = fileStream.read()
        # Initialize a temporary file
        temp = content
        # Define availables methods
        methods = ['bz2', 'gz2', 'lzma']

        # Loop for n iteration of compression process
        for i in range(nb):
            # Get random in between 0 and 2 (includes)
            random = randint(0, 2)
            # Choose method with this random int
            method = methods[random]
            # Some debug
            logger.debug(f"Choosen method for iteration {i + 1} : {method}")
            # Switch case with method and compress
            if method == 'bz2':
                result = compression.bz2_pack(temp)
            elif method == 'gz2':
                result = compression.gz_pack(temp)
            elif method == 'lzma':
                result = compression.lzma_pack(temp)
            # Assign temp to result in case of multiple iterations
            temp = result

        # Open destination file a write the compressed agent
        with open(dst, 'w') as fileStream:
            fileStream.write(result)
        # Display info
        logger.info(f"Agent {src} successfully compressed with {nb} iterations")

    except Exception as error:
        logger.warning(error)





# Define a logger for functions
logger = logging.getLogger('main')