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
	try:
		conn.send("%X\r\n" % msglen)
	#print "%X\r\n" % msglen

		conn.send("%s\r\n" % respmsg)
	except:
		print "fail to send"
	pass

def main():
	conn, (remotehost, remoteport) = s.accept()
	print 'connected by', remotehost, remoteport

	data = conn.recv(1024*2)

	#print "client data : %s" % (data)
	print "client data : %d" % len(data)

	data = "HTTP/1.1 200 OK\r\nDate: Tue, 10 Oct 2006 13:25:22 GMT\r\nServer: Apache/2.2.0 (Unix) DAV/2 mod_ssl/2.2.0 OpenSSL/0.9.8a\r\nCache-Control: no-cache\r\nPragma: no-cache\r\nExpires: -1\r\nTransfer-encoding: chunked\r\nContent-Type: text/html\r\n\r\n"
	try:
		conn.send(data)
		print "send head : %d" % (len(data))
	except:
		print "fail to send HEADER"

	start = time.time()
	loop = 1
	for i in range(1024):
		#time.sleep(0.001)
		# 1Kb
		try:
			sendChunkBody(conn, chr(ord('A')+loop-1)*(i+1)*2)
		except:
			print "fail to send loop %d" % i
			break

		#print "## Loop %d" % (loop)
		loop = (loop+1) % 25
	sendChunkBody(conn, "")


	conn.close()
	print "session finish"
	end = time.time()

	print "lap time = %d" % (end - start)

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

