#!/usr/bin/env python

import socket
import sys

MAX = 65535
PORT = 1060

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

if sys.argv[1:] == ['server']:
    s.bind(('127.0.0.1', PORT))
    print 'Listening at', s.getsockname()
    while True:
        data, address = s.recvfrom(MAX)
        print 'The client at', address, 'says', repr(data)
        s.sendto('Your data was %d bytes' % len(data), address)

elif sys.argv[1:] == ['client']:
    print 'Address before sending: ', s.getsockname()
    s.sendto('This is my message', ('127.0.0.1', PORT))
    print 'Address after sending', s.getsockname()
    data, address = s.recvfrom(MAX) # over promisuous - see text!
    print 'The server', address, 'says', repr(data)


