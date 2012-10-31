#! /usr/bin/env python

import sys
import time
from socket import *

# The standard echo port isn't very useful, it requires root permissions!
# ECHO_PORT = 7
ECHO_PORT = 11111
BUFSIZE = 1024

def main():
	conn, (remotehost, remoteport) = s.accept()
	print 'connected by', remotehost, remoteport

	data = conn.recv(1024)

	#print "client data : %s" % (data)
	print "recv %d bytes" % (len(data))

	conLength = 500*1024
	data = "HTTP/1.1 200 OK\r\nDate: Tue, 10 Oct 2006 13:25:22 GMT\r\nServer: Apache/2.2.0 (Unix) DAV/2 mod_ssl/2.2.0 OpenSSL/0.9.8a\r\nCache-Control: no-cache\r\nPragma: no-cache\r\nExpires: -1\r\nContent-length: %d\r\nContent-Type: text/html\r\n\r\n" % conLength
	time.sleep(0.1)
	conn.send(data)
	#print "send data : %s" % (data)
	time.sleep(0.01)

	data = "A" * (conLength/2)
	conn.send(data)
	print "send %d bytes" % (len(data))

	time.sleep(0.1)
	conn.close()
	print "Close connection"

if len(sys.argv) > 1:
	port = int(eval(sys.argv[1]))
else:
	port = ECHO_PORT

s = socket(AF_INET, SOCK_STREAM)
s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
s.bind(('', port))
s.listen(1)
while 1:
	try:
		main()
	except:
		print "maybe, conn close by PAS"
		pass

