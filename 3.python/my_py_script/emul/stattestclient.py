#!/usr/bin/env python
# -*- coding: EUC-KR -*-
# PAS client
import socket
import time


####
def connPAS(host='localhost', port=50007, debug=0):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.setblocking(0)
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
	
	start = time.time()
	data = ''
	while len(data)==0:
		time.sleep(0.2)
		time.sleep(0.2)
		try:
			one = s.recv(1024)
			#if not one: break
			#if len(one) < 1: break
			data += one
		except:
			continue
		
	print data
	end = time.time()
	print "LENGTH=%d" % (len(data))
	print "lap time = %d" % (end - start)




REQMSG = \
"""
GET %s HTTP/1.1
Host: %s
User-Agent: Mozilla/1.22 (compatible; KUN/1.0; KTF5000; CellPhone)
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

	HOST = 'ktfkunproxy.ktf.com'    # The remote host
	HOST = '210.123.92.140'
	HOST = 'localhost'    # The remote host

	PORT = 50007              # The same port as used by the server

	MDN = "820161002000"  ## Virtual MDN
	MDN = "8201690102000"
	MDN = "8201690102000"
	MDN = "820162010022"
	URL = "http://www.magicn.com�ѵ�"
	URL = "http://www.magicn.com/"
	URL = "http://www.magicn.com/oO???oc?UA????????UA???U��?????e��??O��???|��??|"


	if len(sys.argv)==2:
		if sys.argv[1]=='good':
			MDN = "820162010022"
			URL = "http://www.magicn.com/"
		elif sys.argv[1]=='santa':
			MDN = "8201690102000"
			URL = "http://www.magicn.com/"
		elif sys.argv[1]=='url':
			MDN = "820162010022"
			URL = "http://www.magicn.com/oO???oc?UA????????UA???U��?????e��??O��???|��??|"
		elif sys.argv[1]=='help' or sys.argv[1]=='?':
			print "usage: port mdn url"
			print "mdn = 820161002000, 8201690102000"
			sys.exit()

			
	if len(sys.argv) >= 4:
		PORT = int(sys.argv[1])
		MDN = sys.argv[2]
		URL = sys.argv[3]


	scheme, host, path, params, query, fragment =\
		urlparse.urlparse(URL)

	print "## Paras: ", HOST, URL, host, MDN
	msg = REQMSG % (URL, host, MDN, MDN)	

	sock = connPAS(host=HOST, port=PORT)
	sendtoPAS(sock, msg)
	sock.close()

	
	
