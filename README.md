# Py314

- [Py314](#py314)
  - [Why Py314 ?](#why-py314)
  - [Why this name ?](#why-this-name)
- [Requirements](#requirements)
- [About modules](#about-modules)
  - [Factory](#factory)
    - [Options](#options)

Py314 is a RAT (Remote Access Tool) written in Python 3, inspired by the great Metasploit-Framework pentest tool


`####################################################`  
`#` **This tool is designed for educational purposes only** `#`  
`####################################################`

>Do not abuse this material. Be responsible.  
>All the content of Py314 script is for educational and research purposes only.  
>Do not attempt to violate the law with anything contained here.  
>The authors of this material, or anyone else affiliated in any way, are not going >to accept responsibility for your actions.  


## Why Py314 ?

Hacking is the best way to learn how to secure systems and networks.  
Know how an attack is conducted teach you how to defend against threats.

## Why this name ? 

C'mon, it's a pun with `π` mathematic concept...


# Requirements

Py314 use some externals modules :  
- **PySocks** to use a proxy with socket module
- **cryptography** to perform symmetric encryption
- **netaddr** to check valid IP address
- **pkgconfig** to get includes for compilation process
- **prettytable** to display cool tables
- **pyminifier** to obfuscate python code with compress
- **termcolor** to add some colors in terminal

```
PySocks == 1.6.8
cryptography == 2.6.1
netaddr == 0.7.19
pkgconfig == 1.5.1
prettytable == 0.7.2
pyminifier == 2.1
termcolor == 1.1.0
```

Simply run `pip install -r requirements.txt`

# About modules

`handler` and `factory` modules can be used and are built with Cmd class, to provide a dynamic interpreter and syntax completion.

## Factory

Factory module can generate Py314 agent : 
- **bind_agent**, where Py314 try to connect directly to a existing and launched remote agent
- **reverse_listener**, where Py314 listen on a given IP and port, to get a connection from a remote launched agent

This behaviour is modelled on Metasploit-Framework, with bind_tcp and reverse_tcp payloads.


### Options

Many options can be used with factory module : 
- **host**, to define a IP address
- **port**, to define a bind port
- **password**, to define a password, used for symmetric encryption and decryption
- **type**, to define the agent type
- **outfile**, to define the output agent file (default is ~/.Py314 folder)
- **compress**, to enable compression (True or False)
- **iterations**, to set the number of successives compressions (1 mininum)
- **compile**, to enable final agent compilation (ELF 64 bit binary)

>In case of **bind_agent** agent type :  
**host** option will be an IP address assigned in the remote system  
**port** option will be a port on the remote system  
*Py314 will bind given couple host:port to try to establish a connection with remote agent*

>In case of **reverse_listener** agent type :   
**host** option will be a existing IP address on the local machine  
**port** option will be a available port on the local machine  
*The remote agent will bind the local machine with given couple host:port to try to establish a connection with Py314*

![types](https://user-images.githubusercontent.com/52102633/71740851-f573e380-2e22-11ea-8e28-3fafc3c6e4d8.png)
