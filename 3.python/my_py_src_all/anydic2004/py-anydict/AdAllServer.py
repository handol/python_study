#!/usr/bin/env python
# -*- coding: EUC-KR -*-
# 2008/3/26

import sys
import SocketServer
import adLoader
import AdSearch
import cStringIO


class MyHandler(SocketServer.BaseRequestHandler):
	EngDictSearcher = None
	ExlistDictSearcher = None

	@staticmethod
	def setEngDictSearcher(engdict):
		""" engdict = adLoader.anydict 
			영영, 영한 사전을 담고 있는 클래스.
			
		"""
		MyHandler.EngDictSearcher = engdict 


	@staticmethod
	def setExlistDictSearcher(exdict):
		"""
		exdict = AdSearch.AdSearcher
		예문목록을 가진 사전.
		"""	
		MyHandler.ExlistDictSearcher = exdict


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

			#print func, msg
			res = searchEngDict(MyHandler.EngDictSearcher, func, msg)
			self.request.send(res)

			res = searchExlistDict(MyHandler.ExlistDictSearcher, func, msg)
			self.request.send(res)

			break


def searchEngDict(EngDictSearcher, func, msg):
	res = ''
	try:
		res = EngDictSearcher.search(func, msg)
	except:
		print "ERROR in searching: %d %s" % (func, msg)
	return res


def searchExlistDict(ExlistDictSearcher, func, msg):
	org_stdout = sys.stdout

	output = cStringIO.StringIO()
	sys.stdout = output
	ExlistDictSearcher.query(msg)
	sys.stdout = org_stdout
	res = output.getvalue()
	output.close()
	return res



def main(portnum):
	myServer = SocketServer.TCPServer(('',port), MyHandler)
	myServer.allow_reuse_address = True
	myServer.serve_forever( )


if __name__=='__main__':
	import sys
	import os

	if len(sys.argv) > 1:
		if sys.argv[1]=="ALL":
			start = 'A'
			end = 'Z'
		else:
			start = end = sys.argv[1][0].upper()

	if len(sys.argv) >= 2:
		port = int(sys.argv[2])
	else:
		port = 8900

	print "=== PORT=%d\tLoading: %c ~ %c" % (port, start, end)

	### load Wordnet english dict, 한영 사전
	ADDIR = os.getenv("ANYDICT_HOME")

	AD = adLoader.anydict(
		ADDIR + "/data/wn17.html",
		ADDIR + "/data/webster/", 
		ADDIR + "/data/engdic/", 
		ADDIR + "/data/word.dict",
		ADDIR + "/data/hometopia.dict"
	)
	AD.load(start, end)
	AD.info()
	#AD.prn_anydictt()
	#AD.prn_edict()
	#AD.testit()

	### load 영어 예문
	ExSearch = AdSearch.AdSearcher()
	ExSearch.load(start, end)

	MyHandler.setEngDictSearcher(AD)
	MyHandler.setExlistDictSearcher(ExSearch)

	myServer = SocketServer.TCPServer(('',port), MyHandler)
	myServer.allow_reuse_address = True
	myServer.serve_forever( )

