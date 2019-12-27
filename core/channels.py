import socket
import socks
import logging

def parseProxy(proxy):
    """Function to parse proxy with following syntax <type>://<address>:<port>"""

    try:

        logger = logging.getLogger('main')

        proxyType = proxy.split('://')[0]
        proxyAddress = proxy.split('://')[1]
        proxyIP = proxyAddress.split(':')[0]
        proxyPort = proxyAddress.split(':')[1]
        validProxy = True

        availableProxies = ['SOCKS4', 'SOCKS5', 'HTTP']
        if proxyType.upper() not in availableProxies:
            logger.failure('Please use a valid proxy type : socks4, socks5 or http')
            validProxy = False

        if proxyType.upper() == 'SOCKS4':
            proxyNum = 1
        elif proxyType.upper() == 'SOCKS5':
            proxyNum = 2
        elif proxyType.upper() == 'HTTP':
            proxyNum = 3
        else:
            proxyNum = 'UNVALID'

        logger.debug(f"Proxy type : {proxyType} (type = {proxyNum})")
        logger.debug(f"Proxy IP address : {proxyIP}")
        logger.debug(f"Proxy port : {proxyPort}")

        proxyParam = [proxyNum, proxyIP, int(proxyPort)]



        return validProxy, proxyParam

    except IndexError as error:
        logger.failure('Please specify a proxy with <type>://<ip>:<port>')
        proxyParam = False
        validProxy = False

        return validProxy, proxyParam




def bind_tcp(ip, port, proxy):
    """Create a TCP socket with binding remote agent"""


    logger = logging.getLogger('main')


    logger.debug(f"Remote agent IP address : {ip}")
    logger.debug(f"Remote agent port : {port}")

    channel = socks.socksocket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    channel.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    if proxy != '':
        logger.debug('Proxy option detected, try to parse proxy')
        valid, proxyOpt = parseProxy(proxy)

        if valid is True and len(proxyOpt) == 3:

            logger.debug('Proxy is valid, will be use for connection')
            channel.set_proxy(proxy_type=proxyOpt[0], addr=proxyOpt[1], port=proxyOpt[2])
        else:
            logger.debug('Proxy is invalid, connection aborted')
            return False


    try:

        channel.connect((ip, port))
        logger.success(f"Channel successfully established with remote agent")

    
    except socks.ProxyConnectionError as error:
        logger.failure(f"Can't established connection with specified proxy")
        channel = False

    except socks.GeneralProxyError as error:
        logger.failure(f"Can't established connection to {ip}:{port}")
        logger.debug('General proxy error')
        channel = False


    except ConnectionError as error:
        logger.failure(f"Can't established connection to {ip}:{port}")
        logger.debug(error)
        channel = False



    return channel
    



