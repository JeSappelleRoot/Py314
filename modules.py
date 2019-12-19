from crypto import Crypto

def Shell(channel, password, command):
    """Try to interact with remote agent with a shell"""
# Module to send a shell command to remote agent

    #crypto = Crypto(password)

    # Define a buffer size, 1024 bytes
    bufferSize = 1024

    if command == b'':
        pass
    else:
        # Else, send command to remote agent
        channel.sendall(command.encode())

        # While True, receive data
        while True:
            rawResponse = channel.recv(bufferSize)
            # If all data are smaller than the buffer size, break While loop
            if len(rawResponse) < bufferSize:
                break
        # Decode bytes to string to read the answer of the remote agent
        shellReponse = rawResponse.decode()
        # Print agent's answer
        print(shellReponse)

