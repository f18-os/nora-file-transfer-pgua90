#! /usr/bin/env python3

import sys, os, socket, params, time
from threading import Thread
from framedSock import FramedStreamSock

IP = 0

print("Choose Proxy or Server: 1.) Proxy or 2.) Server: ")
option = input()
if option == 1:
    IP = 50001
if option == 2:
    IP = 50000

switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', IP),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )

progname = "echoserver"
paramMap = params.parseParams(switchesVarDefaults)

debug, listenPort = paramMap['debug'], paramMap['listenPort']

if paramMap['usage']:
    params.usage()

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # listener socket
bindAddr = ("127.0.0.1", listenPort)
lsock.bind(bindAddr)
lsock.listen(5)
print("listening on:", bindAddr)

class ServerThread(Thread):
    requestCount = 0            # one instance / class
    def __init__(self, sock, debug):
        Thread.__init__(self, daemon=True)
        self.fsock, self.debug = FramedStreamSock(sock, debug), debug
        self.start()
    def run(self):
        while True:
            msg = self.fsock.receivemsg()
            if not msg:
                if self.debug: print(self.fsock, "server thread done")
                return
            requestNum = ServerThread.requestCount
            time.sleep(0.001)
            ServerThread.requestCount = requestNum + 1
            msg = ("%s! (%d)" % (msg, requestNum)).encode()
            self.fsock.sendmsg(msg)

    cnt = 0
    while True:
        sock, addr = lsock.accept()
        ServerThread(sock, debug)
        print('Connected by', addr)

        tst = open('text' + str(cnt) + '.txt', w)
        cnt = cnt + 1
        while True:
            data = fs.receivemsg()
            if data:
                tst.write(data.decode())

            else:
                sock.close()
                tst.close()
                break
