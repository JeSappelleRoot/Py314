



# Py314

- [Py314](#py314)
- [Requirements](#requirements)
- [About modules](#about-modules)
  - [Factory](#factory)

Py314 is a RAT (Remote Access Tool) written in Python 3, inspired by the great Metasploit-Framework pentest tool


`####################################################`  
`#` **This tool is designed for educational purposes only** `#`  
`####################################################`

>Do not abuse this material. Be responsible.  
>All the content of Py314 script is for educational and research purposes only.  
>Do not attempt to violate the law with anything contained here.  
>The authors of this material, or anyone else affiliated in any way, are not going >to accept responsibility for your actions.  



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

![agent_type](https://user-images.githubusercontent.com/52102633/71627879-c52a0c00-2bba-11ea-8e72-29e7af42b393.jpg)

