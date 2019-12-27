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


    tempList = []
    focus = ''

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

    def do_bind_agent(self, arg):
        """Try to established a connection with binding a Py314 agent"""
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