import sys
import glob
import socket
import threading
from os import system
from netaddr import ip
from cmd import Cmd
from termcolor import colored
from prettytable import PrettyTable


class Handler():
    """Class to define a handler"""
    def __init__(self):
        self.type = 'bind_tcp'
        self.rhost = ''
        self.rport = 1234




class HandlerPrompt(Cmd):
    """Prompt use to define handler and options"""

    def do_exit(self, arg):
        """Quit Py314"""
        exit()

    def do_bg(self, arg):
        """Return to Py314 main prompt"""
        return True

    def do_settings(self, arg):
        """Show listener settings"""

    def do_show(self, arg):




def startListeners():

    subPrompt = HandlerPrompt()
    subPrompt.prompt = colored('(handler) > ', 'yellow')
    subPrompt.cmdloop()