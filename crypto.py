import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend



class Crypto():
    """Simple class to perform encryption and decryption with Fernet. Initialize with crypto = Crypto('password')"""

    def __init__(self, password):
    
        self.password = password.encode()
        digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
        digest.update(self.password)

        self.key = base64.urlsafe_b64encode(digest.finalize())

        self.fernet = Fernet(self.key)


    def encrypt_file(self, infile, outfile):
        """Encrypt file"""

        try:

            with open(infile, 'rb') as fileStream:
                plainData = fileStream.read()

            with open(outfile, 'wb') as fileStream:

                encrypted = self.fernet.encrypt(plainData)
                fileStream.write(encrypted)
                
        except Exception as error:
            print(error)


    def encrypt_message(self, message):
        """Encrypt a message with str type and return message as str encrypted"""
        
        message = message.encode()
        encrypted = self.fernet.encrypt(message)

        return encrypted.decode()
        
    def decrypt_file(self, infile, outfile):
        """Encrypt file"""

        try:

            with open(infile, 'rb') as fileStream:
                cipherData = fileStream.read()

            with open(outfile, 'wb') as fileStream:

                decrypted = self.fernet.decrypt(cipherData)
                fileStream.write(decrypted)
                
        except Exception as error:
            print(error)

    
    def decrypt_message(self, message):
        """Decrypt a message with str type and return message as str decrypted"""

        message = message.encode()
        decrypted = self.fernet.decrypt(message)

        return decrypted.decode()

    def debug(self):
        """Function to print password and generated key"""
        
        print(self.password.decode())
        print(self.key.decode())



