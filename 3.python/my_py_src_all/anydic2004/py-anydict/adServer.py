#!/usr/bin/env python

import sys
import os
import SocketServer

from daemon import daemonize
from adLoader import anydict


class MyHandler(SocketServer.BaseRequestHandler):
	def handle(self):
		while 1:
			lenpart = self.request.recv(4)
			if not lenpart: break

			#print "LEN:", lenpart
			msglen = int(lenpart)

			msg = self.request.recv(msglen)
			if not msg: break
			if len(msg) != msglen:
				print "read msg incompletely"
				break

			#print "MSG:", msg
			func = 0
			if len(msg) >= 8 and msg[0]=='V':	
				func = int(msg[4:8])
				msg = msg[8:]

			print func, msg
			res = search(func, msg)
			self.request.send(res)
			break


def search(func, msg):
	res = ''
	try:
		res = AD.search(func, msg)
	except:
		print "ERROR in searching: %d %s" % (func, msg)
		sys.stdout.flush()
	return res


def main(portnum):
	myServer = SocketServer.TCPServer(('',port), MyHandler)
	myServer.allow_reuse_address = True
	myServer.serve_forever( )


if __name__=='__main__':
	if len(sys.argv) >= 2:
		port = int(sys.argv[1])
	else:
		port = 8900

	ADDIR = os.getenv("ANYDICT_HOME")

	AD = anydict(
		ADDIR + "/data/wn17.html",
		ADDIR + "/data/webster/", 
		ADDIR + "/data/engdic/", 
		ADDIR + "/data/word.dict",
		ADDIR + "/data/hometopia.dict"
	)

	if port==8910:
		AD.load('a', 'a')
	else:
		AD.load('a', 'z')

	AD.info()
	#AD.prn_anydictt()
	#AD.prn_edict()

	#AD.testit()

	#daemonize()
	sys.stdout.flush()

	myServer = SocketServer.TCPServer(('',port), MyHandler)
	myServer.allow_reuse_address = True
	myServer.serve_forever( )

