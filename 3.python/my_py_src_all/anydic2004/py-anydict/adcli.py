#!/usr/bin/env python
# -*- coding: EUC-KR -*-
import sys
import socket
import time


###
PROTO_VER = 'V001'
def test_dict():
	import util
	while 1:
		a = util.getinput("Enter a word:")
		if a=='.': break

		req_dic_8700(8700, 3, a)
		


#
# send a request(query) to anydict python server, and receive the result
def req_dic(argv, func, word):
	global orgword
	size_res = 0
	if len(argv) >= 2:
		port = int(argv[1])
	else:
		port = 8900

	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	try:
		#sock.connect ( (socket.gethostbyname('localhost'), port) )
		sock.connect ( ("127.0.0.1", port) )
		time.sleep(0.01)

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


def req_dic_8700(port, func, word):
	size_res = 0

	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	try:
		#sock.connect ( (socket.gethostbyname('localhost'), port) )
		sock.connect ( ("127.0.0.1", port) )

	except:
		print "connect fail"

		return 0

	body = "%s %2d %s" % (PROTO_VER, func, word) 
	msg = "%-4d%s" % (len(body), body)
	sock.send (msg)
	print msg
	
	buf = sock.recv (128)
	print buf
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
		print buf
		size_res += len(buf)
		sys.stdout.write(buf)
 
	sock.close()

	return size_res



if __name__=='__main__':
	test_dict()
