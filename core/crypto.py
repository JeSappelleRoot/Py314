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

    # Get main logger
    logger = logging.getLogger('main')

    # Create a string hasher with SHA256 algoritm
    digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
    # Add password to hasher 
    digest.update(password.encode())
    # Generate Fernet key from the SHA256 digest of password
    key = base64.urlsafe_b64encode(digest.finalize())

    logger.debug(f"Password to generate key : {password}")
    logger.debug(f"Key generated : {key}")

    return key

def encrypt_file(password, infile, outfile):
    """Encrypt file"""

    try:

        # Get main logger
        logger = logging.getLogger('main')
        # Create fernet object, with key from given password
        fernet = Fernet(generate_key(password))

        # Open source plain file in binary read mode and get content
        with open(infile, 'rb') as fileStream:
            plainData = fileStream.read()

        # Open output file in binary creation mode
        with open(outfile, 'xb') as fileStream:
            # Encrypt plain content of source file and write it to the destination file
            encrypted = fernet.encrypt(plainData)
            fileStream.write(encrypted)

        logger.debug(f"Source file for encryption : {infile}")
        logger.debug(f"Destination for encryption : {outfile}")
            
    except Exception as error:
        logger.warning(f"An error occured during file encryption : {error}")


def encrypt_message(password, message):
    """Encrypt a message with str type and return message as str encrypted"""
    
    try:

        # Get main logger
        logger = logging.getLogger('main')
        # Create fernet object with key from password
        fernet = Fernet(generate_key(password))

        # Encode message (str to bytes)
        message = message.encode()
        # And encrypt this message with Fernet
        encrypted = fernet.encrypt(message)

        logger.debug(f"Message before encryption : {message.decode()}")
        logger.debug(f"Message after encryption : {encrypted.decode()}")

        return encrypted.decode()
    
    except InvalidToken as error:
        logger.warning(f'An error occured during message encryption : {error}')



def decrypt_file(password, infile, outfile):
    """Encrypt file"""

    try:

        # Get main logger
        logger = logging.getLogger('main')
        # Create fernet object with key from password
        fernet = Fernet(generate_key(password))

        # Open encrypted source file in binary read mode
        with open(infile, 'rb') as fileStream:
            cipherData = fileStream.read()
        # Open plain destination ffile in write binary mode
        with open(outfile, 'wb') as fileStream:
            # Decrypt the encrypted content with fernet
            decrypted = fernet.decrypt(cipherData)
            # And write it to output file
            fileStream.write(decrypted)

        logger.debug(f"Source file for decryption : {infile}")
        logger.debug(f"Destination for decryption : {outfile}")
            
    except Exception as error:
        logger.warning(f"An error occured during file decryption : {error}")


def decrypt_message(password, message):
    """Decrypt a message with str type and return message as str decrypted"""

    try:

        # Get the main logger
        logger = logging.getLogger('main')
        # Create a fernet object with key from password
        fernet = Fernet(generate_key(password))
        # Encode message (str to bytes)
        message = message.encode()
        # Decrypted encrypted message with the fernet object
        decrypted = fernet.decrypt(message)

        logger.debug(f"Message before decryption : {message.decode()}")
        logger.debug(f"Message after decryption : {decrypted.decode()}")

        return decrypted.decode()

    except InvalidToken as error:
        logger.warning(f'An error occured during message decryption : {error}')

