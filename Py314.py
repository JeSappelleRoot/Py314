import re
import os
import sys
import glob
from cmd import Cmd
from termcolor import colored
from handlers import bind_agent
from generaters import factory

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

    def emptyline(self):
        """Called when an empty line is entered in response to the prompt.

        If this method is not overridden, it repeats the last nonempty
        command entered.

        """



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


    homeFolder = os.environ['HOME']
    py314Folder = f"{homeFolder}/.Py314"
    
    if not os.path.isdir(py314Folder):
        print(f"[!] Folder {py314Folder} doesn't exist")
        print(f'[!] It will be created ')
        os.makedirs(py314Folder)

    return



try:

    checkConfig()
    displayBanner()

    Interpreter = Prompt()
    Interpreter.prompt = colored('Py314 > ', 'cyan')
    Interpreter.intro = 'Type help or ? to list commands.'
    Interpreter.cmdloop()






except KeyboardInterrupt:
    exit()

# https://code-maven.com/interactive-shell-with-cmd-in-python
# https://wiki.python.org/moin/CmdModule