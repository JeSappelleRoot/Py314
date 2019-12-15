import re
import os
import sys
import glob
from cmd import Cmd
from termcolor import colored
from listeners import (Py314Bind)


class Prompt(Cmd):


    tempList = []
    focus = ''

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

    def do_help(self, arg):
        sep = '='
        headers = ['name', 'description']
        sepList = []
        for item in headers:
            sepList.append(sep * len(item))
        print('\t\t'.join(headers))
        print('\t\t'.join(sepList))

        commands = self.get_names()
        for cmd in commands:
            if cmd.startswith('do_'):
                doc = getattr(self, cmd).__doc__
                if doc:
                    print(f"{cmd.replace('do_', '')}\t\t{doc}")


    def do_listener(self, arg):
        """Try to establish a connection with a Py314 agent"""

    def do_generate(self, arg):
        """Generate a Py314 agent"""



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


try:


    displayBanner()

    Interpreter = Prompt()
    Interpreter.prompt = colored('Py314 > ', 'cyan')
    Interpreter.intro = 'Type help or ? to list commands.'
    Interpreter.cmdloop()

except KeyboardInterrupt:
    exit()

# https://code-maven.com/interactive-shell-with-cmd-in-python
# https://wiki.python.org/moin/CmdModule