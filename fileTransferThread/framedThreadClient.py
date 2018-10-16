#! /usr/bin/env python3

# Echo client program
import socket, sys, re
import params
from framedSock import FramedStreamSock
from threading import Thread
import time


IP = ""
print("Choose Proxy or Server: 1.) Proxy or 2.) Server: ")
option = input()
if option == 1:
  IP = "localhost:50001"
elif option == 2:
  IP = "localhost:50000"

switchesVarDefaults = (
    (('-s', '--server'), 'server', "localhost:50001"),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )

progname = "framedClient"
paramMap = params.parseParams(switchesVarDefaults)

server, usage, debug  = paramMap["server"], paramMap["usage"], paramMap["debug"]

if usage:
    params.usage()

try:
    serverHost, serverPort = re.split(":", server)
    serverPort = int(serverPort)
except:
    print("Can't parse server:port from '%s'" % server)
    sys.exit(1)

class ClientThread(Thread):
    def __init__(self, serverHost, serverPort, debug):
        Thread.__init__(self, daemon=False)
        self.serverHost, self.serverPort, self.debug = serverHost, serverPort, debug
        self.start()
    def run(self):
       s = None
       for res in socket.getaddrinfo(serverHost, serverPort, socket.AF_UNSPEC, socket.SOCK_STREAM):
           af, socktype, proto, canonname, sa = res
           try:
               print("creating sock: af=%d, type=%d, proto=%d" % (af, socktype, proto))
               s = socket.socket(af, socktype, proto)
           except socket.error as msg:
               print(" error: %s" % msg)
               s = None
               continue
           try:
               print(" attempting to connect to %s" % repr(sa))
               s.connect(sa)
           except socket.error as msg:
               print(" error: %s" % msg)
               s.close()
               s = None
               continue
           break

       if s is None:
           print('could not open socket')
           sys.exit(1)

       fs = FramedStreamSock(s, debug=debug)

       txtFile = input("Enter filename: ")

       with open(txtFile, "rb") as txt:
        try:
          content = txt.read(100)
          print('file opened')
          while content:
            fs.sendmsg(self, b':' + content)
            data = txt.read(100)
        except(FileNotFoundError) as fnferror:
          print("File not found...")
          sys.exit(0)

        except BrokenPipeError as BPError:
          print("Connection lost... ")
          sys.exit(0)

        if not content:
          print("file is empty.")
          sys.exit(0)
        else:
          print("recieved: ", fs.receivemsg())

ClientThread(serverHost, serverPort, debug)
