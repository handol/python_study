#!/usr/bin/env python
# PAS client
import socket
import time


####
def connPAS(host='localhost', port=50007, debug=0):
	print "connecting", host, port
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.setblocking(1)
	if debug: print "after socket(): fd=%d, addr=%s, %d" % (s.fileno(), s.getsockname()[0], s.getsockname()[1])

	#s.bind(("192.168.2.6", port))
	#s.bind((host, port))
	if debug: print "after bind(): fd=%d, addr=%s, %d" % (s.fileno(), s.getsockname()[0], s.getsockname()[1])

	s.connect((host, port))
	if debug: print "after connect(): fd=%d, addr=%s, %d" % (s.fileno(), s.getsockname()[0], s.getsockname()[1])

	if debug: print "peer name: %s %d" % (s.getpeername()[0], s.getpeername()[1])
	return s


####
def sendtoPAS(s, msg):
	s.send(msg)

	print "%s" % (msg)

#time.sleep(1)
	try:
		out = open("kunemul.result.txt", "w")
	except:
		out = None

	
	s.settimeout(3.0)
	start = time.time()
	data = ''
	total = 0
	while 1:		
		try:
			one = s.recv(1024)
			if len(one)>0:
				total += len(one)
				if out:
					out.write(one)
				if len(data) < 1024:
					print one
					data += one
				else:
					print one
					print "# %d %d" % (len(one), total)
			elif len(one)==0:
				print "conn closed"
				break
		except:
			break
		
	end = time.time()
	print "LENGTH=%d" % (len(data))
	print "lap time = %d" % (end - start)
	if out:
		out.close()

#User-Agent: Mozilla/1.22 (compatible; KUN/1.0; KTF5000; CellPhone)

REQMSG = \
"""GET %s HTTP/1.1
Host: %s
User-Agent: Mozilla/1.22 (compatible; KUN/2.0; KTF5000; CellPhone)
COUNTER:1
HTTP_PHONE_NUMBER: 82%s
HTTP_PHONE_SYSTEM_PARAMETER: BASE_ID:326, NID:36, SID:2189, BASE_LAT:0, BASE_LONG:0
HTTP_DEVICE_INFO:LX:176,LY:220,CL:8
HTTP_DRIVER_INFO:IMG:MSIS|NBMP,SND:MA3|SMAF|MA5
HTTP_PLATFORM_INFO:PNAME:BREW,PVER:V1.2,PID:1002
HTTP_CHANNEL_INFO:CH:A
HTTP_MNC_INFO:04
HTTP_MDN_INFO:%s
Cookie: SITESERVER=ID=958c5b3e4ce473494a6db82d70887570;
Proxy-Connection: Keep-Alive
Accept: */*
Accept-Language: en
Accept-Encoding: deflate\r
\r
"""
#Accept-Encoding: deflate


if __name__ == "__main__":
	import sys
	import urlparse

	HOST = 'localhost'    # The remote host


			
	if len(sys.argv) == 3:
		#HOST = sys.argv[1]
		#PORT = int(sys.argv[2])
		MDN = sys.argv[1]
		URL = sys.argv[2]
	else:
		print "MDN URL"
		sys.exit()


	scheme, host, path, params, query, fragment =\
		urlparse.urlparse(URL)

	
	urlpath = path + params + query + fragment
	if urlpath == "":
		urlpath = "/"

	print "urlpath = %s" % urlpath
	msg = REQMSG % (urlpath, host, MDN, MDN)	


	flds = host.split(':')
	HOST = flds[0]
	if len(flds) > 1:
		PORT = int(flds[1])
	else:
		PORT = 80

	sock = connPAS(host=HOST, port=PORT, debug=1)
	sendtoPAS(sock, msg)
	sock.close()

	print "This is result of the Connection to %s:%d" % (HOST, PORT)
	
	
