from cmd import Cmd


class Prompt(Cmd):
    """Simple Py314 agent factory"""

    availableTypes = ['bind_agent', 'reverse_listener']

    optionsDict = {
        'type': ''
        'rhost': '',
        'rport': 1234,
        'password': 'Py314!',
        'proxy': '', 
        'verbose': False
    }











def startFactory():


    subPrompt = Prompt()
    subPrompt.prompt = f"({colored('bind_agent', 'yellow')}) > "
    subPrompt.cmdloop()


