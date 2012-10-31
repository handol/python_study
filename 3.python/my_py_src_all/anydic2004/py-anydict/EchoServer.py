#!/usr/bin/python
# -*- coding: EUC-KR -*-
# 2008/3/10

import SocketServer

class MyHandler(SocketServer.BaseRequestHandler):
	mymesg = "Orginal val"

	@staticmethod
	def setMyMesg(msg):
		MyHandler.mymesg = msg

	def handle(self):
		while 1:
			msg = self.request.recv(1000)
			print msg
			print MyHandler.mymesg
			break
		


# #
def start_server(port):
	myServer = SocketServer.TCPServer(('',port), MyHandler)
	myServer.allow_reuse_address = True
	myServer.serve_forever( )

if __name__=="__main__":
	import sys

	MyHandler.mymesg = "Jennifer"
	MyHandler.setMyMesg("Handol")

	if len(sys.argv) > 1:
		start_server(int(sys.argv[1]))
