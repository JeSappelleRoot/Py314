import logging
from random import randint
from pyminifier import compression


def ofuscate_compression(nb, source, dest):

    try:

        with open(source, 'r') as fileStream:
            content = fileStream.read()

        temp = content
        methods = ['bz2', 'gz2', 'lzma']


        for i in range(nb):

            random = randint(0, 2)
            method = methods[random]
            print(f"Méthode choisie : {method}")

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
        print(error)


logger = logging.getLogger('main')