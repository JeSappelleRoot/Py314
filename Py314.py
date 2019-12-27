#!/usr/bin/env python3

import re
import os
import sys
import glob
import logging
from prettytable import PrettyTable
from cmd import Cmd
from termcolor import colored
from handlers import bind_agent
from generaters import factory
from core.logger import setup_logger


def displayBanner():
    """Banner definition"""

    print(colored(r"""
  _____         ____  __ _  _   
 |  __ \       |___ \/_ | || |  
 | |__) |   _    __) || | || |_ 
 |  ___/ | | |  |__ < | |__   _|
 | |   | |_| |  ___) || |  | |  
 |_|    \__, | |____/ |_|  |_|  
         __/ |                  
        |___/                   

    """, 'blue'))

    return


class Prompt(Cmd):
    """Create prompt commands, class herited by Cmd"""

    # Define empty temporary list and empty focus
    tempList, focus = [], ''

# < -------------------------- OVERRIDE -------------------------- >

    def emptyline(self):
        """Called when an empty line is entered in response to the prompt.

        If this method is not overridden, it repeats the last nonempty
        command entered.

        """

    def do_help(self, arg):
        """Display help about commands"""

        # Get all method of the object
        names = self.get_names()
        # Get all "real" commands, with do_ at the begining
        commands = [names.replace('do_', '') for names in names if names.startswith('do_')]
        
        # If help command have a argument (help <command>), get docstring of this command
        if arg:
            try:
                doc = getattr(self, 'do_' + arg).__doc__
                print(doc)
            # Except AttributeError, if given arg isn't a existing command
            except AttributeError:
                logger.failure(f"No command {arg}")

        # Elif no arg is submitted,  print all docstrings of each commands
        # With PrettyTable module, to have autosize array, with pretty cool delimiters
        elif not arg:
            table = PrettyTable()
            # Define and add headers of array
            headers = ['command', 'description']
            table.field_names = headers
            # Left align each headers in the array
            for header in headers:
                table.align[header] = 'l'

            for command in commands:
                commandDoc = getattr(self, f"do_{command}").__doc__
                table.add_row([command, commandDoc])

            print(table)

# < -------------------------- COMMANDS -------------------------- >

    def do_banner(self, arg):
        """Clear console and display banner"""
        os.system('clear')
        displayBanner()

    def do_clear(self, arg):
        """Clear terminal (shortcut : ctrl-l)"""
        os.system('clear')

    def do_exit(self, arg):
        """Quit Polymole"""
        return True

    def do_handler(self, arg):
        """Try to established a connection with a Py314 agent"""
        bind_agent.startModule()

    def do_reverse_agent(self, arg):
        """Try to established a connection with listening a Py314 agent"""

    def do_factory(self, arg):
        """Generate a Py314 agent"""
        factory.startFactory()


def checkConfig():

    # Get ~ directory
    homeFolder = os.environ['HOME']
    # Define Py314 folder
    py314Folder = f"{homeFolder}/.Py314"
    
    # If Py314 hidden directory doesn't exist, create it
    if not os.path.isdir(py314Folder):
        logger.info(f"[!] Folder {py314Folder} doesn't exist")
        logger.info(f'[!] It will be created ')
        os.makedirs(py314Folder)

    return

def checkLevel(args):
    """Function to check logging module level in argument"""


    # If command line arg = '-v', launch Py314 in debug mode
    if len(args) > 1 and args[1] == '-v':
        level = logging.DEBUG
    # Else, launch Py314 in regular mode (INFO logging level)
    else:
        level = logging.INFO

    return level



try:

    # Define a logger, with 'main' name
    level = checkLevel(sys.argv)
    logger = setup_logger('main', level)
    
    # Check config
    checkConfig()
    # Display awesome banner ;)
    displayBanner()

    # Define a prompt, with Cmd class
    Interpreter = Prompt()
    Interpreter.prompt = colored('Py314 > ', 'cyan')
    Interpreter.intro = 'Type help or ? to list commands.'
    # Launch the main Interpreter
    Interpreter.cmdloop()


except KeyboardInterrupt:
    exit()

# https://code-maven.com/interactive-shell-with-cmd-in-python
# https://wiki.python.org/moin/CmdModule