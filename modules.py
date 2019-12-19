
import crypto

def Shell(channel, password, command):
    """Try to interact with remote agent with a shell"""
# Module to send a shell command to remote agent

    #crypto = Crypto(password)

    # Define a buffer size, 1024 bytes
    bufferSize = 4096

    if command == b'':
        pass
    else:
        # Else, send command to remote agent
        command = crypto.encrypt_message(password, command)
        channel.sendall(command.encode())

        # While True, receive data
        while True:
            print('recv...')
            rawResponse = channel.recv(bufferSize)
            print(rawResponse)
            # If all data are smaller than the buffer size, break While loop
            if len(rawResponse) < bufferSize:
                print('break !')
                break
        # Decode bytes to string to read the answer of the remote agent
        shellReponseEncrypted = rawResponse.decode()
        shellResponse = crypto.decrypt_message(password, shellReponseEncrypted)
        # Print agent's answer
        print(shellResponse)

