
from cmd import Cmd
from termcolor import colored

class Prompt(Cmd):
    """Simple Py314 agent factory"""

    availableTypes = ['bind_agent', 'reverse_listener']

    optionsDict = {
        'type': '',
        'rhost': '',
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
# < -------------------------- COMMANDS -------------------------- >

    def do_bg(self, arg):
        """Return to Py314 main interpreter"""
        return True

    def do_exit(self, arg):
        """Quit Py314"""
        exit()








def startFactory():


    subPrompt = Prompt()
    subPrompt.prompt = f"({colored('factory', 'magenta')}) > "
    subPrompt.cmdloop()


