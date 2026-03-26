#!/usr/bin/env python

"""Logs HTTP requests to the console"""

import socket, time, collections


HOST = '127.0.0.1'
PORT = 31337


def recv_timeout(s, timeout=.2):
    #make socket non blocking
    the_socket = s
    the_socket.setblocking(0)
     
    #total data partwise in an array
    total_data = []
    data = ''
     
    #beginning time
    begin = time.time()
    while 1:
        #if you got some data, then break after timeout
        if total_data and time.time()-begin > timeout:
            break
         
        #if you got no data at all, wait a little longer, twice the timeout
        elif time.time()-begin > timeout*2:
            break
         
        #recv something
        try:
            data = the_socket.recv(8192)
            if data:
                total_data.append(data.decode("utf-8"))
                #change the beginning time for measurement
                begin = time.time()
            else:
                #sleep for sometime to indicate a gap
                time.sleep(0.1)
        except:
            pass
     
    #join all parts to make final string
    ret = ''.join(total_data)
    print(ret)
    return ret


serversock = socket.socket()
serversock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serversock.bind((HOST, PORT))
serversock.listen(10)
while True:
    csock, info = serversock.accept()
    recv_timeout(csock)
    csock.close()
