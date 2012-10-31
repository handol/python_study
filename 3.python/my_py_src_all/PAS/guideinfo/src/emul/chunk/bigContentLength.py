#! /usr/bin/env python
#
# This is the simplest possible server, servicing a single request only.

import sys
import time
from socket import *

# The standard echo port isn't very useful, it requires root permissions!
# ECHO_PORT = 7
ECHO_PORT = 8888
BUFSIZE = 1024

def sendChunkBody(conn, respmsg, msglen=0):
	if msglen==0:
		msglen = len(respmsg)
	conn.send("%X\r\n" % msglen)

	conn.send("%s\r\n" % respmsg)
	pass

def main():
	conn, (remotehost, remoteport) = s.accept()
	print 'connected by', remotehost, remoteport

	data = conn.recv(1024*2)

	print "client data : %s" % (data)

	contentLeng = 32*1024*1024
	data = "HTTP/1.1 200 OK\r\nDate: Tue, 10 Oct 2006 13:25:22 GMT\r\nServer: Apache/2.2.0 (Unix) DAV/2 mod_ssl/2.2.0 OpenSSL/0.9.8a\r\nCache-Control: no-cache\r\nPragma: no-cache\r\nExpires: -1\r\nContent-length: %d\r\nContent-Type: text/html\r\n\r\n" % (contentLeng)
	conn.send(data)
	print "send data : %s" % (data)

	sendChunkBody(conn, "1234567890")
	sendChunkBody(conn, "1234567890", 33*1024*1024)


	conn.close()
	print "child end"

if len(sys.argv) > 1:
	port = int(eval(sys.argv[1]))
else:
	port = ECHO_PORT

print "start server at port %d" % port

s = socket(AF_INET, SOCK_STREAM)
s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
s.bind(('', port))
s.listen(10)
while 1:
	main()

