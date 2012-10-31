#!/usr/bin/python
# -*- coding: EUC-KR -*-
# 2008/3/21

import socket
from AdUtil import *

PROTO_VER = 'V001'

#
# send a request(query) to anydict python server, and receive the result
def req_dic(port, func, word):
	size_res = 0

	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	try:
		#sock.connect ( (socket.gethostbyname('localhost'), port) )
		sock.connect ( ("127.0.0.1", port) )

	except:
		handle_fail()
		#raise
		return size_res

	body = "%s %2d %s" % (PROTO_VER, func, word) 
	msg = "%-4d%s" % (len(body), body)
	sock.send (msg)

	
	buf = sock.recv (128)
	if len(buf) > 10 and buf[:3]=="ORG":
		pos = buf.find('\n',3)
		if pos != -1:
			orgword = buf[4:pos]
			#print "ORG: %s" % orgword
			buf = buf[pos:]

	sys.stdout.write(buf)

	while 1:
		buf = sock.recv (1024*2)
		if buf == '': break
		#print buf
		size_res += len(buf)
		sys.stdout.write(buf)
 
	sock.close()

	return size_res


def handle_fail():
	print "<br/>애니딕 서버가 기동 중입니다. <br/>\n 잠시만 기다려 주세요. <br/>"  



def testit(port):
	fname = "test.res"
	try:
		out = open(fname, "w")
		print """!! Output ==> "%s" """ % (fname)
	except:
		pass

	
	while 1:
		a = getinput("Enter a word:")
		if a=='.': break

		org_stdout = sys.stdout
		sys.stdout = out
	
		req_dic(port, 3, a)
		out.flush()
		sys.stdout = org_stdout
	
	out.close()

if __name__=="__main__":
	import sys

	if len(sys.argv) >= 2:
		port = int(sys.argv[1])
	else:
		port = 8900

	testit(port)
