# Py314

- [Py314](#py314)
  - [Why Py314 ?](#why-py314)
  - [Why this name ?](#why-this-name)
- [Requirements](#requirements)
- [About modules](#about-modules)
  - [Factory](#factory)
    - [Options](#options)
    - [About agent compression](#about-agent-compression)
    - [About agent compilation](#about-agent-compilation)
    - [Demo](#demo)
  - [Handler](#handler)
    - [What can I do with Py314 ?](#what-can-i-do-with-py314)
- [About encryption](#about-encryption)

Py314 is a RAT (Remote Access Tool) written in Python 3, inspired by the great Metasploit-Framework pentest tool.  
All traffic between Py314 and agents are fully symmetric encrypted with Fernet Python3 module


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
- **port**, to define a port to bind or to listen
- **password**, to define a password, used for agent authentification, symmetric encryption and decryption
- **type**, to define the agent type
- **outfile**, to define the output agent file (default is ~/.Py314 folder)
- **compress**, to enable compression (True or False)
- **iterations**, to set the number of successives compressions (1 mininum)
- **compile**, to enable final agent compilation (Unix ELF binary)

>In case of **bind_agent** agent type :  
**host** option will be an IP address assigned in the remote system  
**port** option will be a port on the remote system  
*Py314 will bind given couple host:port to try to establish a connection with remote agent*

>In case of **reverse_listener** agent type :   
**host** option will be a existing IP address on the local machine  
**port** option will be a available port on the local machine  
*The remote agent will bind the local machine with given couple host:port to try to establish a connection with Py314*

![types](https://user-images.githubusercontent.com/52102633/71740851-f573e380-2e22-11ea-8e28-3fafc3c6e4d8.png)


### About agent compression

Compression is performed with `pyinifier` module :  
- `bzip2` method
- `gzip` method
- `lzma` method

Imagine a simple script with the following content : 
```py
print('hello world')
```

With `gzip` compression method, the content will be : 
```py
import zlib, base64
exec(zlib.decompress(base64.b64decode('eJwrKMrMK9FQz0jNyclXKM8vyklR1+QCAFYWBzM=')))
```

The compression is an esay way to perform script obfuscation, **but reverse compression is also easy**.  
That's why Py314 can perform several successive compressions, with different methods between each loops

### About agent compilation

Compilation follow the following recipe : 
- convert Python 3 agent code in Cython language (improve performances) with Python interpreter embed
- compile Cython C source file with gcc to get an Unix ELF binary type (**platform x64/x86 depend of your system**)

>**Cython command** :  
`cython -3 -v --embed agent.py -o agent.c`  
`-3` is used to specify Python 3 (Python2 by default)  
`--embed` is used to embed the Python interpreter

>**GCC command** :  
`gcc agent.c -o bind_agent $(pkg-config --libs --cflags python3)`  
`$(pkg-config --libs --cflags python3)` is used to automatically generate includes paths : `-I/usr/include/python3.7m -I/usr/include/x86_64-linux-gnu/python3.7m -lpython3.7m`


### Demo

![factory](https://user-images.githubusercontent.com/52102633/71747085-57891480-2e34-11ea-922e-1b090635a670.gif)

## Handler

Handler is the module used to try to establish a connection with a remote Py314 agent. This module needs some options : 
- **host**, could be a remote IP or a local address to listen
- **password**, used for agent authentification, symmetric encryption and decryption
- **port**, to define a port to bind or to listen
- **proxy**, to specify a proxy to use, only with **bind_agent** type (support HTTP, SOCKS4 and SOCKS5 proxy)
- **type**, to specify the type of remote agent

>In case of **bind_agent** agent type :  
**host** option will be an IP address used by remote address
**port** option will be a port used by remote agent
*Py314 will bind given couple host:port to try to establish a connection with remote agent*

>In case of **reverse_listener** agent type :   
**host** option will be a existing IP address on the local machine  
**port** option will be a available port on the local machine  
*The remote agent will bind the local machine with given couple host:port to try to establish a connection with Py314*

![handler](https://user-images.githubusercontent.com/52102633/71784293-b75bf880-2fb7-11ea-9fe5-8cec4dbe4a40.gif)  

*Assume following configuration :*
- LAN 10.0.10.0/24
- Py314 ip address : 10.0.10.1/24
- Agent ip address : 10.0.10.166
- Agent type is reverse_listener
- Py314 listen on 1234 port
- Password is `demo_Py314`

### What can I do with Py314 ? 

Py314 is voluntarily weak in options, you can only : 
- check is remote agent is alive (give an answer)
- download remote file
- upload local file
- use basic shell commands

# About encryption

Traffic between Py314 and remote agent is fully encrypted with Fernet Python3 module.  
The password set in factory or in handler modules is used to generate a Fernet key, which will be use to perform symmetric encryption and decryption.  
Download and upload commands encrypt files before downloading or uploading  

