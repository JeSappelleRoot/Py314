import os
import logging
from cmd import Cmd
from random import randint
from termcolor import colored
from generaters import template
from prettytable import PrettyTable

class Prompt(Cmd):
    """Simple Py314 agent factory"""

    availableTypes = ['bind_agent', 'reverse_listener']
    homeFolder = os.environ['HOME']
    py314Folder = f"{homeFolder}/.Py314"

    optionsDict = {
        'host':         [1, '10.0.10.110'],
        'port':         [2, 1234],
        'password':     [3, 'Py314!'],
        'type':         [4, 'bind_agent'],
        'outfile':      [5, f"{py314Folder}/agent.py"],
        'compress':     [6, False],
        'iterations':   [7, randint(2, 12)],
        'compile':      [8, False]
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

    def do_generate(self, arg):
        """Generate agent with given options"""

        generation = True

        logger.debug(f"Type : {self.optionsDict['type'][1]}")
        logger.debug(f"Outfile : {self.optionsDict['outfile'][1]}")
        logger.debug(f"Host : {self.optionsDict['host'][1]}")
        logger.debug(f"Port : {self.optionsDict['port'][1]}")
        logger.debug(f"Password : {self.optionsDict['password'][1]}")
        logger.debug(f"Compression : {self.optionsDict['compress'][1]}")
        logger.debug(f"Iterations : {self.optionsDict['iterations'][1]}")
        logger.debug(f"Compile : {self.optionsDict['compile'][1]}")

        for key, value in self.optionsDict.items():
            if value == '':
                generation = False
                logger.warning(f"The option {key} can't be empty")

        if generation is True:


            socket = template.createSocket(self.optionsDict['type'][1])
            template.writeAgent(
                self.optionsDict['outfile'][1],
                socket,
                self.optionsDict['host'][1],
                self.optionsDict['port'][1],
                self.optionsDict['password'][1]
            )
                

    def do_options(self, arg):
        """Show currents settings of handler"""

        print("""\nThe bind_agent handler is designed to bind a specified host with IP & port combination.""")
        print("""If the connection is successfull, a shell is automatically give, and remote actions are allowed\n""")

        table = PrettyTable()
        headers = ['weight', 'name', 'value', 'description']
        table.field_names = headers
        for header in headers:
            table.align[header] = 'l'

        for option in dir(self):
            if option.startswith('set_'):
                optionName = option.replace('set_', '')
                optionWeight = self.optionsDict[optionName][0] 
                optionValue = self.optionsDict[optionName][1]
                optionDoc = getattr(self, option).__doc__

                table.add_row([optionWeight, optionName, optionValue, optionDoc])

        #print(table)

        print(table.get_string(fields=['name', 'value', 'description'],sortby='weight'))



    def do_set(self, arg):
        """Set value for available option : set <option> <value>"""

        if len(arg.split(' ')) > 2 or len(arg.split(' ')) < 2:
            logger.warning(f"Please specify set <option> <value>")
        
        else:

            availableOptions = [options.replace('set_', '') for options in dir(self) if options.startswith('set_')]
            option = arg.split(' ')[0]
            value = arg.split(' ')[1]

            if option not in availableOptions:
                logger.warning(f"Option {option} can't be set")

            elif option == 'type' and value not in self.availableTypes:
                logger.warning(f"Specify a valid type of agent : ")
                for agent in self.availableTypes:
                    print(f" - {agent}")

            if option == 'compress' or option == 'compile':
                if value.capitalize() == 'True':
                        self.optionsDict[option][1] = True
                elif value.capitalize() == 'False':
                    self.optionsDict[option][1] = False
                else:
                    logger.warning(f'Set {option} option to True or False')
                
            else:
                logger.debug(f'Option [{option}] set to [{value}]')
                self.optionsDict[option][1] = value



    def do_unset(self, arg):
        """Unset value for available option : unset <option>"""

        if len(arg.split(' ')) > 1 or len(arg.split(' ')) < 1:
            logger.warning(f"Please specify unset <option>")
        
        else:

            availableOptions = [options.replace('set_', '') for options in dir(self) if options.startswith('set_')]
            option = arg.split(' ')[0]

            if option not in availableOptions:
                logger.warning(f"Option {option} can't be unset")
            else:
                self.optionsDict[option][1] = ''




# < -------------------------- factory OPTIONS -------------------------- >

    def set_type(self):
        """Define the type of agent : bind_agent/reverse_listener"""

    def set_host(self):
        """Define the IP address to bind/listen"""

    def set_outfile(self):
        """Define the output file which contain agent script"""

    def set_port(self):
        """Define the port of Py314 agent to bind/listen"""

    def set_password(self):
        """Define a password use to connect to Py314 agent and to perform symetric encryption of traffic"""

    def set_compress(self):
        """Enable or disable compression to obfuscate agent code (random choice between bz2, gz2, lzma)"""

    def set_iterations(self):
        """Define number of successives random compression (ignored if compress is set to False)"""
    
    def set_compile(self):
        """Enable or disable final compilation : (ELF binary)"""





def startFactory():

    

    subPrompt = Prompt()
    subPrompt.prompt = f"({colored('factory', 'magenta')}) > "
    subPrompt.cmdloop()


# --------------------------------------------------------------------
# --------------------------- Main -----------------------------------
# --------------------------------------------------------------------

logger = logging.getLogger('main')