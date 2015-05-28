__author__ = 'Phillip'

import socket,subprocess,sys
from datetime import datetime

def Socket():
    remoteServer = raw_input('Enter a remote host to scan:')
    remoteServerIP = socket.gethostbyname(remoteServer)
    print remoteServerIP

    try:
        for port in range(1,2):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex((remoteServerIP,port))
            print result
            print "-"*60
    except Exception:
        print Exception.message


Socket()