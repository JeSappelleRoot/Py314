import os
import base64
import hashlib
import logging
from cryptography.fernet import Fernet, InvalidToken, InvalidSignature
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# https://incolumitas.com/2014/10/19/using-the-python-cryptography-module-with-custom-passwords/



def generate_key(password):
    """Generate fernet key from password"""

    logger = logging.getLogger('main')

    digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
    digest.update(password.encode())
    key = base64.urlsafe_b64encode(digest.finalize())

    logger.debug(f"Password to generate key : {password}")
    logger.debug(f"Key generated : {key}")

    return key

def encrypt_file(password, infile, outfile):
    """Encrypt file"""

    try:

        logger = logging.getLogger('main')
        fernet = Fernet(generate_key(password))

        with open(infile, 'rb') as fileStream:
            plainData = fileStream.read()

        with open(outfile, 'xb') as fileStream:

            encrypted = fernet.encrypt(plainData)
            fileStream.write(encrypted)

        logger.debug(f"Source file for encryption : {infile}")
        logger.debug(f"Destination for encryption : {outfile}")
            
    except Exception as error:
        logger.failure(f"An error occured during file encryption : {error}")


def encrypt_message(password, message):
    """Encrypt a message with str type and return message as str encrypted"""
    
    try:

        logger = logging.getLogger('main')
        fernet = Fernet(generate_key(password))

        message = message.encode()
        encrypted = fernet.encrypt(message)

        logger.debug(f"Message before encryption : {message}")
        logger.debug(f"Message after encryption : {encrypted.decode()}")

        return encrypted.decode()
    
    except InvalidToken as error:
        logger.failure(f'An error occured during message encryption : {error}')



def decrypt_file(password, infile, outfile):
    """Encrypt file"""

    try:

        logger = logging.getLogger('main')
        fernet = Fernet(generate_key(password))

        with open(infile, 'rb') as fileStream:
            cipherData = fileStream.read()

        with open(outfile, 'wb') as fileStream:

            decrypted = fernet.decrypt(cipherData)
            fileStream.write(decrypted)

        logger.debug(f"Source file for decryption : {infile}")
        logger.debug(f"Destination for decryption : {outfile}")
            
    except Exception as error:
        logger.failure(f"An error occured during file decryption : {error}")


def decrypt_message(password, message):
    """Decrypt a message with str type and return message as str decrypted"""

    try:

        logger = logging.getLogger('main')
        fernet = Fernet(generate_key(password))

        message = message.encode()
        decrypted = fernet.decrypt(message)

        logger.debug(f"Message before decryption : {message}")
        logger.debug(f"Message after decryption : {decrypted.decode()}")

        return decrypted.decode()

    except InvalidToken as error:
        logger.failure(f'An error occured during message decryption : {error}')

