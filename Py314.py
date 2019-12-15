import re
import os
import sys
import glob
from cmd import Cmd
from termcolor import colored
from listeners import *



class Prompt(Cmd):


    tempList = []
    focus = ''


    def do_exit(self, arg):
        """Quit Polymole"""
        return True

    def do_clear(self, arg):
        """Clear terminal (shortcut : ctrl-l)"""
        os.system('clear')

    def do_banner(self, arg):
        """Clear console and display banner"""
        os.system('clear')
        displayBanner()


    def do_use(self, arg):
        """Use module/listener/generater"""
        # if 'use' with number
        # Remove '-' to match with negatives numbers 
        if str(arg).lstrip('-').isdigit():
            # If module index is not between 0 and tempList lengh - 1
            if not 0 <= int(arg) <= len(self.tempList) - 1:
                self.emptyline
            else:
                moduleName = str(self.tempList[int(arg)][1])
                self.focus = moduleName
                self.focusObject = self.import_focus(self.focus)

        # Else if 'use' with module name
        else:
            if arg not in dict(self.tempList).values():
                print('[!] Invalid module name')
            else:
                self.focus = arg
                self.focusObject = self.import_focus(self.focus)

        self.focusObject.startModule(moduleName)

    def do_help(self, arg):
        sep = '='
        headers = ['name', 'description']
        sepList = []
        for item in headers:
            sepList.append(sep * len(item))
        print('\t\t'.join(headers))
        print('\t\t'.join(sepList))

        if arg:
            doc = getattr(self, f"do_{arg}").__doc__
            if doc:
                print(f"{arg}\t\t{doc}")
            else:
                print(f"[!] No documentation for {arg} command")
                
        else:
            commands = self.get_names()
            for cmd in commands:
                if cmd.startswith('do_'):
                    doc = getattr(self, cmd).__doc__
                    if doc:
                        print(f"{cmd.replace('do_', '')} \t\t{doc}")

    def do_listen(self, arg):
        """Launch a listener for outgoing/incoming connecion"""

        return


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





displayBanner()

Interpreter = Prompt()
Interpreter.prompt = colored('Py314 > ', 'cyan')
Interpreter.intro = 'Type help or ? to list commands.'
Interpreter.cmdloop()



# https://code-maven.com/interactive-shell-with-cmd-in-python
# https://wiki.python.org/moin/CmdModule